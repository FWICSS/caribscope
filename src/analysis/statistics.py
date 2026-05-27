import pandas as pd
from collections import Counter


def get_hurricanes_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Nombre d'ouragans uniques (par SID) par année."""
    return (
        df.groupby("year")["SID"]
        .nunique()
        .reset_index()
        .rename(columns={"SID": "count"})
        .sort_values("year")
    )


def get_max_category_per_hurricane(df: pd.DataFrame) -> pd.DataFrame:
    """Catégorie maximale atteinte par chaque ouragan (SID)."""
    return (
        df.groupby(["SID", "NAME", "year"])
        .agg(
            max_wind=("USA_WIND", "max"),
            min_pres=("USA_PRES", "min"),
            max_cat_num=("category_num", "max"),
        )
        .reset_index()
    )


def get_records(df: pd.DataFrame) -> dict:
    """Retourne les records historiques."""
    valid_wind = df[df["USA_WIND"] > 0]
    valid_pres = df[df["USA_PRES"] > 0]

    strongest_idx = valid_wind["USA_WIND"].idxmax()
    lowest_pres_idx = valid_pres["USA_PRES"].idxmin()

    strongest = valid_wind.loc[strongest_idx]
    lowest = valid_pres.loc[lowest_pres_idx]

    years_count = get_hurricanes_by_year(df)
    most_active_year = years_count.loc[years_count["count"].idxmax()]

    return {
        "strongest_wind": {
            "name": strongest["NAME"],
            "year": int(strongest["year"]),
            "wind_kt": float(strongest["USA_WIND"]),
        },
        "lowest_pressure": {
            "name": lowest["NAME"],
            "year": int(lowest["year"]),
            "pres_mb": float(lowest["USA_PRES"]),
        },
        "most_active_year": {
            "year": int(most_active_year["year"]),
            "count": int(most_active_year["count"]),
        },
        "total_named": int(df["SID"].nunique()),
        "year_range": (int(df["year"].min()), int(df["year"].max())),
    }


def get_hurricanes_near_island(df: pd.DataFrame, island_lat: float, island_lon: float, radius_deg: float = 3.0) -> pd.DataFrame:
    """Retourne les ouragans dont une position est dans un rayon (degrés) d'une île."""
    nearby_mask = (
        (df["LAT"].between(island_lat - radius_deg, island_lat + radius_deg)) &
        (df["LON"].between(island_lon - radius_deg, island_lon + radius_deg))
    )
    nearby_sids = df.loc[nearby_mask, "SID"].unique()
    return df[df["SID"].isin(nearby_sids)].copy()


def get_intensity_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Évolution de la vitesse max et pression min moyenne par décennie."""
    per_hurricane = get_max_category_per_hurricane(df)
    per_hurricane["decade"] = (per_hurricane["year"] // 10) * 10
    return (
        per_hurricane.groupby("decade")
        .agg(
            mean_max_wind=("max_wind", "mean"),
            mean_min_pres=("min_pres", "mean"),
            count=("SID", "count"),
        )
        .reset_index()
    )


def get_island_profile(df: pd.DataFrame, island_lat: float, island_lon: float, radius_deg: float = 3.0) -> dict:
    """Profil risque complet pour une île : KPIs, top 5, distribution décennie/mois."""
    nearby = get_hurricanes_near_island(df, island_lat, island_lon, radius_deg)
    if nearby.empty:
        return None

    per_storm = get_max_category_per_hurricane(nearby)
    per_storm["decade"] = (per_storm["year"] // 10) * 10

    top5 = per_storm.nlargest(5, "max_wind")[["NAME", "year", "max_wind", "max_cat_num"]].copy()

    by_decade = (
        per_storm.groupby("decade")["SID"]
        .count()
        .reset_index()
        .rename(columns={"SID": "count"})
    )
    most_active_decade = int(by_decade.loc[by_decade["count"].idxmax(), "decade"])

    # Mois à risque : sur les positions proches de l'île
    nearby_positions = nearby[
        (nearby["LAT"].between(island_lat - radius_deg, island_lat + radius_deg)) &
        (nearby["LON"].between(island_lon - radius_deg, island_lon + radius_deg))
    ]
    month_counts = nearby_positions.groupby("month")["SID"].nunique()
    riskiest_month = int(month_counts.idxmax()) if not month_counts.empty else 9

    by_month = month_counts.reset_index().rename(columns={"SID": "count"})

    worst = per_storm.loc[per_storm["max_wind"].idxmax()]

    return {
        "nb_hurricanes": int(per_storm["SID"].nunique()),
        "max_cat_num": int(per_storm["max_cat_num"].max()),
        "worst_name": str(worst["NAME"]),
        "worst_year": int(worst["year"]),
        "worst_wind": float(worst["max_wind"]),
        "most_active_decade": most_active_decade,
        "riskiest_month": riskiest_month,
        "top5": top5,
        "by_decade": by_decade,
        "by_month": by_month,
        "nearby_df": nearby,
    }


def get_monthly_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Nombre d'ouragans par mois (sur l'ensemble de l'historique)."""
    per_hurricane = df.groupby(["SID", "month"]).first().reset_index()
    return (
        per_hurricane.groupby("month")["SID"]
        .count()
        .reset_index()
        .rename(columns={"SID": "count"})
    )
