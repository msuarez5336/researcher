# SQ7 notes (as of 2026-11-12)

## Answer
Fill assumptions: the only measured cost evidence found is on samples ending 2006 (before 2015). It gives quoted spreads of about 23-34% of midpoint for S&P 500 component OTM calls, and for traders who cannot time quotes an effective cost near the conventional effective spread (about 77% of the quoted spread, 6.2 vs 8.1 cents); the "half the quote" figure applies only to sophisticated timers. Use a fill at or beyond mid, scaled to the quoted spread, and charge it at both entry and exit. For many tested conditions use a t-hurdle well above 2 (HLZ: >3.0 in equity factors), correct for overlap (divide t by sqrt of the horizon in the sample's unit), and hold out final data. Call debit spread vs outright call: no single-stock evidence found. Of 20 calls, this run did not reach topics (3) in depth, (4) in depth, or (5).

## Findings
- [E] Quoted spread 8.1c, conventional effective 6.2c, adjusted effective about half the quote; timed trades 1.3c; untimed traders bear the conventional effective spread. 2003-2006, 37 stocks. Secondary summary. SQ7-1, SQ7-2
- [E] Relative quoted spread: short-term (20-70d) OTM calls 34%, long-term (71-180d) OTM calls 23%; OTM wider than ATM than ITM; 1996-2007, S&P 500 stocks. Mid-based returns exclude costs. SQ7-3, SQ7-4
- [E] Spread depends on option return volatility and expiration-cycle availability, not simply on maturity. SQ7-5
- [O] ORATS (vendor): quotes 14 min before close, slippage 75% of bid-ask width for single legs, 53% for four legs. SQ7-6
- [E] Multiple testing: t>3.0 hurdle (equity factors, not options). SQ7-7. FDR selection did not persist out of sample and low costs erased in-sample gains (technical rules, 1897-2011). SQ7-8
- [O/E] Overlap: divide t by sqrt(horizon). SQ7-9
- [E] Index-option bull call spreads: returns heavily cost-affected (index, not single stock). SQ7-10
- [O] Survivorship: need expired contracts and delisted underlyings retained. SQ7-11

## Tables
(a) cost or error | measured size | sample period | what a backtest should do | evidence
- Quoted spread, short-term OTM call | 34% of mid | 1996-2007 (ends <2015) | charge the cost; no fixed fraction given by source | SQ7-3
- Quoted spread, long-term (71-180d) OTM call | 23% of mid | 1996-2007 (ends <2015) | same | SQ7-3
- Effective cost, untimed trader | 6.2c vs 8.1c quote, about 77% of quote | 2003-2006 (ends <2015) | fill about three quarters of the way across the quoted spread; this ratio is my arithmetic from the source's two figures | SQ7-1, SQ7-2
- Effective cost, timed trader | about 50% of quote; timed trades 1.3c | 2003-2006 | do not assume for retail | SQ7-1
- Vendor slippage | 75% of width single leg | unknown | vendor's own rule, self-reported | SQ7-6
- Mid-price returns | exclude spread; illiquid options show higher gross returns | 1996-2007 | do not rank by mid-priced return | SQ7-4
- Delisted names / expired contracts missing | no size measured | n/a | require retained data, historical universe | SQ7-11
- Stale quotes, early exercise, dividends, splits, look-ahead | no measured size found | n/a | not searched beyond one vendor page | none

(b) statistical problem | recommended method | independent periods adequate | source | evidence
- Many conditions tried | t-hurdle above 3.0 (factor setting); FDR control | none stated | HLZ; Bajgrowicz-Scaillet | SQ7-7, SQ7-8
- Overlapping 1-6 month holds | divide t by sqrt(horizon); robust errors perform poorly in small samples (search snippet, not cached) | none stated | Hjalmarsson | SQ7-9
- Few big wins among total losses | not found | not found | not found | none
- Final holdout | not found as a measured rule | not found | not found | none
- Deflated Sharpe (Bailey-Lopez de Prado), Harvey-Liu Sharpe haircut: seen only in search snippets (SSRN 403, PDFs uncacheable); unverified, not recorded as evidence.

## Conflicts
- Muravyev-Pearson say effective costs are about half the quote; that holds only for traders who time quote changes. Untimed traders pay about 77% of the quote. Vendor ORATS assumes 75% of width for single legs, consistent with the untimed case.
- Hedged results (O'Donovan-Yu 2024, seen only in a snippet: none of 24 delta-hedged portfolios profitable after costs) concern hedged returns, not buyer returns; not recorded.

## Not found
- Single-stock call vs call debit spread vs longer-dated evidence (only index McKeon abstract; vendor/broker backtests ignored).
- Spread by strike distance and company size measured; bought-option backtests with costs for 1-6 month maturity.
- Early exercise, dividends, splits error sizes. Position sizing (5): not searched.

## Blocked
papers.ssrn.com (403), core.ac.uk (403), nasdaq.com (disconnect); PDFs (Duke, NBER, mql5 copy of Muravyev-Pearson) unsupported by fetch_page, so original paper figures are via CXO summaries (secondary).

## Search log
1 spreads by maturity/moneyness (search, several sources); 2 effective spread fraction (search, 3 new); 3 multiple testing (search, 3); 4-5 WebFetch PDFs failed; 6 criticism of spreads/corrections (disconfirm, 2 new: CXO, ORATS); 7 cache fetches; 8 read cached; 9 call spread (search, McKeon); 10 overlap (search, Hjalmarsson); 11 backtest pitfalls (search, FlashAlpha); 12-13 cache and grep; 14 transaction cost (search, no new); 15 FDR (search, Bajgrowicz); 16 cache/check. About 19-20 calls used.
