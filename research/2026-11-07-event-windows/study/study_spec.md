# Event-study spec (frozen 2026-11-07, before any run on real events)

Written before running `events.py` on real data. Changes after seeing output are logged at the
bottom as new trials, with the reason. Earnings are excluded throughout (user decision).

## Data (all free; downloads cached in `study/data/`, gitignored)
- Prices: Nasdaq daily OHLCV, 2011-01-03 → 2026-11-06, via `screen.py`'s loader. Tickers:
  SPY, QQQ, IWM, and the single stocks NVDA, TSLA, MU, AAPL, INTC, AMD, AMZN, META, PLTR, GOOGL,
  MSFT, AVGO, ORCL, HOOD, PFE, SOFI.
- Implied vol: Cboe CSVs: VIX, VIX9D (2011+), VIX1D (2022-05+), VIX3M, VVIX, VXN, RVX, VXAPL, VXAZN, VXGOG.
  Mapping: SPY→VIX (VIX9D for 5-day horizons), QQQ→VXN, IWM→RVX, AAPL→VXAPL, AMZN→VXAZN, GOOGL→VXGOG.
- Dealer gamma: SqueezeMetrics `DIX.csv`, column `gex` (an SPX-level proxy, used for all three ETFs).
- FOMC: statement dates parsed from federalreserve.gov (`fomccalendars.htm`, `fomchistorical<YYYY>.htm`).
  Scheduled meetings only; 2025-08-22 (a framework statement, not a meeting) is dropped. Unscheduled
  2020-03-03 and 2020-03-15 are counted as catalysts in C1, not as scheduled M1 events.
- Earnings (exclusion only): Nasdaq earnings calendar for date t and t−1. If the ticker is listed, the
  single-stock event is dropped.

## Common definitions
- r_t = close-to-close log return. σ60_t = stdev(r over t−60..t−1), i.e. excluding day t.
- Option pricing: Black-Scholes, r = 0, no dividends (both simplifications noted). Options are 45
  calendar DTE at entry; after h trading days T falls by h·7/5 calendar days. Entry at close t.
- IV at entry and exit = the mapped vol index at that close. Where there is no index (C2 non-indexed
  stocks) the **proxy** is 100·√252·stdev(r over the last 20 days including today) + 3.4 vol points
  (the median implied−realised gap from the previous run). Proxy results are flagged.
- Structures: **ATM single** (call or put) and **debit spread** (long 0.50Δ / short 0.25Δ, both strikes solved at entry IV).
- Costs: assumed quoted spread = 3% of mid per leg (an assumption, flagged). At k = 0.70 the cost per side = 0.2 × 3% = 0.6% of each leg's value, plus $0.70 per contract. Stress at k = 1.0 (1.5% per side). Both gross and k = 0.70 are reported.
- Holding horizons: **h ∈ {3, 10}** trading days for option P&L. Price-only reversal at h ∈ {1, 3, 5, 10} is reported as context and isn't scored.
- De-clustering: after an event, the same ticker can't trigger the same event type for 10 trading days.
- Periods: in-sample 2011-01 → 2019-12, out-of-sample 2020-01 → 2026-11.

## Windows
- **M1 macro release (FOMC scheduled):** move ratio = |r_t| ÷ implied 1-day move.
  - Implied 1-day move = VIX1D_{t−1}/100/√252 (2022+), and VIX9D_{t−1}/100/√252 for all years as a second series.
  - Straddle proxy = |r_t| / (0.798·implied) − 1.
  - Baseline: all non-FOMC days.
  - Tickers: SPY (also QQQ with VXN).
- **M2 pre-FOMC drift:** ATM call bought at close t−1, sold at close t (h = 1, an exception to the h set).
  - Baseline: ATM calls held one day from a random day.
  - Ticker: SPY.
- **R1 dealer gamma:** for every day t with GEX known, take the straddle-at-implied return over 5 days (VIX9D) and 10 days (VIX), split by GEX < 0 vs ≥ 0 and by GEX quintile.
  - Ticker: SPY.
