# Worked example, paid-data backtest spec and builder brief

*As of 2026-11-07. Part of `research/2026-11-07-intraday-long-options/`. Prior runs cited here live
on branch `claude/inspiring-cerf-epxwvd`.*

## 1. Worked example: SPY gap day, Friday 2026-10-30

**Real data:** SPY prices and VIX1D values below are real (Yahoo 1-hour and 5-minute bars; Nasdaq
daily). **Modelled:** option prices are Black-Scholes at VIX1D, exactly as in the study
(`study/intraday.py`). No free source has historical 0DTE quotes, so the option columns show what
the model says, not what the market charged.

**The day:**
- SPY closed at $769.36 on 10-29 and opened at $761.40 on 10-30. The gap was −1.04%, against a 60-day gap σ of 0.41%, so it triggered rule W2.
- The 5-minute path was flat to slightly up after the open, at $760–761 until 10:00. SPY then fell to $758.06 by 10:30 and to the day's low of $750.36 at about 14:50. It closed at $755.72.
- The gap did not fill.

| Mark (ET) | SPY | VIX1D | σ used |
|---|---|---|---|
| 09:30 | 761.40 | 11.17 | 0.112 |
| 10:30 | 758.06 | 12.73 | 0.127 |
| 11:30 | 758.51 | 12.82 | 0.128 |
| 12:30 | 757.58 | 14.27 | 0.143 |
| 13:30 | 755.59 | 17.48 | 0.175 |
| 14:30 | 751.47 | 23.46 | 0.235 |
| 15:30 | 752.86 | 21.92 | 0.235 (frozen at the 14:30 value) |

**Rule W2-fill, entry 10:30:** buy a call, betting the down-gap fills. The 0DTE ATM 758 call is modelled at $2.22 mid.

**Costs:** spread = max($0.01, 3% × mid) = $0.067.
- At k = 0.70 you pay mid + 0.2 × spread = $2.233, plus $0.007 commission = $2.240 per share ($224 per contract).
- At k = 1.0 you pay the ask: $2.252 + $0.007.

| Exit rule | Exit mid | Net return, k = 0.70 | k = 1.0 |
|---|---|---|---|
| 11:30 (+1 h) | $2.26 | 0.0% | −1.8% |
| 13:30 (+3 h) | $1.04 | −54% | −55% |
| 15:30 | $0.06 | −98% | −98% |
| First profit (FP) | no mark above cost after costs, so it rides to 15:30 | −98% | −98% |
| +50% / −50% (TS) | stopped at 13:30 | −54% | −55% |

**The same day, the other side.** Rule W2-go buys the 758 put at 10:30 for $2.16 mid.
- Exit at 13:30: +57% at k = 0.70.
- Exit at 15:30: +136% at k = 0.70.
- 0.30Δ 755 put: +154% at 15:30.
- Debit spread (long 758 put, short 754 put): +123% at 15:30.
- 1DTE 758 put: +132% at 15:30.

