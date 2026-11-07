# Study spec: same-day long options on SPY/QQQ, plus H-MOM1 day-after (frozen before any run)

Frozen 2026-11-07, before any result was computed. Data was downloaded by `fetch_data.py` and only
its layout was inspected (bars per session). Any change after the first run is logged at the bottom
as an amendment, and the original rule stays reported.

## Data
- **Hourly (Parts 1–2):** Yahoo 1-hour bars for SPY, QQQ and `^VIX1D`. Bars start 09:30, 10:30 … 15:30 ET.
  - Price at mark 09:30 = first bar's open. Price at mark h+1h = the close of the bar starting at h, giving marks 10:30 … 15:30 and 16:00.
  - Sessions: those with all 7 bars for the ticker and VIX1D. Half-days are excluded.
  - Period 2024-01-22 → 2026-11-06 (VIX1D hourly starts 2024-01-22).
- **Daily:** Cboe VIX1D, VIX and VXN closes; Nasdaq daily OHLCV, 2016-10 → 2026-11.
- **Calendars:**
  - FOMC statement dates from the Concretum macro calendar (`macro_events.csv`), cross-checked against federalreserve.gov. On any mismatch, the Fed page wins, and the mismatch is logged.
  - CPI and NFP (08:30) and ISM manufacturing/services (10:00) dates come from the Concretum calendar, a third-party source not checkable against bls.gov (403).
  - Monthly OpEx = the third Friday of each month, or the Thursday before when that Friday is not a session.
- **H-MOM1 events (Part 3):** the prior continuation run's `events.csv` (branch `claude/inspiring-cerf-epxwvd`, copied to `data/prior_continuation_events.csv`). It already excludes earnings on t and t−1. Single stocks only (16 names).

## Option model
- **Pricing:** Black-Scholes, r = 0, no dividends, European.
  - **SPY:** σ = VIX1D at the mark.
  - **QQQ:** σ = VIX1D × (VXN / VIX), using the prior session's daily closes.
- **Frozen window:** at marks ≥ 15:00 (i.e. 15:30 and 16:00), σ = VIX1D at the 14:30 mark. Cboe says near-term vol is frozen in the last 60 business minutes, so VIX1D then mostly reflects the next day.
- **Time to expiry in years.** 0DTE: τ = (minutes to 16:00) / (252 × 405), using Cboe's 405-minute business day; 252 business days is our assumption. 1DTE adds 405/(252×405) = 1/252. A sensitivity with 390-minute days is reported, not used for decisions.
- **Strikes:** SPY and QQQ strikes in $1 steps.
  - ATM = nearest $1 to spot at entry.
  - OTM 0.30Δ: the $1 strike whose BS |Δ| is closest to 0.30.
  - Debit spread: long ATM, short the strike closest to 0.25Δ, same side, same expiry.
- **Known biases:**
  - VIX1D is a variance-swap-style index, so it sits above ATM IV and overprices ATM options. This pushes absolute long returns down.
  - No skew, so OTM puts are priced too cheaply and OTM calls too dearly.
  - Excess vs the same-time baseline removes most of both biases. Absolute returns are reported but not used for decisions.

## Costs (set before the run from the SQ3 evidence and the DPS paper)
- **Quoted spread:** S$ = max($0.01, s × mid). s = 3% for marks 10:30–14:30, and 4.5% at the 09:30 mark and marks ≥ 15:00 (the U-shaped intraday spread). One rate for 0DTE and 1DTE.
- **Per side:**
  - Buy at mid + (k − 0.5)·S$, sell at mid − (k − 0.5)·S$, per leg.
  - k = 0.70 is the base case; k = 1.0 the stress case.
  - Plus $0.70 per contract per side = $0.007 per share.
- **Extra column (reported, not a gate):** "DPS". Per-side cost = 4.5% of mid per leg, i.e. half of the measured average effective spread of ATM SPX 0DTE options, 2004–2021 (Doshi, Pederzoli & Sert 2025, Table 2: 8.7% calls, 9.5% puts).
- **Gross** returns are also reported.
- **Return metric:** net P&L ÷ entry cost (debit paid including costs), in % of premium.

