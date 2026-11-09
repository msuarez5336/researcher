# SQ5 notes (as of 2026-11-09)

## Answer
I found no first-hand account with trade count, period and P&L that I could open and cache. Reddit pages were reachable only through mirrors and search snippets, and the reddit.com search endpoint returned 403. The measured evidence is mostly negative on buying options: retail 0DTE buyers lost money after costs, and the volatility risk premium makes long index options negative in expectation. Evidence on the specific practices (delta, DTE, 50% stops, 1-2% risk) was not found for long options.

## (1) First-hand accounts (all from search snippets via mirrors, NOT opened or verified; none cited in the evidence file)
| URL | date | strategy | holding | platform | period | numbers as stated | repo | grade |
|---|---|---|---|---|---|---|---|---|
| reddit.sentinel-team.org mirror of r/algotrading post (id not resolved) | 2026 | bot, 0-4 DTE long-only options | 0DTE/short swing | unknown | 19 trading days | +39% return, 12.87% max drawdown, commenters flagged small sample/overfit | none seen | C |
| mirror of r/algotrading post | 2026 | call-buying momentum bot | short swing | unknown | 1 week forward test | 38 trades, 73.7% win rate; author said earlier backtests diverged from live | none seen | C |
| mirror of r/algotrading post | 2026 | call buyer on bullish crossover, ITM | unknown | unknown | unknown | no numbers; commenters said slippage/fills main gap | none seen | C |
Mirror host: reddit.sentinel-team.org (snapshots). Treat as unverified leads for a follow-up that can reach reddit.

## (2) Practices
| practice | for | against | conditions | source |
|---|---|---|---|---|
| Buy ITM / higher delta | Bakshi-Kapadia: underperformance is smaller away from the money (cuts the other way, favours OTM, for delta-hedged returns) | none for outright long | S&P 500 index, delta-hedged, pre-2003 data | SQ5-2 [E] |
| Longer DTE, exit early | none found for long options | ORATS test is for short calls only | n/a | SQ5-6 context |
| 1-2% risk, 50% stop, fixed profit target | none found | none found | n/a | not found |
| Avoid earnings | IV contracted ~90% of 1,546 events (SQ5-4); long straddle -18.5%/trade, 22% WR (SQ5-3) | search snippet (not cached): OptionAlpha reported a 50-delta long straddle entered 20 days before earnings and exited at earnings as top performer; IVolatility notes META and PLTR profitable | straddles, not single calls; vendor data | SQ5-3, SQ5-4 [E] |
| Buy when IV low | Bakshi-Kapadia: underperformance greater at high volatility | none tested directly | index, delta-hedged | SQ5-2 |
| Liquid, tight spreads | Beckmeyer et al.: ~60% of retail 0DTE losses were transaction costs; FlashAlpha: result flips with fill model | none | SPX 0DTE retail; short put spreads | SQ5-1, SQ5-5 |
| 0DTE time windows / hard stops | none found | none found | n/a | not found |

## Findings
- [E] Retail 0DTE SPX buyers lost heavily after costs (SQ5-1). Secondary coverage only; paper at SSRN 4404704 not reached. Dollar totals differ by source ($70M in some summaries vs $20M in Bloomberg), different windows.
- [E] Long (delta-hedged) index options have negative average return (SQ5-2).
- [E] Earnings straddle buying is negative on average in vendor tests (SQ5-3, SQ5-4).
- [E] Backtests with mid fills overstate results (SQ5-5).

## Conflicts
Earnings: aggregate long-straddle expectancy is negative (IVolatility) but OptionAlpha's best strategy was a long straddle entered 20 days early; entry timing and single names matter. Search snippets only for the latter, not cached.

## Not found
First-hand long-option bot post-mortem with trade count, period, P&L and costs; any measured test of delta/DTE/stop/profit-target rules for long options; position sizing evidence; 0DTE time-window evidence. No paper cached for Beckmeyer et al.

## Blocked
- www.reddit.com search.json: 403 (fetch_page.py). 
- WebSearch with allowed_domains reddit.com: refused.
- cfr-cologne.de PDF: unsupported content type in the fetch script.
- SSRN not tried/reached.

## Search log (calls used: 12 of 15)
1 search 0DTE retail losses: 3 sources. 2 search reddit bots: mirrors, snippets only. 3 search long option backtest: only short-premium results. 4 fetch cache 4 pages (1 unsupported). 5 search earnings IV crush: 4 sources. 6 search bot post-mortem: generic, non-options. 7 fetch 3 pages (reddit 403). 8 bash grep (counted). 9 search Bakshi-Kapadia (disconfirm). 10 search reddit domain: refused. 11 fetch repec and dev.to. 12 search Beckmeyer: no new sources. Wasn't a dedicated "disconfirm" beyond items 1, 9.
