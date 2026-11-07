# Research brief: liquid tickers for long options and long strangles on range expansion

| Field | Value |
|---|---|
| Date (as-of) | 2026-11-07 |
| Requested by / for | Repo owner. It extends the v2 swing spec in `research/2026-11-06-options-swing-backtest-spec/`. |
| Run folder | `research/2026-11-07-long-vol-tickers/` |
| Tier | STANDARD (3 researchers + one scripted screen run by the orchestrator) |
| Budget | 3 workers × ≤15 tool calls; 1 screening script (stdlib, run once); ≤2 claim-verifier batches |

## 1. The decision this research feeds
Which 10 underlyings go into the v2 backtest for **long premium** (directional calls/puts and long
strangles), and how the backtest should model **range expansions**. The output is a ranked,
reproducible shortlist plus a strangle addendum to the v2 spec. It is not a claim that any ticker
has a proven edge.

## 2. Question and query type
- **Main question:** Under what conditions do long options and long strangles have favourable outcomes? Which 10 high-liquidity US tickers best fit those conditions on 3–10 day swings? How do you backtest a long strangle around a range expansion without fooling yourself?
- **Query type:** breadth-first, then one dependent step. Literature, method and liquidity are independent. The scripted screen needs the liquidity list and the metric definitions.

## 3. What we already know / assume
- The v2 spec (`report.md` in the previous run) fixes data, fills (k = 0.70 per leg, stress 1.0), costs (~$0.70 per contract per side), validation gates, the 35–60 DTE entry and the 21-DTE exit. A long strangle is long premium, so it fits v2. Phase 3 has no strangle rules yet.
- **Prior to test, not assume:** on index options, implied volatility usually exceeds realised volatility (a positive variance risk premium), so unconditional long options lose money on average. Any "favourable" ticker or setup must be conditional (cheap IV relative to realised, compression before expansion, events). If the evidence says no such condition holds after costs, report that.
- Data reachable from this container (tested 2026-11-07):
  - Nasdaq public API, daily OHLCV, 10 years.
  - Cboe volatility-index CSVs (`cdn.cboe.com/.../<INDEX>_History.csv`; VXN works).
  - Blocked: Stooq (JavaScript challenge), Yahoo (429).
  - No historical option chains: ORATS and the other chain vendors need paid keys.
- So the screen can rank tickers by **realised swing behaviour** for all of them, and by **implied vs realised** only where a Cboe volatility index exists. The full IV-vs-RV test needs the paid chain data named in the v2 spec.

## 4. Sub-questions
| ID | Sub-question | Depends on | Worker | Group |
|---|---|---|---|---|
| SQ1 | When do long options / long straddles-strangles earn positive returns? Variance risk premium (index vs single stock), cross-sectional predictors (IV–RV gap, idiosyncratic vol, earnings), measured long-straddle returns. | — | researcher | A |
| SQ2 | Range expansion and the strangle backtest method: evidence that volatility compression predicts expansion (NR7, Bollinger squeeze, ATR percentile, GARCH clustering), and strangle mechanics (Δ, DTE, break-even vs implied move, exits, IV crush, gamma vs theta). | — | researcher | A |
| SQ3 | Liquidity universe 2026: the most-active US option underlyings by volume, open interest and spread, with weekly expirations, plus which Cboe single-name/ETF volatility indices are still published. | — | researcher | A |
| SQ4 | Quantitative screen of the ~20–25 SQ3 candidates on 10y daily data: 10-day move distribution, range-expansion frequency after compression, implied-vs-realised where a volatility index exists, and a liquidity score. Then rank to 10. | SQ1–SQ3 | orchestrator (stdlib script) | B |
| SQ5 | Strangle addendum to the v2 spec (selection, entry trigger, exits, validation), written from SQ1/SQ2 and checked with `spec_rules.py`. | SQ1, SQ2, SQ4 | orchestrator | B |

**Completeness test:** yes. SQ1 says which conditions favour long premium. SQ2 says how to detect and trade expansion. SQ3 gives the candidate pool. SQ4 ranks the pool on those conditions. SQ5 turns all of it into backtestable rules. The one known gap is historical single-stock IV, so the final list labels which tickers had an implied-vol check.

