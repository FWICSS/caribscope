import streamlit as st
import plotly.express as px
from src.data.loader import load_caribbean_tracks, CARIBBEAN_ISLANDS, ISLAND_COORDS
from src.analysis.statistics import get_island_profile

MONTH_NAMES = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre",
}

CAT_LABELS = {
    0: "Dépression / Tempête",
    1: "Catégorie 1", 2: "Catégorie 2", 3: "Catégorie 3",
    4: "Catégorie 4", 5: "Catégorie 5",
}

st.set_page_config(page_title="Dashboard par île", page_icon="🏝️", layout="wide")
st.title("🏝️ Profil de risque par île")

df = load_caribbean_tracks()

islands = [i for i in CARIBBEAN_ISLANDS if i != "Toutes les îles"]
island = st.selectbox("Choisir une île", islands, index=0)

coords = ISLAND_COORDS[island]
island_lat, island_lon = coords

radius = st.slider("Rayon de recherche (degrés)", min_value=1.0, max_value=8.0, value=3.0, step=0.5)

profile = get_island_profile(df, island_lat, island_lon, radius_deg=radius)

if profile is None:
    st.warning("Aucun ouragan trouvé dans ce rayon.")
    st.stop()

st.divider()

# ── KPIs ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("🌀 Ouragans passés", profile["nb_hurricanes"])
c2.metric("💨 Pire ouragan", f"{profile['worst_name']} {profile['worst_year']}", f"{int(profile['worst_wind'])} kt")
c3.metric("📅 Décennie la + active", f"{profile['most_active_decade']}s")
c4.metric("⚠️ Mois le + risqué", MONTH_NAMES[profile["riskiest_month"]])

st.divider()

col_map, col_top = st.columns([3, 2])

with col_map:
    st.subheader("Trajectoires proches")
    nearby = profile["nearby_df"]
    from src.viz.maps import plot_track_map
    fig_map = plot_track_map(nearby, title=f"Ouragans proches de {island}")
    fig_map.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=island_lat, lon=island_lon),
            zoom=4.5,
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_top:
    st.subheader("Top 5 ouragans les plus intenses")
    top5 = profile["top5"].copy()
    top5["Catégorie"] = top5["max_cat_num"].map(CAT_LABELS)
    top5 = top5.rename(columns={
        "NAME": "Nom", "year": "Année",
        "max_wind": "Vent max (kt)",
    })[["Nom", "Année", "Vent max (kt)", "Catégorie"]]
    st.dataframe(top5, hide_index=True, use_container_width=True)

st.divider()

col_decade, col_month = st.columns(2)

with col_decade:
    st.subheader("Fréquence par décennie")
    by_decade = profile["by_decade"]
    fig_dec = px.bar(
        by_decade, x="decade", y="count",
        labels={"decade": "Décennie", "count": "Ouragans"},
        color_discrete_sequence=["#DC143C"],
        template="plotly_dark",
    )
    fig_dec.update_layout(margin=dict(t=20))
    st.plotly_chart(fig_dec, use_container_width=True)

with col_month:
    st.subheader("Répartition par mois")
    by_month = profile["by_month"].copy()
    by_month["month_name"] = by_month["month"].map(MONTH_NAMES)
    fig_month = px.bar(
        by_month.sort_values("month"), x="month_name", y="count",
        labels={"month_name": "Mois", "count": "Passages"},
        color_discrete_sequence=["#FF6347"],
        template="plotly_dark",
    )
    fig_month.update_layout(margin=dict(t=20))
    st.plotly_chart(fig_month, use_container_width=True)
