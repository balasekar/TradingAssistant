"""
screen_longterm_candidates.py
-----------------------------
Long-term quality compounders + dividend stalwarts pulled from
Morningstar / Sure Dividend / Motley Fool 2026 consensus.
Deliberately weighted away from US mega-cap tech to diversify
a concentrated MSFT+HUBS holder.

Pulls price, valuation, dividend, balance sheet via OpenBB / Yahoo.
NOT investment advice — see repo README.

Usage:
    python screen_longterm_candidates.py
"""

from __future__ import annotations
from openbb import obb
import pandas as pd

CANDIDATES = {
    # Quality compounders (non-tech-heavy)
    "TSM":   "TSMC — semis foundry monopoly",
    "RACE":  "Ferrari — luxury moat",
    "MSCI":  "MSCI — index licensing toll-road",
    "APH":   "Amphenol — industrial electronics",
    "EFX":   "Equifax — credit data duopoly",
    "SAP":   "SAP — EU enterprise software",
    # Dividend stalwarts (defensive / income)
    "ABBV":  "AbbVie — pharma, ~4% yield",
    "KO":    "Coca-Cola — Dividend King",
    "WMT":   "Walmart — consumer staples giant",
    "DUK":   "Duke Energy — regulated utility",
    "VZ":    "Verizon — telecom, ~6% yield",
    "SYK":   "Stryker — medical devices",
    # Sector diversifiers
    "BAESY": "BAE Systems — EU defence ADR",
    "SHW":   "Sherwin-Williams — paints/materials",
}


def fmt_money(x):
    try: x = float(x)
    except: return "n/a"
    if pd.isna(x): return "n/a"
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
        if abs(x) >= div: return f"{x/div:.1f}{unit}"
    return f"{x:.2f}"


def fmt_num(x, pct=False, dp=2):
    try: x = float(x)
    except: return "n/a"
    if pd.isna(x): return "n/a"
    return f"{x*100:.{dp}f}%" if pct else f"{x:.{dp}f}"


def pull(tk: str) -> dict:
    out = {"ticker": tk}
    try:
        q = obb.equity.price.quote(tk, provider="yfinance").to_df().iloc[0]
        out["price"] = q.get("last_price") or q.get("price")
        out["52w_low"] = q.get("year_low")
        out["52w_high"] = q.get("year_high")
        out["mcap"] = q.get("market_cap")
    except Exception as exc:
        out["q_err"] = type(exc).__name__
    try:
        m = obb.equity.fundamental.metrics(tk, provider="yfinance").to_df().iloc[0]
        for c in ("pe_ratio", "price_to_book", "dividend_yield",
                  "return_on_equity", "debt_to_equity",
                  "free_cash_flow_yield", "payout_ratio"):
            out[c] = m.get(c) if c in m.index else None
    except Exception as exc:
        out["m_err"] = type(exc).__name__
    return out


def main() -> None:
    print("\n" + "=" * 90)
    print("  Long-term Candidates Screen  (sector-diversified, non-MSFT/HUBS overlap)")
    print("=" * 90)
    rows = []
    for tk, desc in CANDIDATES.items():
        print(f"  fetching {tk:6s} ({desc})...", end=" ", flush=True)
        r = pull(tk); r["desc"] = desc
        rows.append(r)
        print("ok")

    df = pd.DataFrame(rows).set_index("ticker")

    print("\n--- Valuation + Income ---\n")
    print(f"  {'TICK':6s} {'PRICE':>8s} {'52w-pos':>8s} {'P/E':>7s} {'P/B':>6s} "
          f"{'YIELD':>7s} {'PAYOUT':>7s} {'ROE':>7s} {'D/E':>7s}")
    print(f"  {'-'*6} {'-'*8} {'-'*8} {'-'*7} {'-'*6} {'-'*7} {'-'*7} {'-'*7} {'-'*7}")
    for tk, r in df.iterrows():
        try:
            p, lo, hi = float(r["price"]), float(r["52w_low"]), float(r["52w_high"])
            pos = f"{(p-lo)/(hi-lo)*100:.0f}%"
        except: pos = "n/a"
        print(f"  {tk:6s} {fmt_num(r.get('price')):>8s} {pos:>8s} "
              f"{fmt_num(r.get('pe_ratio')):>7s} {fmt_num(r.get('price_to_book')):>6s} "
              f"{fmt_num(r.get('dividend_yield'), pct=True):>7s} "
              f"{fmt_num(r.get('payout_ratio'), pct=True):>7s} "
              f"{fmt_num(r.get('return_on_equity'), pct=True):>7s} "
              f"{fmt_num(r.get('debt_to_equity')):>7s}")


if __name__ == "__main__":
    main()
