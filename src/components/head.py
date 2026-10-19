"""Document head fixes that Streamlit does not expose.

Streamlit renders st.markdown() into the <body>, so <meta> tags written that way
never reach the <head> and are ignored by crawlers and social scrapers. This
module moves them where they belong, from inside the component iframe.

Scope and honesty about it: social scrapers (LinkedIn, X, WhatsApp) do not
execute JavaScript at all, so they will still see the bare Streamlit shell.
Fixing previews for real requires server-rendered HTML, which is what the
planned Next.js migration is for. What this module does fix today:

- lang="fr" instead of lang="en" (screen readers mispronounce the whole site);
- a canonical URL, so JS-rendering crawlers stop treating every path as a dup;
- meta description / OG / Twitter tags placed in <head> rather than <body>.
"""
import json
import os

import streamlit as st

from src.components.embed import embed_html

BASE_URL_DEFAULT = "https://caribscope.fwicss.fr"
DEFAULT_IMAGE = "/app/static/og-default.png"


def _base_url() -> str:
    return os.environ.get("CARIBSCOPE_BASE_URL", BASE_URL_DEFAULT).rstrip("/")


def inject_head(
    title: str,
    description: str,
    path: str = "",
    image: str | None = None,
) -> None:
    """Set lang, canonical and social meta tags on the parent document."""
    canonical = f"{_base_url()}/{path.lstrip('/')}" if path else _base_url()
    tags = {
        "description": description,
        "og:title": title,
        "og:description": description,
        "og:type": "website",
        "og:url": canonical,
        "og:site_name": "CaribScope",
        "og:locale": "fr_FR",
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
    }
    if image:
        tags["og:image"] = image
        tags["twitter:image"] = image

    payload = json.dumps({"tags": tags, "canonical": canonical, "title": title})

    embed_html(
        """
        <script>
        (function () {
          var doc;
          try { doc = window.parent.document; } catch (e) { return; }
          var data = %(payload)s;

          doc.documentElement.setAttribute('lang', 'fr');

          function upsert(key, value) {
            var attr = key.indexOf('og:') === 0 ? 'property' : 'name';
            var el = doc.head.querySelector('meta[' + attr + '="' + key + '"]');
            if (!el) {
              el = doc.createElement('meta');
              el.setAttribute(attr, key);
              doc.head.appendChild(el);
            }
            el.setAttribute('content', value);
          }
          Object.keys(data.tags).forEach(function (k) { upsert(k, data.tags[k]); });

          var link = doc.head.querySelector('link[rel="canonical"]');
          if (!link) {
            link = doc.createElement('link');
            link.setAttribute('rel', 'canonical');
            doc.head.appendChild(link);
          }
          link.setAttribute('href', data.canonical);

          // Les <meta> écrites par st.markdown atterrissent dans le <body> :
          // elles n'y servent à rien et polluent le DOM.
          doc.body.querySelectorAll('meta[name], meta[property]').forEach(function (m) {
            m.remove();
          });
        })();
        </script>
        """ % {"payload": payload},
        height=0,
    )
