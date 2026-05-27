import streamlit as st
import pandas as pd
from src.data.loader import load_caribbean_tracks, CARIBBEAN_ISLANDS, ISLAND_COORDS, CATEGORY_COLORS
from src.analysis.statistics import get_hurricanes_near_island
from src.viz.maps import plot_track_map, plot_heatmap

st.set_page_config(page_title="Trajectoires", page_icon="🗺️", layout="wide")

st.title("🗺️ Trajectoires des ouragans caribéens")

df = load_caribbean_tracks()

# --- Sidebar filtres ---
with st.sidebar:
    st.header("Filtres")

    year_range = st.slider(
        "Période",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        value=(1980, int(df["year"].max())),
        step=1,
    )

    categories = st.multiselect(
        "Catégories Saffir-Simpson",
        options=list(CATEGORY_COLORS.keys()),
        default=["Catégorie 3", "Catégorie 4", "Catégorie 5"],
    )

    island = st.selectbox("Filtrer par île", options=CARIBBEAN_ISLANDS)

    view_mode = st.radio("Vue", ["Trajectoires", "Heatmap densité"])

# --- Filtrage ---
filtered = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

if categories:
    sids_with_cat = filtered[filtered["category"].isin(categories)]["SID"].unique()
    filtered = filtered[filtered["SID"].isin(sids_with_cat)]

if island != "Toutes les îles" and island in ISLAND_COORDS:
    lat, lon = ISLAND_COORDS[island]
    filtered = get_hurricanes_near_island(filtered, lat, lon, radius_deg=4.0)

# --- Métriques ---
n_storms = filtered["SID"].nunique()
col1, col2, col3 = st.columns(3)
col1.metric("Ouragans affichés", f"{n_storms:,}")
col2.metric("Période", f"{year_range[0]}–{year_range[1]}")
col3.metric("Île sélectionnée", island)

# --- Carte ---
if n_storms == 0:
    st.warning("Aucun ouragan correspond aux filtres sélectionnés.")
elif n_storms > 800:
    st.info(f"{n_storms} ouragans — affichage limité aux 800 premiers pour les performances.")
    sample_sids = filtered["SID"].unique()[:800]
    filtered = filtered[filtered["SID"].isin(sample_sids)]

if view_mode == "Trajectoires":
    fig = plot_track_map(filtered)
else:
    fig = plot_heatmap(filtered)

st.plotly_chart(fig, use_container_width=True)

# --- Légende catégories ---
with st.expander("Légende des catégories Saffir-Simpson"):
    cols = st.columns(len(CATEGORY_COLORS))
    for i, (cat, color) in enumerate(CATEGORY_COLORS.items()):
        cols[i].markdown(
            f"<div style='background:{color};padding:6px;border-radius:4px;"
            f"text-align:center;font-size:12px;color:black'>{cat}</div>",
            unsafe_allow_html=True,
        )
