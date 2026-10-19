"""Google Analytics 4 injection with CNIL-compliant consent gating.

GA4 sets cookies and transfers data outside the EU: unlike the previous
Plausible setup, it MUST NOT load before the visitor has explicitly opted in.
This module therefore:

1. pushes Consent Mode v2 defaults (everything denied) before anything else;
2. renders a consent banner in the parent document;
3. loads gtag.js only once the visitor accepts.

Configuration via env vars (or st.secrets):
- GA4_MEASUREMENT_ID   e.g. "G-XXXXXXXXXX". Empty/absent disables all tracking.

Streamlit reruns the whole script on every widget interaction, so page_view
events are guarded by st.session_state to avoid counting one visit many times.
"""
import json
import os
import re
from typing import Any

import streamlit as st

from src.components.embed import embed_html

MEASUREMENT_ID_RE = re.compile(r"^G-[A-Z0-9]{4,20}$")
CONSENT_STORAGE_KEY = "caribscope_consent"


def _setting(name: str, default: str = "") -> str:
    val = os.environ.get(name)
    if val is not None:
        return val
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, AttributeError):
        return default


def measurement_id() -> str:
    """Return a validated GA4 measurement ID, or "" if tracking is disabled."""
    mid = _setting("GA4_MEASUREMENT_ID").strip()
    return mid if MEASUREMENT_ID_RE.match(mid) else ""


def _bootstrap_js(mid: str) -> str:
    """Consent defaults + banner + conditional gtag.js loading."""
    return """
    (function () {
      var doc, win;
      try { doc = window.parent.document; win = window.parent; }
      catch (e) { return; }   // sandboxed iframe, nothing we can do

      var MID = %(mid)s;
      var KEY = %(key)s;

      win.dataLayer = win.dataLayer || [];
      function gtag() { win.dataLayer.push(arguments); }
      win.gtag = win.gtag || gtag;

      // Consent Mode v2: deny everything until the visitor says otherwise.
      if (!win.__csConsentDefaults) {
        gtag('consent', 'default', {
          ad_storage: 'denied',
          ad_user_data: 'denied',
          ad_personalization: 'denied',
          analytics_storage: 'denied',
          functionality_storage: 'granted',
          security_storage: 'granted',
          wait_for_update: 500
        });
        win.__csConsentDefaults = true;
      }

      function loadGa() {
        if (doc.getElementById('ga4-script')) return;
        var s = doc.createElement('script');
        s.id = 'ga4-script';
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=' + MID;
        doc.head.appendChild(s);
        gtag('js', new Date());
        // send_page_view false: page views are sent explicitly on navigation.
        gtag('config', MID, { anonymize_ip: true, send_page_view: false });
      }

      function accept() {
        try { win.localStorage.setItem(KEY, 'granted'); } catch (e) {}
        gtag('consent', 'update', { analytics_storage: 'granted' });
        loadGa();
        removeBanner();
        if (win.__csPendingPageView) {
          gtag('event', 'page_view', win.__csPendingPageView);
          win.__csPendingPageView = null;
        }
      }

      function refuse() {
        try { win.localStorage.setItem(KEY, 'denied'); } catch (e) {}
        removeBanner();
      }

      function removeBanner() {
        var b = doc.getElementById('cs-consent-banner');
        if (b) b.remove();
      }

      function stored() {
        try { return win.localStorage.getItem(KEY); } catch (e) { return null; }
      }

      function showBanner() {
        if (doc.getElementById('cs-consent-banner')) return;
        var wrap = doc.createElement('div');
        wrap.id = 'cs-consent-banner';
        wrap.setAttribute('role', 'dialog');
        wrap.setAttribute('aria-label', "Consentement aux mesures d'audience");
        wrap.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:2147483647;' +
          'background:#161B22;border-top:1px solid #30363d;color:#e6edf3;' +
          'padding:16px 20px;display:flex;gap:16px;align-items:center;' +
          'flex-wrap:wrap;justify-content:center;font-family:system-ui,sans-serif;font-size:14px;';

        var txt = doc.createElement('p');
        txt.style.cssText = 'margin:0;max-width:640px;line-height:1.5;color:#c9d1d9;';
        txt.textContent = "CaribScope utilise Google Analytics pour mesurer son audience. " +
          "Ces cookies ne sont d\u00e9pos\u00e9s qu'avec votre accord. Vous pouvez refuser " +
          "sans perdre aucune fonctionnalit\u00e9 du site.";

        var btnA = doc.createElement('button');
        btnA.type = 'button';
        btnA.textContent = 'Accepter';
        btnA.style.cssText = 'background:#DC143C;color:#fff;border:none;padding:10px 22px;' +
          'border-radius:6px;cursor:pointer;font-size:14px;font-weight:600;';
        btnA.addEventListener('click', accept);

        var btnR = doc.createElement('button');
        btnR.type = 'button';
        btnR.textContent = 'Refuser';
        btnR.style.cssText = 'background:transparent;color:#e6edf3;border:1px solid #6e7681;' +
          'padding:10px 22px;border-radius:6px;cursor:pointer;font-size:14px;';
        btnR.addEventListener('click', refuse);

        var link = doc.createElement('a');
        link.href = '/Mentions_Legales';
        link.textContent = 'En savoir plus';
        link.style.cssText = 'color:#79c0ff;font-size:13px;text-decoration:underline;';

        wrap.appendChild(txt);
        wrap.appendChild(btnA);
        wrap.appendChild(btnR);
        wrap.appendChild(link);
        doc.body.appendChild(wrap);
      }

      // Exposed so the legal page can offer a "change my choice" button.
      win.caribscopeResetConsent = function () {
        try { win.localStorage.removeItem(KEY); } catch (e) {}
        gtag('consent', 'update', { analytics_storage: 'denied' });
        showBanner();
      };

      win.caribscopeConsentState = function () { return stored() || 'unset'; };

      var choice = stored();
      if (choice === 'granted') { loadGa(); }
      else if (choice !== 'denied') { showBanner(); }
    })();
    """ % {"mid": json.dumps(mid), "key": json.dumps(CONSENT_STORAGE_KEY)}


