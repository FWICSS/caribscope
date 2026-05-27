import streamlit as st
from src.data.seismes_loader import load_earthquakes
from src.viz.seismes_maps import plot_earthquake_map

st.set_page_config(page_title="Carte Sismique", page_icon="🌍", layout="wide")
st.title("🌍 Carte Sismique — Caraïbes")
st.caption("Séismes de magnitude ≥ 4.0 dans la zone caribéenne · Source : USGS Earthquake Catalog")

with st.spinner("Chargement des données sismiques…"):
    df_raw = load_earthquakes()

# ── Sidebar filtres ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filtres")
    mag_min = st.slider("Magnitude minimale", 4.0, 8.0, 4.0, 0.1)
    year_min_s = int(df_raw["year"].min())
    year_max_s = int(df_raw["year"].max())
    year_range = st.slider("Période", year_min_s, year_max_s, (year_min_s, year_max_s))
    map_mode = st.radio("Mode carte", ["Points individuels", "Heatmap"])

df = df_raw[
    (df_raw["magnitude"] >= mag_min) &
    (df_raw["year"] >= year_range[0]) &
    (df_raw["year"] <= year_range[1])
].copy()

# ── Métriques ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Séismes affichés", f"{len(df):,}")
c2.metric("Magnitude max", f"{df['magnitude'].max():.1f}" if not df.empty else "N/A")
c3.metric("Profondeur moyenne", f"{df['depth_km'].mean():.1f} km" if not df.empty else "N/A")
c4.metric("Plus récent", str(df["year"].max()) if not df.empty else "N/A")

# ── Carte ────────────────────────────────────────────────────────────────────
if df.empty:
    st.warning("Aucun séisme ne correspond aux filtres.")
    st.stop()

mode = "heatmap" if map_mode == "Heatmap" else "points"
st.plotly_chart(plot_earthquake_map(df, mode=mode), use_container_width=True)

# ── Export ───────────────────────────────────────────────────────────────────
st.download_button(
    label="📥 Télécharger les données filtrées (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name=f"seismes_caraibes_{year_range[0]}_{year_range[1]}_M{mag_min}.csv",
    mime="text/csv",
)
