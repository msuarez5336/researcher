# Options swing-trade backtest spec: validated v2

*Research run `research/2026-11-06-options-swing-backtest-spec/` · as of 2026-11-06 · tier: STANDARD*

Tags: [E] evidence (documented or measured), [O] opinion or convention, ✓ verified against the
original by a fresh-context claim-verifier, ~ read via a summary or snippet only (unverified).
The change log against the original spec (4 cuts, 7 fixes, 6 additions) is in `spec-review.md`.
Worked examples are in `examples.md`.

## Top findings
1. **Your fill rule is about right, but it contradicted itself. Use k = 0.70 of the spread, and stress-test at k = 1.0.** Muravyev & Pearson measure the average effective option spread as about a quarter below conventional estimates, and below 40% for traders who time their executions. A fill at mid + 20% of the spread is therefore reasonable, not optimistic. [E] ✓ ([RFS 2020 abstract](https://ideas.repec.org/a/oup/rfinst/v33y2020i11p4973-5014..html)) {C6}
2. **"End-of-day" option data is a pre-close snapshot, not the 4:00 pm close.** ORATS takes its snapshot 14 minutes before the close. Cboe DataShop takes one at 15:45 ET and one at the close. Entries and exits must be simulated at the snapshot time, so "15 minutes after the open" needs intraday data. [E] ✓ ([ORATS](https://orats.com/university/historical-data), [Cboe](https://datashop.cboe.com/option-quotes)) {C1, C2}
3. **Not every vendor ships historical Greeks.** ORATS includes IV and Greeks. Cboe sells them as a paid add-on computed at 15:45. Databento's OPRA docs list quotes, trades and statistics but no IV or Greeks fields. Massive (formerly Polygon.io) exposes IV and Greeks only in a live snapshot. With Databento or Massive, plan to compute them yourself with one named American-exercise model. [E] ✓ (C4 narrowed) {C1–C4}
4. **The liquidity filter can use at most the prior day's open interest.** Open interest is not updated intraday, and the OCC posts it the morning after each session. Some vendor feeds lag a further day, so check each record's open-interest date. [E] ✓ narrowed ([Options Playbook](https://optionsplaybook.com/options-introduction/open-interest)) {C5}
5. **A single 60/40 split is not walk-forward, and neither one controls overfitting by itself.** The authors of the probability-of-backtest-overfitting (PBO) paper call hold-out "unreliable and inaccurate" for investment backtests. Count every configuration you try, and report PBO or a deflated Sharpe ratio. [E] ✓ ([Bailey et al.](https://scholarworks.wmich.edu/math_pubs/42)) {C9}
6. **The usual "30 / 100+ trades minimum" has no primary source.** Treat it as a convention you set in advance, not a statistical guarantee. [O] ~ ([forum](https://www.elitetrader.com/et/threads/minimum-number-of-trades-required-for-backtesting-results-to-be-trusted.356588/page-2))
7. **The 50%-profit and 21-DTE management rules are vendor conventions, not published measurements.** tastylive calls 50% the "sweet spot" but shows no figures on the pages we read. Keep both rules, but treat them as parameters in the sensitivity grid. [O] ([tastylive](https://www.tastylive.com/definitions/managing-winners))
8. **All-in cost is about $0.70 per contract per side at a $0.65 broker.** IBKR Pro charges $0.65 for premiums of $0.10 or more (less on cheaper options), plus OCC clearing of $0.025. The SEC fee on sales is $20.60 per $1M. The FINRA options trading activity fee (TAF) is $0.00329 per contract but is paused from Oct to Dec 2026. [E] ✓ (C7 narrowed) {C7, C8}

## The v2 spec (hand this to the backtest builder)

**Phase 1: Hypothesis and universe**
- Universe: SPY, QQQ, and S&P 500 members *as of each historical date* whose options trade more than 10,000 contracts a day.
- One hypothesis per test. One catalyst (mean reversion, volatility-contraction breakout, or post-earnings drift) and one structure: **long premium only** (a 0.60–0.70Δ single leg or a 0.50/0.25Δ debit vertical). Credit spreads are a separate hypothesis with their own rules.
- Max hold **10 trading days**.
- **Write before running:** pass/fail gates (Phase 5), sizing (risk a fixed % of equity at max loss, i.e. the debit), max concurrent positions, max per underlying, and a **shares-only baseline** with the same signal.

**Phase 2: Data**
- Point-in-time chains with **bid/ask (NBBO)**, never last trade. Record the snapshot time and execute at it.
  - ORATS: near-EOD ~15:46 ET, 2007+, IV and Greeks included. 1-minute data from Aug 2020.
  - Cboe DataShop: 15:45 ET and close, 2012+, IV and Greeks as an add-on.
  - Databento OPRA: raw quotes. Data before 2023-03-28 is subsampled.
- IV and Greeks: use the vendor's if supplied. Otherwise compute them with **one** American model (e.g. Bjerksund-Stensland 2002), with a named risk-free curve and dividend input. Never mix vendor and self-computed values.
- Events: historical earnings dates, ex-dividend dates and amounts, delisted tickers, historical index membership. Use unadjusted underlying prices for strike and Δ maths. Exclude adjusted (non-standard) contracts.
- Open interest = the latest value dated before the entry day (at best T−1; check the record's OI date).

**Phase 3: Contract selection**
- Expiry: **35–60 DTE**, choosing the one nearest 45.
- Strike: by Δ, as in Phase 1. Reject the trade if no strike falls in the Δ band.
- Liquidity: bid-ask spread ≤ 5–8% of mid and prior-day OI ≥ 500, **on every leg**.

**Phase 4: Entry, management, exit**
- The signal comes from the underlying at bar *t*, e.g. close > 20-EMA and IV Rank < 30. Execution happens at the next available snapshot (EOD data) or at a fixed intraday time (intraday data only).
- Exits are checked at each snapshot. **Priority when several fire: Event > Stop > Time > Profit.**
  - Event: close 1 trading day before earnings, unless the hypothesis is about earnings.
  - Stop: the underlying crosses the invalidation level. Backstop: option value at −50% of the debit. A gap through the stop fills at the next quote, not at the stop level.
  - Time: 10 trading days held, or DTE < 21.
  - Profit: debit spread at 50% of max profit. Single leg at +35% of premium. Both are grid parameters.
- Before each ex-dividend date, close any short call that is ITM when its extrinsic value (≈ the same-strike put's price) is below the dividend. With a 21-DTE floor and debit structures this is the only assignment rule needed. The expiration-day pin rule never fires.

**Phase 5: Simulation and validation**
- Fills: buy at bid + k·(ask−bid), sell at ask − k·(ask−bid), **per leg**. Base k = 0.70. Stress k = 1.0. Optimistic k = 0.5 is reported but never used for a decision. Costs: $0.65 commission plus ~$0.05 fees per contract per side, or your broker's schedule.
- Splits: rolling walk-forward (e.g. 3 years train / 1 year test, stepping 1 year), plus a final holdout that is never touched. Name the regimes each test window covers (2008, 2018-Feb, 2020-Mar, 2022).
- Sensitivity grid: DTE {35, 45, 55} × Δ {0.40, 0.50, 0.60} × profit target {25, 35, 50%}. Accept only a plateau, not a single peak.
- Overfitting control: log every configuration tried. Report PBO (via combinatorially symmetric cross-validation, CSCV) or a deflated Sharpe ratio across all trials.
- Pass gates, all at k = 1.0 out of sample:
  - expectancy > 0 after costs
  - profit factor ≥ 1.3
  - ≥ 100 trades (30 is the floor)
  - positive in ≥ 2 of 3 named regimes
  - beats the shares-only baseline on risk-adjusted return
  - max drawdown within your stated limit

## Evidence by theme

### Data: what "point-in-time" means per vendor
- ORATS documents a near-EOD dataset with full chains, Greeks, theoretical values and IVs, "gathered 14 minutes before the close", from 2007. One-minute intraday chains start in August 2020. These are vendor descriptions of the vendor's own data (self-reported). ORATS's underlying price is derived from option prices through put-call parity, not taken from the stock tape ([ORATS docs](https://orats.com/docs/historical-data-api)). Use a separate equity price source for the underlying signal. [E] {C1}
- Cboe DataShop's Option EOD Summary carries NBBO bid/ask with size at 15:45 and at the close, from January 2012. IV and Greeks are an add-on, computed at 15:45 only. Open interest sits in the EOD record. [E] {C2}
- Databento's OPRA data gives non-standard contracts a numeric suffix (e.g. MSFT1), which makes them easy to exclude. Data before 2023-03-28 is subsampled, and cbbo-1m is the finest BBO there. Its docs list top-of-book quotes, trades and statistics, with no IV or Greeks fields. The absence of IV/Greeks is our inference from that list, not a Databento statement. [E] ✓ partial {C4}
- Massive (Polygon.io renamed on 2025-10-30, [Massive blog](https://massive.com/blog/polygon-is-now-massive)) puts IV and Greeks in a current-state snapshot endpoint with no plan history. That is consistent with Massive's own skill text: "Historical Greeks and IV do not exist on any plan." [E] {C3}
- ThetaData lists Binomial Greeks and EOD Greeks endpoints. Its 2012 start date and 17:15 ET EOD generation time were read only in a search summary. [E/~]
- **Not found:** which pricing model ORATS or Cboe use, price tiers, and how ORATS, Cboe and ThetaData handle expired or delisted contracts. Ask the vendor before you buy.

### Execution costs
- Muravyev & Pearson (RFS 2020): "effective spreads … for traders who time executions are under 40% of conventional measures", and the overall average effective spread is about a quarter smaller than conventional estimates. A secondary summary puts conventional effective spreads at about 80% of the quoted spread. That would put the average trade at roughly k ≈ 0.6–0.8 under our convention. The full-vs-half-spread definition behind that summary is ambiguous, which is why the spec stress-tests at k = 1.0. [E] {C6}
- No source we reached measures fills on retail-only or multi-leg orders. Using k ≥ 0.8 for wide-spread names and multi-leg orders is a judgement call. [O]
- Commissions seen 2026-11-06:
  - IBKR Pro: $0.65 at ≤10k contracts a month for premiums of $0.10 or more ($0.50 for $0.05–0.10, $0.25 below $0.05), $1 order minimum, OCC clearing $0.025.
  - Fidelity: $0.65, plus $0.50 extra for accounts classed as professional options traders.
  - tastytrade: $1 to open, capped at $10 per leg, $0 to close.
  - Robinhood: $0 commission, plus a $0.04 OCC/options regulatory fee (ORF) pass-through. Its fee page gives the SEC fee as $20.60 per $1M of sales since 2026-04-04, and the TAF as $0.00329 a contract on sells, paused 2026-10-01 to 12-31 ([FINRA schedule](https://www.finra.org/rules-guidance/rule-filings/sr-finra-2024-019/fee-adjustment-schedule)). [E] {C7, C8}

### Validation
- PBO paper (J. Computational Finance, 2017): hold-out is "unreliable and inaccurate" for investment backtests. The authors propose CSCV to estimate the probability that the chosen configuration is overfit. [E] {C9}
- Deflated Sharpe ratio: it adjusts an observed Sharpe ratio for the number of independent trials, the non-normality of returns and the sample length. It is implemented in R's `quantstrat` (`deflatedSharpe`). [E] {C9}
- López de Prado, via a secondary summary, argues that a simple walk-forward is a single path and can itself be overfit by re-running it, and that 20 walk-forward attempts likely produce one false 95% strategy. That is why the spec requires counting trials, not only splitting data. [O] ~

### Assignment and management
- Early exercise of an ITM American call just before the ex-date makes economic sense **only when** its remaining extrinsic value is below the dividend. In practice, check the same-strike put's extrinsic value. This is a necessary condition, not a sufficient one, so the spec's force-close rule is deliberately conservative. A short deep-ITM call in that state faces elevated assignment risk the day before the ex-date. Read via exam-prep material, and via a Schwab page reached only as a search snippet. No primary source (OCC, Hull) was reached. [E] ✓ narrowed {C10}
- tastylive's own pages describe closing winners at 50% as the long-run "sweet spot", with a risk/reward rationale and no figures. 21 DTE is widely attributed to tastylive, but we found no measured study. [O]

## Where sources disagree
| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Walk-forward vs hold-out | Practitioners: walk-forward is the standard OOS test | López de Prado / Bailey et al.: both are single-path and overfit-prone unless trials are counted (PBO/DSR) | Walk-forward is fine for one pre-registered configuration. Once you search a grid, add PBO/DSR. |
| Realistic k | Average trade ≈ 0.6–0.8 (the RFS paper and a summary of it) | Timed executions < 0.4 of conventional | k ≈ 0.5 holds only with patient limit orders in liquid names. Use 0.7 base and 1.0 stress for decisions. |

## Outdated or superseded material
- **Polygon.io → Massive** (2025-10-30). `POLYGON_API_KEY` is a deprecated alias of `MASSIVE_API_KEY`, per Massive's skill.
- **FINRA TAF** steps up each year ($0.00279 in 2024–25, $0.00329 in 2026, $0.00390 next) and is paused from Oct to Dec 2026. Re-check the rate at run time.
- **"OPRA" as a provider** (original spec): OPRA is the consolidated feed. The vendors above redistribute it.

## Method and limitations
- 3 `researcher` agents (≤15 calls each; 14, 16 and 14 used), plus 2 orchestrator gap-fill searches, plus 2 `claim-verifier` batches (10 claims: 6 supported, 4 narrowed to the verifier's wording, 0 refuted). 34 evidence items: 31 quotes matched their cached page, and 3 are labelled unverified.
- Blocked or unreadable: theocc.com (403), papers.ssrn.com (403), core.ac.uk (403), optionsclearing.com (connection reset), massive.com options overview (404), Schwab pages (thin), several PDFs (unsupported by the fetcher). As a result, the DSR/CSCV formulas, the OCC's own open-interest timing text, and Hull's early-exercise derivation were not read from primary sources. The conclusions above rely on abstracts, vendor docs and secondary summaries for those points.
- Vendor descriptions of their own data (ORATS, Cboe, Databento, Massive) are self-reported.
- Not researched: IVolatility. Evidence on whether any of the catalysts carries an edge was out of scope.

## Open questions
- Which American-exercise model, rate curve and dividend treatment does ORATS (or Cboe) use? Ask the vendor. It decides whether vendor Greeks and self-computed Greeks can be compared.
- Measured fill ratios for multi-leg retail orders. Bogousslavsky & Muravyev, "Anatomy of Retail Option Trading", is the likely source and was not retrieved.
- Does any tastylive study with published numbers support 21 DTE for long debit structures, as opposed to short strangles?
- Artifact: https://claude.ai/artifact/4wyLfiaCYxCN2V77Cz5ihs (private; source in `artifact/index.html`).
