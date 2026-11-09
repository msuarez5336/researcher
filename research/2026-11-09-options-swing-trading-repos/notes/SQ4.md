# SQ4 notes: backtesting frameworks and historical options data (as of 2026-11-09)

## Answer
For retail long-option backtests the practical stack is a framework plus a paid data vendor; no free source gives usable history. QuantConnect LEAN (with bundled AlgoSeek minute data for SPX/VIX/NDX and 4,000 equity symbols from 2012) is the only candidate where data, intraday option bars and live trading come together. Other frameworks (Optopsy, Lumibot, NautilusTrader) need an external data feed. Default fills are optimistic or absent in most tools, so the fill model is the main risk.

## Frameworks (stars/pushed_at from GitHub search API, read 2026-11-09)
| Name | Repo | Stars | pushed_at | Options features confirmed | Intraday options | Fill model | Reported limits | Status |
|---|---|---|---|---|---|---|---|---|
| QuantConnect LEAN | QuantConnect/Lean | 22466 | 2026-11-09 | Index and equity option datasets, minute/hour/daily (E1,E2) | Yes (minute) | Default fill ignores bid/ask size and volume; custom fill model possible (E3) | Default fill model (E3). Pre-2021 SPXW had no daily 0DTE (QC index options doc, not quoted) | Active |
| Optopsy | goldspanlabs/optopsy (moved from michaelchu/optopsy; old path not searchable) | 1514 | 2026-11-04 | 38 strategies, simulator, chain fetch via EODHD (E4,E6) | Unclear (README shows daily-style data; not confirmed) | Mid, spread, liquidity or per-leg slippage (E4) | README disclaimer: no execution slippage, assignment risk (E5). Needs external data | Active. Includes sold-premium strategies; filter for long ones |
| Lumibot | Lumiwealth/lumibot | 2219 | 2026-11-09 | Options listed as asset class; same code for backtest and live; ThetaData recommended per search summary (E7) | Unclear | Not confirmed | Open issues: #514 options backtest fails (2024), #691 Alpaca option pricing missing (E8, unverified) | Active (high commit rate) |
| NautilusTrader | nautechsystems/nautilus_trader | 31416 | 2026-11-09 | OptionContract, OptionSpread, chain aggregation, Greeks (E9) | Unclear (tick/bar engine, no equity-options data adapter confirmed) | Not confirmed | Open: #4653 backtest needs venue Greeks, #5218 multileg combo in backtest, #5588 expired instruments (E10, unverified) | Active; options support is crypto-venue oriented (Deribit issues) |
| backtrader | mementum/backtrader | 23701 | 2024-08-19 | None confirmed (no options docs checked) | No | n/a | No options support found; no recent pushes | Stale (last push 2024-08-19) |
| vectorbt | polakowo/vectorbt | 9782 | 2026-11-08 | None confirmed; issue search returned no options issues | No | n/a | Not built for option chains (search found no options work) | Active, options not reached |
| optionlab | rgaveiga/optionlab | 590 | 2026-11-07 | Strategy payoff/profit evaluation library | No | n/a | Pricing/payoff library, not a backtester (out of scope per brief) | Active |
| backtesting.py | kernc/backtesting.py | 9216 | 2026-08-05 | Not checked | not reached | | | |

Not pure long: Optopsy (mixed library), optionlab (payoff tool).

## Data sources
| Name | History depth | Resolution | SPX | Price (vendor, date) | Free tier | Reported limits | Status |
|---|---|---|---|---|---|---|---|
| QuantConnect/AlgoSeek | Jan 2012 (E1,E2) | Minute, hourly, daily | Yes (SPX, VIX, NDX; SPXW) | Not captured (data needs QC subscription) | QC free tier not checked | Data only inside QC/LEAN CLI | Active |
| Massive (ex-Polygon.io) | Years of tick history per search summary, depth not confirmed | Aggregate bars any timespan, from trades only (E11,E12) | Not confirmed | Third party June 2026: Starter $29, Advanced $199 (E14); massive.com pricing page showed "$99 /month per dataset" and $29/$49/$99/$199 tiers, not mapped to options | Basic $0 (search summary) | No bar in intervals without trades (E11) | Active; renamed 2025-10-30 (E13, unverified) |
| ThetaData | 6/10/14 yrs by tier (E15,E17,E18) | 1 minute (Value), tick (Standard/Pro) (E16) | "US Index & Stocks" | $40 / $80 / $160 per month (thetadata.net/pricing, 2026-11-09) | None seen | Concurrency limits 2/4/8 requests by tier | Active |
| ORATS | EOD to 2007; 1-minute from Aug 2020 (E27, unverified) | EOD, 14 min before close, 2-min/1-min intraday | Yes (per ORATS marketing, unconfirmed) | Conflicting: $99, $199, $1,395 per month on different pages; unresolved | No | Pricing unclear | Active |
| Cboe DataShop | Not captured | EOD, 15:45 snapshot, 1-min/n-min (E20,E21) | Yes, but index bid/ask needs CGI licence from $1k/month (E22) | Per-dataset, not captured | No | Licence cost (E22) | Active |
| OptionsDX | Not captured | Up to minutely (E19) | Yes (SPX, VIX, SPY) | Not captured (page thin) | Name suggests free EOD; unconfirmed | Not captured | Active |
| Databento OPRA | Not captured (pages thin) | Not captured | Not captured | Not captured | n/a | n/a | Not reached |
| yfinance | Current chains only (E24, forum, unverified) | Snapshot | Index via ^SPX not checked | Free | Yes | Personal use only, unaffiliated (E23); rate limits, incomplete Greeks (search snippet) | Active; fine for forward snapshotting only |