**What this example shows:**
1. **One gap day decides nothing.** Over the 87 out-of-sample gap days, "go" lost against the baseline and "fill" won, but neither was significant (study: SPY fill ATM, entry 09:30, first-profit exit: +16.7 pts, t 1.6; go ATM, entry 09:30, exit 15:30: −17.2 pts, t −1.1).
2. **First-profit exits depend on costs.** At gross prices the call was up 1.8% at 11:30, and FP would have exited there. After costs it was 0.0% and the rule kept holding into a −98% loss. With 0DTE options, a few cents of spread change which path the exit takes.
3. **VIX1D more than doubled through the session**, from 11.2 to 23.5. Part of that rise is real fear, and part is VIX1D shifting weight to Monday's options. The model's exit values use that VIX1D, so the put's modelled gains include some vega that a real 0DTE put may not have carried. This is the main reason the study can't be trusted for exact option P&L.
4. **The open-hour straddle that "passed" in the study** (trial #1,592): at 09:30 the modelled 761 straddle cost $4.21 at mid. SPY moved $3.34 by 10:30, giving a modelled value of $5.00: +16% at k = 0.70, +14% at k = 1.0, and +8% at the DPS cost. The modelled exit uses the same flat business-minute clock, while the first hour carries 23–34% of a session's realised variance in our sample. That is why the pass is flagged as a suspected model artefact (`study/diagnostics.log`).

## 2. Paid-data backtest spec (ready to run once chain data is bought)

This builds on the v2 spec (`research/2026-11-06-options-swing-backtest-spec/report.md`, branch
`claude/inspiring-cerf-epxwvd`). Everything there applies unless changed here. Trial numbering
continues from **#1,966**.

### Data
- **Option quotes:** 1-minute NBBO (bid, ask, sizes) for SPY and QQQ, every expiry ≤ 7 DTE, all strikes within ±10% of spot, 2022-05-16 → present.
  - From 2022-05-16 there are daily expiries on SPY/QQQ. Earlier sessions only have Mon/Wed/Fri expiries; run those as a separate sample.
  - Plus the 10 shortlist single stocks, weekly expiries ≤ 14 DTE, for H-MOM1.
- **Vendors**, all self-reported (see `sources.md`):
  - ORATS 1-minute: from Aug 2020, bid/ask, IV and Greeks; $199/month plus a $1,500 backfill.
  - Cboe DataShop Option Quote Intervals: NBBO from 2012; Greeks are an add-on.
  - ThetaData Standard: 1-minute from 2016.
  - Databento OPRA: cbbo-1m before 2023-03-28 (subsampled), tick after.
  - Massive Options Advanced: quotes from 2022-03-07, no historical Greeks.
- **Underlying:** real 1-minute stock/ETF bars from a separate source. ORATS's underlying is option-implied, so it can't be used for signals.
- **Calendars:** FOMC (federalreserve.gov); CPI/NFP/ISM (Concretum free calendar, or BLS if reachable); monthly OpEx.
- **Quote hygiene:** drop quotes with bid = 0, crossed or locked quotes, or a spread above 50% of mid. Log the share dropped per hour of the day.

### Execution model
- **Signal timing:** signals use bars that close at minute t. Entry is at the NBBO at minute t+1.
- **Fills:** buy at bid + k·(ask − bid), sell at ask − k·(ask − bid), per leg. k = 0.70 base, 1.0 stress. Also report a "DPS" stress: per-side cost = 4.5% of mid.
- **Commission:** $0.70 per contract per side.
- **Sizing:** risk a fixed $ debit per trade.
- **Exits:** no position is held past 15:45 ET. 0DTE positions are never carried to settlement.

### Hypotheses (one trial each; the grid is fixed now)
1. **H-OPEN1: open-hour straddle.** Buy the 0DTE ATM straddle at 09:31 and sell at 10:30.
   - Grid: entry {09:31, 09:35, 09:45}; exit {10:00, 10:30}.
   - Baseline: the same straddle bought at random minutes in 10:30–14:30 and held for the same number of minutes, on the same days.
   - This tests the only free-data pass. It is expected to fail if real option prices already include the open's variance.
   - 6 trials.
2. **H-GAPFILL1: gap fill.** |gap| ≥ 1 × σ60 of gaps; buy against the gap at 09:35 or 10:30.
   - Structures {ATM 0DTE, ATM/0.25Δ debit spread}; exits {first profit, 15:30}.
   - Baseline: random side on non-gap days.
   - Report "go" too, as the mirror image.
   - 2 entries × 2 structures × 2 exits × 2 sides × 2 tickers = 32 trials.
3. **H-ORB-QQQ1: first-hour continuation on QQQ.** |r(09:30→10:30)| ≥ the 60-day median; buy in the direction at 10:31.
   - Structures {ATM 0DTE, debit spread}; exits {15:30, first profit}.
   - Also a 5-minute ORB version: r(09:30→09:35) direction, entry at 09:36.
   - 2 × 2 × 2 = 8 trials.
4. **H-FOMC1: FOMC press conference.**
   - Straddle 13:55 → 14:25 (statement), and straddle 14:25 → 15:30 (press conference).
   - Directional: fade the 14:00–14:25 move at 14:30 and exit at 15:30. The Powell-era reversal (Narain 2026) motivates this.
   - Report by policy cycle.
   - Note: n ≈ 8 meetings a year. With 2022–26 there are about 36 events, so expect "ineligible" unless the effect is very large.
   - 3 trials.
5. **H-MOM1-OPEN: day after a large stock-specific move.** H-MOM1 trigger (trial #1,537 definition), single stocks.
   - Buy the ATM weekly (nearest expiry ≥ 3 DTE) in the move's direction. Entries at the move-day close (15:50 snapshot) vs the next day 09:35 / 10:00. Exit at the next day's 15:45.
   - Chain IV is used, so the IV-proxy bias of the earlier runs disappears.
   - 3 trials.
6. **H-MACRO1: 08:30 CPI/NFP.** ATM straddle at 09:31 → 10:30 and 09:31 → 12:30, vs non-release days. 2 trials.

### Validation
- **Splits:** walk-forward by calendar year (2022H2–2023 train, 2024 test, 2025 test), plus a 2026 holdout that is not touched until the gates are fixed.
- **Pass gates:** the user's strict bar at k = 1.0 on the holdout: OOS excess ≥ 10 pts, t ≥ 3, in-sample of the same sign, k = 1.0 still positive, n_OOS ≥ 20.
- **Reporting:**
  - PBO/deflated Sharpe across all 54 trials.
  - By hour of day: the share of quotes dropped by the hygiene filter, and the median spread as a % of mid by moneyness. This is our first real measurement of 0DTE costs on SPY/QQQ.

## 3. Builder brief (for a coding agent or a future session)

```text
OBJECTIVE
Build and run the intraday paid-data backtest in research/2026-11-07-intraday-long-options/examples.md
section 2, on purchased 1-minute NBBO option data for SPY and QQQ (and the shortlist stocks for
H-MOM1-OPEN), and report each trial's result against the pre-registered gates.

WHY
A free-data study (study/, trials #1,538-#1,965) found no tradeable directional window and one
pass (open-hour 0DTE straddle) that is probably an artefact of modelled prices. Only real quotes
can settle it. The owner decides from your output which, if any, same-day setups to paper-trade.

WHAT IS ALREADY KNOWN
- Spec, costs and gates: examples.md section 2; v2 spec in
  research/2026-11-06-options-swing-backtest-spec/report.md (branch claude/inspiring-cerf-epxwvd).
- Free-data results: study/results.csv, study/vrp.csv, study/diagnostics.log.
- ORATS underlying prices are option-implied; get real 1-minute equity bars separately.
- Earnings are out of scope for every hypothesis.

SCOPE
In: the six hypotheses and exactly the grid listed (54 trials, #1,966-#2,019). Out: adding
hypotheses, changing gates or grids after seeing results (log any change as an amendment, keep
the original result), earnings, selling premium.
Writes: research/<run-date>-intraday-chain-backtest/ only (spec copy, code, results, log).

HOW
- Freeze spec.md (copy of section 2 plus vendor-specific field mapping) and commit before the first run.
- Stdlib Python preferred; if the vendor SDK is required, pin its version.
- Unit-test the fill function, quote-hygiene filter and minute alignment on 3 hand-checked days
  (include 2026-10-30 from examples.md section 1).

BUDGET AND STOPPING
Stop after one full run plus diagnostics. If data coverage for any hypothesis is < 80% of
sessions, stop and report coverage instead of results.

OUTPUT
results.csv (one row per trial: trial no., n_IS/n_OOS, mean, baseline, excess, t, k=1.0 excess,
DPS excess, pass), spreads_by_hour.csv, run.log, and a <=300-word summary with paths.

QUALITY BAR
Never fill at mid. No look-ahead: signals use completed bars only. Report failures as failures.
```
