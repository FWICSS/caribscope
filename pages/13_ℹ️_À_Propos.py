import streamlit as st

st.set_page_config(
    page_title="À propos — CaribScope",
    page_icon="ℹ️",
    layout="wide",
)

st.markdown("""
<meta name="description" content="CaribScope — Observatoire open source des risques naturels dans la Caraïbe. 170 ans de données ouragans, séismes et climat. Projet de Dimitri Aigle.">
<meta property="og:title" content="CaribScope — Observatoire Caribéen">
<meta property="og:description" content="170 ans de données ouragans, séismes et climat dans la Caraïbe. Open source, gratuit, propulsé par NOAA & USGS.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://caribscope.fwicss.fr">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CaribScope — Observatoire Caribéen">
<meta name="twitter:description" content="170 ans de données ouragans, séismes et climat dans la Caraïbe. Open source.">
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0;">
    <div style="font-size:64px;">🌀</div>
    <h1 style="font-size:2.4rem;margin:12px 0 8px 0;">CaribScope</h1>
    <p style="color:#aaa;font-size:1.1rem;max-width:600px;margin:0 auto;">
        Observatoire open source des risques naturels dans la Caraïbe —
        ouragans, séismes, tendances climatiques et prédiction par IA.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Le projet ─────────────────────────────────────────────────────────────────
col_proj, col_stack = st.columns([3, 2])

with col_proj:
    st.subheader("Le projet")
    st.markdown("""
    **CaribScope** est né d'un constat simple : les données sur les risques naturels caribéens
    existent depuis 170 ans, mais elles sont éparpillées, techniques et inaccessibles au grand public.

    L'objectif est d'en faire **l'outil de référence francophone** pour comprendre et visualiser
    ces phénomènes — que tu sois chercheur, journaliste, décideur ou simplement curieux.

    **Ce que couvre CaribScope :**
    - 🌀 **Ouragans** — 1 800+ trajectoires caribéennes depuis 1851 (NOAA HURDAT2)
    - 🌍 **Séismes** — Catalogue sismique Caraïbes (USGS Earthquake Catalog)
    - 🌡️ **Climat** — Tendances de température et surface océanique (SST)
    - 🤖 **IA** — Prédiction de l'intensité des ouragans par Random Forest

    Le projet est **100% open source** et gratuit.
    """)

with col_stack:
    st.subheader("Stack technique")
    st.markdown("""
    | Composant | Technologie |
    |---|---|
    | App | Streamlit |
    | Cartes | Plotly Mapbox |
    | Data | pandas · numpy |
    | ML | scikit-learn |
    | Déploiement | Docker · Coolify |
    | Données | NOAA · USGS |
    """)

st.divider()

# ── Fondateur ─────────────────────────────────────────────────────────────────
st.subheader("Le fondateur")

col_bio, col_links = st.columns([3, 1])

with col_bio:
    st.markdown("""
    <div style="background:#161B22;border:1px solid #30363d;border-radius:12px;padding:28px;">
        <h3 style="margin:0 0 4px 0;">Dimitri Aigle</h3>
        <p style="color:#DC143C;margin:0 0 16px 0;font-size:0.95rem;">Fondateur · Développeur · Data Engineer</p>
        <p style="color:#ccc;line-height:1.7;margin:0;">
            Passionné de données et de la Caraïbe, j'ai lancé CaribScope pour rendre accessibles
            170 ans de données sur les risques naturels caribéens. Le projet combine data engineering,
            visualisation interactive et machine learning appliqué à des données météorologiques réelles.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_links:
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:12px;padding-top:8px;">
        <a href="https://github.com/FWICSS" target="_blank"
           style="display:block;background:#161B22;border:1px solid #30363d;border-radius:8px;
                  padding:12px 16px;text-decoration:none;color:#fff;text-align:center;">
            <span style="font-size:20px;">🐙</span><br>
            <span style="font-size:13px;color:#aaa;">GitHub</span>
        </a>
        <a href="https://dimitriaigle.fr" target="_blank"
           style="display:block;background:#161B22;border:1px solid #30363d;border-radius:8px;
                  padding:12px 16px;text-decoration:none;color:#fff;text-align:center;">
            <span style="font-size:20px;">🌐</span><br>
            <span style="font-size:13px;color:#aaa;">Site web</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Sources de données ────────────────────────────────────────────────────────
st.subheader("Sources de données")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div style="background:#161B22;border:1px solid #30363d;border-radius:8px;padding:16px;">
        <h4 style="color:#DC143C;margin:0 0 8px 0;">🌀 NOAA HURDAT2</h4>
        <p style="color:#aaa;font-size:13px;margin:0;">
            Base de données officielle de la NOAA couvrant toutes les tempêtes tropicales
            de l'Atlantique depuis 1851. Mise à jour annuellement.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="background:#161B22;border:1px solid #30363d;border-radius:8px;padding:16px;">
        <h4 style="color:#FF6347;margin:0 0 8px 0;">🌍 USGS Earthquake Catalog</h4>
        <p style="color:#aaa;font-size:13px;margin:0;">
            Catalogue sismique mondial de l'US Geological Survey.
            Données de magnitude, profondeur et localisation des séismes.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div style="background:#161B22;border:1px solid #30363d;border-radius:8px;padding:16px;">
        <h4 style="color:#4FC3F7;margin:0 0 8px 0;">🌡️ SST Caraïbes</h4>
        <p style="color:#aaa;font-size:13px;margin:0;">
            Données de température de surface océanique (SST)
            pour la zone caribéenne, 1980–2025.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Contribuer ────────────────────────────────────────────────────────────────
st.subheader("Contribuer")
st.markdown("""
CaribScope est open source — les contributions sont bienvenues.

**Comment participer :**
- 🐛 Signaler un bug via les [Issues GitHub](https://github.com/FWICSS/caribscope/issues)
- 💡 Proposer une feature via une Issue ou une Pull Request
- ⭐ Donner une étoile au projet sur GitHub pour le faire connaître

```bash
git clone https://github.com/FWICSS/caribscope.git
cd caribscope
pip install -r requirements.txt
streamlit run app.py
```
""")

st.caption("CaribScope — Projet open source · MIT License · Données NOAA & USGS en accès public")