## Findings
- [E] LEAN has bundled minute-resolution OPRA-derived data for SPX/VIX/NDX and 4,000 equity symbols from 2012 (SQ4-1, SQ4-2).
- [E] LEAN default fill ignores size/volume (SQ4-3) [source is staff forum reply, graded opinion].
- [E] Optopsy offers slippage models but its own disclaimer excludes execution slippage and assignment risk (SQ4-4, 5, 6).
- [E] Massive option bars come only from trades, so illiquid contracts have gaps (SQ4-11); backtests need quote data (bid/ask) for realistic fills, which is a separate quote endpoint not examined.
- [E] ThetaData tiers: $40 (6y, 1-min), $80 (10y, tick), $160 (14y) per month (SQ4-15 to 18).
- [E] Cboe offers 1-minute NBBO data but SPX index quotes need a CGI licence from $1k/month (SQ4-20, 22).
- [O] ORATS says use quotes 14 min before the close and model slippage at 53-75% of bid-ask width (SQ4-25, 26); vendor self-report.
- [E] Search found mid-price fill assumptions flipping results (dev.to 96 SPY put credit spreads post; Pineify 10-20% overstatement claim). Both secondary and not cached, so not recorded as evidence.

## Conflicts
- ORATS slippage floor: the search summary said 56% for four legs, the cached ORATS page says 53%. The cached page was used.
- ORATS and Massive prices differ across pages (ORATS $99/$199/$1,395; Massive pricing page vs third-party list). Check the vendor page at purchase time.

## Not found
- Databento OPRA price, depth and resolution (pages returned thin).
- OptionsDX price and free tier; Cboe DataShop price per dataset.
- Options docs in backtrader and vectorbt (no options features found, not exhaustively checked).
- Lumibot's own docs on ThetaData options and its fill model; Lumibot/Nautilus intraday options status.
- Massive options history depth and plan mapping.
- Optopsy GitHub issues on options problems: issue search returned only old closed issues.

## Blocked
- Hosts/tools: docs.thetadata.us returned thin content; optionsdx.com and databento.com/pricing returned thin (JS-rendered). quantconnect.com/data/tickers returned 404. github.com HTML not used.

## Outdated names a reader may meet
- Polygon.io, now Massive (api.polygon.io still served in transition per search summary).
- michaelchu/optopsy, now goldspanlabs/optopsy (the old path failed in repo search; whether it redirects is unconfirmed).
- backtrader: no push since 2024-08-19.
- Old Polygon price tiers ($99 Developer) in older snapshots.

## Search log
1. gh repo metadata batch for 9 repos (search): 6 repos' stats; 3 old paths failed.
2. WebSearch Polygon rebrand/pricing (search): 3 sources.
3. WebSearch misleading fills (disconfirm): ORATS, dev.to, Pineify, QC forum.
4. fetch_page batch of 8 (optopsy, optionlab, lumibot READMEs, massive, thetadata, optionsdx, databento, QC index): 5 ok, 2 thin.
5. gh issue search first form failed (needs is:issue); second form worked for 5 repos (disconfirm).
6. fetch_page batch of 10 vendor docs: 8 ok.
7. WebSearch yfinance history (search): forum snippet.
8. Grep passes over cached pages (several calls).
9. WebSearch Lumibot ThetaData; WebSearch ORATS pricing; fetch batch (QC forum, ORATS methodology, FlashAlpha, Nautilus docs).
Total about 17 of 20 calls.
