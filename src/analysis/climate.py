import pandas as pd


def get_major_hurricane_pct_by_decade(df: pd.DataFrame) -> pd.DataFrame:
    """% of major hurricanes (cat 4-5, category_num >= 4) by decade."""
    per_storm = (
        df.groupby(["SID", "decade"])
        .agg(max_cat=("category_num", "max"))
        .reset_index()
    )
    grouped = per_storm.groupby("decade").apply(
        lambda g: pd.Series({
            "total": len(g),
            "major_count": int((g["max_cat"] >= 4).sum()),
        }),
        include_groups=False,
    ).reset_index()
    grouped["major_pct"] = (grouped["major_count"] / grouped["total"] * 100).round(1)
    return grouped.sort_values("decade")


def get_season_length_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """First and last month a hurricane appeared, per year."""
    per_storm = df.groupby(["SID", "year", "month"]).first().reset_index()
    grouped = (
        per_storm.groupby("year")
        .agg(first_month=("month", "min"), last_month=("month", "max"))
        .reset_index()
    )
    grouped["season_length"] = grouped["last_month"] - grouped["first_month"]
    return grouped.sort_values("year")


def get_sst_hurricane_correlation(df_hurricanes: pd.DataFrame, df_sst: pd.DataFrame) -> pd.DataFrame:
    """Yearly peak-season (Jul-Oct) SST vs max hurricane wind speed."""
    peak_sst = (
        df_sst[df_sst["month"].between(7, 10)]
        .groupby("year")["sst_c"]
        .mean()
        .reset_index()
        .rename(columns={"sst_c": "sst_peak"})
    )
    max_wind = (
        df_hurricanes[df_hurricanes["USA_WIND"] > 0]
        .groupby("year")["USA_WIND"]
        .max()
        .reset_index()
        .rename(columns={"USA_WIND": "max_wind"})
    )
    return peak_sst.merge(max_wind, on="year")
