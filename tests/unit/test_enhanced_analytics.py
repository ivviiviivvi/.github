#!/usr/bin/env python3
"""Comprehensive unit tests for automation/scripts/enhanced_analytics.py

Focus: ML model training, prediction, feature extraction, and model persistence.
"""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from enhanced_analytics import EnhancedAnalyticsEngine, main
from models import AnalyticsConfig


@pytest.fixture
def mock_client():
    """Mock GitHub API client."""
    return MagicMock()


@pytest.fixture
def config():
    """Default analytics configuration."""
    return AnalyticsConfig()


@pytest.fixture
def engine(mock_client, config, tmp_path):
    """Create EnhancedAnalyticsEngine with mocks."""
    from sklearn.preprocessing import StandardScaler

    with patch.object(EnhancedAnalyticsEngine, "__init__", lambda self, c, g: None):
        eng = EnhancedAnalyticsEngine.__new__(EnhancedAnalyticsEngine)
        eng.config = config
        eng.github = mock_client
        eng.models = {}
        eng.scaler = StandardScaler()
        eng.feature_names = []
        eng.models_dir = tmp_path / "models"
        eng.models_dir.mkdir()
        eng._secret = b"test-secret"
    return eng


@pytest.fixture
def sample_pr():
    """Sample PR data."""
    return {
        "number": 123,
        "additions": 100,
        "deletions": 50,
        "changed_files": 5,
        "created_at": "2024-01-15T10:00:00Z",
        "merged_at": "2024-01-16T14:00:00Z",
        "user": {"login": "testuser"},
        "base": {"ref": "main"},
        "head": {"ref": "feature-branch"},
        "labels": [{"name": "enhancement"}],
    }


@pytest.fixture
def sample_commits():
    """Sample commits data."""
    return [
        {"sha": "abc123", "author": {"login": "testuser"}},
        {"sha": "def456", "author": {"login": "testuser"}},
    ]


@pytest.fixture
def sample_files():
    """Sample files data."""
    return [
        {"filename": "src/main.py", "additions": 50, "deletions": 20},
        {"filename": "tests/test_main.py", "additions": 30, "deletions": 10},
        {"filename": "README.md", "additions": 20, "deletions": 20},
    ]


@pytest.fixture
def sample_reviews():
    """Sample reviews data."""
    return [
        {"user": {"login": "reviewer1"}, "state": "APPROVED"},
        {"user": {"login": "reviewer2"}, "state": "CHANGES_REQUESTED"},
    ]


@pytest.fixture
def sample_comments():
    """Sample comments data."""
    return [
        {"body": "Looks good!"},
        {"body": "Please fix the formatting."},
    ]


@pytest.mark.unit
class TestEnhancedAnalyticsEngineInit:
    """Test EnhancedAnalyticsEngine initialization."""

    def test_initializes_with_config_and_client(self, tmp_path):
        """Test engine initializes with config and client."""
        mock_client = MagicMock()
        config = AnalyticsConfig()

        with patch.object(Path, "mkdir"):
            engine = EnhancedAnalyticsEngine(config, mock_client)

        assert engine.config == config
        assert engine.github == mock_client
        assert engine.models == {}
        assert engine.feature_names == []


@pytest.mark.unit
class TestSignature:
    """Test HMAC signature generation and verification."""

    def test_generates_consistent_signature(self, engine):
        """Test signature is deterministic."""
        data = b"test data"
        sig1 = engine._generate_signature(data)
        sig2 = engine._generate_signature(data)

        assert sig1 == sig2

    def test_different_data_different_signature(self, engine):
        """Test different data produces different signatures."""
        sig1 = engine._generate_signature(b"data1")
        sig2 = engine._generate_signature(b"data2")

        assert sig1 != sig2

    def test_verify_valid_signature(self, engine):
        """Test valid signature verification."""
        data = b"test data"
        sig = engine._generate_signature(data)

        assert engine._verify_signature(data, sig) is True

    def test_verify_invalid_signature(self, engine):
        """Test invalid signature verification."""
        data = b"test data"

        assert engine._verify_signature(data, "invalid-signature") is False