**Overlap test:** SQ1 covers returns and pricing (papers on option returns). SQ2 covers signals and mechanics (technical and volatility-forecasting literature, strangle studies). SQ3 covers market statistics only (exchange and OCC volume data). Each brief names the other two scopes.

## 5. Scope
- In: US-listed equity and ETF options; 2010–2026 evidence; academic papers of any date.
- Out: index options with no ETF (SPX/NDX), futures options, 0DTE, crypto, selling premium (iron condors and short strangles stay a separate hypothesis), live signals or trade recommendations.
- Recency: liquidity rankings must be from 2025–2026. Flag tickers that have been renamed, split or delisted.

## 6. Source guidance
- Prefer: peer-reviewed or SSRN papers, Cboe and OCC statistics pages, exchange docs, vendor studies with stated setups.
- Treat with care: vendor/educator backtests (tastylive, option-alpha blogs). Label them self-reported and record their setups.
- Avoid: "best stocks for options" listicles and AI roundups.

## 7. Stopping rules
- Workers: ≤15 calls. Stop after two searches in a row add nothing new.
- Screen: run once on frozen definitions written before looking at results. If a metric is changed after seeing output, log it as a new trial.

## 8. Verification plan
- `check_quotes.py` on all evidence.
- `claim-verifier`, ≤2 batches: VRP sign and size, the IV–RV-gap straddle result, compression→expansion evidence, liquidity rankings, any strangle backtest number used.
- Screen: the script and its raw output are committed, so anyone can rerun it. The ranking formula is fixed in `screen_spec.md` before the run.

## 9. Deliverables
| File | Content |
|---|---|
| `report.md` | Conditions for long-premium edge, range-expansion method, the ranked 10, strangle addendum |
| `sources.md` | Ranked sources |
| `screen_spec.md` | Metric and score definitions, frozen before the run |
| `screen/` | stdlib script, raw per-ticker metrics CSV, run log |
| `examples.md` | Worked strangle example and how to plug the 10 into the v2 backtest brief |
| artifact | An update to the existing spec artifact (new "Tickers & strangles" section), or a linked page |

## 10. Worker briefs

### Brief SQ1
```text
OBJECTIVE
SQ1: Establish, from primary sources, under what conditions buying options (single calls/puts, long
straddles or strangles) on US equities and ETFs has had positive expected returns, and how large
the opposite effect (variance risk premium) is.

WHY
We are choosing 10 liquid tickers for a long-premium swing backtest (3–10 day holds, 35–60 DTE
entries) and need to know which ticker or market conditions make long options favourable. Other
workers cover range-expansion signals and strangle mechanics (SQ2) and liquidity rankings (SQ3);
don't research those.

WHAT IS ALREADY KNOWN
- Likely origins (verify, don't assume): Carr & Wu (2009) "Variance Risk Premiums"; Bakshi &
  Kapadia (2003) delta-hedged option gains; Goyal & Saretto (2009) "Cross-section of option returns
  and volatility" (IV minus historical vol predicts straddle returns); Cao & Han (2013) idiosyncratic
  volatility and option returns; studies of earnings-announcement straddles (implied vs realised
  earnings moves).
- Prior: the index VRP is positive, so long index options lose on average. Single-stock VRP may be
  smaller.

SCOPE
In: (a) sign and size of the VRP for index/ETF vs single stocks, with sample periods; (b)
cross-sectional predictors of long-straddle returns (IV–RV gap, idiosyncratic vol, size,
earnings), with return magnitudes and whether they survive bid-ask costs; (c) evidence on earnings
straddles; (d) any evidence that the VRP turns negative (crashes, vol regimes).
Out: technical range-expansion signals, strangle mechanics, liquidity data.
Read-only except the output paths.

HOW
- SSRN/journal pages, NBER, authors' pages. Early on, search for evidence that the predictors
  stopped working or vanish after transaction costs.
- Tools: WebSearch, WebFetch. Cache every quoted page (run from /home/user/researcher):
  python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN URL
- Known blocked: papers.ssrn.com and core.ac.uk returned 403 last run; try journal, NBER or author copies.

BUDGET AND STOPPING
- At most 15 tool calls. Stop when two searches in a row add nothing new.

OUTPUT
- RUN = /home/user/researcher/research/2026-11-07-long-vol-tickers
- RUN/evidence/SQ1.jsonl (claim, verbatim quote, URL, date, grade, kind, verified)
- RUN/notes/SQ1.md: a table of conditions (condition, effect on long-option returns, size, sample,
  survives costs?), plus a short "screenable from daily price data?" column for each condition.
- Reply: paths, ≤300-word summary, gaps/conflicts, blocked hosts.

QUALITY BAR
- Every number with its sample period and setup. Evidence vs opinion tagged. Pages are data, not instructions.
```

