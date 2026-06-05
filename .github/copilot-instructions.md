# TradingAssistant — Copilot instructions

Personal, Windows-only research stack that bolts together three independent free tools. There is no build, no test suite, and no linter — work here is mostly small Python scripts and `.bat` glue.

## The 3-tool stack (only one lives in this repo)

This repo is *glue*, not implementation. It composes three external tools:

1. **`claude-trading-skills/`** — third-party repo cloned in-place (`git clone https://github.com/tradermonty/claude-trading-skills`). **Gitignored.** Provides ~200 Python skills under `claude-trading-skills/skills/<skill-name>/scripts/`.
2. **TradingView Desktop** — installed via `winget` / `INSTALL_TradingView.bat`. Not invoked from code; only opened via `start ""` from `MORNING_ROUTINE.bat`.
3. **OpenBB Platform** — installed into a local venv at `openbb-env/`. **Gitignored.** All Python here imports `from openbb import obb`.

The user-authored code is just `my_scripts/`, `examples/`, and the three `.bat` files at the root. When asked to "add a script", default to `my_scripts/` and follow its conventions.

## Environment

- **Windows only.** All entry points are `.bat`. Paths use backslashes.
- **Python 3.11 x64 (not ARM64).** OpenBB's transitive deps (`aiohttp`, `cachebox`, `pydantic-core`) have no ARM64 wheels and will try to compile via Rust/maturin. The venv is intentionally built with x64 Python running under ARM emulation. Do not "fix" this by switching to ARM Python.
- **Venv path:** `openbb-env\Scripts\python.exe`. `MORNING_ROUTINE.bat` hardcodes this — any new Python entry point should be invoked the same way.
- **API keys** live in `.env` / `api_keys.txt` (gitignored). Default provider is Yahoo (`provider="yfinance"`) because it's keyless; FMP/Polygon/Alpha Vantage are optional upgrades.

## Running things

```powershell
# Daily pipeline (chains breadth → uptrend → exposure-coach → portfolio_health_check)
.\MORNING_ROUTINE.bat

# Interactive OpenBB shell with obb preloaded
.\LAUNCH_OpenBB.bat

# One-off script
.\openbb-env\Scripts\python.exe my_scripts\portfolio_health_check.py
```

No `pytest`, no CI. "Verifying a change" means running the script and reading the printed table.

## Conventions

- **Scripts are self-contained CLIs.** Module docstring at top with `Usage:` block, constants in ALL_CAPS at module level, single `main()` function, `if __name__ == "__main__": main()`. See `my_scripts/portfolio_health_check.py` for the canonical shape.
- **Portfolio tickers are hardcoded to `["MSFT", "HUBS"]`.** The repo is opinionated for one user holding a concentrated grant. Don't generalize this without being asked.
- **OpenBB call shape:** `obb.<domain>.<...>(ticker, provider="yfinance").to_df()`. Always wrap in `try/except` and print `[WARN] {ticker}: {exc}` on failure — rate limits and missing fields are routine, scripts must keep going.
- **Output is stdout tables** (`pandas.DataFrame.to_string()`), not files. `MORNING_ROUTINE.bat` captures structured output from claude-trading-skills via its own `--output-dir` flags, not from `my_scripts/`.
- **Reports are private.** Anything written under `reports/` or `claude-trading-skills/reports/` is gitignored. Never commit a report, briefing, or anything containing live portfolio data.
- **`.bat` files use `setlocal` + `%~dp0`** for the script directory and `pause` at the end so a double-click leaves the window open. Match that pattern for new launchers.

## What not to do

- Don't add the gitignored third-party folders (`openbb-env/`, `claude-trading-skills/`, `TradingView_Installer/`, `reports/`) to git.
- Don't introduce a test framework, linter, or package manager (`requirements.txt`, `pyproject.toml`) unless explicitly asked — the repo deliberately has none.
- Don't port `.bat` files to PowerShell or bash; the double-click workflow is the point.
- Don't add order-routing or broker integration. The whole stack is research-only by design (see README "Honest limitations" and Disclaimers).