@pytest.mark.unit
class TestExtractFeatures:
    """Test feature extraction from PRs."""

    def test_extracts_basic_features(
        self, engine, sample_pr, sample_commits, sample_files, sample_reviews, sample_comments
    ):
        """Test basic feature extraction."""
        engine.github.get.side_effect = [
            sample_pr,
            sample_commits,
            sample_files,
            sample_reviews,
            sample_comments,
            [],  # author commits
            [],  # author PRs
            [],  # open PRs
            [],  # closed PRs
            {"workflow_runs": []},  # workflow runs
        ]

        features = engine.extract_features("org", "repo", 123)

        assert features["lines_added"] == 100
        assert features["lines_deleted"] == 50
        assert features["lines_changed"] == 150
        assert features["files_changed"] == 5
        assert features["commits_count"] == 2

    def test_raises_for_missing_pr(self, engine):
        """Test raises error for missing PR."""
        engine.github.get.return_value = None

        with pytest.raises(ValueError, match="not found"):
            engine.extract_features("org", "repo", 999)

    def test_handles_no_reviews(self, engine, sample_pr, sample_commits, sample_files, sample_comments):
        """Test handles PR with no reviews."""
        engine.github.get.side_effect = [
            sample_pr,
            sample_commits,
            sample_files,
            [],  # no reviews
            sample_comments,
            [],  # author commits
            [],  # author PRs
            [],  # open PRs
            [],  # closed PRs
            {"workflow_runs": []},
        ]

        features = engine.extract_features("org", "repo", 123)

        assert features["reviewers_count"] == 0
        assert features["reviews_count"] == 0
        assert features["approval_ratio"] == 0

    def test_handles_no_comments(self, engine, sample_pr, sample_commits, sample_files, sample_reviews):
        """Test handles PR with no comments."""
        engine.github.get.side_effect = [
            sample_pr,
            sample_commits,
            sample_files,
            sample_reviews,
            [],  # no comments
            [],  # author commits
            [],  # author PRs
            [],  # open PRs
            [],  # closed PRs
            {"workflow_runs": []},
        ]

        features = engine.extract_features("org", "repo", 123)

        assert features["comments_count"] == 0
        assert features["avg_comment_length"] == 0

    def test_extracts_file_type_features(
        self, engine, sample_pr, sample_commits, sample_files, sample_reviews, sample_comments
    ):
        """Test file type analysis features."""
        engine.github.get.side_effect = [
            sample_pr,
            sample_commits,
            sample_files,
            sample_reviews,
            sample_comments,
            [],  # author commits
            [],  # author PRs
            [],  # open PRs
            [],  # closed PRs
            {"workflow_runs": []},
        ]

        features = engine.extract_features("org", "repo", 123)

        assert features["test_files_changed"] == 1
        assert features["doc_files_changed"] == 1


@pytest.mark.unit
class TestGetAuthorStats:
    """Test author statistics retrieval."""

    def test_gets_author_stats(self, engine):
        """Test retrieves author statistics."""
        engine.github.get.side_effect = [
            [{"sha": "abc"}, {"sha": "def"}],  # commits
            [
                {"number": 1, "merged_at": "2024-01-15T12:00:00Z", "created_at": "2024-01-15T10:00:00Z"},
                {"number": 2, "merged_at": None, "created_at": "2024-01-14T10:00:00Z"},
            ],  # PRs
        ]

        stats = engine._get_author_stats("org", "repo", "testuser")

        assert stats["total_commits"] == 2
        assert stats["total_prs"] == 2
        assert stats["success_rate"] == 0.5

    def test_handles_no_author_data(self, engine):
        """Test handles new author with no data."""
        engine.github.get.side_effect = [
            [],  # no commits
            [],  # no PRs
        ]

        stats = engine._get_author_stats("org", "repo", "newuser")

        assert stats["total_commits"] == 0
        assert stats["total_prs"] == 0
        assert stats["success_rate"] == 0.5  # Default for new contributors


@pytest.mark.unit
class TestGetRepositoryStats:
    """Test repository statistics retrieval."""

    def test_gets_repository_stats(self, engine):
        """Test retrieves repository statistics."""
        engine.github.get.side_effect = [
            [{"number": 1}, {"number": 2}],  # open PRs
            [{"number": 3, "merged_at": "2024-01-15T12:00:00Z"}, {"number": 4, "merged_at": None}],  # closed PRs
            {"workflow_runs": [{"conclusion": "success"}, {"conclusion": "failure"}]},  # runs
        ]

        stats = engine._get_repository_stats("org", "repo")

        assert stats["open_prs"] == 2
        assert stats["recent_merge_rate"] == 0.5
        assert stats["ci_success_rate"] == 0.5

    def test_handles_no_prs(self, engine):
        """Test handles repository with no PRs."""
        engine.github.get.side_effect = [
            [],  # no open PRs
            [],  # no closed PRs
            {"workflow_runs": []},  # no runs
        ]

        stats = engine._get_repository_stats("org", "repo")

        assert stats["open_prs"] == 0
        assert stats["recent_merge_rate"] == 0.5  # Default
        assert stats["ci_success_rate"] == 0.8  # Default


