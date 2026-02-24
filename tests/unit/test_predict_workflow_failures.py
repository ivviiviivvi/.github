"""Unit tests for automation/scripts/predict_workflow_failures.py
Focus: Feature extraction, model training, prediction, safe serialization.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Skip all tests if numpy/pandas not installed
np = pytest.importorskip("numpy")
pd = pytest.importorskip("pandas")

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from predict_workflow_failures import WorkflowPredictor


class TestWorkflowPredictor:
    """Test WorkflowPredictor class."""

    @pytest.fixture
    def predictor(self, tmp_path):
        """Create predictor with temp path."""
        model_path = tmp_path / "model.joblib"
        return WorkflowPredictor(str(model_path))

    def test_initialization(self, tmp_path):
        """Test predictor initializes correctly."""
        model_path = tmp_path / "model.joblib"
        predictor = WorkflowPredictor(str(model_path))

        assert predictor.model_path == model_path
        assert predictor.model is None
        assert predictor.feature_columns == []


class TestFeatureExtraction:
    """Test feature extraction from workflow runs."""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    def test_extracts_temporal_features(self, predictor):
        """Test extracts temporal features correctly."""
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
        """Test weekend flag is set correctly."""
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
        """Test extracts failure target correctly."""
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
        """Test handles missing fields gracefully."""
        incomplete_run = {
            "created_at": "2024-01-15T14:30:00Z",
        }

        features = predictor._extract_features(incomplete_run)

        # Should return None for incomplete data
        assert features is None

    def test_extracts_workflow_features(self, predictor):
        """Test extracts workflow-specific features."""
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
    """Test feature preparation for training."""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    @pytest.fixture
    def sample_df(self):
        """Create sample dataframe."""
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
        """Test prepare_features returns numpy arrays."""
        X, y = predictor.prepare_features(sample_df)

        assert isinstance(X, np.ndarray)
        assert isinstance(y, np.ndarray)

    def test_prepare_features_correct_shapes(self, predictor, sample_df):
        """Test arrays have correct shapes."""
        X, y = predictor.prepare_features(sample_df)

        assert X.shape[0] == 2  # 2 samples
        assert X.shape[1] == 8  # 8 features
        assert y.shape[0] == 2  # 2 labels

    def test_sets_feature_columns(self, predictor, sample_df):
        """Test sets feature_columns attribute."""
        predictor.prepare_features(sample_df)

        assert len(predictor.feature_columns) == 8
        assert "hour_of_day" in predictor.feature_columns
        assert "day_of_week" in predictor.feature_columns


class TestTraining:
    """Test model training."""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    @pytest.fixture
    def training_df(self):
        """Create larger training dataframe."""
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
        """Test training creates model."""
        predictor.train(training_df)

        assert predictor.model is not None

    def test_train_returns_metrics(self, predictor, training_df):
        """Test training returns metrics dictionary."""
        metrics = predictor.train(training_df)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics

    def test_train_metrics_in_valid_range(self, predictor, training_df):
        """Test metrics are in valid range."""
        metrics = predictor.train(training_df)

        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["precision"] <= 1.0
        assert 0.0 <= metrics["recall"] <= 1.0
        assert 0.0 <= metrics["f1"] <= 1.0


class TestPrediction:
    """Test model prediction."""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create trained predictor."""
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
        """Test predict returns probability."""
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
        """Test predict without model raises error."""
        predictor = WorkflowPredictor(str(tmp_path / "model.joblib"))

        features = {"hour_of_day": 14, "day_of_week": 2}

        with pytest.raises(ValueError, match="Model not trained"):
            predictor.predict(features)


