#!/usr/bin/env python3
"""Fit and test the implied-volatility estimate used when no option quotes are available.

Five stocks have a Cboe volatility index (a real 30-day implied volatility): AAPL, AMZN, GOOGL,
GS, IBM. For those, regress the index on things computable for any stock:

    IV30 = a + b1 * RV20 + b2 * RV60 + b3 * VIX        (all in annualised volatility points)

RV20 / RV60 are the stock's realised volatility over the prior 20 / 60 trading days, using closes
up to and including the day itself. The fit uses the first half of the history only; the error is
then measured on the second half and, separately, on each stock when it is left out of the fit.

Writes backtest/artifact/iv_model.js. Standard library only. Run after fetch_data.py.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "artifact", "data.js")
OUT = os.path.join(HERE, "artifact", "iv_model.js")
SPLIT = 20190101   # fit before, test from


def load():
    txt = open(DATA, encoding="utf-8").read()
    return json.loads(txt[txt.index("{"):txt.rindex("}") + 1])


def realised(close, i, n):
    """Annualised stdev (in points) of the n daily log returns ending at day i, or None."""
    if i < n:
        return None
    rs = []
    for k in range(i - n + 1, i + 1):
        a, b = close[k - 1], close[k]
        if a is None or b is None:
            return None
        rs.append(math.log(b / a))
    m = sum(rs) / n
    return 100 * math.sqrt(252 * sum((r - m) ** 2 for r in rs) / (n - 1))


def solve(A, y):
    """Least squares via normal equations with Gaussian elimination."""
    k = len(A[0])
    M = [[sum(r[i] * r[j] for r in A) for j in range(k)] + [sum(r[i] * t for r, t in zip(A, y))] for i in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(k):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[i][k] / M[i][i] for i in range(k)]


def stats(rows, coef):
    err = [sum(c * x for c, x in zip(coef, r[0])) - r[1] for r in rows]
    n = len(err)
    my = sum(r[1] for r in rows) / n
    ss_res = sum(e * e for e in err)
    ss_tot = sum((r[1] - my) ** 2 for r in rows)
    return {"n": n, "bias": sum(err) / n, "mae": sum(abs(e) for e in err) / n,
            "rmse": math.sqrt(ss_res / n), "r2": 1 - ss_res / ss_tot,
            "mape": 100 * sum(abs(e) / r[1] for e, r in zip(err, rows)) / n}


def main() -> int:
    d = load()
    dates, vix = d["dates"], d["vix"]
    rows = {}   # ticker -> [(features, target, date)]
    for tk, idx in d["volIndex"].items():
        close = d["close"][tk]
        out = []
        for i, day in enumerate(dates):
            if idx[i] is None or vix[i] is None:
                continue
            r20, r60 = realised(close, i, 20), realised(close, i, 60)
            if r20 is None or r60 is None:
                continue
            out.append(([1.0, r20, r60, vix[i]], idx[i], day))
        rows[tk] = out

    allrows = [r for v in rows.values() for r in v]
    fit = [r for r in allrows if r[2] < SPLIT]
    test = [r for r in allrows if r[2] >= SPLIT]
    coef = solve([r[0] for r in fit], [r[1] for r in fit])
    s_fit, s_test = stats(fit, coef), stats(test, coef)

    # The simpler rule used in an earlier run: RV20 + a constant premium (premium fitted on the same half).
    prem = sum(r[1] - r[0][1] for r in fit) / len(fit)
    s_simple = stats(test, [prem, 1.0, 0.0, 0.0])

    loo = {}
    for tk in rows:
        others = [r for t, v in rows.items() if t != tk for r in v if r[2] < SPLIT]
        c = solve([r[0] for r in others], [r[1] for r in others])
        loo[tk] = stats([r for r in rows[tk] if r[2] >= SPLIT], c)

    model = {
        "formula": "IV30 = a + b1*RV20 + b2*RV60 + b3*VIX",
        "coef": {"a": coef[0], "rv20": coef[1], "rv60": coef[2], "vix": coef[3]},
        "fitPeriod": [min(r[2] for r in fit), max(r[2] for r in fit)],
        "testPeriod": [min(r[2] for r in test), max(r[2] for r in test)],
        "fit": s_fit, "test": s_test,
        "simpleRule": {"premium": prem, "test": s_simple},
        "leaveOneOut": loo,
        "stocks": list(rows),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.BT_IV = ")
        json.dump(model, f, indent=1)
        f.write(";\n")

    print("coef: a=%.2f rv20=%.3f rv60=%.3f vix=%.3f" % tuple(coef))
    for name, s in (("fit half", s_fit), ("test half", s_test), ("RV20+%.1f rule, test half" % prem, s_simple)):
        print(f"{name:<28} n={s['n']:>6} bias={s['bias']:+.2f} MAE={s['mae']:.2f} pts ({s['mape']:.1f}%) R2={s['r2']:.2f}")
    for tk, s in loo.items():
        print(f"  left out {tk:<6} test half: bias={s['bias']:+.2f} MAE={s['mae']:.2f} pts ({s['mape']:.1f}%) R2={s['r2']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