@pytest.mark.unit
class TestTrainModels:
    """Test model training."""

    def test_raises_for_insufficient_data(self, engine):
        """Test raises error for insufficient training data."""
        engine.github.get.return_value = [{"number": i} for i in range(5)]  # Only 5 PRs

        with pytest.raises(ValueError, match="Insufficient training data"):
            engine.train_models("org", "repo", 90)

    def test_trains_all_models(self, engine, sample_pr):
        """Test trains all model types."""
        # Create enough PRs for training
        prs = [
            {**sample_pr, "number": i, "merged_at": "2024-01-15T12:00:00Z" if i % 2 == 0 else None} for i in range(30)
        ]

        # Provide enough data for all PRs
        engine.github.get.return_value = prs

        # Create fake feature data for training - vary features for different PRs
        feature_count = [0]

        def make_features(*args, **kwargs):
            feature_count[0] += 1
            return {
                "f1": float(feature_count[0] % 10),
                "f2": float(feature_count[0] % 5),
                "f3": float(feature_count[0] % 3),
            }

        with patch.object(engine, "_save_models"):
            with patch.object(engine, "extract_features", side_effect=make_features):
                results = engine.train_models("org", "repo", 90)

        assert "random_forest" in results
        assert "gradient_boosting" in results
        assert "neural_network" in results
        assert all("accuracy" in r for r in results.values())


@pytest.mark.unit
class TestPredict:
    """Test prediction functionality."""

    def test_makes_prediction(self, engine):
        """Test makes prediction for a PR."""
        # Set up mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([1])
        mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])
        engine.models["random_forest"] = mock_model

        # Fit scaler with sample data
        engine.scaler.fit([[1.0, 2.0]])

        with patch.object(engine, "extract_features", return_value={"f1": 1.0, "f2": 2.0}):
            prediction = engine.predict("org", "repo", 123, "random_forest")

        assert prediction.pr_number == 123
        assert prediction.prediction == "merge"
        assert prediction.confidence == 0.8

    def test_loads_model_if_not_in_memory(self, engine):
        """Test loads model if not in memory."""
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([0])
        mock_model.predict_proba.return_value = np.array([[0.7, 0.3]])

        def mock_load():
            engine.models["random_forest"] = mock_model

        # Fit scaler with sample data
        engine.scaler.fit([[1.0]])

        with patch.object(engine, "_load_models", side_effect=mock_load):
            with patch.object(engine, "extract_features", return_value={"f1": 1.0}):
                prediction = engine.predict("org", "repo", 123, "random_forest")

        assert prediction.prediction == "close"

    def test_raises_for_unknown_model(self, engine):
        """Test raises error for unknown model."""
        with patch.object(engine, "_load_models"):
            with pytest.raises(ValueError, match="not found"):
                engine.predict("org", "repo", 123, "unknown_model")


@pytest.mark.unit
class TestGetFeatureImportance:
    """Test feature importance extraction."""

    def test_gets_feature_importance(self, engine):
        """Test gets feature importance from model."""
        mock_model = MagicMock()
        mock_model.feature_importances_ = np.array([0.3, 0.5, 0.2])
        engine.models["random_forest"] = mock_model
        engine.feature_names = ["feature_a", "feature_b", "feature_c"]

        importance = engine.get_feature_importance("random_forest")

        assert importance.model_name == "random_forest"
        assert "feature_b" in importance.top_features
        assert importance.features["feature_b"] == 0.5

    def test_handles_model_without_feature_importances(self, engine):
        """Test handles model without feature_importances_ attribute."""
        mock_model = MagicMock(spec=[])  # No feature_importances_
        del mock_model.feature_importances_
        engine.models["neural_network"] = mock_model
        engine.feature_names = ["f1", "f2"]

        importance = engine.get_feature_importance("neural_network")

        # Should use uniform importance
        assert len(importance.features) == 2


