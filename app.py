import random
from datetime import date
import streamlit as st
from src.data.loader import load_caribbean_tracks
from src.analysis.statistics import get_max_category_per_hurricane

st.set_page_config(
    page_title="CaribScope",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<meta name="description" content="CaribScope — Observatoire open source des risques naturels dans la Caraïbe. 170 ans de données ouragans, séismes et climat.">
<meta property="og:title" content="CaribScope — Observatoire Caribéen">
<meta property="og:description" content="170 ans de données ouragans, séismes et climat dans la Caraïbe. Open source, gratuit, propulsé par NOAA & USGS.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://caribscope.fwicss.fr">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CaribScope — Observatoire Caribéen">
<meta name="twitter:description" content="170 ans de données ouragans, séismes et climat dans la Caraïbe. Open source.">
""", unsafe_allow_html=True)

st.title("🌀 CaribScope")
st.caption("170 ans de données · Ouragans · Séismes · Climat · IA")

# ── KPIs ─────────────────────────────────────────────────────────────────────
with st.spinner("Chargement des données…"):
    df = load_caribbean_tracks()

c1, c2, c3, c4 = st.columns(4)
c1.metric("🌀 Ouragans caribéens", f"{df['SID'].nunique():,}")
c2.metric("📅 Années de données", f"{int(df['year'].min())}–{int(df['year'].max())}")
c3.metric("💨 Vent max enregistré", f"{int(df['USA_WIND'].max())} kt")
c4.metric("📆 Année la plus active", str(df.groupby("year")["SID"].nunique().idxmax()))

st.divider()

# ── 4 module tiles ────────────────────────────────────────────────────────────
st.subheader("Explorer la plateforme")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background:#1a0a0a;border:1px solid #DC143C55;border-radius:12px;padding:20px;text-align:center;height:160px;">
        <div style="font-size:36px;">🌀</div>
        <h3 style="color:#DC143C;margin:8px 0 4px 0;">Ouragans</h3>
        <p style="color:#888;font-size:13px;margin:0;">Trajectoires · Stats · Explorateur · Comparateur · Analyse</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#1a0f0a;border:1px solid #FF634755;border-radius:12px;padding:20px;text-align:center;height:160px;">
        <div style="font-size:36px;">🌍</div>
        <h3 style="color:#FF6347;margin:8px 0 4px 0;">Séismes</h3>
        <p style="color:#888;font-size:13px;margin:0;">Carte sismique · Statistiques historiques</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#0a0f1a;border:1px solid #4FC3F755;border-radius:12px;padding:20px;text-align:center;height:160px;">
        <div style="font-size:36px;">🌡️</div>
        <h3 style="color:#4FC3F7;margin:8px 0 4px 0;">Climat</h3>
        <p style="color:#888;font-size:13px;margin:0;">Tendances climatiques · Température océan</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background:#0a1a0a;border:1px solid #81C78455;border-radius:12px;padding:20px;text-align:center;height:160px;">
        <div style="font-size:36px;">🤖</div>
        <h3 style="color:#81C784;margin:8px 0 4px 0;">Prédiction IA</h3>
        <p style="color:#888;font-size:13px;margin:0;">Intensité ouragan par Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Ouragan du jour ───────────────────────────────────────────────────────────
st.subheader("🌀 Ouragan du jour")

CAT_LABELS = {
    0: "Dépression / Tempête tropicale",
    1: "Catégorie 1", 2: "Catégorie 2", 3: "Catégorie 3",
    4: "Catégorie 4", 5: "Catégorie 5",
}
CAT_COLORS = {
    0: "#4FC3F7", 1: "#FFD700", 2: "#FFA500",
    3: "#FF4500", 4: "#DC143C", 5: "#8B0000",
}

per_storm = get_max_category_per_hurricane(df)
named = per_storm[per_storm["NAME"].notna() & (per_storm["NAME"] != "UNNAMED") & (per_storm["max_cat_num"] >= 1)]

random.seed(date.today().toordinal())
odj = named.sample(1, random_state=date.today().toordinal()).iloc[0]

cat_num = int(odj["max_cat_num"])
cat_label = CAT_LABELS.get(cat_num, "Inconnu")
cat_color = CAT_COLORS.get(cat_num, "#808080")

odj_col1, odj_col2 = st.columns([1, 3])
with odj_col1:
    st.markdown(f"""
    <div style="background:#111;border:2px solid {cat_color}55;border-radius:12px;padding:24px;text-align:center;">
        <div style="font-size:48px;">🌀</div>
        <h2 style="color:{cat_color};margin:8px 0 4px 0;">{odj['NAME']}</h2>
        <p style="color:#aaa;font-size:16px;margin:0;">{int(odj['year'])}</p>
        <p style="color:{cat_color};font-size:13px;margin:8px 0 0 0;font-weight:bold;">{cat_label}</p>
    </div>
    """, unsafe_allow_html=True)

with odj_col2:
    kc1, kc2, kc3 = st.columns(3)
    kc1.metric("💨 Vent maximum", f"{int(odj['max_wind'])} kt")
    pres = odj.get("min_pres")
    kc2.metric("🌡️ Pression min", f"{int(pres)} mb" if pres and pres > 0 else "N/A")
    kc3.metric("📊 Catégorie max", cat_label)
    st.caption(
        f"**{odj['NAME']} ({int(odj['year'])})** est l'ouragan du jour — tiré aléatoirement parmi "
        f"{len(named):,} ouragans nommés historiques. Reviens demain pour en découvrir un autre."
    )

st.divider()
st.caption("Source : NOAA HURDAT2 · USGS Earthquake Catalog · CaribScope — Projet open source")
