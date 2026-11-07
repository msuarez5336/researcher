# Screen spec (frozen 2026-11-07, before any full run)

Written before the script ran on the candidate list. Any change after seeing output is logged at
the bottom as a new trial, with the reason.

## Data
- Underlying: Nasdaq public API daily OHLCV (`api.nasdaq.com/api/quote/<T>/historical`), 2016-11-07 → 2026-11-06.
  The script flags any daily |log return| > 0.4 as a possible unadjusted split.
- Implied vol proxy: Cboe volatility-index CSVs, only for indices that SQ3 marks active. Map:
  SPY→VIX, QQQ→VXN, IWM→RVX, AAPL→VXAPL, AMZN→VXAZN, GOOGL/GOOG→VXGOG, GS→VXGS, GLD→GVZ,
  USO→OVX, EEM→VXEEM, SLV→VXSLV, XLE→VXXLE.
- Candidates: `notes/SQ3_candidates.txt` (liquidity order).

## Definitions (per ticker, per day t)
- `r_t` = ln(C_t / C_{t-1}). `rv60_t` = stdev(r over t-59..t) × √252.
- `σ10_t` = rv60_t × √(10/252): the 10-day move that recent realised vol implies.
- **`tail10`** = share of days where |ln(C_{t+10}/C_t)| > σ10_t. A normal distribution with
  correctly forecast vol gives ≈ 0.317. Higher values mean 10-day closes beat recent vol more often.
- **`excur10`** = median over t of max_{1..10}(max(H_{t+i}/C_t − 1, 1 − L_{t+i}/C_t)) / σ10_t.
  This is the largest swing *inside* a 10-day trade, relative to recent vol. It is what a
  strangle with a profit target can capture.
- **`expand`**: ATR20_t = 20-day mean true range. A day is compressed when ATR20_t/C_t is in the
  bottom 20% of its trailing 120 days. `ratio_t` = (max H − min L over t+1..t+10) / ATR20_t, and
  q80 = the ticker's 80th percentile of ratio_t over all days. `expand` = P(ratio_t ≥ q80 | compressed)
  ÷ 0.20, a lift over the unconditional base rate. Values above 1 mean compression is followed by
  outsized range more often than usual.
- `swing10` = median |ln(C_{t+10}/C_t)|, raw, for information only. It isn't scored because
  option prices already reflect a ticker's normal volatility.
- **`vrp`** = mean over t of (vol index_t − 100 × realised vol over t+1..t+21) in vol points, only
  where an index exists. Positive means implied usually exceeded the realised vol that followed,
  which is bad for buyers. It is reported, not scored, because it exists for only a few tickers and
  would make scores incomparable. (This departs from the brief's draft and was decided before the run.)
- `liq` = 1 − (liquidity rank − 1)/(N − 1) from the SQ3 order.

## Score and selection
- score = mean of the cross-sectional percentile ranks of tail10, excur10, expand and liq, all
  computed on the full period.
- Top 10 by score form the shortlist. Ties are broken by liq.
- Stability: recompute the ranks on 2016-11→2021-12 (IS) and 2022-01→2026-11 (OOS). Flag any
  ticker whose score rank moves more than 10 places.
- Where vrp exists and is above the median vrp of the indexed tickers, flag "implied usually rich":
  long options there need a stronger conditional edge.

## Known limitations (stated before the run)
- Earnings windows are included. They inflate tail10 and excur10 for single stocks, but implied
  vol prices earnings in, so a high score there does **not** mean cheap options.
- Realised-vol-relative metrics say how often moves beat *recent realised* vol, not *implied* vol.
  Only vrp, on a few tickers, touches implied. The real test is the v2 backtest with ORATS IV.
- Daily bars: intraday excursions are captured only through daily H/L.

## Change log (trials after first run)
- Pre-run amendment (2026-11-07, before running on any candidate): the self-test on an iid
  random walk (σ = 1%/day, 1,419 days) gives `expand` ≈ 1.9, not 1.0, and `tail10` ≈ 0.36, not
  0.317. The cause is estimation noise. A low ATR20 or rv60 reading is partly sampling error, so
  forward ranges look large relative to it. The score uses cross-sectional ranks, so the bias is
  common to all tickers and doesn't change the ranking. When reading absolute values, compare
  `expand` with the ≈ 1.9 null, not with 1.0. No definitions changed.
- Pre-run amendment (2026-11-07, before the candidate run): SQ3 found extra active Cboe indices.
  VXTLT, VXEWZ, VXFXI, VXEFA and VXIBM were added to the vol map (TLT and EWZ are candidates).
  VXXLE returned 403 and is treated as unavailable. vrp isn't scored, so the ranking is unaffected.
- Trial 1 (official, 2026-11-07): frozen definitions on 24 SQ3 candidates → `screen/metrics.csv`.
  VXTLT loaded no data (its CSV has a `DATE,VXTLT` header instead of `CLOSE`), so TLT has no vrp.
- Trial 2 (sensitivity, after seeing Trial 1): `payoff10` = expected payoff of a 1σ strangle priced at
  recent realised vol (`screen/trial2_payoff10.csv`). Reason: `tail10` penalises fat tails, which
  help long options. Reported only.
- Trial 3 (sensitivity): frozen score with at most 2 semiconductor names (6 of the official 10 are
  semis or semi ETFs). Reported only.
- Trial 4 (pricing test): 10-day ATM straddle priced at the Cboe vol index, gross
  (`screen/trial4_straddle_iv.csv`), on the 7 tickers with a usable index.
- Trial 5 (pricing test): Trial 4 split by entry condition: cheap (IV < rv20), rich, squeeze, and both
  (`screen/trial5_conditional.csv`).
- Trials counted: 5 (1 official ranking + 4 reported sensitivities). The deflated-Sharpe/PBO count in
  the v2 backtest should start from here.