- **R2 vol-shock onset (first day of each state, de-clustered):**
  - (a) VIX_{t−1} < 30th percentile of its trailing 252 days and VIX_t/VIX_{t−1} − 1 ≥ 0.20.
  - (b) VIX9D > VIX > VIX3M (full inversion), first day.
  - (c) VVIX ≥ 90th percentile of its trailing 252 days, first day.
  - Measure: straddle-at-implied over 5 (VIX9D) and 10 (VIX) days. Baseline: all days.
  - Tickers: SPY (and QQQ with VXN, applied to the same SPX-based states).
- **C1 post-catalyst reversal, market-wide:**
  - Triggers: (i) |r_t| > 2.5·σ60_t; (ii) VIX_t / min(VIX_{t−3..t−1}) − 1 ≥ 0.30; (iii) FOMC day (scheduled or unscheduled) with |r_t| > 1.5·σ60_t.
  - Trade the reversal: call after a down day, put after an up day.
  - Conditioners (each split reported):
    - VIX tercile at t (full-sample terciles).
    - Close location CLV = (C − L)/(H − L): for down days, CLV ≥ 0.5 means "bouncing"; for up days, CLV ≤ 0.5 means "fading".
    - GEX sign.
  - Tickers: SPY, QQQ, IWM.
- **C2 post-catalyst reversal, single stock (non-earnings):**
  - Trigger: |r_t| > 2.5·σ60_t, and no earnings on t or t−1. Trade the reversal as in C1.
  - Conditioners:
    - Type: *idiosyncratic* if |r_SPY,t| < 1·σ60_SPY; *market-wide* if r_SPY,t has the same sign with |r_SPY,t| > 1.5·σ60_SPY; otherwise *mixed*.
    - Gap share = |O_t − C_{t−1}| / |C_t − C_{t−1}| (≥ 0.5 = gap-driven).
    - CLV as in C1.
    - VIX tercile.
- **C3 implied-vol decay:** for C1/C2 events with an index, the mean IV change from entry to h = 3 and 10, against the same change from random days. Descriptive, not scored.

## Statistics and verdict
- Per window × structure × horizon × split:
  - n events, mean and median return, share of winners.
  - t-stat on events (already de-clustered, so non-overlapping within a ticker).
  - The same statistics for the random-date baseline: every eligible day for that ticker and structure, with the same direction rule (calls for down-move windows are compared with calls on all days).
- **Promising** = all of these hold:
  - the k = 0.70 mean beats the baseline by ≥ 10 percentage points out of sample, with t ≥ 2 on the difference;
  - the in-sample difference has the same sign;
  - n_OOS ≥ 20.
- Every reported cell counts as a trial. The total is printed by the script and appended to the trial
  log, continuing from 5 (previous run).

## Known limitations (stated before the run)
- Vol indices are 30-day (9-day, 1-day) constant-maturity measures, not the 45-DTE ATM or 0.25Δ IV.
  Skew isn't modelled, so the debit spread's short leg is priced at ATM vol. For call spreads (after
  down-shocks) that overstates the short OTM call's value and understates the spread's cost. For put
  spreads (after up-shocks) it understates the short OTM put's value and overstates the cost.
- The 3%-of-mid spread is an assumption. After shocks, spreads widen, so k = 1.0 is the honest check.
- Daily closes only: no intraday entries.

## Change log
- (none yet)
- Pre-run amendment (2026-11-07, before any event run): the Nasdaq API returns at most ~10 years
  (2016-11-07 onward) even when asked for 2011, so the study period is 2016-11 → 2026-11. The split
  becomes in-sample 2016-11 → 2021-06 and out-of-sample 2021-07 → 2026-11 (about half each, and
  out-of-sample includes the 2022 bear market and the 2025 shocks). Vol indices and GEX are cut to the same window.
- Pre-run note (2026-11-07): no reachable CPI or payroll release-date history (bls.gov 403; SQ2 found
  none), so M1 is FOMC-only. CPI and payroll windows are untested, not rejected.
