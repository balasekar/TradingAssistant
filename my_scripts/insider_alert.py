"""
insider_alert.py
----------------
Flags recent insider trades at portfolio companies (MSFT + HUBS).
Run weekly.

Usage:
    python insider_alert.py
"""

from openbb import obb
from datetime import date, timedelta
import pandas as pd

TICKERS = ["MSFT", "HUBS"]
LOOKBACK_DAYS = 30


def main() -> None:
    since = (date.today() - timedelta(days=LOOKBACK_DAYS)).isoformat()
    print("\n" + "=" * 60)
    print(f"  Insider Trades since {since}")
    print("=" * 60)

    for tk in TICKERS:
        print(f"\n--- {tk} ---")
        try:
            df = obb.equity.ownership.insider_trading(tk).to_df()
            if "filing_date" in df.columns:
                df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
                recent = df[df["filing_date"] >= pd.Timestamp(since)]
            else:
                recent = df.head(5)

            if recent.empty:
                print("  (no insider trades in lookback window)")
                continue

            cols = [c for c in ["filing_date", "transaction_type", "shares", "value", "owner_name"] if c in recent.columns]
            print(recent[cols].head(10).to_string(index=False))
        except Exception as exc:
            print(f"  [WARN] {tk}: {exc}")
    print()


if __name__ == "__main__":
    main()
