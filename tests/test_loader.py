import pandas as pd
import pytest
from src.data.loader import _enrich, get_saffir_simpson_category, get_saffir_simpson_number


# ── Saffir-Simpson catégorie ──────────────────────────────────────────────────

class TestGetSaffirSimpsonCategory:
    def test_tropical_depression(self):
        assert get_saffir_simpson_category(30) == "Dépression tropicale"

    def test_tropical_storm(self):
        assert get_saffir_simpson_category(50) == "Tempête tropicale"

    def test_category_1(self):
        assert get_saffir_simpson_category(70) == "Catégorie 1"

    def test_category_2(self):
        assert get_saffir_simpson_category(90) == "Catégorie 2"

    def test_category_3(self):
        assert get_saffir_simpson_category(105) == "Catégorie 3"

    def test_category_4(self):
        assert get_saffir_simpson_category(125) == "Catégorie 4"

    def test_category_5(self):
        assert get_saffir_simpson_category(145) == "Catégorie 5"

    def test_negative_wind(self):
        assert get_saffir_simpson_category(-1) == "Inconnu"

    def test_nan_wind(self):
        assert get_saffir_simpson_category(float("nan")) == "Inconnu"

    def test_boundary_cat1_lower(self):
        assert get_saffir_simpson_category(64) == "Catégorie 1"

    def test_boundary_cat5_lower(self):
        assert get_saffir_simpson_category(137) == "Catégorie 5"


# ── Saffir-Simpson numéro ─────────────────────────────────────────────────────

class TestGetSaffirSimpsonNumber:
    def test_tropical_depression_is_zero(self):
        assert get_saffir_simpson_number(30) == 0

    def test_tropical_storm_is_zero(self):
        assert get_saffir_simpson_number(50) == 0

    def test_cat1(self):
        assert get_saffir_simpson_number(70) == 1

    def test_cat2(self):
        assert get_saffir_simpson_number(90) == 2

    def test_cat3(self):
        assert get_saffir_simpson_number(105) == 3

    def test_cat4(self):
        assert get_saffir_simpson_number(125) == 4

    def test_cat5(self):
        assert get_saffir_simpson_number(145) == 5

    def test_nan_is_zero(self):
        assert get_saffir_simpson_number(float("nan")) == 0


# ── _enrich ───────────────────────────────────────────────────────────────────

class TestEnrich:
    def test_adds_category_column(self, sample_df):
        result = _enrich(sample_df)
        assert "category" in result.columns

    def test_adds_category_num_column(self, sample_df):
        result = _enrich(sample_df)
        assert "category_num" in result.columns

    def test_adds_decade_column(self, sample_df):
        result = _enrich(sample_df)
        assert "decade" in result.columns

    def test_adds_hurricane_date_column(self, sample_df):
        result = _enrich(sample_df)
        assert "Hurricane_Date" in result.columns

    def test_hurricane_date_is_datetime(self, sample_df):
        result = _enrich(sample_df)
        assert pd.api.types.is_datetime64_any_dtype(result["Hurricane_Date"])

    def test_decade_2017_is_2010(self, sample_df):
        result = _enrich(sample_df)
        assert (result[result["year"] == 2017]["decade"] == 2010).all()

    def test_decade_2005_is_2000(self, sample_df):
        result = _enrich(sample_df)
        assert (result[result["year"] == 2005]["decade"] == 2000).all()

    def test_cat5_wind_gets_correct_category(self, sample_df):
        result = _enrich(sample_df)
        # IRMA row with wind=165 → Catégorie 5
        assert result[result["USA_WIND"] == 165]["category"].iloc[0] == "Catégorie 5"

    def test_does_not_modify_input(self, sample_df):
        original_len = len(sample_df)
        _enrich(sample_df)
        assert len(sample_df) == original_len
