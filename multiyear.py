"""
multiyear.py - the 2014 negative-split count, repeated for every Boston year.

Reads the multi-year split table that the companion repo builds:
  ~/data-cache/marathon-pacing-decay/boston_splits.csv.gz
(run fetch_multiyear.py and build_dataset.py in marathon-pacing-decay first).

Same rules as analyze.load(): half split over 30 minutes, finish after the
half, gender M or F. The one difference is that wheelchair and handcycle
entrants are dropped by bib or division here, while analyze.py kept the 2014
wheelchair finishers whose half split was over 30 minutes. The 2014 row is
therefore shown both ways.

Writes tables/years_splits.csv and tables/years_splits.json.
"""
import json, os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.expanduser("~/data-cache/marathon-pacing-decay/boston_splits.csv.gz")


def stats(d):
    r = (d["finish"] - d["half"]) / d["half"]
    fade = (r - 1) * 100
    fh = d["finish"] / 60
    return {"n": int(len(d)), "neg_pct": round(float((r < 1).mean() * 100), 2),
            "even_pct": round(float(((r >= 1) & (r < 1.02)).mean() * 100), 2),
            "median_fade": round(float(fade.median()), 2),
            "sub3_median_fade": round(float(fade[fh < 3].median()), 2),
            "over4_median_fade": round(float(fade[fh > 4].median()), 2),
            "men_neg_pct": round(float((r[d.gender == "M"] < 1).mean() * 100), 2),
            "women_neg_pct": round(float((r[d.gender == "F"] < 1).mean() * 100), 2),
            "median_finish": round(float(d["finish"].median()), 2)}


def main():
    d = pd.read_csv(DATA, dtype={"bib": str})
    d = d[(d["half"] > 30) & (d["finish"] > d["half"]) & d["gender"].isin(["M", "F"])]
    rows = []
    for y, g in d.groupby("year"):
        rows.append({"year": int(y), "comparable": int(y != 2013), **stats(g)})
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(HERE, "tables", "years_splits.csv"), index=False)
    comp = t[t.comparable == 1]
    out = {"source": "boston_splits.csv.gz via multiyear.py; half > 30 min, finish > half, non-runner divisions dropped",
           "note_2014": "tables/summary.csv (31,912 finishers) kept 53 wheelchair entrants (one of them a negative split); this table drops them",
           "years": rows,
           "range_comparable": {k: [float(comp[k].min()), float(comp[k].max())] for k in ("neg_pct", "median_fade")}}
    with open(os.path.join(HERE, "tables", "years_splits.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(t.to_string(index=False))


if __name__ == "__main__":
    main()
