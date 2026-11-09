# SQ3 broker APIs (as of 2026-11-09). Stars/pushed_at from GitHub search API on 2026-11-09.

*Answer:* Best-supported live/paper paths for long calls/puts incl. SPX 0DTE: Alpaca (official alpaca-py; index options live incl. SPXW, paper available, but no spot index data), Interactive Brokers via ib_async (maintained; index options need paid data), Tradier (REST, sandbox is delayed data), Schwab via schwab-py (7-day token, no paper). Webull and tastytrade are usable but with gaps; Robinhood and E*TRADE are weakest.

## Table
| Broker | Library | Official? | Stars | Last push | Options features confirmed | Index opts | Paper | Cost (dated) | Reported limits | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Interactive Brokers | ib-api-reloaded/ib_async | unofficial | 1787 | 2026-11-04 | Option contract type, chains (README) [SQ3-1] | yes (SPX via IBKR; library supports Index type) | yes (IBKR paper acct; not verified here) | Data: SPX needs separate index sub; underlying not included in OPRA; Greeks need Network sub [SQ3-3,4]; fee amounts vary by page, unverified | Data entitlements | maintained |
| IBKR old | erdewit/ib_insync | unofficial | 3281 | 2024-03-14 | - | - | - | - | archived [SQ3-2] | dead (use ib_async) |
| Schwab | alexgolec/schwab-py | unofficial | 480 | 2026-08-26 | chains, option_buy_to_open_limit, SPXW symbols [SQ3-5,7] | likely yes (SPXW symbol helper); order of $SPX not verified | no (not found) | not found | 7-day refresh token [SQ3-6]; no historical options data [SQ3-8]; 120 req/min per third-party wrapper (search, unverified) | maintained |
| Tastytrade | tastyware/tastytrade | unofficial (Tastytrade also has official open API, developer.tastytrade.com) | 259 | 2026-08-07 | chains, streamed quotes/Greeks via DXLink [SQ3-9] | unclear | yes, cert sandbox, resets every 24h, delayed feed [SQ3-10] | not found | DXFeed licensing/streamer issues (issue #142, title only) | maintained |
| Alpaca | alpacahq/alpaca-py | official | 1591 | 2026-11-09 | options orders; multi-leg [SQ3-13] | yes live: SPX, SPXW, VIX, VIXW, DJX, XSP [SQ3-11] | yes, incl. index options [SQ3-14] | fees "contact customer success manager" for index options (search snippet) | no spot index data [SQ3-12]; paper fills differ [SQ3-14]; open issue #515 options chain missing strike/expiration | maintained |
| Tradier | thammo4/uvatradier (28 stars, 2026-04-18); rleonard21/PyTradier 63, 2023-09-30; no official Python lib found | REST API official, wrappers unofficial | 28 | 2026-04-18 | chains+Greeks, multileg, OTOCO, streaming [SQ3-16] | yes (SPX fee listed) | yes sandbox, delayed data [SQ3-17] | Index options $0.35/contract Pro, $0.10 Pro Plus, plus fees; SPX line $0.60 [SQ3-18] | wrappers small/stale | API maintained; wrappers weak |
| Webull | webull-inc/webull-openapi-python-sdk | official | 73 | 2026-10-19 | single/multi-leg options, limit orders [SQ3-20] | conflict: QuantConnect says yes, Webull docs list "Options" with no index mention | no [SQ3-21] | not found | old repo deprecated [SQ3-19]; unofficial tedchou12/webull 640 stars, last push 2024-03-18 | official maintained; unofficial stale |
| Robinhood | jmfernandes/robin_stocks | unofficial | 2127 | 2026-02-11 | description says options supported | unclear | no | commission-free (not verified) | open login/MFA issues [SQ3-24]; no official stock/options API [SQ3-25] | unverified / fragile |
| E*TRADE | jessecooper/pyetrade | unofficial | 250 | 2026-05-15 | place_option_order [SQ3-22] | unclear | sandbox exists (apisb.etrade.com) | not found | token expires midnight ET [SQ3-23, unverified] | maintained (wrapper) |

## Findings
- [E] Alpaca live index options and spot-index-data gap: SQ3-11,12.
- [E] Schwab 7-day token: SQ3-6. [E] Tradier sandbox delayed: SQ3-17. [E] IBKR data entitlement: SQ3-3,4.
- [E] ib_insync archived, ib_async is the fork: SQ3-1,2.

## Conflicts
- Webull index options: QuantConnect docs say supported (SQ3-21); Webull developer docs list US products as "Options" without index mention (search summary claimed an explicit exclusion; I could not confirm in cached page).
- Tradier SPX per-contract fee: $0.60 (fee table) vs $0.35/$0.10 (Pro/Pro Plus note); search found $0.45 on an older page. Likely different plan tiers/dates.
- TradersPost docs say Alpaca has no index options; predates Alpaca's launch announcement; trust Alpaca.

## Not found
Schwab official rate limits and paper trading; tastytrade index-option confirmation and fees; IBKR commission schedule and paper API specifics; Robinhood/E*TRADE index option API support; options-specific fill issues in issue trackers (issue searches returned mostly auth/symbology items; titles only, not read).

## Not reached
Tradier official docs on SPX orders, schwabdev (tylerebowers) wrapper, tastytrade official OAuth SDKs, Public.com, moomoo, Firstrade, Lightspeed.

## Outdated names
TD Ameritrade API / tda-api (replaced by Schwab API; tda-api not checked), ib_insync (archived), webull-inc/openapi-python-sdk (deprecated), tastyworks-api (old name of tastytrade lib; docs at tastyworks-api.readthedocs.io), tedchou12/webull.

## Blocked
github.com HTML (per brief); tastyware.dev, tastyware.github.io, robin_stocks raw README (404); developer.tastytrade.com/sandbox moved (thin) so /docs/sandbox used. Several evidence items are verified=false (API metadata or search-snippet only).

## Search log
Repo metadata loop (search, 9 repos + 3 discovery queries; several repo paths 422); Alpaca index options (search, 15 results); Schwab limits (disconfirm); Tradier fees; Webull OpenAPI (disconfirm, found conflict); IBKR data fees; Robinhood API (disconfirm); tastytrade sandbox; E*TRADE tokens; issue searches for 5 repos; page caches x4. 17 calls used.
