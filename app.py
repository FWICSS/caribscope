import random
from datetime import date

import streamlit as st

from src.analysis.statistics import get_max_category_per_hurricane
from src.components.analytics import inject_analytics
from src.components.email_capture import email_capture_form
from src.components.head import inject_head
from src.data.loader import load_caribbean_tracks, load_home_stats, load_named_storms

st.set_page_config(
    page_title="CaribScope — Observatoire des risques naturels caribéens",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_analytics("Accueil")
inject_head(
    title="CaribScope — Observatoire des risques naturels caribéens",
    description=(
        "170 ans de données sur les ouragans, séismes et tendances climatiques "
        "de la Caraïbe. Trajectoires depuis 1851, catalogue sismique USGS, "
        "prédiction d'intensité par apprentissage automatique. Open source."
    ),
)

st.title("🌀 CaribScope")
st.caption("170 ans de données · Ouragans · Séismes · Climat · IA")

# ── KPIs ─────────────────────────────────────────────────────────────────────
# Les compteurs viennent de data/processed/home.json quand il existe : charger
# les 170 ans de points de trajectoire pour afficher quatre nombres coûtait
# plusieurs secondes au premier rendu.
stats = load_home_stats()
if stats is None:
    with st.spinner("Chargement des données…"):
        df = load_caribbean_tracks()
    stats = {
        "hurricane_count": int(df["SID"].nunique()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "max_wind": int(df["USA_WIND"].max()),
        "busiest_year": int(df.groupby("year")["SID"].nunique().idxmax()),
    }

c1, c2, c3, c4 = st.columns(4)
c1.metric("🌀 Ouragans caribéens", f"{stats['hurricane_count']:,}")
c2.metric("📅 Années de données", f"{stats['year_min']}–{stats['year_max']}")
c3.metric("💨 Vent max enregistré", f"{stats['max_wind']} kt")
c4.metric("📆 Année la plus active", str(stats["busiest_year"]))

st.divider()

# ── 4 module tiles ────────────────────────────────────────────────────────────
# Les titres des tuiles sont des <div> et non des <h3> : ils sont décoratifs, et
# des <h3> sous le <h1> sans <h2> intermédiaire cassaient la hiérarchie lue par
# les lecteurs d'écran.
st.header("Explorer la plateforme")

TILES = [
    ("#1a0a0a", "#DC143C", "🌀", "Ouragans",
     "Trajectoires · Stats · Explorateur · Comparateur · Analyse"),
    ("#1a0f0a", "#FF6347", "🌍", "Séismes",
     "Carte sismique · Statistiques historiques"),
    ("#0a0f1a", "#4FC3F7", "🌡️", "Climat",
     "Tendances climatiques · Température océan"),
    ("#0a1a0a", "#81C784", "🤖", "Prédiction IA",
     "Intensité ouragan par Machine Learning"),
]

for col, (bg, accent, icon, label, blurb) in zip(st.columns(4), TILES):
    with col:
        st.markdown(
            f"""
            <div style="background:{bg};border:1px solid {accent}55;border-radius:12px;
                        padding:20px;text-align:center;height:160px;">
                <div style="font-size:36px;" aria-hidden="true">{icon}</div>
                <div style="color:{accent};margin:8px 0 4px 0;font-size:1.17rem;
                            font-weight:600;">{label}</div>
                <p style="color:#9ca3af;font-size:13px;margin:0;">{blurb}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Ouragan du jour ───────────────────────────────────────────────────────────
st.header("🌀 Ouragan du jour")

CAT_LABELS = {
    0: "Dépression / Tempête tropicale",
    1: "Catégorie 1", 2: "Catégorie 2", 3: "Catégorie 3",
    4: "Catégorie 4", 5: "Catégorie 5",
}
CAT_COLORS = {
    0: "#4FC3F7", 1: "#FFD700", 2: "#FFA500",
    3: "#FF4500", 4: "#DC143C", 5: "#8B0000",
}

named = load_named_storms()
if named is None:
    per_storm = get_max_category_per_hurricane(load_caribbean_tracks())
    named = per_storm[
        per_storm["NAME"].notna()
        & (per_storm["NAME"] != "UNNAMED")
        & (per_storm["max_cat_num"] >= 1)
    ]

random.seed(date.today().toordinal())
odj = named.sample(1, random_state=date.today().toordinal()).iloc[0]

cat_num = int(odj["max_cat_num"])
cat_label = CAT_LABELS.get(cat_num, "Inconnu")
cat_color = CAT_COLORS.get(cat_num, "#808080")

odj_col1, odj_col2 = st.columns([1, 3])
with odj_col1:
    st.markdown(
        f"""
        <div style="background:#111;border:2px solid {cat_color}55;border-radius:12px;
                    padding:24px;text-align:center;">
            <div style="font-size:48px;" aria-hidden="true">🌀</div>
            <div style="color:{cat_color};margin:8px 0 4px 0;font-size:1.5rem;
                        font-weight:700;">{odj['NAME']}</div>
            <p style="color:#b9c0c8;font-size:16px;margin:0;">{int(odj['year'])}</p>
            <p style="color:{cat_color};font-size:13px;margin:8px 0 0 0;
                      font-weight:bold;">{cat_label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with odj_col2:
    kc1, kc2, kc3 = st.columns(3)
    kc1.metric("💨 Vent maximum", f"{int(odj['max_wind'])} kt")
    pres = odj.get("min_pres")
    kc2.metric("🌡️ Pression min", f"{int(pres)} mb" if pres and pres > 0 else "N/A")
    kc3.metric("📊 Catégorie max", cat_label)
    st.caption(
        f"**{odj['NAME']} ({int(odj['year'])})** est l'ouragan du jour, tiré aléatoirement parmi "
        f"{len(named):,} ouragans nommés historiques. Reviens demain pour en découvrir un autre."
    )
    st.page_link(
        "pages/14_🌀_Ouragan_du_Jour.py",
        label="Voir l'analyse complète →",
        icon="🌀",
    )

st.divider()

# ── Capture email ─────────────────────────────────────────────────────────────
email_capture_form(source="home")

st.divider()
foot_left, foot_right = st.columns([3, 1])
with foot_left:
    st.caption(
        "Source : NOAA HURDAT2 · USGS Earthquake Catalog · CaribScope, projet open source. "
        "Les données publiées sont informatives et ne constituent pas une alerte officielle."
    )
with foot_right:
    st.page_link(
        "pages/17_⚖️_Mentions_Legales.py",
        label="Mentions légales · Confidentialité",
        icon="⚖️",
    )
