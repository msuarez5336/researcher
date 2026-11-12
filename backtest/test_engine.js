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
  return { dates, tickers, close, vix: flat(20), vix3m: flat(21), vix6m: flat(22), rate: flat(2), volIndex: {} };
}
const IV = { coef: { a: 4.87, rv20: 0, rv60: 0.505, vix: 0.618 } };
const base = { side: "call", delta: 0.35, dte: 90, exit: { type: "expiry" }, spread: 8, fill: 0.75, lag: 1,
               iv: { premium: 0, term: true, skew: true }, cond: { metric: "ret1", x: 8 }, vix: "any", gap: 10, baseStep: 5,
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
  const tgt = BT.run(ctx, Object.assign({}, base, { exit: { type: "target", mult: 2 }, cond: { metric: "none" } }));
  const early = tgt.trades.length === 0;   // metric none gives no condition trades; check on baseline summary instead
  ok("target exit runs and the baseline has trades", early && tgt.base.n > 100);
}

console.log(failed ? `\n${failed} FAILED` : "\nall passed");
process.exit(failed ? 1 : 0);
