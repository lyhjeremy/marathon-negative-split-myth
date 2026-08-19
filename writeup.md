# The Negative-Split Myth: how 31,912 runners actually paced Boston

**Question.** "Negative split", running the second half faster than the first.
Is the most repeated advice in marathoning. How many runners actually achieve it?

**Data.** Official 2014 Boston Marathon results (public mirror
`llimllib/bostonmarathon`), 31,912 finishers with valid half-marathon splits.
Times are cumulative decimal minutes. First half = half split; second half =
official finish − half split; `ratio = second / first` (>1 means slowing down).

**Results.**
- Negative split (ratio < 1): **2.5%** of finishers.
- Even pacing (within 2%): ~3.9%.
- The remaining ~94% ran a positive split; **median slowdown 14.0%**.
- By finish time, median slowdown rises monotonically: ~5% for sub-3h runners to
  ~22% for runners over 4 hours.
- By gender, women's median slowdown (~13.4%) was slightly lower than men's (~14.8%).

**Interpretation.** The advice is sound but rarely executed: pacing evenly is a
marker of fitness and discipline, and the field overwhelmingly errs toward going
out too fast, never too slow. Boston's net-downhill start exaggerates early speed,
but the lopsided pattern is consistent with findings from many other marathons.

See `analyze.py` for the full computation and `figures/` for the charts.
