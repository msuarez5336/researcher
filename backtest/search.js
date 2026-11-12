#!/usr/bin/env node
/* Grid search over option setups with a locked holdout. Run from the repo root, in this order:
 *
 *   node backtest/search.js grid      write backtest/search/grid.json (the cells, fixed before any run)
 *   node backtest/search.js run       run every cell on the SEARCH period -> results.csv
 *   node backtest/search.js select    checks a-g on the search period -> finalists.json, stress.json
 *   node backtest/search.js holdout   run the saved finalists ONCE on the holdout -> holdout.json
 *   node backtest/search.js report    write finalists.md from the saved files
 *
 * Only `holdout` can touch 2021 onwards: every other command goes through runSearch(), which fixes the
 * period. `holdout` reads finalists.json and refuses to run twice; `select` refuses once holdout.json exists.
 */
"use strict";
const fs = require("fs"), path = require("path");
const BT = require("./artifact/engine.js");
const DIR = path.join(__dirname, "search");
const P = (f) => path.join(DIR, f);
const SEARCH = { from: 20091001, to: 20201231 }, HOLDOUT = { from: 20210101, to: 20261231 };
const MIN_TRADES = 300, MIN_MONTHS = 60, NEIGH_T = 2, YEAR_MIN_TRADES = 10, MIN_YEARS = 8, YEAR_SHARE = 0.7;
const MAX_FINALISTS = 10, MAX_PER_SET = 2, IV_BUMP = 10, NEAR_MISSES = 5;

let _ctx = null;
function ctx() {
  if (_ctx) return _ctx;
  const load = (f) => { const t = fs.readFileSync(path.join(__dirname, "artifact", f), "utf8"); return JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1)); };
  return (_ctx = BT.prepare(load("data.js"), load("iv_model.js")));
}
const readJson = (f) => JSON.parse(fs.readFileSync(P(f), "utf8"));
const writeJson = (f, o) => fs.writeFileSync(P(f), JSON.stringify(o, null, 1) + "\n");

// ---------- the grid ----------
function buildGrid() {
  const F = (metric, op, n, values) => ({ metric, op, n, values });
  const families = [
    F("ret", "<=", 1, [-5, -8, -12]), F("ret", "<=", 5, [-10, -15, -20]), F("ret", "<=", 21, [-15, -20, -30]), F("ret", "<=", 63, [-20, -30, -40]),
    F("ret", ">=", 21, [15, 20, 30]), F("ret", ">=", 63, [20, 30, 50]),
    F("move_sigma", "<=", null, [-2.5, -3.5, -5]), F("move_sigma", ">=", null, [2.5, 3.5, 5]),
    F("from_high", "<=", 252, [1, 3, 5]), F("from_high", ">=", 252, [20, 30, 40]), F("from_low", "<=", 252, [2, 5, 10]),
    F("vs_ma", "<=", 50, [-8, -12, -18]), F("vs_ma", "<=", 200, [-10, -20, -30]), F("vs_ma", ">=", 200, [10, 20, 30]),
    F("mom_12_1", ">=", null, [20, 40, 80]), F("mom_12_1", "<=", null, [-10, -20, -30]),
    F("rsi", "<=", 14, [20, 25, 30]), F("rsi", ">=", 14, [70, 75, 80]), F("down_days", ">=", null, [4, 5, 6]),
    F("rel_ret", "<=", 21, [-10, -15, -20]), F("rel_ret", "<=", 63, [-15, -20, -30]), F("rel_ret", ">=", 63, [15, 20, 30])
  ];
  const partners = [null, { id: "calm", cond: { metric: "vix_pctile", op: "<=", value: 33 } }, { id: "fear", cond: { metric: "vix_pctile", op: ">=", value: 67 } },
    { id: "mktdown", cond: { metric: "mkt_ret", op: "<=", value: -5, n: 21 } }];
  const condSets = [];
  families.forEach((f) => {
    const fam = f.metric + (f.n ? f.n : "") + (f.op === "<=" ? "_le" : "_ge");
    f.values.forEach((v) => { const m = BT.METRICS[f.metric]; if (v < m.min || v > m.max) throw new Error("threshold outside range: " + fam + " " + v); });
    partners.forEach((p) => f.values.forEach((v, k) => {
      const c = { metric: f.metric, op: f.op, value: v }; if (f.n) c.n = f.n;
      condSets.push({ id: fam + "_" + k + (p ? "+" + p.id : ""), family: fam, thresholdIndex: k, partner: p ? p.id : "", conds: p ? [c, p.cond] : [c] });
    }));
  });
  const optionCells = [];
  ["call", "put"].forEach((side) => [0.5, 0.35, 0.2].forEach((delta) => [60, 90, 180].forEach((dte) => ["expiry", "half", "x2"].forEach((exit) =>
    optionCells.push({ id: side + "_d" + delta + "_t" + dte + "_" + exit, side, delta, dte, exit })))));
  return { created: new Date().toISOString(), searchPeriod: SEARCH, holdoutPeriod: HOLDOUT,
    note: "Cells are every condSet crossed with every optionCell. All conditions in a set must hold on the same day. vol_ratio is excluded on purpose.",
    N: condSets.length * optionCells.length, condSets, optionCells };
}

