#!/usr/bin/env node
/* Tests for backtest/artifact/engine.js. Run from the repo root: node backtest/test_engine.js */
"use strict";
const BT = require("./artifact/engine.js");
let failed = 0;
function ok(name, cond, detail) { if (!cond) failed++; console.log((cond ? "ok   " : "FAIL ") + name + (detail ? "  " + detail : "")); }
const near = (a, b, tol) => Math.abs(a - b) <= tol;

// --- pricing against textbook values ---
ok("call S=K=100 T=1 r=5% vol=20% is 10.4506", near(BT.bs(100, 100, 1, 0.2, 0.05, 1), 10.4506, 0.005), BT.bs(100, 100, 1, 0.2, 0.05, 1).toFixed(4));
ok("put  S=K=100 T=1 r=5% vol=20% is 5.5735", near(BT.bs(100, 100, 1, 0.2, 0.05, -1), 5.5735, 0.005));
{ const c = BT.bs(120, 100, 0.5, 0.35, 0.03, 1), p = BT.bs(120, 100, 0.5, 0.35, 0.03, -1);
  ok("put-call parity", near(c - p, 120 - 100 * Math.exp(-0.015), 1e-4)); }
ok("expired option pays intrinsic value", BT.bs(110, 100, 0, 0.3, 0, 1) === 10 && BT.bs(90, 100, 0, 0.3, 0, 1) === 0);
for (const [cp, d] of [[1, 0.5], [1, 0.2], [-1, 0.35]]) {
  const K = BT.strikeForDelta(100, 0.25, 0.4, 0.02, cp, d);
  ok(`strike for ${cp > 0 ? "call" : "put"} delta ${d}`, near(Math.abs(BT.delta(100, K, 0.25, 0.4, 0.02, cp)), d, 1e-4), "K=" + K.toFixed(2));
}

// --- synthetic data helpers ---
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function gauss(u) { return Math.sqrt(-2 * Math.log(u() + 1e-12)) * Math.cos(2 * Math.PI * u()); }
function makeData(nDays, nTk, seed, driftAfterDrop) {
  const u = rng(seed), dates = [], close = {}, tickers = [];
  let y = 2010, m = 1, d = 1;
  for (let i = 0; i < nDays; i++) { dates.push(y * 10000 + m * 100 + d); d++; if (d > 21) { d = 1; m++; if (m > 12) { m = 1; y++; } } }
  for (let t = 0; t < nTk; t++) {
    const tk = "T" + t, c = [100]; let boost = 0;
    for (let i = 1; i < nDays; i++) {
      let r = 0.02 * gauss(u);
      if (u() < 0.004) r = -0.12;                       // occasional sharp fall
      if (boost > 0) { r += driftAfterDrop; boost--; }
      if (r <= -0.1) boost = 60;
      c.push(c[i - 1] * Math.exp(r));
    }
    close[tk] = c; tickers.push(tk);
  }
  const flat = (v) => new Array(nDays).fill(v);
  const sector = {}, group = {}; tickers.forEach((t, k) => { sector[t] = k % 2 ? "Energy" : "Financials"; group[t] = "G" + (k % 3); });
  return { dates, tickers, close, sector, group, spy: close[tickers[0]].map((x) => x / 2), vix: flat(20), vix3m: flat(21), vix6m: flat(22), rate: flat(2), volIndex: {} };
}
const IV = { coef: { a: 4.87, rv20: 0, rv60: 0.505, vix: 0.618 } };
const base = { side: "call", delta: 0.35, dte: 90, exit: { type: "expiry" }, spread: 8, fill: 0.75, lag: 1,
               conds: [{ metric: "ret", op: "<=", value: -8, n: 1 }], gap: 10, baseStep: 5,
               from: 20100101, to: 20991231 };

