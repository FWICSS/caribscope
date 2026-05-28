import streamlit as st
from src.data.seismes_loader import load_earthquakes
from src.analysis.seismes import get_top_earthquakes, get_earthquakes_by_decade, get_magnitude_distribution
from src.viz.seismes_maps import plot_earthquakes_by_decade, plot_magnitude_histogram

st.set_page_config(page_title="Stats Séismes", page_icon="📊", layout="wide")
st.title("📊 Statistiques Sismiques — Caraïbes")
st.caption("Analyse historique des séismes caribéens · Source : USGS")

with st.spinner("Chargement…"):
    df = load_earthquakes()

# ── Top 10 ───────────────────────────────────────────────────────────────────
st.subheader("🔝 Top 10 séismes les plus puissants")
top = get_top_earthquakes(df, n=10)
display_cols = ["magnitude", "place", "year", "depth_km"]
st.dataframe(
    top[display_cols].rename(columns={
        "magnitude": "Magnitude",
        "place": "Lieu",
        "year": "Année",
        "depth_km": "Profondeur (km)",
    }),
    width="stretch",
    hide_index=True,
)

st.divider()

# ── Graphiques ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    decade_df = get_earthquakes_by_decade(df)
    st.plotly_chart(plot_earthquakes_by_decade(decade_df), width="stretch")

with col2:
    dist_df = get_magnitude_distribution(df)
    st.plotly_chart(plot_magnitude_histogram(dist_df), width="stretch")

st.divider()

# ── Données brutes ────────────────────────────────────────────────────────────
with st.expander("Données brutes"):
    st.dataframe(df.sort_values("magnitude", ascending=False).reset_index(drop=True), width="stretch")

st.download_button(
    label="📥 Télécharger toutes les données (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="seismes_caraibes_complet.csv",
    mime="text/csv",
)
