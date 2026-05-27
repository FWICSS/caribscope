import pandas as pd
import pytest
from src.analysis.seismes import get_top_earthquakes, get_earthquakes_by_decade, get_magnitude_distribution


class TestGetTopEarthquakes:
    def test_returns_dataframe(self, sample_earthquakes_df):
        result = get_top_earthquakes(sample_earthquakes_df)
        assert isinstance(result, pd.DataFrame)

    def test_sorted_by_magnitude_descending(self, sample_earthquakes_df):
        result = get_top_earthquakes(sample_earthquakes_df, n=6)
        magnitudes = result["magnitude"].tolist()
        assert magnitudes == sorted(magnitudes, reverse=True)

    def test_respects_n_parameter(self, sample_earthquakes_df):
        result = get_top_earthquakes(sample_earthquakes_df, n=3)
        assert len(result) == 3

    def test_n_larger_than_df_returns_all(self, sample_earthquakes_df):
        result = get_top_earthquakes(sample_earthquakes_df, n=100)
        assert len(result) == len(sample_earthquakes_df)


class TestGetEarthquakesByDecade:
    def test_returns_dataframe(self, sample_earthquakes_df):
        result = get_earthquakes_by_decade(sample_earthquakes_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_decade_and_count_columns(self, sample_earthquakes_df):
        result = get_earthquakes_by_decade(sample_earthquakes_df)
        assert "decade" in result.columns
        assert "count" in result.columns

    def test_total_count_matches_input(self, sample_earthquakes_df):
        result = get_earthquakes_by_decade(sample_earthquakes_df)
        assert result["count"].sum() == len(sample_earthquakes_df)

    def test_decades_are_multiples_of_ten(self, sample_earthquakes_df):
        result = get_earthquakes_by_decade(sample_earthquakes_df)
        assert all(d % 10 == 0 for d in result["decade"])


class TestGetMagnitudeDistribution:
    def test_returns_dataframe(self, sample_earthquakes_df):
        result = get_magnitude_distribution(sample_earthquakes_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_range_and_count_columns(self, sample_earthquakes_df):
        result = get_magnitude_distribution(sample_earthquakes_df)
        assert "range" in result.columns
        assert "count" in result.columns

    def test_total_count_matches_input(self, sample_earthquakes_df):
        result = get_magnitude_distribution(sample_earthquakes_df)
        assert result["count"].sum() == len(sample_earthquakes_df)
