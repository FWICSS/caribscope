"""Email capture form + local CSV storage.

Persistence: appends to data/leads/emails.csv (gitignored).
NOTE: in a containerized deploy (Coolify/Docker), mount data/leads as a
persistent volume — otherwise leads are wiped on each rebuild.
"""
import csv
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

LEADS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "leads"
LEADS_FILE = LEADS_DIR / "emails.csv"
FIELDS = ["captured_at", "email", "source", "user_agent"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _ensure_file() -> None:
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    if not LEADS_FILE.exists():
        with LEADS_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def _store_email(email: str, source: str) -> None:
    _ensure_file()
    row = {
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "email": email.strip().lower(),
        "source": source,
        "user_agent": os.environ.get("HTTP_USER_AGENT", ""),
    }
    with LEADS_FILE.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(row)


def email_capture_form(
    source: str,
    title: str = "📬 Reçois l'ouragan du jour par email",
    subtitle: str = "Un mail par jour pendant la saison cyclonique. Zéro spam, désabonnement en 1 clic.",
    cta: str = "M'abonner",
    key_prefix: str = "email_capture",
) -> None:
    """Render an inline email capture form. `source` identifies the page."""
    state_key = f"{key_prefix}_done_{source}"
    if st.session_state.get(state_key):
        st.success("✅ Merci ! Tu recevras le prochain « Ouragan du jour » dans ta boîte mail.")
        return

    with st.form(key=f"{key_prefix}_{source}", clear_on_submit=True):
        st.markdown(f"#### {title}")
        st.caption(subtitle)
        col_input, col_button = st.columns([3, 1])
        with col_input:
            email = st.text_input(
                "Email",
                placeholder="ton@email.com",
                label_visibility="collapsed",
                key=f"{key_prefix}_input_{source}",
            )
        with col_button:
            submitted = st.form_submit_button(cta, use_container_width=True)

    if submitted:
        if not email or not EMAIL_RE.match(email.strip()):
            st.error("Adresse email invalide.")
            return
        try:
            _store_email(email, source)
        except OSError as exc:
            st.error(f"Erreur de stockage : {exc}")
            return
        st.session_state[state_key] = True
        st.rerun()


def get_leads_count() -> int:
    if not LEADS_FILE.exists():
        return 0
    with LEADS_FILE.open(encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))
