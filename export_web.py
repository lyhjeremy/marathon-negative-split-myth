"""
export_web.py - aggregates for the interactive charts on the write-up page.
Reads the same data with analyze.load(), so the definitions match analyze.py
exactly; it changes no result. Writes tables/web_splits.json (a few KB).
"""
import json, os
import numpy as np
import pandas as pd
from analyze import load, HERE

BANDS = [(120, 150, "2:00-2:30"), (150, 180, "2:30-3:00"), (180, 210, "3:00-3:30"), (210, 240, "3:30-4:00"),
         (240, 270, "4:00-4:30"), (270, 300, "4:30-5:00"), (300, 360, "5:00-6:00")]


def hist(s):
    c = np.clip(s.values, -15, 60)
    h, _ = np.histogram(c, bins=np.arange(-15, 61, 1))
    return h.tolist()


def stats(d):
    return {"n": int(len(d)),
            "neg_pct": round(float((d["ratio"] < 1).mean() * 100), 2),
            "even_pct": round(float(((d["ratio"] >= 1) & (d["ratio"] < 1.02)).mean() * 100), 2),
            "median_fade": round(float(d["slowdown_pct"].median()), 2),
            "median_first": round(float(d["half"].median()), 2),
            "median_second": round(float(d["second"].median()), 2),
            "fade_pctiles": [round(float(v), 2) for v in np.percentile(d["slowdown_pct"], range(0, 101))],
            "hist": hist(d["slowdown_pct"])}


def main():
    df = load()
    out = {"source": "data/boston_2014.csv via analyze.load()", "hist_bins": "1% bins from -15 to 60, values clipped into the end bins",
           "all": stats(df), "bands": [], "gender": {}}
    for lo, hi, lab in BANDS:
        d = df[(df.official > lo) & (df.official <= hi)]
        out["bands"].append(dict(label=lab, lo=lo, hi=hi, **stats(d)))
    for g, name in [("M", "men"), ("W", "women")]:
        d = df[df.gender == g]
        out["gender"][name] = {k: v for k, v in stats(d).items() if k not in ("fade_pctiles", "hist")}
    with open(os.path.join(HERE, "tables", "web_splits.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    a = out["all"]
    print(a["n"], a["neg_pct"], a["even_pct"], a["median_fade"])
    for b in out["bands"]:
        print(b["label"], b["n"], b["median_fade"], b["median_first"], b["median_second"], b["neg_pct"])
    print(out["gender"])


if __name__ == "__main__":
    main()
