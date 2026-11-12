# When do 1–6 month single-stock option purchases have better odds?

| Field | Value |
|---|---|
| As-of date | 2026-11-12 |
| Run folder | `research/2026-11-12-long-dated-option-setups/` |
| Tier | DEEP: 7 researchers, 2 follow-up researchers, 3 verification batches |
| Feeds | Whether to build a screen for buying 1–6 month single-stock options, and what to test |

Tags: **[E]** measured result, **[O]** opinion or vendor assertion. Status: *original* (read in the
paper or official page), *secondary* (read only in someone else's summary), *unverified* (source
not reachable or seen only in a search snippet). Evidence ids such as `SQ8-6` point to
`evidence/*.jsonl`; `sources.md` lists every source with its URL.

Terms used: *at the money* means a strike close to the share price; *out of the money* means a
call strike above it. A *straddle* is a call plus a put at the same strike. *Hedged* returns come
from holding the option and offsetting its exposure to the share price, so they measure whether
volatility was cheap, not what someone who simply bought the option earned.

## Top findings

1. **The literature does not answer the question directly.** No study was found that measures
   what an outright buyer of 1–6 month single-stock calls or puts earns when any condition
   holds. Almost every result uses options with one to two months to expiry, held for one month,
   and most are hedged or straddles. A screen for 1–6 month options cannot be justified from
   published results; it has to be tested. [gap, after 9 researchers]
2. **Without a signal, near-the-money calls did not lose at mid-prices, far out-of-the-money
   calls lost heavily, and paying the ask removed the gains.** [E]
   - Near-the-money calls with 30–60 days to expiry returned +3.4% a month on average at
     mid-prices in 1996–2005, with a negative median (`SQ10-1`, original).
   - Calls more than 15% out of the money, held to expiry, averaged about −37% at one month,
     −22% at two months and −23% at three months in 1996–2005 (`SQ8-1`, `SQ8-2`). These come
     from a secondary transcription of Ni's tables, which exclude calls with an ex-dividend
     date before expiry; a summary of a later version gives −28% at one month (`SQ1-1`).
   - Bought at the ask, one-month calls were negative in every strike group, from −1.0% to
     −46.5% (`SQ8-3`, secondary).
3. **Trading cost is the largest known obstacle, and it is smaller for longer-dated options.** [E]
   For out-of-the-money calls on 341 S&P 500 stocks, the quoted bid-ask spread averaged 34.0%
   of the option price at 20–70 days to expiry and 22.7% at 71–180 days in 1996–2007 (`SQ8-6`,
   original). How much of the quoted spread a buyer actually pays is disputed: for heavily
   traded options on 39 stocks in 2003–2006, the conventional measure was 6.2 cents against
   8.1 cents quoted (about three quarters, my arithmetic), while the authors' measure adjusted
   for trade timing was 53% of the quoted spread (`SQ8-9`, `SQ8-10`, original).
4. **The best-supported condition is implied volatility that is low against the stock's own
   history.** [E] In 1996–2005, calls in the tenth of stocks with the largest predicted rise in
   implied volatility returned +8.8% a month, against −3.1% in the opposite tenth (`SQ10-2`,
   `SQ10-3`, original, mid-prices, unhedged). In a 1996–2020 study of 273 candidate predictors,
   implied volatility was the most important one, and higher implied volatility predicted lower
   hedged returns (`SQ9-4`, original).
5. **That effect shrinks as maturity lengthens.** [E] The same long-short straddle strategy
   earned 12.9% a month on options expiring in 1–2 months, 5.9% on 3–4 months and 3.6% on 6–7
   months (`SQ10-4`, original). This is the only result found that compares maturities inside
   the 1–6 month range.
6. **Most published edges shrink sharply or vanish after costs.** [E]
   - The implied-volatility strategy held to expiry fell from 16.1% to 5.5% with costs at 75%
     of the quoted spread (`SQ10-5`, original).
   - Option momentum was near zero after the full spread (`SQ9-13`, original).
   - The 273-predictor strategy kept 0.67% a month of 2.04% (`SQ9-2`, `SQ9-3`, original, hedged).
