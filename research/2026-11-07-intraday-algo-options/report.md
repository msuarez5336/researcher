# Intraday signals and exit rules for buying single options

*Research run `research/2026-11-07-intraday-algo-options/`. As of 2026-11-07. Tier: DEEP.*

**Who this is for:** a self-directed trader who buys one call or put, at most once or twice a
day, on US ETF or large single-stock options, through a retail broker.

**Tags used in this report:**
- **[E]** marks a measured result, given with its setup.
- **[O]** marks an opinion or a recommendation.
- **✓** means the claim was checked against the original page by an independent claim-verifier.
- **~** means the claim was read only through a summary or snippet, or was partly verified.
- **Claim numbers (C1–C20)** refer to the files in `verdicts/`.

> **Bottom line [O]:** No published, independently replicated rule shows that buying single options
> on an intraday signal is profitable after costs. The evidence supports *testing* three or four
> specific rules, not trading them. Every rule should first be backtested on real bid/ask option
> quotes, then paper-traded.

## Top findings
1. **Buying options loses money on average, and costs are the biggest part of the loss on
   short-dated trades.**
   - Zero-beta at-the-money S&P straddles lost about 3% a week in the 1990s.
     [E] ([Coval & Shumway 2001](https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:3:p:983-1009)) ✓
   - In 0DTE SPX options, retail traders lost about $184k a day, and about 60% of that loss was
     transaction costs.
     [E] ([Swedroe's summary of the 2023 working paper](https://www.wealthmanagement.com/equities/retail-investors-are-in-love-with-same-day-options)).
     The figures are verified against the summary ✓; the SSRN original was not reachable.
   - So any entry signal has to beat both the volatility risk premium and the spread.
2. **The best-documented entry signals are three momentum rules from the open or the first
   half-hour.**
   - First half-hour momentum: the first half-hour return predicts the last half-hour.
     [E] ([Gao et al., JFE 2018](https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414)) ✓
     In the 2014 working-paper version, out-of-sample R² was up to 0.018 on SPY.
     ([CXO summary](https://cxoadvisory.com/calendar-effects/first-and-last-half-hours-of-trading-linked)) ~
   - The 5-minute opening-range breakout. [E]
     ([CXO summary](https://www.cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy)) ~
   - SPY "noise area" momentum. [E]
     ([working paper](https://www.alexandria.unisg.ch/handle/20.500.14171/122124))
   - None has an independent, net-of-cost, out-of-sample test. Two show signs of decay
     (finding 5).
3. **The overnight gap and dealer-gamma levels do not work as stand-alone direction signals.**
   - The SPY gap and the open-to-close return have a correlation of 0.01 (1993–2025). This is
     descriptive, not a test of a trading rule.
     [E] ([CXO](https://www.cxoadvisory.com/technical-trading/gap-reversal-or-continuation)) ✓
   - End-of-day GEX had no statistically significant added power for next-day volatility once VIX
     and at-the-money implied volatility were controlled for. Dealer delta exposure did not predict
     direction (vendor test, 1,972 SPY days, 2018–2026).
     [E] ([FlashAlpha](https://flashalpha.com/articles/gex-dex-vex-chex-8-year-backtest-spy-vix-control)) ✓
   - Negative dealer gamma may still work as a *filter* on momentum, but the evidence conflicts
     (see the disagreements table).
4. **No study tests any exit rule on bought single options.**
   - The only evidence comes from stocks and futures, and it disagrees on whether stops help.
     [E] ([Kaminski & Lo](https://dspace.mit.edu/handle/1721.1/114876);
     [Lei & Li](https://openjournals.libs.uga.edu/fsr/article/view/4933))
   - Volatility-based exits are a sensible design to test, not a proven edge.
5. **The candidate rules are weaker in independent tests.**
   - A replication of the opening-range breakout on index CFDs reproduces the gross edge, but
     after costs the result is about zero.
     [E] ([replication](https://www.mql5.com/en/blogs/post/776235), self-published blog) ✓
   - First half-hour momentum: a related variant, where the overnight return predicts the last
     half-hour, "disappears in the out-of-sample period".
     [E] ([Rosa 2022](https://econpapers.repec.org/RePEc:wly:jfutmk:v:42:y:2022:i:12:p:2218-2234)) ✓
6. **The pattern-day-trader rule has been replaced.** FINRA Notice 26-10 removes the $25k minimum and
   the day-trade count, effective 2026-06-04. Brokers may phase it in until 2027-10-20.
   [E] ([FINRA](https://www.finra.org/rules-guidance/notices/26-10)) ✓
7. **A credible backtest needs bid/ask option quotes at least every minute.** Two sources found here:
   - ThetaData has tick-level quotes on its $80/month plan.
     [E] ([pricing](https://thetadata.net/pricing)) ✓
   - Cboe DataShop has 1-minute quotes back to 2012.
   - Filling at the mid-price overstates returns.

## 1. Entry signals that fire once or twice a day

| Signal | When it fires | Best evidence | Measured result | Costs / out-of-sample | Status |
|---|---|---|---|---|---|
| First half-hour momentum | 10:00 sets the direction; entry 15:30, exit at the close | Gao, Han, Li & Zhou, JFE 2018 (grade A, SPY 1993–2013) ✓ | From the 2014 working-paper version (Gao, Han & Zhou, SPY 1999–2012): out-of-sample R² up to 0.018. A timing rule earned 6.3% a year gross, against -0.5%. R² was 0.048 on high-volatility mornings. The JFE version may report different R² values (not checked; host blocked). ~ | Gross only. A QuantConnect test for 2015–2020 [underperformed its benchmark](https://www.quantconnect.com/research/15348/intraday-etf-momentum/). Rosa 2022 found the overnight variant fails out-of-sample. | Weakened |
| 5-minute opening-range breakout (ORB) | 9:35, in the direction of the first bar | Zarattini & Aziz, SSRN 2023 (read via the CXO summary) | QQQ: 33.2% a year against 14.9% (Jan 2016–Feb 2023). Commission included; no spread or slippage; up to 4x leverage; no out-of-sample period ([per the replication](https://www.mql5.com/en/blogs/post/776235)). ~ | The CFD replication for 2015–2026 is gross +0.13 R a trade and net about 0. It was negative in 4 of 5 markets. | Weakened |
| SPY "noise area" momentum | A break of the band around the average intraday move, checked every 30 min | Zarattini, Aziz & Barbon (working paper) | 19.6% a year net of costs, Sharpe 1.33, 2007 to early 2024 ✓. The paper's abstract does not state the trailing-stop and flat-at-close mechanics; they come from SQ1's notes ~. | Costs included. In-sample, with no independent test. It can fire more than twice a day. | Unknown |
| "Stocks in Play" ORB | The same ORB on stocks with unusual volume or news | Zarattini, Barbon & Aziz ([working paper](https://alexandria.unisg.ch/handle/20.500.14171/122125)) | Top-20 portfolio: Sharpe 2.81 net (2016–2023). | A one-year (2016) [QuantConnect recreation](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/) found Sharpe 2.4. Users report gaps between backtest and live results. | Unknown |
| Overnight gap fade or continuation | At the open | CXO, SPY Jan 1993–Mar 2025 | Correlation 0.01 ✓. This is descriptive, not a test of a trading rule. | n/a | **Drop** as a stand-alone signal |
| Macro releases, earnings opens, VWAP reversion | n/a | Not covered (out of budget) | n/a | n/a | Open question |

**Reading [O]:** These are all *momentum* signals, so they suit buying a call or put in the
signal's direction. Their reported edges are small per trade, in R² or R terms. The open-range
and noise-area results depend on leverage and on low cost assumptions. Expressing them through
options adds the spread and time decay.

## 2. Signals from options data: filters, not triggers

- **Dealer gamma (GEX/DEX):**
  - A vendor test on 1,972 SPY days found GEX had no statistically significant added power for
    next-day volatility after VIX and at-the-money IV (rho -0.03, p=0.18). It was modestly useful
    over VIX alone. DEX did not predict direction (p=0.97).
    [E] grade B, vendor, end-of-day data, no costs ✓
  - Baltussen et al. (JFE 2021) find intraday momentum concentrated on *negative* net-gamma days.
    In S&P 500 futures (1996–2020), the momentum coefficient was 6.63 (t=4.78) on negative-gamma
    days and 0.82 (t=1.03) otherwise.
    [E] ([Alpha Architect summary](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)).
    The claim-verifier checked the published paper on the author's site ✓.
  - Cboe found SPX 0DTE dealer gamma small: 0.04–0.17% of S&P futures volume. It also found no
    rise in sudden 1-minute moves of 2 standard deviations after 0DTE grew.
    [E] ([Cboe](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options), SPX 0DTE 2022–23; Cboe is an interested party) ✓
  - **Use [O]:** at most, a regime filter on the momentum rules. It is worth testing, not
    assuming.
- **The straddle-implied "expected move":**
  - On 193 Wednesday SPY 0DTE sessions (Jul 2022–Apr 2026), the close landed inside the move
    implied at 10:00 in 71.0% of sessions, against 68.3% expected if fairly priced. Median
    realised moves from 10:00 to the close ran about 13% below implied. ✓
    [E] ([FlashAlpha](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study))
  - VIX1D also overstates realised S&P volatility.
    [E] ([J. Futures Markets 2025](https://ideas.repec.org/a/wly/jfutmk/v45y2025i11p2092-2108.html))
  - **Use [O]:** this is the natural *unit* for targets and stops (section 4). It also warns that
    a bought option starts with the implied move priced slightly rich.
- **Put-call volume:**
  - Pan & Poteshman's result is daily, on 1990–2001 data, and was not replicated after 2010.
    ([NBER](https://www.nber.org/papers/w10925))
  - **Outdated.** Drop it as an intraday trigger.

## 3. Which option to buy

There is no direct evidence on returns by expiration and delta for signal-timed purchases.
What there is:
- **[E] Buyers lose on average.** See Coval & Shumway, and the retail 0DTE losses, about 60% of
  them from costs.
- **[E] Held-to-expiry 0DTE SPX buys (Vilkov, Sept 2016–Jan 2024, via the Hull Tactical
  summary):** some trades, such as buying deep in-the-money calls, are profitable at the median.
  Return distributions are so wide that most strategies' average returns are not statistically
  significant. Much of the P&L is explained by the index's realised skewness.
  ([summary](https://hulltactical.com/2026/07/08/0dte-options-tiny-edge-huge-distribution/)) ~
- **[E] Late-day 0DTE quotes:** deep strikes stop quoting late in the day, so stops and exits
  there may not fill (SQ6 notes).
- **[O] Recommended starting point to test.** This is reasoning, not evidence:
  - **Delta about 0.55–0.70**, slightly in the money. You pay less of the price as time value
    and spread per unit of delta. Out-of-the-money "lottery" buys are where retail losses
    concentrate.
  - **Expiration matched to the holding period:**
    - For exits on the same afternoon (ORB, noise area): 1–7 DTE on SPY or QQQ. Avoid 0DTE
      entered after about 14:00 because of time decay and thin late quotes.
    - For the 30-minute last-half-hour rule: 0DTE or 1DTE, with the strike near the money.
    - For signals held over several days: 2–6 weeks.
  - **SPY and QQQ first**, then large single stocks. Single-stock spreads are wider, and none of
    the stock rules were tested with options.
  - **Avoid holding long options through earnings** unless that is the trade. One vendor season
    (2026) favoured straddle buyers, against the long-run evidence.
    ([ORATS](https://orats.com/blog/earnings-straddles-strong-season-2026))

## 4. Exit rules

**No study tests premium stops, volatility-scaled targets, time stops, breakeven stops or partial
exits on bought single options [E].** The nearest evidence:

| Exit evidence | Market | Result |
|---|---|---|
| Kaminski & Lo (J. Financial Markets 2014) ✓ | Index futures | Some stop-loss policies raise expected return and lower volatility. Only the abstract was read. |
| Lei & Li (Financial Services Review 2009) ✓ | NYSE/AMEX stocks 1970–2005, stops of 5–20 daily standard deviations | Stops neither reduce nor increase losses compared with buy-and-hold. Certain trailing stops reduce volatility, in simulations only at some stop levels. |
| [Practitioner test](https://hackernoon.com/dollar-stop-losses-vs-volatility-stop-losses-algorithmic-trading-tips-oj8j32jv) (grade C) | 3 futures markets, daily bars, about 5 years, with costs | An ATR stop beat a dollar stop in 66% of comparisons. **No stop** beat both. |
| [1DTE iron-condor backtest](https://jwplatta.github.io/posts/distribution-and-regime-effects-in-a-1dte-options-strategy) (short premium) | SPX, 2022–2025 | About 50–70% of stop-outs would have recovered. |
| Signal papers' own exits | ORB, noise area, first half-hour | The stop at the far side of the opening bar, or a VWAP/band trailing stop, and a forced exit at the close. These are tested only on the underlying. |

**[O] Exit design to test.** Define exits on the *underlying*, in volatility units, and carry them
out through the option. Spread spikes make stops on the option's own price unreliable.

| Exit | Rule to test | Broker order |
|---|---|---|
| Invalidation stop | The signal's own level: far side of the opening range, re-entry into the noise band, or VWAP | A conditional order triggered by the underlying's price that sells the option at a limit. IBKR supports this ✓. Elsewhere, an alert plus a manual or API order. |
| Volatility stop | Underlying moves 0.3–0.5× the expected move against the entry (the expected move comes from the at-the-money straddle at entry) | As above |
| Target | Underlying moves 0.75–1.0× the expected move in your favour. A trailing stop on the underlying once 0.5× is reached. | As above, or an OCO pair (target and stop) on the option |
| Time stop | Flat by 15:50 for 0DTE and 1DTE. For 1–7 DTE, the signal's horizon (the close) or N days. | Time-based order or API job |
| Catastrophe stop | The option loses 50–60% of premium, as a backstop only | A stop-limit on the option inside an OCO |

The 71% containment figure helps set expectations. Measured from 10:00, the close ended outside
1× the expected move on about 29% of days (32% if fairly priced), split between the two directions.
A full 1× target is therefore ambitious without a strong signal. Partial targets at 0.5× need
testing.

## 5. Costs, rules and brokers

- **Commissions** are small next to spreads at 1–2 trades a day:
  - tastytrade: $1 a contract to open, $0 to close;
  - IBKR Pro: from $0.65 a contract;
  - Tradier: $0.35 on Lite, $0 on Pro;
  - Webull: $0.
  - Sources: SQ5 notes.
- **No current measured spreads** by moneyness, expiration and time of day for SPY, QQQ or IWM
  were found.
  - Muravyev & Pearson's "effective spreads about a third smaller" uses a 2003–2006 sample and is
    **outdated**.
    ([RePEc](https://econpapers.repec.org/RePEc:oup:rfinst:v:33:y:2020:i:11:p:4973-5014.))
  - Measure spreads yourself from the backtest data.
- **The pattern-day-trader rule** is replaced by intraday margin standards (FINRA 26-10). Your
  broker may apply the old rule until 2027-10-20.
- **Order support**, from what was verified:
  - **IBKR** supports conditional orders triggered by another contract's price (an
    underlying-triggered option exit) ✓. It also has an API and paper trading.
  - **Schwab** has trigger-then-OCO orders in thinkorswim, through a community API library
    (grade C).
  - **Alpaca** supports single-leg option stop and stop-limit orders, paper trading and an API.
    Bracket and OCO orders on options were not found.
  - **Webull** OCO orders can fill both legs, by its own FAQ. ~
  - Bracket and OCO support at tastytrade, Tradier, Fidelity and Robinhood was **not checked**.
- **[O] Recommendation:** IBKR is the only broker *verified* here for exits driven by the
  underlying's price.

## 6. Data and backtest method

| Need | Option (price as of 2026-11-07) |
|---|---|
| 1-minute or tick option quotes | ThetaData Standard: $80/month, tick quotes (best bid and offer across exchanges), 10 years ✓. Cboe DataShop Option Intervals: 1-minute quotes from 2012, with optional IV and Greeks; price on request. Massive (formerly Polygon) Options Advanced: $199/month, the only *individual* plan with quotes ✓. Business plans are priced separately. Databento: 1-minute quotes, usage-priced. |
| Not enough | ORATS history, which is end-of-day only. Cboe's end-of-day snapshot at 15:45. Trade-only feeds. |
| Underlying minute bars | Any of the above, or broker data |

**Backtest checklist [O, from SQ6 sources]:**
1. Buy at the ask and sell at the bid. Re-run at 50%, 75% and 100% of the spread. ORATS's rule
   of thumb is 75%.
2. Reject stale, crossed and one-sided quotes. Treat a missing quote as no fill, especially
   for 0DTE late in the day.
3. Use only implied volatility, gamma and expected-move values timestamped *before* the entry bar.
4. Fill stop exits at the bid one bar later, not at the trigger price.
5. Hold out 2023–2026 untouched. Use walk-forward testing, and report the number of rule variants
   tried. Deflated Sharpe ratio and probability of backtest overfitting (Bailey & López de Prado)
   apply, but were only seen as SSRN abstracts ~.
6. Cboe changed how it records quote size on 2026-06-22. Expect a structural break in any filter
   based on size.

## 7. Rule cards to backtest first

All four are **[O] hypotheses built from the evidence above**. None has been tested as an option
trade.

| | A. QQQ/SPY opening-range breakout | B. SPY noise-area momentum (first signal only) | C. Last half-hour momentum | D. Stocks-in-Play ORB on large stocks |
|---|---|---|---|---|
| Signal | Direction of the 9:30–9:35 bar; enter at 9:35 | First break of the noise band after 10:00 | Sign of the return from the prior close to 10:00. Enter at 15:30. | Top 1–2 large stocks by unusual opening volume; 5-minute ORB |
| Filter to test | Opening range larger than X% of the expected move; negative dealer gamma | VIX1D or expected-move regime | Only on high-volatility mornings (R² 0.048); negative gamma | News or earnings day (consider skipping because of IV crush) |
| Option | Call or put, delta about 0.6, 1–7 DTE | Delta about 0.6, 1–7 DTE | 0DTE or 1DTE, delta about 0.55 | Delta about 0.6, nearest weekly with more than 3 DTE |
| Stop | Far side of the opening bar (on the underlying) | Back inside the band, or VWAP | 0.3× the remaining expected move | Far side of the opening bar |
| Target | 0.75–1× expected move, or a trailing stop | Trailing on VWAP or the band | None; exit at 15:58 | 1× expected move, or trailing |
| Time stop | 15:50 | 15:50 | 15:58 | 15:50 |
| Evidence | C, weakened (net about 0 in replication) | B, in-sample only | A, weakened out-of-sample | B, in-sample; replicated for 2016 only |
| Main risk | The edge is smaller than the spread plus time decay | It fires more often than you want | A 30-minute hold makes the spread dominant | Wide single-stock spreads and gaps |

**Drop list:**
- Overnight gap fade or continuation.
- GEX or DEX as a direction signal.
- Put-call-ratio triggers on old data.
- Buying 0DTE out-of-the-money "lottery" options.
- Any "win-rate" claim from course or alert services (none checkable).
- The Bali et al. option-return seasonality result (CFR WP 26-02): momentum within the same
  half-day, 0.22–0.45% per half-day, lasting at least 20 business days ✓. It is about
  *delta-hedged* option returns, not a buy-only rule.
  ([RePEc](https://econpapers.repec.org/RePEc:zbw:cfrwps:336775))

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Does the ORB work? | 33% a year on QQQ (Zarattini & Aziz) | Net about 0 across 5 markets (CFD replication) | A: zero slippage, 2016–2023, leverage. B: fixed point costs, 2015–2026. Neither is peer-reviewed. |
| Intraday momentum out-of-sample | Significant out-of-sample (Gao et al., to 2013) | Disappears out-of-sample (Rosa 2022, overnight variant); weak 2015–2020 (QuantConnect) | It fades in later samples. The variants differ. |
| Dealer gamma's effect | Negative gamma means momentum (Baltussen, futures to 2020) | Gamma is too small to matter (Cboe 2023). Another working paper says gamma predicts reversal (snippet only). | Sample and market differ: before and after 0DTE growth, futures and SPX. |
| Do stops help? | Yes, at some frequencies (Kaminski & Lo, futures) | No return gain (Lei & Li, stocks; practitioner futures test) | It depends on whether returns are autocorrelated. Neither tested options. |
| Do option buyers lose? | Yes: Coval & Shumway, retail 0DTE, Vilkov's mean | The 2026 earnings season favoured straddle buyers (ORATS) | One vendor season against the long-run average |
| ThetaData history depth | 6, 10 and 14 years (pricing page today) | 4, 8 and 12 years (older marketing) | The current page is used |

## Outdated or superseded material
- **The pattern-day-trader rule ($25k minimum)** is replaced by FINRA intraday margin standards,
  effective 2026-06-04. Brokers may phase it in until 2027-10-20.
- **Polygon.io** is now **Massive**.
- **TD Ameritrade's API** has moved to the Schwab Trader API.
- **Samples that end before 2022**, before daily ETF expirations: Gao et al. (to 2013), Coval &
  Shumway (1990s), Pan & Poteshman (1990–2001), Muravyev & Pearson (2003–2006), Baltussen
  (to 2020).
- **Cboe's quote-size capture** changed on 2026-06-22.

## Method and limitations
- **Workers:** 7 `researcher` agents in two waves (budgets of 15–20 calls each, 117 tool calls in
  all), 1 `brief-reviewer` and 4 `claim-verifier` batches covering 20 claims. Verdicts: 11
  supported and 9 partial, with fixes applied; none unsupported or contradicted. 70 of 74 evidence
  quotes match their cached pages. The 4 others are marked unverified.
- **Blocked or unreadable sources:**
  - papers.ssrn.com (403). The Zarattini, Beckmeyer, Vilkov and Bailey & López de Prado
    originals were read only through summaries.
  - The page cache can't read PDFs. The Gao, Baltussen, CFR and Fan & Zhang PDFs were read via
    abstracts or summaries.
  - github.com (403).
  - Hosts that returned errors: research.glassnode.com, mdpi.com, carey.jhu.edu, acfr.aut.ac.nz
    (403); dspace.mit.edu (429); schwab.com pricing (authorisation error); IBKR order-type docs
    (503).
- **Main weakness:** most strategy numbers are in-sample working papers or practitioner tests.
  None is an option-level P&L of a signal-timed purchase. The rule cards are therefore designs to
  test, not evidence-backed strategies.
- **Not covered for budget reasons:** macro-release and earnings-open signals, VWAP reversion,
  time-of-day effects, IV skew and term-structure signals, and current measured option spreads.

## Open questions
- What is the option-level P&L of rule cards A–D with bid/ask fills, 2019–2026, on SPY and QQQ?
  This needs a backtest on ThetaData or Cboe 1-minute quotes. It is the single test that would
  change this answer.
- What are the actual SPY and QQQ option spreads by delta, expiration and time of day? Measure
  them from the same data.
- Does negative dealer gamma (properly estimated) improve rules A and C after 2022?
- What bracket/OCO and underlying-triggered order support do tastytrade, Schwab and Tradier
  offer? This needs a direct check of each broker's docs or a paper account.
