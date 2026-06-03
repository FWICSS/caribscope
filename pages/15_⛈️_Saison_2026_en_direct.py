"""Live Atlantic hurricane season tracker (NHC current storms)."""
import datetime as dt
from typing import Any

import plotly.graph_objects as go
import requests
import streamlit as st

from src.components.analytics import inject_plausible
from src.components.email_capture import email_capture_form
from src.viz.share import share_buttons

st.set_page_config(
    page_title="Saison 2026 en direct — CaribScope",
    page_icon="⛈️",
    layout="wide",
)

inject_plausible()

NHC_FEED = "https://www.nhc.noaa.gov/CurrentStorms.json"
ATLANTIC_BASINS = {"AL", "atlantic", "atl"}

CAT_PALETTE = {
    "TD": "#4FC3F7",
    "TS": "#FFD700",
    "HU1": "#FFA500",
    "HU2": "#FF7043",
    "HU3": "#FF4500",
    "HU4": "#DC143C",
    "HU5": "#8B0000",
    "PT": "#90A4AE",
    "STD": "#4FC3F7",
    "STS": "#FFD700",
}

CLASSIFICATION_LABEL = {
    "TD": "Dépression tropicale",
    "TS": "Tempête tropicale",
    "HU": "Ouragan",
    "PT": "Post-tropical",
    "STD": "Dépression subtropicale",
    "STS": "Tempête subtropicale",
}


@st.cache_data(ttl=900)
def fetch_current_storms() -> dict[str, Any]:
    try:
        r = requests.get(NHC_FEED, timeout=10, headers={"User-Agent": "CaribScope/1.0"})
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as exc:
        return {"_error": str(exc), "activeStorms": []}


