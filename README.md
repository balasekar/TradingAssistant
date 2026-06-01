# TradingAssistant — an amateur's 3-tool stack

> A free, AI-augmented trading research environment built for someone holding **a concentrated equity grant** (in my case: 100 MSFT + 100 HUBS as an employee). Designed to give you the same daily decision pipeline a junior analyst at a hedge fund would follow, in ~25 minutes a day, for **$0**.

---

## Why this exists

If you got equity from your employer, you have one big problem and one little one:

- **Big problem:** you are *concentrated* in a single stock (and probably a single sector) with no diversification strategy.
- **Little problem:** every "trading tool" on the internet either costs $300/mo (Bloomberg, FactSet), wants to sell you a course, or is built for active day-traders — not for someone who wants to make 2-3 deliberate decisions a quarter.

This repo bolts together **three free tools** that, when used together, replicate ~80% of what a professional desk does:

1. **claude-trading-skills** — discipline ("am I in a friendly or hostile market today?")
2. **TradingView (free tier)** — visualization ("what is my stock actually doing?")
3. **OpenBB Platform** — research ("what are the facts behind the price?")

---

## The 3-tool stack at a glance

| | Tool 1: claude-trading-skills | Tool 2: TradingView | Tool 3: OpenBB |
|---|---|---|---|
| **Role** | Discipline coach | Microscope | Research librarian |
| **Asks** | "Should I be aggressive or defensive?" | "What is MSFT doing right now?" | "What are MSFT's facts?" |
| **Interface** | Markdown + Python scripts | GUI app | Python shell |
| **Cost** | Free forever | Free tier (excellent) | Free forever |
| **Time to learn** | 1 hour | 30 mins | 1-2 hours |
| **Time per day** | 15 mins (or 0 if scripted) | 5 mins | 5 mins (scripted) |
| **Repository** | [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | [tradingview.com](https://www.tradingview.com) | [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) |

---

# 🛠️ Tool 1 — claude-trading-skills

**What it is in one sentence:** A library of 56 "skill folders" (~200 Python implementations + AI instructions) that turn Claude into a disciplined trading analyst.

**Analogy:** A chef's mise-en-place. The **skills** are recipes (market-breadth-analyzer, exposure-coach, …). The **workflows** are tasting menus that chain skills together (`market-regime-daily`, `core-portfolio-weekly`, …). You — the chef — pick the menu and Claude cooks.

### What's inside

| Layer | Count | Examples |
|---|---|---|
| Skills (atomic recipes) | 56 categories, ~200 scripts | market-breadth-analyzer, uptrend-analyzer, exposure-coach, covered-call-builder |
| Workflows (menus) | 5 | `market-regime-daily`, `core-portfolio-weekly`, `swing-opportunity-daily`, `trade-memory-loop`, `monthly-performance-review` |
| Agents / commands / skillsets | Many | Higher-level orchestrators |

### The flagship workflow: `market-regime-daily`

Runs in ~15 min, beginner difficulty, **no paid API needed**. Pulls public CSVs published by TraderMonty (the author) at `tradermonty.github.io/market-breadth-analysis/`.

```
Step 1: market-breadth-analyzer   → 6-component breadth score (0-100)
Step 2: uptrend-analyzer          → 5-component sector participation (0-100)
Step 3: (optional, paid) market-top-detector  ⏭ skipped on free tier
Step 4: exposure-coach            → synthesizes into NEW_ENTRY_ALLOWED / REDUCE_ONLY / CASH_PRIORITY
```

### Sample live output (2026-06-01)

```
Market Breadth Composite:   42.4/100  🟡 Neutral   (60-75% exposure)
Uptrend Participation:      57.7/100  🟡 Neutral   (60-80% exposure)
Exposure Coach:             22%       ⚠️ CASH_PRIORITY (LOW confidence)

Red flags:
  - S&P +11.3% over 60d while breadth -6.3% (dangerous divergence)
  - 200MA "Pink Zone" active 55 consecutive days
  - Breadth at 28th historical percentile

Bright spots:
  - Tech is #1 sector (36.6% uptrend ratio — good for MSFT)
  - Risk-on rotation intact (Cyclicals lead Defensives +8.8pp)
```

### Honest limitations

1. **Markdown-based reasoning ≠ deterministic code.** Two Claude runs of the same skill can produce slightly different prose.
2. **Optional inputs require paid APIs** (FMP, etc.). Skipping them clamps `exposure-coach` confidence to LOW.
3. **No order routing.** Outputs are research only; you still place trades through your broker.
4. **Japanese-first in places** (PROJECT_VISION.ja.md, README.ja.md). English docs are catching up.
5. **State folder is not backed up** by default — if you destroy it you lose journal history. (We exclude it from git for the same reason.)

---

# 🛠️ Tool 2 — TradingView (Desktop / Web)

**What it is in one sentence:** The world's most popular charting platform — Bloomberg-like visuals for retail. Looks at price; doesn't trade for you.

### What you get on the free tier

| Feature | Free | Notes |
|---|---|---|
| Charts on any stock | ✅ Unlimited | |
| Indicators per chart | 2 | Plenty for an amateur |
| Price alerts | ✅ Unlimited (desktop) | The #1 underused feature |
| Real-time US data | ❌ 15-min delayed | Fine for swing/long-term, useless for day trading |
| Paper trading | ✅ | Practice before risking real money |
| Stock screener | ✅ Basic | Run Buffett-style filters in seconds |
| Community ideas | ✅ | Idea generation, not gospel |

### 3 starter workflows for a concentrated holder

| Workflow | When | What you do |
|---|---|---|
| **Daily 2-min check** | After morning briefing | Glance MSFT + HUBS: price vs 50MA vs 200MA, RSI, any triggered alerts |
| **Covered-call strike picker** | When you plan a call | Add `20-day high` + `Bollinger Bands`, pick a strike above resistance & outside upper band |
| **Earnings-week defense** | Week before earnings | Look at last 4 earnings reactions on the chart — that's your expected move |

### Recommendation

**Stay on the free tier for 6+ months.** The 15-minute delay is irrelevant for someone who holds MSFT for years. Upgrade only when you find yourself wanting it (you probably won't).

---

# 🛠️ Tool 3 — OpenBB Platform

**What it is in one sentence:** A free, Python-based aggregator of 30+ financial data sources (Yahoo, SEC EDGAR, FRED, CBOE, Binance, …) behind one unified API.

### Top 5 uses for an employee shareholder

```python
from openbb import obb

# 1. Fundamentals snapshot
obb.equity.fundamental.metrics("MSFT").to_df()

# 2. Dividend history & growth streak
obb.equity.fundamental.dividends("MSFT").to_df()

# 3. Macro indicators (the Fed publishes these)
obb.economy.fred_series("FEDFUNDS").to_df()   # Fed Funds Rate
obb.economy.fred_series("DGS10").to_df()      # 10Y Treasury

# 4. SEC filings + insider trades
obb.equity.fundamental.filings("MSFT")
obb.equity.ownership.insider_trading("MSFT")

# 5. News across watchlist
obb.news.company("MSFT", limit=20)
```

### Honest limitations

1. **Python only.** Real learning curve if you haven't typed Python (1-2 hours).
2. **Best data is paid.** Yahoo (the free default) has gaps. Fine for amateur use, not for serious trading.
3. **Rate limits exist.** Yahoo throttles around ~100 req/min — build pauses into batch scripts.
4. **No trading.** Pure research; doesn't talk to your broker.
5. **OpenBB Terminal (the polished GUI) is now paid.** What's installed here is the open-source **Platform** — same data, different interface.

---

# 🚀 Installation

> **Tested on Windows ARM64 (Surface Pro X / Snapdragon). The Intel x64 path is even simpler.**

### Prerequisites

- Windows 10/11
- ~500 MB free disk space
- An internet connection
- Optional: a free [TradingView](https://www.tradingview.com) account

### 1. Clone this repo

```powershell
cd "$env:USERPROFILE\OneDrive\Documents"   # or wherever you keep projects
git clone https://github.com/<YOUR-USERNAME>/AISidekick-TradingAssistant.git AISidekick\TradingAssistant
cd AISidekick\TradingAssistant
```

### 2. Tool 1 — claude-trading-skills

```powershell
git clone https://github.com/tradermonty/claude-trading-skills
```

### 3. Tool 2 — TradingView Desktop

```powershell
winget install --id TradingView.TradingViewDesktop --silent --accept-package-agreements --accept-source-agreements
```

(Or run `INSTALL_TradingView.bat`.)

### 4. Tool 3 — OpenBB Platform (the tricky bit on ARM64)

**The trap:** OpenBB depends on `aiohttp`, `cachebox` (Rust), `pydantic-core`, etc. — none have prebuilt wheels for Windows ARM64. Default `pip install` calls `cargo build` via maturin and fails without Rust installed.

**The fix:** install **Python 3.11 x64** (not ARM) — it runs under ARM emulation, slightly slower but it gets the prebuilt x64 wheels.

```powershell
# Install x64 Python (one-time, system-wide)
winget install --id Python.Python.3.11 --architecture x64 --silent --accept-package-agreements --accept-source-agreements

# Create the venv using the x64 python
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m venv openbb-env

# Activate + install
.\openbb-env\Scripts\Activate.ps1
pip install openbb
deactivate
```

**Verify:**

```powershell
.\openbb-env\Scripts\python.exe -c "from openbb import obb; print(obb.equity.price.quote('MSFT').to_df())"
```

If you see a price, you're done.

---

# 🎯 Daily routine — `MORNING_ROUTINE.bat`

Double-click `MORNING_ROUTINE.bat` and it will:

1. **Step 1/4** — run `market-breadth-analyzer` against today's live CSV
2. **Step 2/4** — run `uptrend-analyzer` against the sector data
3. **Step 3/4** — chain both outputs into `exposure-coach`
4. **Step 4/4** — run `portfolio_health_check.py` to pull live MSFT + HUBS fundamentals
5. **Auto-open** the briefing + a TradingView MSFT chart in your browser

Total: ~2 minutes wall-clock, ~25 minutes of your reading time.

All outputs land in `claude-trading-skills\reports\daily-YYYY-MM-DD\` as both `.md` (human) and `.json` (machine).

---

# 📁 Repo layout

```
TradingAssistant/
├── README.md                    ← you are here
├── .gitignore                   ← excludes venv, installer, reports
│
├── INSTALL_TradingView.bat      ← one-click TradingView installer
├── LAUNCH_OpenBB.bat            ← opens Python shell with OpenBB pre-loaded
├── MORNING_ROUTINE.bat          ← the daily one-click pipeline
│
├── my_scripts/                  ← your custom OpenBB scripts
│   ├── portfolio_health_check.py    ← weekly: fundamentals snapshot
│   ├── macro_watch.py               ← monthly: Fed, 10Y, CPI, jobs
│   └── insider_alert.py             ← weekly: insider buys/sells
│
├── claude-trading-skills/       ← Tool 1 (git-cloned, gitignored)
├── openbb-env/                  ← Tool 3 venv (gitignored, 270 MB)
├── TradingView_Installer/       ← Tool 2 installer (gitignored, 140 MB)
└── reports/                     ← daily briefings (gitignored - private)
```

---

# ❓ Honest answers to common questions

**Q: Why three tools instead of one?**
A: No single free tool does all three jobs well. Trying to make TradingView do research, or OpenBB do charts, is fighting the tools. They are specialised — together they cover the ground.

**Q: Can I use this for day trading?**
A: No. The free tiers have 15-min data delays. This is built for someone making **2-3 deliberate decisions per quarter**, not for scalping.

**Q: I don't know Python. Is OpenBB worth it?**
A: Honestly — maybe skip it for the first month. Run just Tools 1 + 2 daily and see how much they teach you. Add OpenBB once you've copy-pasted your way through one Python tutorial.

**Q: How much money do I need to make this worth it?**
A: If you own >$10k in a single stock, the discipline payoff is enormous. Below that, just buy index funds and ignore daily noise.

**Q: Why is the breadth score so low when the S&P is at all-time highs?**
A: That's *exactly* the value of Tool 1 — it tells you when the index is being carried by a handful of mega-caps and the average stock is weak. This is when concentrated-tech holders get hurt the most.

---

# ⚠️ Disclaimers

- **Educational only.** None of this is investment advice. The data is real; interpreting it for your tax, risk, and time-horizon is your job.
- **Don't push your daily reports to GitHub.** They're gitignored for a reason — your portfolio activity is private.
- **Verify before trusting.** AI tooling makes mistakes. Spot-check the outputs against your broker's data before acting.
- **Past patterns ≠ future outcomes.** Every signal can fail.

---

# 🙏 Credits

- **TraderMonty** for the open-source [claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) library and the public market-breadth dashboard
- **TradingView** for the best free charting platform on the internet
- **OpenBB** for proving Bloomberg-class data doesn't need to cost $24k/year
- **GitHub Copilot CLI** for stitching it together

---

*Built for amateurs who want to be a little less amateurish.*