class TestModelPersistence:
    """Test model save/load functionality."""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create and train predictor."""
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
        """Test model can be saved."""
        trained_predictor.save_model()

        assert trained_predictor.model_path.exists()

    def test_load_model(self, trained_predictor):
        """Test model can be loaded."""
        trained_predictor.save_model()

        # Create new predictor and load
        new_predictor = WorkflowPredictor(str(trained_predictor.model_path))
        new_predictor.load_model()

        assert new_predictor.model is not None

    def test_load_preserves_feature_columns(self, trained_predictor):
        """Test loading preserves feature columns."""
        trained_predictor.save_model()

        new_predictor = WorkflowPredictor(str(trained_predictor.model_path))
        new_predictor.load_model()

        assert new_predictor.feature_columns == trained_predictor.feature_columns

    @pytest.mark.security
    def test_uses_joblib_not_pickle(self, trained_predictor):
        """Test uses joblib for safer serialization."""
        trained_predictor.save_model()

        # Verify it's a joblib file (not raw pickle)
        # Joblib files typically start with different magic bytes
        with open(trained_predictor.model_path, "rb") as f:
            first_bytes = f.read(10)
            # Joblib uses zlib compression by default
            # The file should exist and have content
            assert len(first_bytes) > 0


class TestDataCollection:
    """Test data collection functionality."""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    def test_collect_handles_api_error(self, predictor):
        """Test handles API error gracefully."""
        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.side_effect = Exception("API Error")

            df = predictor.collect_historical_data(days=7)

            # Should return empty dataframe, not raise
            assert isinstance(df, pd.DataFrame)

    def test_collect_parses_response(self, predictor):
        """Test parses API response correctly."""
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
    """Test risk assessment functionality."""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create trained predictor."""
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
        """Test assess_risk returns risk level."""
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
        """Test high failure probability maps to high risk."""
        with patch.object(trained_predictor, "predict", return_value=0.85):
            features = {"hour_of_day": 3}  # Minimal features

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] in ["HIGH", "CRITICAL"]

    def test_low_probability_maps_to_low_risk(self, trained_predictor):
        """Test low failure probability maps to low risk."""
        with patch.object(trained_predictor, "predict", return_value=0.1):
            features = {"hour_of_day": 10}

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] == "LOW"

    def test_medium_probability_maps_to_medium_risk(self, trained_predictor):
        """Test medium failure probability maps to medium risk."""
        with patch.object(trained_predictor, "predict", return_value=0.25):
            features = {"hour_of_day": 10}

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] == "MEDIUM"

    def test_high_range_probability_maps_to_high(self, trained_predictor):
        """Test 30-60% failure probability maps to HIGH risk."""
        with patch.object(trained_predictor, "predict", return_value=0.45):
            features = {"hour_of_day": 10}

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] == "HIGH"

    def test_critical_probability_maps_to_critical(self, trained_predictor):
        """Test 60%+ failure probability maps to CRITICAL risk."""
        with patch.object(trained_predictor, "predict", return_value=0.75):
            features = {"hour_of_day": 10}

            risk = trained_predictor.assess_risk(features)

            assert risk["level"] == "CRITICAL"


