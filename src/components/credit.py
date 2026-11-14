"""Crédit « Réalisé par TAFRAP Studio » affiché en pied de page.

Le lien porte des paramètres UTM communs à tous les sites du studio, pour que la
mesure d'audience de tafrap.fr sache, le jour où elle les lit, quelles visites
viennent de CaribScope. Ces paramètres ne servent à rien tant que tafrap.fr ne
les lit pas : ils sont posés d'avance, sans effet de bord sur ce site.
"""
import html

import streamlit as st

CREDIT_URL = (
    "https://tafrap.fr/"
    "?utm_source=caribscope.fwicss.fr&utm_medium=credit&utm_campaign=realisations"
)
CREDIT_LABEL = "Réalisé par TAFRAP Studio"


def credit_html() -> str:
    """Retourne le HTML du crédit, lien ouvert dans un nouvel onglet.

    `st.markdown` en Markdown pur ne permet pas `target="_blank"` : le lien
    remplacerait l'application dans l'onglet courant. D'où le HTML, échappé
    pour rester sûr si l'adresse ou le libellé changent un jour.
    """
    url = html.escape(CREDIT_URL, quote=True)
    label = html.escape(CREDIT_LABEL)
    return (
        '<p style="font-size:0.8rem;opacity:0.7;margin:0;">'
        f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
        "</p>"
    )


def render_credit() -> None:
    """Affiche le crédit à l'endroit courant de la page Streamlit."""
    st.markdown(credit_html(), unsafe_allow_html=True)
