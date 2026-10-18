# Codebook: `gdp_2025.csv`

GDP per capita data from the World Bank's World Development Indicators (WDI), cleaned for the 2025 analysis and ready to merge with the GovTech and V-Dem 2025 data.

## Structure

| | |
|---|---|
| **Unit of observation** | One country |
| **Countries** | 217 (all WDI economies; regional and income aggregates removed) |
| **Rows** | 217 |
| **Unique key** | `iso3` (`year` is included so you can also merge on `iso3` + `year`) |
| **Produced by** | `scripts/01_clean_gdp.py` |

## Variables

| Variable | Type | Description | Source / WDI code |
|---|---|---|---|
| `iso3` | text | Three-letter ISO country code. **Merge key.** | WDI `Country Code` |
| `country` | text | Country name | WDI metadata `TableName` |
| `year` | integer | Always 2025: the year the GDP figures refer to, matching the GovTech 2025 wave. | Set in script |
| `gdp_pc_ppp` | number | GDP per capita, PPP, constant 2021 international $. Adjusted for price differences between countries and for inflation. **Main control variable.** | `NY.GDP.PCAP.PP.KD` |
| `ln_gdp_pc_ppp` | number | Natural log of `gdp_pc_ppp`. **Use this in the regression.** | Calculated |
| `gdp_pc_usd` | number | GDP per capita, current US$, at market exchange rates. **Robustness check.** | `NY.GDP.PCAP.CD` |
| `region` | text | World Bank region (7 categories) | WDI country metadata |
| `income_group` | text | World Bank income group: Low, Lower middle, Upper middle, High | WDI country metadata |

## Missing values

Blank cells mean the World Bank has no 2025 figure yet. Rows are kept so the gaps stay visible.

- **`gdp_pc_ppp` missing for 32 countries.** About half are small territories that aren't in GovTech or V-Dem anyway (e.g. Aruba, Guam, Greenland, Isle of Man). The ones that matter for the analysis are **Afghanistan, Cuba, Eritrea, Lebanon, North Korea, South Sudan, Syria, United Arab Emirates, Venezuela and Yemen**. Bahamas, Liechtenstein, Monaco and San Marino are also missing but aren't covered by V-Dem.
- **`gdp_pc_usd` missing for 31 countries**, the same list minus Venezuela.

After merging with GovTech and V-Dem, expect about **163 countries** in the model that includes GDP, against 174 without it. Most of the countries lost are autocracies or conflict-affected states, which is why the model is also run without the GDP control.

## Notes for merging

- **Codes to fix on the GovTech side** (WDI codes are standard and left unchanged): Kosovo `KSV` → `XKX`.
- **Not in WDI:** Taiwan has no WDI data and drops out when merging.
- **Income group** is the World Bank's current classification.
- Use a **left merge** from the GovTech table so no GovTech country is lost silently. Then check which countries have no GDP.

```python
merged = gtmi_2025.merge(gdp, on="iso3", how="left")
print(merged.loc[merged["gdp_pc_ppp"].isna(), "iso3"].tolist())
```

## Sources

- GDP per capita, PPP: https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD
- GDP per capita, current US$: https://data.worldbank.org/indicator/NY.GDP.PCAP.CD
