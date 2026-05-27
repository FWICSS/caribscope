import streamlit as st
import pandas as pd
from src.data.loader import load_caribbean_tracks, CARIBBEAN_ISLANDS, ISLAND_COORDS
from src.analysis.statistics import get_hurricanes_near_island, get_max_category_per_hurricane
from src.viz.maps import plot_single_track
from src.viz.charts import plot_hurricane_timeline

st.set_page_config(page_title="Explorateur", page_icon="🔍", layout="wide")

st.title("🔍 Explorateur")

df = load_caribbean_tracks()

mode = st.radio("Explorer par", ["Ouragan", "Île"], horizontal=True)

st.divider()

if mode == "Ouragan":
    st.subheader("Profil d'un ouragan")

    col1, col2 = st.columns(2)
    with col1:
        all_names = sorted(df["NAME"].dropna().unique().tolist())
        name = st.selectbox("Nom de l'ouragan", all_names, index=all_names.index("IRMA") if "IRMA" in all_names else 0)

    available_years = sorted(df[df["NAME"] == name]["year"].unique().tolist(), reverse=True)
    with col2:
        year = st.selectbox("Année", available_years)

    track = df[(df["NAME"] == name) & (df["year"] == year)]

    if track.empty:
        st.warning("Aucune donnée pour cet ouragan.")
    else:
        max_wind = track["USA_WIND"].max()
        min_pres = track["USA_PRES"].min()
        duration = track["Hurricane_Date"].max() - track["Hurricane_Date"].min() if track["Hurricane_Date"].notna().any() else None
        max_cat = track.loc[track["USA_WIND"].idxmax(), "category"] if track["USA_WIND"].notna().any() else "N/A"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Catégorie max", max_cat)
        c2.metric("Vitesse max", f"{int(max_wind)} kt" if pd.notna(max_wind) else "N/A")
        c3.metric("Pression min", f"{int(min_pres)} mb" if pd.notna(min_pres) else "N/A")
        c4.metric("Durée", f"{duration.days} jours" if duration else "N/A")

        col_map, col_chart = st.columns([3, 2])
        with col_map:
            st.plotly_chart(plot_single_track(df, name, year), use_container_width=True)
        with col_chart:
            st.plotly_chart(plot_hurricane_timeline(df, name, year), use_container_width=True)

        with st.expander("Données brutes"):
            st.dataframe(
                track[["Hurricane_Date", "LAT", "LON", "USA_WIND", "USA_PRES", "category"]]
                .sort_values("Hurricane_Date")
                .reset_index(drop=True),
                use_container_width=True,
            )

else:
    st.subheader("Ouragans près d'une île")

    island = st.selectbox("Île", [i for i in CARIBBEAN_ISLANDS if i != "Toutes les îles"])
    radius = st.slider("Rayon de recherche (degrés lat/lon)", 1.0, 8.0, 3.0, 0.5)

    if island in ISLAND_COORDS:
        lat, lon = ISLAND_COORDS[island]
        nearby = get_hurricanes_near_island(df, lat, lon, radius_deg=radius)
        summary = get_max_category_per_hurricane(nearby).sort_values("year", ascending=False)

        st.metric(f"Ouragans ayant approché {island}", f"{summary.shape[0]}")

        st.dataframe(
            summary[["NAME", "year", "max_wind", "min_pres", "max_cat_num"]]
            .rename(columns={
                "NAME": "Nom",
                "year": "Année",
                "max_wind": "Vent max (kt)",
                "min_pres": "Pression min (mb)",
                "max_cat_num": "Catégorie max",
            })
            .reset_index(drop=True),
            use_container_width=True,
        )

        from src.viz.maps import plot_track_map
        st.plotly_chart(plot_track_map(nearby, title=f"Ouragans proches de {island}"), use_container_width=True)
