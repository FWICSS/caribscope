"""Internal KPI board — leads captured, sources, daily breakdown.

This page exports personal data (the leads CSV), so access is FAIL-CLOSED:
CARIBSCOPE_KPI_PIN must be set whenever CARIBSCOPE_ENV=production, otherwise
the page refuses to render. Without the production flag it stays open for local
dev only.

A PIN in a text field is a weak gate. For anything beyond a solo project, put
HTTP Basic auth on the reverse proxy in front of this route instead.
"""
import csv
import hmac
import os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.components.analytics import inject_analytics
from src.components.head import inject_head
from src.components.email_capture import LEADS_FILE

st.set_page_config(
    page_title="KPIs internes — CaribScope",
    page_icon="📈",
    layout="wide",
)

inject_analytics("KPIs Internes")
inject_head(
    title="KPIs internes — CaribScope",
    description=(
        "Tableau de bord interne."
    ),
    path="KPIs_Internes",
)


def _expected_pin() -> str | None:
    val = os.environ.get("CARIBSCOPE_KPI_PIN")
    if val:
        return val
    try:
        return st.secrets.get("CARIBSCOPE_KPI_PIN") or None
    except (FileNotFoundError, AttributeError):
        return None


MAX_ATTEMPTS = 5


def _is_authorized() -> bool:
    """Gate the page. Fail CLOSED: no PIN configured means no access in prod.

    The previous behaviour (no PIN -> open) exposed the leads export publicly
    whenever CARIBSCOPE_KPI_PIN was missing from the deployment env.
    """
    expected = _expected_pin()
    if not expected:
        if os.environ.get("CARIBSCOPE_ENV", "").lower() == "production":
            st.title("🔒 KPIs internes")
            st.error(
                "Page indisponible : aucun code d'accès n'est configuré sur cette "
                "instance. Définir CARIBSCOPE_KPI_PIN dans les variables "
                "d'environnement."
            )
            return False
        return True  # dev local uniquement

    if st.session_state.get("_kpi_unlocked"):
        return True

    attempts = st.session_state.get("_kpi_attempts", 0)
    st.title("🔒 KPIs internes")
    if attempts >= MAX_ATTEMPTS:
        st.error("Trop de tentatives. Recharge la page pour réessayer.")
        return False

    pin = st.text_input("Code d'accès", type="password")
    if st.button("Valider"):
        # compare_digest: pas de fuite d'information par le temps de comparaison
        if hmac.compare_digest(pin or "", expected):
            st.session_state["_kpi_unlocked"] = True
            st.session_state["_kpi_attempts"] = 0
            st.rerun()
        else:
            st.session_state["_kpi_attempts"] = attempts + 1
            st.error(f"Code invalide. Tentative {attempts + 1}/{MAX_ATTEMPTS}.")
    return False


if not _is_authorized():
    st.stop()


st.title("📈 KPIs internes — CaribScope")
st.caption(
    "Tableau de bord acquisition-first. Les 5 KPIs quotidiens du framework. "
    "Sources hors-Plausible à reporter manuellement (revenu, ads)."
)

# ── Leads ─────────────────────────────────────────────────────────────────────
if not Path(LEADS_FILE).exists():
    st.info("Aucun lead capté pour l'instant. La capture email écrit dans `data/leads/emails.csv`.")
    st.stop()

leads_df = pd.read_csv(LEADS_FILE)
leads_df["captured_at"] = pd.to_datetime(leads_df["captured_at"], errors="coerce", utc=True)
leads_df["day"] = leads_df["captured_at"].dt.date

today = date.today()
yesterday = today - timedelta(days=1)
last_7 = today - timedelta(days=7)
last_30 = today - timedelta(days=30)

total = len(leads_df)
today_count = (leads_df["day"] == today).sum()
yest_count = (leads_df["day"] == yesterday).sum()
last_7_count = (leads_df["day"] >= last_7).sum()
last_30_count = (leads_df["day"] >= last_30).sum()

# ── 5 KPIs ────────────────────────────────────────────────────────────────────
st.subheader("Les 5 KPIs (jour J)")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Revenu du jour", "0 €", help="À reporter manuellement ici tant qu'il n'y a pas de Stripe.")
c2.metric("📬 Nouveaux emails", today_count, delta=int(today_count) - int(yest_count))
c3.metric(
    "👁️ Vues totales",
    "—",
    help="À reporter depuis Plausible (api Plausible non câblée).",
)
c4.metric("💸 Coût acquisition", "0 €", help="0 € tant que pas d'ads payantes.")
c5.metric("⭐ Nouveaux clients payants", 0)

st.divider()

# ── Leads — détails ───────────────────────────────────────────────────────────
st.subheader("📬 Captures email")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total cumulé", total)
k2.metric("7 derniers jours", last_7_count)
k3.metric("30 derniers jours", last_30_count)
k4.metric("Jour J", today_count)

# Graph par jour
daily = leads_df.groupby("day").size().reset_index(name="emails")
daily["day"] = pd.to_datetime(daily["day"])
if not daily.empty:
    fig = px.bar(daily, x="day", y="emails", title="Captures email par jour")
    fig.update_layout(height=320, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, width="stretch")

# Sources
st.subheader("🚪 Sources de capture")
src = leads_df.groupby("source").size().reset_index(name="count").sort_values("count", ascending=False)
st.dataframe(src, width="stretch")

# Export
with st.expander("📥 Export CSV"):
    st.download_button(
        "Télécharger emails.csv",
        data=Path(LEADS_FILE).read_bytes(),
        file_name="caribscope_leads.csv",
        mime="text/csv",
    )

st.caption(
    "💡 KPIs revenu / vues / coût acquisition à reporter dans le Google Sheet quotidien "
    "(voir TODO.md). Cette page reste la source de vérité pour les emails captés."
)
