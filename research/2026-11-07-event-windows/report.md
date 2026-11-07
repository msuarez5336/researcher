# When do long-option opportunities open? Macro events, regimes and post-catalyst reversal

*Research run `research/2026-11-07-event-windows/` · as of 2026-11-07 · tier: STANDARD · earnings
excluded (user decision) · builds on `../2026-11-07-long-vol-tickers/` and the v2 spec in
`../2026-11-06-options-swing-backtest-spec/`*

Tags: [E] evidence, [O] opinion, ✓ verified by a fresh-context claim-verifier, ~ summary or snippet
only. [S] = this run's event study (`study/`): Nasdaq daily data 2016-11 → 2026-11, Cboe vol
indices, SqueezeMetrics GEX, Fed FOMC calendar. Options are priced with Black-Scholes at the index
IV and repriced at exit. In-sample (IS) is 2016-11 → 2021-06, out-of-sample (OOS) is 2021-07 → 2026-11.
"Excess" = return minus the same option bought on random days.

## Answer first: the opportunity calendar

| Window | How to spot it in advance | What we measured [S] (OOS unless stated) | Prior evidence | Status |
|---|---|---|---|---|
| **Single-stock shock, non-earnings, VIX in its middle third** | ticker's daily move > 2.5σ, no earnings that day or the day before, VIX in the middle tercile; buy the reversal side, hold 10 days | ATM +20 pts excess (t 2.6, n 103); 0.50/0.25 spread +16 pts (t 3.3). Same sign in-sample | Reversal after no-news moves ✓ {C3}, but large liquid stocks tend to continue ✓ {C1} | **Lead, unconfirmed.** It is likely a multiple-testing false positive (2 of ~81 eligible cells, about the chance rate) and is inflated by the IV proxy (below). Reprice with chain IV before using it. |
| **FOMC day (straddle)** | scheduled FOMC statement day | 1-day straddle at implied: SPY −2% (VIX9D), QQQ +7%, against −19% / −16% on other days. Excess +18 / +23 pts, t 1.3 / 1.8. In-sample strongly negative (−39%). With VIX1D (2022+): −4%, t 0.4 | Index straddles lose around macro releases *except* FOMC ✓ {C5}; a recent piece says FOMC was overpriced in 10 of 12 events ~ | **Watch.** It worked after mid-2021 (the hiking cycle) but not before. Regime-dependent, not a standing edge. |
| **Post-FOMC reversal** | FOMC-day move > 1.5σ; buy the reversal side at the close | ATM 3-day +29% (excess +31 pts, t 2.1, n 30); spread 3-day +10% (t 2.1). In-sample negative (−11%, n 9) | FOMC-day reversal on E-minis +0.18% per event, 1997–2020 ✓ {C10} | **Watch.** Fails the in-sample sign check, with a tiny in-sample n. Re-test with intraday entry. |
| **Pre-FOMC drift (calls)** | buy an ATM call at the close the day before FOMC | −0.9% net, excess ≈ 0 | The drift "essentially disappeared after 2015" ✓ {C4} | **No edge** (confirmed). |
| **Dealer short gamma (GEX < 0)** | SqueezeMetrics GEX < 0 | 10-day straddle at implied: −31%, excess −7 pts. In-sample it was +19% | GEX adds no information once VIX and IV are controlled ✓ {C6} | **No edge.** The sign flipped between halves. |
| **Volatility-shock onset** (VIX jump from calm, full term-structure inversion, VVIX ≥ p90) | Cboe index states, first day | 4–29 events per state. Mixed: QQQ 5-day after inversion +17% (t 1.4), SPY VVIX 10-day −20%. In-sample VVIX was +43% | VIX lags realised at a panic's onset, then overshoots ✓ {C7} | **Inconclusive.** Too few events, and no state held up in both halves. |
| **Buying the bounce after an index shock day** | SPY/QQQ/IWM move > 2.5σ; buy the reversal side | ATM 10-day: −24%, **excess −21 pts (t −3.5)**; spread −16% (t −2.4). The price kept going (−0.9% over 10 days) | Liquid assets continue rather than reverse ✓ {C1} | **Avoid.** The most robust result in the study is negative. |
| **After a VIX spike (+30% in ≤ 3 days)** | Cboe VIX | ATM/spread excess −4 to +4 pts, not significant. IV falls afterwards | IV mean-reverts. A vendor's "+5% SPY after IV spikes" rests on 9 spikes and loses significance without overlap ✓ {C9} | **No edge for options.** The bounce, if any, is paid for by IV decay. |

