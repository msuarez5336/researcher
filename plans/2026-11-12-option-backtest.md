# Plan: build the 1–6 month option backtest

As of 2026-11-12. Implements `research/2026-11-12-long-dated-option-setups/backtest-spec.md`
(called "the spec" below). Findings and their limits are in `report.md` in the same folder.

## Goal

A tool that answers, for one condition at a time: when the condition holds, does buying a 1–6
month call or put on that stock earn more than buying the same kind of option with no
condition, after realistic entry and exit prices, on data the condition was not tuned on?

Done means: the baseline and the first three conditions (A1, A3, B1 in the spec) have been run
on real option quotes, with a locked holdout period run exactly once, and a written result.

## Decisions needed from the owner

| # | Decision | Recommendation | Why |
|---|---|---|---|
| D1 | Where the code lives | A new repository | This repo's scripts are standard-library only; the backtest needs data libraries and will grow tests and data tooling of its own |
| D2 | Where the data lives and the tests run | Your own machine or a cloud storage bucket, not a cloud session | The vendor describes the history as roughly 500GB with a 14-day download window; a cloud session here has about 30GB free and is wiped when it ends |
| D3 | Buy option data now or after the prototype | After phase 1 | Phase 1 needs no purchase and proves the machinery; the purchase starts a 14-day download clock |
| D4 | Which stocks | Stocks passing an option-liquidity floor computed from the option data itself on each date | Avoids buying index-membership history and avoids picking today's survivors |
| D5 | Share-price source that includes delisted companies | Decide in phase 2 after pricing two vendors | The research could not retrieve these prices |

D1 and D2 block phase 2. Phase 1 can start in any location.

## Design

```
raw files ──> ingest ──> point-in-time store (Parquet, queried with DuckDB)
                              │
              ┌───────────────┼────────────────┐
           signals         pricing          contracts
        (one module     (real quotes,     (pick by target
        per condition)   or estimate)      delta and expiry)
              └───────────────┼────────────────┘
                          simulator ──> trade log ──> evaluation ──> result tables
```

- **Point-in-time store.** Every row carries the date it became public. Signals read through
  one function that takes an as-of date and cannot return later rows. This is the main defence
  against using information from the future.
- **Pricing interface.** One interface, two implementations: real quotes, and the estimate in
  spec section 3. The simulator does not know which it is using; every result is stamped with it.
- **Trade log.** One row per simulated trade: signal values, contract, entry and exit quotes,
  the fill assumption, outcome. All statistics are computed from the log, so a new statistic
  never needs a re-run.
- **Trial register.** Every run appends its condition, parameters and date to a file. The count
  of trials is an input to the significance test (spec section 6, step 5).
- **Stack.** Python, pandas, DuckDB over Parquet files, pytest. DuckDB is not installed in this
  environment; pandas is.

## Phases

### Phase 1: machinery on free data (no purchase)

| Step | Deliverable | Check that it works |
|---|---|---|
| 1.1 | Project skeleton, tests, trial register | Tests run |
| 1.2 | Share-price loader from a free source, for a fixed list of about 50 large stocks | Split-adjusted prices match a second source on spot dates |
| 1.3 | Point-in-time store and as-of reader | Test: changing any row dated after the as-of date leaves the output unchanged |
| 1.4 | Group B signals: B1 sharp fall, B2 and B3 past returns, B4 52-week distance | Hand-computed values for three stocks match |
| 1.5 | Estimated pricing (spec section 3) | Matches a textbook option price to the cent on known inputs |
| 1.6 | Contract selection and simulator with all fill assumptions and the three exit rules | A hand-worked trade reproduces exactly; a held-to-expiry trade pays intrinsic value |
| 1.7 | Evaluation: baseline grid, condition-versus-baseline tables, full distribution, overlap-adjusted t-statistic | A synthetic dataset with a planted effect is detected; one with no effect is not |

Output of phase 1 is working code. Its numbers are **not evidence**: the stock list is today's
survivors and the option prices are estimates with known blind spots (spec section 3).

### Phase 2: real data

| Step | Deliverable | Check that it works |
|---|---|---|
| 2.1 | Decide D1, D2, D5; buy the option history | — |
| 2.2 | Ingest option chains to Parquet, partitioned by date | Row counts per day are plausible; no day missing against the exchange calendar |
| 2.3 | Data quality report: crossed or zero quotes, missing implied volatility, coverage of expired contracts and delisted stocks | Report written; exclusions decided and recorded before any signal is run |
| 2.4 | Delisting-inclusive share prices and a stable company identifier joined to the option data | Every option row maps to a share price on its date |
| 2.5 | Free dated inputs: FINRA short interest with publication lag, EDGAR earnings and insider dates, FRED rate | As-of reader test from 1.3 passes on each |
| 2.6 | Liquidity-floor universe (D4) | Universe membership on a past date does not change when later data is added |

### Phase 3: calibrate and sanity-check

| Step | Deliverable | Check that it works |
|---|---|---|
| 3.1 | Estimated price versus real mid-quote, by maturity, strike distance and recent share return | Error table written. This fills a gap the research could not |
| 3.2 | Unconditional baseline on real quotes for the delta × maturity grid, at each fill assumption | Direction agrees with published figures where maturities overlap: far out-of-the-money calls lose most, and paying more of the spread lowers every cell (report, finding 2) |
| 3.3 | Lock the holdout: the final third of the history is moved out of reach of the default reader | A normal run cannot read holdout dates |

### Phase 4: test conditions on the development period

Order: A3 implied-volatility level, A1 implied volatility against own history, B1 sharp fall,
then B2–B4, A2, A4, A5. B5 and B6 (short interest, insider buying) come last and are labelled
untested ideas, since the research collected no evidence for them.

For each condition: condition-versus-baseline table per grid cell, full outcome distribution,
splits by year, by size group and by whether an earnings date fell in the holding period, and
the overlap-adjusted t-statistic. A condition passes to phase 5 only if it clears the bar set
in spec section 6 and is not confined to one period.

### Phase 5: holdout and write-up

- Fix the passing conditions and their parameters in writing.
- Run the holdout once. No parameter changes afterwards.
- Write the result: what passed, what failed, the trial count, and what the test cannot show.

## Risks

| Risk | Effect | Handling |
|---|---|---|
| Too few independent periods | A 3–6 month hold over about 19 years gives few non-overlapping samples, so real effects may not reach significance | Report it as "not detectable", not as "no effect"; weight the 30–120 day cells where samples are larger |
| Option data lacks delisted stocks | Results flatter than reality for buyers of puts, harsher or kinder for calls | Step 2.3 measures coverage; if poor, price a second vendor that states its delisted coverage |
| Snapshot is 14 minutes before the close | Entry at the next day's snapshot is not a tradable close price | Consistent use of the same snapshot for signal and fills; noted in results |
| No scheduled earnings dates in history | The earnings control uses actual dates, which were not all known in advance | Use it as a split, not as a trading signal |
| Overfitting through many variants | A passing condition is chance | Trial register, the raised t-statistic bar, single holdout run |
| Payoffs are mostly total losses with rare large wins | Means are unstable | Report medians and the share of total losses beside every mean |

## What is not in this plan

- Any recommendation to trade. The outcome is a measurement.
- Intraday data, weekly or same-day options, index options.
- Analyst-estimate signals: no reliable dated source was found.
- Live scanning for current setups. That is a separate tool, worth building only for
  conditions that pass phase 5.
