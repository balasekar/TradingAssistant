"""
Moving Average Crossover Strategy Backtest — S&P 500
======================================================

Strategy:
    - Long when 50-day SMA > 200-day SMA ("golden cross")
    - Flat (cash) when 50-day SMA <= 200-day SMA ("death cross")
    - Signals lagged 1 bar to avoid look-ahead bias
    - No leverage, no shorts, no transaction costs modelled by default
      (toggle COST_BPS below to add a per-trade slippage/commission estimate).

Outputs:
    - Performance summary (CAGR, Vol, Sharpe, Max Drawdown, Hit Rate)
    - Comparison vs. Buy & Hold
    - Equity curve + drawdown chart (saved to PNG)

Run:
    pip install yfinance pandas numpy matplotlib
    python ma_crossover_backtest.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TICKER      = "^GSPC"     # S&P 500 index
LOOKBACK_Y  = 5           # years of history
SHORT_WIN   = 50          # fast SMA
LONG_WIN    = 200         # slow SMA
COST_BPS    = 0.0         # round-trip cost in basis points per signal flip (e.g. 2.0 = 2bps)
RISK_FREE   = 0.0         # annualized risk-free rate for Sharpe (set e.g. 0.04 for 4%)
TRADING_DAYS = 252


# ---------------------------------------------------------------------------
# 1. Data
# ---------------------------------------------------------------------------
def load_prices(ticker: str, years: int) -> pd.DataFrame:
    end = pd.Timestamp.today().normalize()
    start = end - pd.DateOffset(years=years)
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if df.empty:
        raise RuntimeError(f"No data returned for {ticker}")
    # yfinance can return a MultiIndex when downloading a single ticker — flatten it.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Close"]].rename(columns={"Close": "price"}).dropna()


# ---------------------------------------------------------------------------
# 2. Signals & strategy returns
# ---------------------------------------------------------------------------
def build_signals(prices: pd.DataFrame, short_win: int, long_win: int) -> pd.DataFrame:
    df = prices.copy()
    df["sma_short"] = df["price"].rolling(short_win).mean()
    df["sma_long"]  = df["price"].rolling(long_win).mean()

    # Raw position: 1 when fast > slow, else 0 (long/flat)
    df["position_raw"] = (df["sma_short"] > df["sma_long"]).astype(int)

    # Shift by 1 day — you can only act on the *next* bar after the signal forms.
    df["position"] = df["position_raw"].shift(1).fillna(0)

    df["ret"] = df["price"].pct_change().fillna(0)
    df["strat_ret_gross"] = df["position"] * df["ret"]

    # Transaction costs: charged whenever position changes.
    trades = df["position"].diff().abs().fillna(0)
    df["cost"] = trades * (COST_BPS / 10_000)
    df["strat_ret"] = df["strat_ret_gross"] - df["cost"]

    return df.dropna(subset=["sma_long"])  # drop warm-up period


# ---------------------------------------------------------------------------
# 3. Performance metrics
# ---------------------------------------------------------------------------
def equity_curve(returns: pd.Series, start_value: float = 1.0) -> pd.Series:
    return start_value * (1.0 + returns).cumprod()


def max_drawdown(eq: pd.Series) -> tuple[float, pd.Timestamp, pd.Timestamp]:
    """Returns (max_dd, peak_date, trough_date). max_dd is negative."""
    running_peak = eq.cummax()
    drawdown = eq / running_peak - 1.0
    trough = drawdown.idxmin()
    peak = eq.loc[:trough].idxmax()
    return float(drawdown.min()), peak, trough


def cagr(eq: pd.Series) -> float:
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    return (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1


def sharpe(returns: pd.Series, rf: float = 0.0) -> float:
    excess = returns - rf / TRADING_DAYS
    if excess.std() == 0:
        return 0.0
    return np.sqrt(TRADING_DAYS) * excess.mean() / excess.std()


def summary(name: str, returns: pd.Series) -> dict:
    eq = equity_curve(returns)
    dd, peak, trough = max_drawdown(eq)
    return {
        "Strategy":      name,
        "CAGR":          f"{cagr(eq) * 100:.2f}%",
        "Ann. Vol":      f"{returns.std() * np.sqrt(TRADING_DAYS) * 100:.2f}%",
        "Sharpe":        f"{sharpe(returns, RISK_FREE):.2f}",
        "Max Drawdown":  f"{dd * 100:.2f}%",
        "MDD Peak":      peak.strftime("%Y-%m-%d"),
        "MDD Trough":    trough.strftime("%Y-%m-%d"),
        "Final Equity":  f"{eq.iloc[-1]:.3f}x",
    }


# ---------------------------------------------------------------------------
# 4. Plotting
# ---------------------------------------------------------------------------
def plot_results(df: pd.DataFrame, out_path: str = "backtest_results.png") -> None:
    eq_strat = equity_curve(df["strat_ret"])
    eq_bh    = equity_curve(df["ret"])

    dd_strat = eq_strat / eq_strat.cummax() - 1
    dd_bh    = eq_bh    / eq_bh.cummax()    - 1

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True,
                              gridspec_kw={"height_ratios": [2, 1.2, 1]})

    # Price + MAs + position shading
    ax0 = axes[0]
    ax0.plot(df.index, df["price"],     label="S&P 500", color="black", lw=1)
    ax0.plot(df.index, df["sma_short"], label=f"{SHORT_WIN}d SMA", color="tab:blue", lw=1)
    ax0.plot(df.index, df["sma_long"],  label=f"{LONG_WIN}d SMA", color="tab:red",  lw=1)
    ax0.fill_between(df.index, df["price"].min(), df["price"].max(),
                     where=df["position"] == 1, alpha=0.08, color="green",
                     label="Long")
    ax0.set_title(f"{TICKER}: Price & SMA Crossover Signals")
    ax0.legend(loc="upper left"); ax0.grid(alpha=0.3)

    # Equity curves
    ax1 = axes[1]
    ax1.plot(eq_strat.index, eq_strat, label="MA Crossover", color="tab:blue", lw=1.4)
    ax1.plot(eq_bh.index,    eq_bh,    label="Buy & Hold",  color="gray",     lw=1.2)
    ax1.set_title("Equity Curve (growth of 1)")
    ax1.legend(loc="upper left"); ax1.grid(alpha=0.3)

    # Drawdown
    ax2 = axes[2]
    ax2.fill_between(dd_strat.index, dd_strat * 100, 0, color="tab:blue", alpha=0.4, label="Strategy DD")
    ax2.plot(dd_bh.index, dd_bh * 100, color="gray", lw=1, label="Buy & Hold DD")
    ax2.set_title("Drawdown (%)")
    ax2.set_ylabel("Drawdown %"); ax2.legend(loc="lower left"); ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    print(f"Chart saved to: {out_path}")


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"Loading {LOOKBACK_Y}y of {TICKER} ...")
    prices = load_prices(TICKER, LOOKBACK_Y)
    print(f"Loaded {len(prices)} bars: {prices.index[0].date()} -> {prices.index[-1].date()}")

    df = build_signals(prices, SHORT_WIN, LONG_WIN)

    rows = [
        summary(f"MA Crossover {SHORT_WIN}/{LONG_WIN}", df["strat_ret"]),
        summary("Buy & Hold", df["ret"]),
    ]
    results = pd.DataFrame(rows).set_index("Strategy")

    # Trade stats
    flips = int(df["position"].diff().abs().fillna(0).sum())
    pct_long = 100 * df["position"].mean()

    print("\n=== Performance Summary ===")
    print(results.to_string())
    print(f"\nSignal flips (entries+exits): {flips}")
    print(f"Time in market (long): {pct_long:.1f}%")
    if COST_BPS > 0:
        print(f"Transaction cost applied: {COST_BPS} bps per flip")

    plot_results(df)


if __name__ == "__main__":
    main()
