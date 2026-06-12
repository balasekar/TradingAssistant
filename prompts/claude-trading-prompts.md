# Claude Trading Prompts (AI Panda thread)

> 16 prompts from [@AIPandaX](https://x.com/AIPandaX) that turn Claude (or any chat LLM) into a "Wall Street hedge fund manager." Verbatim from the source thread. Use these *outside* `MORNING_ROUTINE.bat` — they're conversation starters, not Python steps.

## Source

- **Author:** AI Panda ([@AIPandaX](https://x.com/AIPandaX))
- **Thread head:** <https://x.com/AIPandaX/status/2033613492134215795>
- **Posted:** 2026-03-16
- **Fetched:** 2026-06-12 (via `nitter.tiekoetter.com` — X's authenticated render blocks the public thread)
- **OP:** "🚨BREAKING: Claude can now analyze the stock market and build your trading strategy in hours not weeks. Here are 16 powerful prompts that act like a Wall Street hedge fund manager (for free)."

## Quick reference

| # | Persona | When to use it |
|---|---|---|
| 1 | Portfolio Architect | Diversifying around the MSFT + HUBS grant |
| 2 | Earnings Decoder | Before MSFT/HUBS earnings reactions |
| 3 | Risk Manager | Before sizing any new entry |
| 4 | Macro Economist | After a Fed announcement / `macro_watch.py` |
| 5 | Backtest Engineer | Designing a new rule before paper-trading it |
| 6 | Sentiment Tracker | After `insider_alert.py` + a news pull |
| 7 | Technical Analyst | At the TradingView chart, hunting an entry |
| 8 | Dividend Compounder | Long-term candidate screening |
| 9 | Options Strategist | Selling covered calls on the 100 MSFT lot |
| 10 | Insider Tracker | When `insider_alert.py` shows cluster buys |
| 11 | Sector Rotator | When exposure-coach flags `REDUCE_ONLY` |
| 12 | Bear Market Shield | Tech-concentrated hedging (directly fits this user) |
| 13 | Behavioral Coach | After a losing streak — psychology reset |
| 14 | Crypto Correlator | Side research only — not part of the stack |
| 15 | Exit Strategist | Locking gains on a winner |
| 16 | Trade Journal Analyst | Monthly review of a manual trade log |

---

## 1. The Portfolio Architect
*Stop guessing what to buy.*

```
Act as a fiduciary financial advisor. I have [Amount] to invest.
Build a diversified stock portfolio tailored for [Goal].
Explain the exact percentage allocation for each sector and why.
```

## 2. The Earnings Decoder
*Read between the lines of corporate jargon.*

```
Analyze this recent earnings call transcript for [Company].
Act as a cynical short-seller. Highlight the 3 biggest red flags
the CEO tried to hide and explain how they impact the stock price.
```

## 3. The Risk Manager
*Protect your capital at all costs.*

```
I want to trade [Stock] at [Price]. Act as a strict risk manager.
Calculate my exact position size, stop-loss level, and take-profit
targets assuming I only want to risk 1% of my total [Account Size]
portfolio.
```

## 4. The Macro Economist
*Understand the big picture.*

```
The Federal Reserve just announced [News/Rate Hike]. Act as a macro
hedge fund manager. Explain exactly how this impacts tech stocks,
commodities, and real estate over the next 6 months.
```

## 5. The Backtest Engineer
*Test before you trade.*

```
Act as a quantitative analyst. I want to trade a moving average
crossover strategy on the S&P 500. Write the Python code using
pandas and yfinance to backtest this strategy over the last 5 years
and calculate the maximum drawdown.
```

## 6. The Sentiment Tracker
*Follow the crowd to fade the crowd.*

```
I will paste the last 20 news headlines about [Company]. Act as a
behavioral finance expert. Analyze the market sentiment. Is the
market overly euphoric or in panic mode? Tell me if this is a
contrarian buying opportunity.
```

## 7. The Technical Analyst
*Find your entry points.*

```
Explain how to combine the RSI indicator with Volume Profile to
find high-probability entry points for day trading [Stock]. Give
me a step-by-step checklist to confirm a breakout before I buy.
```

## 8. The Dividend Compounder
*Build passive income safely.*

```
Act as a value investor like Warren Buffett. Screen for 5 stocks
with a dividend yield over 3%, a payout ratio under 50%, and
consecutive dividend growth for 10 years. Explain the moat of
each business.
```

## 9. The Options Strategist
*Generate income in a flat market.*

```
I own 100 shares of [Stock]. Act as an options trader. Explain
how to set up a covered call strategy to generate weekly income.
Tell me exactly which strike price and expiration date to choose
to minimize the risk of losing my shares.
```

## 10. The Insider Tracker
*Follow the smart money.*

```
The CEO and CFO of [Company] just bought large amounts of their
own stock. Act as an institutional analyst. Explain the historical
win rate of mimicking insider cluster buying and outline a trade
setup to capitalize on this.
```

## 11. The Sector Rotator
*Catch the money flow.*

```
We are entering an economic recession. Act as a portfolio strategist.
Tell me exactly which 3 stock market sectors historically outperform
during a recession and which 3 sectors I need to sell immediately.
```

## 12. The Bear Market Shield
*Profit when everything crashes.*

```
My portfolio is heavily weighted in tech stocks. Act as a hedging
expert. Give me 3 cost-effective ways to hedge my portfolio against
a 20% market crash using inverse ETFs or put options.
```

## 13. The Behavioral Coach
*Master your psychology.*

```
I just lost 3 trades in a row and feel the urge to revenge trade.
Act as a trading psychologist. Give me a strict mental framework
to reset my emotions and a checklist I must pass before taking
my next trade.
```

## 14. The Crypto Correlator
*Trade the overlap.*

```
Act as a cross-asset trader. Explain the current correlation between
Bitcoin and the Nasdaq 100. How can I use a breakout in tech stocks
as a leading indicator to trade crypto?
```

## 15. The Exit Strategist
*Know when to walk away.*

```
I am up 40% on my position in [Stock]. Act as a ruthless portfolio
manager. Give me a trailing stop-loss strategy to lock in profits
without getting shaken out by normal market volatility.
```

## 16. The Trade Journal Analyst
*Learn from your mistakes.*

```
Here is my trading log for the last month: [Insert Data]. Act as
a performance coach. Identify my most profitable time of day, my
worst performing setup, and give me one strict rule to improve
my win rate next month.
```

---

## Mapping to this repo's 3-tool stack

This is opinionated for the repo owner (100 MSFT + 100 HUBS concentrated grant, daily `MORNING_ROUTINE.bat`).

| Trigger | Reach for |
|---|---|
| `exposure-coach` reports `CASH_PRIORITY` or `REDUCE_ONLY` | **#1 Portfolio Architect** (diversify the freed cash), then **#11 Sector Rotator** (which sectors to rotate into) |
| MSFT or HUBS earnings within 7 days | **#2 Earnings Decoder** — pull transcript link with `obb.equity.fundamental.transcript("MSFT")`, paste into Claude |
| Planning a new entry (size unknown) | **#3 Risk Manager** — feed it the current price from OpenBB and your account size |
| `macro_watch.py` shows Fed/CPI move | **#4 Macro Economist** |
| Want to test a rule before paper-trading | **#5 Backtest Engineer** — already templated in `examples/ma_crossover_backtest.py` |
| `insider_alert.py` shows recent activity | **#10 Insider Tracker** (cluster context) + **#6 Sentiment Tracker** (paste 20 headlines from `obb.news.company`) |
| At the TradingView chart, looking for entry | **#7 Technical Analyst** |
| Adding a new long-term candidate | **#8 Dividend Compounder** alongside `screen_longterm_candidates.py` |
| Selling premium against the 100 MSFT lot | **#9 Options Strategist** — note: requires you to provide the live option chain; OpenBB has `obb.derivatives.options.chains("MSFT", provider="yfinance")` |
| Tech-heavy portfolio worried about a crash | **#12 Bear Market Shield** — directly applicable; pair with `portfolio_health_check.py` output to quantify the concentration first |
| Up >30% on HUBS | **#15 Exit Strategist** |
| Post-loss psychology reset | **#13 Behavioral Coach** — no tooling, just paste and read |
| Monthly performance review | **#16 Trade Journal Analyst** — this repo has no journaling script; if you start one, write it to `my_scripts/trade_journal.py` |

**Out of scope for this repo:** #14 (crypto) — keep as side research; this stack is equity-focused.

## Caveats

- A persona prompt does not create an actual fiduciary, regulatory, or advisory relationship.
- The LLM will confidently state percentages, strike prices, and historical win rates that are *not* sourced from live data unless you paste in the data (OpenBB output, transcripts, headlines). Always grab the real numbers from OpenBB / TradingView first; the prompt then *interprets* them.
- Re-read the disclaimers in the repo's `README.md` before acting on any output.
