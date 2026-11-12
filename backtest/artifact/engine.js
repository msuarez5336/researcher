/* Option backtest engine on estimated prices. Runs in the browser (window.BT) and in Node (module.exports).
 *
 * Everything a signal reads on day i uses closes up to and including day i. Entry is at the close of
 * day i + lag. Option prices come from Black-Scholes with an implied volatility ESTIMATED from the
 * stock's realised volatility and the VIX (see calibrate_iv.py); no real option quotes are used.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.BT = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // ---------- maths ----------
  function ncdf(x) {
    // Abramowitz-Stegun 7.1.26 on erf; absolute error below 1.5e-7.
    var z = Math.abs(x) / Math.SQRT2;
    var t = 1 / (1 + 0.3275911 * z);
    var e = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-z * z);
    return x >= 0 ? 0.5 * (1 + e) : 0.5 * (1 - e);
  }
  function ninv(p) {
    // Acklam's rational approximation; relative error below 1.2e-9.
    var a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.3577518672690, -30.66479806614716, 2.506628277459239];
    var b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572];
    var c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783];
    var d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416];
    var q, r;
    if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    if (p > 1 - 0.02425) { q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    q = p - 0.5; r = q * q;
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
  }
  /** Black-Scholes price. vol and r are decimals, T in years, cp = +1 call, -1 put. No dividends. */
  function bs(S, K, T, vol, r, cp) {
    if (T <= 0 || vol <= 0) return Math.max(cp * (S - K), 0);
    var sd = vol * Math.sqrt(T);
    var d1 = (Math.log(S / K) + (r + 0.5 * vol * vol) * T) / sd;
    var d2 = d1 - sd;
    return cp * (S * ncdf(cp * d1) - K * Math.exp(-r * T) * ncdf(cp * d2));
  }
  function delta(S, K, T, vol, r, cp) {
    var d1 = (Math.log(S / K) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
    return cp > 0 ? ncdf(d1) : ncdf(d1) - 1;
  }
  /** Strike whose Black-Scholes delta has absolute value absDelta. */
  function strikeForDelta(S, T, vol, r, cp, absDelta) {
    var d1 = cp > 0 ? ninv(absDelta) : ninv(1 - absDelta);
    return S * Math.exp(-d1 * vol * Math.sqrt(T) + (r + 0.5 * vol * vol) * T);
  }

  // ---------- per-stock features ----------
  var TD = 252, CAL = 365;

  function prepare(data, ivModel) {
    var n = data.dates.length;
    var ctx = { data: data, iv: ivModel, n: n, feat: {}, vixTercile: null };
    return ctx;
  }

  function rollingStd(lr, n, len) {
    // out[i] = annualised stdev in points of the n log returns ending at i (needs all present)
    var out = new Float64Array(len).fill(NaN), s = 0, s2 = 0, cnt = 0, i, x;
    for (i = 0; i < len; i++) {
      x = lr[i];
      if (x === x) { s += x; s2 += x * x; cnt++; }
      if (i >= n) { x = lr[i - n]; if (x === x) { s -= x; s2 -= x * x; cnt--; } }
      if (cnt === n) { var v = (s2 - s * s / n) / (n - 1); out[i] = 100 * Math.sqrt(Math.max(v, 0) * TD); }
    }
    return out;
  }

  function features(ctx, tk) {
    if (ctx.feat[tk]) return ctx.feat[tk];
    var c = ctx.data.close[tk], n = ctx.n, i;
    var close = new Float64Array(n), lr = new Float64Array(n).fill(NaN);
    for (i = 0; i < n; i++) close[i] = c[i] == null ? NaN : c[i];
    for (i = 1; i < n; i++) lr[i] = Math.log(close[i] / close[i - 1]);
    var rv20 = rollingStd(lr, 20, n), rv60 = rollingStd(lr, 60, n), rv250 = rollingStd(lr, 250, n);
    // sigma of the 60 returns BEFORE today, for sizing today's move
    var sig60 = new Float64Array(n).fill(NaN);
    for (i = 1; i < n; i++) sig60[i] = rv60[i - 1] / 100 / Math.sqrt(TD);
    // 252-day high and low of closes, including today
    var hi = new Float64Array(n).fill(NaN), lo = new Float64Array(n).fill(NaN);
    for (i = 251; i < n; i++) {
      var h = -Infinity, l = Infinity, ok = true;
      for (var k = i - 251; k <= i; k++) { var x = close[k]; if (x !== x) { ok = false; break; } if (x > h) h = x; if (x < l) l = x; }
      if (ok) { hi[i] = h; lo[i] = l; }
    }
    var m = ctx.iv.coef, vix = ctx.data.vix, iv30 = new Float64Array(n).fill(NaN);
    var real = ctx.data.volIndex && ctx.data.volIndex[tk];
    var ivReal = new Float64Array(n).fill(NaN);
    for (i = 0; i < n; i++) {
      if (rv20[i] === rv20[i] && rv60[i] === rv60[i] && vix[i] != null) iv30[i] = Math.max(8, m.a + m.rv20 * rv20[i] + m.rv60 * rv60[i] + m.vix * vix[i]);
      if (real && real[i] != null) ivReal[i] = real[i];
    }
    return (ctx.feat[tk] = { close: close, lr: lr, rv20: rv20, rv60: rv60, rv250: rv250, sig60: sig60, hi: hi, lo: lo, iv30: iv30, ivReal: ivReal });
  }

  function vixTerciles(ctx) {
    // tercile of today's VIX within its trailing 252 days: 0 low, 1 middle, 2 high
    if (ctx.vixTercile) return ctx.vixTercile;
    var v = ctx.data.vix, n = ctx.n, out = new Int8Array(n).fill(-1);
    for (var i = 251; i < n; i++) {
      if (v[i] == null) continue;
      var below = 0, cnt = 0;
      for (var k = i - 251; k <= i; k++) if (v[k] != null) { cnt++; if (v[k] < v[i]) below++; }
      var q = below / cnt; out[i] = q < 1 / 3 ? 0 : q < 2 / 3 ? 1 : 2;
    }
    return (ctx.vixTercile = out);
  }

  // ---------- implied-volatility estimate ----------
  /** Estimated implied volatility (decimal) for an option on tk at day i with `days` calendar days left and strike K. */
  function estIV(ctx, f, i, days, S, K, o) {
    var base = (o.useRealIndex && f.ivReal[i] === f.ivReal[i]) ? f.ivReal[i] : f.iv30[i];
    if (base !== base) return NaN;
    base += o.premium || 0;
    if (o.term !== false && days > 30) {
      var d = ctx.data, v = d.vix[i], v3 = d.vix3m[i], v6 = d.vix6m[i];
      if (v != null && v3 != null && v6 != null) {
        var r3 = v3 / v, r6 = v6 / v, ratio;
        if (days <= 93) ratio = 1 + (r3 - 1) * (days - 30) / 63;
        else if (days <= 180) ratio = r3 + (r6 - r3) * (days - 93) / 87;
        else ratio = r6;
        base *= ratio;
      }
    }
    if (o.skew !== false && K !== S) {
      // Slope of implied volatility against log strike/price, from a 1996-2005 sample of stock options:
      // 20% below the price about +6% relative, 20% above about -1% relative.
      var lm = Math.log(K / S);
      base *= 1 + (lm < 0 ? -0.28 : -0.05) * lm;
    }
    return Math.max(base, 5) / 100;
  }

  // ---------- conditions ----------
  var METRICS = {
    none: { label: "No condition (baseline only)" },
    ret1: { label: "One-day fall", unit: "%", def: 8, min: 3, max: 20, step: 1, test: function (f, i, p) { return f.lr[i] === f.lr[i] && Math.exp(f.lr[i]) - 1 <= -p.x / 100; } },
    sigma: { label: "One-day fall, in multiples of the stock's usual daily move", unit: "×", def: 3, min: 1.5, max: 6, step: 0.5, test: function (f, i, p) { return f.sig60[i] === f.sig60[i] && f.lr[i] <= -p.x * f.sig60[i]; } },
    retN: { label: "Fall over the past N trading days", unit: "%", def: 20, min: 5, max: 50, step: 5, window: true, test: function (f, i, p) { var a = f.close[i - p.n]; return i >= p.n && a === a && f.close[i] / a - 1 <= -p.x / 100; } },
    upN: { label: "Rise over the past N trading days", unit: "%", def: 20, min: 5, max: 50, step: 5, window: true, test: function (f, i, p) { var a = f.close[i - p.n]; return i >= p.n && a === a && f.close[i] / a - 1 >= p.x / 100; } },
    low52: { label: "Within X% of the 52-week low", unit: "%", def: 5, min: 0, max: 20, step: 1, test: function (f, i, p) { return f.lo[i] === f.lo[i] && f.close[i] <= f.lo[i] * (1 + p.x / 100); } },
    high52: { label: "Within X% of the 52-week high", unit: "%", def: 2, min: 0, max: 20, step: 1, test: function (f, i, p) { return f.hi[i] === f.hi[i] && f.close[i] >= f.hi[i] * (1 - p.x / 100); } },
    mom: { label: "12-month return, skipping the latest month, at least", unit: "%", def: 30, min: -40, max: 100, step: 10, test: function (f, i, p) { var a = f.close[i - 252], b = f.close[i - 21]; return i >= 252 && a === a && b === b && b / a - 1 >= p.x / 100; } },
    rvlow: { label: "Recent volatility at most X% of its one-year level", unit: "%", def: 60, min: 30, max: 100, step: 5, circular: true, test: function (f, i, p) { return f.rv20[i] === f.rv20[i] && f.rv250[i] === f.rv250[i] && f.rv20[i] <= f.rv250[i] * p.x / 100; } }
  };

  // ---------- one trade ----------
  /**
   * Simulate buying one option. Signal day is `sig`; entry is at the close of sig + lag.
   * Returns null when data is missing or the option's life runs past the end of the data.
   */
  function trade(ctx, f, sig, cfg) {
    var i = sig + (cfg.lag == null ? 1 : cfg.lag), n = ctx.n;
    var life = Math.round(cfg.dte * TD / CAL);           // trading days to expiry
    var last = i + life;
    if (last >= n) return null;
    var S = f.close[i]; if (S !== S) return null;
    var cp = cfg.side === "put" ? -1 : 1;
    var r = (ctx.data.rate[i] == null ? 0 : ctx.data.rate[i]) / 100;
    var T = cfg.dte / CAL;
    var atm = estIV(ctx, f, i, cfg.dte, S, S, cfg.iv); if (atm !== atm) return null;
    var K = strikeForDelta(S, T, atm, r, cp, cfg.delta);
    var vol = estIV(ctx, f, i, cfg.dte, S, K, cfg.iv);
    var mid = bs(S, K, T, vol, r, cp);
    if (!(mid > 0.01)) return null;
    var half = cfg.spread / 100 / 2 * cfg.fill;             // share of mid paid each way
    var cost = mid * (1 + half);
    var ex = cfg.exit, stopAt = last, exitDay = last, proceeds = NaN;
    if (ex.type === "days") stopAt = Math.min(last, i + Math.max(1, Math.round(life * ex.frac)));
    var target = ex.type === "target" ? cost * ex.mult : Infinity;
    for (var d = i + 1; d <= stopAt; d++) {
      var Sd = f.close[d];
      if (Sd !== Sd) { if (d === stopAt) return null; continue; }
      if (d === last) { proceeds = Math.max(cp * (Sd - K), 0); exitDay = d; break; }
      if (ex.type === "expiry") continue;
      if (d === stopAt || ex.type === "target") {
        var left = cfg.dte - (d - i) * CAL / TD;
        var v = estIV(ctx, f, d, left, Sd, K, cfg.iv);
        if (v !== v) { if (d === stopAt) return null; continue; }
        var m = bs(Sd, K, left / CAL, v, r, cp) * (1 - half);
        if (d === stopAt || m >= target) { proceeds = m; exitDay = d; break; }
      }
    }
    if (proceeds !== proceeds) return null;
    return { sig: sig, entry: i, exit: exitDay, S: S, K: K, iv: vol, cost: cost, Sx: f.close[exitDay], ret: proceeds / cost - 1 };
  }

  // ---------- run ----------
  function idxOnOrAfter(dates, ymd) { var lo = 0, hi = dates.length; while (lo < hi) { var m = (lo + hi) >> 1; if (dates[m] < ymd) lo = m + 1; else hi = m; } return lo; }

  function summarise(tr, hold) {
    var n = tr.length, s = { n: n };
    if (!n) return s;
    var rets = tr.map(function (t) { return t.ret; }).sort(function (a, b) { return a - b; });
    var sum = 0, lost = 0, win = 0, x2 = 0, x5 = 0, x10 = 0;
    for (var k = 0; k < n; k++) { var r = rets[k]; sum += r; if (r <= -0.99) lost++; if (r > 0) win++; if (r >= 1) x2++; if (r >= 4) x5++; if (r >= 9) x10++; }
    s.mean = sum / n; s.median = n % 2 ? rets[(n - 1) / 2] : (rets[n / 2 - 1] + rets[n / 2]) / 2;
    s.lost = lost / n; s.win = win / n; s.x2 = x2 / n; s.x5 = x5 / n; s.x10 = x10 / n; s.best = rets[n - 1];
    s.hold = hold;
    return s;
  }

  var BINS = [-0.99, -0.5, 0, 0.5, 1, 2, 4];   // upper edges; last bin is above 4
  var BIN_LABELS = ["Total loss", "−99 to −50%", "−50 to 0%", "0 to +50%", "+50 to +100%", "+100 to +200%", "+200 to +400%", "Above +400%"];
  function histogram(tr) {
    var h = new Array(BINS.length + 1).fill(0);
    tr.forEach(function (t) { var b = 0; while (b < BINS.length && t.ret > BINS[b]) b++; h[b]++; });
    return h.map(function (c) { return tr.length ? c / tr.length : 0; });
  }

  /**
   * cfg: { side, delta, dte, exit:{type:'expiry'|'days'|'target', frac, mult}, spread, fill, lag,
   *        iv:{premium, term, skew, useRealIndex}, cond:{metric, x, n}, vix:'any'|'low'|'mid'|'high',
   *        gap, baseStep, from, to, tickers }
   */
  function run(ctx, cfg) {
    var dates = ctx.data.dates, n = ctx.n;
    var a = Math.max(idxOnOrAfter(dates, cfg.from), 252), b = Math.min(idxOnOrAfter(dates, cfg.to + 1), n) - 1;
    var tickers = cfg.tickers || ctx.data.tickers;
    var met = METRICS[cfg.cond.metric], terc = vixTerciles(ctx);
    var wantT = { any: -1, low: 0, mid: 1, high: 2 }[cfg.vix || "any"];
    var cond = [], base = [], gap = cfg.gap == null ? 10 : cfg.gap, step = cfg.baseStep || 5;
    tickers.forEach(function (tk, ti) {
      var f = features(ctx, tk), lastSig = -1e9, i, t;
      for (i = a; i <= b; i++) {
        if (f.close[i] !== f.close[i]) continue;
        if ((i + ti) % step === 0) { t = trade(ctx, f, i, cfg); if (t) { t.tk = tk; base.push(t); } }
        if (met.test && i - lastSig >= gap && (wantT < 0 || terc[i] === wantT) && met.test(f, i, cfg.cond)) {
          t = trade(ctx, f, i, cfg);
          if (t) { t.tk = tk; cond.push(t); lastSig = i; }
        }
      }
    });

    // Baseline mean per calendar year of entry, used to compare like with like.
    var by = {}, yr = function (t) { return Math.floor(dates[t.entry] / 10000); };
    base.forEach(function (t) { var y = yr(t); (by[y] = by[y] || { n: 0, s: 0, cn: 0, cs: 0 }); by[y].n++; by[y].s += t.ret; });
    cond.forEach(function (t) { var y = yr(t); (by[y] = by[y] || { n: 0, s: 0, cn: 0, cs: 0 }); by[y].cn++; by[y].cs += t.ret; });
    var years = Object.keys(by).sort().map(function (y) { var o = by[y]; return { year: +y, baseN: o.n, baseMean: o.n ? o.s / o.n : null, condN: o.cn, condMean: o.cn ? o.cs / o.cn : null }; });

    // Excess over the same-year baseline, then a t-statistic on monthly averages so that trades
    // entered in the same month count once, divided by sqrt(holding months) for overlapping holds.
    var months = {}, exSum = 0, exN = 0;
    cond.forEach(function (t) {
      var o = by[yr(t)]; if (!o.n) return;
      var e = t.ret - o.s / o.n; t.excess = e; exSum += e; exN++;
      var m = Math.floor(dates[t.entry] / 100); (months[m] = months[m] || []).push(e);
    });
    var mm = Object.keys(months).map(function (m) { var v = months[m]; return v.reduce(function (p, q) { return p + q; }, 0) / v.length; });
    var excess = { n: exN, mean: exN ? exSum / exN : null, months: mm.length, t: null, tAdj: null };
    if (mm.length >= 3) {
      var mu = mm.reduce(function (p, q) { return p + q; }, 0) / mm.length;
      var sd = Math.sqrt(mm.reduce(function (p, q) { return p + (q - mu) * (q - mu); }, 0) / (mm.length - 1));
      if (sd > 0) {
        excess.t = mu / (sd / Math.sqrt(mm.length));
        var holdMonths = (cfg.exit.type === "days" ? cfg.dte * cfg.exit.frac : cfg.dte) / 30;
        excess.tAdj = excess.t / Math.sqrt(Math.max(1, holdMonths));
      }
    }

    var perTk = {};
    cond.forEach(function (t) { var o = (perTk[t.tk] = perTk[t.tk] || { tk: t.tk, n: 0, s: 0, best: -1 }); o.n++; o.s += t.ret; if (t.ret > o.best) o.best = t.ret; });
    return {
      cond: summarise(cond), base: summarise(base), excess: excess, years: years,
      histCond: histogram(cond), histBase: histogram(base), binLabels: BIN_LABELS,
      trades: cond, perTicker: Object.keys(perTk).map(function (k) { var o = perTk[k]; o.mean = o.s / o.n; return o; }),
      range: [dates[a], dates[b]]
    };
  }

  return { ncdf: ncdf, ninv: ninv, bs: bs, delta: delta, strikeForDelta: strikeForDelta, prepare: prepare, features: features,
           estIV: estIV, trade: trade, run: run, METRICS: METRICS, BIN_LABELS: BIN_LABELS };
});
