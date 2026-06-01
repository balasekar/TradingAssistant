"""
macro_watch.py
--------------
Pulls the 4 macro indicators that most affect tech valuations.
Run monthly (or after every Fed meeting).

Usage:
    python macro_watch.py
"""

from openbb import obb

SERIES = {
    "Fed Funds Rate":  "FEDFUNDS",
    "10Y Treasury":    "DGS10",
    "Core CPI":        "CPILFESL",
    "Unemployment":    "UNRATE",
}


def main() -> None:
    print("\n" + "=" * 60)
    print("  Macro Watch  (tech-sensitive indicators, live FRED data)")
    print("=" * 60 + "\n")
    for name, sid in SERIES.items():
        try:
            df = obb.economy.fred_series(sid).to_df().tail(2)
            latest = df.iloc[-1, 0]
            prior = df.iloc[-2, 0] if len(df) > 1 else None
            arrow = "->" if prior is None else ("UP" if latest > prior else "DOWN" if latest < prior else "FLAT")
            print(f"  {name:18s} {sid:10s}  {latest:>8.3f}  ({arrow} from {prior})")
        except Exception as exc:
            print(f"  {name:18s} {sid:10s}  ERROR: {exc}")
    print("\nReminder: rising rates compress growth-tech P/E. Watch the 10Y.\n")


if __name__ == "__main__":
    main()
