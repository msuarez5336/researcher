# SQ3: which single option to buy (as of 2026-11-07)

## Answer
Evidence reachable in 15 calls says long options have negative average returns, and short-dated retail buys lose mostly through costs plus the variance risk premium. I found no rigorous study of long-call/put returns by expiry and delta paired with a directional signal. The best lead is Vilkov's held-to-expiry SPX study, which I only saw via a summary.

## Findings
- Long ATM straddles lost about 3%/week on SPX (1990s sample, old for the field). [E] SQ3-1
- Retail 0DTE SPX losses, net of costs, about 60% from costs; buyers have negative expected return before expenses. [E] SQ3-2, [O] SQ3-3 (grade C: secondary summary of an SSRN paper; no direct quote of the paper)
- Vilkov: median-profitable deep-ITM call buys, but averages are not statistically distinguishable from zero; P&L tied to realized index skewness. [E, secondary] SQ3-4, SQ3-5
- Earnings: straddles usually priced rich, but 2026 season returned about 45% (vendor). [E, self-reported] SQ3-6. Search snippets also gave ORATS history of actual/implied about 85% (not cached or verified).

## Conflicts
Unconditional buyer losses (SQ3-1..3) versus ORATS 2026 earnings season gains (SQ3-6): regime/season dependent, single season.

## Not found
Long-call/put returns by DTE and delta (academic); captured fraction of a correct move by expiry; entry-time-of-day premium effects; Bandi-Fusari-Reno (a pricing paper, not returns); signal-paired option P&L (candidate: Cologne CFR 26-02 on intraday option momentum, PDF unsupported by the fetcher, snippet only); MDPI earnings straddle paper (403). Primary papers (Beckmeyer et al., Vilkov, Bryzgalova) are on SSRN, blocked, so not verified.

## Blocked
papers.ssrn.com (per brief), mdpi.com 403, carey.jhu.edu 403; cfr-cologne.de and aeaweb.org PDFs unsupported by fetch_page.

## Search log
1 Beckmeyer retail 0DTE (search, 3 new); 2 Bandi Fusari Reno (search, 1); 3 retail 0DTE losses (disconfirm/against, 1); 4 Coval Shumway (search, 1); 5 0DTE returns by moneyness (search, 0 useful); 6 delta-hedged returns by moneyness (search, 0 usable); 7 earnings straddles (search, 2); 8 0DTE buyers signal (search, 2: Vilkov, CFR 26-02). Fetches/caches: 3 calls.

## Table
| expiration | moneyness / delta | condition | sample | avg return | fills & costs | grade | source id |
|---|---|---|---|---|---|---|---|
| ~1 week | ATM straddle (zero-beta) | unconditional | SPX options, 1990s (outdated) | about -3%/week | not stated in abstract | A | SQ3-1 |
| 0DTE | mixed, puts worse | unconditional (retail buys and sells) | SPX, about 2 years to 2023 | aggregate retail loss $184k/day ($358k post May 2022) | actual retail fills incl. costs; about 60% of loss is costs | C | SQ3-2, SQ3-3 |
| 0DTE held to expiry | deep ITM calls | unconditional | SPX Sep 2016 to Jan 2024 | positive median, mean not different from zero | not stated in summary | C | SQ3-4 |
| earnings event | ATM straddle | event | one 2026 season, single stocks | about +45% | vendor, fills not stated | B | SQ3-6 |