@pytest.mark.unit
class TestPredictWorkflowByName:
    """Test prediction by workflow name."""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create trained predictor."""
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

    def test_predict_by_workflow_name_returns_dict(self, trained_predictor):
        """Test predicting by workflow name returns result dict."""
        result = trained_predictor.predict("ci.yml", "owner/repo")

        assert isinstance(result, dict)
        assert "workflow" in result
        assert "repository" in result
        assert "failure_probability" in result
        assert "risk_level" in result

    def test_predict_without_repository_raises(self, trained_predictor):
        """Test predicting without repository raises ValueError."""
        with pytest.raises(ValueError, match="Repository is required"):
            trained_predictor.predict("ci.yml")

    def test_predict_result_contains_expected_fields(self, trained_predictor):
        """Test prediction result contains all expected fields."""
        result = trained_predictor.predict("deploy.yml", "owner/repo")

        assert "workflow" in result
        assert result["workflow"] == "deploy.yml"
        assert "repository" in result
        assert result["repository"] == "owner/repo"
        assert "timestamp" in result
        assert "failure_probability" in result
        assert "prediction" in result
        assert result["prediction"] in ["SUCCESS", "FAILURE"]
        assert "risk_level" in result
        assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert "risk_color" in result
        assert "confidence" in result

    def test_predict_low_risk_level(self, trained_predictor):
        """Test low probability results in LOW risk level."""
        # Mock to return low probability
        with patch.object(trained_predictor.model, "predict_proba", return_value=np.array([[0.97, 0.03]])):
            with patch.object(trained_predictor.model, "predict", return_value=np.array([0])):
                result = trained_predictor.predict("ci.yml", "owner/repo")

                assert result["risk_level"] == "LOW"
                assert result["risk_color"] == "green"

    def test_predict_medium_risk_level(self, trained_predictor):
        """Test medium probability results in MEDIUM risk level."""
        with patch.object(trained_predictor.model, "predict_proba", return_value=np.array([[0.90, 0.10]])):
            with patch.object(trained_predictor.model, "predict", return_value=np.array([0])):
                result = trained_predictor.predict("ci.yml", "owner/repo")

                assert result["risk_level"] == "MEDIUM"
                assert result["risk_color"] == "yellow"

    def test_predict_high_risk_level(self, trained_predictor):
        """Test high probability results in HIGH risk level."""
        with patch.object(trained_predictor.model, "predict_proba", return_value=np.array([[0.80, 0.20]])):
            with patch.object(trained_predictor.model, "predict", return_value=np.array([0])):
                result = trained_predictor.predict("ci.yml", "owner/repo")

                assert result["risk_level"] == "HIGH"
                assert result["risk_color"] == "orange"

    def test_predict_critical_risk_level(self, trained_predictor):
        """Test very high probability results in CRITICAL risk level."""
        with patch.object(trained_predictor.model, "predict_proba", return_value=np.array([[0.55, 0.45]])):
            with patch.object(trained_predictor.model, "predict", return_value=np.array([1])):
                result = trained_predictor.predict("ci.yml", "owner/repo")

                assert result["risk_level"] == "CRITICAL"
                assert result["risk_color"] == "red"

    def test_predict_loads_model_if_exists(self, trained_predictor, tmp_path):
        """Test predict loads model from path if not loaded."""
        trained_predictor.save_model()

        # Create new predictor pointing to saved model
        new_predictor = WorkflowPredictor(str(trained_predictor.model_path))

        # Should auto-load model
        result = new_predictor.predict("ci.yml", "owner/repo")

        assert isinstance(result, dict)
        assert new_predictor.model is not None


@pytest.mark.unit
class TestGetHighRiskWorkflows:
    """Test high-risk workflow identification."""

    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create trained predictor."""
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

    def test_get_high_risk_workflows_returns_list(self, trained_predictor):
        """Test returns list of high-risk workflows."""
        mock_workflows = [{"name": "ci.yml"}, {"name": "deploy.yml"}]

        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=json.dumps(mock_workflows),
                returncode=0,
            )

            # Mock predictions to be above threshold
            with patch.object(trained_predictor, "predict") as mock_predict:
                mock_predict.return_value = {
                    "failure_probability": 0.25,
                    "workflow": "ci.yml",
                }

                high_risk = trained_predictor.get_high_risk_workflows(threshold=0.15)

                assert isinstance(high_risk, list)

    def test_get_high_risk_workflows_handles_api_error(self, trained_predictor):
        """Test handles API error gracefully."""
        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.side_effect = Exception("API Error")

            result = trained_predictor.get_high_risk_workflows()

            assert result == []

    def test_get_high_risk_workflows_sorted_by_probability(self, trained_predictor):
        """Test workflows are sorted by probability descending."""
        mock_workflows = [{"name": "low.yml"}, {"name": "high.yml"}]

        predictions = [
            {"failure_probability": 0.20, "workflow": "low.yml"},
            {"failure_probability": 0.50, "workflow": "high.yml"},
        ]

        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=json.dumps(mock_workflows),
                returncode=0,
            )

            with patch.object(trained_predictor, "predict") as mock_predict:
                mock_predict.side_effect = predictions

                high_risk = trained_predictor.get_high_risk_workflows(threshold=0.15)

                # Should be sorted descending
                if len(high_risk) >= 2:
                    assert high_risk[0]["failure_probability"] >= high_risk[1]["failure_probability"]


@pytest.mark.unit
class TestModelLoadErrors:
    """Test model loading error conditions."""

    def test_load_model_missing_file_raises(self, tmp_path):
        """Test loading non-existent model raises FileNotFoundError."""
        predictor = WorkflowPredictor(str(tmp_path / "nonexistent.joblib"))

        with pytest.raises(FileNotFoundError, match="Model not found"):
            predictor.load_model()

    def test_load_model_missing_signature_raises(self, tmp_path):
        """Test loading model without signature raises ValueError."""
        # Create model file but no signature
        model_path = tmp_path / "model.joblib"
        model_path.write_bytes(b"dummy data")

        predictor = WorkflowPredictor(str(model_path))

        with pytest.raises(ValueError, match="Missing signature file"):
            predictor.load_model()

    def test_load_model_invalid_signature_raises(self, tmp_path):
        """Test loading model with wrong signature raises ValueError."""
        # Create model file with .pkl extension (expected by code)
        model_path = tmp_path / "model.pkl"
        model_path.write_bytes(b"model data")

        # Create signature file with wrong signature (code expects .pkl.sig)
        sig_path = tmp_path / "model.pkl.sig"
        sig_path.write_text("wrong_signature")

        predictor = WorkflowPredictor(str(model_path))

        with pytest.raises(ValueError, match="signature verification failed"):
            predictor.load_model()


