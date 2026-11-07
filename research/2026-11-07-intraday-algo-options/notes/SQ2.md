# SQ2 notes (as of 2026-11-07)
## Answer
No options-derived signal found with robust, costed, out-of-sample evidence for predicting direction of an ETF over hours-to-days. Best-supported: negative net-gamma days show stronger intraday momentum (S&P futures, to 2020); implied move/VIX1D is a reasonable but slightly rich range yardstick (close contained ~71% for 10:00 straddle, 193 SPY days). GEX itself shows no incremental volatility or direction power over VIX/IV in the one open backtest found (vendor, EOD).
## Findings
- GEX adds nothing beyond VIX/ATM IV for next-day RV; DEX no next-day direction [E] SQ2-1, SQ2-2 (vendor blog, grade B, single author).
- Hedging feedback adds no intraday-variance power in a student thesis [E] SQ2-6 (grade C, not peer reviewed).
- Negative NGE days: intraday momentum; positive NGE: none [E] SQ2-7 (peer reviewed JFE, but NGE from index options+leveraged ETFs, futures, to 2020, no option P&L).
- Straddle implied move contains close 71.0%; realized ~13% below implied [E] SQ2-3. VIX1D overestimates realised vol [E] SQ2-4.
- Pan-Poteshman put-call signal: 1990-2001, outdated, single stocks, signal needs buyer-initiated open volume (needs OPRA/ISE-type open-close data) [E] SQ2-5.
## Conflicts
- Gamma mechanism: positive dealer gamma dampens intraday vol/reversal (Quantpedia-reviewed paper, unidentified, via search snippet only) versus thesis finding no hedging channel (SQ2-6) versus Baltussen momentum on negative NGE (SQ2-7). Conditions differ (variance vs return, futures vs index).
- Expected move vs range: close-to-close containment ~71% (SQ2-3) vs unverified video claim that SPX high-low range is ~2x VIX1D move. Not recorded as evidence.
## Not found
- Post-2010 replication of Pan-Poteshman; independent peer-reviewed GEX estimation-error study; any costed backtest of buying options on a gamma/flow signal; verified IV skew/term-structure intraday direction studies (not searched, budget); unusual option volume studies.
## Blocked
- research.glassnode.com 403 (Glassnode claim: naive GEX sign assumption misestimates dealer position; unverified, search snippet only). nd.edu PDF unsupported content-type by fetch_page (used Alpha Architect page copy of paper text instead). SSRN not tried.
## Search log
1 dealer gamma intraday 0DTE (search; 0 usable beyond thesis). 2 GEX does not predict (disconfirm; FlashAlpha). 3 Baltussen (lead). 4 VIX1D expected move (search; FlashAlpha, JFM). 5 Pan Poteshman (lead; NBER). 6 0DTE order flow (search; Princeton ES-futures thesis: ~0.48 ES pts per SD signed delta flow, unrecorded). Budget used about 12 of 15.
## Table
| signal | data needed | horizon | target | use | sample | effect size | OOS? | grade | source id |
|---|---|---|---|---|---|---|---|---|---|
| GEX level | OI by strike, IV, dealer-sign assumption | next day | range | filter | SPY 2018-26 | none after VIX/IV controls | no | B | SQ2-1 |
| DEX | OI, delta | next day | direction | entry | SPY 2018-26 | 0.00% top-bottom | no | B | SQ2-2 |
| Net gamma sign | index option OI, lev-ETF AUM | last 30 min | direction | filter | futures 1974-2020 | momentum only on negative NGE | no | C | SQ2-7 |
| Hedging channel | 0DTE flow | intraday | range | filter | 2026 thesis | no added power | partly | C | SQ2-6 |
| Straddle implied move | ATM 0DTE quotes | same day | range | target/filter | SPY 193 days 2022-26 | 71.0% contain close | no | B | SQ2-3 |
| VIX1D | Cboe index | 1 day | range | filter | SPX, JFM 2025 | overestimates RV | yes (paper) | A | SQ2-4 |
| Put-call ratio (open buy volume) | OPRA open/close | 1-5 days | direction | entry | stocks 1990-2001 | 40bp/day, 1%/wk | no | A | SQ2-5 |
