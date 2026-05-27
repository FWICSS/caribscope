import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.loader import load_caribbean_tracks, CARIBBEAN_ISLANDS, ISLAND_COORDS
from src.analysis.statistics import (
    get_hurricanes_near_island,
    get_max_category_per_hurricane,
    get_hurricanes_by_year,
    get_monthly_distribution,
    get_intensity_trend,
)
from src.viz.charts import (
    plot_hurricanes_per_year,
    plot_monthly_distribution,
    plot_intensity_trend,
    plot_wind_pressure_scatter,
)

st.set_page_config(page_title="Analyse personnalisée", page_icon="🧪", layout="wide")

st.title("🧪 Analyse personnalisée")
st.caption("Appliquez des filtres et générez vos propres statistiques et graphiques.")

df_full = load_caribbean_tracks()

MONTHS_FR = {
    1: "Jan", 2: "Fév", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
    7: "Juil", 8: "Août", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc",
}

CAT_COLORS = {
    "Dépression/Tempête trop.": "#87CEEB",
    "Catégorie 1": "#FFD700",
    "Catégorie 2": "#FFA500",
    "Catégorie 3": "#FF6347",
    "Catégorie 4": "#DC143C",
    "Catégorie 5": "#8B0000",
    "Inconnu": "#808080",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filtres")

    st.subheader("Point de départ")
    preset = st.selectbox("Jeu de données", CARIBBEAN_ISLANDS)

    if preset != "Toutes les îles":
        radius = st.slider("Rayon autour de l'île (degrés)", 1.0, 8.0, 3.0, 0.5)
        lat, lon = ISLAND_COORDS[preset]
        df = get_hurricanes_near_island(df_full, lat, lon, radius_deg=radius)
    else:
        df = df_full.copy()

    st.divider()
    st.subheader("Filtres additionnels")

    year_min, year_max = int(df_full["year"].min()), int(df_full["year"].max())
    year_range = st.slider("Période", year_min, year_max, (year_min, year_max))
    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    all_cats = [
        "Dépression tropicale", "Tempête tropicale",
        "Catégorie 1", "Catégorie 2", "Catégorie 3", "Catégorie 4", "Catégorie 5",
    ]
    selected_cats = st.multiselect("Catégories", all_cats, default=all_cats)
    if selected_cats:
        df = df[df["category"].isin(selected_cats)]

    selected_months = st.multiselect(
        "Mois", options=list(range(1, 13)), default=list(range(1, 13)),
        format_func=lambda m: MONTHS_FR[m],
    )
    if selected_months:
        df = df[df["month"].isin(selected_months)]

    st.divider()
    st.subheader("Graphiques à afficher")
    show_per_year  = st.checkbox("Ouragans par année", value=True)
    show_monthly   = st.checkbox("Distribution mensuelle", value=True)
    show_intensity = st.checkbox("Intensité par décennie", value=True)
    show_scatter   = st.checkbox("Pression / Vent (scatter)", value=True)
    show_cat_pie   = st.checkbox("Répartition par catégorie", value=True)

# ── Main ──────────────────────────────────────────────────────────────────────
if df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

valid_wind = df[df["USA_WIND"] > 0]
valid_pres = df[df["USA_PRES"] > 0]
per_year   = get_hurricanes_by_year(df)

st.subheader(f"Résultats · {preset} · {year_range[0]}–{year_range[1]}")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Ouragans uniques",  df["SID"].nunique())
k2.metric("Points de mesure",  len(df))
k3.metric("Vent max (kt)",     f"{int(valid_wind['USA_WIND'].max())}"  if not valid_wind.empty else "N/A")
k4.metric("Pression min (mb)", f"{int(valid_pres['USA_PRES'].min())}"  if not valid_pres.empty else "N/A")
k5.metric("Moy. / an",        round(per_year["count"].mean(), 1)       if not per_year.empty else "N/A")

st.divider()

# Ligne 1
col1, col2 = st.columns(2)

if show_per_year and not per_year.empty:
    with col1:
        st.plotly_chart(plot_hurricanes_per_year(per_year), use_container_width=True)

if show_monthly:
    monthly = get_monthly_distribution(df)
    if not monthly.empty:
        with col2:
            st.plotly_chart(plot_monthly_distribution(monthly), use_container_width=True)

# Ligne 2
col3, col4 = st.columns(2)

if show_intensity:
    intensity = get_intensity_trend(df)
    if not intensity.empty:
        with col3:
            st.plotly_chart(plot_intensity_trend(intensity), use_container_width=True)

if show_scatter and not valid_wind.empty:
    with col4:
        st.plotly_chart(plot_wind_pressure_scatter(df), use_container_width=True)

# Camembert catégories
if show_cat_pie:
    cat_num_to_label = {
        0: "Dépression/Tempête trop.",
        1: "Catégorie 1", 2: "Catégorie 2",
        3: "Catégorie 3", 4: "Catégorie 4", 5: "Catégorie 5",
    }
    per_hurricane = get_max_category_per_hurricane(df)
    per_hurricane["cat_label"] = per_hurricane["max_cat_num"].map(cat_num_to_label).fillna("Inconnu")
    cat_dist = (
        per_hurricane.groupby("cat_label")["SID"]
        .count().reset_index().rename(columns={"SID": "count"})
    )
    fig_pie = px.pie(
        cat_dist,
        names="cat_label",
        values="count",
        title="Répartition par catégorie maximale atteinte",
        template="plotly_dark",
        color="cat_label",
        color_discrete_map=CAT_COLORS,
    )
    fig_pie.update_layout(height=420)
    st.plotly_chart(fig_pie, use_container_width=True)

# Données brutes
with st.expander("Données brutes"):
    cols = [c for c in ["NAME", "year", "month", "Hurricane_Date", "LAT", "LON", "USA_WIND", "USA_PRES", "category"] if c in df.columns]
    st.dataframe(
        df[cols].sort_values(["year", "Hurricane_Date"]).reset_index(drop=True),
        use_container_width=True,
    )
    st.download_button(
        label="📥 Télécharger les données filtrées (CSV)",
        data=df[cols].sort_values(["year", "Hurricane_Date"]).to_csv(index=False).encode("utf-8"),
        file_name=f"analyse_ouragans_{preset.replace(' ', '_')}_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv",
    )
