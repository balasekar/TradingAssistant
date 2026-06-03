---
name: researching-stocks-with-tradingassistant
description: >
  Use when Bala asks to evaluate one or more stocks, build a watchlist screen,
  decide whether to deploy capital today, or design a long-term investing
  strategy. Drives the TradingAssistant repo (claude-trading-skills + OpenBB)
  for the market regime + per-ticker data, layers Irish tax rules and Bala's
  existing concentration (MSFT + HUBS), and ends with a plain-English plan.
tags: [investing, trading, tradingassistant, openbb, ireland, livesite-style]
usage: >
  Triggers: "is X worth buying", "screen these tickers", "what should I do
  with €N", "long-term picks", "should I invest today", "evaluate this
  watchlist", any request mentioning TradingAssistant / OpenBB / claude-trading-skills.
---

# Researching stocks with the TradingAssistant repo

End-to-end skill for Bala's home investing flow. Drives the three tools in his `TradingAssistant` repo and produces decision-grade output without giving "advice" (always caveat per the repo's README disclaimers).

## When this fires

- "Are these tickers worth buying?"
- "Where should I put €X?"
- "What does the market look like today, should I deploy cash?"
- "Long-term picks for next 5–10 years"
- "Build me a screen / watchlist analysis"

## Persona constraints to always honour

These are stable Bala-specific facts. **Never produce a plan that contradicts them:**

| Constraint | Why it matters |
|---|---|
| **Lives in Dublin, Ireland** | Individual stocks: 33% CGT + €1,270/yr exemption. UCITS ETFs (incl. VWCE/SXR8): 41% Exit Tax + **8-year deemed disposal**. For long-term holds, individual stocks beat ETFs on tax. |
| **Already holds 100 MSFT + 100 HUBS** | He is concentrated in US tech (mega + small-mid cap SaaS). New positions should diversify, not double down. |
| **EUR base currency** | USD-listed positions add FX volatility. Prefer EUR-listed equivalents when both exist (e.g., SAP on XETRA, RACE on Borsa Italiana, BAESY on LSE). |
| **Not investment advice** | Always close with the repo's standard disclaimer. Frame as "what the tools report" not "what to do". |

## The 4-phase pipeline

```
Phase 0: Bootstrap   →   Phase 1: Regime   →   Phase 2: Per-ticker   →   Phase 3: Strategy
(only if missing)        (Tool 1)              (Tool 3)                   (synthesis + plan)
```

### Phase 0 — Environment bootstrap (skip if already done)

Repo path: `C:\src\copilot-worktrees\TradingAssistant\<worktree>\` (varies per session) **or** `%USERPROFILE%\OneDrive\Documents\AISidekick\TradingAssistant`.

Check first:

```powershell
$root = "<repo-root>"
Test-Path "$root\openbb-env\Scripts\python.exe"
Test-Path "$root\claude-trading-skills\skills"
```

If missing, install per README in this exact order (some steps take ~5-10 min, queue them in background and continue with other prep):

```powershell
# 1. Python 3.11 x64 (NOT ARM — OpenBB deps have no ARM64 wheels)
winget install --id Python.Python.3.11 --architecture x64 --silent --accept-package-agreements --accept-source-agreements

# 2. Venv using the x64 python explicitly
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m venv "$root\openbb-env"

# 3. OpenBB (slow — ~5-10 min, run async)
& "$root\openbb-env\Scripts\python.exe" -m pip install openbb --quiet

# 4. claude-trading-skills clone (fast)
git clone --depth 1 https://github.com/tradermonty/claude-trading-skills "$root\claude-trading-skills"
```

Smoke test once OpenBB is ready:

```powershell
& "$root\openbb-env\Scripts\python.exe" -c "from openbb import obb; print(obb.equity.price.quote('MSFT', provider='yfinance').to_df()[['last_price']])"
```

### Phase 1 — Market regime read (Tool 1)

**Always run this first.** It tells you whether to deploy aggressively or hold cash. Three scripts chained:

```powershell
$TODAY   = (Get-Date).ToString("yyyy-MM-dd")
$REPORTS = "$root\claude-trading-skills\reports\daily-$TODAY"
$PY      = "$root\openbb-env\Scripts\python.exe"
New-Item -ItemType Directory -Force -Path $REPORTS | Out-Null
$env:PYTHONIOENCODING="utf-8"; $env:PYTHONUTF8="1"