**Bottom line:**
- No episodic window cleared the frozen bar in a way that can be told apart from chance.
- What the data does show with confidence:
  - **Implied vol falls after shocks** (−1.1 to −1.6 vol points over 10 days, against ≈ 0 on random days). That drag is what kills long calls/puts bought for a rebound. In the losing reversal cells, debit spreads lost less than single legs (e.g. index shock days, 10 days: −16% vs −24%).
  - **Buying the bounce after a big index down-day loses money.**
- The three leads worth confirming with real option-chain data:
  1. Non-earnings single-stock shocks in mid-VIX regimes.
  2. FOMC-day straddles in a hiking or cutting cycle.
  3. Post-FOMC reversal, with intraday entry.

## Why the leads are weak
- **Multiple testing.** This run scored 343 cells (348 trials including the previous run). Of the ~81 cells eligible for the bar (k = 0.70 costs, n_OOS ≥ 20), 4 reached t ≥ 2 with ≥ 10 points of excess, and chance alone would give about 2–4. Meanwhile 11 cells were significantly *negative*.
- **The IV proxy flatters single-stock reversals.** For the 13 stocks without a Cboe index, IV was proxied by 20-day realised vol plus 3.4 points. The shock day stays inside that 20-day window at both entry and exit, so the proxy can't show post-shock IV decay. On indexed stocks the decay is real (−1.1 points over 10 days, C3). The proxy split itself is unremarkable (+3 pts excess, t 0.5), and indexed names alone show +9 pts (t 0.9, n 55).
- **Mechanism mismatch.** The literature says reversal profits rise with VIX (Nagel ✓ {C2}). Our only positive cell is the *middle* VIX tercile. The high tercile shows −2 pts.

## Evidence by theme

### Post-catalyst mean reversion
- **Reversal vs momentum.** Medhat & Schmeling (RFS 2022) find one-month reversal concentrated in low-turnover stocks, while high-turnover stocks, strongest among the largest and most liquid, show short-term *momentum*.
  - Large-cap reversal earned 0.84%/month gross, against 1.41% in small caps.
  - Across the full sample, the average monthly transaction cost of 1.94% wiped out the strategy's gross return. These figures come from the Alpha Architect summary.
  - [E] ✓ narrowed {C1}
- **News vs no news.** Large moves *without* analyst recommendations reverse; those *with* them drift (Savor 2012). [E] ✓ {C3} Chan (2003) on news vs no-news was read by title only. [E] ~
- **VIX dependence.** Reversal and liquidity-provision returns are highly predictable with VIX (Nagel, RFS 2012). [E] ✓ {C2}
- **Our data.**
  - Index shock days continued rather than reversed: −0.2% after 1 day, −0.9% after 10.
  - VIX-spike days reversed slightly: +1.1% after 10 days.
  - Non-earnings single-stock shocks reversed about +0.1–1.1% after 10 days in mid and high VIX, and continued in low VIX (−2.1%).
  - [S]
- **Implied-vol decay after shocks.** IV fell −1.56 pts over 10 days after index events and −1.10 after indexed single-stock events, against about +0.05 on random days. [S] Literature: index IV adjusts gradually after jumps (Kanniainen & Magris). [E] ~

### Macro events
- **Pre-FOMC drift.** Lucca & Moench: over 80% of the equity premium since 1994 was earned in the 24 hours before FOMC. The drift "essentially disappeared after 2015" (Kurov, Wolfe & Gilbert 2021). [E] ✓ {C4} Our 2016–2026 data agrees: ≈ 0. [S]
- **Macro straddles.** Index straddles lose around macro announcements, with FOMC the exception (OptionMetrics summary). [E] ✓ {C5} Ours: FOMC straddles were much worse than other days before mid-2021 and better after. [S]
- **FOMC-day reversal.** Baglioni & Ribeiro (via CXO Advisory): +0.18% net per event, Sharpe 0.36, 1997–2020. [E] ✓ (secondary only; the SSRN original is blocked) {C10}
- **CPI and payrolls:** untested. No reachable release-date history (bls.gov 403).

### Market structure and regimes
- **Dealer gamma.** Raw GEX correlates with next-day realised vol (ρ ≈ −0.36). The relationship vanishes after controlling for VIX and ATM IV (−0.03, p 0.18) in a practitioner backtest. [E] ✓ {C6} Ours: GEX < 0 straddles were +19% in-sample and −31% out-of-sample. [S]
- **Shock onset.** In 2008, realised vol ran above VIX from July to November, then VIX overshot in early 2009. In panics VIX lags, then overreacts. [E] ✓ {C7} Ours: too few onset events since 2016 (4–29 per state) to conclude. [S]
- **After VIX spikes.** Man Group's top-20 spikes: when the S&P rose in the week after a spike, the second week was negative on average. [E] ✓ {C8} IVolatility's "+5.12% SPY over 20 days after IV spikes" rests on 9 spike days (2021–2026) using its own SPY IV index, and is not significant with non-overlapping windows. [E] ✓ {C9}

