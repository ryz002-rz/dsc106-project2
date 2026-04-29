# DSC 106 — Project 2: Persuasive / Deceptive Visualization

**Group:** Keith Gong · Roxanne Wang · Ryan Zhang
**Course:** DSC 106, Spring 2026
**Proposition:** "China's economic rise has made meaningful climate progress impossible."

## Files

```
project2/
├── index.html            ← the final submission page
├── images/
│   ├── viz1_china_vs_west.png    ← FOR  · Annual emissions change from 1990
│   ├── viz2_renewables.png       ← FOR  · Renewable energy share over time
│   ├── viz3_per_capita.png       ← AGAINST · 2018 per-capita CO₂
│   └── viz4_cumulative.png       ← AGAINST · Cumulative CO₂ since 1960
├── generate_images.py    ← script that produces the four PNGs
└── climate-change.csv    ← source data (World Bank Climate Change Indicators)
```

## Reproducing the visualizations

```bash
python3 generate_images.py
# writes the four PNGs into ./images/
```

Requires `matplotlib` and `numpy` only.

## Deploying to GitHub Pages

1. Copy the `project2/` folder into your portfolio repository.
2. Commit and push.
3. The page will be live at `https://<your-github-username>.github.io/<repo>/project2/`.

GitHub Pages serves `index.html` automatically when a directory is requested,
so no extra configuration is needed. All image references in `index.html` are
relative paths (`images/…`), so they will resolve correctly once deployed.

## Source

World Bank Climate Change Indicators dataset (1960–2018).
Indicators used: `CO2 emissions (kt)`, `CO2 emissions (metric tons per capita)`,
and `Renewable energy consumption (% of total final energy consumption)`.
