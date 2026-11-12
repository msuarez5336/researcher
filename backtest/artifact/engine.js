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
    var ctx = { data: data, iv: ivModel, n: n, feat: {} };
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
    var c = ctx.data.close[tk], n = ctx.n, i, first = -1;
    var close = new Float64Array(n).fill(NaN), lr = new Float64Array(n).fill(NaN);
    for (i = 0; i < n; i++) {
      if (c[i] != null) { close[i] = c[i]; if (first < 0) first = i; }
      else if (first >= 0) close[i] = close[i - 1];        // a missing day inside the history keeps the last close
    }
    for (i = 1; i < n; i++) lr[i] = Math.log(close[i] / close[i - 1]);
    var rv20 = rollingStd(lr, 20, n), rv60 = rollingStd(lr, 60, n), rv250 = rollingStd(lr, 250, n);
    var sig60 = new Float64Array(n).fill(NaN);              // usual daily move, from the 60 returns BEFORE today
    for (i = 1; i < n; i++) sig60[i] = rv60[i - 1] / 100 / Math.sqrt(TD);
    var m = ctx.iv.coef, vix = ctx.data.vix, iv30 = new Float64Array(n).fill(NaN);
    var real = ctx.data.volIndex && ctx.data.volIndex[tk];
    var ivReal = new Float64Array(n).fill(NaN);
    for (i = 0; i < n; i++) {
      if (rv20[i] === rv20[i] && rv60[i] === rv60[i] && vix[i] != null) iv30[i] = Math.max(8, m.a + m.rv20 * rv20[i] + m.rv60 * rv60[i] + m.vix * vix[i]);
      if (real && real[i] != null) ivReal[i] = real[i];
    }
    return (ctx.feat[tk] = { first: first, close: close, lr: lr, rv20: rv20, rv60: rv60, rv250: rv250, sig60: sig60, iv30: iv30, ivReal: ivReal, c: {} });
  }

  // ---------- cached series for conditions ----------
  function memo(o, key, build) { return o[key] || (o[key] = build()); }
  function rollExt(close, n, len, first, isMax) {
    // out[i] = max (or min) of the n closes ending at i, by a monotonic queue
    var out = new Float64Array(len).fill(NaN), q = new Int32Array(len), h = 0, t = 0, i;
    if (first < 0) return out;
    for (i = first; i < len; i++) {
      while (t > h && (isMax ? close[q[t - 1]] <= close[i] : close[q[t - 1]] >= close[i])) t--;
      q[t++] = i;
      if (q[h] <= i - n) h++;
      if (i - first + 1 >= n) out[i] = close[q[h]];
    }
    return out;
  }
  function movAvg(close, n, len, first) {
    var out = new Float64Array(len).fill(NaN), s = 0, i;
    if (first < 0) return out;
    for (i = first; i < len; i++) { s += close[i]; if (i - first >= n) s -= close[i - n]; if (i - first + 1 >= n) out[i] = s / n; }
    return out;
  }
  function rsi(lr, n, len, first) {
    // Wilder's relative strength index on daily closes
    var out = new Float64Array(len).fill(NaN), g = 0, l = 0, i, k = 0;
    if (first < 0) return out;
    for (i = first + 1; i < len; i++) {
      var up = Math.max(lr[i], 0), dn = Math.max(-lr[i], 0); k++;
      if (k <= n) { g += up / n; l += dn / n; } else { g = (g * (n - 1) + up) / n; l = (l * (n - 1) + dn) / n; }
      if (k >= n) out[i] = l === 0 ? 100 : 100 - 100 / (1 + g / l);
    }
    return out;
  }
  function streak(lr, len, sign) {
    var out = new Float64Array(len), i;
    for (i = 1; i < len; i++) out[i] = sign * lr[i] > 0 ? out[i - 1] + 1 : 0;
    return out;
  }
  function vixPctile(ctx) {
    return memo(ctx, "_vp", function () {
      var v = ctx.data.vix, n = ctx.n, out = new Float64Array(n).fill(NaN);
      for (var i = 251; i < n; i++) {
        if (v[i] == null) continue;
        var below = 0, cnt = 0;
        for (var k = i - 251; k <= i; k++) if (v[k] != null) { cnt++; if (v[k] < v[i]) below++; }
        out[i] = 100 * below / cnt;
      }
      return out;
    });
  }
  function pctChange(a, i, n) { var x = a[i - n], y = a[i]; return i >= n && x != null && y != null && x === x && y === y ? (y / x - 1) * 100 : NaN; }

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
  // Each metric gives one number for a stock on a day, from data up to and including that day.
  // A condition is { metric, op: "<=" | ">=", value, n }. All conditions must hold together.
  var METRICS = {
    ret: { doc: "percent change in the share price over the past n trading days (negative = fell)", unit: "%", n: 1, nMin: 1, nMax: 252, min: -90, max: 300,
      get: function (ctx, f, i, n) { return pctChange(f.close, i, n); } },
    move_sigma: { doc: "today's move divided by the stock's usual daily move over the prior 60 days (negative = down; -3 is a fall three times the usual size)", unit: "x", min: -15, max: 15,
      get: function (ctx, f, i) { return f.lr[i] / f.sig60[i]; } },
    from_high: { doc: "percent below the highest close of the past n trading days (0 = at the high; n = 252 is the 52-week high)", unit: "%", n: 252, nMin: 5, nMax: 756, min: 0, max: 95,
      get: function (ctx, f, i, n) { var h = memo(f.c, "hi" + n, function () { return rollExt(f.close, n, ctx.n, f.first, true); })[i]; return (1 - f.close[i] / h) * 100; } },
    from_low: { doc: "percent above the lowest close of the past n trading days (0 = at the low; n = 252 is the 52-week low)", unit: "%", n: 252, nMin: 5, nMax: 756, min: 0, max: 500,
      get: function (ctx, f, i, n) { var l = memo(f.c, "lo" + n, function () { return rollExt(f.close, n, ctx.n, f.first, false); })[i]; return (f.close[i] / l - 1) * 100; } },
    vs_ma: { doc: "percent above (+) or below (-) the n-day moving average of closes", unit: "%", n: 50, nMin: 5, nMax: 250, min: -80, max: 200,
      get: function (ctx, f, i, n) { var a = memo(f.c, "ma" + n, function () { return movAvg(f.close, n, ctx.n, f.first); })[i]; return (f.close[i] / a - 1) * 100; } },
    mom_12_1: { doc: "percent return from 12 months ago to 1 month ago (classic momentum)", unit: "%", min: -90, max: 500,
      get: function (ctx, f, i) { var a = f.close[i - 252], b = f.close[i - 21]; return i >= 252 ? (b / a - 1) * 100 : NaN; } },
    rsi: { doc: "relative strength index over n days, 0 to 100 (below 30 is usually called oversold, above 70 overbought)", unit: "", n: 14, nMin: 2, nMax: 50, min: 0, max: 100,
      get: function (ctx, f, i, n) { return memo(f.c, "rsi" + n, function () { return rsi(f.lr, n, ctx.n, f.first); })[i]; } },
    down_days: { doc: "number of consecutive down closes ending today", unit: " days", min: 0, max: 20,
      get: function (ctx, f, i) { return memo(f.c, "dn", function () { return streak(f.lr, ctx.n, -1); })[i]; } },
    up_days: { doc: "number of consecutive up closes ending today", unit: " days", min: 0, max: 20,
      get: function (ctx, f, i) { return memo(f.c, "up", function () { return streak(f.lr, ctx.n, 1); })[i]; } },
    vol_ratio: { doc: "the stock's 20-day volatility as a percent of its one-year volatility (below 100 = quieter than usual)", unit: "%", min: 10, max: 400, circular: true,
      get: function (ctx, f, i) { return 100 * f.rv20[i] / f.rv250[i]; } },
    rel_ret: { doc: "the stock's percent change over n days minus the S&P 500's (negative = lagged the market)", unit: " pts", n: 20, nMin: 1, nMax: 252, min: -90, max: 300,
      get: function (ctx, f, i, n) { return pctChange(f.close, i, n) - pctChange(ctx.data.spy, i, n); } },
    mkt_ret: { doc: "percent change in the S&P 500 (SPY) over the past n trading days", unit: "%", n: 20, nMin: 1, nMax: 252, min: -60, max: 100, market: true,
      get: function (ctx, f, i, n) { return pctChange(ctx.data.spy, i, n); } },
    vix: { doc: "level of the VIX, the market's fear gauge (about 12-15 is calm, above 25 is fearful)", unit: "", min: 8, max: 90, market: true,
      get: function (ctx, f, i) { var v = ctx.data.vix[i]; return v == null ? NaN : v; } },
    vix_pctile: { doc: "where today's VIX sits within its past year, 0 to 100 (below 33 = calm third, above 67 = fearful third)", unit: "", min: 0, max: 100, market: true,
      get: function (ctx, f, i) { return vixPctile(ctx)[i]; } }
  };
  function holds(ctx, f, i, conds) {
    for (var k = 0; k < conds.length; k++) {
      var c = conds[k], v = METRICS[c.metric].get(ctx, f, i, c.n);
      if (v !== v || (c.op === "<=" ? v > c.value : v < c.value)) return false;
    }
    return true;
  }

  // ---------- reading a setup written by a person or a model ----------
  var EXITS = { expiry: { type: "expiry" }, half: { type: "days", frac: 0.5 }, quarter: { type: "days", frac: 0.25 }, x2: { type: "target", mult: 2 }, x3: { type: "target", mult: 3 } };
  function clamp(v, lo, hi) { return Math.min(hi, Math.max(lo, v)); }
  function nearest(v, list) { return list.reduce(function (p, q) { return Math.abs(q - v) < Math.abs(p - v) ? q : p; }); }
  /**
   * Turn an untrusted object into a safe setup. Unknown metrics are dropped and listed in `dropped`;
   * numbers are clamped to each metric's range. Never throws.
   */
  function sanitize(raw, data) {
    var out = { conds: [], option: {}, population: null, note: "", dropped: [] };
    if (!raw || typeof raw !== "object") return out;
    (Array.isArray(raw.conditions) ? raw.conditions : []).slice(0, 6).forEach(function (c) {
      var m = c && METRICS[c.metric], v = c && Number(c.value);
      if (!m || (c.op !== "<=" && c.op !== ">=") || v !== v) { out.dropped.push(c && typeof c.metric === "string" ? c.metric.slice(0, 40) : "unreadable condition"); return; }
      var cond = { metric: c.metric, op: c.op, value: clamp(v, m.min, m.max) };
      if (m.n) { var n = Math.round(Number(c.n)); cond.n = n === n ? clamp(n, m.nMin, m.nMax) : m.n; }
      out.conds.push(cond);
    });
    var o = raw.option && typeof raw.option === "object" ? raw.option : {};
    if (o.side === "call" || o.side === "put") out.option.side = o.side;
    if (Number(o.delta) > 0) out.option.delta = nearest(Number(o.delta), [0.5, 0.35, 0.2, 0.1]);
    if (Number(o.dte) > 0) out.option.dte = nearest(Number(o.dte), [30, 60, 90, 120, 180]);
    if (typeof o.exit === "string" && EXITS[o.exit]) out.option.exit = o.exit;
    var p = raw.population && typeof raw.population === "object" ? raw.population : null;
    if (p && data) {
      var secs = {}, grps = {}; data.tickers.forEach(function (t) { secs[data.sector[t]] = 1; if (data.group) grps[data.group[t]] = 1; });
      var pop = { sectors: (Array.isArray(p.sectors) ? p.sectors : []).filter(function (x) { return secs[x]; }),
                  groups: (Array.isArray(p.groups) ? p.groups : []).filter(function (x) { return grps[x]; }),
                  tickers: (Array.isArray(p.tickers) ? p.tickers : []).filter(function (x) { return data.close[x]; }) };
      if (pop.sectors.length || pop.groups.length || pop.tickers.length) out.population = pop;
    }
    if (typeof raw.note === "string") out.note = raw.note.slice(0, 400);
    return out;
  }
  function fmt(v) { return (Math.round(Math.abs(v) * 10) / 10).toString(); }
  function span(n) { return n === 1 ? "one day" : n === 5 ? "a week" : n === 21 || n === 20 ? "a month" : n === 63 || n === 60 ? "three months" : n === 126 ? "six months" : n === 252 ? "a year" : n + " trading days"; }
  /** One condition in plain words. */
  function describe(c) {
    var v = c.value, a = fmt(v), le = c.op === "<=";
    switch (c.metric) {
      case "ret": return v < 0 && le ? "fell " + a + "% or more in " + span(c.n) : v > 0 && !le ? "rose " + a + "% or more in " + span(c.n) : "changed by " + (le ? "at most " : "at least ") + (v < 0 ? "−" : "+") + a + "% in " + span(c.n);
      case "move_sigma": return v < 0 && le ? "fell today by " + a + " times its usual daily move or more" : v > 0 && !le ? "rose today by " + a + " times its usual daily move or more" : "today's move was " + (le ? "at most " : "at least ") + (v < 0 ? "−" : "") + a + " times its usual size";
      case "from_high": return (le ? "within " + a + "% of" : a + "% or more below") + " its " + (c.n === 252 ? "52-week" : c.n + "-day") + " high";
      case "from_low": return (le ? "within " + a + "% of" : a + "% or more above") + " its " + (c.n === 252 ? "52-week" : c.n + "-day") + " low";
      case "vs_ma": return v <= 0 && le ? (v === 0 ? "below" : a + "% or more below") + " its " + c.n + "-day average" : v >= 0 && !le ? (v === 0 ? "above" : a + "% or more above") + " its " + c.n + "-day average" : "price " + (le ? "at most " : "at least ") + (v < 0 ? "−" : "+") + a + "% against its " + c.n + "-day average";
      case "mom_12_1": return "12-month return (skipping the latest month) " + (le ? "at most " : "at least ") + (v < 0 ? "−" : "+") + a + "%";
      case "rsi": return c.n + "-day RSI " + (le ? "at or below " : "at or above ") + a;
      case "down_days": return (le ? "at most " : "at least ") + a + " down days in a row";
      case "up_days": return (le ? "at most " : "at least ") + a + " up days in a row";
      case "vol_ratio": return "recent volatility " + (le ? "at most " : "at least ") + a + "% of its one-year level";
      case "rel_ret": return v < 0 && le ? "lagged the S&P 500 by " + a + " points or more over " + span(c.n) : v > 0 && !le ? "beat the S&P 500 by " + a + " points or more over " + span(c.n) : "return against the S&P 500 over " + span(c.n) + (le ? " at most " : " at least ") + (v < 0 ? "−" : "+") + a + " points";
      case "mkt_ret": return v < 0 && le ? "the S&P 500 fell " + a + "% or more in " + span(c.n) : v > 0 && !le ? "the S&P 500 rose " + a + "% or more in " + span(c.n) : "the S&P 500 changed by " + (le ? "at most " : "at least ") + (v < 0 ? "−" : "+") + a + "% in " + span(c.n);
      case "vix": return "the VIX was " + (le ? "at or below " : "at or above ") + a;
      case "vix_pctile": return le && v <= 40 ? "the market was calm (VIX in the lowest " + a + "% of its past year)" : !le && v >= 60 ? "the market was fearful (VIX in the highest " + fmt(100 - v) + "% of its past year)" : "the VIX was " + (le ? "at or below" : "at or above") + " the " + a + "th percentile of its past year";
    }
    return c.metric;
  }

  // ---------- one trade ----------
  var IV_DEFAULT = { premium: 0, term: true, skew: true, useRealIndex: false };
  var COST_DEFAULT = { spread: 8, fill: 0.75 };   // quoted spread as % of the option price; share of it paid
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
    var ivo = cfg.iv || IV_DEFAULT;
    var atm = estIV(ctx, f, i, cfg.dte, S, S, ivo); if (atm !== atm) return null;
    var K = strikeForDelta(S, T, atm, r, cp, cfg.delta);
    var vol = estIV(ctx, f, i, cfg.dte, S, K, ivo);
    var mid = bs(S, K, T, vol, r, cp);
    if (!(mid > 0.01)) return null;
    var half = (cfg.spread == null ? COST_DEFAULT.spread : cfg.spread) / 100 / 2 * (cfg.fill == null ? COST_DEFAULT.fill : cfg.fill);   // share of mid paid each way
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
        var v = estIV(ctx, f, d, left, Sd, K, ivo);
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
   * cfg: { side, delta, dte, exit:{type:'expiry'|'days'|'target', frac, mult}, conds:[{metric, op, value, n}],
   *        spread, fill, lag, iv, gap, baseStep, from, to, tickers }
   */
  function run(ctx, cfg) {
    var dates = ctx.data.dates, n = ctx.n;
    var a = Math.max(idxOnOrAfter(dates, cfg.from), 252), b = Math.min(idxOnOrAfter(dates, cfg.to + 1), n) - 1;
    var tickers = cfg.tickers || ctx.data.tickers;
    var conds = cfg.conds || [];
    var cond = [], base = [], gap = cfg.gap == null ? 10 : cfg.gap, step = cfg.baseStep || 5;
    tickers.forEach(function (tk, ti) {
      var f = features(ctx, tk), lastSig = -1e9, i, t;
      for (i = a; i <= b; i++) {
        if (f.close[i] !== f.close[i]) continue;
        if ((i + ti) % step === 0) { t = trade(ctx, f, i, cfg); if (t) { t.tk = tk; base.push(t); } }
        if (conds.length && i - lastSig >= gap && holds(ctx, f, i, conds)) {
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
           estIV: estIV, trade: trade, run: run, METRICS: METRICS, EXITS: EXITS, sanitize: sanitize, describe: describe, BIN_LABELS: BIN_LABELS,
           IV_DEFAULT: IV_DEFAULT, COST_DEFAULT: COST_DEFAULT };
});
