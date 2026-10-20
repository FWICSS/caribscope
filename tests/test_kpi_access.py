"""Accès à la page KPIs internes : fermée par défaut, ouverte sans code
seulement en développement déclaré (CARIBSCOPE_ENV=development)."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
PAGE = str(next(ROOT.glob("pages/16_*KPIs_Internes.py")))


def _run(monkeypatch, tmp_path, **env):
    # Hors du dépôt : le .streamlit/secrets.toml local ne doit pas fournir de PIN.
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(ROOT))
    for name in ("CARIBSCOPE_ENV", "CARIBSCOPE_KPI_PIN"):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    at = AppTest.from_file(PAGE, default_timeout=30)
    at.run()
    return at


def _locked_without_pin(at):
    return any("Page indisponible" in e.value for e in at.error)


def test_sans_aucune_variable_la_page_est_fermee(monkeypatch, tmp_path):
    at = _run(monkeypatch, tmp_path)
    assert _locked_without_pin(at)
    assert not at.text_input


def test_production_sans_pin_la_page_est_fermee(monkeypatch, tmp_path):
    at = _run(monkeypatch, tmp_path, CARIBSCOPE_ENV="production")
    assert _locked_without_pin(at)


@pytest.mark.parametrize("env", ["development", "dev", "local"])
def test_developpement_declare_ouvre_sans_code(monkeypatch, tmp_path, env):
    at = _run(monkeypatch, tmp_path, CARIBSCOPE_ENV=env)
    assert not _locked_without_pin(at)
    assert not at.text_input


def test_avec_pin_le_code_est_demande(monkeypatch, tmp_path):
    at = _run(monkeypatch, tmp_path, CARIBSCOPE_ENV="production", CARIBSCOPE_KPI_PIN="un-code-de-test")
    assert not _locked_without_pin(at)
    assert at.text_input and at.text_input[0].label == "Code d'accès"
