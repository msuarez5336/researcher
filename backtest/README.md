# Option setup backtest (estimated prices)

Phase 1 of `plans/2026-11-12-option-backtest.md`, built without bought data. It tests whether
buying a 1–6 month call or put after a chosen setup did better than buying the same option on
ordinary days. **Option prices are estimates, not quotes**: results rank ideas, they are not
evidence of profit.

| File | What it does |
|---|---|
| `fetch_data.py` | Downloads daily closes for 65 stocks (Yahoo Finance) and Cboe volatility indexes; writes `artifact/data.js`. Raw files are cached in `data/raw/` (gitignored). |
| `calibrate_iv.py` | Fits the implied-volatility estimate on the five stocks with a Cboe volatility index, measures its error on later years, writes `artifact/iv_model.js`. |
| `artifact/engine.js` | The backtest engine: pricing, signals, trade simulation, statistics. Runs in the browser and in Node. |
| `artifact/index.html` | The interactive page. Published as an artifact with the three `.js` files beside it. |
| `test_engine.js` | Engine tests: pricing against textbook values, no use of future data, a planted effect is found and a null is not. |
| `run_cli.js` | Runs one configuration from the command line. |

```bash
python3 backtest/fetch_data.py        # refresh data (add --refresh to refetch everything)
python3 backtest/calibrate_iv.py      # refit and re-measure the volatility estimate
node backtest/test_engine.js          # tests
node backtest/run_cli.js '{"cond":{"metric":"ret1","x":8}}'
```

## How option prices are estimated

`IV30 = a + b1·RV20 + b2·RV60 + b3·VIX`, fitted on AAPL, AMZN, GOOGL, GS and IBM for 2011–2018
and checked on 2019–2026. The coefficients and measured errors are in `artifact/iv_model.js`;
`calibrate_iv.py` prints them. The 30-day estimate is scaled to the option's maturity with
VIX3M/VIX and VIX6M/VIX, tilted by strike distance, and fed to Black-Scholes with the 13-week
T-bill rate and no dividends. The approach extends the realised-volatility-plus-margin proxy
used in the earlier event-windows run.

## Known limits

- The 65 stocks were chosen in 2026, so all survived. That flatters calls.
- No earnings dates, so no earnings premium in prices.
- After a sharp fall the estimate rises more slowly than real implied volatility, which
  flatters fall-and-rebound setups.
- Any strike is assumed available; the bid-ask spread is an assumption set by the user.
- The volatility fit used 2011–2018 data and is applied from 2009, a mild use of later data.
- 2021–2026 is the holdout. The page locks it until the user unlocks it.