## Baselines and excess
- **Triggered cells:** baseline = the same structure, entry mark and exit rule on every eligible session in the same split where the trigger did not fire.
  - Side: the mean of the call and the put (a random side), at the same time of day.
  - Excess = cell mean − baseline mean. t = Welch t of cell vs baseline.
- **Untriggered time-of-day cells** (straddles at a fixed time on all days): baseline = the same structure and holding length bought at every other eligible entry mark on the same sessions (a random-time baseline).
- **Day-type straddle cells** (FOMC, macro, OpEx): baseline = the same structure and marks on all other sessions, except OpEx, whose baseline is the other Fridays.

## Splits
- Hourly: IS = 2024-01-22 → 2025-05-30, OOS = 2025-06-02 → 2026-11-06.
- Daily Part 3: IS = 2016-11 → 2021-06, OOS = 2021-07 → 2026-11, matching the continuation run.
- VIX1D daily: IS = 2022-05-13 → 2024-06-28, OOS = 2024-07-01 → 2026-11-06.

## Exit rules (directional cells)
- Fixed: exit at the named mark.
- **FP (first profit):** the first later mark where the net exit value is greater than the entry cost. Otherwise 15:30.
- **TS:** at the first later mark, mid ≥ 1.5× or ≤ 0.5× the entry mid. Otherwise 15:30.
- No exit after 15:30 except the momentum cell (W3), which is defined as last-half-hour and exits at 16:00 at intrinsic minus k costs.

## Part 1: intraday VRP (SPY, VIX1D = SPX; descriptive cells, counted as trials)
- **1a. Variance ratio by mark.** For each mark m ∈ {09:30 … 15:30}: implied variance to the close = σ_m² × τ_m. Realised variance = the sum of squared hourly log returns from m to 16:00. Report the mean of each, the ratio of means, and the share of days where realised > implied.
  - Day types: all, FOMC, 08:30 macro (CPI or NFP), 10:00 ISM, monthly OpEx, other.
  - 7 × 6 = 42 cells.
  - 390-minute sensitivity reported.
- **1b. Daily.** VIX1D close on t−1, squared over 252, against realised SPX-proxy variance on t (SPY close-to-close and open-to-close squared log returns).
  - Day types as above (2022-05 → 2026-11).
  - 2 realised definitions × 6 day types = 12 cells.
- **1c. ATM straddles held to a later mark.**
  - 0DTE straddle (S0) and 1DTE straddle (S1).
  - Windows:
    - open 09:30→10:30;
    - 10:30→15:30;
    - midday 11:30→13:30;
    - power hour 14:30→15:30;
    - last half-hour 15:30→16:00 (S0 at intrinsic).
  - For SPY and QQQ: 5 windows × 2 structures × 2 tickers = 20 cells, each against the random-time baseline. They are counted, but are eligible for the bar only on net excess.

## Part 2: directional and event windows (SPY and QQQ)
Structures for directional cells: A0 (ATM 0DTE), O0 (0.30Δ 0DTE), A1 (ATM 1DTE) and D0 (ATM/0.25Δ 0DTE debit spread).

- **W1 Opening-range (first hour).**
  - Signal: r1 = ln(P10:30 / P09:30).
  - Trigger: |r1| ≥ the median |r1| of the prior 60 sessions.
  - Two variants: continuation (side = sign r1) and fade (side = −sign r1).
  - Entry at 10:30. Exits: 11:30, 13:30, 15:30, FP, TS.
  - 2 × 5 × 4 × 2 = 80 cells.
- **W2 Gap.**
  - Signal: g = ln(P09:30 / P16:00 of the prior session).
  - Trigger: |g| ≥ the standard deviation of g over the prior 60 sessions.
  - Two variants: go (side = sign g) and fill (side = −sign g).
  - Entries at 09:30 and 10:30. Exits for the 09:30 entry: 10:30, 12:30, 15:30, FP, TS. Exits for the 10:30 entry: 11:30, 13:30, 15:30, FP, TS.
  - 2 × 2 × 5 × 4 × 2 = 160 cells.
