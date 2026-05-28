import streamlit as st
from src.data.loader import load_caribbean_tracks
from src.analysis.statistics import get_intensity_trend, get_hurricanes_by_year
from src.analysis.climate import get_major_hurricane_pct_by_decade, get_season_length_by_year
from src.viz.charts import plot_hurricanes_per_year, plot_intensity_trend
from src.viz.climate_charts import plot_major_hurricane_pct, plot_season_length

st.set_page_config(page_title="Tendances Climatiques", page_icon="📈", layout="wide")
st.title("📈 Tendances Climatiques — Caraïbes")
st.caption("Les ouragans s'intensifient-ils ? 170 ans de données NOAA HURDAT2.")

with st.spinner("Chargement…"):
    df = load_caribbean_tracks()

per_year = get_hurricanes_by_year(df)
intensity = get_intensity_trend(df)
major_pct = get_major_hurricane_pct_by_decade(df)
season = get_season_length_by_year(df)

# ── KPIs ─────────────────────────────────────────────────────────────────────
recent_decade = major_pct[major_pct["decade"] >= 2010]["major_pct"].mean()
old_decade = major_pct[major_pct["decade"] <= 1980]["major_pct"].mean()
delta_pct = round(recent_decade - old_decade, 1) if not major_pct.empty else 0

c1, c2, c3 = st.columns(3)
c1.metric("% Cat 4-5 depuis 2010", f"{recent_decade:.1f}%", delta=f"{delta_pct:+.1f}% vs avant 1980")
c2.metric("Ouragan le + intense (vent)", f"{int(df['USA_WIND'].max())} kt")
c3.metric("Années de données", f"{int(df['year'].min())}–{int(df['year'].max())}")

st.divider()

# ── Graphiques ligne 1 ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_hurricanes_per_year(per_year), width="stretch")
with col2:
    st.plotly_chart(plot_intensity_trend(intensity), width="stretch")

# ── Graphiques ligne 2 ────────────────────────────────────────────────────────
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(plot_major_hurricane_pct(major_pct), width="stretch")
with col4:
    st.plotly_chart(plot_season_length(season), width="stretch")
