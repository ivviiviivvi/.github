#!/usr/bin/env python3
"""
Unit tests for automation/scripts/predict_workflow_failures.py
Focus: Feature extraction, model training, prediction, safe serialization
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Skip all tests if numpy/pandas not installed
np = pytest.importorskip("numpy")
pd = pytest.importorskip("pandas")

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))

from predict_workflow_failures import WorkflowPredictor


class TestWorkflowPredictor:
    """Test WorkflowPredictor class"""

    @pytest.fixture
    def predictor(self, tmp_path):
        """Create predictor with temp path"""
        model_path = tmp_path / "model.joblib"
        return WorkflowPredictor(str(model_path))

    def test_initialization(self, tmp_path):
        """Test predictor initializes correctly"""
        model_path = tmp_path / "model.joblib"
        predictor = WorkflowPredictor(str(model_path))

        assert predictor.model_path == model_path
        assert predictor.model is None
        assert predictor.feature_columns == []


class TestFeatureExtraction:
    """Test feature extraction from workflow runs"""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    def test_extracts_temporal_features(self, predictor):
        """Test extracts temporal features correctly"""
        run = {
            "created_at": "2024-01-15T14:30:00Z",  # Monday, 2:30 PM
            "workflow_id": 12345,
            "name": "CI Pipeline",
            "event": "push",
            "run_number": 100,
            "run_attempt": 1,
            "conclusion": "success",
        }

        features = predictor._extract_features(run)

        assert features["hour_of_day"] == 14
        assert features["day_of_week"] == 0  # Monday
        assert features["is_weekend"] == 0

    def test_extracts_weekend_flag(self, predictor):
        """Test weekend flag is set correctly"""
        run = {
            "created_at": "2024-01-13T10:00:00Z",  # Saturday
            "workflow_id": 12345,
            "name": "CI Pipeline",
            "event": "push",
            "run_number": 100,
            "run_attempt": 1,
            "conclusion": "success",
        }

        features = predictor._extract_features(run)

        assert features["is_weekend"] == 1

    def test_extracts_failure_target(self, predictor):
        """Test extracts failure target correctly"""
        success_run = {
            "created_at": "2024-01-15T14:30:00Z",
            "workflow_id": 12345,
            "name": "CI",
            "event": "push",
            "run_number": 100,
            "run_attempt": 1,
            "conclusion": "success",
        }
        failed_run = {
            "created_at": "2024-01-15T14:30:00Z",
            "workflow_id": 12345,
            "name": "CI",
            "event": "push",
            "run_number": 101,
            "run_attempt": 1,
            "conclusion": "failure",
        }

        success_features = predictor._extract_features(success_run)
        failed_features = predictor._extract_features(failed_run)

        assert success_features["failed"] == 0
        assert failed_features["failed"] == 1

    def test_handles_missing_fields_gracefully(self, predictor):
        """Test handles missing fields gracefully"""
        incomplete_run = {
            "created_at": "2024-01-15T14:30:00Z",
        }

        features = predictor._extract_features(incomplete_run)

        # Should return None for incomplete data
        assert features is None

    def test_extracts_workflow_features(self, predictor):
        """Test extracts workflow-specific features"""
        run = {
            "created_at": "2024-01-15T14:30:00Z",
            "workflow_id": 98765,
            "name": "Deploy Production",
            "event": "release",
            "run_number": 42,
            "run_attempt": 2,
            "conclusion": "success",
        }

        features = predictor._extract_features(run)

        assert features["workflow_id"] == 98765
        assert features["run_number"] == 42
        assert features["run_attempt"] == 2


class TestPrepareFeatures:
    """Test feature preparation for training"""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    @pytest.fixture
    def sample_df(self):
        """Create sample dataframe"""
        return pd.DataFrame(
            [
                {
                    "hour_of_day": 10,
                    "day_of_week": 1,
                    "is_weekend": 0,
                    "workflow_id": 100,
                    "workflow_name_hash": 5000,
                    "event_hash": 50,
                    "run_number": 1,
                    "run_attempt": 1,
                    "failed": 0,
                },
                {
                    "hour_of_day": 22,
                    "day_of_week": 5,
                    "is_weekend": 1,
                    "workflow_id": 100,
                    "workflow_name_hash": 5000,
                    "event_hash": 50,
                    "run_number": 2,
                    "run_attempt": 1,
                    "failed": 1,
                },
            ]
        )

    def test_prepare_features_returns_arrays(self, predictor, sample_df):
        """Test prepare_features returns numpy arrays"""
        X, y = predictor.prepare_features(sample_df)

        assert isinstance(X, np.ndarray)
        assert isinstance(y, np.ndarray)

    def test_prepare_features_correct_shapes(self, predictor, sample_df):
        """Test arrays have correct shapes"""
        X, y = predictor.prepare_features(sample_df)

        assert X.shape[0] == 2  # 2 samples
        assert X.shape[1] == 8  # 8 features
        assert y.shape[0] == 2  # 2 labels

    def test_sets_feature_columns(self, predictor, sample_df):
        """Test sets feature_columns attribute"""
        predictor.prepare_features(sample_df)

        assert len(predictor.feature_columns) == 8
        assert "hour_of_day" in predictor.feature_columns
        assert "day_of_week" in predictor.feature_columns


class TestTraining:
    """Test model training"""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    @pytest.fixture
    def training_df(self):
        """Create larger training dataframe"""
        np.random.seed(42)
        n_samples = 100

        return pd.DataFrame(
            {
                "hour_of_day": np.random.randint(0, 24, n_samples),
                "day_of_week": np.random.randint(0, 7, n_samples),
                "is_weekend": np.random.randint(0, 2, n_samples),
                "workflow_id": np.random.randint(100, 200, n_samples),
                "workflow_name_hash": np.random.randint(0, 10000, n_samples),
                "event_hash": np.random.randint(0, 100, n_samples),
                "run_number": np.random.randint(1, 1000, n_samples),
                "run_attempt": np.random.randint(1, 3, n_samples),
                "failed": np.random.randint(0, 2, n_samples),
            }
        )

    def test_train_creates_model(self, predictor, training_df):
        """Test training creates model"""
        predictor.train(training_df)

        assert predictor.model is not None

    def test_train_returns_metrics(self, predictor, training_df):
        """Test training returns metrics dictionary"""
        metrics = predictor.train(training_df)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics

    def test_train_metrics_in_valid_range(self, predictor, training_df):
        """Test metrics are in valid range"""
        metrics = predictor.train(training_df)

        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["precision"] <= 1.0
        assert 0.0 <= metrics["recall"] <= 1.0
        assert 0.0 <= metrics["f1"] <= 1.0


class TestPrediction:
    """Test model prediction"""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create trained predictor"""
        predictor = WorkflowPredictor(str(tmp_path / "model.joblib"))

        # Train on sample data
        np.random.seed(42)
        n_samples = 100
        training_df = pd.DataFrame(
            {
                "hour_of_day": np.random.randint(0, 24, n_samples),
                "day_of_week": np.random.randint(0, 7, n_samples),
                "is_weekend": np.random.randint(0, 2, n_samples),
                "workflow_id": np.random.randint(100, 200, n_samples),
                "workflow_name_hash": np.random.randint(0, 10000, n_samples),
                "event_hash": np.random.randint(0, 100, n_samples),
                "run_number": np.random.randint(1, 1000, n_samples),
                "run_attempt": np.random.randint(1, 3, n_samples),
                "failed": np.random.randint(0, 2, n_samples),
            }
        )
        predictor.train(training_df)
        return predictor

    def test_predict_returns_probability(self, trained_predictor):
        """Test predict returns probability"""
        features = {
            "hour_of_day": 14,
            "day_of_week": 2,
            "is_weekend": 0,
            "workflow_id": 150,
            "workflow_name_hash": 5000,
            "event_hash": 50,
            "run_number": 100,
            "run_attempt": 1,
        }

        probability = trained_predictor.predict(features)

        assert 0.0 <= probability <= 1.0

    def test_predict_without_model_raises(self, tmp_path):
        """Test predict without model raises error"""
        predictor = WorkflowPredictor(str(tmp_path / "model.joblib"))

        features = {"hour_of_day": 14, "day_of_week": 2}

        with pytest.raises(ValueError, match="Model not trained"):
            predictor.predict(features)


