"""Écrit les balises de partage dans la coquille HTML servie par Streamlit.

Pourquoi : Streamlit sert un `index.html` figé (`<title>Streamlit</title>`, aucune
balise meta) et ne rend la page qu'en JavaScript. Les robots de LinkedIn, X,
WhatsApp et Facebook n'exécutent pas ce JavaScript : l'aperçu d'un lien vers
caribscope.fwicss.fr n'affichait donc que « Streamlit », sans titre ni image.
`src/components/head.py` corrige le DOM côté navigateur, ce qui ne suffit pas
pour ces robots. Ce script modifie le fichier lui-même, une fois, à la
construction de l'image Docker (voir `Dockerfile`).

Effets de bord : réécrit `index.html` dans le paquet `streamlit` installé.
Idempotent : un second passage remplace le bloc précédent au lieu de le doubler.
Erreurs : `FileNotFoundError` si le paquet Streamlit n'est pas installé.
"""
from __future__ import annotations

import html
import importlib.util
import re
import sys
from pathlib import Path

BASE_URL = "https://caribscope.fwicss.fr"
TITLE = "CaribScope — Observatoire des risques naturels caribéens"
DESCRIPTION = (
    "170 ans de données sur les ouragans, séismes et tendances climatiques "
    "de la Caraïbe. Trajectoires depuis 1851, catalogue sismique USGS, "
    "prédiction d'intensité par apprentissage automatique. Open source."
)
# Servie par Streamlit grâce à `enableStaticServing` (fichier `static/og-default.jpg`).
IMAGE_PATH = "/app/static/og-default.jpg"
MARK_START = "<!-- caribscope:meta -->"
MARK_END = "<!-- /caribscope:meta -->"


def meta_block(base_url: str = BASE_URL, title: str = TITLE,
               description: str = DESCRIPTION, image_path: str = IMAGE_PATH) -> str:
    """Bloc de balises prêt à insérer dans `<head>`, encadré de marqueurs."""
    base = base_url.rstrip("/")
    image = f"{base}{image_path}"
    t, d = html.escape(title, quote=True), html.escape(description, quote=True)
    lines = [
        MARK_START,
        f'<meta name="description" content="{d}" />',
        f'<link rel="canonical" href="{base}/" />',
        f'<meta property="og:type" content="website" />',
        f'<meta property="og:site_name" content="CaribScope" />',
        f'<meta property="og:locale" content="fr_FR" />',
        f'<meta property="og:title" content="{t}" />',
        f'<meta property="og:description" content="{d}" />',
        f'<meta property="og:url" content="{base}/" />',
        f'<meta property="og:image" content="{image}" />',
        '<meta property="og:image:width" content="1200" />',
        '<meta property="og:image:height" content="630" />',
        f'<meta property="og:image:alt" content="{html.escape("Carte des trajectoires d’ouragans de la Caraïbe depuis 1851", quote=True)}" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{t}" />',
        f'<meta name="twitter:description" content="{d}" />',
        f'<meta name="twitter:image" content="{image}" />',
        MARK_END,
    ]
    return "\n".join(lines)


def patch(source: str, **kwargs: str) -> str:
    """Retourne le HTML corrigé : titre, `lang="fr"`, bloc meta avant `</head>`.

    Le bloc déjà présent (entre les marqueurs) est retiré avant insertion, pour
    qu'une reconstruction de l'image ne l'empile pas.
    """
    title = kwargs.get("title", TITLE)
    out = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>",
                 source, count=1, flags=re.S)
    out = re.sub(r'<html(\s[^>]*?)?\slang="[^"]*"', r'<html\1 lang="fr"', out, count=1)
    if 'lang="fr"' not in out:
        out = out.replace("<html", '<html lang="fr"', 1)
    out = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", "",
                 out, flags=re.S)
    if "</head>" not in out:
        raise ValueError("index.html sans </head> : structure inattendue")
    return out.replace("</head>", meta_block(**kwargs) + "\n</head>", 1)


def streamlit_index_path() -> Path:
    """Chemin de l'`index.html` du paquet Streamlit installé."""
    spec = importlib.util.find_spec("streamlit")
    if spec is None or not spec.submodule_search_locations:
        raise FileNotFoundError("paquet streamlit introuvable")
    return Path(next(iter(spec.submodule_search_locations))) / "static" / "index.html"


def main() -> int:
    path = streamlit_index_path()
    path.write_text(patch(path.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"balises de partage écrites dans {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