def _page_view_js(page_title: str, page_path: str) -> str:
    payload = json.dumps({
        "page_title": page_title,
        "page_path": page_path,
        "page_location": None,  # filled in browser-side, see below
    })
    return """
    (function () {
      var win;
      try { win = window.parent; } catch (e) { return; }
      var params = %(payload)s;
      params.page_location = win.location.href;
      if (!win.gtag) { return; }
      if (win.caribscopeConsentState && win.caribscopeConsentState() !== 'granted') {
        win.__csPendingPageView = params;   // replayed if consent is given
        return;
      }
      win.gtag('event', 'page_view', params);
    })();
    """ % {"payload": payload}


def inject_analytics(page_title: str | None = None) -> None:
    """Set up GA4 + consent banner, and send one page_view per page change.

    Call once at the top of every page, right after st.set_page_config().
    """
    mid = measurement_id()
    if not mid:
        return

    page_title = page_title or "CaribScope"
    page_path = "/" + page_title.replace(" ", "_")

    script = _bootstrap_js(mid)

    # Streamlit reruns on every interaction: only emit page_view when the page
    # actually changed, otherwise a single visit inflates into dozens of hits.
    if st.session_state.get("_ga_last_page") != page_title:
        st.session_state["_ga_last_page"] = page_title
        script += _page_view_js(page_title, page_path)

    embed_html("<script>%s</script>" % script, height=0)


def track_event(name: str, **params: Any) -> None:
    """Send a GA4 custom event (no-op when tracking is off or consent denied)."""
    if not measurement_id():
        return
    payload = json.dumps(params)
    embed_html(
        """
        <script>
        (function () {
          var win;
          try { win = window.parent; } catch (e) { return; }
          if (!win.gtag) return;
          if (win.caribscopeConsentState && win.caribscopeConsentState() !== 'granted') return;
          win.gtag('event', %(name)s, %(payload)s);
        })();
        </script>
        """ % {"name": json.dumps(name), "payload": payload},
        height=0,
    )


def consent_reset_button() -> None:
    """Render a 'change my cookie choice' control (for the legal page)."""
    if not measurement_id():
        st.caption("La mesure d'audience est désactivée sur cette instance.")
        return
    embed_html(
        """
        <button type="button" id="cs-reset-consent"
          style="background:#21262d;color:#e6edf3;border:1px solid #30363d;padding:10px 18px;
                 border-radius:6px;cursor:pointer;font-size:14px;font-family:system-ui,sans-serif;">
          Modifier mon choix sur les cookies
        </button>
        <script>
          document.getElementById('cs-reset-consent').addEventListener('click', function () {
            try { window.parent.caribscopeResetConsent(); } catch (e) {}
          });
        </script>
        """,
        height=56,
    )
