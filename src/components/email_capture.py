"""Email capture form + local CSV storage.

Persistence: appends to data/leads/emails.csv (gitignored).
NOTE: in a containerized deploy (Coolify/Docker), mount data/leads as a
persistent volume — otherwise leads are wiped on each rebuild.

GDPR: the form collects personal data, so it must state the purpose, the legal
basis and a link to the privacy policy at the point of collection. See
pages/17_⚖️_Mentions_Légales.py.
"""
import csv
import re
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from src.components.analytics import track_event

LEADS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "leads"
LEADS_FILE = LEADS_DIR / "emails.csv"
FIELDS = ["captured_at", "email", "source", "user_agent"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_CSV_DANGEROUS_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
MAX_SUBMISSIONS_PER_SESSION = 5
PRIVACY_PAGE = "pages/17_⚖️_Mentions_Légales.py"


def _csv_safe(value: str) -> str:
    """Neutralize spreadsheet formula injection at CSV-write time."""
    if value and value[0] in _CSV_DANGEROUS_PREFIXES:
        return "'" + value
    return value


def _user_agent() -> str:
    """Read the real UA from the Streamlit request context.

    The previous implementation read os.environ["HTTP_USER_AGENT"], which is a
    CGI variable that Streamlit never sets: the column was empty on every row.
    """
    try:
        return st.context.headers.get("User-Agent", "")
    except Exception:
        return ""


def _ensure_file() -> None:
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    if not LEADS_FILE.exists():
        with LEADS_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def _store_email(email: str, source: str) -> None:
    _ensure_file()
    row = {
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "email": _csv_safe(email.strip().lower()),
        "source": _csv_safe(source),
        "user_agent": _csv_safe(_user_agent()),
    }
    with LEADS_FILE.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(row)


def email_capture_form(
    source: str,
    title: str = "📬 Reçois l'ouragan du jour par email",
    subtitle: str = "Un mail par jour pendant la saison cyclonique. Zéro spam.",
    cta: str = "M'abonner",
    key_prefix: str = "email_capture",
) -> None:
    """Render an inline email capture form. `source` identifies the page."""
    state_key = f"{key_prefix}_done_{source}"
    if st.session_state.get(state_key):
        st.success("✅ Merci ! Tu recevras le prochain « Ouragan du jour » dans ta boîte mail.")
        # Émis ici et pas avant st.rerun() : un rerun interrompt le script et le
        # composant HTML n'atteindrait jamais le navigateur.
        if not st.session_state.get(f"{state_key}_tracked"):
            st.session_state[f"{state_key}_tracked"] = True
            track_event("newsletter_signup", source=source)
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

        # Mention d'information RGPD au point de collecte (article 13).
        st.caption(
            "En vous abonnant, vous consentez à recevoir la newsletter « Ouragan du jour ». "
            "Votre adresse est conservée par CaribScope pour ce seul usage, jamais cédée, "
            "et supprimée sur simple demande à contact@dimsinfoservices.dev. "
            "Détails dans les [mentions légales et la politique de confidentialité]"
            "(/Mentions_Legales)."
        )

    if submitted:
        attempts = st.session_state.get(f"{key_prefix}_attempts", 0)
        if attempts >= MAX_SUBMISSIONS_PER_SESSION:
            st.error("Trop de tentatives depuis cette session.")
            return
        st.session_state[f"{key_prefix}_attempts"] = attempts + 1

        if not email or not EMAIL_RE.match(email.strip()):
            st.error("Adresse email invalide.")
            return
        if len(email) > 254:  # RFC 5321
            st.error("Adresse email trop longue.")
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