# 1/3 Breadth
& $PY "$root\claude-trading-skills\skills\market-breadth-analyzer\scripts\market_breadth_analyzer.py" `
    --detail-url  "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" `
    --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv" `
    --output-dir  $REPORTS

# 2/3 Uptrend
& $PY "$root\claude-trading-skills\skills\uptrend-analyzer\scripts\uptrend_analyzer.py" --output-dir $REPORTS

# 3/3 Exposure-Coach (synthesis)
$b = Get-ChildItem "$REPORTS\market_breadth_*.json" | Sort LastWriteTime -Desc | Select -First 1
$u = Get-ChildItem "$REPORTS\uptrend_analysis_*.json" | Sort LastWriteTime -Desc | Select -First 1
& $PY "$root\claude-trading-skills\skills\exposure-coach\scripts\calculate_exposure.py" `
    --breadth $b.FullName --uptrend $u.FullName --output-dir $REPORTS
```

**Read the result this way:**

| Coach verdict | What it means for a plan |
|---|---|
| `NEW_ENTRY_ALLOWED` | Deploy normally. Lump-sum acceptable. |
| `REDUCE_ONLY` | **Tranche the deployment** (e.g., 40% now / 35% in 3w / 25% in 6-8w). Anchor on names near 52w lows. |
| `CASH_PRIORITY` | Hold cash. Only buy if user insists, and only highest-conviction defensive names. |

Confidence is often LOW in this repo because optional paid inputs (FMP etc.) aren't wired in — call this out so the user knows the coach is reading a partial picture.

### Phase 2 — Per-ticker screen (Tool 3, OpenBB)

Two reusable scripts already exist in `my_scripts/`:

| Script | Purpose | When |
|---|---|---|
| `screen_watchlist.py` | Speculative watchlist screen — price, 52w range, P/E, ROE, D/E, dividend yield, recent headlines | User pastes a list of tickers and asks "are these worth buying" |
| `screen_longterm_candidates.py` | Quality compounder / dividend stalwart screen — same metrics, curated `CANDIDATES` dict, sector-diversified | User asks "what should I buy for long-term" |

To screen a new list, **edit the `TICKERS` (or `CANDIDATES`) constant at the top** and re-run:

```powershell
& "$root\openbb-env\Scripts\python.exe" "$root\my_scripts\screen_watchlist.py"
```

Both follow the repo's script convention (module docstring with `Usage:`, ALL_CAPS constants, single `main()`).

**Interpreting the screen output — the key columns:**

| Column | Bull signal | Bear signal | Why |
|---|---|---|---|
| **52w position** | < 30% | > 80% | Coach in `REDUCE_ONLY` → buy on weakness, not at highs |
| **ROE** | > 15% positive | Negative | Profitable vs cash-burning |
| **D/E** | < 1.0 | > 1.0 (esp. > 5) | Leverage = fragility under rate/liquidity shocks |
| **P/E** | < 25 for quality | n/a or > 100 | n/a usually means no earnings; >100 is priced-for-perfection |
| **Dividend yield** | 2-6% sustainable | > 7% (yield trap?) or payout > 100% | High yield often = price drop signal |

### Phase 3 — Strategy synthesis & plan

Combine Phase 1 regime + Phase 2 screen + persona constraints. Always present **both** a technical analysis section **and** a plain-English section. Bala explicitly asks for the layman version most sessions.

Strategy template:

