# SQ5 notes: costs, rules, broker execution (as of 2026-11-07)

## Answer
The PDT rule has been replaced: FINRA Rule 4210 intraday margin standards took effect 2026-06-04 (broker phase-in to 2027-10-20), so the $25,000 minimum and 4-trades-in-5-days designation are gone, but broker implementation may lag. Commissions for buying a few options a day are small (about $0 to $1 per contract plus about $0.04 regulatory fees), so spread, not commission, is the main cost. I found no current, measured quoted/effective spread numbers for SPY/QQQ/IWM by moneyness or time of day.

## Findings
- [E] PDT replaced by intraday margin rule, effective 2026-06-04, phase-in to 2027-10-20 (SQ5-1, SQ5-2). Secondary news reports (not cached) say SEC approved 2026-04-14.
- [E] Commissions: tastytrade $1 open/$0 close, $10 cap per leg (SQ5-6); Webull $0 (SQ5-7); Fidelity $0 commission plus an unspecified contract fee (SQ5-9); IBKR Pro $0.65 per contract at lowest tier, $1 min per order (SQ5-10); Robinhood $0.04 per contract ORF/OCC (SQ5-12); Tradier $0.35 Lite, $0 Pro (SQ5-13).
- [E] Alpaca supports options, single-leg stop and stop-limit, paper trading by default, auto-exercise of ITM at expiry (SQ5-3, 4, 5). Alpaca bracket/OCO for options: not found.
- [E] IBKR conditional orders can reference another contract's price and submit/cancel an order (SQ5-11). Bracket/OCA exist in TWS API (search summary only, bracket page 503).
- [E] Schwab Trader API supports TRIGGER and OCO strategies via schwab-py, a community library (SQ5-14, grade C). Schwab commission page returned an error and Schwab learn pages were thin.
- [E] Spread literature: Muravyev and Pearson found effective spreads below quoted spreads, sample 2003-2006 (SQ5-15, unverified, from search snippet). Hoshi et al. working papers (bauer.uh.edu DPS series) link intraday order-flow volatility to wider spreads, strongest for 0DTE and 1-6 DTE; read via search summary only, not recorded as evidence.
- [O] Webull FAQ says OCO can occasionally double-execute (SQ5-16, unverified).

## Conflicts
- Robinhood: a search summary said $0.50 contract fee for stock options. The fee page I cached shows the $0.35/$0.50 contract fee in the index-options section only. I did not confirm stock/ETF option commission is $0 (not stated in the lines I read).
- Fidelity: "$0 commission" headline vs "Option contract fees apply" (amount not captured, commonly $0.65 but not verified).

## Not found
- Measured quoted/effective spreads for SPY/QQQ/IWM and single stocks by moneyness, DTE, time of day (post-2022). Price-improvement statistics. Cash-account settlement rule for options (T+1 as of 2024 not checked). Early-assignment rules for long options (long holders are not assigned; not sourced). Bracket/OCO support for options at Alpaca, tastytrade, Robinhood, Tradier, Fidelity. Robinhood official options API. Paper trading at Schwab, tastytrade, Fidelity, Robinhood.

## Blocked
- schwab.com pricing: authorization error page. schwab.com learn pages: thin. IBKR bracket docs: HTTP 503. Robinhood US options-fee article URL guess: 404. tradier.com/products/pricing: 404. IBKR WebFetch returned 403 (fetch_page worked). Not checked: Fidelity order types, tastytrade order types/API, Tradier order types, IBKR paper docs.

## Search log
- PDT 2026 (search): FINRA 26-10 plus news, 1 primary source.
- Muravyev Pearson (search): paper abstract pages, no time-of-day numbers.
- 0DTE spreads by time of day (disconfirm/gap check): found only working papers and weak sources; no clean measurement.
- IBKR bracket/conditional (2 searches), Schwab OCO/API, Robinhood fees, Tradier fees, Webull API: summaries; several cached.
- Direct fetches: IBKR, Schwab, Alpaca, tastytrade, Webull, Fidelity, Robinhood, Tradier, FINRA.
- Budget: 20 of 20 used.

## Table 1: costs and rules
| cost or rule | product | measured value / rule text | as-of | grade | source |
|---|---|---|---|---|---|
| PDT rule | US margin accounts | Replaced by intraday margin rule; $25k min and day-trade count removed; effective 2026-06-04, phase-in to 2027-10-20 | 2026-04 | A | SQ5-1, SQ5-2 |
| Cash-account option settlement | US options | not checked | n/a | n/a | n/a |
| Early assignment/exercise | long options | Alpaca auto-exercises ITM at expiry by default; assignment risk for long-only not sourced | 2026-11 | B | SQ5-5 |
| Timing-adjusted effective spread | 37 stocks + 2 ETFs, 2003-2006 | about 1/3 below conventional effective spread (summary only; outdated) | 2020 paper | A (unverified) | SQ5-15 |
| Quoted/effective spread, SPY/QQQ/IWM by DTE/time | n/a | not found | n/a | n/a | n/a |
| Price improvement | n/a | not found | n/a | n/a | n/a |
| Regulatory/clearing fee | Robinhood options | $0.04 per contract | 2026-11 | B | SQ5-12 |

## Table 2: brokers
| broker | options commission | bracket/OCO on options | underlying-triggered conditional | API | paper trading | source |
|---|---|---|---|---|---|---|
| Interactive Brokers | $0.65 per contract Pro (lowest tier), $1 min/order | TWS API bracket/OCA (search summary; docs page 503) | Yes, contract price conditions (SQ5-11) | TWS API (yes, per search summary) | recommended in docs (summary only) | SQ5-10, SQ5-11 |
| Schwab | unreachable | OCO and 1st-triggers-OCO in thinkorswim (search summary, page thin) | not checked | Trader API; TRIGGER/OCO via schwab-py (C) | not checked | SQ5-14 |
| Fidelity | $0 plus contract fee (amount not captured) | not checked | not checked | not checked | not checked | SQ5-9 |
| tastytrade | $1 open, $0 close, $10 cap per leg | not checked | not checked | API listed on site nav, not checked | not checked | SQ5-6 |
| Tradier | $0.35 Lite; $0 Pro/Pro Plus | not checked | not checked | API listed | sandbox (search summary only) | SQ5-13 |
| Webull | $0 | OCO/OTOCO via API (search summary only, unverified); FAQ warns of double-fill | not checked | Trading API supports options | not found for API | SQ5-7, SQ5-8, SQ5-16 |
| Robinhood | $0.04 regulatory per contract; stock/ETF option commission not confirmed | stop and stop-limit exist (page body empty); bracket not checked | not checked | no options API found | not checked | SQ5-12 |
| Alpaca | not stated in docs | stop/stop-limit single-leg only; bracket/OCO not found | not found | yes, REST API | yes, default | SQ5-3, 4, 5 |