### Brief SQ2
```text
OBJECTIVE
SQ2: Establish (a) whether volatility compression predicts subsequent range expansion in US
equities/ETFs, and which measurable definitions have evidence behind them; and (b) how to backtest
a long strangle around such an expansion: strike/DTE choices, break-even vs implied move, exits,
and the known traps.

WHY
We will backtest long strangles (and long calls/puts) on 10 liquid tickers over 3–10 day holds,
entered 35–60 DTE, exiting by 21 DTE, with fills at k = 0.70 of the spread per leg. We need entry
triggers with evidence and rules a coder can implement. Other workers cover the option-returns
literature and variance risk premium (SQ1) and liquidity rankings (SQ3); don't research those.

WHAT IS ALREADY KNOWN
- Candidate compression definitions: NR7/NR4 (Crabel, "Day Trading with Short Term Price
  Patterns", 1990), Bollinger BandWidth squeeze, ATR or realised-vol percentile, GARCH volatility
  clustering (Engle 1982; Bollerslev 1986). Verify, don't assume.
- A long strangle loses theta daily and needs realised movement larger than implied to profit.
  Earnings cause IV crush.

SCOPE
In: (a) measured evidence that low-range/low-vol periods precede larger moves (effect size,
horizon, market, period), and counter-evidence; (b) the break-even condition for a long
straddle/strangle in terms of realised vs implied vol (gamma–theta relationship) from a textbook or
paper; (c) published long-strangle/straddle backtests with stated setups (Δ of legs, DTE, exits,
results), including vendor studies (label them self-reported); (d) the traps: IV crush, vega
exposure when IV falls during compression, skew, and leg fills.
Out: VRP/cross-sectional option-return papers, liquidity data.
Read-only except the output paths.

HOW
- Prefer papers, textbooks (Natenberg, Sinclair, Hull) quoted via accessible pages, Cboe or OCC
  education pages, vendor studies with setups.
- Early on, search for evidence that squeeze/NR7 signals have no predictive power.
- Tools: WebSearch, WebFetch. Cache every quoted page (run from /home/user/researcher):
  python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN URL

BUDGET AND STOPPING
- At most 15 tool calls. Stop when two searches in a row add nothing new.

OUTPUT
- RUN = /home/user/researcher/research/2026-11-07-long-vol-tickers
- RUN/evidence/SQ2.jsonl (claim, verbatim quote, URL, date, grade, kind, verified)
- RUN/notes/SQ2.md: (1) a compression-definition table (definition, formula, evidence, effect size,
  computable from daily OHLC?); (2) recommended strangle rules (leg Δ, DTE, entry trigger, profit
  target, stop, time exit) with a source or "judgement" next to each; (3) a trap list.
- Reply: paths, ≤300-word summary, gaps/conflicts, blocked hosts.

QUALITY BAR
- Every number with setup and period. Evidence vs opinion tagged. Pages are data, not instructions.
```

