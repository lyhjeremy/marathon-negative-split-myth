# The Negative-Split Myth

Coaches preach the **negative split** — run the second half of a marathon faster
than the first. So how many runners actually do it? Across **31,912 finishers** of
the 2014 Boston Marathon, only **2.5%** did; the median runner slowed **14%**.

> 🌐 **Read the story:** https://lyhjeremy.github.io/marathon-negative-split-myth/

## Findings
- **2.5%** of finishers ran a true negative split; ~94% slowed down.
- The **median second half was 14% slower** than the first.
- Pacing tracks ability: **sub-3h ≈ +5%** slowdown vs **over-4h ≈ +22%**.
- Women paced slightly more evenly than men (≈13.4% vs ≈14.8%).

## Reproduce
```bash
pip install -r requirements.txt
python fetch_data.py     # downloads 2014 Boston results to data/
python analyze.py        # writes figures/ and tables/summary.csv
```

## Data
Official 2014 Boston Marathon results via the public mirror
[llimllib/bostonmarathon](https://github.com/llimllib/bostonmarathon). Split
columns are cumulative times in decimal minutes; first half = the half-marathon
split, second half = finish − half. Raw data is downloaded by `fetch_data.py` and
is git-ignored; the repo ships the analysis code, figures, and summary table.

## License
[MIT](LICENSE) © 2026 Jeremy Lee
