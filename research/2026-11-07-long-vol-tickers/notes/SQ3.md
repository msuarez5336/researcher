# SQ3 notes (as of 2026-11-07)

**Answer:** Liquidity is dominated by SPY, QQQ, NVDA, IWM, TSLA, then MU, AAPL, INTC, AMD, AMZN, META, IBIT. Per-symbol OCC/Cboe 2025 statistics were not reachable (theocc.com 403), so the ranking uses dated secondary single-day / 1-month figures. OI and measured spreads were not published in any source found. Of the Cboe single-name/ETF vol indices, all but VXXLE returned CSVs current to 2026-11-05/06.

## Candidates (secondary rankings; contracts/day; OI not found)
| # | Ticker | Type | Volume | Source + date | Weeklies | Spread note |
|---|---|---|---|---|---|---|
|1|SPY|ETF|12.2M (11/6); 11.7M 1-mo avg (10/30); 19.0M (11/5)|E3, E1, E5|y (daily)|penny at all prices|
|2|QQQ|ETF|8.25M; 8.7M avg; 13.0M|E3,E1,E5|y (daily)|penny at all prices|
|3|NVDA|stock|4.40M; 2.6M avg; 4.68M|E3,E1,E5|y|penny-class (assumed, not opened)|
|4|IWM|ETF|2.04M; 1.9M avg; 3.11M|same|y|penny at all prices|
|5|TSLA|stock|2.55M; 2.0M avg; 2.25M|same|y|penny-class (assumed)|
|6|MU|stock|1.57M; 1.1M avg; 1.91M|same|y|unverified|
|7|AAPL|stock|1.47M; 1.2M avg; 1.42M|same|y|unverified|
|8|INTC|stock|1.08M (11/6); 1.44M (11/5)|E3,E5|y|unverified|
|9|AMD|stock|1.06M; 0.93M|E3,E5|y|unverified|
|10|AMZN|stock|0.91M (11/5)|E5|y|unverified|
|11|META|stock|0.97M (11/6); 0.66M (11/5)|E3,E5|y|unverified|
|12|IBIT|ETF|1.06M (11/5)|E5|y|unverified|
|13-24|SMH, TLT (906k 1-mo avg), PLTR, GOOGL, MSFT, EWZ (1.1M 1-mo avg), AVGO, ORCL, HOOD, PFE, SOXX, SOFI|mixed|0.5-0.9M (11/5)|E5,E2|mostly y (weeklies not verified per name)|unverified|

Excluded: leveraged ETFs (SOXL, TQQQ), and newly listed/odd symbols (SPCX labelled "SpaceX", DRAM, IREN, CRWV) due to short history or unclear identity. SPX/VIX index products out of scope.
Weeklies: not documented per name in sources; all names above are widely known to have weeklies (unverified assumption). Penny rule: $0.01 below $3, $0.05 above, except SPY/QQQ/IWM $0.01 always (E8, search summary only).

## Volatility indices (CSV https://cdn.cboe.com/api/global/us_indices/daily_prices/<IDX>_History.csv, checked 2026-11-07)
| Index | Underlying | Status | Last date |
|---|---|---|---|
|VIX|S&P 500|active|2026-11-05|
|VXN|Nasdaq-100|active|2026-11-06|
|RVX|Russell 2000|active|2026-11-06|
|VXAPL|AAPL|active|2026-11-06|
|VXAZN|AMZN|active|2026-11-06|
|VXGOG|GOOGL|active|2026-11-06|
|VXGS|GS|active|2026-11-06|
|VXIBM|IBM|active|2026-11-06|
|GVZ|GLD/gold|active|2026-11-06|
|OVX|USO/oil|active|2026-11-06|
|VXEEM|EEM|active|2026-11-06|
|VXSLV|SLV|active|2026-11-06|
|VXEWZ|EWZ|active|2026-11-06|
|VXFXI|FXI|active|2026-11-06|
|VXTLT|TLT|active|2026-11-06|
|VXEFA|EFA|active|2026-11-06|
|VXXLE|XLE|HTTP 403 AccessDenied; not available|n/a|
No VIX-style index exists for NVDA, TSLA, MSFT, META, SPY, IWM, MU. Last dates read via curl tail; E9-E12 hold cached quotes for VXAPL, GVZ, VIX, VXXLE.

## Findings
- Volume snapshots [E] E1-E5. Industry totals [E] E6,E7 (unverified, summaries). Penny rule [E] E8 (unverified).
## Conflicts
Absolute volumes differ by source/day (SPY 11.7M avg vs 19.0M on 11/5, a spike day); different dates and methods. Use rank, not level.
## Not found
OCC/Cboe per-symbol 2025 ADV, open interest per underlying, measured spread data, per-name weeklies list.
## Blocked
theocc.com (403), cdn.cboe.com VXXLE (403), marketchameleon (thin), optioncharts/marketchameleon MostActive (404), optionsanalysissuite via script (429; WebFetch worked).
## Search log
1 search: most active underlyings (search, several sources); 2 search: OCC annual (search, OCC hits blocked); 3 search: top 25 2025 (search, 0 new usable); 4 search: penny pilot (search, Cboe archive); disconfirm: attempts at OCC primary data failed. Budget used 15.
