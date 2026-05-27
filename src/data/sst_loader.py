from pathlib import Path
import pandas as pd

try:
    import streamlit as st
    _cache = st.cache_data
except ImportError:
    def _cache(fn=None, **kw):
        return fn if fn else lambda f: f

DATA_DIR = Path(__file__).parent.parent.parent / "data"
SST_FILE = DATA_DIR / "sst_caribbean_1980_2025.csv"


@_cache
def load_sst() -> pd.DataFrame:
    if not SST_FILE.exists():
        raise FileNotFoundError(
            f"SST data not found at {SST_FILE}. "
            "Run: python scripts/generate_sst.py"
        )
    return pd.read_csv(SST_FILE)
