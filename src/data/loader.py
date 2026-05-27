import pandas as pd
from pathlib import Path

try:
    import streamlit as st
    _cache = st.cache_data
except ImportError:
    def _cache(fn):
        return fn
    st = None  # type: ignore[assignment]

DATA_DIR = Path(__file__).parent.parent.parent / "data"


@_cache
def load_caribbean_tracks() -> pd.DataFrame:
    """Charge les ouragans caribéens avec enrichissement."""
    parquet = DATA_DIR / "processed" / "caribbean.parquet"
    if parquet.exists():
        return pd.read_parquet(parquet)
    df = pd.read_csv(DATA_DIR / "hurricanes_Past_In_Caribbean.csv", low_memory=False)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")], errors="ignore")
    return _enrich(df)


@_cache
def load_all_tracks() -> pd.DataFrame:
    """Charge l'historique HURDAT2 complet (64MB). Utiliser avec précaution sur Streamlit Cloud."""
    df = pd.read_csv(DATA_DIR / "Historical_Hurricane_Tracks.csv", low_memory=False)
    return _enrich(df)


def _enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["category"] = df["USA_WIND"].apply(get_saffir_simpson_category)
    df["category_num"] = df["USA_WIND"].apply(get_saffir_simpson_number)
    df["decade"] = (df["year"] // 10) * 10
    if "Hurricane_Date" in df.columns:
        df["Hurricane_Date"] = pd.to_datetime(df["Hurricane_Date"], errors="coerce")
    else:
        df["Hurricane_Date"] = pd.to_datetime(
            df["year"].astype(str) + "-" +
            df["month"].astype(str).str.zfill(2) + "-" +
            df["day"].astype(str).str.zfill(2),
            errors="coerce",
        )
    return df


def get_saffir_simpson_category(wind_kt) -> str:
    if pd.isna(wind_kt) or wind_kt < 0:
        return "Inconnu"
    if wind_kt < 34:
        return "Dépression tropicale"
    if wind_kt < 64:
        return "Tempête tropicale"
    if wind_kt < 83:
        return "Catégorie 1"
    if wind_kt < 96:
        return "Catégorie 2"
    if wind_kt < 113:
        return "Catégorie 3"
    if wind_kt < 137:
        return "Catégorie 4"
    return "Catégorie 5"


def get_saffir_simpson_number(wind_kt) -> int:
    if pd.isna(wind_kt) or wind_kt < 34:
        return 0
    if wind_kt < 64:
        return 0
    if wind_kt < 83:
        return 1
    if wind_kt < 96:
        return 2
    if wind_kt < 113:
        return 3
    if wind_kt < 137:
        return 4
    return 5


CATEGORY_COLORS = {
    "Dépression tropicale": "#87CEEB",
    "Tempête tropicale":    "#00BFFF",
    "Catégorie 1":          "#FFD700",
    "Catégorie 2":          "#FFA500",
    "Catégorie 3":          "#FF6347",
    "Catégorie 4":          "#DC143C",
    "Catégorie 5":          "#8B0000",
    "Inconnu":              "#808080",
}

CARIBBEAN_ISLANDS = [
    "Toutes les îles",
    "Martinique",
    "Guadeloupe",
    "Saint-Martin",
    "Saint-Barthélemy",
    "Haiti",
    "Cuba",
    "Puerto Rico",
    "Dominique",
    "Sainte-Lucie",
    "Saint-Vincent",
    "Barbade",
    "Trinidad et Tobago",
    "Jamaïque",
    "République Dominicaine",
]

# Coordonnées centrales de chaque île (lat°N, lon°W en négatif)
# Boîte caribéenne : LAT 5–25°N, LON -100–-55°W  (toutes les îles françaises sont à 14–18°N, 61–63°W)
ISLAND_COORDS = {
    "Martinique":             (14.6415, -61.0242),  # Fort-de-France
    "Guadeloupe":             (16.2650, -61.5510),  # Pointe-à-Pitre
    "Saint-Martin":           (18.0731, -63.0822),  # Marigot (partie française)
    "Saint-Barthélemy":       (17.8999, -62.8339),  # Gustavia
    "Haiti":                  (18.9712, -72.2852),
    "Cuba":                   (21.5218, -77.7812),
    "Puerto Rico":            (18.2208, -66.5901),
    "Dominique":              (15.4150, -61.3710),
    "Sainte-Lucie":           (13.9094, -60.9789),
    "Saint-Vincent":          (13.2528, -61.1971),
    "Barbade":                (13.1939, -59.5432),
    "Trinidad et Tobago":     (10.6918, -61.2225),
    "Jamaïque":               (18.1096, -77.2975),
    "République Dominicaine": (18.7357, -70.1627),
}
