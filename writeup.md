# The Negative-Split Myth: how 31,912 runners paced Boston

**Question.** A negative split means running the second half of a marathon faster than the first. It is the most repeated pacing advice in the sport. How many runners actually manage it?

**Data.** Official 2014 Boston Marathon results from the public mirror `llimllib/bostonmarathon`: 31,912 finishers with valid half-marathon splits. Times are cumulative decimal minutes. First half is the half split; second half is official finish minus the half split. `ratio = second / first`, so a ratio above 1 means the runner slowed down.

**Results.**

- Negative split (ratio below 1): 2.5% of finishers, 803 runners.
- Even pacing (ratio 1.00 to 1.02): 3.9%.
- Everyone else, 93.6%, slowed by more than 2%. The median slowdown was 14.0%.
- By finish time, the median slowdown rises at every step, from 4.5% for 2:00 to 2:30 finishers to 26.8% for 5:00 to 6:00 finishers. Sub-3-hour runners slowed 5.3%; runners over 4 hours slowed 21.7%.
- Women's median slowdown (13.4%) was slightly lower than men's (14.8%).

**Interpretation.** The advice is sound but rarely carried out. Even pacing goes with fitness, and the field's errors run almost entirely toward starting too fast. The data cannot say how much even pacing causes faster times and how much fitter runners simply have more in reserve at halfway.

**Limitations.** One race, one course. Boston's net-downhill start encourages fast early miles and its hills come late, so some of the slowdown belongs to the course. The halfway mat is the only checkpoint used, and weather is not modeled. `figures/02_split_categories.png` bins "even" as within 2% either side, so its negative-split bar shows 1.5% rather than 2.5%.

See `analyze.py` for the computation and `figures/` for the charts.
