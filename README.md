# Democracy, Income and Digital Transparency

**Team Yellow** · Data Science coursework, 2026

Do more democratic countries have more digital transparency, holding income constant? This project combines three public datasets for 2025 to find out:

- **World Bank GovTech Dataset** → digital transparency (outcome)
- **V-Dem** → democracy (predictor)
- **World Bank WDI** → GDP per capita (control)

## Hypothesis

- **H1:** In 2025, a higher electoral democracy score is associated with a higher digital transparency score, and the association remains positive and statistically significant after controlling for GDP per capita.
- **H0:** Once GDP per capita is controlled for, there is no association between democracy and digital transparency.

## Models

| Model | Formula | Purpose |
|---|---|---|
| 1 | transparency ~ polyarchy | Raw relationship |
| 2 | transparency ~ polyarchy + ln_gdp_pc_ppp | **Tests H1** |
| 3 | transparency ~ libdem + ln_gdp_pc_ppp | Robustness: other democracy measure |
| 4 | transparency ~ polyarchy + ln_gdp_pc_usd | Robustness: other GDP measure |
| 5 | transparency ~ polyarchy + ln_gdp_pc_ppp + region | Robustness: compare within regions |
| 6 | transparency ~ polyarchy (all 175 countries) | Robustness: keep countries without GDP |

Plus a leave-one-theme-out check of the index. Details in [`docs/decision_log.md`](docs/decision_log.md).

## Repository structure

```
datascience2026/
├── README.md               ← this file
├── digital_transparency_analysis.ipynb   ← the full analysis, start to finish
├── data/
│   ├── raw/                ← original downloads, never edited (see data/raw/README.txt)
│   └── processed/          ← files created by the code
├── outputs/                ← regression results, residuals, figures
├── scripts/
│   └── 01_clean_gdp.py     ← WDI GDP → data/processed/gdp_2025.csv
└── docs/
    ├── decision_log.md     ← every analytical decision and why
    └── gdp_codebook.md     ← variables in gdp_2025.csv
```

## How to reproduce

Open `digital_transparency_analysis.ipynb` from the repository root and choose *Run All*.

```
pip install pandas numpy openpyxl statsmodels matplotlib jupyter
```

(`scripts/01_clean_gdp.py` is the earlier stand-alone GDP cleaning step; the notebook now includes it.)

Files in `data/processed/` can always be deleted and recreated from `data/raw/`.

## Rules for this repository

1. Never edit anything in `data/raw/`.
2. Every change to the data happens in a script, never by hand.
3. Record every analytical decision in `docs/decision_log.md`.
4. Commit after each meaningful step, with a message saying what changed.

## Data sources

| Dataset | Version | Licence | Link |
|---|---|---|---|
| World Bank GovTech Dataset | Dec 2025 release | See World Bank terms | [Data catalog](https://datacatalog.worldbank.org/search/dataset/0037889/govtech-dataset) |
| V-Dem Country-Year Core | v16 (March 2026) | See V-Dem terms | [V-Dem](https://www.v-dem.net/data/the-v-dem-dataset/country-year-v-dem-core-v16/) |
| WDI GDP per capita, PPP | `NY.GDP.PCAP.PP.KD` | See World Bank terms | [WDI](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD) |
| WDI GDP per capita, US$ | `NY.GDP.PCAP.CD` | See World Bank terms | [WDI](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD) |

Full citations are in [`data/raw/README.txt`](data/raw/README.txt).