1. **Diversification filter** — strike anything that overlaps MSFT (mega-cap US tech) or HUBS (US SaaS). Bias toward sectors he doesn't own: healthcare, consumer staples, utilities, industrials, EU/Asia geographies.
2. **Tranching schedule** — if coach says `REDUCE_ONLY`, default to 40/35/25 over 6-8 weeks. Anchor tranche 1 on the names lowest in their 52w range.
3. **EUR-listed substitutions** — for any USD-listed pick that has an EUR cross-listing, mention it. Saves him 0.10-0.50% FX fees per trade.
4. **Circuit breakers** — pause remaining tranches if coach moves to `CASH_PRIORITY`, breadth < 30, or a single position grows > 40% of the basket.
5. **Tax footnotes** — remind about the €1,270 CGT exemption (harvest annually) and that individual stocks beat UCITS ETFs for long-term Irish holders.

## Output formatting

- Use **emoji-headed sections** (📊 📋 🎯 ⚠️) — Bala's existing reports use this style.
- Lead with a one-paragraph TL;DR.
- Always end with a Markdown table that lists positions, EUR amounts, and tranches — he wants something he can execute against.
- **Always close with the README disclaimer**: "Educational only. None of this is investment advice."

## Saving reports (always-save, config-driven)

**Always save every plan/analysis you produce in this skill.** Don't ask first — Bala has standardised on persistent output. Defaults are loaded from the sibling config file:

```
~/.copilot/skills/researching-stocks-with-tradingassistant/config.json
```

Read these keys at the start of every run:

| Key | Default | Meaning |
|---|---|---|
| `report_output_dir` | `C:\Users\bgnanasekar\OneDrive - Microsoft\Documents\AISidekick\Trading` | Where to write the report. Create the folder if missing. |
| `report_filename_pattern` | `{date}_investing_{slug}.md` | `{date}` = `YYYY-MM-DD`, `{slug}` = short kebab-case title (≤ 6 words). |
| `always_save_reports` | `true` | Master switch. If `false`, fall back to opt-in behaviour. |
| `default_tranche_split_pct` | `[40, 35, 25]` | Used when coach says `REDUCE_ONLY`. |
| `default_tranche_intervals_weeks` | `[0, 3, 6]` | Weeks-from-today for each tranche. |
| `regime_circuit_breaker_breadth_below` | `30` | If breadth drops below this, pause remaining tranches. |
| `regime_circuit_breaker_coach_verdict` | `CASH_PRIORITY` | If coach hits this, pause remaining tranches. |
| `existing_holdings_to_avoid_overlap` | `[MSFT, HUBS]` | Strike any candidate that overlaps these themes. |
| `preferred_eur_listings` | dict | If a USD pick has an EUR cross-listing here, surface it. |

**How to read the config from PowerShell:**

```powershell
$cfg = Get-Content "$env:USERPROFILE\.copilot\skills\researching-stocks-with-tradingassistant\config.json" -Raw | ConvertFrom-Json
$outDir = $cfg.report_output_dir
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$slug = "longterm-basket"   # derive per session
$fname = $cfg.report_filename_pattern.Replace("{date}", (Get-Date).ToString("yyyy-MM-dd")).Replace("{slug}", $slug)
$report | Out-File -FilePath (Join-Path $outDir $fname) -Encoding utf8
```

**Filename examples:**
- `2026-06-03_investing_longterm-basket.md`
- `2026-06-03_investing_watchlist-spec-10.md`
- `2026-06-03_investing_morning-regime.md`

**Always tell the user where the report was saved** (full path) at the end of the response.

**To change behaviour permanently** (e.g., new save path, different tranche split), edit `config.json` — never hard-code values in this skill or in scripts.

## Common gotchas (UPDATE as you find new ones)

