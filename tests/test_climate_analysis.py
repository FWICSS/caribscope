import pandas as pd
import pytest
from src.analysis.climate import (
    get_major_hurricane_pct_by_decade,
    get_season_length_by_year,
    get_sst_hurricane_correlation,
)


class TestGetMajorHurricanePctByDecade:
    def test_returns_dataframe(self, enriched_df):
        result = get_major_hurricane_pct_by_decade(enriched_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self, enriched_df):
        result = get_major_hurricane_pct_by_decade(enriched_df)
        for col in ["decade", "total", "major_count", "major_pct"]:
            assert col in result.columns

    def test_pct_between_0_and_100(self, enriched_df):
        result = get_major_hurricane_pct_by_decade(enriched_df)
        assert (result["major_pct"] >= 0).all()
        assert (result["major_pct"] <= 100).all()

    def test_sample_df_has_major_hurricanes(self, enriched_df):
        # IRMA (165kt) and DEAN (140kt) are cat 4-5 → major
        result = get_major_hurricane_pct_by_decade(enriched_df)
        assert result["major_count"].sum() > 0


class TestGetSeasonLengthByYear:
    def test_returns_dataframe(self, enriched_df):
        result = get_season_length_by_year(enriched_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self, enriched_df):
        result = get_season_length_by_year(enriched_df)
        for col in ["year", "first_month", "last_month", "season_length"]:
            assert col in result.columns

    def test_season_length_positive(self, enriched_df):
        result = get_season_length_by_year(enriched_df)
        assert (result["season_length"] >= 0).all()


class TestGetSstHurricaneCorrelation:
    def test_returns_dataframe(self, enriched_df, sample_sst_df):
        result = get_sst_hurricane_correlation(enriched_df, sample_sst_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self, enriched_df, sample_sst_df):
        result = get_sst_hurricane_correlation(enriched_df, sample_sst_df)
        for col in ["year", "sst_peak", "max_wind"]:
            assert col in result.columns
