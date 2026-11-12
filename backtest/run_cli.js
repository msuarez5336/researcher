#!/usr/bin/env node
/* Run one configuration from the command line: node backtest/run_cli.js '{"cond":{"metric":"ret1","x":8}}' */
"use strict";
const fs = require("fs"), path = require("path");
const BT = require("./artifact/engine.js");
const load = (f) => { const t = fs.readFileSync(path.join(__dirname, "artifact", f), "utf8"); return JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1)); };
const ctx = BT.prepare(load("data.js"), load("iv_model.js"));
const cfg = Object.assign({ side: "call", delta: 0.35, dte: 90, exit: { type: "expiry" }, spread: 8, fill: 0.75, lag: 1,
  iv: { premium: 0, term: true, skew: true }, cond: { metric: "none" }, vix: "any", gap: 10, baseStep: 5,
  from: 20091001, to: 20201231 }, JSON.parse(process.argv[2] || "{}"));
const t0 = Date.now(), r = BT.run(ctx, cfg), ms = Date.now() - t0;
const pc = (x) => x == null ? "  n/a" : (x * 100).toFixed(1).padStart(7) + "%";
const row = (name, s) => console.log(name.padEnd(10), String(s.n).padStart(6), pc(s.mean), pc(s.median), pc(s.lost), pc(s.win), pc(s.x2), pc(s.x5));
console.log(`${r.range[0]}..${r.range[1]}  ${ms} ms`);
console.log("".padEnd(10), "     n", "   mean", " median", "  lost", "   win", "  >=2x", "  >=5x");
row("condition", r.cond); row("baseline", r.base);
console.log("excess vs same-year baseline:", pc(r.excess.mean), " t:", r.excess.t && r.excess.t.toFixed(2), " overlap-adjusted t:", r.excess.tAdj && r.excess.tAdj.toFixed(2), " months:", r.excess.months);
