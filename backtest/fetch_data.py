#!/usr/bin/env python3
"""Download free daily data for the option backtest and write backtest/artifact/data.js.

Sources (no key needed):
  - Yahoo Finance chart API: split-adjusted daily closes per stock, SPY, and ^IRX (13-week T-bill yield).
  - S&P 500 member list with sectors (github.com/datasets/s-and-p-500-companies).
  - Cboe index history files: VIX, VIX3M, VIX6M and the five single-stock volatility indexes.

Raw downloads are cached in backtest/data/raw/ (gitignored). Standard library only.

Usage (from the repo root):
  python3 backtest/fetch_data.py            # fetch what is missing, rebuild data.js
  python3 backtest/fetch_data.py --refresh  # refetch everything
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
OUT = os.path.join(HERE, "artifact", "data.js")
UA = {"User-Agent": "Mozilla/5.0 (research-script)"}

# Universe rule: current S&P 500 members, ranked by average daily dollar volume over the latest 60
# trading days, top N. Membership and ranking are as of the build date, so every stock survived to
# 2026: results are flattered by that (see README).
CONSTITUENTS = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
TOP_N = 200
REFERENCE = "SPY"   # market reference for conditions; never traded in the backtest

VOL_INDEXES = ["VIX", "VIX3M", "VIX6M", "VXAPL", "VXAZN", "VXGOG", "VXGS", "VXIBM"]
STOCK_INDEX = {"AAPL": "VXAPL", "AMZN": "VXAZN", "GOOGL": "VXGOG", "GS": "VXGS", "IBM": "VXIBM"}
START = dt.date(2008, 6, 1)   # prices; tests start later, once every input has history


def get(url: str) -> bytes:
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed: {url}: {last}")


def cached(name: str, url: str, refresh: bool) -> bytes:
    path = os.path.join(RAW, name)
    if os.path.exists(path) and not refresh:
        with open(path, "rb") as f:
            return f.read()
    body = get(url)
    with open(path, "wb") as f:
        f.write(body)
    return body


def yahoo(symbol: str, refresh: bool, volume: bool = False):
    """Return {date: close} with split-adjusted (not dividend-adjusted) closes; with volume=True also
    return the average close x volume over the latest 60 days."""
    p1 = int(dt.datetime(START.year, START.month, START.day, tzinfo=dt.timezone.utc).timestamp())
    p2 = int(time.time()) + 86400
    sym = urllib.request.quote(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d"
    res = json.loads(cached(f"yahoo_{symbol.strip('^')}.json", url, refresh))["chart"]["result"][0]
    out = {}
    closes = res["indicators"]["quote"][0]["close"]
    off = res["meta"].get("gmtoffset", 0)
    for ts, c in zip(res["timestamp"], closes):
        if c is not None:
            d = dt.datetime.fromtimestamp(ts + off, dt.timezone.utc).date()
            out[d] = c
    if volume:
        vols = res["indicators"]["quote"][0]["volume"]
        pairs = [(c, v) for c, v in zip(closes, vols) if c is not None and v][-60:]
        return out, (sum(c * v for c, v in pairs) / len(pairs) if pairs else 0.0)
    return out


def cboe(name: str, refresh: bool) -> dict:
    url = f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{name}_History.csv"
    txt = cached(f"cboe_{name}.csv", url, refresh).decode("utf-8", "replace")
    out = {}
    for row in csv.reader(io.StringIO(txt)):
        if len(row) >= 2 and row[0][:1].isdigit():
            m, d, y = row[0].split("/")
            try:
                out[dt.date(int(y), int(m), int(d))] = float(row[-1])   # close is the last column
            except ValueError:
                pass
    return out


def rnd(x):
    if x is None:
        return None
    return round(x, 4) if x < 10 else round(x, 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    os.makedirs(RAW, exist_ok=True)

    members = []
    for row in csv.DictReader(io.StringIO(cached("sp500_constituents.csv", CONSTITUENTS, args.refresh).decode("utf-8"))):
        members.append({"tk": row["Symbol"].replace(".", "-"), "name": row["Security"],
                        "sector": row["GICS Sector"], "group": row["GICS Sub-Industry"]})
    prices, dollar, failed = {}, {}, []
    for k, m in enumerate(members):
        fresh = not os.path.exists(os.path.join(RAW, f"yahoo_{m['tk']}.json")) or args.refresh
        try:
            prices[m["tk"]], dollar[m["tk"]] = yahoo(m["tk"], args.refresh, volume=True)
        except Exception as e:  # noqa: BLE001 - report and continue
            failed.append(f"{m['tk']}: {e}")
        if fresh:
            time.sleep(0.2)
        if k % 50 == 49:
            print(f"  fetched {k + 1}/{len(members)}", flush=True)
    keep = set(sorted(dollar, key=dollar.get, reverse=True)[:TOP_N]) | (set(STOCK_INDEX) & set(prices))
    members = [m for m in members if m["tk"] in keep]
    TICKERS = [m["tk"] for m in members]
    spy = yahoo(REFERENCE, args.refresh)
    vols = {n: cboe(n, args.refresh) for n in VOL_INDEXES}
    irx = yahoo("^IRX", args.refresh)

    # Master calendar: days on which VIX and at least half the stocks have a close.
    days = sorted(d for d in vols["VIX"] if d >= START and sum(d in p for p in prices.values()) >= len(prices) / 2)
    def col(series):
        return [rnd(series.get(d)) for d in days]

    data = {
        "built": dt.date.today().isoformat(),
        "dates": [d.year * 10000 + d.month * 100 + d.day for d in days],
        "tickers": [t for t in TICKERS if t in prices],
        "sector": {m["tk"]: m["sector"] for m in members},
        "group": {m["tk"]: m["group"] for m in members},
        "name": {m["tk"]: m["name"] for m in members},
        "universe": f"The {len(members)} most actively traded current S&P 500 stocks by dollar volume",
        "spy": col(spy),
        "close": {t: col(prices[t]) for t in TICKERS if t in prices},
        "vix": col(vols["VIX"]), "vix3m": col(vols["VIX3M"]), "vix6m": col(vols["VIX6M"]),
        "rate": col(irx),
        "volIndex": {tk: col(vols[ix]) for tk, ix in STOCK_INDEX.items()},
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.BT_DATA = ")
        json.dump(data, f, separators=(",", ":"))
        f.write(";\n")
    print(f"days {len(days)} {days[0]} .. {days[-1]}; tickers {len(data['tickers'])}; "
          f"data.js {os.path.getsize(OUT) / 1e6:.2f} MB")
    late = sum(1 for tk in data["tickers"] if data["close"][tk][0] is None)
    print(f"  {late} stocks start after {days[0]}")
    if failed:
        print("FAILED:", *failed, sep="\n  ")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
