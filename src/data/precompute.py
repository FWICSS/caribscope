from pathlib import Path
import pandas as pd
from src.data.loader import _enrich

DATA_DIR = Path(__file__).parent.parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"


def precompute() -> None:
    PROCESSED_DIR.mkdir(exist_ok=True)
    csv_path = DATA_DIR / "hurricanes_Past_In_Caribbean.csv"
    df = pd.read_csv(csv_path, low_memory=False)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")], errors="ignore")
    df = _enrich(df)
    output = PROCESSED_DIR / "caribbean.parquet"
    df.to_parquet(output, index=False)
    print(f"Precompute: {len(df):,} rows → {output}")


if __name__ == "__main__":
    precompute()
