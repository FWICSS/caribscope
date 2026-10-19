"""Build the derived artefacts the app reads at runtime.

Run at container start (see start.sh). Produces:
- caribbean.parquet   : enriched track points, used by the exploration pages
- home.json           : the 4 home-page counters
- named_storms.parquet: one row per named storm, used by the "hurricane of the
                        day" block

home.json and named_storms.parquet exist so the home page no longer has to load
170 years of track points just to render four numbers and pick one storm.
"""
import json
from pathlib import Path

import pandas as pd

from src.analysis.statistics import get_max_category_per_hurricane
from src.data.loader import _enrich

DATA_DIR = Path(__file__).parent.parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"


def _home_payload(df: pd.DataFrame) -> dict:
    return {
        "hurricane_count": int(df["SID"].nunique()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "max_wind": int(df["USA_WIND"].max()),
        "busiest_year": int(df.groupby("year")["SID"].nunique().idxmax()),
    }


def precompute() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_DIR / "hurricanes_Past_In_Caribbean.csv"
    df = pd.read_csv(csv_path, low_memory=False)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")], errors="ignore")
    df = _enrich(df)

    output = PROCESSED_DIR / "caribbean.parquet"
    df.to_parquet(output, index=False)
    print(f"Precompute: {len(df):,} rows → {output}")

    home_path = PROCESSED_DIR / "home.json"
    home_path.write_text(json.dumps(_home_payload(df)), encoding="utf-8")
    print(f"Precompute: home counters → {home_path}")

    per_storm = get_max_category_per_hurricane(df)
    named = per_storm[
        per_storm["NAME"].notna()
        & (per_storm["NAME"] != "UNNAMED")
        & (per_storm["max_cat_num"] >= 1)
    ]
    named_path = PROCESSED_DIR / "named_storms.parquet"
    named.to_parquet(named_path, index=False)
    print(f"Precompute: {len(named):,} named storms → {named_path}")


if __name__ == "__main__":
    precompute()
