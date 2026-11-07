# Continuation study spec (frozen 2026-11-07, before any run)

**Question:** after a large move, does buying a short-dated option *in the direction of the move*
pay, and which exit rule works best? Same tickers, same data and same pricing framework as
`../study/study_spec.md`. Earnings are excluded. The artifact is not updated (user decision).

**Motivation:** the reversal study found index shock days continued (−0.9% over 10 days on the
reversal side) and buying the bounce lost 21 points against random days. Medhat & Schmeling find
liquid stocks show short-term momentum, and Savor finds news-driven moves drift.

## What counts as a large move (decided at the close of day t, ex ante)
- **Size (primary):** |r_t| ≥ k·σ60_t, with σ60 = stdev of daily log returns over t−60..t−1 (today
  excluded) and **k ∈ {2.0, 2.5, 3.0}**. The move is measured against the ticker's own recent
  volatility, so a 3% day is large for SPY but ordinary for TSLA.
- **Quality filters** (reported as splits at k = 2.5 only, entry at day t's close):
  - *close strength:* close in the top 20% of the day's range for up moves (bottom 20% for down), i.e. CLV ≥ 0.8 / ≤ 0.2, against "faded" (otherwise).
  - *volume:* volume_t ≥ 2× its 20-day average, against below. This is a proxy for real news, since Savor's drift comes from information events.
  - *gap:* gap share |O_t − C_{t−1}| / |C_t − C_{t−1}| ≥ 0.5 (gap-driven), against intraday.
  - *type (stocks only):* idiosyncratic / market-wide / mixed, defined as in the reversal study.
  - *VIX regime:* VIX_t tercile within its **trailing 252 days** (low / mid / high). This fixes the full-sample look-ahead in the reversal study.
- Earnings on t or t−1 → the stock event is dropped. De-clustering: one event per ticker per 10 trading days, per k.

## Entry
- **EOD:** buy at the close of day t (the move day).
- **Confirmed:** buy at the close of t+1, only if day t+1 closed further in the move's direction. Otherwise no trade.
- Direction: an up move buys a call, a down move buys a put.
- Next-open entry is **not testable**: there is no intraday IV or option quotes in free data.

## Options (Black-Scholes, r = 0, no dividends)
- **Structures:** ATM 7 DTE, ATM 14 DTE, ATM 30 DTE, and a 0.30Δ OTM option at 14 DTE.
- **IV:**
  - ETFs and indexed stocks (SPY→VIX, QQQ→VXN, IWM→RVX, AAPL→VXAPL, AMZN→VXAZN, GOOGL→VXGOG) use the index at the entry close and at each exit close.
  - **Short-dated adjustment:** for DTE ≤ 14, IV × (VIX9D_t / VIX_t), the market's own short-vs-30-day ratio that day. Short-dated IV is usually higher than 30-day IV right after shocks, and ignoring that would flatter 7–14 DTE buys.
  - **Non-indexed stocks:** entry IV = 100·√252·stdev(r over t−19..t) + 3.4 points (as before). On event trades, exit IV on day d = entry IV × D(d, direction), where D is the mean of IV_{t+d}/IV_t over indexed-ticker events in this run, computed separately for up and down moves. Random-day baseline trades keep the rolling proxy at exit, since IV barely moves on random days. This replaces the old proxy, which couldn't show post-shock IV decay.
- Time: T_d = (DTE − d·7/5)/365. At or past expiry the option is worth its intrinsic value.

## Exits (checked at closes only; max hold 5 trading days)
1. Fixed hold: exit at day **1, 2, 3 or 5**.
2. **First green:** exit at the first close where P&L after costs is > 0; else day 5.
3. **Green + 1** / **Green + 2:** first green close d, then exit at d+1 or d+2 (capped at 5); else day 5.
4. **TP/SL:** exit at the first close with P&L ≥ +30% or ≤ −40%; else day 5.
5. **Trail:** after the first green close, exit at the first close where the underlying moves against the trade's direction; else day 5.

That makes 9 exit rules.

## Costs, baseline, statistics
- Costs as before: quoted spread assumed at 3% of mid. At k = 0.70: 0.6% of value per side plus $0.70 per contract. k = 1.0 stress: 1.5%. The gross case is also computed.
- **Baseline:** the same structure and exit rule, entered at the close of every eligible day with the same option type (calls compared with random calls, puts with random puts). Per ticker and period. Excess = event return − baseline mean.
- Price-only continuation is reported for context: signed return of the move direction after 1, 2, 3 and 5 days, by k.
- Pools: **ETFs** (SPY, QQQ, IWM) and **stocks** (the 16 names), scored separately.
- Periods: IS 2016-11 → 2021-06, OOS 2021-07 → 2026-11.

## Grid and multiple testing
- Main grid: k ∈ {2.0, 2.5, 3.0} × structure {4} × exit {9} × entry {2} × pool {2} = 432 scored cells (k = 0.70).
- Filter splits: k = 2.5, entry EOD only: structure {4} × exit {9} × split values (ETFs 9, stocks 12) = 756 cells. Total ≈ 1,188 scored cells.
- Every scored cell counts. The trial count continues from 348.
- **Promising (stricter than before, because of the grid size):** at k = 0.70, all of:
  - OOS excess ≥ +10 points with **t ≥ 3**;
  - IS excess > 0;
  - n_OOS ≥ 30;
  - the same cell at **k = 1.0** keeps OOS excess > 0.
- At t ≥ 3, about 0.1% of null cells pass by chance, so roughly one false positive is expected in ~1,000 cells.

## Known limitations (before the run)
- Daily closes only: no intraday entries, stops or targets. A real TP/SL would fill intraday at different prices.
- 7-DTE ATM options on single stocks often have quoted spreads well above 3% of mid. The k = 1.0 stress partly covers that.
- The term-structure adjustment uses the S&P 500's VIX9D/VIX ratio for every ticker.

## Change log
- (none yet)
