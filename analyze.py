"""
analyze.py - The Negative-Split Myth (Boston Marathon 2014)
===========================================================
Do marathoners actually run the second half faster than the first ("negative
split"), as coaches advise? We measure every finisher's first-half vs second-half
time and ask who, if anyone, manages it.

Split columns are cumulative times in decimal minutes. First half = the half-
marathon split; second half = official finish - half split.

Outputs: figures/*.png and tables/summary.csv
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
FIG = os.path.join(HERE, "figures")
TAB = os.path.join(HERE, "tables")
INK, GOLD, TEAL, CORAL, GREEN = "#1a1a2e", "#D4A537", "#15868C", "#E0567A", "#1f9d6b"

plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200, "font.size": 12,
    "axes.edgecolor": "#888", "axes.grid": True, "grid.color": "#e8e2d4",
    "axes.axisbelow": True, "figure.facecolor": "white", "axes.facecolor": "white",
})


def load():
    df = pd.read_csv(os.path.join(HERE, "data", "boston_2014.csv"))
    for c in ["half", "official", "5k", "40k"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["half", "official"])
    df = df[(df["half"] > 30) & (df["official"] > df["half"])]
    df["second"] = df["official"] - df["half"]
    df["ratio"] = df["second"] / df["half"]          # >1 = slowed down
    df["slowdown_pct"] = (df["ratio"] - 1) * 100
    df["gender"] = df["gender"].astype(str).str.upper().str[0]
    df = df[df["gender"].isin(["M", "W", "F"])].replace({"F": "W"})
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    return df


def main():
    os.makedirs(FIG, exist_ok=True); os.makedirs(TAB, exist_ok=True)
    df = load()
    n = len(df)
    neg = (df["ratio"] < 1).mean()
    even = ((df["ratio"] >= 1.0) & (df["ratio"] < 1.02)).mean()
    med_slow = df["slowdown_pct"].median()
    print(f"Finishers analyzed: {n:,}")
    print(f"Negative split (2nd half faster): {neg*100:.1f}%")
    print(f"Within 2% (even):                 {even*100:.1f}%")
    print(f"Median second-half slowdown:      {med_slow:.1f}%")

    # ---- Fig 1: distribution of slowdown ----
    fig, ax = plt.subplots(figsize=(8, 4.6))
    d = df["slowdown_pct"].clip(-15, 60)
    ax.hist(d, bins=80, color=TEAL, alpha=0.85)
    ax.axvline(0, color=INK, lw=2, ls="--", label="even pace")
    ax.axvline(med_slow, color=CORAL, lw=2, label=f"median +{med_slow:.0f}%")
    ax.set_xlabel("Second half slower than first (%)")
    ax.set_ylabel("Runners")
    ax.set_title("Almost everyone slows down in the second half", color=INK, weight="bold")
    ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/01_slowdown_distribution.png"); plt.close(fig)

    # ---- Fig 2: negative vs even vs positive ----
    cats = pd.cut(df["ratio"], [-9, 0.99, 1.02, 9], labels=["Negative split", "Even (±2%)", "Positive split"])
    share = cats.value_counts(normalize=True).reindex(["Negative split", "Even (±2%)", "Positive split"]) * 100
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    bars = ax.bar(share.index, share.values, color=[GREEN, GOLD, CORAL])
    for b, v in zip(bars, share.values):
        ax.text(b.get_x() + b.get_width()/2, v + 1, f"{v:.1f}%", ha="center", weight="bold")
    ax.set_ylabel("Share of finishers (%)"); ax.set_ylim(0, max(share.values)*1.15)
    ax.set_title("How Boston 2014 paced its two halves", color=INK, weight="bold")
    fig.tight_layout(); fig.savefig(f"{FIG}/02_split_categories.png"); plt.close(fig)

    # ---- Fig 3: faster runners pace more evenly ----
    df["finish_h"] = df["official"] / 60
    bins = pd.cut(df["finish_h"], [2, 2.5, 3, 3.5, 4, 4.5, 5, 6])
    g = df.groupby(bins, observed=True)["slowdown_pct"].median()
    fig, ax = plt.subplots(figsize=(8, 4.6))
    xlabels = ["2-2.5h", "2.5-3h", "3-3.5h", "3.5-4h", "4-4.5h", "4.5-5h", "5-6h"]
    ax.plot(range(len(g)), g.values, "-o", color=TEAL, lw=2.5, ms=7)
    ax.set_xticks(range(len(g))); ax.set_xticklabels(xlabels)
    ax.set_xlabel("Finish time"); ax.set_ylabel("Median second-half slowdown (%)")
    ax.set_title("The faster you finish, the more evenly you paced", color=INK, weight="bold")
    fig.tight_layout(); fig.savefig(f"{FIG}/03_slowdown_by_finish.png"); plt.close(fig)

    # ---- Fig 4: by gender ----
    gg = df.groupby("gender")["slowdown_pct"].median()
    df["neg"] = (df["ratio"] < 1)
    negg = df.groupby("gender")["neg"].mean() * 100
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    names = {"M": "Men", "W": "Women"}
    order = [g for g in ["M", "W"] if g in gg.index]
    bars = ax.bar([names[o] for o in order], [gg[o] for o in order], color=[INK, CORAL])
    for b, o in zip(bars, order):
        ax.text(b.get_x()+b.get_width()/2, gg[o]+0.3, f"+{gg[o]:.1f}%\n({negg[o]:.1f}% neg-split)", ha="center", weight="bold", fontsize=10)
    ax.set_ylabel("Median second-half slowdown (%)")
    ax.set_title("Women paced slightly more evenly than men", color=INK, weight="bold")
    fig.tight_layout(); fig.savefig(f"{FIG}/04_by_gender.png"); plt.close(fig)

    # ---- summary table ----
    summary = pd.DataFrame({
        "metric": ["finishers", "negative_split_pct", "even_within_2pct", "median_slowdown_pct",
                   "men_median_slowdown", "women_median_slowdown",
                   "sub3_median_slowdown", "over4h_median_slowdown"],
        "value": [n, round(neg*100, 2), round(even*100, 2), round(med_slow, 2),
                  round(gg.get("M", np.nan), 2), round(gg.get("W", np.nan), 2),
                  round(df[df.finish_h < 3]["slowdown_pct"].median(), 2),
                  round(df[df.finish_h > 4]["slowdown_pct"].median(), 2)],
    })
    summary.to_csv(f"{TAB}/summary.csv", index=False)
    print("\nSaved figures + tables/summary.csv")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
