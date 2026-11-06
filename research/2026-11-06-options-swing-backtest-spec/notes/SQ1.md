# SQ1 notes (as of 2026-11-06)

*Answer:* For daily-entry swing backtests, the two vendors with documented historical bid/ask plus IV/Greeks are ORATS (near-EOD snapshot 14 min before close, from 2007, 1-min intraday from Aug 2020) and Cboe DataShop (NBBO at 15:45 ET and at close, from Jan 2012, IV/Greeks paid add-on at 15:45). H3 is supported: neither snapshot is the 16:00 close. Databento supplies raw OPRA quotes (you compute IV/Greeks). Massive's Greeks/IV appear only in a current-state snapshot endpoint, consistent with the skill's "no historical Greeks" claim.

*Findings:*
- ORATS EOD = ~15:46 ET, 2007+, Greeks/IV/theoretical values included [E, self-reported] SQ1-1, SQ1-2. ORATS underlying is put-call-parity derived, not a true stock price [E] SQ1-3.
- Cboe: NBBO+size at 15:45 and close; OI only in EOD snapshot; IV/Greeks only at 15:45, extra purchase; 2012+ [E] SQ1-4..6.
- Databento: adjusted contracts get suffix symbols (MSFT1) [E] SQ1-7; pre-2023-03-28 data is subsampled, cbbo-1m finest BBO, OI-only stats [E] SQ1-8, SQ1-9.
- Polygon -> Massive rename 2025-10-30 [E, primary] SQ1-10. Snapshot endpoint "Plan History: Not applicable" [E] SQ1-11.
- ThetaData lists Binomial Greeks and EOD Greeks endpoints [E, listing only] SQ1-12; 2012-06-01 start is from a search summary [unverified] SQ1-13.

| Vendor | (a) bid/ask | (b) EOD time / granularity | (c) start | (d) IV/Greeks, model | (e) expired / adjusted contracts | (f) indicative tier |
|---|---|---|---|---|---|---|
| ORATS | yes (snapshot bid/ask used) | ~15:46 ET (14 min pre-close); 1-min intraday | 2007; intraday Aug 2020 | yes, ORATS-derived (SMV); American model not confirmed | splits history endpoint; adjusted-contract handling not found | not found |
| Cboe DataShop | NBBO + size | 15:45 and close | Jan 2012 | IV/Greeks paid add-on at 15:45; model not found | not found | not found |
| Databento OPRA | NBBO via cbbo-1m, mbp, etc. | tick; cbbo-1m finest pre-2023-03-28 | pre-2023-03-28 is subsampled; earliest date not confirmed | none; compute yourself | suffix symbols (MSFT1); definitions schema | not found |
| Massive | quotes need higher tier (unverified) | n/a | not found | snapshot only, no history | not found | not found |
| ThetaData | yes (quote/EOD) | EOD report 17:15 ET (unverified) | 2012-06-01 (unverified) | yes, incl. Binomial Greeks | not found | not found |
| IVolatility | not researched (budget) | | | | | |

*Recommended default:* ORATS near-EOD for 35-60 DTE delta-selected entries (Greeks/IV ready, 2007 history, bid/ask at ~15:46), modelling fills at bid/ask or mid-with-haircut at that snapshot, with a note that the real close differs. Cboe 15:45 is the audited alternative. For intraday execution use ORATS 1-min (2020+) or Databento (compute IV with an American model). Do not use Massive for historical Greeks.

*Conflicts:* ORATS 14-min-before-close (docs) vs a forum-derived "3:46 pm" (search summary only); consistent. ORATS timing is self-reported.

*Not found:* OI publication timing vs trading day (OCC page returned 403); Massive historical option quote tiers/start year (docs/options/overview 404); pricing model (Bjerksund-Stensland etc.) for any vendor; indicative-price tiers; expired/delisted handling for ORATS, Cboe, ThetaData; IVolatility; Databento OPRA start date.

*Blocked:* theocc.com 403; massive.com/docs/options/overview 404; docs.thetadata.us root thin.

*Search log:* (1) ORATS 14 min snapshot - disconfirm/search, 1 new; (2) Polygon Massive rename - search, confirmed via primary fetch; (3) ThetaData start/Greeks - search, 1 new. Fetch batches: 2 (vendor docs, 11 pages). ~9 tool calls used.
