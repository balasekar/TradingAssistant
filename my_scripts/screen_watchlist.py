"""
screen_watchlist.py
-------------------
Quick per-ticker screen for a watchlist of candidate buys.
Pulls price, valuation, recent performance, and headlines via OpenBB / Yahoo.

NOT investment advice — see repo README disclaimers.

Usage:
    python screen_watchlist.py
"""

from __future__ import annotations

from openbb import obb
import pandas as pd

TICKERS = [
    "ONDS",  # Ondas Holdings
    "RGTI",  # Rigetti Computing
    "RKLB",  # Rocket Lab
    "IREN",  # Iris Energy
    "ASTS",  # AST SpaceMobile
    "TE",    # (ambiguous — may not resolve)
    "OSCR",  # Oscar Health
    "NBIS",  # Nebius Group
    "OSS",   # One Stop Systems
    "RDW",   # Redwire
]


def safe(fn, default=None):
    try:
        return fn()
    except Exception as exc:
        return f"ERR:{type(exc).__name__}"


def quote(tk: str) -> dict:
    out = {"ticker": tk}
    # Current price + day change
    try:
        q = obb.equity.price.quote(tk, provider="yfinance").to_df()
        if not q.empty:
            r = q.iloc[0]
            out["price"] = r.get("last_price") or r.get("price")
            out["change_pct"] = r.get("change_percent")
            out["mcap"] = r.get("market_cap")
            out["52w_low"] = r.get("year_low")
            out["52w_high"] = r.get("year_high")
            out["volume"] = r.get("volume")
    except Exception as exc:
        out["quote_err"] = f"{type(exc).__name__}: {exc}"
    # Fundamentals
    try:
        m = obb.equity.fundamental.metrics(tk, provider="yfinance").to_df()
        if not m.empty:
            r = m.iloc[0]
            for c in ("pe_ratio", "price_to_sales", "price_to_book",
                      "return_on_equity", "debt_to_equity", "dividend_yield"):
                if c in m.columns:
                    out[c] = r.get(c)
    except Exception as exc:
        out["fund_err"] = f"{type(exc).__name__}"
    return out


def headlines(tk: str, limit: int = 3) -> list[str]:
    try:
        n = obb.news.company(symbol=tk, limit=limit, provider="yfinance").to_df()
        if "title" in n.columns:
            return n["title"].head(limit).tolist()
    except Exception as exc:
        return [f"news err: {type(exc).__name__}"]
    return []


def fmt_money(x) -> str:
    try:
        x = float(x)
    except Exception:
        return "n/a"
    if pd.isna(x):
        return "n/a"
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(x) >= div:
            return f"{x/div:.2f}{unit}"
    return f"{x:.2f}"


def fmt_num(x, pct: bool = False, dp: int = 2) -> str:
    try:
        x = float(x)
    except Exception:
        return "n/a"
    if pd.isna(x):
        return "n/a"
    return f"{x*100:.{dp}f}%" if pct else f"{x:.{dp}f}"


def main() -> None:
    print("\n" + "=" * 78)
    print("  Watchlist Screen  (live via OpenBB / Yahoo)")
    print("=" * 78)

    rows = []
    news_by_tk = {}
    for tk in TICKERS:
        print(f"  fetching {tk} ...", end=" ", flush=True)
        rows.append(quote(tk))
        news_by_tk[tk] = headlines(tk, limit=3)
        print("ok")

    df = pd.DataFrame(rows).set_index("ticker")

    # Pretty per-row print
    print("\n--- Quote / Valuation ---\n")
    for tk, r in df.iterrows():
        price = fmt_num(r.get("price"))
        chg = fmt_num(r.get("change_pct"), pct=False, dp=2)
        mcap = fmt_money(r.get("mcap"))
        lo52 = fmt_num(r.get("52w_low"))
        hi52 = fmt_num(r.get("52w_high"))
        pe = fmt_num(r.get("pe_ratio"))
        ps = fmt_num(r.get("price_to_sales"))
        roe = fmt_num(r.get("return_on_equity"), pct=True)
        de = fmt_num(r.get("debt_to_equity"))
        dy = fmt_num(r.get("dividend_yield"), pct=True)

        # Position in 52w range
        pos = "n/a"
        try:
            p = float(r.get("price")); lo = float(r.get("52w_low")); hi = float(r.get("52w_high"))
            if hi > lo:
                pos = f"{(p - lo) / (hi - lo) * 100:.0f}%"
        except Exception:
            pass

        print(f"  {tk:6s}  px {price:>9s}  ({chg:>6s}%)  mcap {mcap:>8s}  "
              f"52w {lo52}-{hi52} (pos {pos})")
        print(f"          P/E {pe:>8s}  P/S {ps:>6s}  ROE {roe:>8s}  D/E {de:>6s}  yld {dy:>7s}")
        if r.get("quote_err"):
            print(f"          [WARN] quote: {r['quote_err']}")
        if r.get("fund_err"):
            print(f"          [WARN] fundamentals: {r['fund_err']}")

    # Headlines
    print("\n--- Recent headlines ---\n")
    for tk in TICKERS:
        print(f"  {tk}:")
        items = news_by_tk.get(tk, [])
        if not items:
            print("    (no headlines)")
        for h in items:
            print(f"    - {h}")
        print()


if __name__ == "__main__":
    main()
