import streamlit as st
from src.data.loader import load_caribbean_tracks
from src.analysis.statistics import (
    get_hurricanes_by_year,
    get_records,
    get_intensity_trend,
    get_monthly_distribution,
)
from src.viz.charts import (
    plot_hurricanes_per_year,
    plot_intensity_trend,
    plot_monthly_distribution,
    plot_wind_pressure_scatter,
    plot_basin_distribution,
)

st.set_page_config(page_title="Statistiques", page_icon="📊", layout="wide")

st.title("📊 Statistiques — 170 ans d'ouragans caribéens")

df = load_caribbean_tracks()

# --- Records ---
records = get_records(df)

st.subheader("Records historiques")
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Ouragan le + puissant",
    f"{records['strongest_wind']['name']} ({records['strongest_wind']['year']})",
    f"{records['strongest_wind']['wind_kt']:.0f} kt",
)
c2.metric(
    "Pression la + basse",
    f"{records['lowest_pressure']['name']} ({records['lowest_pressure']['year']})",
    f"{records['lowest_pressure']['pres_mb']:.0f} mb",
)
c3.metric(
    "Année la + active",
    str(records["most_active_year"]["year"]),
    f"{records['most_active_year']['count']} ouragans",
)
c4.metric(
    "Total ouragans analysés",
    f"{records['total_named']:,}",
    f"{records['year_range'][0]}–{records['year_range'][1]}",
)

st.divider()

# --- Fréquence annuelle ---
st.subheader("Fréquence annuelle")
by_year = get_hurricanes_by_year(df)
st.plotly_chart(plot_hurricanes_per_year(by_year), use_container_width=True)

st.divider()

# --- Intensité par décennie + saisonnalité ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Intensité par décennie")
    trend = get_intensity_trend(df)
    st.plotly_chart(plot_intensity_trend(trend), use_container_width=True)

with col2:
    st.subheader("Saisonnalité")
    monthly = get_monthly_distribution(df)
    st.plotly_chart(plot_monthly_distribution(monthly), use_container_width=True)

st.divider()

# --- Pression vs Vitesse + Répartition bassins ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Pression vs Vitesse du vent")
    st.plotly_chart(plot_wind_pressure_scatter(df), use_container_width=True)

with col4:
    st.subheader("Répartition par bassin")
    st.plotly_chart(plot_basin_distribution(df), use_container_width=True)