// ---------- running ----------
function cfgOf(set, opt, period, extra) {
  return Object.assign({ side: opt.side, delta: opt.delta, dte: opt.dte, exit: BT.EXITS[opt.exit], conds: set.conds, from: period.from, to: period.to }, extra || {});
}
/** The only way non-holdout commands run the engine: the period cannot be passed in. */
function runSearch(set, opt, extra) { return BT.run(ctx(), cfgOf(set, opt, SEARCH, extra)); }
function figures(r) {
  const ys = r.years.filter((y) => y.condN >= YEAR_MIN_TRADES && y.baseMean != null);
  return { trades: r.cond.n, months: r.excess.months, mean: r.cond.n ? r.cond.mean : null, median: r.cond.n ? r.cond.median : null, lost: r.cond.n ? r.cond.lost : null,
    baseN: r.base.n, baseMean: r.base.n ? r.base.mean : null, baseLost: r.base.n ? r.base.lost : null,
    excess: r.excess.mean, t: r.excess.t, tAdj: r.excess.tAdj, yearsCounted: ys.length, yearsPositive: ys.filter((y) => y.condMean - y.baseMean > 0).length };
}
const COLS = ["cell", "set", "family", "threshold_index", "partner", "side", "delta", "dte", "exit", "status", "trades", "months", "mean", "median", "lost",
  "base_n", "base_mean", "base_lost", "excess", "t", "tAdj", "years_counted", "years_positive", "setup"];
const num = (x, d) => x == null || x !== x ? "" : (+x.toFixed(d == null ? 5 : d)).toString();

function cmdGrid() {
  fs.mkdirSync(DIR, { recursive: true });
  if (fs.existsSync(P("results.csv"))) throw new Error("results.csv already exists; the grid is fixed. Delete backtest/search/ to start over.");
  const g = buildGrid(); writeJson("grid.json", g);
  console.log(`grid.json: ${g.condSets.length} condition sets x ${g.optionCells.length} option cells = ${g.N} cells`);
}