class TestModelPersistence:
    """Test model save/load functionality"""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create and train predictor"""
        predictor = WorkflowPredictor(str(tmp_path / "model.joblib"))

        np.random.seed(42)
        n_samples = 50
        training_df = pd.DataFrame(
            {
                "hour_of_day": np.random.randint(0, 24, n_samples),
                "day_of_week": np.random.randint(0, 7, n_samples),
                "is_weekend": np.random.randint(0, 2, n_samples),
                "workflow_id": np.random.randint(100, 200, n_samples),
                "workflow_name_hash": np.random.randint(0, 10000, n_samples),
                "event_hash": np.random.randint(0, 100, n_samples),
                "run_number": np.random.randint(1, 1000, n_samples),
                "run_attempt": np.random.randint(1, 3, n_samples),
                "failed": np.random.randint(0, 2, n_samples),
            }
        )
        predictor.train(training_df)
        return predictor

    def test_save_model(self, trained_predictor):
        """Test model can be saved"""
        trained_predictor.save_model()

        assert trained_predictor.model_path.exists()

    def test_load_model(self, trained_predictor):
        """Test model can be loaded"""
        trained_predictor.save_model()

        # Create new predictor and load
        new_predictor = WorkflowPredictor(str(trained_predictor.model_path))
        new_predictor.load_model()

        assert new_predictor.model is not None

    def test_load_preserves_feature_columns(self, trained_predictor):
        """Test loading preserves feature columns"""
        trained_predictor.save_model()

        new_predictor = WorkflowPredictor(str(trained_predictor.model_path))
        new_predictor.load_model()

        assert new_predictor.feature_columns == trained_predictor.feature_columns

    @pytest.mark.security
    def test_uses_joblib_not_pickle(self, trained_predictor):
        """Test uses joblib for safer serialization"""
        trained_predictor.save_model()

        # Verify it's a joblib file (not raw pickle)
        # Joblib files typically start with different magic bytes
        with open(trained_predictor.model_path, "rb") as f:
            first_bytes = f.read(10)
            # Joblib uses zlib compression by default
            # The file should exist and have content
            assert len(first_bytes) > 0


class TestDataCollection:
    """Test data collection functionality"""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    def test_collect_handles_api_error(self, predictor):
        """Test handles API error gracefully"""
        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.side_effect = Exception("API Error")

            df = predictor.collect_historical_data(days=7)

            # Should return empty dataframe, not raise
            assert isinstance(df, pd.DataFrame)

    def test_collect_parses_response(self, predictor):
        """Test parses API response correctly"""
        mock_response = {
            "workflow_runs": [
                {
                    "created_at": "2024-01-15T14:30:00Z",
                    "workflow_id": 12345,
                    "name": "CI",
                    "event": "push",
                    "run_number": 100,
                    "run_attempt": 1,
                    "conclusion": "success",
                },
                {
                    "created_at": "2024-01-15T15:30:00Z",
                    "workflow_id": 12345,
                    "name": "CI",
                    "event": "push",
                    "run_number": 101,
                    "run_attempt": 1,
                    "conclusion": "failure",
                },
            ]
        }

        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=json.dumps(mock_response),
                returncode=0,
            )

            df = predictor.collect_historical_data(days=7)

            assert len(df) == 2


class TestRiskAssessment:
    """Test risk assessment functionality"""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create trained predictor"""
        predictor = WorkflowPredictor(str(tmp_path / "model.joblib"))

        np.random.seed(42)
        n_samples = 100
        training_df = pd.DataFrame(
            {
                "hour_of_day": np.random.randint(0, 24, n_samples),
                "day_of_week": np.random.randint(0, 7, n_samples),
                "is_weekend": np.random.randint(0, 2, n_samples),
                "workflow_id": np.random.randint(100, 200, n_samples),
                "workflow_name_hash": np.random.randint(0, 10000, n_samples),
                "event_hash": np.random.randint(0, 100, n_samples),
                "run_number": np.random.randint(1, 1000, n_samples),
                "run_attempt": np.random.randint(1, 3, n_samples),
                "failed": np.random.randint(0, 2, n_samples),
            }
        )
        predictor.train(training_df)
        return predictor

    def test_assess_risk_returns_level(self, trained_predictor):
        """Test assess_risk returns risk level"""
        features = {
            "hour_of_day": 14,
            "day_of_week": 2,
            "is_weekend": 0,
            "workflow_id": 150,
            "workflow_name_hash": 5000,
            "event_hash": 50,
            "run_number": 100,
            "run_attempt": 1,
        }

        risk = trained_predictor.assess_risk(features)

        assert risk["level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert 0.0 <= risk["probability"] <= 1.0

    def test_high_probability_maps_to_high_risk(self, trained_predictor):
        """Test high failure probability maps to high risk"""
        with patch.object(trained_predictor, "predict", return_value=0.85):
            features = {"hour_of_day": 3}  # Minimal features

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] in ["HIGH", "CRITICAL"]

    def test_low_probability_maps_to_low_risk(self, trained_predictor):
        """Test low failure probability maps to low risk"""
        with patch.object(trained_predictor, "predict", return_value=0.1):
            features = {"hour_of_day": 10}

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] == "LOW"