// --- held-to-expiry trade pays intrinsic value on the expiry-day close ---
{ const data = makeData(1500, 1, 7, 0), ctx = BT.prepare(data, IV), f = BT.features(ctx, "T0");
  const t = BT.trade(ctx, f, 400, base);
  const intrinsic = Math.max(f.close[t.exit] - t.K, 0);
  ok("hold to expiry: return equals intrinsic / cost - 1", near(t.ret, intrinsic / t.cost - 1, 1e-12));
  ok("entry is the day after the signal", t.entry === 401 && t.exit === 401 + Math.round(90 * 252 / 365));
  const mid = t.cost / (1 + 0.08 / 2 * 0.75);
  ok("entry cost is mid plus 75% of half the spread", near(mid, BT.bs(t.S, t.K, 90 / 365, t.iv, 0.02, 1), 1e-9));
  const t0 = BT.trade(ctx, f, 400, Object.assign({}, base, { fill: 0 }));
  ok("paying the spread lowers the return", t.ret < t0.ret || (t.ret === -1 && t0.ret === -1));
}

// --- no information from the future ---
{ const data = makeData(1500, 3, 11, 0), ctx = BT.prepare(data, IV);
  const cut = 900, r1 = BT.run(ctx, base);
  const data2 = JSON.parse(JSON.stringify(data));
  for (const tk of data2.tickers) for (let i = cut + 1; i < 1500; i++) data2.close[tk][i] *= 1.5 + (i % 7) / 10;
  const r2 = BT.run(BT.prepare(data2, IV), base);
  const key = (t) => [t.tk, t.sig, t.K.toFixed(6), t.cost.toFixed(6)].join("|");
  const before = (r) => r.trades.filter((t) => t.entry <= cut).map(key).join(";");
  ok("changing prices after day N leaves signals, strikes and costs up to N unchanged", before(r1) === before(r2) && before(r1).length > 0);
  const done = (r) => r.trades.filter((t) => t.exit <= cut).map((t) => key(t) + "|" + t.ret.toFixed(9)).join(";");
  ok("...and leaves the returns of trades that ended by day N unchanged", done(r1) === done(r2) && done(r1).length > 0);
}

// --- a planted effect is found, and no effect is not ---
{ const planted = BT.run(BT.prepare(makeData(4000, 30, 3, 0.004), IV), base);
  ok("planted rebound after sharp falls is detected", planted.excess.mean > 0.2 && planted.excess.tAdj > 3,
     `excess ${(planted.excess.mean * 100).toFixed(0)} pts, adj t ${planted.excess.tAdj.toFixed(1)}, n ${planted.cond.n}`);
  const none = BT.run(BT.prepare(makeData(4000, 30, 3, 0), IV), base);
  ok("no planted effect gives an adjusted t-statistic below 3", Math.abs(none.excess.tAdj) < 3,
     `excess ${(none.excess.mean * 100).toFixed(0)} pts, adj t ${none.excess.tAdj.toFixed(1)}, n ${none.cond.n}`);
}

// --- exits ---
{ const data = makeData(1500, 2, 5, 0), ctx = BT.prepare(data, IV);
  const half = BT.run(ctx, Object.assign({}, base, { exit: { type: "days", frac: 0.5 } }));
  ok("fixed-period exit leaves after half the option's life", half.trades.every((t) => t.exit - t.entry === Math.round(Math.round(90 * 252 / 365) * 0.5)));
  const tgt = BT.run(ctx, Object.assign({}, base, { exit: { type: "target", mult: 2 }, conds: [] }));
  const early = tgt.trades.length === 0;   // no conditions gives no setup trades; check the baseline instead
  ok("target exit runs and the baseline has trades", early && tgt.base.n > 100);
}

// --- condition measures against brute force ---
{ const data = makeData(900, 2, 21, 0), ctx = BT.prepare(data, IV), f = BT.features(ctx, "T1"), M = BT.METRICS;
  let okHi = true, okLo = true, okMa = true, okRsi = true;
  for (const i of [260, 400, 555, 899]) {
    const w = Array.from(f.close.slice(i - 251, i + 1)), w50 = Array.from(f.close.slice(i - 49, i + 1));
    okHi = okHi && near(M.from_high.get(ctx, f, i, 252), (1 - f.close[i] / Math.max(...w)) * 100, 1e-9);
    okLo = okLo && near(M.from_low.get(ctx, f, i, 252), (f.close[i] / Math.min(...w) - 1) * 100, 1e-9);
    okMa = okMa && near(M.vs_ma.get(ctx, f, i, 50), (f.close[i] / (w50.reduce((p, q) => p + q, 0) / 50) - 1) * 100, 1e-9);
    const r = M.rsi.get(ctx, f, i, 14); okRsi = okRsi && r >= 0 && r <= 100;
  }
  ok("distance from 52-week high matches brute force", okHi); ok("distance from 52-week low matches brute force", okLo);
  ok("distance from 50-day average matches brute force", okMa); ok("RSI stays between 0 and 100", okRsi);
  const two = BT.run(ctx, Object.assign({}, base, { conds: [{ metric: "ret", op: "<=", value: -8, n: 1 }, { metric: "from_low", op: "<=", value: 5, n: 252 }] }));
  const one = BT.run(ctx, base);
  ok("adding a second condition never adds trades", two.cond.n <= one.cond.n && one.cond.n > 0, `${one.cond.n} -> ${two.cond.n}`);
}

