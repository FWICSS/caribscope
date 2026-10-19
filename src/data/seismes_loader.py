import time
from pathlib import Path

import pandas as pd
import requests

try:
    import streamlit as st
    _cache = st.cache_data
except ImportError:
    def _cache(fn=None, **kw):
        return fn if fn else lambda f: f

DATA_DIR = Path(__file__).parent.parent.parent / "data"
CACHE_FILE = DATA_DIR / "earthquakes_caribbean.csv"
CACHE_MAX_AGE_S = 24 * 3600

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
USGS_PARAMS = {
    "format": "geojson",
    "starttime": "1900-01-01",
    "minmagnitude": 4.0,
    # Zone caribéenne : Golfe du Honduras → Petites Antilles
    "minlatitude": 8.0,
    "maxlatitude": 28.0,
    "minlongitude": -90.0,
    "maxlongitude": -58.0,
    "orderby": "time",
    "limit": 20000,
}

COLUMNS = ["magnitude", "latitude", "longitude", "depth_km", "place", "time", "year", "month"]


def _parse_geojson(data: dict) -> pd.DataFrame:
    rows = []
    for feature in data.get("features", []):
        props = feature.get("properties") or {}
        coords = (feature.get("geometry") or {}).get("coordinates") or [None, None, None]
        rows.append({
            "magnitude": props.get("mag"),
            "longitude": coords[0],
            "latitude": coords[1],
            "depth_km": coords[2] if len(coords) > 2 else None,
            "place": props.get("place"),
            "time": props.get("time"),
        })

    df = pd.DataFrame(rows, columns=["magnitude", "latitude", "longitude", "depth_km", "place", "time"])
    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
    df = df.dropna(subset=["magnitude", "latitude", "longitude", "time"]).reset_index(drop=True)
    df["year"] = df["time"].dt.year.astype(int)
    df["month"] = df["time"].dt.month.astype(int)
    return df[COLUMNS]


def fetch_earthquakes(use_cache: bool = True) -> pd.DataFrame:
    if use_cache and CACHE_FILE.exists() and time.time() - CACHE_FILE.stat().st_mtime < CACHE_MAX_AGE_S:
        df = pd.read_csv(CACHE_FILE)
        df["time"] = pd.to_datetime(df["time"], utc=True, format="ISO8601")
        return df

    response = requests.get(USGS_URL, params=USGS_PARAMS, timeout=30)
    response.raise_for_status()
    df = _parse_geojson(response.json())

    if use_cache:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            df.to_csv(CACHE_FILE, index=False)
        except OSError:
            pass
    return df


@_cache(ttl=CACHE_MAX_AGE_S, show_spinner=False)
def load_earthquakes() -> pd.DataFrame:
    return fetch_earthquakes()
