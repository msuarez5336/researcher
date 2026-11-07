# SQ2 notes (as of 2026-11-07)

## Answer
Volatility clustering (positive autocorrelation of volatility measures over days) is well documented in general (Cont 2001, Quantitative Finance 1(2):223-236; seen only via search snippet, not cached, unverified). But I found NO peer-reviewed or out-of-sample test that NR7, a Bollinger squeeze or an ATR percentile predicts a larger subsequent range or a profitable long strangle. Available "evidence" for squeeze/NR7 is assertion or vendor single-stock backtests (SQ2-1..4). Long straddle/strangle break-even is a realized-vs-implied variance condition (SQ2-5,6), and measured long-straddle results are poor when implied exceeds realized (SQ2-9,10). Compression signals must be treated as hypotheses to test, with a null baseline.

## (1) Compression definitions
| Definition | Formula | Evidence found | Effect size | Daily OHLC? |
|---|---|---|---|---|
| NR4/NR7 (Crabel 1990) | High-Low is min of last 4 / 7 bars | Assertion only (SQ2-1,2); TradingView 65%-vs-50% claim unmethodised, not cached | none verified | Yes |
| Bollinger BandWidth squeeze | (Upper-Lower)/Middle, 20d, 2 sd; "low" = <10% or 125-day low (Nasdaq snippet, not cached) | Assertion (SQ2-3); vendor single-stock backtest (SQ2-4) | none verified | Yes (close only) |
| ATR / realised-vol percentile | ATR14/close or close-to-close/Parkinson/GK vol, percentile over 126-252d | Not found as a tested predictor; rationale = vol clustering/mean reversion | none | Yes |
| GARCH conditional vol | Engle 1982, Bollerslev 1986 | Not retrieved; clustering is persistence, so low vol tends to be followed by low vol short-run (opposes naive "coil" idea) [O, my inference] | none | Yes (fitted) |
| Range ratio (e.g. 5d range / 20d range) | judgement | none | none | Yes |
Key caveat: clustering implies persistence in the short run; mean reversion to a long-run level is the only support for expansion, and it acts over weeks-months, not 3-10 days.

## (2) Strangle rules (coder-implementable)
- Legs: long OTM call + put at ~25-30 delta (judgement; Fidelity SQ2-8 notes strangle decays faster/more total-loss than straddle). Also test ATM straddle as control.
- DTE: enter 35-60, exit by 21 (brief spec; tastylive 21-DTE management is for short premium, not validated for longs).
- Entry trigger: compression flag (NR7 or BandWidth/ATR percentile <=10-20) AND an option-side filter: implied move (straddle price/spot) below trailing realized move over equal horizon. Judgement, supported by SQ2-10 (entry pays only when implied < realized).
- Break-even: total premium P; need |move| > P at exit, or on day basis ~ S*IV/sqrt(252) per day per SQ2-6. Compare implied move to median of historical 3-10d absolute return.
- Profit target: judgement, e.g. +30-50% of debit; stop: -40-50% debit; time exit: day 10 or 21 DTE whichever first. No source.
- Fills: k=0.70 of spread per leg per brief; run sensitivity k=0.5/1.0.
- Controls: random-date entries, and same-trigger entries with no filter; report per-trade median as well as mean.

## (3) Traps
- IV crush/earnings: exclude earnings windows (SQ2-9: mean IV drop 15.6 vol pts, 22% win rate, -18.5%/trade). [E, vendor]
- Vega: positive vega, so IV falling during compression hurts (SQ2-7). Lagged IV compresses with realised vol, so cheapness is not edge.
- Theta: strangle decays faster than straddle (SQ2-8); breakeven needs moves > S*IV/sqrt(252) daily (SQ2-6).
- Skew: OTM puts richer than calls on equities; fixed-delta strangle is asymmetric in cost; use same-delta and report each leg [O, general knowledge, no source retrieved].
- Fills/spreads on OTM legs; stale quotes; use bid/ask, never mid.
- Overlapping signals (clustered NR7 days) inflate sample count; de-dupe, use cooldown.
- Multiple testing of thresholds; use out-of-sample years.
- Look-ahead: compute signal on close, enter next open/close.
- Direction-neutral flags: SQ2-1.

## Conflicts
Practitioner sources (StockCharts, LuxAlgo, SentimenTrader) assert squeeze precedes expansion; none supplies a baseline. ORATS/Nasdaq 2019 result (SPX 30 DTE long straddle exit 10d; reported +3.36% annualised since 2018 but worse since 2007) came only via search snippet; fetch failed; unverified. Option Strategist and tastylive (snippets, pages thin) argue no edge buying low-IV straddles.

## Not found
Peer-reviewed test of NR7/squeeze/ATR percentile -> range expansion; any published long strangle backtest with delta/DTE/exit setups on ETFs; Natenberg/Sinclair/Hull quote (not accessible); Harbourfront VIX reversion claim unverified.

## Blocked
nasdaq.com (RemoteDisconnected); arxiv PDF unsupported by fetcher; tastylive pages returned only boilerplate (thin); papers.ssrn.com not attempted.

## Search log
1 NR7 no edge (disconfirm): 0 rigorous. 2 Bollinger squeeze expansion: vendor only. 3 straddle breakeven: FlashAlpha, Fidelity. 4 tastylive long strangle: short-strangle only. 5 low-vol regimes papers: weak. 6 long straddle backtests: IVolatility, ORATS snippet. 7 BB squeeze fails (disconfirm): none. 8 Coval-Shumway: SQ1 scope. 9 Cont stylized facts: snippet. 10 low-IV straddle: Option Strategist snippet. Fetch batches 3 (one failed).