// --- reading a setup from untrusted input ---
{ const data = makeData(300, 4, 2, 0);
  const s = BT.sanitize({ conditions: [{ metric: "ret", op: "<=", value: -1e9, n: 99999 }, { metric: "<script>", op: "<=", value: 1 }, { metric: "rsi", op: "between", value: 30 },
      { metric: "vix_pctile", op: ">=", value: "67" }],
    option: { side: "sideways", delta: 0.3, dte: 100, exit: "rm -rf" }, population: { sectors: ["Energy", "Nonsense"], tickers: ["T1", "ZZZZ"] }, note: "x".repeat(900) }, data);
  ok("unknown metrics and operators are dropped", s.conds.length === 2 && s.dropped.length === 2);
  ok("numbers are clamped to each measure's range", s.conds[0].value === -90 && s.conds[0].n === 252);
  ok("option fields snap to allowed values or are ignored", s.option.side === undefined && s.option.delta === 0.35 && s.option.dte === 90 && s.option.exit === undefined);
  ok("population keeps only known sectors and stocks", s.population.sectors.join() === "Energy" && s.population.tickers.join() === "T1");
  ok("notes are length-limited", s.note.length === 400);
  ok("garbage input gives an empty setup", BT.sanitize("hello", data).conds.length === 0 && BT.sanitize(null, data).conds.length === 0);
  ok("plain-language description", BT.describe({ metric: "ret", op: "<=", value: -20, n: 20 }) === "fell 20% or more in a month" &&
     BT.describe({ metric: "from_low", op: "<=", value: 5, n: 252 }) === "within 5% of its 52-week low", BT.describe({ metric: "ret", op: "<=", value: -20, n: 20 }));
}

// --- optional parameters used by backtest/search.js ---
{ const data = makeData(1500, 4, 5, 0), ctx = BT.prepare(data, IV);
  const full = BT.run(ctx, base);
  const again = BT.run(ctx, Object.assign({}, base, { baseTrades: full.baseTrades }));
  ok("reusing a saved baseline gives the same result", again.base.n === full.base.n && again.base.mean === full.base.mean && again.cond.n === full.cond.n &&
     again.excess.mean === full.excess.mean && again.excess.tAdj === full.excess.tAdj && JSON.stringify(again.years) === JSON.stringify(full.years));
  const f = BT.features(ctx, "T0"), cfgH = Object.assign({}, base, { exit: { type: "days", frac: 0.5 } });
  const t = BT.trade(ctx, f, 400, cfgH), tb = BT.trade(ctx, f, 400, Object.assign({}, cfgH, { ivEntryAdd: 10 }));
  ok("entry-only volatility bump raises the entry volatility and cost", tb.iv > t.iv + 0.05 && tb.cost > t.cost, `${t.iv.toFixed(3)} -> ${tb.iv.toFixed(3)}`);
  const half = 0.08 / 2 * 0.75, left = 90 - (tb.exit - tb.entry) * 365 / 252;
  const vx = BT.estIV(ctx, f, tb.exit, left, tb.Sx, tb.K, BT.IV_DEFAULT);
  ok("entry-only volatility bump leaves the exit price on the unbumped estimate", near((tb.ret + 1) * tb.cost, BT.bs(tb.Sx, tb.K, left / 365, vx, 0.02, 1) * (1 - half), 1e-9));
  ok("no bump by default", BT.trade(ctx, f, 400, Object.assign({}, cfgH, { ivEntryAdd: 0 })).ret === t.ret);
}

console.log(failed ? `\n${failed} FAILED` : "\nall passed");
process.exit(failed ? 1 : 0);
