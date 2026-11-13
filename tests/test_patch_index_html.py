"""Le correctif des balises de partage s'applique sur la vraie coquille Streamlit."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "deploy"))
import patch_index_html as p  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "streamlit-index.html"


@pytest.fixture
def shell() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_title_replaced(shell):
    out = p.patch(shell)
    assert "<title>Streamlit</title>" not in out
    assert "<title>CaribScope — Observatoire des risques naturels caribéens</title>" in out


def test_lang_is_french(shell):
    out = p.patch(shell)
    assert 'lang="fr"' in out
    assert 'lang="en"' not in out


def test_meta_in_head_with_absolute_image(shell):
    out = p.patch(shell)
    head = out.split("</head>")[0]
    assert '<meta property="og:title"' in head
    assert '<meta property="og:image" content="https://caribscope.fwicss.fr/app/static/og-default.jpg"' in head
    assert '<meta name="twitter:card" content="summary_large_image"' in head
    assert '<link rel="canonical" href="https://caribscope.fwicss.fr/"' in head


def test_idempotent(shell):
    once = p.patch(shell)
    twice = p.patch(once)
    assert twice == once
    assert twice.count(p.MARK_START) == 1


def test_without_head_fails_loudly():
    with pytest.raises(ValueError):
        p.patch("<html><body></body></html>")
