# Same-day long options on liquid US underlyings: when, if ever, do they pay?

*Research run `research/2026-11-07-intraday-long-options/`, as of 2026-11-07, tier STANDARD. Earnings
are excluded (standing decision). This run builds on three prior runs, all on branch
`claude/inspiring-cerf-epxwvd` (cited, not merged): the v2 spec
`research/2026-11-06-options-swing-backtest-spec/`, `research/2026-11-07-long-vol-tickers/` and
`research/2026-11-07-event-windows/`.*

**Tags:**
- **[E]** evidence: a measured result, with its number and setup.
- **[O]** opinion or convention.
- **[S]** this run's pre-registered study (`study/`).
- **✓** verified against the source by a fresh-context claim-verifier; **~** read only via a summary or snippet.
- **{C#}** claim id in `claims/` and `verdicts/`.

**Study basics [S]:**
- Data: SPY and QQQ hourly bars with hourly VIX1D, 2024-01-22 → 2026-11-06. In-sample (IS) runs to 2025-05; out-of-sample (OOS) is 2025-06 → 2026-11, 357 sessions.
- Option prices are **modelled** (Black-Scholes at VIX1D), not observed.
- Costs per leg: base k = 0.70 (pay mid + 0.2 × the quoted spread), stress k = 1.0 (pay the full quoted spread), plus $0.70 per contract per side. The quoted spread is the larger of $0.01 and 3% of the option price, or 4.5% at the open and after 15:00.
- "Excess" = the cell's net return minus the same trade at the same clock time on non-trigger days (or at other clock times, for time-of-day cells), in points of premium.
- 428 trials, #1,538–#1,965.

## Answer first: the intraday opportunity table

| Window | Trigger | Structure | Exit | Evidence (measured [S] / prior [E]) | Status |
|---|---|---|---|---|---|
| **Open hour, volatility** | none (every day) | 0DTE ATM straddle, 09:30 | 10:30 | [S] OOS excess **+12.7 pts SPY (t 8.1), +19.7 pts QQQ (t 10.2)**. Same sign IS, holds at k = 1.0. These are the only two passes of the bar. The 1DTE version is weak (+1 / +4.6 pts). Diagnostics show the gain comes from the model's even time decay (a flat clock), while the first hour carries 23–34% of the day's realised variance against a 15% clock share. Real option prices probably charge for that. | **Untestable on free data** (artefact suspected). First test on chain data (H-OPEN1). |
| **Gap fill** | \|gap\| ≥ 1σ of 60-day gaps | 0DTE ATM call/put against the gap, or a debit spread | first profit, or 15:30 | [S] SPY: mean excess +8 to +10 pts over 40 cells, best t 2.05 (ATM, 09:30 entry, first-profit exit +16.7 pts, t 1.6). QQQ +3 to +9 pts. IS same sign but small. No rigorous literature found. | **Watch** |
| **Gap-and-go** | same | 0DTE in the gap direction | any | [S] SPY: mean excess −11 to −15 pts; 14 of 40 SPY cells have t ≤ −2. QQQ −2 to −10 pts. | **Avoid** (SPY), no edge (QQQ) |
| **First-hour continuation (ORB-like)** | \|r(09:30→10:30)\| ≥ 60-day median | 0DTE ATM in the direction, at 10:30 | 15:30 | [S] SPY ≈ 0 (mean excess +0.5 pts). QQQ ATM +11 pts OOS (t 1.1), IS +40 pts (t 2.9). [E] The ORB working papers report large gains with zero spread or slippage; an independent net-of-cost replication got about 0 out of sample ✓ (narrowed) {C9}. | **Watch** (QQQ), no edge (SPY) |
| **First-hour fade** | same | against the move | any | [S] mean excess −2 pts, no cell with t > 0.9 | **No edge** |
| **Intraday momentum (last half-hour)** | sign of r(prior close→10:30) | 0DTE in that direction, 15:30 | 16:00 | [S] excess ≈ 0 (SPY −0.8, QQQ +0.2 pts); absolute about −25% to −43% per trade at k = 0.70. [E] Gao et al. SPY 1993–2013 ✓; later checks weak ✓ {C6, C7}. | **No edge** (for options: the move is too small for 30-minute theta and spread) |
| **08:30 CPI/NFP, intraday** | release day | 0DTE/1DTE straddle bought at 09:30 | 10:30 / 12:30 / 15:30 | [S] excess −5 to +6 pts, all t < 1 (n_OOS 31) | **No edge** after the release |
| **08:30 CPI/NFP, through the release** | release tomorrow | 1DTE straddle from the prior close | next-day close | [S, descriptive] SPY realised/implied close-to-close variance was 1.26 OOS and 1.06 IS on CPI/NFP days, vs 0.95 / 0.86 on all days. The prior-close VIX1D underpriced these days on average, but realised beat implied on only 25% of them. | **Watch** (needs chain data; it isn't a same-session trade) |
| **10:00 ISM** | release day | straddle 09:30 | 10:30 / 12:30 | [S] excess −2 to −8 pts | **No edge** |
| **FOMC statement and press conference** | FOMC day | 0DTE straddle 13:30, or the fade of the 13:30→14:30 move | 15:30 | [S] SPY straddle 13:30→15:30 +26 pts OOS (t 1.6), IS +57. Fade ATM +47 pts OOS but IS −5. Only n_OOS = 13, so ineligible. [E] Powell press conferences carry more than 3× the volatility of his predecessors' and tend to reverse the statement move ✓ {C13}. | **Watch** (underpowered; needs minute data to split 14:00 from 14:30) |
| **Midday lull** | none | 0DTE/1DTE straddle 11:30 | 13:30 | [S] SPY excess +5.5 pts (t 3.4) vs other hours, but the absolute return is −4% (0DTE); below the 10-point bar | **No edge** |
| **Power hour / last half-hour, volatility** | none | 0DTE straddle 14:30 or 15:30 | 15:30 / 16:00 | [S] excess −27 to −30 pts (t −10 to −23); absolute −30% to −37%. Partly a model effect: VIX1D is frozen from about 15:00 and leans on next-day options. [E] Spreads widen into the close ✓ {C2, C15}. | **Avoid** |
| **Monthly OpEx (pinning)** | third Friday | straddle 10:30 / 13:30 | 15:30 | [S] vs other Fridays: −8 to +1 pts, n.s. Realised/implied variance at the open was lowest on OpEx (0.70–0.72). [E] Dealers keep positive net gamma on expiration day, and 0DTE dampens volatility on average (Adams et al.) ✓ narrowed {C11}. Cboe (2023): no discernible impact {C12}. | **Avoid** (long vol on OpEx); no edge |
| **Day after an H-MOM1 move** | H-MOM1 trigger (single stock, 2.5σ, stock-specific, volume ≥ 2×, strong close, VIX not high) | ATM 7–14 DTE in the move direction, entry at the prior close vs the next open | next close | [S] OOS (2021-07 → 2026-11, n 27): the next day returns +2.9% (t 3.6), of which +0.9% overnight and **+2.1% open→close** (t 2.9). Options: close entry +43 pts excess (t 3.2), open entry +29 pts (t 2.8). **IS (2016–21) excess is negative (−7 to −12 pts)**, so it fails the bar. | **Watch** (regime-dependent; the open entry keeps about two-thirds of the edge) |

**Bottom line:**
- Across 342 eligible cells, no directional same-day long-option rule on SPY or QQQ cleared the pre-registered bar.
  - 18 cells had t ≥ 2 and 28 had t ≤ −2, which is about what chance plus a few real negatives would give.
  - The two passes are the open-hour 0DTE straddle on SPY and QQQ. They rest on modelled prices in exactly the place where the model is weakest (how a 0DTE option decays through the first hour), so they are a hypothesis for chain data, not an edge.
- Of the external evidence, the most robust is about cost, not edge. ATM SPX 0DTE options cost about 9% of premium per round trip in effective spread (2004–21) ✓ {C1}. Retail 0DTE buyers lost 53–61% per position on average ✓ {C4}.
- Worth a paid test, in order:
  1. The open-hour straddle (to kill or confirm the artefact).
  2. Gap fill.
  3. H-MOM1 with an open entry.
  4. The FOMC press conference.
  5. QQQ first-hour continuation.
- Spec and builder brief: `examples.md`.

## Q2. Does 0DTE implied vol over- or under-price intraday moves?

**Our measurement [S, descriptive]** (`study/vrp.csv`): SPY realised variance from a given mark to the close, divided by VIX1D-implied variance for the same span (Cboe's 405-minute business day).

| Window | All days, IS / OOS | Notes |
|---|---|---|
| From the 09:30 open | 0.92 / 0.86 | Implied is above realised on about 75% of days. A ratio of 0.86 is about 7% overpricing in vol terms. |
| From 13:30 | 0.57 / 0.39 | Mostly not a VRP. VIX1D shifts weight to next-day options through the session and freezes same-day vol from about 3 pm ✓ {C3}, so it overstates same-day remaining variance late in the day. |
| Prior close → next close | 0.86 / 0.95 | Closest to fair. On CPI/NFP days 1.06 / 1.26 (under-priced on average, driven by a few big days); on OpEx days 0.86 / 0.57 (over-priced). |
| Next open → close | 0.56 / 0.66 | The prior-close VIX1D includes the overnight gap. |

- **Literature:** SPX 0DTE options carry a positive but tiny variance risk premium (Vilkov, Sept 2016–Jan 2024, positions opened at 10:00), and no structure held to expiry was consistently profitable [E] ✓ / ~ {C5}.
- **Intraday vs over days:** in ratio terms the same-day premium looks *smaller* than the multi-day one.
  - At the open, realised/implied variance is about 0.86–0.92, and close-to-close 0.86–0.95.
  - The prior run measured implied 2–4 vol points above realised on 10-day options, and ATM straddles at implied lost 7–23%.
  - So for a same-day buyer the vol premium is a smaller toll than for a multi-day buyer. The spread and the decay through the session are the bigger ones (next section). [S]
- **Single-stock 0DTE:** not testable.
  - Since 2026-01-26, Cboe lists up to two Monday and Wednesday expiries on qualifying names, not daily expiries.
  - To qualify, a name must meet all of: market cap over $700bn (or ETF AUM over $50bn), more than 10M option sides a month, a position limit of at least 250k contracts, and membership of the Penny Interval Program.
  - The Q1 2026 list: TSLA, NVDA, AAPL, IBIT, AMZN, META, AVGO, GOOGL, MSFT.
  - ✓ narrowed {C14} No free intraday IV exists for single stocks.

## Q3. Structures, exits and costs

- **Costs dominate at 0DTE** [E] ✓ {C1, C2}:
  - ATM SPX effective spreads averaged 8.7% (calls) and 9.5% (puts) of the option price for 0DTE, 6.2–6.3% for 1–6 DTE, and about 2% beyond 3 weeks (OPRA trades, 2004 – July 2021, Doshi, Pederzoli & Sert 2025).
  - SPX option spreads are described as roughly U-shaped through the day, widest at the open and near the close (Cao, Jacobs & Ke 2024, as cited by DPS). Older evidence on CBOE equity options shows spreads falling after the open and then levelling off. ✓ narrowed {C2}
  - A one-day SPY snapshot about 5 minutes before the close (Sept 2023; the source gives both 12 and 13 Sept) showed 5.8% spreads on 0DTE options priced near $1, vs about 1% on other expiries ✓ narrowed {C15}.
  - Effective spreads measure what traders actually paid. So the study's base case (about 0.6–0.9% per side for an ATM option) is likely **optimistic for SPX**. On penny-quoted SPY/QQQ that is unmeasured. The study therefore also reports a "DPS" column at 4.5% per side, which lowered OOS excess only modestly (e.g. #1,592: 12.7 → 12.0 pts), because excess differences out most of the cost.
- **Retail outcome** [E] ✓ {C4}: in Beckmeyer, Branger & Gayda's retail data, the average long SPX 0DTE position lost 53% of its value (full sample) and 61% since May 2022, while shorts earned 48% and 56%.
- **ATM vs OTM vs 1DTE vs debit spread** [S], mean over the 76 directional cells per structure (OOS, k = 0.70):

  | Structure | Mean net return | Range | Mean \|excess\| |
  |---|---|---|---|
  | ATM 0DTE | −2.3% | −43% to +33% | 8.8 pts |
  | 0.30Δ OTM 0DTE | −0.1% | −67% to +58% | 14.3 pts |
  | ATM 1DTE | +6.5% | −8% to +25% | 5.0 pts |
  | ATM/0.25Δ 0DTE debit spread | −8.7% | −32% to +11% | 6.1 pts |

  - OTM 0DTE is the most extreme in both directions.
  - The debit spread narrows the outcomes but has the *worst* mean, because it pays the spread on two legs.
  - The 1DTE's positive mean is mostly a model effect: VIX1D rises through the session, which lifts the modelled exit value of the longer-dated option. Its *excess* is about zero (−0.7 pts).
  - Conclusion [O, from S]: no structure turns a weak signal into an edge. Structure choice changes the variance of outcomes more than the mean. Chain data must decide between 1DTE and 0DTE.
- **Exits** [S], mean OOS excess by exit rule within each family:
  - *First profit* (exit at the first hourly mark where the trade is up after costs) was best only for SPY gap fill: +14.2 pts vs +8.2 at 15:30.
  - For QQQ first-hour continuation, holding to 15:30 was best (+9.3 pts vs +2.6 first profit).
  - +50%/−50% target/stop was never best.
  - No exit rule turned a losing family positive. The exit choice moved results by about 5–10 pts, less than the window choice did.
  - First-profit exits are cost-sensitive: in the worked example, a +1.8% gross gain became 0.0% net, the rule did not fire, and the trade rode to −98%.
- **Intraday gamma/theta:** no primary source measured 0DTE theta by hour. Ours is modelled, so we leave it untested. The first hour realises 23–34% of the session's variance (SPY/QQQ, 2024–26) [S]. A model that decays options evenly through the day misprices it. Real 0DTE prices must be used.

## Q4. Data: what exists, from when, and what free data can test

| Source | Intraday option NBBO | From | IV/Greeks | Price (listed) | Status |
|---|---|---|---|---|---|
| ORATS 1-minute | bid/ask, 1-minute snapshots | Aug 2020 | yes (vendor) | $199/mo + $1,500 backfill (individual) | ✓ {C16}. Its underlying price is option-implied, so real stock bars are needed separately. |
| Cboe DataShop Option Quote Intervals | NBBO + size, 1–405 min | Jan 2012 | add-on | not listed. SPX underlying needs a licence from $1,000/mo | ✓ {C19} |
| ThetaData | Value 1-minute; Standard and Pro tick-level | 2020 / 2016 / June 2012 (options) | Greeks endpoints | not on cached pages | ✓ corrected {C18}. Free tier = 1 year of EOD. Deep ITM/OTM 0DTE strikes may be unquoted. |
| Databento OPRA | cbbo-1m before 2023-03-28 (subsampled); tick after | 2013 | none listed; compute your own | from $0.04/GB | ✓ {C17} |
| Massive (formerly Polygon.io) | quotes | 2022-03-07 | no historical Greeks | Options Advanced $199/mo | ✓ {C20} |
| FirstRate Data | EOD only | 2010 | yes | — | [E] |

All vendor facts are self-reported. Not researched: IVolatility, AlgoSeek, OptionMetrics intraday.

**Recommendation [O]:**
- For 2022–26 at arbitrary minutes with vendor IV/Greeks, use ORATS.
- For raw NBBO on a budget, use a Databento pilot on SPY/QQQ only, or Massive Advanced (confirm its depth first).
- Either way, buy real 1-minute underlying bars separately.

**Free data, tested from this container on 2026-11-07:**

| Source | What it gives | Status |
|---|---|---|
| Yahoo chart API | 1-hour bars back to 2023-12 (SPY, QQQ, single stocks); `^VIX1D` hourly from 2024-01-22; 5-minute bars for 60 days; 1-minute for 8 days per request | reachable |
| Cboe `cdn.cboe.com` | VIX1D daily from 2022-05-13, VIX, VIX9D, VXN | reachable |
| api.nasdaq.com | 10 years of daily OHLCV | reachable |
| Concretum macro calendar | free public CSV export of CPI/NFP/FOMC/ISM dates and ET times, no login; FOMC dates match federalreserve.gov for all 40 meetings since 2022 | reachable |
| federalreserve.gov | FOMC calendar | reachable |

- **No free source of historical intraday option quotes was found**: not on Hugging Face, not from Alpha Vantage's demo key, and ThetaData's free tier is EOD only.
- **Blocked:**
  - bls.gov (403);
  - sec.gov (403 on the DERA 0DTE PDF);
  - web.archive.org, stooq.com (connection reset);
  - fred.stlouisfed.org (HTTP/2 error);
  - www1.villanova.edu (SSL error);
  - papers.ssrn.com (403, known from earlier runs).
- **PDFs** from nber.org, nd.edu, lse.ac.uk and afajof.org couldn't be parsed by the fetcher. The orchestrator read the DPS paper's PDF directly with pdftotext.

## Evidence by theme

### Price-path windows (the underlying)
- **Intraday momentum.**
  - Gao, Han, Li & Zhou (JFE 2018): on SPY over 1993–2013, the first half-hour return (measured from the prior close) predicts the last half-hour [E] ✓ {C6}.
  - An earlier working-paper version (SPY 1999–2012) reports 6.3% a year gross for timing the last half-hour vs −0.5% always holding it, with frictions ignored [E] ✓ narrowed {C6}.
  - Baltussen et al. (JFE 2021) find it in 60+ futures from 1974 to 2020 and link it to gamma hedging [E] ✓ {C8}.
  - Later checks are weak: correlation 0.12 (R² 0.014) on SPY 2012–14, and Rosa (JFM 2022) finds the overnight variant fails out of sample [E] ✓ {C7}.
  - Ours: excess ≈ 0 for options [S].
- **Opening-range breakout.**
  - Zarattini, Barbon & Aziz (SFI working paper 2024): Sharpe 2.81, 36% alpha on the top-20 "stocks in play" over 2016–23.
  - A separate QQQ paper (Zarattini & Aziz 2023) reports 33.2% vs 14.9% CAGR with no spread or slippage.
  - An independent net-of-cost replication on index CFDs found at most +0.06R out of sample over 2021–26.
  - [E, working papers / self-reported] ✓ narrowed {C9}.
- **Overnight vs intraday.** Momentum and reversal profits accrue entirely overnight or entirely intraday, typically with opposite signs (Lou, Polk & Skouras 2019) [E] ✓ {C10}. For H-MOM1 in 2021–26, about 70% of the next-day continuation came during the session [S].
- **Gap fill vs go, midday, closing (MOC) imbalances:** no rigorous source found. The practitioner claims were not cached, so they are not used.

### Events and dealer positioning
- **FOMC:** Powell press conferences carry more than 3× the volatility of Yellen's and Bernanke's, and since COVID markets tend to move against the statement reaction during the press conference [E] ✓ {C13}. FOMC-day reversal (CXO summary of Baglioni & Ribeiro) is from the prior run.
- **Dealer gamma and 0DTE:**
  - Adams et al. (SSRN 5641974, read via Quantpedia's summary): 0DTE options dampen S&P 500 volatility on average through a shift in market makers' hedging needs. Higher net gamma predicts E-mini order-flow reversal for about an hour, and dealers keep positive net gamma through expiration day [E, via summary] ✓ narrowed {C11}. The draft first credited this to Dim, Eraker & Vilkov. Their separate paper (SSRN 4692190) reportedly finds that 0DTE gamma does not propagate volatility [E ~, not read].
  - Cboe (self-reported, an interested venue, Sept 2023): the close-to-close minus intraday realised vol gap averaged 2.7 points in 2023, equal to its 10-year average, and Cboe concluded there was no discernible 0DTE impact. This is a descriptive comparison, not a causal test [E] ✓ narrowed {C12}.
  - Amplification is claimed only conditionally (one-sided positioning, short-gamma dealers). We found no verified measurement of it.
- **CPI/NFP/ISM intraday effect sizes:** no systematic source found. Our numbers above are the only measurement.

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Is the open predictable? | ORB papers: large gains on stocks in play / QQQ | Replication: ≈ 0 net on index CFDs; ours ≈ 0 on SPY | A: single stocks with news, gross of spread. B: indices after costs. |
| Intraday momentum | Gao et al., Baltussen et al.: significant | CXO 2012–14 and Rosa: weak or gone out of sample | A: long samples, futures, extreme first-hour moves. B: recent SPY, ordinary days. |
| Does 0DTE gamma amplify moves? | Media and some practitioners: yes | Adams et al. (dampens on average), Cboe 2023 (no discernible impact), Dim–Eraker–Vilkov (no propagation, ~) | Amplification is plausible only with one-sided, short-gamma dealer books, which is not the average. |
| H-MOM1 continuation | 2021–26: strong, mostly intraday next day [S] | 2016–21: reversal [S] | Regime-dependent. The prior run found the same split. |
| Is the open-hour straddle cheap? | Model with VIX1D: yes, t 8–10 [S] | Real prices likely charge for the open's variance [O] | Only 1-minute chain data can decide. |

## Outdated or renamed
- **Polygon.io → Massive** (2025-10-30, per the v2 spec run).
- **"Single-stock 0DTE"** is mostly a misnomer. About nine qualifying names got extra Monday and Wednesday expiries from 2026-01-26, not daily ones ✓ {C14}.
- **VIX1D before 2023:** Cboe's daily history starts on 2022-05-13 (back-filled); the index launched in April 2023 [O, from the Cboe file and SQ3].
- **The DPS spread sample ends in July 2021**, before SPX had daily expiries (May 2022). Today's 0DTE spreads may differ.

## Method and limitations
- **Effort:** 4 researchers (12–17 tool calls each); orchestrator gap-fills (DPS PDF, Concretum calendar, VIX1D convention); 1 skill search and scan (`security-scan.md`, nothing adopted); 4 claim-verifier batches (20 claims: 12 supported, 7 narrowed to the verifier's wording, 1 contradicted and corrected (ThetaData tier dates), 1 misattribution fixed (C11)); one stdlib study with its spec frozen and committed before the run (`study/study_spec.md`, commit 535a5c3).
- **Option P&L is modelled.**
  - Black-Scholes at VIX1D: no skew; ATM overpriced by VIX1D's variance-swap construction; OTM puts underpriced.
  - The exit valuation uses VIX1D, which leans on next-day options as the day goes on.
  - Excess vs the same-time baseline removes level biases, but not biases that depend on the time of day. That is exactly why the open-hour pass and the late-day losses are suspect in opposite directions.
- **Hourly bars only:** no 5-minute opening range, no split between the 14:00 statement and the 14:30 press conference, and target/stop exits checked hourly.
- **H-MOM1:** events come from the prior run (earnings already excluded); IV proxy = 20-day realised + 3.4 vol points; n_OOS = 27.
- **Sample:** VIX1D intraday covers 2.8 years and one regime (no 2022 bear market intraday). FOMC n_OOS = 13.
- **Calendars:** CPI/NFP/ISM dates come from a third-party calendar (Concretum) because bls.gov is blocked. FOMC dates match the Fed exactly.
- **Not verified against originals:** the Vilkov figures come through blog summaries (~). Ni, Pearson & Poteshman pinning was seen only as a snippet and is not used.
- **Trials:** cumulative count now 1,965. Next trial: #1,966.
