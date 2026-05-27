import numpy as np
import pandas as pd
import pytest
from src.ml.train import build_features
from src.ml.predict import predict_category, get_feature_importance


class TestBuildFeatures:
    def test_returns_X_and_y(self, enriched_df):
        X, y = build_features(enriched_df)
        assert X is not None
        assert y is not None

    def test_X_has_5_columns(self, enriched_df):
        X, y = build_features(enriched_df)
        assert X.shape[1] == 5

    def test_y_is_integer_array(self, enriched_df):
        X, y = build_features(enriched_df)
        assert y.dtype in [np.int32, np.int64, int]

    def test_y_values_in_0_to_5_range(self, enriched_df):
        X, y = build_features(enriched_df)
        assert y.min() >= 0
        assert y.max() <= 5

    def test_rows_with_invalid_pressure_excluded(self, enriched_df):
        df_bad = enriched_df.copy()
        df_bad.loc[0, "USA_PRES"] = 0
        X_clean, _ = build_features(enriched_df)
        X_bad, _ = build_features(df_bad)
        assert len(X_bad) < len(X_clean)


class TestPredictCategory:
    @pytest.fixture
    def trained_model(self, enriched_df):
        from sklearn.ensemble import RandomForestClassifier
        X, y = build_features(enriched_df)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        return {"model": model, "features": ["USA_PRES", "LAT", "LON", "month", "decade"]}

    def test_returns_dict(self, trained_model):
        result = predict_category(trained_model, pressure=940, lat=18.0, lon=-65.0, month=9, decade=2020)
        assert isinstance(result, dict)

    def test_has_required_keys(self, trained_model):
        result = predict_category(trained_model, pressure=940, lat=18.0, lon=-65.0, month=9, decade=2020)
        for key in ["category_num", "category_label", "probabilities"]:
            assert key in result

    def test_category_num_in_valid_range(self, trained_model):
        result = predict_category(trained_model, pressure=940, lat=18.0, lon=-65.0, month=9, decade=2020)
        assert 0 <= result["category_num"] <= 5

    def test_probabilities_sum_to_one(self, trained_model):
        result = predict_category(trained_model, pressure=940, lat=18.0, lon=-65.0, month=9, decade=2020)
        assert abs(sum(result["probabilities"].values()) - 1.0) < 0.01

    def test_low_pressure_predicts_high_category(self, trained_model):
        result_strong = predict_category(trained_model, pressure=910, lat=18.0, lon=-65.0, month=9, decade=2020)
        result_weak = predict_category(trained_model, pressure=1000, lat=18.0, lon=-65.0, month=9, decade=2020)
        assert result_strong["category_num"] >= result_weak["category_num"]


class TestGetFeatureImportance:
    @pytest.fixture
    def model_dict(self, enriched_df):
        from sklearn.ensemble import RandomForestClassifier
        X, y = build_features(enriched_df)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        return {"model": model, "features": ["USA_PRES", "LAT", "LON", "month", "decade"]}

    def test_returns_dataframe(self, model_dict):
        result = get_feature_importance(model_dict)
        assert isinstance(result, pd.DataFrame)

    def test_has_feature_and_importance_columns(self, model_dict):
        result = get_feature_importance(model_dict)
        assert "feature" in result.columns
        assert "importance" in result.columns