## v2 spec addendum: confirmation tests (not trading rules)
Run these only with chain data (ORATS), so that IV, skew and spreads are real. Each one is a
new pre-registered trial, and the count starts at 348.
1. **H-C2m: non-earnings single-stock shock, mid-VIX.** Trigger: |r| > 2.5σ60, no earnings on t or t−1, VIX in the 1/3–2/3 tercile of its trailing 10 years. Buy a 0.50/0.25Δ debit spread on the reversal side, 35–60 DTE, at the close. Exit at day 10, at +50% of max, or at a close beyond the shock-day extreme. Universe: the 10-ticker shortlist plus the 16 stocks here. Pass: the v2 gates **and** beating random-date spreads by ≥ 10 points at k = 1.0.
2. **H-FOMC: FOMC-day straddle and post-FOMC reversal.** Straddle bought at the close before the statement, sold at the close after. Reversal: buy the opposite side at the FOMC-day close when the move > 1.5σ, and hold 3 days. Report each policy cycle separately (hiking, holding, cutting).
3. **Structure rule for any post-shock long option:** default to a debit spread. Post-shock IV falls, and in the losing reversal cells single legs lost more than spreads. Single legs only did better where the price reversal was strong.

## Where sources disagree
| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Do big moves reverse? | Yes for no-news moves, more so in high VIX (Savor, Nagel) | Large liquid stocks continue (Medhat & Schmeling); our index shock days continued | Reversal: small, illiquid stocks, no-news moves. Continuation: liquid ETFs and megacaps, which are what we can trade with options. |
| FOMC straddles | Positive (OptionMetrics summary) | Overpriced in 10 of 12 recent events (Nasdaq piece ~) | Depends on the cycle. Ours were negative 2016–21 and near zero or positive 2021–26. |
| Pre-FOMC drift | Persists (Ignatieva & Ohashi 2025 ~; NY Fed 2018 ~) | Disappeared after 2015 (Kurov et al. ✓) | Our data agrees with "disappeared" for close-to-close SPY calls. |

## Follow-up: buying *with* the move (continuation), 2026-11-07
Spec, script and results: `continuation/` (spec frozen before the run). Same 19 tickers, earnings
excluded, artifact not updated.

**Question:** after a large move, does buying a short-dated call (up move) or put (down move) pay,
and when should you exit?

**Defining "large":** the day's move ≥ k × the ticker's own 60-day daily σ (move day excluded),
with k = 2.0, 2.5 or 3.0. The quality filters were close strength, volume ≥ 2× average, gap vs
intraday, stock-specific vs market-wide, and the VIX tercile over the trailing year.

**Result: no rule passed the pre-registered bar. There is a regime-dependent single-stock lead.**

| Finding | 2016-11 → 2021-06 | 2021-07 → 2026-11 |
|---|---|---|
| Price after a 2.5σ stock move, day 1 (move direction) | −0.5% (reversal) | **+0.5% (continuation)** |
| Price after a 2.5σ ETF move, day 1 | +0.1% | +0.3% |
| Stocks, 2.5σ moves: buy at the move-day close (ATM 7/14/30 DTE or 0.30Δ 14 DTE), sell at the next close, vs random days (k = 0.70) | −4 to −5 pts | **+5 to +12 pts (t 2.4–2.7)** |
| Same, 3σ moves | −5 to −6 pts | +7 to +17 pts (t 2.3–2.6) |
| Stocks, *confirmed* entry (wait for day 2 to continue), 1–2 day holds | mixed (−18 to +8 pts) | −2 to −12 pts |
| ETFs, any structure or exit | mostly t < 1 | no cell with t > 1.7 |

**Exit rules (stocks, move-day-close entry, mean over structures and k, 2021–26 excess at k = 0.70):**

| Exit | Excess | t (avg) | Win rate |
|---|---|---|---|
| **Sell at the next close (1 day)** | **+8.8 pts** | **2.4** | 48% |
| 2 days | +7.5 | 1.3 | 45% |
| 3 days | +7.6 | 0.9 | 42% |
| 5 days | −0.6 | 0.0 | 35% |
| First green close | +7.7 | 1.2 | **68%** |
| Green + 1 day | +4.6 | 0.3 | 49% |
| Green + 2 days | +4.5 | 0.5 | 42% |
| +30% target / −40% stop | +8.7 | 1.4 | 46% |
| Trail (exit when the stock turns against you) | −0.5 | −0.4 | 41% |

