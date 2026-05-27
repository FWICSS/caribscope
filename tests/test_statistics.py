import pytest
from src.analysis.statistics import (
    get_hurricanes_by_year,
    get_hurricanes_near_island,
    get_intensity_trend,
    get_max_category_per_hurricane,
    get_monthly_distribution,
)


# ── get_hurricanes_by_year ────────────────────────────────────────────────────

class TestGetHurricanesByYear:
    def test_returns_one_row_per_year(self, enriched_df):
        result = get_hurricanes_by_year(enriched_df)
        assert set(result["year"]) == {2005, 2007, 2017}

    def test_count_is_one_per_year(self, enriched_df):
        result = get_hurricanes_by_year(enriched_df)
        assert (result["count"] == 1).all()

    def test_sorted_ascending(self, enriched_df):
        result = get_hurricanes_by_year(enriched_df)
        assert list(result["year"]) == sorted(result["year"])


# ── get_max_category_per_hurricane ────────────────────────────────────────────

class TestGetMaxCategoryPerHurricane:
    def test_irma_max_wind(self, enriched_df):
        result = get_max_category_per_hurricane(enriched_df)
        irma = result[result["NAME"] == "IRMA"]
        assert irma["max_wind"].iloc[0] == 165

    def test_dean_min_pres(self, enriched_df):
        result = get_max_category_per_hurricane(enriched_df)
        dean = result[result["NAME"] == "DEAN"]
        assert dean["min_pres"].iloc[0] == 905

    def test_one_row_per_hurricane(self, enriched_df):
        result = get_max_category_per_hurricane(enriched_df)
        assert len(result) == 3


# ── get_hurricanes_near_island ────────────────────────────────────────────────

class TestGetHurricanesNearIsland:
    def test_includes_hurricane_in_range(self, enriched_df):
        # IRMA a un point à (17.0, -63.0) → dans un rayon de 3° autour de (17.0, -63.0)
        result = get_hurricanes_near_island(enriched_df, 17.0, -63.0, radius_deg=3.0)
        assert "IRMA" in result["NAME"].values

    def test_excludes_hurricane_out_of_range(self, enriched_df):
        # Aucun ouragan du sample_df n'est proche de (0, 0)
        result = get_hurricanes_near_island(enriched_df, 0.0, 0.0, radius_deg=3.0)
        assert result.empty

    def test_returns_all_track_points_of_matching_hurricane(self, enriched_df):
        # IRMA a 5 points, tous doivent être retournés même ceux hors rayon
        result = get_hurricanes_near_island(enriched_df, 17.0, -63.0, radius_deg=3.0)
        irma_points = result[result["NAME"] == "IRMA"]
        assert len(irma_points) == 5


# ── get_intensity_trend ───────────────────────────────────────────────────────

class TestGetIntensityTrend:
    def test_groups_by_decade(self, enriched_df):
        result = get_intensity_trend(enriched_df)
        # 2005 → décennie 2000, 2007 → 2000, 2017 → 2010
        assert set(result["decade"]) == {2000, 2010}

    def test_has_mean_max_wind_column(self, enriched_df):
        result = get_intensity_trend(enriched_df)
        assert "mean_max_wind" in result.columns

    def test_decade_2000_count_is_2(self, enriched_df):
        result = get_intensity_trend(enriched_df)
        row_2000 = result[result["decade"] == 2000]
        assert row_2000["count"].iloc[0] == 2  # DEAN + KATRINA


# ── get_monthly_distribution ──────────────────────────────────────────────────

class TestGetMonthlyDistribution:
    def test_september_count(self, enriched_df):
        result = get_monthly_distribution(enriched_df)
        sept = result[result["month"] == 9]["count"].iloc[0]
        assert sept == 1  # IRMA uniquement

    def test_august_count(self, enriched_df):
        result = get_monthly_distribution(enriched_df)
        aug = result[result["month"] == 8]["count"].iloc[0]
        assert aug == 2  # DEAN + KATRINA

    def test_only_active_months_returned(self, enriched_df):
        result = get_monthly_distribution(enriched_df)
        assert set(result["month"]).issubset({8, 9})