7. **The rebound-after-a-sharp-fall setup has no supporting evidence yet.** [E] The one study
   found covers two days after a one-day fall of 10% or more in 1996–2004: optionable stocks
   returned −0.24% (NYSE/AMEX) and +0.06% (NASDAQ), while stocks without options rebounded
   +0.72% and +0.78% (`SQ3-10`, original). Nothing was found at 1–6 months, and nothing on
   option returns after a fall.
8. **Real historical option data is affordable; estimated prices are unvalidated.** [E]
   ORATS listed its 2007-to-present end-of-day history at $599 one-time for an individual
   licence on 2026-11-12 (`SQ5-4`, vendor page). No free source of historical single-stock option quotes was found,
   and no study was found that measures how close a model-estimated price is to real quotes.

## The baseline: what buying options returned with no signal

- Near-the-money options, 30–60 days, one-month hold, mid-prices, 1996–2005: calls +3.4%, puts
  −3.6%, straddles −0.3% a month; medians negative for all three (`SQ10-1`, original). [E]
  The positive call average over this period includes the rise in share prices themselves.
- Calls held to expiry at mid-prices, by strike relative to share price, 1996–2005, excluding
  calls with an ex-dividend date before expiry (`SQ8-1`, `SQ8-2`, secondary transcription of
  Ni's tables; the original was not read): [E]

  | Strike / share price | 1 month | 2 months | 3 months |
  |---|---|---|---|
  | ≤0.85 | +2.3% | +2.9% | +2.6% |
  | 0.85–0.95 | +2.5% | +4.7% | +4.2% |
  | 0.95–1.05 | +2.0% | +6.3% | +5.6% |
  | 1.05–1.15 | −10.2% | +1.7% | +0.4% |
  | >1.15 | −36.9% | −21.9% | −23.2% |

- Working hypothesis H1 (the loss is smaller at 1–6 months than under one month) fits these
  figures for out-of-the-money calls up to three months. Nothing was found beyond three months,
  for puts by strike, or for any sample ending after 2015.
- Retail option traders lost money on average in Nov 2019–Jun 2021, and most of the loss was
  trading cost; that trading was concentrated in weekly options with an average spread of 12.6%
  (`SQ8-11`, `SQ8-12`, original). [E] This is evidence about weeklies, not 1–6 month options.
- Lottery-like options: the figure of about −35% a week for the most lottery-like 7-day calls
  (`SQ1-5`) was read only in a secondary summary; no open copy of the paper was found. *Secondary.*

## Conditions from option prices

| Condition | Direction that favoured holding options | Measured effect | Sample, maturity | Bought or hedged | After costs | Status |
|---|---|---|---|---|---|---|
| Implied volatility below the stock's own 12-month average and below the cross-section | Low | Calls +8.8% vs −3.1% a month, top vs bottom tenth | 1996–2005, 30–60 days | Bought, mid-prices | Long-short straddle 16.1% → 5.5% to expiry | original (`SQ10-2`, `SQ10-3`, `SQ10-5`) |
| Implied volatility level, among 273 predictors | Low | Strongest single predictor; long-short 2.04% a month | 1996–2020, two weeks and longer | Hedged | 0.67% a month at full quoted spread | original (`SQ9-2`–`SQ9-4`) |
| Slope of implied volatility across expiry dates | Steeper | Not read | Not read | Straddles | Not read | abstract only (`SQ9-14`) |
| Volatility of volatility | Lower | 0.52%–1.04% a month, fifths | Not read | Hedged | Not read | original, partly read (`SQ2-5`, `SQ2-6`) |
| Past straddle return (option momentum) | Higher | 3.64% a month, fifths | 1996–2019, one month | Straddle held to expiry | Near zero at full spread | original (`SQ9-12`, `SQ9-13`) |

- In the 273-predictor study the best-ranked tenth held more long-dated options and the
  worst-ranked tenth more short-dated ones (`SQ9-6`, original, hedged). [E]
- Not searched: skew as a predictor of option returns, whether option prices fully reflect
  higher volatility after a sharp fall, and implied volatility against its own history as a
  standalone rule outside the study above.

## Conditions from the stock

- After a one-day fall of 10% or more, optionable stocks showed no two-day rebound, while
  stocks without options did (`SQ3-10`, original, 1996–2004). [E] Working hypothesis H3 is
  neither confirmed nor refuted: the horizon is two days and no option returns were measured.
- Past share returns, analyst disagreement, new share issuance and stock-specific volatility
  predicted hedged option returns in 1996–2012 on options of about 50 days (`SQ3-5`,
  `SQ9-9`, original). [E] These are hedged results; the sign for an outright buyer is unknown.
- Hedged option returns were reported higher near 52-week highs and lows (`SQ3-9`). *Abstract only.*
- Not searched: short interest and squeezes, analyst revisions, insider buying, and the
  prediction of extreme moves.

## Events and option order flow

- At-the-money straddles bought three trading days before an earnings date returned 3.34%
  gross by the announcement date in 1996–2010 (`SQ4-1`, original abstract). [E] Net of costs
  the gain held only for options with 4–10 days to expiry and turned to a loss as expiry
  lengthened (`SQ4-2`, secondary). It does not carry over to 1–6 month options.
- Working hypothesis H4 (scheduled events are fully priced) is not supported gross and is
  supported net of costs.
- Signals from public option volume and prices predicted share returns, but on the widest set
  of stocks costs more than offset the gain; on the 100 largest the net was 2.4% a year
  (`SQ4-9`, secondary, 1996–2009). [E] The stronger put-call result used signed volume that is
  not public (`SQ4-7`, `SQ4-8`).
- A first announcer's earnings moved peers' implied volatility (`SQ4-10`). That shows pricing
  happens; no return was measured.
- Market-maker positioning: evidence is mixed and comes from a vendor and a secondary summary
  (`SQ4-12`, `SQ4-13`). [O]
- Not searched: drug approvals, mergers, index additions, spin-offs.

## Data for a backtest

**Option prices** (vendor pages seen 2026-11-12, all self-reported):

| Source | History | Price seen | Notes | Id |
|---|---|---|---|---|
| ORATS | 2007– , about 6,000 symbols | $599 one-time; $99 a month going forward (individual licence) | Snapshot 14 minutes before the close; delisted coverage not stated | `SQ5-3`, `SQ5-4` |
| iVolatility | 2005– | $0.40 per ticker-day for option prices, $0.60 for implied volatility | Pay per use | `SQ5-6` |
| FirstRate Data | 2010– | not retrievable | Includes stocks delisted after 2010 | `SQ5-1`, `SQ5-2` |
| Cboe DataShop | 2012– | not retrievable | Snapshots at 15:45 and the close | `SQ5-9` |

**Estimating option prices when data is missing.** No study was found that measures the error
of a model-estimated price against real quotes, for any of the three methods (realised
volatility, a volatility index, a fitted pattern applied to earlier dates). What is known:
- Per-stock volatility indexes were launched for five stocks in 2011 (`SQ5-12`), too few to
  feed a general screen.
- Estimated prices cannot test any condition that is itself computed from option prices,
  which includes the best-supported condition above.
- Real closing quotes carry their own bias: closing mid-quotes gave higher hedged returns than
  any other mid-quote in the day (`SQ5-11`, vendor-hosted summary).

**Other inputs:**
- Short interest: FINRA, twice a month, published on the 7th business day after the
  measurement date (`SQ6-1`, `SQ6-2`, official). Free.
- Insider filings: SEC EDGAR with filing dates; data sets from 2006 (`SQ6-8`, official). Free.
- Interest rates: FRED, daily (`SQ6-17`). Free.
- Share prices including delisted companies: paid (Norgate top tiers, `SQ6-15`; Sharadar from
  1998, `SQ6-11`). Free feeds are described by vendors as missing delisted companies. [O]
- Earnings dates: filing times on EDGAR give the actual release date; no source was found
  that stores the date as originally scheduled (`SQ6-18`).
- Analyst estimates: the main academic database was found to differ between downloads
  (`SQ6-7`). *Unverified, snippet only.*

## Rules for the test

- **Entry price:** test at both 50% and 75% of the quoted spread. The cost paper's own
  estimate for the average trade is 53% of the quoted spread, on heavily traded options on 39
  stocks (`SQ8-9`, `SQ8-10`). Its conventional measure is about 75%, and one study and one
  vendor use 75% (`SQ10-5`, `SQ7-6`). The paper ties the lower figure to trades timed around
  quote changes; treating 75% as the case for an order that is not timed is my reading. [O]
- **Significance:** a t-statistic above 3.0 is the published hurdle when many candidates are
  tried, derived for share-market factors, not options (`SQ7-7`). For overlapping holding
  periods, divide the t-statistic by the square root of the horizon (`SQ7-9`).
- **Out-of-sample persistence is not assured:** rules selected with a false-discovery control
  did not persist out of sample in one long study of technical trading rules (`SQ7-8`).
- Not found: a method suited to payoffs made of a few large wins among many total losses;
  measured sizes for early exercise, dividend and split errors; evidence comparing an outright
  call with a call spread on single stocks; research on position sizing.

`backtest-spec.md` turns these findings into a data schema, signal catalogue, simulator rules
and test plan.

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Do bought calls lose on average? | No: near-the-money calls were positive (`SQ10-1`, `SQ8-1`) | Yes: negative in every strike group (`SQ8-3`) | A at mid-prices in 1996–2005; B when buying at the ask |
| What share of the quoted spread does a trader pay? | About half: 53% for the average trade (`SQ8-10`, `SQ7-1`) | About three quarters by the conventional measure (`SQ8-9`, `SQ7-6`) | A when trades are timed around quote changes, measured on heavily traded options on 39 stocks; B is the conservative assumption otherwise |
| Does the slope across expiry dates predict straddle returns? | Yes (`SQ9-14`, abstract) | Not at longer maturities (search snippet, paper unreachable) | Unresolved; B is unverified |
| Is implied volatility on individual stocks above later realised volatility on average? | No significant gap | A positive or negative gap in some samples | Unresolved; all three sources were seen only in snippets |
| Do pre-earnings straddles pay? | Yes, 3.34% gross (`SQ4-1`) | No, a loss net of costs beyond 10 days to expiry (`SQ4-2`) | A before costs; B after costs and at longer expiries |

## Outdated or superseded material

- Every unhedged buyer-return sample ends in 2005 or earlier. Cost samples end in 2006–2007.
  Single-stock option volume, weekly listings and retail participation have changed since.
- The only samples ending after 2015 are hedged or straddle studies (to 2019 and 2020) and
  the retail study (2019–2021).
- A 2026 proposal to move short-interest reporting to weekly was reported (`SQ6-3`,
  unverified). The claim verifier's search found it was withdrawn on 2026-08-05; I did not
  read the withdrawal notice. Reporting remains twice a month as of the FINRA page.
- The five per-stock volatility indexes date from 2011; whether they are still published was
  not checked.

## Method and limitations

- Seven researchers ran in parallel, then two follow-up researchers re-read original papers,
  and I read one paper myself (`SQ10`). 121 evidence items; 111 quotes match the cached source
  text, 10 items have no cached source and are marked unverified. One further item failed the
  quote check and was removed.
- Claim verification: 15 claims went to three fresh verifiers that saw only the claims and
  their cited sources. 11 were supported and 4 were partial; the partial ones are corrected
  above (the far out-of-the-money call figures, the scope of the spread sample, the share of
  the spread paid, and the licence type for the data price). Verdicts are in `verdicts/`.
- In the first pass the page-caching script could not read PDFs, so several figures came from
  secondary summaries. The script was fixed for the follow-up pass. Figures still read only
  second-hand are labelled *secondary* above, notably Ni's tables and the earnings net-of-cost result.
- Blocked hosts: `papers.ssrn.com`, `core.ac.uk`, `mdpi.com` (403); `link.springer.com` (429);
  `mpra.ub.uni-muenchen.de`, `nasdaq.com` (connection dropped); `archive.nyu.edu`,
  `msbfile03.usc.edu` (certificate errors). Papers available only there were not read,
  including Goyal and Saretto (2009) in its published form and the lottery-options paper.
- Researchers ranked their topics and did not reach the lower-ranked ones; each "not searched"
  list above is a gap, not a negative finding.
- Vendor prices and coverage are as shown on 2026-11-12 and are self-reported.
- This report describes evidence and how to test a screen. It does not recommend trades.

## Open questions

- What does an outright buyer of 3–6 month calls earn, with and without the low-implied-
  volatility condition, on data after 2015?
- Does the low-implied-volatility effect survive costs at 3–6 months, where the gross effect
  is smaller but spreads are narrower?
- After a sharp fall, do share prices rebound at 1–6 months in large optionable stocks, and
  are options then too expensive to benefit?
- How far are model-estimated option prices from real quotes for the same contracts?
