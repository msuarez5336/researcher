# SQ4 notes (as of 2026-11-07). All vendor facts are self-reported.

## Answer
Four vendors sell historical intraday option NBBO that covers 2022-2026 at minute granularity: Cboe DataShop (1-min NBBO from Jan 2012, IV/Greeks add-on), ORATS (1-min from Aug 2020, built-in IV/Greeks), ThetaData (1-min on Value/Standard, tick on Pro) and Databento (cbbo-1m, pay per GB). No free source with intraday option quotes was found. The cheapest listed price found is Massive Options Advanced at USD 199/mo, but its quote-history depth is not stated (Plan History table starts 2022-03-07) and it has no historical IV/Greeks. ORATS at USD 1,500 one-time plus USD 199/mo is the cheapest with vendor IV/Greeks.

## (1) Vendor table
| Vendor | Quote type | Granularity | Start | 0DTE/expired | IV/Greeks | Price/plan (listed) | Format | Caveats | Ev |
|---|---|---|---|---|---|---|---|---|---|
| ORATS 1-minute | NBBO bid/ask+sizes (field names say NBBO) | 1 min snapshots, all strikes | Aug 2020 | chain by tradeDate+ticker, expired included by date query; 0DTE not checked | yes: bid/mid/ask IV, delta..rho, SMV | individual USD 199/mo recurring; USD 1,500 one-time backfill; S3 fees extra (page says USD 1-2k); pro priced separately | API CSV/JSON, S3 | underlying price is option-implied (put-call parity), not real stock price; same-day history only to last 15 min | 1-3 |
| Databento OPRA | consolidated last sale + NBBO (cbbo/tcbbo/mbp-1) | cbbo-1m before 2023-03-28; cbbo-1s, cmbp-1, tcbbo after | 2013 | listed with definitions; 0DTE not checked | none listed | usage from USD 0.04/GB (which schema costs more: not stated on page); subscription plans not read | DBN/CSV, API | pre-2023-03-28 data is subsampled; no Greeks, compute yourself | 4-6 |
| Massive (ex-Polygon) | quotes | tick | records back to 2022-03-07 | not checked | no historical (known from brief) | Options Advanced USD 199/mo (Developer USD 79 lacks quotes) | REST, flat files | quote-history depth for Advanced "All history" but table starts 2022-03-07 | 13-14 |
| ThetaData | every OPRA NBBO | Value/Standard 1 min, Pro tick | tiers: Value 2021-01-01, Standard 2016-01-01, Pro 2012-06 | docs warn 0DTE far strikes not quoted late in day | yes (Greeks endpoints; IV) | plan prices NOT on cached pages (search snippet: Value USD 40/mo, unverified) | REST via local terminal | Value tier is 15-min delayed live; free = 1y EOD only | 7-9 |
| Cboe DataShop Option Quote Intervals | NBBO + size, OHLCV | 1,5,10,15,20,30,60,390,405 min | Jan 2012 | expired contracts: not stated | add-on purchase | price not stated on page (order form only) | files | SPX underlying needs CGIF licence from USD 1000/mo; early-close caveat for 390-min | 10-12 |
| FirstRate Data | bid/ask, EOD only | EOD | Jan 2010 | n/a | greeks, IV | not read | files | no intraday options | 15 |
| IVolatility, AlgoSeek, LiveVol, OptionMetrics/WRDS | not researched (budget) | | | | | | | | |

## (2) Free sources, test results
| Source | Test (2026-11-07) | Result |
|---|---|---|
| Hugging Face API search "options"/"spy"/"0dte"/"spx options" | HTTP 200 | only unrelated or non-US sets (e.g. india-index-options-1m, gauss314/options-IV-SP500 EOD IV by name, crypto options). No SPY/SPX 0DTE quote set found |
| Kaggle search URL | 404 | landing only, login for downloads |
| DoltHub /repositories | 301 | not examined |
| GitHub search API | 200 | not parsed |
| Alpha Vantage demo key, SPY 1min and HISTORICAL_OPTIONS | 200 | demo-only notice; free-key limits not verified [O] |
| FirstRate free-intraday-data page | fetched | HTML only, not read |
| cdn.cboe.com VIX1D_History.csv | 307 | guessed URL, redirect not followed; do not rely |
| ThetaData free tier | docs | 1 year EOD only, no intraday |
Intraday VIX1D before 2024-01-22: none found. Yahoo chart: 1-hour bars only (from brief).

## (3) Recommendation
Cheapest listed with NBBO at arbitrary minutes 2022-2026: Massive Options Advanced (USD 199/mo) in raw quotes, but it lacks IV/Greeks and its true 2022 depth must be confirmed. If vendor IV/Greeks matter, ORATS (USD 1,500 + USD 199/mo, 1-min from Aug 2020) is the cleanest single source. Databento (pay per GB, 1-min before Mar 2023, tick after) is a cheaper pilot for a few symbols but you compute IV/Greeks. ThetaData Value/Standard likely competitive but prices unverified. Lacking in all: real underlying minute bars (ORATS excludes them; Yahoo gives 5-min only 60 days) and any free option quote history.

## (4) Reachability (curl, 2026-11-07)
huggingface.co 200; api.github.com 200; alphavantage.co 200; orats.com 200; datashop.cboe.com 200; kaggle.com search 404 (host up); dolthub.com 301; cdn.cboe.com 307; firstratedata.com, massive.com, databento.com, thetadata.net, docs.thetadata.us fetched OK via fetch_page.py. thetadata.net/subscribe returned "thin".

## (5) Blocked
None new this run. From brief: bls.gov 403, stooq.com reset, fred.stlouisfed.org HTTP/2 error.

## Conflicts
ThetaData free tier: rate limit 30 req/min on docs page vs 20 in a search summary; docs page used. Databento start: 2013 on product page; cbbo-1m before 2023-03-28 subsampled. Competitor claim (FlashAlpha) that ORATS is EOD-only is contradicted by ORATS's 1-min page.

## Not found
Cboe DataShop price; ThetaData plan prices; Databento per-schema OPRA cost; Massive Advanced real lookback; IVolatility, AlgoSeek, OptionMetrics intraday status; any free SPY/SPX 0DTE quote set; user reports on Databento/ORATS quality (search found none; ThetaData 2019-Dec 2022 extended-hours gap per search snippet only, not verified); Alpha Vantage free-key limits.

## Search log
ORATS intraday (search, 1 new); ThetaData pricing (search, snippets only); Databento OPRA (search); Cboe intervals (search); complaints (disconfirm; found ThetaData data-issues docs); Massive pricing (search). Budget: about 15 calls.
