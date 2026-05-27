import numpy
import pandas as pd
import pytest
import requests
from unittest.mock import patch, MagicMock
from src.data.seismes_loader import fetch_earthquakes, _parse_geojson


MOCK_GEOJSON = {
    "features": [
        {
            "properties": {
                "mag": 7.2,
                "place": "15km SSE of Port-au-Prince, Haiti",
                "time": 1628000000000,
            },
            "geometry": {"coordinates": [-72.5, 18.4, 10.0]},
        },
        {
            "properties": {
                "mag": 5.1,
                "place": "near Martinique",
                "time": 1440000000000,
            },
            "geometry": {"coordinates": [-61.0, 14.8, 15.5]},
        },
    ]
}


class TestParseGeojson:
    def test_returns_dataframe(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self):
        result = _parse_geojson(MOCK_GEOJSON)
        for col in ["magnitude", "latitude", "longitude", "depth_km", "place", "time", "year", "month"]:
            assert col in result.columns, f"Missing column: {col}"

    def test_row_count_matches_features(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert len(result) == 2

    def test_magnitude_values_correct(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert result["magnitude"].iloc[0] == pytest.approx(7.2)

    def test_latitude_extracted_from_geometry(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert result["latitude"].iloc[0] == pytest.approx(18.4)

    def test_longitude_extracted_from_geometry(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert result["longitude"].iloc[0] == pytest.approx(-72.5)

    def test_time_is_datetime(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert pd.api.types.is_datetime64_any_dtype(result["time"])

    def test_year_column_derived_from_time(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert result["year"].iloc[0] == 2021

    def test_month_column_derived_from_time(self):
        result = _parse_geojson(MOCK_GEOJSON)
        assert isinstance(result["month"].iloc[0], (int, numpy.integer))


class TestFetchEarthquakes:
    def test_returns_dataframe_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_GEOJSON
        mock_response.raise_for_status.return_value = None

        with patch("src.data.seismes_loader.requests.get", return_value=mock_response):
            result = fetch_earthquakes(use_cache=False)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    def test_raises_on_http_error(self):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404")

        with patch("src.data.seismes_loader.requests.get", return_value=mock_response):
            with pytest.raises(requests.HTTPError):
                fetch_earthquakes(use_cache=False)
