"""
portfolio_health_check.py
-------------------------
Pulls live fundamentals for the user's concentrated tech holdings
(100 MSFT + 100 HUBS) via OpenBB. Run weekly.

Usage:
    python portfolio_health_check.py
"""

from openbb import obb
import pandas as pd

TICKERS = ["MSFT", "HUBS"]
COLS = ["pe_ratio", "price_to_book", "dividend_yield", "debt_to_equity", "return_on_equity"]


def main() -> None:
    print("\n" + "=" * 60)
    print("  Portfolio Health Check  (live data via OpenBB / Yahoo)")
    print("=" * 60)

    rows = []
    for tk in TICKERS:
        try:
            df = obb.equity.fundamental.metrics(tk, provider="yfinance").to_df()
            row = {"ticker": tk}
            for c in COLS:
                row[c] = df[c].iloc[0] if c in df.columns and not df.empty else None
            rows.append(row)
        except Exception as exc:
            print(f"  [WARN] {tk}: {exc}")
            rows.append({"ticker": tk, "error": str(exc)})

    out = pd.DataFrame(rows).set_index("ticker")
    print("\n" + out.to_string())

    print("\nQuick read:")
    for tk, r in out.iterrows():
        pe = r.get("pe_ratio")
        dy = r.get("dividend_yield")
        pe_str = f"P/E {pe:.1f}" if isinstance(pe, (int, float)) and pd.notna(pe) else "P/E n/a"
        dy_str = f"yield {dy*100:.2f}%" if isinstance(dy, (int, float)) and pd.notna(dy) else "no dividend"
        print(f"  {tk:6s}  {pe_str:12s}  {dy_str}")
    print()


if __name__ == "__main__":
    main()
