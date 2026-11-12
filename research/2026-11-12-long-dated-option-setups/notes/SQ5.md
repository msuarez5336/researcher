# SQ5 notes (as of 2026-11-12). Budget: 20 calls used.

## Answer
Real end-of-day US stock-option history is purchasable by an individual: ORATS (2007+, $599 one-time seen), iVolatility (2005+, pay per ticker-day, $0.40), FirstRate (2010+, delisted-after-2010 included, price not retrieved), Cboe DataShop (2012+, price not retrieved), MarketData.app (2010+, no historical IV), ThetaData. No free source of historical stock-option quotes was found. I found NO paper that measures how far a model price built from realised vol, a vol index or a fitted surface sits from actual historical quotes; accuracy of estimates is largely "not found", and the measured biases found concern real closing quotes, not estimates.

## Findings
- FirstRate: from Jan 2010, bid/ask, bid/ask IV, OI, greeks; >4000 delisted tickers (only delisted after 2010). [E, self-reported] SQ5-1, 2. Price not retrievable (verified false for price).
- ORATS: ~6,000 symbols, snapshot 14 min before close, since 2007; $99/mo forward, $599 one-time history (seen 2026-11-12); no US stock prices supplied. [E, self-reported] SQ5-3,4,5. Delisted coverage not stated.
- iVolatility: since 2005, $0.20/$0.40/$0.60 per ticker-day by dataset (seen 2026-11-12); bid/ask/IV/greeks/volume/OI described; 5 tickers x 30 days = $60. Delisted: search snippet only. SQ5-6.
- MarketData.app: EOD quotes from 2010 with OI and volume; no historical greeks/IV (you would compute IV yourself). SQ5-7.
- ThetaData: Individual plan personal-use only, $40/$80/$160 per month; history years and EOD IV not verified. SQ5-8.
- Cboe DataShop: bid/ask+size at 15:45 and close, OHLC, volume, OI, from Jan 2012; IV/greeks at 15:45 extra. SQ5-9,10.
- Closing-quote bias [E, hedged]: Goyenko-Zhang: close mid-quotes inflate delta-hedged returns vs other intraday mids, up to 1%/day. Sample/maturity not read. SQ5-11. Molnar et al. 2025 and Wallmeier 2024 report further measurement-error and timing problems (snippets, unverified). SQ5-14,15.
- Per-stock vol indexes: Cboe VIX-method indexes exist for only five names since 2011 (SQ5-12); FRED carries VXAPL (SQ5-20). Not usable as a general screen input.
- Free partial: Cboe free monthly/yearly volume files (SQ5-13, unverified); OCC batch volume/OI downloads (SQ5-19, unverified, per-symbol history not confirmed). Own daily snapshots going forward: not searched in depth; the ORATS $99/mo and MarketData.app plans are paid routes; no free source verified.
- Realised-vol-fed pricing: look-ahead risk if vol measured forward [O] SQ5-18. Carr-Wu: stock variance premium mostly negative, smaller than index [E, unverified] SQ5-16, so a realised-vol model would on average price below real quotes; magnitude not extracted.
- Surface-fitting: only within-day fit comparisons found; no test of projecting a surface backwards. SQ5-17.

## Table (a) data sources
| source | history | fields | strikes/expiries | snapshot | expired/delisted | price, date seen | limits | ids |
|---|---|---|---|---|---|---|---|---|
| FirstRate | 2010+ | bid/ask, bid/ask IV, OI, greeks, last | full chain | not stated | delisted after 2010 yes | not retrievable | licence not read | 1,2 |
| ORATS near-EOD | 2007+ | bid/ask/mid IV, vol, OI, greeks, SMV | full chain ~6000 symbols | 14 min pre-close | delisted not stated | $599 one-time, $99/mo; 2026-11-12 | 14-day S3 download window; no stock prices | 3,4,5 |
| iVolatility | 2005+ (varies) | NBBO, vol, OI, IV, greeks | every listed contract | not stated | snippet: delisted yes (unverified) | $0.40/ticker-day (opt prices), $0.60 IV; 2026-11-12 | pay per use | 6 |
| MarketData.app | 2010+ | bid, ask, last, vol, OI; no hist IV | full OPRA | not stated | not stated | not retrievable | no intraday history | 7 |
| ThetaData | 6/10/14 yrs (unverified) | not verified for EOD IV | n/a | n/a | n/a | $40/80/160 mo; 2026-11-12 | personal use only | 8 |
| Cboe DataShop | 2012+ | NBBO+size, OHLC, vol, OI; IV/greeks extra | every series | 15:45 and close | not stated | not retrievable | per-file purchase | 9,10 |
| Cboe volume files | from 2019 page | volume only | by symbol | n/a | n/a | free (unverified) | no OI | 13 |

## Table (b) estimation methods
| method | inputs | measured error vs real quotes | known bias | supports / cannot support | ids |
|---|---|---|---|---|---|
| BS + trailing realised vol | stock prices, rate, dividends | NOT FOUND | variance premium mostly negative so model tends to under-price; no skew; no event premium; no spread | rough screening of price level only; not skew, event, or IV-based signals | 16,18 |
| BS + forward realised vol | same | n/a | look-ahead | invalid | 18 |
| BS + vol index (market or 5 stocks) | Cboe index, stock | NOT FOUND | only five stocks have indexes | none for general stocks | 12 |
| fitted IV surface backward | short real sample | NOT FOUND (only in-sample fit studies) | extrapolation untested | cannot be validated | 17 |
Spreads: none of the above model bid-ask. Signals computed from option prices cannot run on estimates.

## Conflicts
None direct. Vendor claims are self-reported. Closing-quote bias (Goyenko-Zhang) conflicts with using end-of-day snapshots as fill prices; ORATS 14-min and Cboe 15:45 snapshots are vendor mitigations.

## Not found
Any study quantifying the error of model-estimated historical option prices vs quotes; any backtest on estimated prices with reviewer critique; free historical stock-option quotes; pricing for FirstRate, Cboe, MarketData.app. Not searched: broker feeds, self-snapshot tooling, Polygon/Massive, OptionMetrics/WRDS pricing (academic access), historicaloptiondata.com, OptionsDX product pages (shop lists TSLA/AAPL/NVDA etc. chains, $0-$20 per product, WebFetch only).
All studies cited: sample period/maturity/costs not read in most; none verified as ending after 2015.

## Blocked
Molnar PDF, unifr.ch PDF: fetch_page unsupported (PDF); SSRN not tried. Pricing pages dynamic for FirstRate, Cboe.

## Search log
1 vendor broad (search, 6 sources); OptionsDX/Cboe/Theta fetches (3); fetch_page 7 vendors; BS-realised-vol accuracy (disconfirm, 0 useful papers); IvyDB errors (disconfirm, 4); Goyenko-Zhang (2); BS historical vol studies (weak); Cboe single-stock indexes (3); PDF fetch 5; surface extrapolation (0 direct); Cboe free files (1); grep (1); Molnar (0 new); OCC (1); variance premium (1 Carr-Wu).
