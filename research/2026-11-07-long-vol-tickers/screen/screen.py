"""Long-vol ticker screen. Implements screen_spec.md exactly (stdlib only).

Usage (from repo root):
    python3 research/2026-11-07-long-vol-tickers/screen/screen.py \
        --tickers research/2026-11-07-long-vol-tickers/notes/SQ3_candidates.txt \
        --vol-indices VIX,VXN,...   # only those SQ3 marked active
    python3 research/2026-11-07-long-vol-tickers/screen/screen.py --selftest

Downloads are cached in screen/data/ (gitignored). Writes screen/metrics.csv and screen/run.log.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics as st
import sys
import time
import urllib.request
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
START, END = "2016-11-07", "2026-11-06"
IS_END, OOS_START = date(2021, 12, 31), date(2022, 1, 1)
VOL_MAP = {"SPY": "VIX", "QQQ": "VXN", "IWM": "RVX", "AAPL": "VXAPL", "AMZN": "VXAZN",
           "GOOGL": "VXGOG", "GOOG": "VXGOG", "GS": "VXGS", "GLD": "GVZ", "USO": "OVX",
           "EEM": "VXEEM", "SLV": "VXSLV", "XLE": "VXXLE",
           "TLT": "VXTLT", "EWZ": "VXEWZ", "FXI": "VXFXI", "EFA": "VXEFA", "IBM": "VXIBM"}
UA = {"User-Agent": "Mozilla/5.0 (research-script)", "Accept": "application/json, text/csv"}


# ------------------------------------------------------------------ data
def _get(url: str) -> bytes:
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read()
        except Exception:  # network hiccup: back off and retry
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("unreachable")


def load_ohlc(ticker: str) -> list[tuple[date, float, float, float, float]]:
    DATA.mkdir(exist_ok=True)
    cache = DATA / f"{ticker}.json"
    if not cache.exists():
        rows = None
        for cls in ("stocks", "etf"):
            url = (f"https://api.nasdaq.com/api/quote/{ticker}/historical?assetclass={cls}"
                   f"&fromdate={START}&limit=9999&todate={END}")
            d = json.loads(_get(url)).get("data") or {}
            rows = (d.get("tradesTable") or {}).get("rows")
            if rows:
                break
        if not rows:
            raise RuntimeError(f"no data for {ticker}")
        cache.write_text(json.dumps(rows))
    rows = json.loads(cache.read_text())
    num = lambda s: float(str(s).replace("$", "").replace(",", ""))
    out = [(datetime.strptime(r["date"], "%m/%d/%Y").date(), num(r["open"]), num(r["high"]),
            num(r["low"]), num(r["close"])) for r in rows]
    return sorted(out)


def load_vol_index(name: str) -> dict[date, float]:
    DATA.mkdir(exist_ok=True)
    cache = DATA / f"{name}.csv"
    if not cache.exists():
        cache.write_bytes(_get(f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{name}_History.csv"))
    out = {}
    for row in csv.DictReader(cache.read_text().splitlines()):
        try:
            out[datetime.strptime(row["DATE"], "%m/%d/%Y").date()] = float(row["CLOSE"])
        except (KeyError, ValueError):
            continue
    return out


# ------------------------------------------------------------------ metrics
def pct_rank_in_window(xs: list[float], i: int, n: int) -> float | None:
    if i < n - 1:
        return None
    win = xs[i - n + 1:i + 1]
    return sum(1 for v in win if v <= xs[i]) / n


def metrics(bars, vol=None, d_from=None, d_to=None) -> dict:
    """All metrics for days t whose date lies in [d_from, d_to] (lookbacks may reach earlier)."""
    dts = [b[0] for b in bars]; H = [b[2] for b in bars]; L = [b[3] for b in bars]; C = [b[4] for b in bars]
    n = len(bars)
    r = [math.nan] + [math.log(C[i] / C[i - 1]) for i in range(1, n)]
    split_flags = [str(dts[i]) for i in range(1, n) if abs(r[i]) > 0.4]
    tr = [math.nan] + [max(H[i] - L[i], abs(H[i] - C[i - 1]), abs(L[i] - C[i - 1])) for i in range(1, n)]
    atr = [math.nan] * n
    for i in range(20, n):
        atr[i] = sum(tr[i - 19:i + 1]) / 20
    atrp = [atr[i] / C[i] if not math.isnan(atr[i]) else math.nan for i in range(n)]

    tail_hits = tail_n = 0; excur = []; swing = []; ratios = []; compressed = []; vrp = []
    for t in range(60, n - 21):
        if (d_from and dts[t] < d_from) or (d_to and dts[t] > d_to):
            continue
        rv60 = st.stdev(r[t - 59:t + 1]) * math.sqrt(252)
        s10 = rv60 * math.sqrt(10 / 252)
        if s10 <= 0:
            continue
        m10 = math.log(C[t + 10] / C[t])
        tail_n += 1; tail_hits += abs(m10) > s10
        ex = max(max(H[t + i] / C[t] - 1, 1 - L[t + i] / C[t]) for i in range(1, 11))
        excur.append(ex / s10); swing.append(abs(m10))
        if t >= 140 and not math.isnan(atr[t]):
            ratios.append((max(H[t + 1:t + 11]) - min(L[t + 1:t + 11])) / atr[t])
            pr = pct_rank_in_window(atrp, t, 120)
            compressed.append(pr is not None and pr <= 0.20)
        if vol and dts[t] in vol:
            fwd = r[t + 1:t + 22]
            vrp.append(vol[dts[t]] - 100 * st.stdev(fwd) * math.sqrt(252))
    if tail_n < 250:
        return {"n_days": tail_n}
    q80 = sorted(ratios)[int(0.8 * (len(ratios) - 1))]
    comp_hits = [ra >= q80 for ra, c in zip(ratios, compressed) if c]
    return {
        "n_days": tail_n,
        "tail10": tail_hits / tail_n,
        "excur10": st.median(excur),
        "expand": (sum(comp_hits) / len(comp_hits)) / 0.20 if comp_hits else math.nan,
        "n_compressed": len(comp_hits),
        "swing10": st.median(swing),
        "vrp": st.mean(vrp) if len(vrp) > 250 else math.nan,
        "split_flags": ";".join(split_flags),
    }


def pct_ranks(vals: dict[str, float]) -> dict[str, float]:
    good = {k: v for k, v in vals.items() if not math.isnan(v)}
    order = sorted(good, key=good.get)
    n = len(order)
    return {k: (i / (n - 1) if n > 1 else 1.0) for i, k in enumerate(order)}


def score(rows: dict[str, dict], liq: dict[str, float]) -> dict[str, float]:
    ranks = {m: pct_ranks({t: rows[t].get(m, math.nan) for t in rows}) for m in ("tail10", "excur10", "expand")}
    out = {}
    for t in rows:
        parts = [ranks[m].get(t) for m in ranks] + [liq[t]]
        parts = [p for p in parts if p is not None]
        out[t] = sum(parts) / len(parts) if len(parts) == 4 else math.nan
    return out


def rank_order(sc: dict[str, float], liq: dict[str, float]) -> list[str]:
    return sorted((t for t in sc if not math.isnan(sc[t])), key=lambda t: (-sc[t], -liq[t]))


# ------------------------------------------------------------------ main
def run(tickers: list[str], active_vol: set[str]) -> None:
    log = [f"run {datetime.now().isoformat(timespec='seconds')}  tickers={len(tickers)}  vol={sorted(active_vol)}"]
    N = len(tickers)
    liq = {t: 1 - i / (N - 1) for i, t in enumerate(tickers)}
    full, ins, oos = {}, {}, {}
    for t in tickers:
        try:
            bars = load_ohlc(t)
        except Exception as e:
            log.append(f"{t}: DATA ERROR {e}"); continue
        vname = VOL_MAP.get(t)
        vol = load_vol_index(vname) if vname in active_vol else None
        full[t] = metrics(bars, vol)
        ins[t] = metrics(bars, None, None, IS_END)
        oos[t] = metrics(bars, None, OOS_START, None)
        log.append(f"{t}: bars={len(bars)} {bars[0][0]}..{bars[-1][0]} vol={vname if vol else '-'} "
                   f"split_flags={full[t].get('split_flags') or 'none'}")
        time.sleep(0.5)
    liq = {t: liq[t] for t in full}
    sc, sc_is, sc_oos = score(full, liq), score(ins, liq), score(oos, liq)
    order, o_is, o_oos = rank_order(sc, liq), rank_order(sc_is, liq), rank_order(sc_oos, liq)
    indexed = [full[t]["vrp"] for t in full if not math.isnan(full[t].get("vrp", math.nan))]
    vrp_med = st.median(indexed) if indexed else math.nan
    with open(HERE / "metrics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "ticker", "score", "liq", "tail10", "excur10", "expand", "n_compressed",
                    "swing10", "vrp", "rank_IS", "rank_OOS", "unstable", "implied_rich"])
        for i, t in enumerate(order, 1):
            m = full[t]
            ri = o_is.index(t) + 1 if t in o_is else ""
            ro = o_oos.index(t) + 1 if t in o_oos else ""
            unstable = bool(ri and ro and abs(ri - ro) > 10)
            rich = (not math.isnan(m["vrp"])) and m["vrp"] > vrp_med
            w.writerow([i, t, f"{sc[t]:.3f}", f"{liq[t]:.3f}", f"{m['tail10']:.3f}", f"{m['excur10']:.3f}",
                        f"{m['expand']:.3f}", m["n_compressed"], f"{m['swing10']:.4f}",
                        "" if math.isnan(m["vrp"]) else f"{m['vrp']:.2f}", ri, ro, unstable, rich])
    log.append(f"wrote {HERE/'metrics.csv'}; top10={order[:10]}")
    (HERE / "run.log").write_text("\n".join(log) + "\n")
    print("\n".join(log))


def selftest() -> None:
    import random
    random.seed(7)
    bars, c, d0 = [], 100.0, date(2016, 1, 1)
    for i in range(1500):
        ret = random.gauss(0, 0.01)
        o = c; c = c * math.exp(ret)
        bars.append((date.fromordinal(d0.toordinal() + i), o, max(o, c) * 1.003, min(o, c) * 0.997, c))
    m = metrics(bars)
    assert 0.25 < m["tail10"] < 0.40, m  # iid normal: ~0.317
    assert m["excur10"] > 0.8, m
    assert 0.5 < m["expand"] < 3.0, m  # iid null is ~1.9 (ATR noise), see screen_spec.md
    assert m["split_flags"] == ""
    sc = score({"A": m, "B": {**m, "tail10": m["tail10"] + .1}}, {"A": 1.0, "B": 0.0})
    assert set(sc) == {"A", "B"}
    print("selftest ok:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in m.items()})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers"); ap.add_argument("--vol-indices", default="")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); sys.exit(0)
    tick = [l.strip().upper() for l in Path(a.tickers).read_text().splitlines() if l.strip() and not l.startswith("#")]
    run(tick, {v.strip().upper() for v in a.vol_indices.split(",") if v.strip()})
