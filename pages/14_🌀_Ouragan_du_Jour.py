import json
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data.loader import load_caribbean_tracks
from src.analysis.statistics import get_max_category_per_hurricane
from src.viz.maps import plot_single_track
from src.viz.charts import plot_hurricane_timeline
from src.components.analytics import inject_plausible
from src.components.email_capture import email_capture_form
from src.viz.share import share_buttons

st.set_page_config(
    page_title="Ouragan du Jour — CaribScope",
    page_icon="🌀",
    layout="wide",
)

inject_plausible()

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_descriptions() -> dict:
    p = Path("data/hurricane_descriptions.json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

@st.cache_data
def load_named_storms():
    df = load_caribbean_tracks()
    per_storm = get_max_category_per_hurricane(df)
    named = per_storm[
        per_storm["NAME"].notna() &
        (per_storm["NAME"] != "UNNAMED") &
        (per_storm["max_cat_num"] >= 1)
    ].reset_index(drop=True)
    return df, named

df, named = load_named_storms()
descriptions = load_descriptions()

CAT_LABELS = {
    0: "Dépression / Tempête tropicale",
    1: "Catégorie 1", 2: "Catégorie 2", 3: "Catégorie 3",
    4: "Catégorie 4", 5: "Catégorie 5",
}
CAT_COLORS = {
    0: "#4FC3F7", 1: "#FFD700", 2: "#FFA500",
    3: "#FF4500", 4: "#DC143C", 5: "#8B0000",
}
CAT_EMOJIS = {0: "🌀", 1: "🌀", 2: "🌀", 3: "⚠️", 4: "🔴", 5: "☠️"}

# ── Sélection de l'ouragan ────────────────────────────────────────────────────
seed = date.today().toordinal()
odj = named.sample(1, random_state=seed).iloc[0]

name     = odj["NAME"]
year     = int(odj["year"])
cat_num  = int(odj["max_cat_num"])
cat_label = CAT_LABELS.get(cat_num, "Inconnu")
cat_color = CAT_COLORS.get(cat_num, "#808080")
cat_emoji = CAT_EMOJIS.get(cat_num, "🌀")
desc_key  = f"{name}_{year}"
desc      = descriptions.get(desc_key, {})

track = df[(df["NAME"] == name) & (df["year"] == year)]
max_wind = track["USA_WIND"].max()
min_pres = track["USA_PRES"].min()
dates    = track["Hurricane_Date"].dropna().sort_values()
duration = (dates.iloc[-1] - dates.iloc[0]).days if len(dates) >= 2 else None

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d0d0d,#1a0505);
            border:2px solid {cat_color}55;border-radius:16px;
            padding:32px 40px;margin-bottom:24px;">
    <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
        <div style="font-size:72px;line-height:1;">{cat_emoji}</div>
        <div>
            <h1 style="margin:0;font-size:3rem;color:{cat_color};letter-spacing:2px;">
                {name}
            </h1>
            <p style="margin:4px 0 0 0;color:#aaa;font-size:1.2rem;">{year}</p>
        </div>
        <div style="margin-left:auto;">
            <span style="background:{cat_color};color:#000;font-weight:bold;
                         padding:8px 18px;border-radius:20px;font-size:0.95rem;">
                {cat_label}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("🌀 Ouragan du jour — tiré aléatoirement parmi les ouragans caribéens historiques")

st.divider()

# ── Métriques ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("💨 Vent max", f"{int(max_wind)} kt  ({round(max_wind * 1.852)} km/h)" if pd.notna(max_wind) else "N/A")
c2.metric("🌡️ Pression min", f"{int(min_pres)} mb" if pd.notna(min_pres) else "N/A")
c3.metric("📊 Catégorie max", cat_label)
c4.metric("⏱️ Durée", f"{duration} jours" if duration is not None else "N/A")

st.divider()

# ── Résumé IA ─────────────────────────────────────────────────────────────────
if desc and not desc.get("error") and desc.get("resume"):
    st.markdown(f"""
    <div style="background:#111827;border-left:4px solid {cat_color};
                border-radius:0 8px 8px 0;padding:20px 24px;margin-bottom:20px;">
        <p style="color:#e5e7eb;font-size:1.05rem;line-height:1.7;margin:0;font-style:italic;">
            {desc['resume']}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Carte + Timeline ──────────────────────────────────────────────────────────
col_map, col_chart = st.columns([3, 2])
with col_map:
    st.plotly_chart(plot_single_track(df, name, year), width="stretch")
    share_buttons(
        page_path=f"Ouragan_du_Jour?storm={name}&year={year}",
        label=f"{name} ({year}) — CaribScope",
        key=f"share_track_{name}_{year}",
    )
with col_chart:
    st.plotly_chart(plot_hurricane_timeline(df, name, year), width="stretch")

st.divider()

# ── Analyse IA ────────────────────────────────────────────────────────────────
if desc and not desc.get("error"):

    st.subheader("🤖 Analyse par intelligence artificielle")

    # Analyse complète
    if desc.get("analyse_complete"):
        st.markdown("#### Analyse complète")
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;
                    padding:24px;line-height:1.8;color:#cbd5e1;">
            {desc['analyse_complete']}
        </div>
        """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    # Points clés
    with col_l:
        if desc.get("points_cles"):
            st.markdown("#### Points clés")
            for pt in desc["points_cles"]:
                st.markdown(f"""
                <div style="background:#161B22;border:1px solid #30363d;border-radius:8px;
                            padding:10px 14px;margin-bottom:8px;color:#e2e8f0;">
                    ▸ {pt}
                </div>
                """, unsafe_allow_html=True)

    # Anecdote + Comparaison
    with col_r:
        if desc.get("anecdote"):
            st.markdown("#### Anecdote")
            st.markdown(f"""
            <div style="background:#1a1200;border:1px solid #FFD70044;border-radius:8px;
                        padding:14px 16px;color:#FFD700;line-height:1.6;">
                💡 {desc['anecdote']}
            </div>
            """, unsafe_allow_html=True)

        if desc.get("comparaison"):
            st.markdown("#### Comparaison historique")
            st.markdown(f"""
            <div style="background:#0a1628;border:1px solid #4FC3F744;border-radius:8px;
                        padding:14px 16px;color:#94a3b8;line-height:1.6;margin-top:16px;">
                🔄 {desc['comparaison']}
            </div>
            """, unsafe_allow_html=True)

    # Fiabilité
    if desc.get("fiabilite_info"):
        st.caption(f"ℹ️ {desc['fiabilite_info']}")

else:
    st.info("Aucune analyse IA disponible pour cet ouragan.")

st.divider()

# ── Données brutes ────────────────────────────────────────────────────────────
with st.expander("📋 Données brutes HURDAT2"):
    st.dataframe(
        track[["Hurricane_Date", "LAT", "LON", "USA_WIND", "USA_PRES", "category"]]
        .sort_values("Hurricane_Date")
        .reset_index(drop=True),
        width="stretch",
    )

st.divider()

# ── Capture email ─────────────────────────────────────────────────────────────
email_capture_form(
    source="ouragan_du_jour",
    title="📬 Reçois l'ouragan du jour chaque matin",
    subtitle="Un ouragan historique + une alerte si une tempête active menace la Caraïbe. 0 spam.",
)

st.caption("Source : NOAA HURDAT2 · Analyse : Claude AI (Anthropic) · CaribScope — Projet open source")
