"""Event studies for episodic long-option windows. Implements study_spec.md (stdlib only).

Usage (from repo root):
    python3 research/2026-11-07-event-windows/study/events.py --selftest
    python3 research/2026-11-07-event-windows/study/events.py            # full run

Writes study/results.csv (one row per scored cell), study/events.csv (every event), study/run.log.
Downloads cached in study/data/ (gitignored). Earnings are used only to exclude single-stock events.
"""
from __future__ import annotations

import csv
import json
import math
import random
import re
import statistics as st
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
sys.path.insert(0, str(HERE.parents[1] / "2026-11-07-long-vol-tickers" / "screen"))
import screen  # noqa: E402  (reuses the Nasdaq OHLCV loader and its cache)

UA = {"User-Agent": "Mozilla/5.0 (research-script)"}
START = date(2016, 11, 7)
OOS_START = date(2021, 7, 1)
ETFS = ["SPY", "QQQ", "IWM"]
STOCKS = ["NVDA", "TSLA", "MU", "AAPL", "INTC", "AMD", "AMZN", "META", "PLTR", "GOOGL", "MSFT",
          "AVGO", "ORCL", "HOOD", "PFE", "SOFI"]
IV_MAP = {"SPY": "VIX", "QQQ": "VXN", "IWM": "RVX", "AAPL": "VXAPL", "AMZN": "VXAZN", "GOOGL": "VXGOG"}
VRP_PROXY = 3.4
DTE0 = 45
COST = {"gross": 0.0, "k0.70": 0.006, "k1.00": 0.015}
COMM = 0.007  # $0.70 per contract = 0.007 per share
NON_MEETING = {date(2025, 8, 22)}
UNSCHEDULED = {date(2020, 3, 3), date(2020, 3, 15)}
TRIALS = 0


# ------------------------------------------------------------------ data
def _get(url: str) -> bytes:
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read()
        except Exception:
            if a == 3:
                raise
            time.sleep(2 ** (a + 1))


def cached(name: str, url: str) -> str:
    DATA.mkdir(exist_ok=True)
    p = DATA / name
    if not p.exists():
        p.write_bytes(_get(url))
    return p.read_text(encoding="utf-8", errors="replace")


