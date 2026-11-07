# SQ7 notes (as of 2026-11-07)

*Answer:* No candidate has a clean independent post-publication out-of-sample test on SPY/QQQ with option-buying P&L. The best-documented decay is C1 (net about zero after costs on index CFDs, SQ1-5/6) and the overnight variant of C3 (Rosa 2022, SQ7-1). C6 turned out to be a delta-hedged option-return seasonality paper, not a tradable option-buying rule.

*Findings*
- C1: only independent replication is SQ1-5/SQ1-6 (CFDs, 2015-2026): gross reproduces, net about zero, OOS 2021-26 at most +0.06 R on NQ, negative 2015-2017. [E, grade C blog]. Vendor posts (cutemarkets) say ORB fails under realistic option fills but gave no checkable numbers; not recorded. [O]
- C2: only a 2016 one-year QuantConnect recreation (Sharpe 2.396) [E, SQ7-3]; forum notes live-vs-backtest gap [O, SQ7-4]. No post-2023 test found.
- C3: Rosa 2022 finds the overnight-return variant disappears OOS [E, SQ7-1]; QC 2015-2020 weak (SQ1-11). Search summary mentions a 16-country replication with 12/16 significant (unverified, not recorded).
- C4: no replication post-2020 found; Cboe says no rise in last-hour moves with 0DTE; other work says higher dealer gamma means reversals [SQ7-5, unverified].
- C5: no independent OOS test found; only TradingView/Python code ports and authors' own claims [O]. Sample ends 2024, in-sample.
- C6: CFR 26-02 = Bali, Goyal, Moerke, Weigert, "In Search of Seasonality in Intraday and Overnight Option Returns"; momentum in half-day option returns 0.22-0.45% per half-day, patterns increase over time [E, SQ7-2]. It is about delta-hedged returns and market-maker supply constraints; no replication yet (new, 2026). Data 2004-2021 single-stock options per search summary (unverified). Raw buy-only returns after spreads not tested here.

*Conflicts:* C4: Baltussen (negative gamma means momentum) vs later 0DTE work (dealer gamma means reversal); samples and markets differ (futures to 2020 vs 0DTE era). C6 "increase over time" vs decay in C1/C3.

*Not found:* Independent QQQ/SPY option-based ORB replications with bid/ask fills; post-2018 SPY first-half-hour test; post-publication C5 test; live fund results; VIX-regime splits for C1/C2/C5.

*Blocked:* cfr-cologne.de PDF is not cacheable (application/pdf unsupported); abstract taken from econpapers. SSRN not tried. Budget used: 14 of 15.

*Search log:* CFR 26-02 (search, 1 new, found paper); intraday momentum decay (search, Rosa 2022); ORB QQQ replication fails (disconfirm, mql5 already known); fetch of 3 pages; 0DTE gamma momentum (disconfirm, Cboe/Quantpedia); stocks in play decay (disconfirm, vendor blogs only); noise area replication (0 new); Baltussen replication (0 new).

| candidate | replicated? | post-publication result | decay / crowding | verdict | ids |
|---|---|---|---|---|---|
| C1 ORB QQQ | CFD blog, 2015-2026 | net about 0 R; OOS 2021-26 <= +0.06 R | cost-driven; 2015-17 negative | weakened | SQ1-4, SQ1-5, SQ1-6 |
| C2 Stocks in play | QC, 2016 only | unknown | live gap in forum | unknown | SQ1-8, SQ7-3, SQ7-4 |
| C3 first half-hour | QC 2015-2020; Rosa 2022 (overnight variant) | weak; overnight variant vanishes OOS | regime dependent | weakened | SQ1-1, SQ1-2, SQ1-11, SQ7-1 |
| C4 gamma filter | none found | unknown; Cboe: no 0DTE effect on last hour | 0DTE may flip sign | unknown | SQ2-7, SQ7-5 |
| C5 noise area | none independent | unknown | none found | unknown | SQ1-9 |
| C6 option momentum | none yet | paper says growing over time | supply-side | unknown | SQ7-2 |
