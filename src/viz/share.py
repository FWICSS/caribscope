"""Share / export helpers for Plotly charts in Streamlit.

PNG download is delegated to Plotly's built-in modebar (browser-side, no kaleido
needed). This module adds a "copy link" + social share buttons under a chart.
"""
import os
import urllib.parse

import streamlit as st
import streamlit.components.v1 as components

BASE_URL_DEFAULT = "https://caribscope.fwicss.fr"


def _base_url() -> str:
    return os.environ.get("CARIBSCOPE_BASE_URL", BASE_URL_DEFAULT).rstrip("/")


def share_buttons(
    page_path: str = "",
    label: str = "CaribScope — Observatoire Caribéen",
    key: str = "share",
) -> None:
    """Render a share toolbar: copy link, X (Twitter), LinkedIn.

    Args:
        page_path: optional suffix appended to base URL (e.g. "Ouragan_du_Jour?storm=Maria&year=2017")
        label: text used for share intent
        key: unique key per chart on the page
    """
    url = f"{_base_url()}/{page_path.lstrip('/')}" if page_path else _base_url()
    enc_url = urllib.parse.quote(url, safe="")
    enc_text = urllib.parse.quote(label, safe="")
    x_url = f"https://twitter.com/intent/tweet?text={enc_text}&url={enc_url}"
    li_url = f"https://www.linkedin.com/sharing/share-offsite/?url={enc_url}"

    components.html(
        f"""
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;
                    font-family:system-ui,sans-serif;margin:4px 0 12px 0;">
            <button id="copy-{key}"
                    style="background:#1f2937;color:#e5e7eb;border:1px solid #374151;
                           padding:6px 12px;border-radius:6px;cursor:pointer;font-size:13px;">
                🔗 Copier le lien
            </button>
            <a href="{x_url}" target="_blank" rel="noopener"
               style="background:#0f172a;color:#e5e7eb;border:1px solid #374151;
                      padding:6px 12px;border-radius:6px;text-decoration:none;font-size:13px;">
                𝕏 Partager
            </a>
            <a href="{li_url}" target="_blank" rel="noopener"
               style="background:#0a66c2;color:#fff;border:1px solid #0a66c2;
                      padding:6px 12px;border-radius:6px;text-decoration:none;font-size:13px;">
                in Partager
            </a>
            <span style="color:#888;font-size:12px;">
                📷 Télécharger en PNG : icône appareil photo dans la barre Plotly
            </span>
            <span id="status-{key}" style="color:#22c55e;font-size:12px;"></span>
        </div>
        <script>
        (function() {{
            var btn = document.getElementById('copy-{key}');
            var status = document.getElementById('status-{key}');
            if (!btn) return;
            btn.addEventListener('click', function() {{
                navigator.clipboard.writeText('{url}').then(function() {{
                    status.textContent = '✓ copié';
                    setTimeout(function() {{ status.textContent = ''; }}, 1800);
                }}).catch(function() {{
                    status.textContent = '✗ échec — copie manuelle';
                }});
            }});
        }})();
        </script>
        """,
        height=60,
    )
