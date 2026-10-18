"""
Clean World Bank WDI GDP per capita data for the 2025 analysis.

Uses 2025 GDP figures, matching the 2025 GovTech wave. Countries without a
2025 figure are kept with blank GDP values.

Input : data/raw/GDP_PPP_03102026.zip, data/raw/GDP_USD_03102026.zip (unchanged downloads)
Run   : from the repository root:  python scripts/01_clean_gdp.py
Output: data/processed/gdp_2025.csv  (one row per country)
"""
import zipfile
import numpy as np
import pandas as pd

# ---- Settings -------------------------------------------------------------
PPP_ZIP = "data/raw/GDP_PPP_03102026.zip"   # GDP pc, PPP (constant 2021 intl $)
USD_ZIP = "data/raw/GDP_USD_03102026.zip"      # GDP pc, current US$
GDP_YEAR = "2025"        # GDP year used
ANALYSIS_YEAR = 2025     # GovTech wave it is paired with (merge key)
OUTPUT = "data/processed/gdp_2025.csv"


def read_from_zip(zip_path, prefix):
    """Read the CSV inside a WDI zip whose filename starts with `prefix`."""
    with zipfile.ZipFile(zip_path) as z:
        name = next(n for n in z.namelist() if n.startswith(prefix))
        # The data file has 4 lines of notes above the header; metadata files don't.
        skip = 4 if prefix == "API_" else 0
        return pd.read_csv(z.open(name), skiprows=skip)


def gdp_column(zip_path, value_name):
    """Take one year's GDP column from a WDI data file."""
    data = read_from_zip(zip_path, "API_")
    return data[["Country Code", GDP_YEAR]].rename(
        columns={"Country Code": "iso3", GDP_YEAR: value_name})


# ---- 1. Country list: real countries only, no aggregates ------------------
meta = read_from_zip(PPP_ZIP, "Metadata_Country")
# Aggregates like "World" or "Low income" have no Region in the metadata.
countries = meta[meta["Region"].notna()][["Country Code", "TableName", "Region", "IncomeGroup"]]
countries.columns = ["iso3", "country", "region", "income_group"]

# ---- 2. Add GDP and the log variable --------------------------------------
gdp = (countries
       .merge(gdp_column(PPP_ZIP, "gdp_pc_ppp"), on="iso3", how="left")
       .merge(gdp_column(USD_ZIP, "gdp_pc_usd"), on="iso3", how="left"))
gdp["ln_gdp_pc_ppp"] = np.log(gdp["gdp_pc_ppp"])
gdp["year"] = ANALYSIS_YEAR

gdp = gdp[["iso3", "country", "year", "gdp_pc_ppp", "ln_gdp_pc_ppp",
           "gdp_pc_usd", "region", "income_group"]]
gdp = gdp.sort_values("iso3").reset_index(drop=True)

# ---- 3. Quick checks ------------------------------------------------------
assert gdp["iso3"].is_unique, "duplicate countries"
print(f"Countries: {len(gdp)}")
print(f"Missing GDP (PPP): {gdp['gdp_pc_ppp'].isna().sum()}")
print(f"Missing GDP (US$): {gdp['gdp_pc_usd'].isna().sum()}")

gdp.to_csv(OUTPUT, index=False)
print(f"Saved {OUTPUT}")
