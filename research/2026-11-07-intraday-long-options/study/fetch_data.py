"""Download and cache the free data for the intraday study (stdlib only).

Usage (from repo root):
    python3 research/2026-11-07-intraday-long-options/study/fetch_data.py

Writes raw responses to study/data/ (kept in git so the run is reproducible: Yahoo's hourly
window rolls forward, so a later re-fetch would not return the same sessions).
Sources:
- Yahoo chart API: 1-hour bars (range 730d) for SPY, QQQ, ^VIX1D, ^VIX, ^VIX9D, ^VXN;
  5-minute bars (range 60d) for SPY and ^VIX1D (worked example only).
- Cboe daily index CSVs (cdn.cboe.com): VIX1D, VIX, VIX9D, VXN.
- Nasdaq historical daily OHLCV (api.nasdaq.com), 2016-10 -> today, SPY, QQQ and 16 stocks.
- federalreserve.gov FOMC calendar pages (statement dates).
- Concretum Group macro event calendar (free public export, no login): CPI, NFP, FOMC, ISM
  release dates and ET times, 2022-01 -> 2026-11 (calendar.concretumgroup.com/api/events/export/).
  Third-party; FOMC dates are cross-checked against federalreserve.gov in the study script.
- The H-MOM1 event list is copied from the prior continuation run (branch
  claude/inspiring-cerf-epxwvd, research/2026-11-07-event-windows/continuation/events.csv)
  with `git show`; it is not re-derived here because it needs the earnings calendar.
"""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
UA = {"User-Agent": "Mozilla/5.0 (research-script)"}
HOURLY = ["SPY", "QQQ", "^VIX1D", "^VIX", "^VIX9D", "^VXN"]
FIVEMIN = ["SPY", "^VIX1D"]
CBOE = ["VIX1D", "VIX", "VIX9D", "VXN"]
DAILY_ETF = ["SPY", "QQQ"]
DAILY_STK = ["NVDA", "TSLA", "MU", "AAPL", "INTC", "AMD", "AMZN", "META", "PLTR", "GOOGL", "MSFT",
             "AVGO", "ORCL", "HOOD", "PFE", "SOFI"]
PRIOR_BRANCH = "origin/claude/inspiring-cerf-epxwvd"
PRIOR_EVENTS = "research/2026-11-07-event-windows/continuation/events.csv"


def get(url: str) -> bytes:
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            if a == 3:
                raise RuntimeError(f"{url}: {e}") from e
            time.sleep(2 ** (a + 1))
    raise AssertionError


def save(name: str, url: str, force: bool = False) -> None:
    p = DATA / name
    if p.exists() and not force:
        return
    p.write_bytes(get(url))
    print(f"saved {name} ({p.stat().st_size} bytes)", flush=True)
    time.sleep(0.5)


def main() -> None:
    DATA.mkdir(exist_ok=True)
    for s in HOURLY:
        q = s.replace("^", "%5E")
        save(f"yh_1h_{s.strip('^')}.json", f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?interval=1h&range=730d")
    for s in FIVEMIN:
        q = s.replace("^", "%5E")
        save(f"yh_5m_{s.strip('^')}.json", f"https://query1.finance.yahoo.com/v8/finance/chart/{q}?interval=5m&range=60d")
    for s in CBOE:
        save(f"cboe_{s}.csv", f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{s}_History.csv")
    for tk in DAILY_ETF + DAILY_STK:
        ac = "etf" if tk in DAILY_ETF else "stocks"
        save(f"nq_{tk}.json", f"https://api.nasdaq.com/api/quote/{tk}/historical?assetclass={ac}"
             f"&fromdate=2016-10-01&limit=9999&todate=2026-11-07")
    for pg in ["fomccalendars.htm", "fomchistorical2020.htm"]:
        save(f"fed_{pg}", f"https://www.federalreserve.gov/monetarypolicy/{pg}")
    save("macro_events.csv", "https://calendar.concretumgroup.com/api/events/export/?start=2022-01-01"
         "&end=2026-11-07&layout=long&include_assumed_time=true&events=cpi,nfp,fomc,ism_mfg,ism_services")
    out = DATA / "prior_continuation_events.csv"
    if not out.exists():
        txt = subprocess.run(["git", "show", f"{PRIOR_BRANCH}:{PRIOR_EVENTS}"], capture_output=True,
                             text=True, check=True).stdout
        out.write_text(txt)
        print(f"copied prior events ({len(txt.splitlines())} lines)")


if __name__ == "__main__":
    sys.exit(main())
