# momentum_overlay.py  -  desk model "Momentum Overlay"   (legacy, runs on the desk PC)
# Scheduled by Windows Task Scheduler via run_momentum.bat, first business day of the month 08:30.
# Reads the nightly price export made by the old Eikon macro and writes target weights for the desk.
#
# Author: desk quant (left in 2025).  Do not change the maths without telling the PM.

import sys
import numpy as np
import pandas as pd

EXPORT = r"C:\Desk\exports\prices_export.csv"        # columns: ric, price_date, close_last, close_official
OUTDIR = r"C:\Desk\models\momentum\output"
LOOKBACK_MONTHS = 3
MIN_OBS = 120
TOP_N = 20
CAP = 0.10


def run(month_end, export=EXPORT, outdir=OUTDIR):
    h = pd.read_csv(export, parse_dates=["price_date"])
    # the export is split-adjusted (Eikon history). use the last trade, official close if there is no trade
    h["price"] = h.close_last.fillna(h.close_official)
    wide = h.pivot(index="price_date", columns="ric", values="price").sort_index()

    me = pd.Timestamp(month_end)
    w = wide[wide.index <= me]
    w = w.loc[:, w.notna().sum() >= MIN_OBS]
    p_now = w.ffill().iloc[-1]
    start = me - pd.offsets.MonthEnd(LOOKBACK_MONTHS)
    p_then = w[w.index <= start].ffill().iloc[-1]
    score = (p_now / p_then - 1).dropna()

    rets = np.log(w.ffill()).diff().iloc[-63:]
    vol = rets.std() * np.sqrt(252)

    top = score.sort_values(ascending=False).head(TOP_N)
    iv = 1 / vol[top.index]
    wt = iv / iv.sum()
    for _ in range(10):                       # cap at 10%, spread the excess pro rata
        over = wt > CAP
        if not over.any():
            break
        excess = (wt[over] - CAP).sum()
        wt[over] = CAP
        wt[~over] += excess * wt[~over] / wt[~over].sum()

    out = pd.DataFrame({"ric": top.index, "score": top.values.round(8), "weight": wt.values.round(8)})
    out.to_csv(rf"{outdir}\target_weights_{me:%Y-%m}.csv", index=False)
    return out


if __name__ == "__main__":
    # run for the month that just ended (uses the PC's local clock)
    today = pd.Timestamp.now()
    run(today - pd.offsets.MonthEnd(1) if today.day > 0 else today)
    sys.exit(0)
