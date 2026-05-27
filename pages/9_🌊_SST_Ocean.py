import streamlit as st
from src.data.loader import load_caribbean_tracks
from src.data.sst_loader import load_sst
from src.analysis.climate import get_sst_hurricane_correlation
from src.viz.climate_charts import plot_sst_trend, plot_sst_correlation

st.set_page_config(page_title="Température Océan (SST)", page_icon="🌊", layout="wide")
st.title("🌊 Température de Surface de l'Océan — Caraïbes")
st.caption("Évolution de la SST 1980–2025 et corrélation avec l'intensité des ouragans.")
st.info(
    "📌 Données SST synthétiques basées sur les tendances IPCC AR6 pour la région Caraïbes "
    "(moyenne ~28°C, +1.8°C depuis 1980). Remplaçable par les données NOAA ERSSTV5 réelles.",
    icon="ℹ️",
)

try:
    df_sst = load_sst()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

with st.spinner("Chargement des ouragans…"):
    df_hurr = load_caribbean_tracks()

# ── Métriques ────────────────────────────────────────────────────────────────
sst_1980 = df_sst[df_sst["year"] == 1980]["sst_c"].mean()
sst_2024 = df_sst[df_sst["year"] == 2024]["sst_c"].mean()
delta = round(sst_2024 - sst_1980, 2)

c1, c2, c3 = st.columns(3)
c1.metric("SST moyenne 1980", f"{sst_1980:.1f} °C")
c2.metric("SST moyenne 2024", f"{sst_2024:.1f} °C", delta=f"{delta:+.2f} °C")
c3.metric("Mois le plus chaud", "Août–Septembre")

st.divider()

# ── Graphiques ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(plot_sst_trend(df_sst), use_container_width=True)

with col2:
    corr_df = get_sst_hurricane_correlation(df_hurr, df_sst)
    st.plotly_chart(plot_sst_correlation(corr_df), use_container_width=True)

# ── Données mensuelles ────────────────────────────────────────────────────────
st.subheader("Données mensuelles")
year_sel = st.slider("Année", int(df_sst["year"].min()), int(df_sst["year"].max()), 2020)
monthly = df_sst[df_sst["year"] == year_sel].copy()
st.dataframe(
    monthly[["month", "sst_c"]].rename(columns={"month": "Mois", "sst_c": "SST (°C)"}),
    use_container_width=True,
    hide_index=True,
)
