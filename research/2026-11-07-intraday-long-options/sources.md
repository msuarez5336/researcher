# Sources: same-day long options on liquid US underlyings

*As of 2026-11-07. Ranked by usefulness to the question, not by popularity.*

**Status key:**
- ✓ verified against the original page, by quote check and a fresh-context claim-verifier;
- ~ read via a summary or snippet only;
- ✗ unreachable.

Vendor and exchange pages describe their own products or markets: **self-reported**.

## Primary sources (papers, official docs, first-party write-ups)
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | Doshi, Pederzoli & Sert, [Risky Intraday Order Flow and Option Liquidity](https://bauer.uh.edu/hdoshi/docs/DPS_May_2025.pdf) | working paper (PDF, read via pdftotext) | 2025-05-23 | ✓ {C1}; ✓ narrowed {C2} | SQ3-9, SQ3-10 | Best measured 0DTE cost figure: ATM SPX effective spread 8.7–9.5% (2004–2021). The sample predates SPX daily expiries. |
| 2 | Cboe, [What the VIX and VIX1D indices attempt to measure](https://www.cboe.com/insights/posts/what-the-vix-and-vix-1-d-indices-attempt-to-measure-and-how-they-differ) | exchange, self-reported | 2023 | ✓ {C3} | SQ3-1, SQ3-2 | Explains why VIX1D can't be read as same-day vol after about 3 pm. Essential for interpreting the study. |
| 3 | Narain, [Market impact of Fed communications: the role of the press conference](https://www.ijcb.org/journal/v22n1/market-impact-fed-communications-role-press-conference) | journal (IJCB) | 2026-01 | ✓ {C13} | SQ2-7, SQ2-8 | Motivates H-FOMC1: Powell press conferences carry more than 3× the volatility of his predecessors' and reverse the statement move. |
| 4 | Gao, Han, Li & Zhou, Market intraday momentum ([econpapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414)) | journal (JFE), abstract | 2018 | ✓ narrowed {C6} | SQ1-1 | Origin of first → last half-hour momentum. Too small to pay for 0DTE (our W3). |
| 5 | Baltussen, Da, Lammers & Martens, Hedging demand and market intraday momentum ([econpapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403)) | journal (JFE), abstract | 2021 | ✓ {C8} | SQ1-5 | Gamma-hedging mechanism; futures-wide. |
| 6 | Rosa, intraday momentum out of sample ([econpapers](https://econpapers.repec.org/RePEc:wly:jfutmk:v:42:y:2022:i:12:p:2218-2234)) | journal (JFM), abstract | 2022 | ✓ {C7} | SQ1-4 | Counter-evidence: the overnight variant disappears out of sample. |
| 7 | Lou, Polk & Skouras, A tug of war ([econpapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:134:y:2019:i:1:p:192-213)) | journal (JFE), abstract | 2019 | ✓ {C10} | SQ1-10 | Overnight vs intraday split. Framing for the H-MOM1 open entry. |
| 8 | Cboe notice, [Monday/Wednesday expirations](https://www.cboe.com/notices/content/?id=58202) | exchange notice | 2026-01 | ✓ narrowed {C14} | SQ3-8 | Single stocks have no daily expiries. Lists the eligibility criteria. |
| 9 | Zarattini, Barbon & Aziz, [A profitable day trading strategy for the US equity market](https://ideas.repec.org/p/chf/rpseri/rp2498.html) | working paper (SFI RP 24-98) | 2024 | ✓ narrowed {C9} | SQ1-6 | Strong ORB claims, not peer-reviewed. The source of H-ORB-QQQ1. |
| 10 | Heston, Korajczyk & Sadka (JF 2010), Glasserman et al. (arXiv 2025) | journal / preprint, abstracts | 2010 / 2025 | ✓ (quote check only) | SQ1-11, SQ1-12 | Background on intraday periodicity and overnight returns. Not load-bearing. |
| 11 | ORATS [one-minute data](https://orats.com/one-minute-data), [intraday API docs](https://orats.com/docs/historical-intraday-api) | vendor, self-reported | 2026 | ✓ {C16} | SQ4-1..3 | Recommended vendor if IV/Greeks are needed. Its underlying price is option-implied. |
| 12 | Cboe DataShop [Option Quote Intervals](https://datashop.cboe.com/options-intervals) | vendor, self-reported | 2026 | ✓ {C19} | SQ4-10..12 | Deepest NBBO history (2012). Price not listed. |
| 13 | Databento [OPRA docs](https://databento.com/docs/venues-and-datasets/opra-pillar), [options](https://databento.com/options) | vendor, self-reported | 2026 | ✓ {C17} | SQ4-4..6 | Cheap pilot. Subsampled before 2023-03-28. No Greeks. |
| 14 | ThetaData [subscriptions](https://http-docs.thetadata.us/Articles/Getting-Started/Subscriptions.html), [data issues](https://docs.thetadata.us/Articles/Data-And-Requests/Data-Issues.html), [options data](https://thetadata.net/options-data) | vendor, self-reported | 2026 | ✓ corrected {C18} | SQ4-7..9 | Options: Value 1-minute from 2020, Standard tick from 2016, Pro from 2012-06. Prices not read. |
| 15 | Massive [quotes docs](https://massive.com/docs/rest/options/trades-quotes/quotes.md), [flat files](https://massive.com/docs/flat-files/options/quotes) | vendor, self-reported | 2026 | ✓ {C20} | SQ4-13, SQ4-14 | Quotes from 2022-03-07 on Options Advanced ($199/mo). No historical Greeks. |
| 16 | Cboe, [Evaluating the market impact of SPX 0DTE options](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options) | exchange, self-reported (an interested party) | 2023-09-08 | ✓ narrowed {C12} | SQ2-4, SQ2-5 | Descriptive "no impact" view. Dated. |

## Data sources used by the study (all reached 2026-11-07)
| Source | What | Status | Verdict |
|---|---|---|---|
| Yahoo chart API (query1.finance.yahoo.com) | 1-hour bars for SPY, QQQ, ^VIX1D, ^VIX, ^VIX9D, ^VXN; 5-minute bars for SPY and ^VIX1D | ✓ cached in `study/data/` | Only free intraday VIX1D. About 2.8 years. Raw files committed, because the window rolls. |
| Cboe cdn.cboe.com daily index CSVs | VIX1D (from 2022-05-13), VIX, VIX9D, VXN | ✓ | Reliable. |
| api.nasdaq.com historical | daily OHLCV 2016-10 → 2026-11 | ✓ | As in the prior runs. |
| Concretum Group [macro calendar](https://calendar.concretumgroup.com) (public export endpoint) | CPI, NFP, FOMC, ISM dates and ET times | ✓; FOMC matched federalreserve.gov (40 of 40) | Third party; stands in for bls.gov (blocked). |
| federalreserve.gov FOMC calendar | statement dates | ✓ | Authoritative. |
| Prior run's `continuation/events.csv` (branch `claude/inspiring-cerf-epxwvd`) | H-MOM1 events, earnings excluded | ✓ (git) | Reused, not re-derived. |

## Secondary and practitioner sources
| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 17 | [Retail investors are in love with same-day options](https://www.wealthmanagement.com/equities/retail-investors-are-in-love-with-same-day-options) (summary of Beckmeyer, Branger & Gayda) | WealthManagement | 2023 | ✓ {C4} against the summary; the paper was not read (SSRN blocked) | Retail long 0DTE −53% / −61% per position. Use with that caveat. |
| 18 | [Quantpedia summary](https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/) of Adams et al., SSRN 5641974 | Quantpedia | 2026 | ✓ narrowed {C11} | 0DTE dampens volatility on average. Originally misattributed to Dim, Eraker & Vilkov by the worker; corrected. |
| 19 | [The 0DTE illusion](https://breakingnasdaq.beehiiv.com/p/the-0dte-illusion); [Hull Tactical](https://hulltactical.com/2026/07/08/0dte-options-tiny-edge-huge-distribution/) (summaries of Vilkov) | blogs | 2026 | ✓ {C5} against the summaries only | Tiny 0DTE VRP. Vilkov's paper not read. |
| 20 | CXO Advisory ([intraday momentum](https://www.cxoadvisory.com/?p=25481), [ORB on QQQ](https://www.cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy)) | CXO | 2014 / 2023 | ✓ {C6, C7, C9} | Useful replication context. Secondary. |
| 21 | [MQL5 ORB replication](https://www.mql5.com/en/blogs/post/776235) | independent trader, self-reported | 2026 | ✓ {C9} | Net-of-cost ORB ≈ 0 out of sample on index CFDs. |
| 22 | [Schaeffer's: 0DTE spreads](https://www.schaeffersresearch.com/content/bgs/2023/09/22/0dte-options-are-higher-spreads-imminent) | Schaeffer's, self-reported | 2023-09 | ✓ narrowed {C15} | One-day anecdote: 5.8% spread near the close. |
| 23 | [Volos: improving 0DTE returns](https://www.volossoftware.com/insights/improving-0dte-trading-returns) | vendor, self-reported | n.d. | quote ✓ | NDX expiry spreads in bps of spot. Not used for the cost model. |
| 24 | [CXO: Baglioni & Ribeiro](https://www.cxoadvisory.com/?p=43272) | CXO | 2021 | quote ✓ (verified in the prior run) | FOMC 13:50 → close reversal, +0.18% per event. |
| 25 | Harbourfront Quant summaries | Substack | 2024 | page thin; quote not found | Dropped; replaced by #18. |

## Screened and excluded
- **Third-party skills** (`security-scan.md`): mphinance `0dte-flow` (order-placement code, external secret store), majiayu000 `ib-0dte` (pointer page only) and senderic `0dte-trader` (private pipeline, no licence). None used.
- **Ni, Pearson & Poteshman (2005) pinning:** seen as a search snippet only; not used for any conclusion.
- **[macro-impact-archive](https://macro-impact-archive-1.pages.dev/cpi-release-dates-2026/):** 2026 CPI dates only. Superseded by the Concretum export.
- **Blocked or unreadable:**
  - bls.gov (403); sec.gov DERA PDF (403);
  - web.archive.org and stooq.com (connection reset); fred.stlouisfed.org (HTTP/2 error);
  - www1.villanova.edu (SSL); papers.ssrn.com (403);
  - PDFs at nber.org, nd.edu, lse.ac.uk and afajof.org (unparsed by the fetcher).
- **cfr-cologne.de 25-09** (Agarwal et al., retail options in India): downloaded but off-scope (non-US).
