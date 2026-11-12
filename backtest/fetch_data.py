#!/usr/bin/env python3
"""Download free daily data for the option backtest and write backtest/artifact/data.js.

Sources (no key needed):
  - Yahoo Finance chart API: split-adjusted daily closes per stock, and ^IRX (13-week T-bill yield).
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

# Large, liquid, optionable US stocks across sectors. Chosen in 2026, so the list is made of
# companies that survived to 2026: results are flattered by that (see README).
TICKERS = """AAPL MSFT AMZN GOOGL META NVDA TSLA AVGO AMD INTC MU ORCL CSCO IBM QCOM TXN ADBE CRM NFLX PYPL
JPM BAC C WFC GS MS AXP V MA BLK
JNJ PFE MRK ABBV LLY UNH BMY GILD AMGN CVS
XOM CVX COP SLB
BA CAT GE HON UPS LMT MMM
WMT COST HD NKE MCD SBUX DIS KO PEP PG
T VZ F GM""".split()
SECTOR = {}
for sec, names in (("Technology", TICKERS[0:20]), ("Financials", TICKERS[20:30]), ("Health care", TICKERS[30:40]),
                   ("Energy", TICKERS[40:44]), ("Industrials", TICKERS[44:51]), ("Consumer", TICKERS[51:61]),
                   ("Telecom and autos", TICKERS[61:65])):
    for n in names:
        SECTOR[n] = sec

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


def yahoo(symbol: str, refresh: bool) -> dict:
    """Return {date: close} with split-adjusted (not dividend-adjusted) closes."""
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

    prices, failed = {}, []
    for tk in TICKERS:
        try:
            prices[tk] = yahoo(tk, args.refresh)
        except Exception as e:  # noqa: BLE001 - report and continue
            failed.append(f"{tk}: {e}")
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
        "sector": SECTOR,
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
    for tk in data["tickers"]:
        first = next(d for d, c in zip(days, data["close"][tk]) if c is not None)
        if first > days[0]:
            print(f"  {tk} starts {first}")
    if failed:
        print("FAILED:", *failed, sep="\n  ")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
