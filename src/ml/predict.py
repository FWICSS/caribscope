from pathlib import Path
import numpy as np
import pandas as pd
import joblib

try:
    import streamlit as st
    _cache = st.cache_resource
except ImportError:
    def _cache(fn):
        return fn

MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "hurricane_intensity.pkl"

CATEGORY_LABELS = {
    0: "Dépression / Tempête tropicale",
    1: "Catégorie 1",
    2: "Catégorie 2",
    3: "Catégorie 3",
    4: "Catégorie 4",
    5: "Catégorie 5",
}


@_cache
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run: python src/ml/train.py"
        )
    return joblib.load(MODEL_PATH)


def predict_category(
    model,
    pressure: float,
    lat: float,
    lon: float,
    month: int,
    decade: int = 2020,
) -> dict:
    X = np.array([[pressure, lat, lon, month, decade]])
    cat_num = int(model["model"].predict(X)[0])
    proba_arr = model["model"].predict_proba(X)[0]
    classes = model["model"].classes_
    probabilities = {int(c): float(p) for c, p in zip(classes, proba_arr)}
    return {
        "category_num": cat_num,
        "category_label": CATEGORY_LABELS.get(cat_num, "Inconnu"),
        "probabilities": probabilities,
    }


def get_feature_importance(model) -> pd.DataFrame:
    features = model["features"]
    importances = model["model"].feature_importances_
    return (
        pd.DataFrame({"feature": features, "importance": importances})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