@pytest.mark.unit
class TestModelPersistence:
    """Test model saving and loading."""

    def test_saves_models_with_signature(self, engine, tmp_path):
        """Test saves models with HMAC signature."""
        from sklearn.ensemble import RandomForestClassifier

        # Create a real model for testing
        rf = RandomForestClassifier(n_estimators=2, random_state=42)
        rf.fit([[1, 2], [3, 4]], [0, 1])
        engine.models = {"random_forest": rf}
        engine.feature_names = ["f1", "f2"]
        engine.models_dir = tmp_path / "models"
        engine.models_dir.mkdir(parents=True, exist_ok=True)

        engine._save_models()

        # Check that model files were created
        model_files = list(engine.models_dir.glob("random_forest_*.joblib"))
        assert len(model_files) == 1

        # Check that signature file was created
        sig_files = list(engine.models_dir.glob("random_forest_*.sig"))
        assert len(sig_files) == 1

    def test_loads_models_with_signature_verification(self, engine, tmp_path):
        """Test loads models with signature verification."""
        # Create mock model file
        model_file = tmp_path / "models" / "random_forest_20240115.joblib"
        model_file.parent.mkdir(parents=True, exist_ok=True)
        model_file.write_bytes(b"mock model data")

        # Create signature file
        sig_file = model_file.with_suffix(".sig")
        sig = engine._generate_signature(b"mock model data")
        sig_file.write_text(sig)

        engine.models_dir = tmp_path / "models"

        with patch("enhanced_analytics.joblib.load", return_value=MagicMock()):
            engine._load_models()

        assert "random_forest" in engine.models

    def test_rejects_tampered_model(self, engine, tmp_path):
        """Test rejects model with invalid signature."""
        # Create mock model file
        model_file = tmp_path / "models" / "random_forest_20240115.joblib"
        model_file.parent.mkdir(parents=True, exist_ok=True)
        model_file.write_bytes(b"mock model data")

        # Create invalid signature
        sig_file = model_file.with_suffix(".sig")
        sig_file.write_text("invalid-signature")

        engine.models_dir = tmp_path / "models"
        engine._load_models()

        # Model should not be loaded
        assert "random_forest" not in engine.models


@pytest.mark.unit
class TestMainFunction:
    """Test main() function."""

    def test_main_train(self, capsys):
        """Test main with --train flag."""
        with patch("sys.argv", ["enhanced_analytics.py", "--owner", "org", "--repo", "repo", "--train"]):
            with patch("enhanced_analytics.load_config", return_value=AnalyticsConfig()):
                with patch("enhanced_analytics.GitHubAPIClient"):
                    with patch.object(
                        EnhancedAnalyticsEngine,
                        "train_models",
                        return_value={"random_forest": {"accuracy": 0.85, "precision": 0.8, "recall": 0.9, "f1": 0.85}},
                    ):
                        main()

        captured = capsys.readouterr()
        assert "Training Results" in captured.out
        assert "0.85" in captured.out

    def test_main_predict_without_pr_number(self, capsys):
        """Test main --predict without PR number exits with error."""
        with patch("sys.argv", ["enhanced_analytics.py", "--owner", "org", "--repo", "repo", "--predict"]):
            with patch("enhanced_analytics.load_config", return_value=AnalyticsConfig()):
                with patch("enhanced_analytics.GitHubAPIClient"):
                    with pytest.raises(SystemExit) as exc_info:
                        main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_main_predict_with_pr_number(self, capsys):
        """Test main --predict with PR number."""
        from models import AnalyticsPrediction

        mock_prediction = AnalyticsPrediction(
            pr_number=123,
            prediction="merge",
            confidence=0.85,
            model_name="random_forest",
            features={},
            timestamp=datetime.now(),
        )

        with patch(
            "sys.argv", ["enhanced_analytics.py", "--owner", "org", "--repo", "repo", "--predict", "--pr-number", "123"]
        ):
            with patch("enhanced_analytics.load_config", return_value=AnalyticsConfig()):
                with patch("enhanced_analytics.GitHubAPIClient"):
                    with patch.object(EnhancedAnalyticsEngine, "predict", return_value=mock_prediction):
                        main()

        captured = capsys.readouterr()
        assert "Prediction" in captured.out
        assert "merge" in captured.out

    def test_main_feature_importance(self, capsys):
        """Test main --feature-importance flag."""
        from models import FeatureImportance

        mock_importance = FeatureImportance(
            model_name="random_forest",
            features={"lines_changed": 0.3, "commits_count": 0.2},
            top_features=["lines_changed", "commits_count"],
        )

        with patch("sys.argv", ["enhanced_analytics.py", "--owner", "org", "--repo", "repo", "--feature-importance"]):
            with patch("enhanced_analytics.load_config", return_value=AnalyticsConfig()):
                with patch("enhanced_analytics.GitHubAPIClient"):
                    with patch.object(EnhancedAnalyticsEngine, "get_feature_importance", return_value=mock_importance):
                        main()

        captured = capsys.readouterr()
        assert "Feature Importance" in captured.out
        assert "lines_changed" in captured.out

    def test_main_no_args_shows_help(self, capsys):
        """Test main with no action shows help."""
        with patch("sys.argv", ["enhanced_analytics.py", "--owner", "org", "--repo", "repo"]):
            with patch("enhanced_analytics.load_config", return_value=AnalyticsConfig()):
                with patch("enhanced_analytics.GitHubAPIClient"):
                    with patch("argparse.ArgumentParser.print_help") as mock_help:
                        main()
                        mock_help.assert_called_once()
