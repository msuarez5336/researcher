# SQ2 notes (as of 2026-11-07). Budget: 15 calls used. Thin: most intraday effect sizes NOT found.

## Answer
Best evidence says 0DTE/dealer gamma dampens intraday vol on average (effect fades within ~1h) rather than amplifying it; amplification is conditional (large one-sided or rolled-over positioning). For FOMC, the only measured intraday result found is Narain (IJCB 2026): Powell-era press conferences carry >3x the volatility of Bernanke/Yellen ones and tend to reverse the statement move. No systematic intraday CPI/NFP/10:00 effect sizes were found.

## 1. Event windows
- FOMC 14:00 statement -> 14:30 presser: mechanism = presser carries independent policy news (FRBSF wp2025-30, search snippet only, unverified). Evidence [E] SQ2-7, SQ2-8 (Narain 2026, Powell era, post-COVID reversal). Baglioni-Ribeiro [E] SQ2-6: 13:50-to-close fade of prior 24h return, +0.18%/event, 180 events 1997-2020. Anecdotes (Dec 2022, Mar 2025 faded statement gains) from media, not recorded as evidence. Sample size/exact effect sizes in Narain not extracted.
- CPI/NFP 08:30: only anecdotal implied-move figures (Citi ~1% S&P implied for Jan 2025 CPI; Risk.net 0DTE volume spikes on CPI days since late 2022). Realized vs implied intraday: NOT found systematically. [O]
- 10:00 data (ISM/JOLTS): nothing found.
- OpEx: Ni-Pearson-Poteshman 2005 [E, unverified, snippet] strike clustering on expiry; no 0DTE-era OpEx pinning measurement found.

## 2. Pinning vs amplification
| Finding | Conditions | Ids |
|---|---|---|
| Dampening / mean-reversion | Positive dealer net gamma (market makers net long gamma through 0DTE day); effect dissipates ~1h; E-mini flow reverses | SQ2-1,2,3 |
| No aggregate effect | Balanced institutional/retail 0DTE flow; Cboe self-reported, close-to-close minus intraday vol spread 2.7 pts = 10y avg | SQ2-4,5 |
| Pinning at strikes | Large OI, dealers net long options (single stocks, pre-0DTE) | SQ2-11 |
| Amplification | Not shown unconditionally; dealers short gamma or one-sided flow is the hypothesised case. Princeton 2026 senior thesis (search snippet only, not fetched) says others find positive 0DTE-volatility association but hedging-feedback not the main mechanism | none verified |

## 3. Release-date source
- Official BLS (cpi.htm, bls.ics, archived_sched.htm): curl 403 Access Denied (bot policy).
- https://macro-impact-archive-1.pages.dev/cpi-release-dates-2026/ : HTML table, 2026 CPI only, loads (200, cached). Third party. SQ2-10.
- https://concretumgroup.com/a-macro-event-calendar-for-research-and-backtests/ : free CSV generator (CPI, NFP, FOMC, since 1927). Page loads (200); actual CSV not tested, may need interactive JS. Dates are scheduled dates, verify times.
- https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm : 200, FOMC dates cached.
- datasets/cpi-us on GitHub loads but is CPI values, not release dates.
- Apify actors exist (paid/hosted). No GitHub CSV of 2022-26 release dates found. Consider deriving from BLS monthly sched pages via another route or the Concretum CSV.

## 4. Counter-evidence
Cboe and Dim et al. argue against amplification; Cboe is a venue with an interest in 0DTE (self-reported). June 2026 vol-desk recap (blog, unverified) claims CPI-day implied ±1.8-2.2% vs ±0.6-1.0% normal day; not recorded.

## Conflicts
Dampening (average, within-day) vs Princeton thesis/other papers citing positive 0DTE-vol association; Narain reversal (Powell era) vs Bernanke/Yellen reinforcement; Jubinski & Tomljanovich 2017 single stocks: returns unresponsive to FOMC but conditional vol rises (snippet).

## Not found
Intraday 30-min absolute return CPI vs normal days; share of range in first 15 min after 14:00; 10:00 releases; 0DTE-era OpEx pinning; Andersen et al. and Lucca-Moench intraday figures (not searched directly).

## Blocked
bls.gov (403 for page, ics, archived schedule). Not opened: papers.ssrn.com.

## Search log
1 0DTE gamma volatility amplify (search, 6+ sources); 2 FOMC intraday reversal (search, mostly media); 3 curl x4 date sources; 4 fetch_page x4 (Cboe, Harbourfront, Quantpedia, CXO); 5 BLS dates search (found macro-impact page); 6 fetch macro-impact; 7 Fed press conference papers (disconfirm-ish; found Narain); 8 CPI intraday implied vs realized (anecdotal); 9 fetch IJCB + Fed calendar; 10 dates dataset search (Concretum); 11 fetch Concretum; 12 Ni-Pearson-Poteshman search.
