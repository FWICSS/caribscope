import pandas as pd


def get_top_earthquakes(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.nlargest(n, "magnitude")
        .reset_index(drop=True)
    )


def get_earthquakes_by_decade(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["decade"] = (df["year"] // 10) * 10
    return (
        df.groupby("decade")
        .size()
        .reset_index(name="count")
        .sort_values("decade")
    )


def get_magnitude_distribution(df: pd.DataFrame) -> pd.DataFrame:
    bins = [4.0, 5.0, 6.0, 7.0, 9.0]
    labels = ["4.0–5.0", "5.0–6.0", "6.0–7.0", "7.0+"]
    df = df.copy()
    df["range"] = pd.cut(df["magnitude"], bins=bins, labels=labels, right=False)
    counts = (
        df.groupby("range", observed=True)
        .size()
        .reset_index(name="count")
    )
    counts["range"] = counts["range"].astype(str)
    return counts
