# Decision log

Every analytical decision, in order, with the reason for it. Add new entries at the bottom.

## 1. Research question

| Date | Decision | Reason |
|---|---|---|
| Oct 2026 | First idea: GTMI group transitions and GDP vs GTMI scores. | Initial exploration of the GovTech panel. |
| Oct 2026 | **Changed** to: do more democratic countries have more digital transparency, holding income constant? | More original question; links a technical dataset to a political one. GDP kept as a control because richer countries tend to be both more democratic and more digital. |
| Oct 2026 | One main question, with sub-questions feeding into it. Transition matrix dropped. | Keep scope manageable within 4 weeks. |

## 2. Waves

| Decision | Reason |
|---|---|
| Analyse **2025 only**. | GovTech methodology changed between waves (e.g. 37 countries apparently "lost" their open data portal 2022→2025, most likely a stricter definition; 2020 data collected from websites, 2022/2025 from government surveys). Only 39 countries changed V-Dem regime type 2020–2025, too few to study change. |
| Use **2025 GDP**, not 2024. | All three datasets refer to the same year. Accepts more missing GDP (32 vs 22 countries). |

## 3. Transparency index

| Decision | Reason |
|---|---|
| ~~5 top-level indicators, equal weights~~ → **replaced** by a 28-indicator weighted index built by the team. | With 2025 only, sub-indicators no longer need to exist in all waves. They capture quality and actual use (e.g. "RTI laws actively enforced", "portal widely used"), not just whether a tool exists. |
| 8 themes with weights: Open Data 20, RTI Law 20, E-Procurement 15, Open Government 15, Citizen Participation 10, Citizen Feedback 10, Engagement Statistics 5, Job Portal 5. | Team judgement of each theme's importance for transparency. Tested with leave-one-theme-out. |
| Rescale each indicator to 0–1 by dividing by its highest possible value; index = weighted sum, 0–100. | Indicators use different scales (0–1, 0–2, 0–3). |
| I-25.3 and I-30.2: answers 1 and 2 recoded to 1. | Both answers are forms of "yes" (e.g. petitions on the same or a separate portal). |
| Top-level indicators (I-12, I-28 …) not included. | Sub-indicators already cover them; including both would double-count. |
| Only Nicaragua has missing values (all indicators). | Dropped. |

## 4. Democracy

| Decision | Reason |
|---|---|
| Main predictor: V-Dem Electoral Democracy Index (`v2x_polyarchy`). | Academic standard; focuses on elections, so less overlap with transparency than the Liberal Democracy Index. |
| `v2x_libdem` used only in a separate robustness model. | Correlates 0.98 with `polyarchy`; never in the same model. |
| `v2x_regime` used for descriptives and plot colours only, not in the regression. | Built from the same data as `polyarchy`; including both double-counts democracy. |

## 5. Income

| Decision | Reason |
|---|---|
| Control: log GDP per capita, PPP, constant 2021 international $ (`NY.GDP.PCAP.PP.KD`). | PPP adjusts for price differences; log because income matters more at low levels and to reduce the influence of very rich countries. |
| Robustness: log GDP per capita, current US$ (`NY.GDP.PCAP.CD`). | Slightly better coverage (includes Venezuela). |
| Do not use IMF figures to fill gaps. | Different price base (current, not constant 2021, international $); doesn't mix cleanly with WDI. |

## 6. Merging and country codes

| Decision | Reason |
|---|---|
| Merge on `iso3`; inner merge GovTech × V-Dem, then left merge GDP. | Keeps all countries with outcome and predictor; GDP gaps stay visible. |
| Models 1 and 2 use the same 164 countries (all with GDP); Model 6 re-runs Model 1 on all 175. | A fair comparison of the democracy coefficient with and without income. |
| Recode GovTech `KSV` → `XKX` (Kosovo). | Match V-Dem and WDI. |
| Recode GovTech `WBG` → `PSE` (Palestine); V-Dem score = average of West Bank (`PSE`) and Gaza (`PSG`); regime type from West Bank. | V-Dem scores the two separately; GovTech and WDI treat Palestine as one economy. Footnote in write-up. |
| Strip whitespace from GovTech codes; drop the summary rows at the bottom of `GTMI_Data`. | Data cleaning. |

## 7. Missing data

| Countries | Missing | Handling |
|---|---|---|
| Nicaragua | All GovTech 2025 indicators (refused survey) | Drop |
| 22 small states (Andorra, Antigua and Barbuda, Bahamas, Belize, Brunei, Dominica, Grenada, Kiribati, Liechtenstein, Macao, Marshall Islands, Micronesia, Monaco, Nauru, Palau, Samoa, San Marino, St. Kitts and Nevis, St. Lucia, St. Vincent and the Grenadines, Tonga, Tuvalu) | Not in V-Dem | Drop; limitation |
| Afghanistan, Lebanon, UAE, Syria | 2025 GDP | Main models: dropped from GDP models. Sensitivity check: latest WDI value (2024; Syria 2022), flagged `gdp_imputed = 1` |
| Venezuela | PPP GDP | Included in Model 4 (US$) |
| Taiwan | Not in WDI | Optional: national statistics (US$) in Model 4, flagged |
| Cuba, Eritrea, North Korea, South Sudan, Yemen | No reliable GDP from any source | Drop from GDP models; limitation |

Final sample: 175 countries with transparency and democracy; 164 also with 2025 PPP GDP.

## 8. Robustness checks

1. Model 3: `libdem` instead of `polyarchy`.
2. Model 4: US$ GDP instead of PPP GDP.
3. Model 5: adds world region.
4. Model 6: Model 1 on the full sample (175, including countries without GDP).
5. Leave-one-theme-out: rebuild the index 8 times, dropping one theme each time; re-run Model 2.
6. Optional: Freedom House score instead of V-Dem (covers the 22 small states).
7. Optional: Model 2 with filled-in GDP for Afghanistan, Lebanon, UAE, Syria.

Rule: each check changes one thing only.

## 9. Raw data

| Date | Action |
|---|---|
| 03 Oct 2026 | All four datasets downloaded; see `data/raw/README.txt`. |
| 16 Oct 2026 | Raw files renamed with download date; Mac system files removed; V-Dem zip rebuilt with original contents only (no Mac files, no extra folder). Contents verified identical to downloads by checksum. |
| 16 Oct 2026 | End-to-end notebook `digital_transparency_analysis.ipynb` added: index, V-Dem, GDP, merge, regressions, robustness, residuals. Replaces the separate team notebooks. |
