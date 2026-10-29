# The Negative-Split Myth

How many marathoners run the second half faster than the first? I counted every one of the 31,912 finishers of the 2014 Boston Marathon, and 2.5% did.

[Live site](https://lyhjeremy.github.io/marathon-negative-split-myth/) · [Write-up](https://lyhjeremy.github.io/marathon-negative-split-myth/overview/)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

- 2.5% of finishers (803 of 31,912) ran a negative split. Another 3.9% finished within 2% of even, and 93.6% slowed by more than that.
- The median second half was 14.0% slower than the first.
- Fade tracks ability: a median 5.3% slowdown for sub-3-hour finishers against 21.7% for runners over 4 hours.
- Women slowed slightly less than men, 13.4% against 14.8%.

The [write-up](https://lyhjeremy.github.io/marathon-negative-split-myth/overview/#yours) lets you enter your own halfway split and finish time and see how your fade compares with the Boston runners in your finish band.

![Histogram of second-half slowdown for 31,912 Boston 2014 finishers, almost all to the right of even pace and peaking around a 12 to 15 percent slowdown](figures/01_slowdown_distribution.png)

## October 2026 upgrade: every Boston year with splits

The 2014 numbers above are unchanged. `multiyear.py` repeats the count for every Boston year with public splits, using the multi-year table built in the companion repo. 2014 turns out to be one of the hardest years to negative split: the second-lowest share and the biggest median fade of the eight.

| Year | Finishers | Negative split | Median fade | Under 3:00 | Over 4:00 |
|---|---|---|---|---|---|
| 2014 | 31,859 | 2.5% | +14.0% | +5.2% | +21.7% |
| 2015 | 26,570 | 7.7% | +7.3% | +3.3% | +12.7% |
| 2016 | 26,613 | 2.6% | +12.1% | +7.1% | +16.5% |
| 2017 | 26,393 | 3.1% | +12.8% | +5.5% | +17.3% |
| 2021 | 15,291 | 4.7% | +11.7% | +4.9% | +19.8% |
| 2022 | 24,745 | 6.9% | +8.3% | +3.8% | +15.1% |
| 2023 | 26,674 | 10.8% | +5.8% | +2.7% | +11.9% |
| 2024 | 25,757 | 2.4% | +13.7% | +6.4% | +19.2% |
| 2013 (halted) | 16,096 | 6.0% | +7.7% | +3.9% | +16.6% |

From `tables/years_splits.csv`. Wheelchair and handcycle entrants are dropped by bib or division. The original 2014 count (31,912) kept 53 wheelchair finishers, one of them a negative split, so the 2014 row here has 31,859 runners with the same 2.5% and 14.0%; its under-3:00 median is 5.2% rather than 5.3% for the same reason. 2013 was stopped at about 4:09 on the race clock, so only the faster part of the field finished; it is listed and left out of comparisons. 2018 and 2019 are missing because the public files have no splits.

The companion repo, [Hitting the Wall](https://github.com/lyhjeremy/marathon-pacing-decay), now has a [live split tool](https://lyhjeremy.github.io/marathon-pacing-decay/#tool) trained on these years and tested on 2024.

## Method

Each runner's race is split at the half-marathon timing mat. First half is the half split; second half is official finish time minus the half split. The ratio second / first above 1 means the runner slowed. A ratio below 1 is a negative split, and 1.00 to 1.02 counts as even.

The analysis is descriptive: shares and medians over the full field, then medians grouped by finish-time band (2:00 to 6:00 in half-hour steps, 5:00 to 6:00 as one band) and by gender. Every finisher is counted and nothing is modeled, so the numbers are exact for this race.

Stack: Python, pandas, NumPy, matplotlib.

## How to run

```bash
pip install -r requirements.txt
python fetch_data.py     # downloads 2014 Boston results to data/
python analyze.py        # writes figures/ and tables/summary.csv
python export_web.py     # writes tables/web_splits.json for the site's charts

# per-year table: build the multi-year data in marathon-pacing-decay first
# (fetch_multiyear.py, build_dataset.py), then
python multiyear.py      # writes tables/years_splits.csv and .json
```

## Repo layout

| Path | Contents |
|---|---|
| `fetch_data.py` | Downloads the results CSV into `data/` (git-ignored) |
| `analyze.py` | Computes the splits, writes four figures and the summary table |
| `figures/` | Slowdown histogram, pacing categories, slowdown by finish band, by gender |
| `export_web.py` | Band histograms, percentiles and medians for the interactive charts, using the same `load()` as `analyze.py` |
| `tables/summary.csv` | Headline numbers |
| `multiyear.py`, `tables/years_splits.*` | The same count for every Boston year with splits |
| `tables/web_splits.json` | Chart data for the site (8 KB) |
| `index.html`, `overview/` | The GitHub Pages site |
| `writeup.md` | Short write-up |

## Data

Official 2014 Boston Marathon results from the public mirror [llimllib/bostonmarathon](https://github.com/llimllib/bostonmarathon). Split columns are cumulative times in decimal minutes. Other years: 2015 to 2017 from a Kaggle mirror, 2021 to 2024 from [williamsorg4/BostonMarathonTimeModel](https://github.com/williamsorg4/BostonMarathonTimeModel); sources and row counts are in the companion repo's `tables/years.csv`.

## Limitations

The headline is one race on one course, and the per-year table shows it was a hard one; the spread between years (2.4% to 10.8% negative splits) says the day matters, and this data can't say how much of that is weather. Boston drops early and puts its hills between miles 16 and 21, which makes an even split harder than on a flat course, and its qualified field is faster than a typical marathon's. The halfway mat is the only checkpoint used, and weather is not modeled. The pacing-categories chart (`figures/02_split_categories.png`) counts "even" as within 2% either side, so its negative-split bar reads 1.5%; the headline rule (ratio below 1) gives 2.5%.

## License

[MIT](LICENSE) © 2026 Jeremy Lee