- **The edge, where it exists, is in the first day.** Holding longer, letting a winner run one or two more days, or trailing all gave it back. Waiting for confirmation misses it entirely, because the continuation happens *on* day 1.
- **"First green" wins most often** (68%) but makes about the same on average. The losers that never turn green ride to day 5.
- **Bigger moves pay more per trade:** about +3–7 pts at 2σ, +5–12 at 2.5σ and +7–17 at 3σ, but with fewer events.
- **Filters (2.5σ, ATM 14 DTE, 1-day hold, 2021–26):**
  - Stock-specific moves: +16 pts (t 2.6). Market-wide: +1.
  - Volume ≥ 2×: +18 (t 2.6). Normal volume: +4.
  - Strong close: +9 (t 2.7). Faded close: +2.
  - VIX low or mid: +15 / +19. **VIX high: −3.**
  - In 2016–21 the same filters were mostly flat or negative. Low VIX was +4 pts, on 28 events.
- **Year by year** (2.5σ stocks, ATM 14 DTE, 2-day hold): 2017 −9%, 2018 −21%, 2019 −26%, 2020 +11%, 2021 −1%, 2022–24 +2% to +4%, 2025 +7%, 2026 +16%. The sign changed around 2020.
- **Multiple testing:** 1,188 cells (cumulative 1,536 trials). One cell passed: OTM 0.30Δ 14 DTE, first-green exit, stock-specific moves. Chance would produce about that many at t ≥ 3.
- **Literature fit:** this is consistent with liquid stocks showing short-term momentum (Medhat & Schmeling ✓) and news-driven moves drifting (Savor ✓; high volume as the news proxy). It doesn't explain why 2016–19 reversed.

**Hypothesis to forward-test (not a trading rule): H-MOM1.**
- **Trigger:** a single stock (shortlist universe, no earnings on t or t−1) moves ≥ 2.5σ60, stock-specific (|SPY| < 1σ), on volume ≥ 2× its 20-day average, closing in the top/bottom 20% of its range in the move's direction. VIX must be below the top tercile of its trailing year.
- **Trade:** buy an ATM 14-DTE call/put in the move's direction at the close. Sell at the next close.
- **Test:** this combination was *not* run, so it is one new trial (#1,537). Run it on chain data (ORATS bid/ask at the close snapshot) and paper-trade forward. It passes only if out-of-sample excess ≥ 10 pts with t ≥ 3 at k = 1.0, and only if 2016–21 isn't negative on chain data.

**Limits:**
- Daily closes only. A real "next close" exit is fine, but intraday targets would fill differently.
- Short-dated IV is approximated by the 30-day index × VIX9D/VIX. 7-DTE single-stock spreads are often wider than the assumed 3%, although results hold at k = 1.0.
- The non-indexed stock IV uses a proxy with an empirical decay table. Results were similar on indexed names (+6.8% vs +5.8% for the proxied names, 2-day hold, 2021–26).

## Method and limitations
- **Effort:** 3 researchers (≤15 calls each); one stdlib event study (`study/events.py`) with a spec frozen before the run (`study/study_spec.md`); 2 claim-verifier batches (10 claims: 9 supported, 1 narrowed).
- **Prices:** the Nasdaq API serves only about 10 years, so the study covers 2016-11 → 2026-11. 2008 and 2011 are outside it, and so is any regime-onset sample of decent size.
- **Option pricing:** Black-Scholes at constant-maturity vol indices (30-day, 9-day, 1-day). No skew, no dividends, r = 0. Spreads were assumed at 3% of mid. The single-stock IV proxy is biased, as shown above.
- **Look-ahead in one conditioner:** VIX terciles (15.0 / 19.5) were computed over the whole 2016–2026 sample, as the frozen spec said. A live rule must use trailing terciles, and H-C2m's confirmation test does.
- **Not tested:** CPI and payrolls (no date source), intraday entries, and earnings (excluded by request).
- **Blocked:** papers.ssrn.com, core.ac.uk (403); PDFs (NBER, NY Fed, JFQA) that the fetcher can't parse; bls.gov (403); efmaefm.org (503).
- Artifact: https://claude.ai/artifact/4wyLfiaCYxCN2V77Cz5ihs, section "When opportunities open" (private).
