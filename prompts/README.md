# prompts/

Curated, attributed prompts that fit this repo's research-only workflow.

Each file documents:

- **Source** — original URL + author + date
- **Prompt(s)** — verbatim text, with `[PLACEHOLDERS]` left untouched
- **How they fit the 3-tool stack** — a table mapping each prompt to a trigger in `MORNING_ROUTINE.bat` output or in one of the `my_scripts/` scripts

> Use these with a general-purpose chat LLM (Claude, ChatGPT, etc.). They are *not* part of `MORNING_ROUTINE.bat` and do not execute Python — they are conversation starters that you paste into a chat after looking at the morning briefing.

## Current files

- `claude-trading-prompts.md` — 16 "hedge fund manager" personas from [@AIPandaX](https://x.com/AIPandaX) (Mar 2026). Short, tactical prompts (Portfolio Architect, Risk Manager, Options Strategist, etc.) mapped to triggers in the daily routine.
- `claude-quant-desk-prompts.md` — 15 long-form "Wall Street desk" personas from [@thisdudelikesAI](https://x.com/thisdudelikesAI) (Mar 2026). Heavyweight scaffolding prompts (Goldman strategy memo, Renaissance backtest engine, Bridgewater macro framework) — best as one-off learning projects, not daily triggers.
- `grok-trading-prompts.md` — 7 short Grok-focused prompts from [@elora_khatun](https://x.com/elora_khatun) (Jun 2026). Most overlap with the AI Panda set; the unique value is in prompts that depend on Grok's live X/web access (scan-the-market, news-to-trade).