- **W3 Intraday momentum (Gao et al. analogue).**
  - Signal: r = ln(P10:30 / P16:00 of the prior session). Side = sign r.
  - Entry at 15:30, exit at 16:00.
  - Two variants: all days, and |r| ≥ the 67th percentile of the prior 60 sessions.
  - 2 × 4 × 2 = 16 cells. The baseline is the random side on non-trigger days. For "all days" there are none, so the baseline is the mean of the call and the put on the same days.
- **W4 FOMC (14:00 statement, 14:30 press conference).**
  - Straddles S0 and S1, entry 13:30, exits 14:30 and 15:30: 2 × 2 × 2 = 8 cells.
  - Directional: side = ±sign(ln P14:30 / P13:30). Continuation and fade, entry 14:30, exit 15:30: 2 × 4 × 2 = 16 cells.
  - Hourly bars can't split the statement from the press conference.
- **W5 08:30 macro (CPI or NFP).**
  - Straddles S0 and S1, entry 09:30, exits 10:30, 12:30 and 15:30: 2 × 3 × 2 = 12 cells.
  - Directional: gap go and fill on macro days, entry 10:30, exits 13:30 and 15:30: 2 × 2 × 4 × 2 = 32 cells. The baseline is non-macro days.
- **W6 10:00 ISM.** Straddles S0 and S1, entry 09:30, exits 10:30 and 12:30: 2 × 2 × 2 = 8 cells.
- **W7 Monthly OpEx.** Straddles S0 and S1, entries 10:30 and 13:30, exit 15:30, against the other Fridays: 2 × 2 × 2 = 8 cells.

## Part 3: H-MOM1 day-after (daily, single stocks)
- **Pools:**
  - "strict": the H-MOM1 definition. k = 2.5, idiosyncratic, volume high, close strong, VIX low or mid.
  - "all": every k = 2.5 single-stock event.
- **Price only:** direction-signed overnight (C_t → O_t+1), intraday (O_t+1 → C_t+1) and full (C_t → C_t+1) log returns.
  - Baseline: the same ticker's unconditional mean of each return in the split, signed by the event direction.
  - 3 × 2 pools = 6 cells.
- **Options:** ATM 14-DTE and ATM 7-DTE, call or put in the move direction, exit at the close of t+1.
  - Entry at the close of t vs at the open of t+1: 2 entries × 2 structures × 2 pools = 8 cells.
  - **IV proxy:** 20-day realised + 3.4 vol points, the same at entry and exit, as in the prior runs. There is no intraday IV, so the open entry uses the same IV as the prior close.
  - Spread: 3% of mid; k = 0.70 / 1.0.
  - Baseline: the same structure at the same entry time on random sessions of the same ticker (all non-event sessions in the split, mean of call and put).

## Trials and pass bar
- Every cell above counts as one trial, numbered from **#1,538** in the order listed. That gives 42 + 12 + 20 + 80 + 160 + 16 + 24 + 44 + 8 + 8 + 6 + 8 = **428** cells, i.e. trials #1,538 → #1,965.
- **Pass** requires all of:
  - OOS net excess ≥ +10 pts at k = 0.70;
  - Welch t ≥ 3;
  - IS excess of the same sign;
  - OOS excess at k = 1.0 > 0;
  - n_OOS ≥ 20.
- Cells with n_OOS < 20 are reported and counted but marked ineligible.
- Part 1a/1b cells are descriptive. They answer Q2 and can't "pass".
- Expected false passes at t ≥ 3 over ~350 eligible cells: about 0.5.

## Outputs
`results.csv` (one row per cell, with its trial number), `vrp.csv` (Part 1a/1b), `run.log`, and `trades_sample.csv` (the first 200 trades for audit).

## Amendments
(none yet)