function cmdRun() {
  const g = readJson("grid.json"), out = fs.openSync(P("results.csv"), "w"), t0 = Date.now();
  fs.writeSync(out, COLS.join(",") + "\n");
  let done = 0;
  g.optionCells.forEach((opt) => {
    let baseTrades = null, buf = "";
    g.condSets.forEach((set) => {
      const head = [set.id + "|" + opt.id, set.id, set.family, set.thresholdIndex, set.partner, opt.side, opt.delta, opt.dte, opt.exit];
      const desc = '"' + set.conds.map(BT.describe).join(" AND ") + '"';
      let row;
      try {
        const r = runSearch(set, opt, baseTrades ? { baseTrades } : null), f = figures(r);
        baseTrades = r.baseTrades;
        row = head.concat([f.trades ? "ok" : "no_trades", f.trades, f.months, num(f.mean), num(f.median), num(f.lost), f.baseN, num(f.baseMean), num(f.baseLost),
          num(f.excess), num(f.t, 4), num(f.tAdj, 4), f.yearsCounted, f.yearsPositive, desc]);
      } catch (e) {
        row = head.concat(["error: " + String(e.message).replace(/[",\n]/g, " "), "", "", "", "", "", "", "", "", "", "", "", "", "", desc]);
      }
      buf += row.join(",") + "\n"; done++;
    });
    fs.writeSync(out, buf);
    console.log(`${opt.id}  ${done}/${g.N}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  });
  fs.closeSync(out);
}

function readResults() {
  const lines = fs.readFileSync(P("results.csv"), "utf8").trim().split("\n"), cols = lines[0].split(",");
  const numeric = { trades: 1, months: 1, mean: 1, median: 1, lost: 1, base_n: 1, base_mean: 1, base_lost: 1, excess: 1, t: 1, tAdj: 1, years_counted: 1, years_positive: 1, delta: 1, dte: 1, threshold_index: 1 };
  return lines.slice(1).map((ln) => {
    const q = ln.indexOf('"'), parts = ln.slice(0, q - 1).split(","), o = {};
    parts.push(ln.slice(q + 1, -1));
    cols.forEach((c, k) => { o[c] = numeric[c] ? (parts[k] === "" ? null : +parts[k]) : parts[k]; });
    return o;
  });
}

// ---------- checks a-d, from results.csv alone ----------
function basicChecks(rows, N) {
  const bar = BT.ninv(1 - 0.025 / N), by = {};
  rows.forEach((r) => { by[r.cell] = r; });
  rows.forEach((r) => {
    const opt = r.cell.split("|")[1];
    const neigh = [r.threshold_index - 1, r.threshold_index + 1].filter((k) => k >= 0 && k <= 2)
      .map((k) => by[r.family + "_" + k + (r.partner ? "+" + r.partner : "") + "|" + opt]);
    r.neighbours = neigh.map((n) => ({ cell: n.cell, excess: n.excess, tAdj: n.tAdj }));
    r.a = r.trades >= MIN_TRADES && r.months >= MIN_MONTHS;
    r.b = r.tAdj != null && r.tAdj >= bar;
    r.c = r.excess != null && neigh.every((n) => n.excess != null && n.tAdj != null && Math.sign(n.excess) === Math.sign(r.excess) && n.tAdj >= NEIGH_T);
    r.d = r.years_counted >= MIN_YEARS && r.years_positive / r.years_counted >= YEAR_SHARE;
  });
  return bar;
}

// ---------- checks e-g, extra runs on the search period ----------
function stress(row, g) {
  const set = g.condSets.find((s) => s.id === row.set), opt = g.optionCells.find((o) => o.id === row.cell.split("|")[1]), data = ctx().data;
  const base = runSearch(set, opt);
  const sectors = Array.from(new Set(data.tickers.map((t) => data.sector[t]))).sort();
  const bySector = sectors.map((s) => {
    const r = runSearch(set, opt, { tickers: data.tickers.filter((t) => data.sector[t] !== s) });
    return { removed: s, trades: r.cond.n, excess: r.excess.mean };
  });
  const fill = runSearch(set, opt, { fill: 1 });
  // Setup trades pay for 10 more volatility points at entry; ordinary-day trades keep the default estimate.
  const vol = runSearch(set, opt, { ivEntryAdd: IV_BUMP, baseTrades: base.baseTrades });
  const worst = bySector.reduce((p, q) => (q.excess < p.excess ? q : p));
  return { cell: row.cell, excess: base.excess.mean, sectors: bySector, worstSector: worst, fillFull: { excess: fill.excess.mean, tAdj: fill.excess.tAdj },
    volBump: { excess: vol.excess.mean, tAdj: vol.excess.tAdj, mean: vol.cond.mean },
    e: bySector.every((s) => s.excess > 0), f: fill.excess.mean > 0, g: vol.excess.mean > 0 };
}
const pick = (r) => ({ cell: r.cell, set: r.set, family: r.family, partner: r.partner, side: r.side, delta: r.delta, dte: r.dte, exit: r.exit, setup: r.setup,
  trades: r.trades, months: r.months, mean: r.mean, median: r.median, lost: r.lost, baseMean: r.base_mean, baseLost: r.base_lost, excess: r.excess, t: r.t, tAdj: r.tAdj,
  yearsCounted: r.years_counted, yearsPositive: r.years_positive, neighbours: r.neighbours, checks: { a: r.a, b: r.b, c: r.c, d: r.d } });
function capPerSet(list, max) {
  const seen = {}, out = [];
  list.forEach((r) => { seen[r.set] = (seen[r.set] || 0) + 1; if (seen[r.set] <= MAX_PER_SET && out.length < max) out.push(r); });
  return out;
}

function cmdSelect() {
  if (fs.existsSync(P("holdout.json"))) throw new Error("holdout.json exists: the holdout has been run, so finalists can no longer be re-selected.");
  const g = readJson("grid.json"), rows = readResults();
  if (rows.length !== g.N) throw new Error(`results.csv has ${rows.length} rows, grid has ${g.N}`);
  const bar = basicChecks(rows, g.N);
  const cnt = (f) => rows.filter(f).length;
  const funnel = { N: g.N, bar, ok: cnt((r) => r.status === "ok"), noTrades: cnt((r) => r.status === "no_trades"), errors: cnt((r) => r.status.startsWith("error")),
    a: cnt((r) => r.a), ab: cnt((r) => r.a && r.b), abNegative: cnt((r) => r.a && r.tAdj != null && r.tAdj <= -bar), abc: cnt((r) => r.a && r.b && r.c), abcd: cnt((r) => r.a && r.b && r.c && r.d) };
  const byT = (p, q) => q.tAdj - p.tAdj;
  const cands = rows.filter((r) => r.a && r.b && r.c && r.d).sort(byT);
  const tested = cands.map((r) => { const s = stress(r, g); console.log("stress", r.cell, s.e, s.f, s.g); return Object.assign(pick(r), { stress: s, checks: Object.assign(pick(r).checks, { e: s.e, f: s.f, g: s.g }) }); });
  const passAll = tested.filter((r) => r.stress.e && r.stress.f && r.stress.g);
  funnel.abcde = tested.filter((r) => r.stress.e).length; funnel.abcdefg = passAll.length;
  const finalists = capPerSet(passAll, MAX_FINALISTS);
  funnel.finalists = finalists.length;
  // Closest failures: cells with enough trades and a positive excess that are not finalists, ordered by how many
  // of checks b, c, d they pass, then by tAdj. Cells that passed a-d but failed e-g come first.
  const isFinal = {}; finalists.forEach((r) => { isFinal[r.cell] = 1; });
  const failedLate = tested.filter((r) => !(r.stress.e && r.stress.f && r.stress.g));
  const score = (r) => (r.b ? 1 : 0) + (r.c ? 1 : 0) + (r.d ? 1 : 0);
  const rest = rows.filter((r) => r.a && r.excess > 0 && r.tAdj != null && !(r.b && r.c && r.d)).sort((p, q) => score(q) - score(p) || byT(p, q));
  const near = capPerSet(failedLate.concat(capPerSet(rest, 50).map(pick)), NEAR_MISSES).map((r) => {
    if (!r.stress) { r.stress = stress(rows.find((x) => x.cell === r.cell), g); Object.assign(r.checks, { e: r.stress.e, f: r.stress.f, g: r.stress.g }); console.log("near miss", r.cell); }
    return r;
  });
  writeJson("stress.json", { note: "Checks e-g for every cell that passed a-d, and the closest failures. Search period only.", passedAtoD: tested, nearMisses: near });
  writeJson("finalists.json", { created: new Date().toISOString(), searchPeriod: SEARCH, N: g.N, bar, funnel, finalists });
  console.log(JSON.stringify(funnel));
}

function cmdHoldout() {
  if (fs.existsSync(P("holdout.json"))) throw new Error("holdout.json exists: the holdout is run once only.");
  const fin = readJson("finalists.json"), g = readJson("grid.json");
  const results = fin.finalists.map((f) => {
    const set = g.condSets.find((s) => s.id === f.set), opt = g.optionCells.find((o) => o.id === f.cell.split("|")[1]);
    const r = BT.run(ctx(), cfgOf(set, opt, HOLDOUT));
    return Object.assign({ cell: f.cell, range: r.range, years: r.years }, figures(r));
  });
  writeJson("holdout.json", { created: new Date().toISOString(), holdoutPeriod: HOLDOUT, results });
  console.log(`holdout run for ${results.length} finalist(s)`);
}

// ---------- report ----------
function cmdReport() {
  const g = readJson("grid.json"), fin = readJson("finalists.json"), st = readJson("stress.json"), rows = readResults();
  const hold = fs.existsSync(P("holdout.json")) ? readJson("holdout.json") : null;
  const bar = basicChecks(rows, g.N), fu = fin.funnel;
  const pc = (x) => x == null ? "n/a" : (x >= 0 ? "+" : "−") + Math.abs(x * 100).toFixed(1) + "%";
  const sh = (x) => x == null ? "n/a" : (x * 100).toFixed(0) + "%";
  const tt = (x) => x == null ? "n/a" : x.toFixed(2).replace("-", "−");
  const optWords = (r) => `${r.side}, delta ${r.delta}, ${r.dte} days, ${{ expiry: "held to expiry", half: "sold at half-life", x2: "sold at double or held to expiry" }[r.exit]}`;
  const cnt = (f) => rows.filter(f).length;
  const t2 = cnt((r) => r.a && r.tAdj >= 2), tm2 = cnt((r) => r.a && r.tAdj <= -2), nA = cnt((r) => r.a);
  const failed = (c) => "abcdefg".split("").filter((k) => c[k] === false).join(", ") || "none";
  const L = [];
  L.push("# Option setup grid search: finalists", "");
  L.push(`Written by \`node backtest/search.js report\` from \`results.csv\`, \`finalists.json\`, \`stress.json\` and \`holdout.json\`. Grid fixed ${g.created.slice(0, 10)}; search period ${SEARCH.from} to ${SEARCH.to}; holdout ${HOLDOUT.from} onwards.`, "");
  L.push("## The short answer", "");
  L.push(fin.finalists.length
    ? `${fin.finalists.length} cell(s) passed all seven checks on the search period. Their holdout figures are in the table below. They are candidates for checking on real option prices, not evidence of profit.`
    : `**No setup passed all seven checks.** Of ${fu.N} combinations tried on ${SEARCH.from}–${SEARCH.to}, none made buying options reliably better than buying the same option on ordinary days by the standard set in advance. Because there were no finalists, nothing was run on the holdout.`, "");
  L.push("## What was tried", "");
  L.push(`- **${fu.N} cells**: ${g.condSets.length} setups (66 single conditions, and each of them combined with a calm market, a fearful market, or a market that fell 5% in a month) × ${g.optionCells.length} option choices (call or put; delta 0.5, 0.35, 0.2; 60, 90 or 180 days; held to expiry, sold at half-life, or sold on doubling).`);
  L.push(`- ${fu.ok} cells produced trades, ${fu.noTrades} had no trades, ${fu.errors} failed to run. No threshold had to be adjusted.`);
  L.push(`- **The bar**: a tAdj of **${bar.toFixed(2)}** or more. tAdj measures how far the setup's average return sits above the ordinary-day average, in units of its own noise, after allowing for overlapping trades. A single test usually uses about 2; trying ${fu.N} combinations needs ${bar.toFixed(2)} to keep the chance of even one lucky pass at about 5%.`, "");
  L.push("## How many cleared each check", "");
  L.push("| Check | Cells passing |", "|---|---|");
  L.push(`| a. at least ${MIN_TRADES} trades over at least ${MIN_MONTHS} months | ${fu.a} |`);
  L.push(`| a and b. also tAdj ≥ ${bar.toFixed(2)} | ${fu.ab} |`);
  L.push(`| a–c. also neighbouring thresholds agree (same sign, tAdj ≥ ${NEIGH_T}) | ${fu.abc} |`);
  L.push(`| a–d. also positive in ≥ ${YEAR_SHARE * 100}% of years, with ≥ ${MIN_YEARS} usable years | ${fu.abcd} |`);
  L.push(`| a–e. also positive with any one sector removed | ${fu.abcde} |`);
  L.push(`| a–g. also positive paying the whole spread, and with volatility +${IV_BUMP} points at entry | ${fu.abcdefg} |`);
  L.push(`| Finalists kept (at most ${MAX_FINALISTS}, at most ${MAX_PER_SET} per setup) | ${fu.finalists} |`, "");
  L.push(`**Expected by chance.** If no setup had any real effect and the cells were independent, about ${(0.025 * 1).toFixed(3)} cells in total would clear the bar on the upside (${(0.05).toFixed(2)} counting both directions), so effectively none. ${fu.ab} cleared it on the upside and ${fu.abNegative} were as far below ordinary days as the bar is above.`);
  L.push(`For scale, with the usual single-test threshold of 2: ${t2} of the ${nA} cells that passed check a had tAdj ≥ 2 and ${tm2} had tAdj ≤ −2; chance alone would give about ${(nA * (1 - BT.ncdf(2))).toFixed(0)} each way. The cells are far from independent (the same trades appear in many of them), so these counts are a rough guide only.`, "");

  const hBy = {}; if (hold) hold.results.forEach((h) => { hBy[h.cell] = h; });
  L.push("## Finalists", "");
  if (!fin.finalists.length) L.push("None.", "");
  else {
    L.push("Each row pair is one finalist: search period first, holdout second. \"Excess\" is the setup's average return minus the ordinary-day average of the same calendar year. \"Lost everything\" is the share of trades that lost at least 99% of the premium.", "");
    L.push("| # | Setup | Option | Period | Trades | Average return | Ordinary-day average | Excess | tAdj | Lost everything |", "|---|---|---|---|---|---|---|---|---|---|");
    fin.finalists.forEach((f, k) => {
      const h = hBy[f.cell];
      L.push(`| ${k + 1} | ${f.setup} | ${optWords(f)} | search | ${f.trades} | ${pc(f.mean)} | ${pc(f.baseMean)} | ${pc(f.excess)} | ${tt(f.tAdj)} | ${sh(f.lost)} |`);
      L.push(h ? `| | | | holdout | ${h.trades} | ${pc(h.mean)} | ${pc(h.baseMean)} | ${pc(h.excess)} | ${tt(h.tAdj)} | ${sh(h.lost)} |` : "| | | | holdout | not run | | | | | |");
    });
    L.push("", "### Checks passed only narrowly", "");
    L.push(`"Narrow" here means: fewer than ${Math.round(MIN_TRADES * 1.2)} trades or ${Math.round(MIN_MONTHS * 1.2)} months; tAdj within 10% of the bar; a neighbour's tAdj under 2.5; positive years under 80% or only ${MIN_YEARS}–${MIN_YEARS + 1} usable years; or a stress test (sector removed, whole spread paid, volatility +${IV_BUMP}) that leaves less than half of the excess.`, "");
    fin.finalists.forEach((f, k) => {
      const n = [], s = f.stress;
      if (f.trades < MIN_TRADES * 1.2 || f.months < MIN_MONTHS * 1.2) n.push(`a (${f.trades} trades, ${f.months} months)`);
      if (f.tAdj < bar * 1.1) n.push(`b (tAdj ${tt(f.tAdj)})`);
      const wn = Math.min.apply(null, f.neighbours.map((x) => x.tAdj)); if (wn < 2.5) n.push(`c (neighbour tAdj ${tt(wn)})`);
      if (f.yearsPositive / f.yearsCounted < 0.8 || f.yearsCounted <= MIN_YEARS + 1) n.push(`d (${f.yearsPositive} of ${f.yearsCounted} years positive)`);
      if (s.worstSector.excess < f.excess / 2) n.push(`e (excess ${pc(s.worstSector.excess)} without ${s.worstSector.removed})`);
      if (s.fillFull.excess < f.excess / 2) n.push(`f (excess ${pc(s.fillFull.excess)} paying the whole spread)`);
      if (s.volBump.excess < f.excess / 2) n.push(`g (excess ${pc(s.volBump.excess)} with volatility +${IV_BUMP} at entry)`);
      L.push(`${k + 1}. ${f.setup} — ${optWords(f)}: ${n.length ? n.join("; ") : "none narrow"}.`);
    });
    L.push("");
  }
  const extra = st.passedAtoD.length - fin.finalists.length;
  if (st.passedAtoD.length) L.push(`${st.passedAtoD.length} cell(s) passed checks a–d and were put through e–g; ${extra} of them are not finalists (failed e–g or dropped by the per-setup cap). Details are in \`stress.json\`.`, "");

  L.push("## Closest failures", "");
  L.push(`The ${st.nearMisses.length} cells that came closest: cells that passed a–d but failed a later check first, then cells with enough trades and a positive excess, ordered by how many of checks b, c, d they passed and then by tAdj (at most ${MAX_PER_SET} per setup). Checks e–g were run for these too. All figures are from the search period.`, "");
  L.push("| Setup | Option | Trades | Average return | Ordinary-day average | Excess | tAdj | Lost everything | Years positive | Excess, whole spread | Excess, volatility +" + IV_BUMP + " | Worst excess with one sector removed | Checks failed |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|");
  st.nearMisses.forEach((f) => {
    const s = f.stress;
    L.push(`| ${f.setup} | ${optWords(f)} | ${f.trades} | ${pc(f.mean)} | ${pc(f.baseMean)} | ${pc(f.excess)} | ${tt(f.tAdj)} | ${sh(f.lost)} | ${f.yearsPositive} of ${f.yearsCounted} | ${pc(s.fillFull.excess)} | ${pc(s.volBump.excess)} | ${pc(s.worstSector.excess)} (${s.worstSector.removed}) | ${failed(f.checks)} |`);
  });
  L.push("", "Check letters: a enough trades and months; b tAdj at the bar; c neighbouring thresholds agree; d consistent across years; e survives removing any sector; f survives paying the whole spread; g survives higher volatility at entry.", "");
  const best = rows.filter((r) => r.a && r.tAdj != null).sort((p, q) => q.tAdj - p.tAdj)[0], worst = rows.filter((r) => r.a && r.tAdj != null).sort((p, q) => p.tAdj - q.tAdj)[0];
  L.push(`Highest tAdj among cells with enough trades: ${tt(best.tAdj)} (${best.setup}; ${optWords(best)}). Lowest: ${tt(worst.tAdj)} (${worst.setup}; ${optWords(worst)}).`, "");

  L.push("## What this does and does not show", "");
  L.push("- **Option prices are estimates.** No real option quotes were used. Prices come from a formula fed with a volatility estimated from each stock's recent swings and the VIX. A result here ranks ideas; it does not show what a real trade would have paid or returned.");
  L.push("- **The stocks are survivors and recent winners.** The 200 stocks are 2026 S&P 500 members chosen by 2026 trading activity. Companies that failed or shrank are missing, which flatters calls.");
  L.push("- **No earnings dates.** Real options cost more ahead of earnings; the estimate does not know when earnings fall.");
  L.push("- **After sharp falls the estimate is too cheap.** Real option prices jump faster than the estimate, which flatters fall-and-rebound setups. Check g probes this but does not correct it.");
  L.push("- **The holdout is not perfectly fresh.** The owner has already looked at 2021–2026 on the page for the one-day-fall setup, so for that setup the holdout is not an untouched test.");
  L.push("- **Search-period trades run past the period's end.** A trade entered in late 2020 is closed in 2021, so the last few months of search-period trades use early-2021 prices. Holdout trades are separate trades entered from 2021.");
  L.push("- **Stress test g** raises volatility by " + IV_BUMP + " points at entry for the setup trades only; the ordinary-day trades keep the default estimate.");
  L.push("- A finalist is a candidate for checking on real option prices, not evidence of profit. \"None found\" means none met this standard on estimated prices, not that no setup can work. Nothing here is trading advice.", "");
  fs.writeFileSync(P("finalists.md"), L.join("\n"));
  console.log("wrote finalists.md");
}

const cmd = process.argv[2];
const cmds = { grid: cmdGrid, run: cmdRun, select: cmdSelect, holdout: cmdHoldout, report: cmdReport };
if (!cmds[cmd]) { console.error("usage: node backtest/search.js grid|run|select|holdout|report"); process.exit(2); }
cmds[cmd]();
