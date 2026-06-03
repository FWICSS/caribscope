"""Internal KPI board — leads captured, sources, daily breakdown.

Protected by a simple env var (CARIBSCOPE_KPI_PIN). If unset, the page is open
in local dev. Set it in Coolify env vars for prod.
"""
import csv
import os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.components.analytics import inject_plausible
from src.components.email_capture import LEADS_FILE

st.set_page_config(
    page_title="KPIs internes — CaribScope",
    page_icon="📈",
    layout="wide",
)

inject_plausible()


def _expected_pin() -> str | None:
    val = os.environ.get("CARIBSCOPE_KPI_PIN")
    if val:
        return val
    try:
        return st.secrets.get("CARIBSCOPE_KPI_PIN") or None
    except (FileNotFoundError, AttributeError):
        return None


def _is_authorized() -> bool:
    expected = _expected_pin()
    if not expected:
        return True
    if st.session_state.get("_kpi_unlocked"):
        return True
    st.title("🔒 KPIs internes")
    pin = st.text_input("Code d'accès", type="password")
    if st.button("Valider"):
        if pin == expected:
            st.session_state["_kpi_unlocked"] = True
            st.rerun()
        else:
            st.error("Code invalide.")
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
