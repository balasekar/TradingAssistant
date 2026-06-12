# Grok Trading Prompts (Elora Khatun thread)

> 7 short, Grok-focused trading prompts from [@elora_khatun](https://x.com/elora_khatun). Lighter and more retail-friendly than the two Claude threads in this folder. Most prompts overlap with the AI Panda set — kept here for completeness and because Grok's live X/web access changes which prompts are practically useful.

## Source

- **Author:** Elora khatun ([@elora_khatun](https://x.com/elora_khatun))
- **Thread head:** <https://x.com/elora_khatun/status/2064975714252914849>
- **Posted:** 2026-06-11
- **Fetched:** 2026-06-12 (via `nitter.tiekoetter.com`)
- **OP:** "GROK IS A STOCK TRADING GENIUS. MOST PEOPLE HAVE NO IDEA HOW TO USE IT. HERE ARE 7 PROMPTS TO UNLOCK STOCK TRADING AUTOMATION:"

## Quick reference

| # | Title | Overlaps with |
|---|---|---|
| 1 | Trading Ideas Generator | AI Panda #7 (Technical Analyst) |
| 2 | Automated Technical Analyst | AI Panda #7 |
| 3 | News to Trading Converter | AI Panda #6 (Sentiment Tracker) |
| 4 | Strategy Backtester | AI Panda #5, Ryan Hart #2 |
| 5 | Portfolio Risk Manager | AI Panda #12 (Bear Market Shield), Ryan Hart #3 |
| 6 | Trading Journal Analyzer | AI Panda #16 (Trade Journal Analyst) — near-duplicate |
| 7 | Fully Automated Trading Plan | **Unique** — daily timestamped checklist |

> **Why Grok specifically?** Grok has live X/web access baked in, so prompts that say "scan today's market" or "summarize the latest news" actually work without you pasting in the data. Claude needs the data pasted. That's the real difference — not the prompts themselves.

---

## Prompt 1 — Trading Ideas Generator

```
Scan today's market and generate 5 high-probability trading setups
for [insert stock/index/sector]. Include entry price, exit targets,
stop-loss, and risk/reward ratio. Explain why each setup works
based on technical and fundamental factors.
```

## Prompt 2 — Automated Technical Analyst

```
Analyze [insert action/ticker] using daily and weekly charts.
Break down support/resistance levels, trend lines, moving averages,
and momentum indicators. Provide a step-by-step trading signal
(Buy/Hold/Sell) with justification.
```

## Prompt 3 — News to Trading Converter

```
Summarize the latest news on [insert company/sector] and translate
them into trading implications. Provide possible short- and long-term
effects, expected price movement range, and recommended positioning.
```

## Prompt 4 — Strategy Backtester

```
Perform a backtest of [insert trading strategy: e.g., moving average
crossover, RSI divergence] on [insert stock/index] over the last
[insert time period]. Present win rate, profit factor, maximum
drawdown, and improvements to increase the edge.
```

## Prompt 5 — Portfolio Risk Manager

```
Analyze my portfolio: [insert tickers and % allocation]. Highlight
weak points, overexposure, and hidden correlations. Suggest a
rebalancing adjusted to risk and hedging strategies to protect
against a 20% market downturn.
```

## Prompt 6 — Trading Journal Analyzer

```
Review my last 20 trades: [insert trades with entry/exit points
and results]. Identify recurring mistakes, missed opportunities,
and behavioral biases. Give me 3 personalized rules to immediately
improve consistency in my trading.
```

## Prompt 7 — Fully Automated Trading Plan

```
Design a daily trading plan for [insert market/asset]. Include
pre-market scanning, opening strategy, mid-session adjustments,
and closing strategy. Deliver it as a checklist with timestamps
that I can follow like a professional trader.
```

---

## Mapping to this repo's 3-tool stack

The unique value here is **prompts #1, #2, #3** — when fed into Grok (or any LLM with live web access), they substitute for the data-pull step you'd otherwise do with OpenBB. Useful when you want a fast second opinion without firing up `LAUNCH_OpenBB.bat`.

| Prompt | When to use | Notes |
|---|---|---|
| **#1 Trading Ideas** | Looking for *new* candidates to add to `screen_watchlist.py` | Run via Grok so it can scan today's tape. Then validate any returned ticker with `obb.equity.fundamental.metrics(...)` before doing anything. |
| **#2 Technical Analyst** | At the TradingView chart on MSFT or HUBS | Same intent as AI Panda #7 — pick whichever phrasing you like. |
| **#3 News to Trading Converter** | After `insider_alert.py` or before earnings | Strong fit for Grok because of live news access. With Claude, paste headlines from `obb.news.company(...)`. |
| **#4 Strategy Backtester** | One-off rule sketch before writing real code | LLM-only backtests are unreliable — for anything you'll act on, use `examples/ma_crossover_backtest.py` and the Ryan Hart #2 (Renaissance) prompt instead. |
| **#5 Portfolio Risk Manager** | After `portfolio_health_check.py` | Paste the output table as your `[insert tickers and % allocation]`. The "hedging strategies to protect against a 20% downturn" output overlaps with AI Panda #12 — pick one. |
| **#6 Trading Journal Analyzer** | Functionally identical to AI Panda #16 | Use whichever phrasing is cleaner. There is still no journaling script in `my_scripts/`. |
| **#7 Fully Automated Trading Plan** | One-time exercise to build a personal daily checklist | The output is a routine, not a recurring prompt. Once you have a checklist you like, save it (don't keep re-asking). The repo's `MORNING_ROUTINE.bat` is the long-term home for that checklist. |

**Out of scope:** none — all 7 are at least vaguely applicable. The thread's real limitation is depth (these prompts are one-liners; the Ryan Hart prompts in `claude-quant-desk-prompts.md` produce much more rigorous output for the same questions).

## Caveats

- **"Scan today's market" only works in LLMs with live tools** (Grok via X/web, ChatGPT with browsing on). In Claude without tools, you must paste the data yourself.
- **#4 (backtest) without code is hallucination.** Any "win rate / max drawdown" the LLM gives you without writing and running real Python is invented. Cross-check with `examples/ma_crossover_backtest.py`.
- **#5 (risk manager) is the weakest of the three risk prompts in this folder.** Prefer Ryan Hart #3 (Two Sigma) if you want a real framework; use this one only for a quick gut-check.
- Standard repo disclaimers apply — see `README.md`.