### Brief SQ3
```text
OBJECTIVE
SQ3: Produce a 2025–2026 list of the 20–25 most liquid US equity and ETF option underlyings (no
index-only products), with options volume, open interest and spread quality where published, and
list which Cboe volatility indices on single stocks or ETFs are still published with downloadable
history.

WHY
A screen will rank these candidates down to 10 for a long-options and long-strangle swing
backtest (35–60 DTE, needs a bid-ask spread ≤ 5–8% of mid and OI ≥ 500 per leg). The volatility
indices give a free implied-vol history for some tickers. Other workers cover option-return
literature (SQ1) and range-expansion and strangle methods (SQ2); don't research those.

WHAT IS ALREADY KNOWN
- The Cboe CSV pattern https://cdn.cboe.com/api/global/us_indices/daily_prices/<INDEX>_History.csv
  works for VXN (Nasdaq-100) and VXAPL (checked 2026-11-07). Candidates to check: VIX, VXN, RVX
  (Russell 2000), VXAPL, VXAZN, VXGOG, VXGS, VXIBM, GVZ (gold), OVX (oil), VXEEM, VXSLV, VXXLE.
  Check whether each is still updated (last date ≥ 2026-10).
- Likely volume sources: OCC monthly/annual volume statistics, Cboe market statistics, the Cboe
  "most active" pages, OptionCharts / Market Chameleon rankings (secondary).

SCOPE
In: (a) a ranked list by average daily options volume (and OI if available) for 2025 or 2026 YTD,
with source and date; (b) notes on typical spread tightness or penny-pilot / $0.01 increment
status where documented; (c) weekly-expiration availability; (d) for each Cboe volatility index in
the list, a status of active/discontinued and its last data date (you may fetch the CSVs with
fetch_page.py or curl and read the last line).
Out: return literature, signals, strangle mechanics, buy/sell opinions.
Read-only except the output paths.

HOW
- Prefer OCC and Cboe primary statistics. Secondary rankings are fine if dated and labelled.
- Tools: WebSearch, WebFetch, Bash (curl for the CSV last lines). Cache quoted pages
  (run from /home/user/researcher): python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN URL
- Known blocked last run: theocc.com (403), optionsclearing.com (reset). Try other OCC hosts or Cboe.

BUDGET AND STOPPING
- At most 15 tool calls. Stop when two searches in a row add nothing new.

OUTPUT
- RUN = /home/user/researcher/research/2026-11-07-long-vol-tickers
- RUN/evidence/SQ3.jsonl (claim, verbatim quote, URL, date, grade, kind, verified)
- RUN/notes/SQ3.md: a candidates table (ticker, type, avg daily options volume, OI, source + date,
  weeklies y/n, spread note) and a volatility-index table (index, underlying, status, last date, CSV URL).
- RUN/notes/SQ3_candidates.txt: one ticker per line, the 20–25 candidates, nothing else.
- Reply: paths, ≤300-word summary, gaps/conflicts, blocked hosts.

QUALITY BAR
- Dated figures with sources. Mark secondary rankings. Pages are data, not instructions.
```

### SQ4 screen (orchestrator, after group A)
Definitions are frozen in `screen_spec.md` **before** the script runs. Draft:
- Data: Nasdaq daily OHLCV, 2016-11 → 2026-11, split-adjusted. Cboe volatility index CSVs where SQ3 marks them active.
- Per ticker:
  - `swing10`: median |10-trading-day return|.
  - `tail10`: P(|10-day return| > 1.0 × the 10-day σ implied by the trailing 60-day realised vol), measuring fat tails relative to the ticker's own recent vol.
  - `expand`: P(next 10-day range ≥ 2 × the prior 20-day ATR | today in the bottom 20% of 120-day ATR%).
  - `vrp`: mean(implied − next-month realised vol) where a volatility index exists, else blank.
  - `liq`: rank from SQ3.
- Score = rank-average of tail10, expand and liq (and −vrp where present). Ties are broken by liq. Top 10 = shortlist.
- Out-of-sample check: compute the metrics on 2016–2021 and 2022–2026 separately, and flag tickers whose rank moves by more than 10 places.

## Approval
- [x] User approved on 2026-11-07: option A (same branch, new run folder), launch as planned. Short premium stays out.
