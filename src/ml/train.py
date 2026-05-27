from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

MODELS_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODELS_DIR / "hurricane_intensity.pkl"

FEATURES = ["USA_PRES", "LAT", "LON", "month", "decade"]


def build_features(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    clean = df[(df["USA_PRES"] > 0) & (df["USA_PRES"] < 1050)].copy()
    X = clean[FEATURES].values
    y = clean["category_num"].values.astype(int)
    return X, y


def train_model(df: pd.DataFrame) -> RandomForestClassifier:
    X, y = build_features(df)
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X, y)
    return model


def save_model(model: RandomForestClassifier) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    from src.data.loader import load_caribbean_tracks
    df = load_caribbean_tracks()
    print(f"Training on {len(df):,} rows…")
    model = train_model(df)
    save_model(model)
    print("Done.")