def vol_index(name: str) -> dict[date, float]:
    txt = cached(f"{name}.csv", f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{name}_History.csv")
    rows = list(csv.reader(txt.splitlines()))
    hdr = [h.strip().upper() for h in rows[0]]
    col = hdr.index("CLOSE") if "CLOSE" in hdr else len(hdr) - 1
    out = {}
    for r in rows[1:]:
        try:
            out[datetime.strptime(r[0], "%m/%d/%Y").date()] = float(r[col])
        except (ValueError, IndexError):
            pass
    return out


def gex() -> dict[date, float]:
    txt = cached("DIX.csv", "https://squeezemetrics.com/monitor/static/DIX.csv")
    out = {}
    for r in csv.DictReader(txt.splitlines()):
        try:
            out[date.fromisoformat(r["date"])] = float(r["gex"])
        except (ValueError, KeyError):
            pass
    return out


def fomc_dates() -> set[date]:
    pages = ["fomccalendars.htm"] + [f"fomchistorical{y}.htm" for y in range(2016, 2021)]
    out = set()
    for pg in pages:
        try:
            txt = cached(f"fed_{pg}", f"https://www.federalreserve.gov/monetarypolicy/{pg}")
        except Exception:
            continue
        for s in re.findall(r"monetary(\d{8})a\.htm", txt):
            d = datetime.strptime(s, "%Y%m%d").date()
            if d >= START and d not in NON_MEETING:
                out.add(d)
    return out


def earnings_on(d: date) -> set[str]:
    p = DATA / "earn" / f"{d}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        try:
            raw = _get(f"https://api.nasdaq.com/api/calendar/earnings?date={d}")
            time.sleep(0.4)
        except Exception:
            raw = b'{"data":{"rows":[]},"error":"fetch failed"}'
        p.write_bytes(raw)
    try:
        rows = (json.loads(p.read_text()).get("data") or {}).get("rows") or []
    except json.JSONDecodeError:
        rows = []
    return {r.get("symbol", "").upper() for r in rows}


class Series:
    def __init__(self, tk: str):
        bars = [b for b in screen.load_ohlc(tk) if b[0] >= START]
        self.tk = tk
        self.d = [b[0] for b in bars]
        self.O = [b[1] for b in bars]; self.H = [b[2] for b in bars]
        self.L = [b[3] for b in bars]; self.C = [b[4] for b in bars]
        self.idx = {d: i for i, d in enumerate(self.d)}
        n = len(bars)
        self.r = [math.nan] + [math.log(self.C[i] / self.C[i - 1]) for i in range(1, n)]
        self.s60 = [math.nan] * n
        for i in range(61, n):
            self.s60[i] = st.stdev(self.r[i - 60:i])
        self.rv20 = [math.nan] * n
        for i in range(20, n):
            self.rv20[i] = st.stdev(self.r[i - 19:i + 1]) * math.sqrt(252)

    def clv(self, i):
        rng = self.H[i] - self.L[i]
        return (self.C[i] - self.L[i]) / rng if rng > 0 else 0.5


# ------------------------------------------------------------------ Black-Scholes
def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def ninv(p):
    """Inverse standard normal CDF (Acklam's rational approximation, |error| < 1.2e-9 after one Newton step)."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    pl = 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p > 1 - pl:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    else:
        q = p - 0.5; r = q * q
        x = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    e = ncdf(x) - p
    return x - e * math.sqrt(2 * math.pi) * math.exp(x * x / 2)


def bs(S, K, T, v, cp):
    if T <= 0 or v <= 0:
        return max(0.0, S - K) if cp == "C" else max(0.0, K - S)
    d1 = (math.log(S / K) + 0.5 * v * v * T) / (v * math.sqrt(T)); d2 = d1 - v * math.sqrt(T)
    return S * ncdf(d1) - K * ncdf(d2) if cp == "C" else K * ncdf(-d2) - S * ncdf(-d1)


def strike_for_delta(S, T, v, cp, delta):
    d1 = ninv(delta) if cp == "C" else ninv(1 - delta)
    return S * math.exp(-d1 * v * math.sqrt(T) + 0.5 * v * v * T)


def option_returns(S0, S1, iv0, iv1, h, cp, structure):
    """Returns {cost: return} for a 45-DTE position bought at S0/iv0, sold h trading days later at S1/iv1."""
    T0 = DTE0 / 365; T1 = (DTE0 - h * 7 / 5) / 365
    if structure == "atm":
        legs = [(S0, +1)]
    else:
        legs = [(strike_for_delta(S0, T0, iv0, cp, 0.50), +1), (strike_for_delta(S0, T0, iv0, cp, 0.25), -1)]
    p0 = [bs(S0, K, T0, iv0, cp) for K, _ in legs]
    p1 = [bs(S1, K, T1, iv1, cp) for K, _ in legs]
    v0 = sum(q * x for (_, q), x in zip(legs, p0)); v1 = sum(q * x for (_, q), x in zip(legs, p1))
    out = {}
    for name, c in COST.items():
        cost0 = sum(c * x + COMM for x in p0) if c else 0.0
        cost1 = sum(c * x + COMM for x in p1) if c else 0.0
        paid = v0 + cost0
        out[name] = (v1 - cost1 - paid) / paid if paid > 0 else math.nan
    return out


def option_return(S0, S1, iv0, iv1, h, cp, structure, cost):
    return option_returns(S0, S1, iv0, iv1, h, cp, structure)[cost]


# ------------------------------------------------------------------ helpers
class IV:
    def __init__(self, ser: Series, idx: dict | None):
        self.ser, self.idx, self.proxy = ser, idx, idx is None

    def at(self, i):
        if self.idx is not None:
            v = self.idx.get(self.ser.d[i])
            return v / 100 if v else math.nan
        v = self.ser.rv20[i]
        return (100 * v + VRP_PROXY) / 100 if not math.isnan(v) else math.nan


def tstat(xs):
    if len(xs) < 3:
        return math.nan
    sd = st.stdev(xs)
    return st.mean(xs) / (sd / math.sqrt(len(xs))) if sd > 0 else math.nan


def declustered(idxs, gap=10):
    out, last = [], -10 ** 9
    for i in sorted(idxs):
        if i - last > gap:
            out.append(i); last = i
    return out


BASE_CACHE: dict = {}


def baseline(ser, iv, cp, structure, h, cost, period):
    key = (ser.tk, cp, structure, h, period)
    if key not in BASE_CACHE:
        xs = {c: [] for c in COST}
        for i in range(62, len(ser.d) - h):
            if (ser.d[i] >= OOS_START) != (period == "OOS"):
                continue
            a, b = iv.at(i), iv.at(i + h)
            if math.isnan(a) or math.isnan(b):
                continue
            for c, v in option_returns(ser.C[i], ser.C[i + h], a, b, h, cp, structure).items():
                xs[c].append(v)
        BASE_CACHE[key] = {c: (st.mean(v) if v else math.nan) for c, v in xs.items()}
    return BASE_CACHE[key][cost]


ROWS: list[dict] = []
EVENTS: list[dict] = []


def score_cell(window, label, split, structure, h, cost, evs):
    """evs: list of (period, ret, base). Adds one results row; each call is one trial."""
    global TRIALS
    TRIALS += 1
    row = {"window": window, "label": label, "split": split, "structure": structure, "h": h, "cost": cost}
    for per in ("IS", "OOS"):
        xs = [r for p, r, b in evs if p == per and not math.isnan(r)]
        ex = [r - b for p, r, b in evs if p == per and not math.isnan(r) and not math.isnan(b)]
        row[f"n_{per}"] = len(xs)
        row[f"mean_{per}"] = round(st.mean(xs), 4) if xs else ""
        row[f"excess_{per}"] = round(st.mean(ex), 4) if ex else ""
        row[f"t_excess_{per}"] = round(tstat(ex), 2) if len(ex) >= 3 else ""
        row[f"win_{per}"] = round(sum(x > 0 for x in xs) / len(xs), 3) if xs else ""
    ok = (cost == "k0.70" and row["n_OOS"] >= 20 and row["excess_OOS"] != "" and row["excess_OOS"] >= 0.10
          and row["t_excess_OOS"] != "" and row["t_excess_OOS"] >= 2 and row["excess_IS"] != "" and row["excess_IS"] > 0)
    row["promising"] = ok
    ROWS.append(row)


def per(ser, i): return "OOS" if ser.d[i] >= OOS_START else "IS"


# ------------------------------------------------------------------ windows
def straddle_ret(ser, i, h, ivv):
    """10-/5-day ATM straddle priced at implied ivv (annualised, decimal), gross, held to expiry."""
    return abs(ser.C[i + h] / ser.C[i] - 1) / (0.798 * ivv * math.sqrt(h / 252)) - 1


def run_M(series, vix, vix9d, vix1d, vxn, fomc):
    spy = series["SPY"]
    fdays = set()
    for d in fomc:
        if d in UNSCHEDULED:
            continue
        nd = d
        while nd not in spy.idx and nd <= spy.d[-1]:
            nd += timedelta(days=1)
        if nd in spy.idx:
            fdays.add(spy.idx[nd])
    # M1: 1-day straddle proxy on FOMC days vs non-FOMC days
    for tk, src, name in (("SPY", vix1d, "VIX1D"), ("SPY", vix9d, "VIX9D"), ("QQQ", vxn, "VXN")):
        ser = series[tk]
        days = {ser.idx[spy.d[i]] for i in fdays if spy.d[i] in ser.idx}
        allv = {"IS": [], "OOS": []}; ev = []
        for i in range(1, len(ser.d)):
            v = src.get(ser.d[i - 1])
            if not v:
                continue
            ret = abs(ser.C[i] / ser.C[i - 1] - 1) / (0.798 * v / 100 / math.sqrt(252)) - 1
            if i in days:
                ev.append((per(ser, i), ret, i))
                EVENTS.append({"window": "M1", "ticker": tk, "date": str(ser.d[i]), "series": name,
                               "move_ratio": round((ret + 1), 3)})
            else:
                allv[per(ser, i)].append(ret)
        base = {p: (st.mean(x) if x else math.nan) for p, x in allv.items()}
        score_cell("M1 FOMC day", f"{tk} vs {name}", "all", "straddle-1d", 1, "gross",
                   [(p, r, base[p]) for p, r, _ in ev])
    # M2: pre-FOMC ATM call, close t-1 -> close t
    ivs = IV(spy, vix)
    for cost in ("gross", "k0.70"):
        ev = []
        for i in sorted(fdays):
            if i < 63:
                continue
            a, b = ivs.at(i - 1), ivs.at(i)
            if math.isnan(a) or math.isnan(b):
                continue
            ret = option_return(spy.C[i - 1], spy.C[i], a, b, 1, "C", "atm", cost)
            ev.append((per(spy, i), ret, baseline(spy, ivs, "C", "atm", 1, cost, per(spy, i))))
        score_cell("M2 pre-FOMC drift", "SPY", "all", "atm", 1, cost, ev)


def run_R(series, vix, vix9d, vix3m, vvix, vxn, gx):
    for tk, iv10, iv5 in (("SPY", vix, vix9d), ("QQQ", vxn, vxn)):
        ser = series[tk]
        for h, src in ((5, iv5), (10, iv10)):
            rets = {}
            for i in range(1, len(ser.d) - h):
                v = src.get(ser.d[i])
                if v:
                    rets[i] = straddle_ret(ser, i, h, v / 100)
            base = {p: st.mean([r for i, r in rets.items() if per(ser, i) == p]) for p in ("IS", "OOS")}
            # R1 gamma
            if tk == "SPY":
                g = {i: gx.get(ser.d[i]) for i in rets if gx.get(ser.d[i]) is not None}
                for lab, cond in (("GEX<0", lambda x: x < 0), ("GEX>=0", lambda x: x >= 0)):
                    sel = declustered([i for i, x in g.items() if cond(x)], gap=h - 1)
                    score_cell("R1 dealer gamma", f"{tk} straddle@implied", lab, "straddle", h, "gross",
                               [(per(ser, i), rets[i], base[per(ser, i)]) for i in sel])
                qs = sorted(g.values()); cuts = [qs[int(len(qs) * k / 5)] for k in range(1, 5)]
                for q in range(5):
                    lo = cuts[q - 1] if q else -math.inf; hi = cuts[q] if q < 4 else math.inf
                    sel = declustered([i for i, x in g.items() if lo <= x < hi], gap=h - 1)
                    score_cell("R1 dealer gamma", f"{tk} straddle@implied", f"GEX quintile {q+1}", "straddle", h,
                               "gross", [(per(ser, i), rets[i], base[per(ser, i)]) for i in sel])
            # R2 regime onset (SPX-based states)
            states = {"R2a VIX jump from calm": [], "R2b full inversion": [], "R2c VVIX >= p90": []}
            vd = [d for d in ser.d]
            prev_inv = False; prev_vv = False
            for i in range(253, len(vd) - h):
                d, dp = vd[i], vd[i - 1]
                v, vp = vix.get(d), vix.get(dp)
                if v and vp:
                    hist = [vix[x] for x in vd[i - 253:i - 1] if x in vix]
                    if hist and vp < sorted(hist)[int(0.3 * len(hist))] and v / vp - 1 >= 0.20:
                        states["R2a VIX jump from calm"].append(i)
                n9, n3 = vix9d.get(d), vix3m.get(d)
                inv = bool(v and n9 and n3 and n9 > v > n3)
                if inv and not prev_inv:
                    states["R2b full inversion"].append(i)
                prev_inv = inv
                vv = vvix.get(d)
                hist = [vvix[x] for x in vd[i - 252:i] if x in vvix]
                hi = bool(vv and hist and vv >= sorted(hist)[int(0.9 * len(hist))])
                if hi and not prev_vv:
                    states["R2c VVIX >= p90"].append(i)
                prev_vv = hi
            for lab, idxs in states.items():
                sel = [i for i in declustered(idxs) if i in rets]
                for i in sel:
                    EVENTS.append({"window": lab, "ticker": tk, "date": str(ser.d[i]), "h": h,
                                   "ret": round(rets[i], 4)})
                score_cell(lab, f"{tk} straddle@implied", "all", "straddle", h, "gross",
                           [(per(ser, i), rets[i], base[per(ser, i)]) for i in sel])


def reversal_cells(window, label, ser_of, iv_of, events, splits):
    """events: list of (ticker, i, cp, tags dict). Scores all/each split x structure x h x cost."""
    for structure in ("atm", "spread"):
        for h in (3, 10):
            for cost in ("gross", "k0.70", "k1.00"):
                buckets = {"all": []}
                for tk, i, cp, tags in events:
                    ser, iv = ser_of[tk], iv_of[tk]
                    if i + h >= len(ser.d):
                        continue
                    a, b = iv.at(i), iv.at(i + h)
                    if math.isnan(a) or math.isnan(b):
                        continue
                    p = per(ser, i)
                    ret = option_return(ser.C[i], ser.C[i + h], a, b, h, cp, structure, cost)
                    item = (p, ret, baseline(ser, iv, cp, structure, h, cost, p))
                    buckets["all"].append(item)
                    for k in splits:
                        buckets.setdefault(f"{k}={tags[k]}", []).append(item)
                for split, evs in buckets.items():
                    score_cell(window, label, split, structure, h, cost, evs)


def run_C(series, ivs, vix, fomc, gx):
    spy = series["SPY"]
    vterc = sorted(vix[d] for d in spy.d if d in vix); t1, t2 = vterc[len(vterc) // 3], vterc[2 * len(vterc) // 3]

    def vix_t(d):
        v = vix.get(d)
        return "na" if v is None else ("low" if v < t1 else "mid" if v < t2 else "high")

    fom = set(fomc)
    # C1 market-wide
    c1 = []
    for tk in ETFS:
        ser = series[tk]
        cand = {"shock": [], "vixspike": [], "fomc": []}
        for i in range(63, len(ser.d) - 10):
            d = ser.d[i]
            if abs(ser.r[i]) > 2.5 * ser.s60[i]:
                cand["shock"].append(i)
            v = vix.get(d); w = [vix.get(ser.d[j]) for j in range(i - 3, i)]
            if v and all(w) and v / min(w) - 1 >= 0.30:
                cand["vixspike"].append(i)
            if (d in fom or (d - timedelta(days=1)) in UNSCHEDULED) and abs(ser.r[i]) > 1.5 * ser.s60[i]:
                cand["fomc"].append(i)
        for trig, idxs in cand.items():
            for i in declustered(idxs):
                move = ser.r[i] if trig != "vixspike" else math.log(ser.C[i] / ser.C[i - 3])
                cp = "C" if move < 0 else "P"
                clv = ser.clv(i)
                tags = {"trigger": trig, "vix": vix_t(ser.d[i]),
                        "close": ("bouncing" if clv >= 0.5 else "at-extreme") if cp == "C" else ("fading" if clv <= 0.5 else "at-extreme"),
                        "gex": ("neg" if gx.get(ser.d[i], 0) < 0 else "pos")}
                c1.append((tk, i, cp, tags))
                EVENTS.append({"window": "C1", "ticker": tk, "date": str(ser.d[i]), "trigger": trig, "side": cp, **tags,
                               "rev_1d": round(-math.copysign(1, move) * math.log(ser.C[i + 1] / ser.C[i]), 4),
                               "rev_3d": round(-math.copysign(1, move) * math.log(ser.C[i + 3] / ser.C[i]), 4),
                               "rev_10d": round(-math.copysign(1, move) * math.log(ser.C[i + 10] / ser.C[i]), 4)})
    reversal_cells("C1 market-wide reversal", "SPY/QQQ/IWM pooled", series, ivs, c1, ["trigger", "vix", "close", "gex"])
    # C2 single stocks, non-earnings
    c2 = []; dropped = 0
    for tk in STOCKS:
        ser = series.get(tk)
        if not ser:
            continue
        for i in declustered([i for i in range(63, len(ser.d) - 10) if abs(ser.r[i]) > 2.5 * ser.s60[i]]):
            if tk in earnings_on(ser.d[i]) or tk in earnings_on(ser.d[i - 1]):
                dropped += 1
                continue
            j = spy.idx.get(ser.d[i])
            if j is None or math.isnan(spy.s60[j]):
                continue
            rs, ss = spy.r[j], spy.s60[j]
            kind = "idio" if abs(rs) < ss else ("market" if rs * ser.r[i] > 0 and abs(rs) > 1.5 * ss else "mixed")
            gap = abs(ser.O[i] - ser.C[i - 1]) / abs(ser.C[i] - ser.C[i - 1]) if ser.C[i] != ser.C[i - 1] else 0
            cp = "C" if ser.r[i] < 0 else "P"; clv = ser.clv(i)
            tags = {"type": kind, "gap": "gap-driven" if gap >= 0.5 else "intraday", "vix": vix_t(ser.d[i]),
                    "close": ("bouncing" if clv >= 0.5 else "at-extreme") if cp == "C" else ("fading" if clv <= 0.5 else "at-extreme"),
                    "iv": "index" if not ivs[tk].proxy else "proxy"}
            c2.append((tk, i, cp, tags))
            EVENTS.append({"window": "C2", "ticker": tk, "date": str(ser.d[i]), "side": cp, **tags,
                           "rev_3d": round(-math.copysign(1, ser.r[i]) * math.log(ser.C[i + 3] / ser.C[i]), 4),
                           "rev_10d": round(-math.copysign(1, ser.r[i]) * math.log(ser.C[i + 10] / ser.C[i]), 4)})
    reversal_cells("C2 single-stock reversal (non-earnings)", "16 stocks pooled", series, ivs, c2,
                   ["type", "gap", "vix", "close", "iv"])
    # C3 IV decay after C1/C2 events with an index vs random days (descriptive)
    c3 = []
    for h in (3, 10):
        for name, evs in (("C1", c1), ("C2 indexed", [e for e in c2 if not ivs[e[0]].proxy])):
            dd, base = [], []
            for tk, i, cp, tags in evs:
                iv = ivs[tk]
                if i + h < len(iv.ser.d) and not math.isnan(iv.at(i)) and not math.isnan(iv.at(i + h)):
                    dd.append(100 * (iv.at(i + h) - iv.at(i)))
            for tk in {e[0] for e in evs}:
                iv = ivs[tk]
                base += [100 * (iv.at(i + h) - iv.at(i)) for i in range(63, len(iv.ser.d) - h)
                         if not math.isnan(iv.at(i)) and not math.isnan(iv.at(i + h))]
            c3.append(f"C3 {name} h={h}: mean IV change after events {st.mean(dd):+.2f} pts (n={len(dd)}) "
                      f"vs random days {st.mean(base):+.2f} pts")
    return dropped, c3


# ------------------------------------------------------------------ main
def main():
    log = [f"run {datetime.now().isoformat(timespec='seconds')}"]
    say = lambda m: print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)
    series = {tk: Series(tk) for tk in ETFS + STOCKS}
    v = {n: vol_index(n) for n in ("VIX", "VIX9D", "VIX1D", "VIX3M", "VVIX", "VXN", "RVX", "VXAPL", "VXAZN", "VXGOG")}
    gx = gex(); fomc = fomc_dates()
    log.append(f"FOMC dates {len(fomc)} ({min(fomc)}..{max(fomc)}); GEX days {len(gx)}; tickers {len(series)}")
    ivs = {tk: IV(series[tk], v.get(IV_MAP.get(tk, ""))) for tk in series}
    say("data loaded"); run_M(series, v["VIX"], v["VIX9D"], v["VIX1D"], v["VXN"], fomc)
    say("M done"); run_R(series, v["VIX"], v["VIX9D"], v["VIX3M"], v["VVIX"], v["VXN"], gx)
    say("R done"); dropped, c3 = run_C(series, ivs, v["VIX"], fomc, gx); say("C done")
    log.append(f"C2 single-stock events dropped for earnings: {dropped}")
    log += c3
    with open(HERE / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys())); w.writeheader(); w.writerows(ROWS)
    keys = sorted({k for e in EVENTS for k in e})
    with open(HERE / "events.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(EVENTS)
    prom = [r for r in ROWS if r["promising"]]
    log.append(f"cells scored (trials this run): {TRIALS}; cumulative trials incl. previous run: {TRIALS + 5}")
    log.append(f"promising cells: {len(prom)}")
    for r in prom:
        log.append(f"  PROMISING {r['window']} | {r['label']} | {r['split']} | {r['structure']} h={r['h']} "
                   f"| excess OOS {r['excess_OOS']} (t {r['t_excess_OOS']}, n {r['n_OOS']}) IS {r['excess_IS']}")
    (HERE / "run.log").write_text("\n".join(log) + "\n")
    print("\n".join(log))


def selftest():
    # put-call parity and delta-strike round trip
    S, K, T, v = 100, 105, 45 / 365, 0.25
    assert abs(bs(S, K, T, v, "C") - bs(S, K, T, v, "P") - (S - K)) < 1e-9
    K25 = strike_for_delta(S, T, v, "C", 0.25)
    d1 = (math.log(S / K25) + 0.5 * v * v * T) / (v * math.sqrt(T))
    assert abs(ncdf(d1) - 0.25) < 1e-6
    Kp = strike_for_delta(S, T, v, "P", 0.25)
    d1p = (math.log(S / Kp) + 0.5 * v * v * T) / (v * math.sqrt(T))
    assert abs((ncdf(d1p) - 1) + 0.25) < 1e-6 and Kp < S < K25
    # unchanged price and IV loses only time value; costs make it worse
    g = option_return(100, 100, 0.2, 0.2, 10, "C", "atm", "gross")
    n = option_return(100, 100, 0.2, 0.2, 10, "C", "atm", "k0.70")
    assert -0.2 < g < 0 and n < g
    # IV crush hurts a call even when price rises a little; spread is less vega-sensitive
    a = option_return(100, 101, 0.35, 0.25, 3, "C", "atm", "gross")
    s = option_return(100, 101, 0.35, 0.25, 3, "C", "spread", "gross")
    assert a < 0 and s > a
    assert declustered([1, 2, 3, 20, 25, 40]) == [1, 20, 40]
    print("selftest ok: atm flat 10d gross", round(g, 3), "net", round(n, 3), "| crush atm", round(a, 3), "spread", round(s, 3))


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