- **OpenBB needs Python 3.11 x64** — never ARM64. ARM-Python triggers a Rust/maturin compile that fails. The venv must be built with the x64 interpreter at `%LOCALAPPDATA%\Programs\Python\Python311\python.exe`.
- **`dividend_yield` from yfinance is already in percent**, not a fraction. Display formatters that do `value * 100` will double-scale (e.g., VZ shows "591%" but the real yield is 5.91%). When reading raw output, divide by 100.
- **`obb.equity.price.quote()` often returns `n/a` for `market_cap`, `change_percent`, `volume`** via yfinance — don't rely on those fields, use `to_df()` from `obb.equity.fundamental.metrics()` for hard numbers.
- **`exposure-coach` confidence is almost always LOW** because optional paid inputs (`regime`, `top_risk`, `institutional`, `sector`, `theme`, `ftd`) aren't wired in. Call this out so the user understands the verdict is partial.
- **Headlines via `obb.news.company(symbol=..., provider="yfinance")`** — the `symbol=` kwarg is required (positional `tk` raises a deprecation warning in OpenBB 1.6+).
- **Reports under `claude-trading-skills/reports/` are gitignored** and contain live portfolio data. Never push them, never paste full report contents into external systems.
- **Worktree paths vary** — the repo lives at `C:\src\copilot-worktrees\TradingAssistant\<worktree-name>\` and the worktree name changes per session. Always check `pwd` / `git rev-parse --show-toplevel` first.
- **Tickers that look standard can be ambiguous** — `TE` resolved to T1 Energy (small-cap solar, near-term euphoria), NOT TE Connectivity (which is `TEL`). Always confirm via the OpenBB `quote()` output before reasoning about a name.

## Learnings log

Append to this section every session that yields a new insight. Format: `YYYY-MM-DD — finding — action to incorporate next time`.

- **2026-06-03** — First end-to-end run. Confirmed bootstrap-from-empty works in ~10 min (Python winget install + venv + `pip install openbb` + claude-trading-skills clone). Regime came back `REDUCE_ONLY` so plan defaulted to 40/35/25 tranching. EUR-listed substitutions for SAP (XETRA) and RACE (Borsa Italiana) were well-received. → Codified the persona constraints, gotchas, and tranching defaults into this skill.
- **2026-06-03** — Watchlist screen of 10 speculative tickers (ONDS/RGTI/RKLB/IREN/ASTS/TE/OSCR/NBIS/OSS/RDW) revealed 7/10 sat above 70% of 52w range, 8/10 cash-burning, 4 with extreme leverage. Confirms that "low in 52w range + positive ROE + D/E < 5" is a strong heuristic filter to apply automatically in the synthesis step. → Add an explicit "framework verdict" column to the screener output in the next iteration.
- **2026-06-03** — User explicitly asked for a "plain English plan" after the technical version. → Layperson section is now part of the default output template, not an opt-in.
- **2026-06-03** — User asked to always persist outputs and made the save path configurable. → Introduced `config.json` next to this SKILL.md. Default save path is `C:\Users\bgnanasekar\OneDrive - Microsoft\Documents\AISidekick\Trading`. `always_save_reports: true`. Every run must write the final report there and report the full path back to the user.

## Related files in the repo

- `my_scripts/portfolio_health_check.py` — daily portfolio fundamentals (MSFT + HUBS hardcoded)
- `my_scripts/macro_watch.py` — monthly macro indicators (Fed funds, 10Y, CPI, unemployment)
- `my_scripts/insider_alert.py` — weekly insider trades for portfolio names
- `my_scripts/screen_watchlist.py` — speculative watchlist screen (this skill)
- `my_scripts/screen_longterm_candidates.py` — quality-compounder screen (this skill)
- `MORNING_ROUTINE.bat` — orchestrates Phase 1 + portfolio health check daily
- `.github/copilot-instructions.md` — repo conventions

## Disclaimer (paste verbatim at the end of every plan)

> **Educational only.** None of this is investment advice. The data is real; interpreting it for your tax, risk, and time-horizon is your job. AI tooling makes mistakes — spot-check outputs against your broker's data before acting. Past patterns ≠ future outcomes.