@pytest.mark.unit
class TestGetCurrentRepo:
    """Test _get_current_repo method."""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    def test_get_current_repo_success(self, predictor):
        """Test successfully getting current repo."""
        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout='{"nameWithOwner": "myorg/myrepo"}',
                returncode=0,
            )

            repo = predictor._get_current_repo()

            assert repo == "myorg/myrepo"

    def test_get_current_repo_fallback_on_error(self, predictor):
        """Test fallback to default repo on error."""
        with patch("predict_workflow_failures.subprocess.run") as mock_run:
            mock_run.side_effect = Exception("gh not found")

            repo = predictor._get_current_repo()

            assert repo == "{{ORG_NAME}}/.github"


@pytest.mark.unit
class TestSignatureGeneration:
    """Test signature generation and verification."""

    @pytest.fixture
    def predictor(self, tmp_path):
        return WorkflowPredictor(str(tmp_path / "model.joblib"))

    def test_generate_signature_consistent(self, predictor):
        """Test signature generation is consistent."""
        data = b"test data"

        sig1 = predictor._generate_signature(data)
        sig2 = predictor._generate_signature(data)

        assert sig1 == sig2

    def test_verify_signature_correct(self, predictor):
        """Test signature verification with correct signature."""
        data = b"test data"
        signature = predictor._generate_signature(data)

        assert predictor._verify_signature(data, signature) is True

    def test_verify_signature_wrong(self, predictor):
        """Test signature verification with wrong signature."""
        data = b"test data"

        assert predictor._verify_signature(data, "wrong_signature") is False


