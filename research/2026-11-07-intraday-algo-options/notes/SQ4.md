# SQ4 notes (as of 2026-11-07)

## Answer
No study found that tests stop, target or time exits on long single options. The evidence is from stocks and futures (transfer to options unproven) and is mixed. Stops help mainly when returns are trending, and they cut volatility more than they add return. ATR-scaled stops beat fixed-dollar stops only modestly in the one practitioner test found, and no stop beat both in that test.

## Findings
- [E] Kaminski & Lo: on index futures, stop-loss policies can raise expected return and cut volatility at longer sampling frequencies (SQ4-1). Search summary said that under a random walk stops only lower expected return; I could not cache the full text (MIT PDF HTTP 429), so that statement is not in the evidence file.
- [E] Lei & Li: stocks, stops neither reduce nor increase losses vs buy-and-hold (SQ4-2). They tested stops of 5, 10 or 20 daily-return standard deviations (SQ4-7, unverified snippet).
- [E] Practitioner futures test: ATR stop beat dollar stop 66% of the time, but no stop was best (SQ4-3, SQ4-4). Grade C, in-sample, slippage included.
- [E] 1DTE SPX iron condor (short premium): 50-70% of stop-outs would have recovered (SQ4-5). Opposite sign to long options, so only the whipsaw mechanism may transfer.
- [E, unverified] Trailing stop Sharpe 1.28 vs 0.92 fixed, commodity factors (SQ4-6).

## Conflicts
Kaminski & Lo and Fan & Zhang say stops help (with momentum or regime shifts, or in commodities). Lei & Li and the practitioner test say no benefit in return terms. Which holds depends on return autocorrelation. Nothing tested long options.

## Not found
- Any study of percent-of-premium stops on long options.
- Any study of sigma, expected-move or ATR targets on long options.
- Any study of time stops or breakeven stops on long options.
- Any study of partial exits.
- Authoritative broker docs on options stops: the Schwab and ISE pages failed. The Cboe article URL returned 404.
- Only a search snippet supports the order-mapping claims below; no cached source does. Treat them as [O] practitioner opinion.

## Blocked
dspace PDF (429), acfr.aut.ac.nz (403), iseoptions.com and stocknews.com (404), Schwab help page (502).

## Search log
1. Kaminski Lo stop-loss (search): 1 source.
2. ATR vs fixed stop (disconfirm and search): 2 sources.
3. 0DTE long-option stop premium (search): 1 source.
4. Exit rules long options study (search): 1 source.
5. Volatility-scaled stop momentum (search): 1 source.
6. Lei & Li (search): 1 source.
7. Options stop mapping, underlying alert (search): 0 usable cached.
8. 0DTE time-of-day theta (search): 0 usable.

## Table 1
| exit rule | defined on | unit | tested where | sample | effect vs baseline | grade | source |
|---|---|---|---|---|---|---|---|
| ATR stop vs dollar stop | underlying | ATR | futures (crude, gold, mini S&P), daily | about 5 years | ATR won 66% of comparisons; no stop beat both | C | SQ4-3, SQ4-4 |
| Stop at 5, 10 or 20 daily sigma | underlying | daily sigma | US stocks | 1970-2005 | no return gain; risk down for trailing | A/C | SQ4-2, SQ4-7 |
| Stop-loss policies | underlying | percent loss | index futures | daily | more return and less volatility at longer frequencies | A | SQ4-1 |
| Trailing vs fixed stop | underlying | percent | commodity factors | 1983-2022 | Sharpe 1.28 vs 0.92 (unverified) | B | SQ4-6 |
| Max-loss stop | option spread | credit multiple | SPX 1DTE iron condor | 2022-2025 | 50-70% of stops would have recovered | C | SQ4-5 |
| Premium stop, time stop, breakeven, partial exit on long options | n/a | n/a | not tested | n/a | no evidence | n/a | none |

## Table 2
| exit rule | broker order needed | known execution risk |
|---|---|---|
| Stop on option premium | stop or stop-limit on the option, with OCO or bracket | [O] wide or briefly spiking quotes can trigger it; a stop becomes a market order; thin contracts may not allow stops |
| Underlying sigma or ATR level | price alert or conditional order on the underlying, then a limit sell on the option | [O] needs a platform supporting conditional orders; the option's bid-ask at trigger is unknown |
| Time stop | time-based or manual sell, or a conditional order | [O] spread widens near the close; no tested evidence |
