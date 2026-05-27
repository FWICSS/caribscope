import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import patch
from src.data.sst_loader import load_sst, SST_FILE


class TestLoadSst:
    def setup_method(self):
        # Clear Streamlit cache between tests to avoid cross-test pollution
        try:
            load_sst.clear()
        except AttributeError:
            pass

    def test_returns_dataframe_when_file_exists(self, tmp_path, sample_sst_df):
        csv_path = tmp_path / "sst.csv"
        sample_sst_df.to_csv(csv_path, index=False)

        with patch("src.data.sst_loader.SST_FILE", csv_path):
            result = load_sst()

        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self, tmp_path, sample_sst_df):
        csv_path = tmp_path / "sst.csv"
        sample_sst_df.to_csv(csv_path, index=False)

        with patch("src.data.sst_loader.SST_FILE", csv_path):
            result = load_sst()

        for col in ["year", "month", "sst_c"]:
            assert col in result.columns

    def test_raises_file_not_found_when_missing(self, tmp_path):
        missing = tmp_path / "does_not_exist.csv"
        with patch("src.data.sst_loader.SST_FILE", missing):
            with pytest.raises(FileNotFoundError):
                load_sst()

    def test_sst_values_in_realistic_range(self, tmp_path, sample_sst_df):
        csv_path = tmp_path / "sst.csv"
        sample_sst_df.to_csv(csv_path, index=False)

        with patch("src.data.sst_loader.SST_FILE", csv_path):
            result = load_sst()

        assert result["sst_c"].min() > 20.0
        assert result["sst_c"].max() < 35.0