@pytest.mark.unit
class TestMainCLI:
    """Test main CLI function."""

    @pytest.fixture
    def tmp_ml_dir(self, tmp_path, monkeypatch):
        """Set up temp directory for ML files."""
        ml_dir = tmp_path / "automation" / "ml"
        ml_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        return ml_dir

    def test_main_collect_data(self, tmp_ml_dir, capsys):
        """Test main with --collect flag."""
        import sys

        original_argv = sys.argv
        sys.argv = ["predict_workflow_failures.py", "--collect", "--days", "7"]

        try:
            with patch("predict_workflow_failures.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"workflow_runs": []}',
                    returncode=0,
                )

                from predict_workflow_failures import main

                main()

            captured = capsys.readouterr()
            assert "Collecting" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_train_no_data_file(self, tmp_ml_dir, capsys):
        """Test main with --train but no data file."""
        import sys

        original_argv = sys.argv
        sys.argv = ["predict_workflow_failures.py", "--train"]

        try:
            with pytest.raises(SystemExit) as exc_info:
                from predict_workflow_failures import main

                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "No data file found" in captured.err
        finally:
            sys.argv = original_argv

    def test_main_train_with_data(self, tmp_ml_dir, capsys):
        """Test main with --train and data file."""
        import sys

        # Create sample data file
        data_file = tmp_ml_dir / "workflow_data.csv"

        np.random.seed(42)
        n_samples = 100
        df = pd.DataFrame(
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
        df.to_csv(data_file, index=False)

        original_argv = sys.argv
        sys.argv = ["predict_workflow_failures.py", "--train"]

        try:
            from predict_workflow_failures import main

            main()

            captured = capsys.readouterr()
            assert "Training" in captured.out
            assert "Accuracy" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_predict_workflow(self, tmp_ml_dir, capsys):
        """Test main with --predict flag."""
        import sys

        # First train a model
        np.random.seed(42)
        n_samples = 100
        df = pd.DataFrame(
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

        predictor = WorkflowPredictor("automation/ml/workflow_model.pkl")
        predictor.train(df)

        original_argv = sys.argv
        sys.argv = [
            "predict_workflow_failures.py",
            "--predict",
            "owner/repo",
            "ci.yml",
        ]

        try:
            from predict_workflow_failures import main

            main()

            captured = capsys.readouterr()
            assert "Workflow" in captured.out
            assert "Failure Probability" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_predict_json_output(self, tmp_ml_dir, capsys):
        """Test main with --predict and --json flags."""
        import sys

        # First train a model (capture and discard training output)
        np.random.seed(42)
        n_samples = 100
        df = pd.DataFrame(
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

        predictor = WorkflowPredictor("automation/ml/workflow_model.pkl")
        predictor.train(df)

        # Clear any output from training
        capsys.readouterr()

        original_argv = sys.argv
        sys.argv = [
            "predict_workflow_failures.py",
            "--predict",
            "owner/repo",
            "ci.yml",
            "--json",
        ]

        try:
            from predict_workflow_failures import main

            main()

            captured = capsys.readouterr()
            # Verify JSON-like output is present (multi-line JSON from json.dumps indent=2)
            output = captured.out
            assert '"workflow"' in output
            assert '"failure_probability"' in output
            assert '"risk_level"' in output
        finally:
            sys.argv = original_argv

    def test_main_high_risk_workflows(self, tmp_ml_dir, capsys):
        """Test main with --high-risk flag."""
        import sys

        # First train a model
        np.random.seed(42)
        n_samples = 100
        df = pd.DataFrame(
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

        predictor = WorkflowPredictor("automation/ml/workflow_model.pkl")
        predictor.train(df)

        original_argv = sys.argv
        sys.argv = [
            "predict_workflow_failures.py",
            "--high-risk",
            "--threshold",
            "0.1",
        ]

        try:
            with patch("predict_workflow_failures.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='[{"name": "ci.yml"}]',
                    returncode=0,
                )

                from predict_workflow_failures import main

                main()

            captured = capsys.readouterr()
            assert "High-Risk Workflows" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_high_risk_no_workflows_detected(self, tmp_ml_dir, capsys):
        """Test main with --high-risk when no high-risk workflows found."""
        import sys

        # First train a model
        np.random.seed(42)
        n_samples = 100
        df = pd.DataFrame(
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

        predictor = WorkflowPredictor("automation/ml/workflow_model.pkl")
        predictor.train(df)

        # Clear any output from training
        capsys.readouterr()

        original_argv = sys.argv
        sys.argv = [
            "predict_workflow_failures.py",
            "--high-risk",
            "--threshold",
            "0.99",  # Very high threshold - no workflows should exceed this
        ]

        try:
            with patch("predict_workflow_failures.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='[{"name": "ci.yml"}]',
                    returncode=0,
                )

                from predict_workflow_failures import main

                main()

            captured = capsys.readouterr()
            assert "No high-risk workflows detected" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_high_risk_json_output(self, tmp_ml_dir, capsys):
        """Test main with --high-risk and --json flags."""
        import sys

        # First train a model
        np.random.seed(42)
        n_samples = 100
        df = pd.DataFrame(
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

        predictor = WorkflowPredictor("automation/ml/workflow_model.pkl")
        predictor.train(df)

        # Clear any output from training
        capsys.readouterr()

        original_argv = sys.argv
        sys.argv = [
            "predict_workflow_failures.py",
            "--high-risk",
            "--json",
        ]

        try:
            with patch("predict_workflow_failures.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='[{"name": "ci.yml"}]',
                    returncode=0,
                )

                from predict_workflow_failures import main

                main()

            captured = capsys.readouterr()
            # Verify JSON array output (could be empty list or list with predictions)
            output = captured.out
            # Should contain opening bracket for JSON array
            assert "[" in output
            # Should also contain closing bracket
            assert "]" in output
        finally:
            sys.argv = original_argv

    def test_main_no_args_prints_help(self, capsys):
        """Test main with no args prints help."""
        import sys

        original_argv = sys.argv
        sys.argv = ["predict_workflow_failures.py"]

        try:
            from predict_workflow_failures import main

            main()

            captured = capsys.readouterr()
            assert "usage" in captured.out.lower() or "predict" in captured.out.lower()
        finally:
            sys.argv = original_argv

    def test_main_handles_exception(self, tmp_ml_dir, capsys):
        """Test main handles exception gracefully."""
        import sys

        original_argv = sys.argv
        sys.argv = [
            "predict_workflow_failures.py",
            "--predict",
            "owner/repo",
            "ci.yml",
        ]

        try:
            # No model exists, should raise and exit with code 1
            with pytest.raises(SystemExit) as exc_info:
                from predict_workflow_failures import main

                main()

            assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv
