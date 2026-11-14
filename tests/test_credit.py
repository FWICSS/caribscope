from src.components.credit import CREDIT_URL, credit_html


def test_credit_pointe_vers_tafrap_avec_utm():
    assert CREDIT_URL.startswith("https://tafrap.fr/?")
    assert "utm_source=caribscope.fwicss.fr" in CREDIT_URL
    assert "utm_medium=credit" in CREDIT_URL
    assert "utm_campaign=realisations" in CREDIT_URL


def test_credit_html_nouvel_onglet_et_libelle():
    rendu = credit_html()
    assert 'target="_blank"' in rendu
    assert 'rel="noopener"' in rendu
    assert "Réalisé par TAFRAP Studio" in rendu
    # Les & de l'URL sont échappés dans l'attribut href.
    assert "&amp;utm_medium=credit" in rendu
