# Prompt: intraday long-option opportunities

Paste everything below the line into a new session on this repo (branch `claude/inspiring-cerf-epxwvd`
or a branch made from it).

---

/research When, within a single trading day, does buying options (calls or puts held minutes to hours, closed the same day) have a positive expected return after realistic costs on liquid US underlyings? Which intraday windows, triggers, structures and exits are worth a pre-registered backtest?

Context: read these first. They are prior runs in this repo, and their findings are the starting point, not to be re-researched.
- `research/2026-11-06-options-swing-backtest-spec/report.md`: the v2 backtest spec (fills at k = 0.70 of the spread per leg, stress at k = 1.0, about $0.70 per contract per side, walk-forward with a holdout, gates written in advance, trial counting).
- `research/2026-11-07-long-vol-tickers/report.md`: the 10-ticker shortlist (QQQ, AAPL, NVDA, MU, AMD, SMH, HOOD, TSLA, SOXX, SOFI). Unconditional long volatility loses: 10-day straddles at implied lost 7–23%. Implied runs 2–4 vol points above realised.
- `research/2026-11-07-event-windows/report.md`, including "Follow-up: buying with the move": implied vol falls 1–1.6 points after shocks; buying the bounce after index shock days loses; pre-FOMC drift ≈ 0 since 2016; FOMC-day straddles are regime-dependent. Single stocks show next-day continuation after large, stock-specific, high-volume moves in 2021–26 but not 2016–21 (hypothesis H-MOM1, trial #1,537, not yet run).
- Earnings are **out of scope** (my standing decision).

What I want answered:
1. **Intraday windows**, each with mechanism, prior evidence and effect size:
   - the open (first 5–30 minutes; opening-range breakout vs fade);
   - gap days (gap-and-go vs gap-fill);
   - scheduled macro releases (08:30 ET CPI/payrolls, 10:00 ET data, 14:00 ET FOMC statement and the 14:30 press conference);
   - midday lull vs the last hour (power hour, market-on-close imbalances);
   - option-expiration days and 0DTE dealer-gamma effects (pinning vs amplification);
   - the day after an H-MOM1-type move, comparing an open entry with the previous close.
2. **Does 0DTE/1DTE implied vol (Cboe VIX1D, single-stock 0DTE) under- or over-price intraday moves,** and in which windows? Is the VRP different intraday than over days?
3. **Structures and exits for same-day longs:** ATM vs OTM 0DTE/1DTE vs weeklies; debit spreads vs single legs. Exits: time-based (e.g. 30/60/120 minutes, before 15:45), first-profit, target/stop, underlying-based invalidation. Gamma/theta behaviour inside the day, and the cost of 0DTE bid-ask spreads.
4. **Data:** which sources give historical **intraday option quotes (NBBO), not just bars,** with IV/Greeks, and from what year? Candidates: ORATS 1-minute (2020+), Databento OPRA, Massive, ThetaData, Cboe DataShop. Which free sources can test anything here (e.g. VIX1D history, Cboe intraday data, any free intraday equity bars)? Test reachability from this container and report blocked hosts by name. Don't fill gaps with guesses.

Method requirements:
- Tier **STANDARD** unless you think it needs DEEP. Show me the brief and worker briefs and wait for my OK before launching anything.
- Before installing or using any third-party skill, search for it, download it into an isolated scratch folder and scan it for security issues, as in `research/2026-11-06-options-swing-backtest-spec/security-scan.md`.
- Separate measured evidence from opinion. Label vendor and educator studies (tastylive, SpotGamma, Option Alpha, etc.) as self-reported, with their setups.
- If free data allows, run a small **pre-registered** intraday study:
  - freeze `study_spec.md` before any run;
  - use a random-time baseline at the same time of day;
  - split in-sample/out-of-sample;
  - use costs at k = 0.70 and k = 1.0 with 0DTE-appropriate spread assumptions;
  - count every cell as a trial, continuing from **#1,538**;
  - judge cells with the stricter bar from the continuation study: OOS excess ≥ 10 points, t ≥ 3, IS same sign, k = 1.0 still positive.
- If free data can't test it, say so plainly. Then deliver a ready-to-run backtest spec and a builder brief for paid intraday chain data, as in the earlier `examples.md` files.

Deliverables, in a new run folder `research/<date>-intraday-long-options/`:
- `brief.md`, `report.md` (answer first: an intraday opportunity table with window, trigger, structure, exit, measured or prior evidence, and status: promising / watch / no edge / avoid / untestable), `sources.md`, `examples.md` (one worked intraday example on one ticker, with real prices where available), and any `study/` scripts and results. Use stdlib Python only, run from the repo root.
- Run claim verification with fresh-context verifiers on every load-bearing number.
- **Don't update the existing artifact.** At the end, offer a separate page.
- Commit and push to the working branch as you go. Keep replies short.
