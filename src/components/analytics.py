"""Inject Plausible Analytics into the Streamlit document.

Configuration via env vars (or st.secrets):
- PLAUSIBLE_DOMAIN  (default: caribscope.fwicss.fr)
- PLAUSIBLE_SCRIPT_URL  (default: https://plausible.io/js/script.js)

Set PLAUSIBLE_DOMAIN to an empty string to disable tracking.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

DEFAULT_DOMAIN = "caribscope.fwicss.fr"
DEFAULT_SCRIPT = "https://plausible.io/js/script.js"


def _setting(name: str, default: str) -> str:
    val = os.environ.get(name)
    if val is not None:
        return val
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, AttributeError):
        return default


def inject_plausible() -> None:
    domain = _setting("PLAUSIBLE_DOMAIN", DEFAULT_DOMAIN)
    if not domain:
        return
    script_url = _setting("PLAUSIBLE_SCRIPT_URL", DEFAULT_SCRIPT)

    components.html(
        f"""
        <script>
          (function() {{
            try {{
              var doc = window.parent.document;
              if (doc.getElementById('plausible-analytics')) return;
              var s = doc.createElement('script');
              s.id = 'plausible-analytics';
              s.defer = true;
              s.setAttribute('data-domain', '{domain}');
              s.src = '{script_url}';
              doc.head.appendChild(s);
            }} catch (e) {{ /* iframe sandbox — silently ignore */ }}
          }})();
        </script>
        """,
        height=0,
    )
