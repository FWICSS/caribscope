"""Single place where HTML fragments get embedded in the page.

Streamlit deprecated streamlit.components.v1.html in favour of st.iframe and
announced its removal. requirements.txt allows streamlit>=1.28, where st.iframe
does not exist, so both paths have to be supported.

Order matters. components.html is tried FIRST because the two APIs are not
interchangeable for our main use case: most embeds here are invisible script
tags rendered with height=0, and st.iframe rejects that outright
("Invalid height value: 0. Height must be either a positive integer (pixels),
'stretch', or 'content'"). Using st.iframe as the primary path therefore breaks
every page that injects analytics. The fallback clamps to 1px so the app keeps
working the day components.html is actually removed.
"""
import streamlit as st

try:  # streamlit < 1.61 and, for now, every current version
    import streamlit.components.v1 as _components
except ImportError:  # pragma: no cover - only once components.v1 is dropped
    _components = None


def embed_html(content: str, height: int = 0) -> None:
    """Render an HTML fragment in a sandboxed iframe."""
    if _components is not None:
        _components.html(content, height=height)
    elif hasattr(st, "iframe"):
        st.iframe(content, height=max(1, height))
