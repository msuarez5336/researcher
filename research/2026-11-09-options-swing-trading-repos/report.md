# GitHub repos that tried buying options on stocks and indexes, from 0DTE to under 3 months

*Research run `research/2026-11-09-options-swing-trading-repos/` · as of 2026-11-09 · tier: DEEP*

Tags: [E] measured or documented result · [O] opinion · ✓ quote checked against the cached
original · ~ read via a snippet or an uncached page, unverified. Every return figure below is
the author's own; no code was run. This is a survey of what people tried, not financial advice.

Scope, as set by the user: positions opened by buying calls or puts (premium selling is out),
on stocks and indexes (index ETFs are labelled), held from intraday up to under 3 months.

## Top findings

1. **No repo found shows a profitable long-option system on real money.** Of the eight repos
   read in code, none has a live-money record; results are backtests or paper trading, and
   most price options with a Black-Scholes model instead of historical quotes. [E] ✓
2. **The best-built swing study is `Darson2004/kelly-event-vol`, and its edge is narrow.** It
   buys an at-the-money straddle 14 days before earnings on real exchange quotes and reports
   +6.39% per trade after spread and commissions on 193 trades. The same rule entered 7 days
   before earns +0.24%, and the author says the exit cost is unmeasured and the result turns
   negative if the exit pays more than 0.605 of the half-spread. [E]
   ([README](https://raw.githubusercontent.com/Darson2004/kelly-event-vol/HEAD/README.md)) ✓
3. **The most-starred find, `randomwalkhan/Short-Term-Reversal-Strategy` (266 stars), reports
   +690.85% on modelled prices.** Its backtest prices the calls with a Black-Scholes function
   and the worker found no spread or commission cost in the backtest scripts. It does keep a
   live paper log, and the author demoted one entry type after it underperformed on paper. [E]
   ([README](https://raw.githubusercontent.com/randomwalkhan/Short-Term-Reversal-Strategy/HEAD/README.md)) ✓
4. **Three of four 0DTE repos report no edge from buying options.** One finds profit factor
   0.97 for a signal-free 0.20-delta call bought at the ask over 951 days; one states "Eleven
   research waves found no long-premium options edge"; one found that after fixing a cost bug
   "No structure retains a materially positive net Sharpe ratio". [E] ✓
5. **The one positive 0DTE record is small, on paper, and contradicted by the repo's own
   document.** `milgar7969/alpaca-options-framework` shows 104 paper trades with profit factor
   1.26 on a dashboard, while its strategy PDF gives a clean total of -$121 for an earlier
   window. [E] dashboard ✓, PDF ~
6. **The strongest outside evidence is against the trade type itself.** A University of
   Münster study of Cboe data finds retail investors lost $241,000 on an average day in
   S&P 500 0DTE options (February 2021 to September 2023), over $125 million in total, of
   which over $90 million was transaction costs, and attributes the losses to single-leg
   trades that pay premium up front. [E]
   ([paper](https://wp.lancs.ac.uk/fofi2024/files/2024/04/FoFI-2024-146-Leander-Gayda.pdf)) ✓
7. **For execution, Alpaca and Interactive Brokers are the two best-supported paths.**
   `alpaca-py` is official and Alpaca offers SPX and VIX options through its API, but no spot
   index data. `ib_async` is the maintained successor to the archived `ib_insync`. Schwab's
   login token lasts seven days. [E] ✓ (archive status of `ib_insync` ~)
8. **Realistic backtests need paid data.** No free source of historical option quotes was
   found. QuantConnect bundles minute-level index and equity option data from January 2012;
   ThetaData starts at $40/month for six years of 1-minute data. [E] ✓
9. **Most of the usual advice for buying options has no published test in what we found.**
   No measured test turned up for delta choice, days to expiry, position sizing or profit
   targets on long options. The exceptions are stops and earnings timing, covered below. [E]

## What the repos tried, and what they reported

Eight repos were cloned and read. Four trade on a swing timeframe, four trade 0DTE.

| Repo | Idea | Option prices | Costs | Author-reported result | Verdict |
|---|---|---|---|---|---|
| [`Darson2004/kelly-event-vol`](https://raw.githubusercontent.com/Darson2004/kelly-event-vol/HEAD/README.md) | Straddle 14 days before earnings, 42 liquid stocks, 2020-09 to 2026-08 | Real quotes | Half-spread fraction plus $0.75 per contract | +6.39% per trade net, n=193; +0.24% if entered 7 days before | Study |
| [`randomwalkhan/Short-Term-Reversal-Strategy`](https://raw.githubusercontent.com/randomwalkhan/Short-Term-Reversal-Strategy/HEAD/README.md) | ~30-day calls after large intraday drops, QQQ and leveraged ETFs | Modelled | None found in backtest | +690.85%, max drawdown -26.42%, 117 trades, 69.2% wins; paper equity $117,024.80 on 2026-11-06 | Study; licence is "All rights reserved" |
| [`carolinehutchins05-prog/options-desk`](https://raw.githubusercontent.com/carolinehutchins05-prog/options-desk/HEAD/README.md) | Trend-screened calls on S&P 500 stocks, sold within 5 sessions | Modelled | 2% half-spread each way | Mean -0.37% per trade on 117,754 trades, 45.2% wins; "near breakeven" | Useful negative control |
| [`erictao947/earnings-vol-study`](https://raw.githubusercontent.com/erictao947/earnings-vol-study/HEAD/src/phase7_backtest.py) | Sells the straddle before earnings | — | — | Out of scope (premium selling) | Skip |
| [`milgar7969/alpaca-options-framework`](https://raw.githubusercontent.com/milgar7969/alpaca-options-framework/HEAD/README.md) | SPY (ETF) 0DTE calls and puts on a momentum signal, mornings only | Paper fills | Simulated | Dashboard: 104 trades, 48.1% wins, +$539, profit factor 1.26. PDF: clean total -$121 for 2026-05-20 to 06-17 ~ | Study the execution code |
| [`YichengYang-Ethan/0dte-strategy`](https://raw.githubusercontent.com/YichengYang-Ethan/0dte-strategy/HEAD/README.md) | SPX 0.20-delta 0DTE call, 09:45 to 15:55, no signal, 951 days | Real quotes, buy at ask, sell at bid | In the fills | Profit factor 0.97 with no stop; 1.28 with a -40% stop | Study the method |
| [`vilkovgr/0dte-strategies`](https://raw.githubusercontent.com/vilkovgr/0dte-strategies/HEAD/KNOWN-ISSUES.md) | Replication package for a paper; mixed long and short SPX structures | Real data (not fetchable) | Yes, after a bug fix | No structure keeps a materially positive net Sharpe | Skip |
| [`luphillip041-hub/odte-bot`](https://raw.githubusercontent.com/luphillip041-hub/odte-bot/HEAD/README.md) | SPY/QQQ (ETF) 0DTE calls and puts, ~0.25 delta | Modelled, 10% slippage per side | Yes | "Eleven research waves found no long-premium options edge" | Read the docs, skip the bot |

Things worth knowing behind the table:

- **Only two repos use real option quotes for a long-option test**: `kelly-event-vol` and
  `0dte-strategy`. Both state their own weaknesses. [E] ✓
- **`kelly-event-vol`'s fill model** is "mid ± φ · ½ spread, with φ = 0.5 by default, plus
  $0.75 per contract". The headline holds only under one filter (implied move at most 0.90×
  the past realised move) and only at 14 days before earnings. [E] ✓
- **`options-desk`'s code differs from its README.** The README describes 45–60 day calls;
  the worker found the backtest runs 30 calendar days with 45 as a sensitivity. The 95%
  confidence interval on the mean is -2.7% to +1.9%, so no edge is shown either way.
  [E] results file ✓, code reading ~
- **`alpaca-options-framework` stops new entries at noon** because, in the author's words,
  afternoons were "net -$514/47 trades in Jul". Its dashboard figures are not in the repo, so
  they cannot be reproduced from the clone. [E] ✓
- **A stop changed the 0DTE baseline's sign, at a price.** In `0dte-strategy` the -40% stop
  lifts profit factor from 0.97 to 1.28, but the worker's reading is that the win rate falls
  from 18.7% to 9.7%. One rule, one period, no commissions stated. [E] profit factors ✓,
  win rates ~
- **Buying the option instead of the underlying cost edge.** The same author's earlier
  next-day SPY call test reports the "long-call wrapper ate ~41% of edge; debit spread ate
  ~95%". [E] ✓

Other repos seen but not read in code:

- **No outcome published:** `rus237sell/trade-algo-v2`, `wheelieinvestor/openclaw-bot`,
  `trevorgordon981/Agentic-Trader`, `kaiuribess/Optedge`. [E] ✓
- **Not pure long (spreads):** `Jennycruzy/convex`, `AKzar1el/clockcross`,
  `ProgramComputer/earnings-trade-automation`. ~
- **Over the 3-month limit (300–800 day calls):** `davidwang0116/QQQ-LEAPS-CALL-INFINITE-ROLL-BACKTEST`,
  `anti31415/qqq-leaps-strategy`, `Kizo07/LEAPS-Stock-Substitute-Backtest`. Out of scope.
- **Unread leads:** `giordanoshai/alpaca-0DTE`, `Javier-Garzo/ern-wo-options-backtester`,
  `pranay123-stack/ibkr-trading-bots`, and a SPY weekly-call backtest inside
  `Lumiwealth/lumibot` (`docs/research/2026-09-23-alpaca-options-backtests`). ~

## Which practices have a result behind them

| Practice | What was found | Status |
|---|---|---|
| Avoid buying before earnings | A vendor backtest of S&P 500 earnings straddles, entered 9 days before and exited the next session, reports -18.5% per trade with a 22% win rate ([IVolatility](https://www.ivolatility.com/news/3147)). `kelly-event-vol` reports +6.39% for a filtered entry 14 days before. | [E] ✓ both; they conflict, see below |
| Use a hard stop on 0DTE | One test: -40% stop moves profit factor from 0.97 to 1.28 | [E] ✓ single test |
| Trade defined time windows on 0DTE | One repo cut afternoon entries after losing $514 on 47 afternoon trades in one month | [E] ✓ one month, paper |
| Model fills at the spread, not the mid | A short-put-spread backtest flips from positive at mid fills to breakeven or negative at honest fills ([FlashAlpha](https://flashalpha.com/articles/vrp-short-put-spreads-honest-7-year-backtest)); `kelly-event-vol` flips sign at 0.605 of the half-spread on exit | [E] ✓ (first is a selling strategy) |
| Trade only liquid contracts | `Short-Term-Reversal-Strategy` gates live entries on spread, open interest and volume; no test of the gate's effect | [O] ~ |
| Buy higher delta, buy more time, size at 1–2%, fixed profit targets, buy when volatility is low | No measured test on long options found | Not found |

Background evidence on the trade type:

- **Retail 0DTE buyers lose, mostly to costs.** Beckmeyer, Branger and Gayda (version of
  15 December 2023): "$241,000 on an average day" between February 2021 and September 2023,
  rising to "$350,000 per day" since daily expirations began in May 2022, and "Roughly 60% of
  daily losses are the result of transaction costs". Multi-leg trades did better than
  single-leg ones. [E] ✓
- **Implied volatility usually falls after earnings.** Option Alpha reports it contracted
  after about 90% of 1,546 earnings events ([post](https://optionalpha.com/we-stopped-trading-earnings-after-we-saw-this-new-research-188320.html)).
  Vendor self-report. [E] ✓
- **Hedged long index options have earned less than zero on average** in older data (Bakshi
  and Kapadia, 2003, [abstract](https://ideas.repec.org/a/oup/rfinst/v16y2003i2p527-566.html)).
  This is for delta-hedged positions, so it does not transfer directly to outright calls
  and puts. [E] ✓

## Platforms

### Brokers and client libraries

| Broker | Library | Stars | Last commit | Options points | Caveat |
|---|---|---|---|---|---|
| Alpaca | `alpacahq/alpaca-py`, official | 1,591 | 2026-11-09 | Index options live through the API, including SPX, SPXW, VIX and XSP ([blog](https://alpaca.markets/blog/alpaca-launches-index-options-via-trading-api)); paper trading | No spot index data; Alpaca warns paper fills differ from live |
| Interactive Brokers | `ib-api-reloaded/ib_async` | 1,787 | 2025-12-06 | Maintained successor to `ib_insync` | Spot SPX and Greeks need extra data subscriptions ([IBKR](https://www.interactivebrokers.com/docs/general/market-data-subscriptions/popular-market-data-subscriptions)) |
| Schwab | `alexgolec/schwab-py`, unofficial | 480 | 2025-08-04 | Buy-to-open order templates, weekly SPX symbols | "Tokens are only good for seven days" ([docs](https://schwab-py.readthedocs.io/en/latest/auth.html)); no historical options data; no paper trading found |
| Tradier | Official REST API | — | — | Chains and Greeks; sandbox | Sandbox fills against delayed data; index options $0.35 per contract on Pro, $0.10 on Pro Plus ([pricing](https://tradier.com/individuals/pricing)) |
| Tastytrade | `tastyware/tastytrade`, unofficial | 259 | 2026-08-07 | Chains, streamed quotes and Greeks | Sandbox resets every 24 hours on a delayed feed ([docs](https://developer.tastytrade.com/docs/sandbox)) |
| Webull | `webull-inc/webull-openapi-python-sdk`, official | 73 | not checked | Single and multi-leg options | Old SDK deprecated; no paper trading per QuantConnect ~ |
| Robinhood, E*TRADE | `robin_stocks`, `pyetrade`, unofficial | 2,127 / 250 | not checked | — | No official Robinhood options API ~; E*TRADE tokens expire at midnight Eastern ~ |

All ✓ unless marked ~. Stars are the GitHub API count on 2026-11-09. "Last commit" is the
default branch; `ib_async` and `schwab-py` show later pushes (2026-11-04 and 2026-08-26) to
other branches.

Among the eight repos read, three trade through Alpaca paper accounts
(`alpaca-options-framework`, `odte-bot`, and the live log of `Short-Term-Reversal-Strategy`
is paper; its broker was not confirmed).

### Backtesting frameworks and data

| Tool | Stars | Last commit | What it gives | Limit |
|---|---|---|---|---|
| `QuantConnect/Lean` | 22,466 | 2026-11-09 | Bundled minute data: SPX, VIX, NDX options and 4,000 equity option symbols from January 2012 ([index](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-index-options), [equity](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-equity-options)) | Default fill model "does not take size or volume into account" (staff forum reply) [O] |
| `goldspanlabs/optopsy` | 1,514 | 2026-11-04 | Options backtester with slippage settings | Needs an outside data provider; its own disclaimer says results omit liquidity, slippage and assignment risk |
| `Lumiwealth/lumibot` | 2,219 | 2026-11-05 | One strategy class for backtest and live | Open issues on option backtests ~ |
| `nautechsystems/nautilus_trader` | 31,416 | 2026-11-10 | Option instruments, Greeks, chains | Open issues on option backtesting ~ |

| Data source | History and resolution | Price as stated by the vendor |
|---|---|---|
| ThetaData | 6 years at 1-minute; 10 years at tick; 14 years | $40, $80, $160 per month ([pricing](https://thetadata.net/pricing)) |
| Cboe DataShop | 1-minute option quotes with sizes | SPX index bid/ask needs a licence, "fees start at $1k/month" ([page](https://datashop.cboe.com/option-quotes)) |
| Massive (formerly Polygon.io) | Option bars built from trades only, so quiet contracts have gaps ([docs](https://massive.com/docs/options/getting-started)) | Not captured from the vendor |
| ORATS | Backtester assumes slippage of 75% of the spread on single legs ([method](https://orats.com/university/backtesting-methodology)) | Prices differ across its pages; not reconciled |
| yfinance | Current chains only ~ | Free; Yahoo's API is personal-use only |

All ✓ unless marked ~. Databento, OptionsDX prices, and whether backtrader, vectorbt or
backtesting.py handle options were not reached.

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Does buying straddles before earnings lose money? | Yes: -18.5% per trade, 22% wins (IVolatility, S&P 500, 2021–2026, entered 9 days before, exited next session) | No, for a subset: +6.39% per trade (`kelly-event-vol`, 42 liquid names, entered 14 days before, only when the implied move is at most 0.90× the past realised move) | A is the unfiltered average across the index. B is a filtered subset with an earlier entry, and it shrinks to +0.24% at 7 days. |
| Is long 0DTE profitable? | Positive: profit factor 1.26 on 104 paper trades (`alpaca-options-framework` dashboard) | Negative or flat: profit factor 0.97 unconditional (`0dte-strategy`); no edge in eleven research waves (`odte-bot`); -$121 clean total in the first repo's own PDF ~ | A is ~5-minute scalps on simulated paper fills over four weeks. B uses historical quotes or longer research. Neither side used real money. |
| Do modelled-price call backtests show an edge? | +690.85% in one year (`Short-Term-Reversal-Strategy`, no spread cost found) | -0.37% per trade (`options-desk`, 2% half-spread each way) | Different rules and universes. Both use Black-Scholes prices, so neither observes real fills. |
| How much did retail lose per day on 0DTE? | $350,000 since May 2022 (paper, December 2023 version) | $358,000 (press coverage of an earlier version) | Different versions and sample ends of the same paper. Use the paper. |
| Tradier's SPX commission | $0.35 or $0.10 per contract by plan | $0.60 on the SPX line of the fee table | Probably plan tiers plus exchange fees; not resolved. |

## Outdated or superseded material

- **`ib_insync`**: archived in 2024 ~; use `ib_async`.
- **TD Ameritrade API and `tda-api`**: replaced by the Schwab API and `schwab-py`. The
  retirement itself was not checked in this run.
- **Webull `openapi-python-sdk`**: deprecated; replaced by `webull-openapi-python-sdk`. ✓
- **Polygon.io**: now trades as Massive; the docs say "formerly Polygon.io" ✓, the rename
  date of 2025-10-30 is from a snippet ~.
- **`michaelchu/optopsy`**: the project now lives at `goldspanlabs/optopsy`. ✓
- **Pages saying Alpaca has no index options** predate Alpaca's launch of them. ~

## Method and limitations

- **Workers:** 5 discovery researchers, 2 follow-up researchers, 2 deep-read researchers
  and 1 brief reviewer, 111 evidence items. Claim verification results are in `verdicts/`.
- **Quote check:** 101 of 111 items matched their cached source at the last full check; the
  rest are labelled ~ here.
- **Reddit was effectively blocked.** Its search returned 403 and web search limited to
  reddit.com was refused. No first-hand "I ran this" account with trade count, period and
  P&L was found anywhere outside GitHub, so the report has none. Absence here is not
  evidence that none exist.
- **GitHub coverage is partial.** Repo search returned nothing for long queries and workers
  saw only the top results of short ones. Several code-search hits were never opened.
- **Nothing was run.** Results are as the authors state them. Two result sets are not in
  the repos at all (the `alpaca-options-framework` dashboard and the `kelly-event-vol`
  holdout).
- **`github.com` pages were blocked**, so stars come from the API and issue contents were
  read only through search results.
- **The SQ3 and SQ4 platform tables are a breadth pass.** Commissions for Interactive
  Brokers and Tastytrade, and Schwab rate limits, were not found.

## Open questions

- Do `kelly-event-vol`'s results survive a measured exit cost? Its author names this as the
  gap; the test needs exit-side quote data.
- What do the `Short-Term-Reversal-Strategy` live paper trades sum to against its backtest
  over the same dates? The trade CSV is in the repo and could be tallied.
- Is there any live-money long-option record on GitHub? The unread leads above and a Reddit
  search from an unblocked network are the next places to look.
