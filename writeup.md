# The Negative-Split Myth: how 31,912 runners paced Boston

Run the second half of a marathon faster than the first. That is the negative split, and it is the most repeated pacing advice in the sport. I have run fourteen marathons and wanted to know how many people in a big field manage it, so I took one full field and counted.

The field is the 2014 Boston Marathon, from the public `llimllib/bostonmarathon` mirror of the official results: 31,912 finishers with a valid half-marathon split. Times are cumulative decimal minutes. The first half is the half split, the second half is official finish minus the half split, and `ratio = second / first`, so a ratio above 1 means the runner slowed down.

## What the split times show

Only 2.5% of finishers (803 runners) ran a negative split, meaning a ratio below 1. Another 3.9% ran close to even (a ratio of 1.00 to 1.02), and the other 93.6% slowed by more than 2%. The median runner's second half was 14.0% slower than the first.

The fade grows with finish time at every step, from a median 4.5% for the 2:00 to 2:30 group to 26.8% for those who took 5:00 to 6:00. Runners under 3 hours slowed 5.3%; runners over 4 hours slowed 21.7%. Women's median slowdown (13.4%) was slightly lower than men's (14.8%).

So the advice holds up, but very few people carry it out. Even pacing goes with fitness, and the field's errors run almost entirely toward starting too fast. What the data can't separate is how much even pacing causes faster times and how much fitter runners simply have more left at halfway.

## Where this could mislead

It is one race on one course. Boston's net-downhill start invites fast early miles and its hills come late, so some of the slowdown belongs to the course. The halfway mat is the only checkpoint I used, and weather is not modeled. One chart also uses a different rule from the text: `figures/02_split_categories.png` bins "even" as within 2% either side, so its negative-split bar shows 1.5% where the headline figure is 2.5%.

## October 2026 upgrade

One race left open whether 2014 was typical, so I ran the same count on every Boston year with public splits: 2014 to 2017 and 2021 to 2024 (`multiyear.py`, `tables/years_splits.csv`). The share of negative splits ranged from 2.4% in 2024 to 10.8% in 2023, and the median second-half fade from 5.8% to 14.0%. 2014 had the second-lowest share and the biggest fade of the eight, so it was close to the worst year in the set to try this advice. The two numbers move together: in years when the field fades less, more runners manage a negative split. Fast runners still fade least in every year, from 2.7% (2023) to 7.1% (2016) for the under-3:00 group.

Two details. The original 2014 count kept 53 wheelchair finishers whose half split was over 30 minutes; the per-year table drops them, which leaves the 2014 share and median unchanged at 2.5% and 14.0%. The 2013 race was halted, so its finishers are the faster part of the field and it is left out of the comparison.

The companion study now has a live split tool that predicts a finish band, wall risk and pacing type from the splits you have so far, trained on these years and tested on 2024: https://lyhjeremy.github.io/marathon-pacing-decay/#tool

See `analyze.py` and `multiyear.py` for the computation and `figures/` for the charts.
