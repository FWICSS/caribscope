import streamlit as st
from src.data.loader import load_caribbean_tracks
from src.viz.maps import plot_heatmap

st.set_page_config(page_title="Heatmap Zones à Risque", page_icon="🔥", layout="wide")
st.title("🔥 Zones à risque — Densité de passage")
st.caption("Concentration géographique des trajectoires d'ouragans caribéens depuis 1851")

df = load_caribbean_tracks()

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    cat_min = st.selectbox(
        "Catégorie minimum",
        options=[0, 1, 2, 3, 4, 5],
        format_func=lambda x: {
            0: "Toutes (dépression+)",
            1: "Cat. 1+", 2: "Cat. 2+", 3: "Cat. 3+ (majeurs)",
            4: "Cat. 4+", 5: "Cat. 5 uniquement",
        }[x],
        index=0,
    )
with col2:
    year_min = st.slider("Depuis l'année", min_value=int(df["year"].min()), max_value=2010, value=1851, step=10)
with col3:
    radius = st.slider("Rayon de chaleur", min_value=5, max_value=30, value=12, step=5,
                       help="Rayon en pixels du noyau de densité")

filtered = df[
    (df["category_num"] >= cat_min) &
    (df["year"] >= year_min)
]

st.metric("Points de trajectoire affichés", f"{len(filtered):,}", f"{df['SID'].nunique()} ouragans source")

if filtered.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

fig = plot_heatmap(filtered)
fig.update_traces(radius=radius)
fig.update_layout(
    title=f"Densité de passage — Cat. {cat_min}+ · {year_min}–2022"
)
st.plotly_chart(fig, width="stretch")

st.caption(
    "**Lecture :** Les zones rouge foncé indiquent les couloirs de passage les plus fréquents. "
    "La côte Est des Petites Antilles et le golfe du Mexique concentrent historiquement le plus de passages de catégorie 3+."
)
