# SQ3 notes (as of 2026-11-07). Budget used: 15/15 (thin on primary-source numbers; most papers are PDF/SSRN and could not be cached)

## Answer
Same-day SPX options carry a statistically real but economically tiny variance risk premium, so buyers lose gross of costs on average (retail long 0DTE: -53% to -61% per trade). No source found showing positive returns for ATM or OTM 0DTE buyers. Spread data found are anecdotal or vendor-only, so the cost model must still be calibrated from raw quotes (not found in primary tables).

## Findings
(1) Intraday VRP: Vilkov (via secondary summaries, unverified against paper) finds 0DTE VRP positive, ~0.001% from 10am to close, Sep 2016-Jan 2024 [E, SQ3-4, SQ3-5]. No by-time-of-day or day-type table or 2-4 pt vol comparison obtained.
(2) Returns by structure: Retail long -53% (full) / -61% (since May 2022); short +48%/+56% [E, SQ3-3]. Vilkov: no structure held to expiry consistently profitable; long-call/short-put risk reversal ~+0.01% of index before costs [E, SQ3-4]. Exit-rule evidence (intraday exits, spreads/debit) not found.
(3) Intraday theta/gamma: not found from a primary source. Only the VIX1D frozen-window design is documented [SQ3-2].
(4) Spread table (usable inputs, all weak):
 - SPY 0DTE, 5 min before close, 2023-09-13: ~$1 options 5.8% of mid vs ~1% other expiries; ATM penny spread 0.14/0.15 = 6.7% [SQ3-6] (one day, self-reported).
 - NDX 0DTE ATM: expiring ITM ~6 bps of spot mid-to-bid; round-trip cost 300-350 bps/yr at 25% slippage [SQ3-7] (self-reported, % of spot, not of premium).
 - Doshi-Pederzoli-Sert (DPS May 2025) and SEC DERA paper (2503) discuss 0DTE spreads; PDFs unsupported by the cache script, not read. Read them next for spreads.
 - Not found: SPX/XSP/QQQ median % of mid by moneyness and hour. Muravyev-Pearson k=0.70 is the brief's, not rechecked.
(5) VIX1D convention: business years and business minutes, 405-minute session, weights shift from today's strip to next day's; near-term vol frozen at last valid value in the last 60 business minutes (~3pm ET) [E, SQ3-1, SQ3-2]. Implication: hourly BS pricing should use T = remaining business minutes/(405*252 business-year minutes); VIX1D after ~3pm is mostly next-day vol, not same-day. I did not see the exact business-year day count (252 assumed; check white paper).
(6) Single stocks: Cboe lists up to two Monday and Wednesday expiries on qualifying names (mkt cap >$700bn, ETF AUM >$50bn) from 2026-01-26; excluded on days when earnings are after close [E, SQ3-8]. Nasdaq ISE filed similarly (per FOW, unquoted). Daily Tue/Thu not confirmed. SPY/QQQ/IWM already had daily expiries. DJX daily from 2026-05-18 (search snippet, not cached).
(7) Counter-evidence: SQ3-5 (Hull) says VRP exists; the ex-ante OptionMetrics 0DTE VRP is positive but Friday-only (snippet, vendor). No positive buyer returns found. Note retail trades pay wider spreads than a model with k=0.70 would assume.

## Conflicts
- "Tiny VRP (0.001%)" (Vilkov via blog) vs the brief's 2-4 vol pt multi-day gap: different horizons; the figure is per-day return scale, not vol points, so not directly comparable.
- Retail -53% average loss includes spread and fees and is in premium terms, while Vilkov's figures are % of index; different denominators.

## Not found
Primary-source hourly implied vs realised table; day-type splits; theta/gamma by hour; measured SPX/XSP/QQQ spread tables; 1DTE and weekly returns; debit spread returns; Bandi-Fusari-Renò, Almeida et al. numbers (only snippets).

## Blocked
PDFs unsupported by fetch_page.py: bauer.uh.edu DPS papers, sec.gov DERA PDF and SR-Cboe PDF. SSRN blocked (known). Vilkov and Beckmeyer numbers are via secondary summaries (grade C).

## Search log
1. Beckmeyer returns (search) 3 new; 2. VIX1D methodology (search) 2; 3. spreads % of mid (search) 4; 4. buyers positive returns (disconfirm) 2; 5. Vilkov Frankfurt (search) 2; 6. single-stock daily expirations (search) 3; 7. Bandi/Almeida buyer returns (disconfirm) 0 new primaries; plus 5 fetch/grep calls.
