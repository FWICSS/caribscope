import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.loader import load_caribbean_tracks, CATEGORY_COLORS
from src.viz.maps import plot_track_map
from src.viz.charts import plot_hurricane_timeline

st.set_page_config(page_title="Comparateur", page_icon="⚡", layout="wide")

st.title("⚡ Comparateur d'ouragans")
st.caption("Comparez deux ouragans côte à côte")

df = load_caribbean_tracks()
all_names = sorted(df["NAME"].dropna().unique().tolist())

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Ouragan A")
    name_a = st.selectbox("Nom A", all_names, index=all_names.index("IRMA") if "IRMA" in all_names else 0, key="name_a")
    years_a = sorted(df[df["NAME"] == name_a]["year"].unique().tolist(), reverse=True)
    year_a = st.selectbox("Année A", years_a, key="year_a")

with col_b:
    st.subheader("Ouragan B")
    name_b = st.selectbox("Nom B", all_names, index=all_names.index("DEAN") if "DEAN" in all_names else 1, key="name_b")
    years_b = sorted(df[df["NAME"] == name_b]["year"].unique().tolist(), reverse=True)
    year_b = st.selectbox("Année B", years_b, key="year_b")

st.divider()

track_a = df[(df["NAME"] == name_a) & (df["year"] == year_a)]
track_b = df[(df["NAME"] == name_b) & (df["year"] == year_b)]


def get_summary(track):
    if track.empty:
        return {}
    valid_wind = track[track["USA_WIND"] > 0]
    valid_pres = track[track["USA_PRES"] > 0]
    duration = None
    if track["Hurricane_Date"].notna().any():
        duration = (track["Hurricane_Date"].max() - track["Hurricane_Date"].min()).days
    return {
        "max_wind": valid_wind["USA_WIND"].max() if not valid_wind.empty else None,
        "min_pres": valid_pres["USA_PRES"].min() if not valid_pres.empty else None,
        "max_cat": track.loc[valid_wind["USA_WIND"].idxmax(), "category"] if not valid_wind.empty else "N/A",
        "duration_days": duration,
        "n_points": len(track),
    }


s_a = get_summary(track_a)
s_b = get_summary(track_b)

# --- Tableau de comparaison ---
st.subheader("Comparaison")

metrics = {
    "Catégorie max": ("max_cat", None),
    "Vitesse max (kt)": ("max_wind", "kt"),
    "Pression min (mb)": ("min_pres", "mb"),
    "Durée (jours)": ("duration_days", "j"),
    "Points de mesure": ("n_points", None),
}

cols = st.columns(len(metrics))
for i, (label, (key, unit)) in enumerate(metrics.items()):
    val_a = s_a.get(key)
    val_b = s_b.get(key)

    fmt = lambda v: f"{v:.0f} {unit}" if (unit and v is not None and isinstance(v, float)) else (str(v) if v is not None else "N/A")

    with cols[i]:
        st.markdown(f"**{label}**")
        st.markdown(f"🔴 `{fmt(val_a)}`")
        st.markdown(f"🔵 `{fmt(val_b)}`")

st.divider()

# --- Cartes côte à côte ---
st.subheader("Trajectoires")
map_col_a, map_col_b = st.columns(2)

with map_col_a:
    if not track_a.empty:
        from src.viz.maps import plot_single_track
        st.plotly_chart(
            plot_single_track(df, name_a, year_a),
            use_container_width=True,
        )
    else:
        st.warning(f"Pas de données pour {name_a} {year_a}")

with map_col_b:
    if not track_b.empty:
        from src.viz.maps import plot_single_track
        st.plotly_chart(
            plot_single_track(df, name_b, year_b),
            use_container_width=True,
        )
    else:
        st.warning(f"Pas de données pour {name_b} {year_b}")

st.divider()

# --- Évolution temporelle superposée ---
st.subheader("Évolution de la vitesse du vent")

fig = go.Figure()

if not track_a.empty and track_a["USA_WIND"].notna().any():
    ta = track_a.sort_values("Hurricane_Date")
    fig.add_trace(go.Scatter(
        x=list(range(len(ta))),
        y=ta["USA_WIND"],
        name=f"{name_a} {year_a}",
        line=dict(color="#DC143C", width=2),
    ))

if not track_b.empty and track_b["USA_WIND"].notna().any():
    tb = track_b.sort_values("Hurricane_Date")
    fig.add_trace(go.Scatter(
        x=list(range(len(tb))),
        y=tb["USA_WIND"],
        name=f"{name_b} {year_b}",
        line=dict(color="#00BFFF", width=2),
    ))

fig.update_layout(
    xaxis_title="Étape de mesure",
    yaxis_title="Vitesse du vent (kt)",
    template="plotly_dark",
    height=350,
    legend=dict(orientation="h"),
)
st.plotly_chart(fig, use_container_width=True)