def _classification_key(storm: dict[str, Any]) -> str:
    cls = (storm.get("classification") or "").upper()
    if cls != "HU":
        return cls
    intensity = storm.get("intensity")
    try:
        wind = int(intensity) if intensity is not None else 0
    except (TypeError, ValueError):
        wind = 0
    if wind >= 157:
        return "HU5"
    if wind >= 130:
        return "HU4"
    if wind >= 111:
        return "HU3"
    if wind >= 96:
        return "HU2"
    return "HU1"


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _filter_atlantic(storms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for s in storms:
        basin = str(s.get("binNumber") or s.get("basin") or "").upper()
        if basin.startswith("AL") or basin in ATLANTIC_BASINS or s.get("id", "").upper().startswith("AL"):
            out.append(s)
    return out


# ── Header ────────────────────────────────────────────────────────────────────
st.title("⛈️ Saison cyclonique 2026 — en direct")
st.caption(
    "Tempêtes actives surveillées par le National Hurricane Center (NOAA). "
    "Mise à jour automatique toutes les 15 minutes."
)

data = fetch_current_storms()
if data.get("_error"):
    st.error(f"Impossible de joindre le flux NHC : {data['_error']}")

all_storms = data.get("activeStorms", []) or []
atlantic = _filter_atlantic(all_storms)

# ── KPIs ──────────────────────────────────────────────────────────────────────
now = dt.datetime.now(dt.timezone.utc)
season_start = dt.datetime(now.year, 6, 1, tzinfo=dt.timezone.utc)
season_end = dt.datetime(now.year, 11, 30, tzinfo=dt.timezone.utc)
in_season = season_start <= now <= season_end

c1, c2, c3, c4 = st.columns(4)
c1.metric("🌀 Tempêtes actives (Atlantique)", len(atlantic))
c2.metric("🌍 Tempêtes actives (Monde)", len(all_storms))
c3.metric("📅 Saison", f"{now.year}", "en cours" if in_season else "hors saison")
c4.metric(
    "🕒 Dernière mise à jour",
    now.strftime("%H:%M UTC"),
    help="Cache rafraîchi toutes les 15 minutes.",
)

st.divider()

# ── Aucune tempête active ────────────────────────────────────────────────────
if not atlantic:
    if in_season:
        st.success(
            "✅ **Aucune tempête active dans l'Atlantique en ce moment.** "
            "La saison est en cours — la situation peut évoluer rapidement. "
            "Reviens demain ou abonne-toi pour être alerté."
        )
    else:
        st.info(
            f"🌤️ Hors saison cyclonique active (saison officielle Atlantique : "
            f"1ᵉʳ juin → 30 novembre). Aucune tempête tropicale n'est attendue."
        )

    st.markdown("#### En attendant — explore l'historique")
    cols = st.columns(3)
    with cols[0]:
        st.page_link("pages/14_🌀_Ouragan_du_Jour.py", label="🌀 Ouragan du jour", icon="🌀")
    with cols[1]:
        st.page_link("pages/1_🗺️_Trajectoires.py", label="🗺️ Trajectoires historiques", icon="🗺️")
    with cols[2]:
        st.page_link("pages/12_🔥_Heatmap_Risques.py", label="🔥 Zones à risque", icon="🔥")

else:
    # ── Carte ─────────────────────────────────────────────────────────────────
    st.subheader("🗺️ Position actuelle des systèmes")
    fig = go.Figure()
    for s in atlantic:
        lat = _as_float(s.get("latitudeNumeric") or s.get("latitude"))
        lon = _as_float(s.get("longitudeNumeric") or s.get("longitude"))
        if lat is None or lon is None:
            continue
        key = _classification_key(s)
        color = CAT_PALETTE.get(key, "#FFFFFF")
        name = s.get("name") or s.get("id") or "Système"
        intensity = s.get("intensity") or "?"
        fig.add_trace(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode="markers+text",
            marker=dict(size=22, color=color),
            text=[name],
            textposition="top right",
            textfont=dict(color="#fff", size=13),
            hovertemplate=(
                f"<b>{name}</b><br>"
                f"Catégorie: {key}<br>"
                f"Vent: {intensity} kt<br>"
                f"Lat: {lat:.1f}°, Lon: {lon:.1f}°"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", center=dict(lat=20, lon=-60), zoom=3),
        margin=dict(l=0, r=0, t=10, b=0),
        height=550,
    )
    st.plotly_chart(fig, width="stretch")
    share_buttons(page_path="Saison_2026_en_direct", label="Saison cyclonique 2026 en direct — CaribScope")

    st.divider()

    # ── Cartes par système ────────────────────────────────────────────────────
    st.subheader("📋 Détail des systèmes actifs")
    for s in atlantic:
        key = _classification_key(s)
        color = CAT_PALETTE.get(key, "#FFFFFF")
        cls = (s.get("classification") or "").upper()
        label = CLASSIFICATION_LABEL.get(cls, cls or "Système")
        name = s.get("name") or s.get("id") or "Système"
        intensity = s.get("intensity") or "?"
        pressure = s.get("pressure") or "?"
        movement = s.get("movementDir") or ""
        movement_speed = s.get("movementSpeed") or ""

        st.markdown(
            f"""
            <div style="background:#0d1117;border-left:4px solid {color};
                        border-radius:0 8px 8px 0;padding:16px 20px;margin-bottom:12px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <h3 style="margin:0;color:{color};">{name}</h3>
                    <span style="background:{color};color:#000;font-weight:bold;
                                 padding:3px 10px;border-radius:12px;font-size:0.8rem;">
                        {label} · {key}
                    </span>
                </div>
                <p style="color:#94a3b8;margin:8px 0 0 0;">
                    💨 {intensity} kt · 🌡️ {pressure} mb · ➡️ {movement} {movement_speed} kt
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Capture email ─────────────────────────────────────────────────────────────
email_capture_form(
    source="saison_2026",
    title="🚨 Sois alerté dès qu'une tempête menace la Caraïbe",
    subtitle="Alerte email quand un système actif entre dans la zone Antilles-Caraïbes. Saison 2026 (juin → novembre).",
    cta="M'alerter",
)

st.caption(
    "Source : National Hurricane Center (NOAA) · Flux CurrentStorms.json · "
    "Affichage non officiel — pour une décision opérationnelle, consulter directement nhc.noaa.gov."
)
