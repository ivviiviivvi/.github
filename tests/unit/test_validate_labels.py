#!/usr/bin/env python3
"""Unit tests for automation/scripts/validate_labels.py

Focus: Label validation and creation for GitHub repositories.
"""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock secret_manager before importing validate_labels
# Save original and restore after imports to avoid polluting other tests
_original_secret_manager = sys.modules.get("secret_manager")
sys.modules["secret_manager"] = MagicMock()

from validate_labels import LabelValidator

# Restore original secret_manager module after imports
if _original_secret_manager is not None:
    sys.modules["secret_manager"] = _original_secret_manager
else:
    sys.modules.pop("secret_manager", None)


@pytest.mark.unit
class TestLabelValidatorInit:
    """Test LabelValidator initialization."""

    @pytest.fixture
    def mock_config_file(self, tmp_path):
        """Create a mock configuration file."""
        config = {
            "repositories": ["owner/repo1", "owner/repo2"],
            "labels": [
                {"name": "bug", "color": "d73a4a", "description": "Bug report"},
                {"name": "feature", "color": "a2eeef", "description": "New feature"},
            ],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return config_path

    def test_loads_config_from_path(self, mock_config_file):
        """Test validator loads config from provided path."""
        with patch("validate_labels.ensure_github_token"):
            validator = LabelValidator(mock_config_file)

        assert len(validator.config["repositories"]) == 2
        assert len(validator.config["labels"]) == 2

    def test_fix_mode_disabled_by_default(self, mock_config_file):
        """Test fix mode is disabled by default."""
        with patch("validate_labels.ensure_github_token"):
            validator = LabelValidator(mock_config_file)

        assert validator.fix_mode is False

    def test_fix_mode_can_be_enabled(self, mock_config_file):
        """Test fix mode can be enabled."""
        with patch("validate_labels.ensure_github_token"):
            validator = LabelValidator(mock_config_file, fix_mode=True)

        assert validator.fix_mode is True


@pytest.mark.unit
class TestLabelConfigLoading:
    """Test configuration loading and parsing."""

    @pytest.fixture
    def validator_with_dict_labels(self, tmp_path):
        """Create validator with dict-format labels in config."""
        config = {
            "repositories": ["owner/repo"],
            "labels": {
                "bug": {"color": "d73a4a", "description": "Bug report"},
                "feature": {"color": "a2eeef", "description": "New feature"},
            },
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_converts_dict_labels_to_list(self, validator_with_dict_labels):
        """Test dict-format labels are converted to list format."""
        labels = validator_with_dict_labels.config["labels"]

        assert isinstance(labels, list)
        assert len(labels) == 2

        # Check structure
        for label in labels:
            assert "name" in label
            assert "color" in label
            assert "description" in label


@pytest.mark.unit
class TestColorNormalization:
    """Test color normalization functionality."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a basic validator."""
        config = {"repositories": [], "labels": []}
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_removes_hash_prefix(self, validator):
        """Test hash prefix is removed from colors."""
        result = validator._normalize_color("#d73a4a")
        assert result == "d73a4a"

    def test_handles_no_hash(self, validator):
        """Test colors without hash are unchanged."""
        result = validator._normalize_color("d73a4a")
        assert result == "d73a4a"

    def test_converts_to_lowercase(self, validator):
        """Test colors are converted to lowercase."""
        result = validator._normalize_color("D73A4A")
        assert result == "d73a4a"


@pytest.mark.unit
class TestLabelsMatch:
    """Test label matching logic."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a basic validator."""
        config = {"repositories": [], "labels": []}
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_matching_labels_return_true(self, validator):
        """Test identical labels return True."""
        existing = {"name": "bug", "color": "d73a4a"}
        required = {"name": "bug", "color": "d73a4a"}

        assert validator._labels_match(existing, required) is True

    def test_different_names_return_false(self, validator):
        """Test different names return False."""
        existing = {"name": "bug", "color": "d73a4a"}
        required = {"name": "feature", "color": "d73a4a"}

        assert validator._labels_match(existing, required) is False

    def test_different_colors_return_false(self, validator):
        """Test different colors return False."""
        existing = {"name": "bug", "color": "d73a4a"}
        required = {"name": "bug", "color": "a2eeef"}

        assert validator._labels_match(existing, required) is False

    def test_color_comparison_ignores_hash(self, validator):
        """Test color comparison ignores hash prefix."""
        existing = {"name": "bug", "color": "d73a4a"}
        required = {"name": "bug", "color": "#d73a4a"}

        assert validator._labels_match(existing, required) is True

    def test_color_comparison_case_insensitive(self, validator):
        """Test color comparison is case insensitive."""
        existing = {"name": "bug", "color": "D73A4A"}
        required = {"name": "bug", "color": "d73a4a"}

        assert validator._labels_match(existing, required) is True


@pytest.mark.unit
class TestGetRepoLabels:
    """Test fetching labels from repository."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a basic validator."""
        config = {"repositories": [], "labels": []}
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_returns_labels_on_success(self, validator):
        """Test returns parsed labels on successful API call."""
        mock_result = MagicMock()
        mock_result.stdout = json.dumps([{"name": "bug", "color": "d73a4a", "description": "Bug report"}])

        with patch("subprocess.run", return_value=mock_result):
            labels = validator._get_repo_labels("owner/repo")

        assert len(labels) == 1
        assert labels[0]["name"] == "bug"

    def test_returns_none_on_subprocess_error(self, validator, capsys):
        """Test returns None when subprocess fails."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "gh", stderr="API error")
            labels = validator._get_repo_labels("owner/repo")

        assert labels is None
        captured = capsys.readouterr()
        assert "Error fetching labels" in captured.out

    def test_returns_none_on_json_error(self, validator, capsys):
        """Test returns None when JSON parsing fails."""
        mock_result = MagicMock()
        mock_result.stdout = "invalid json"

        with patch("subprocess.run", return_value=mock_result):
            labels = validator._get_repo_labels("owner/repo")

        assert labels is None
        captured = capsys.readouterr()
        assert "Error parsing" in captured.out


@pytest.mark.unit
class TestCreateLabel:
    """Test label creation functionality."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a basic validator."""
        config = {"repositories": [], "labels": []}
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_returns_true_on_success(self, validator):
        """Test returns True when label is created successfully."""
        label = {"name": "bug", "color": "d73a4a", "description": "Bug report"}

        with patch("subprocess.run"):
            result = validator._create_label("owner/repo", label)

        assert result is True

    def test_returns_false_on_error(self, validator, capsys):
        """Test returns False when creation fails."""
        label = {"name": "bug", "color": "d73a4a", "description": "Bug report"}

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "gh", stderr="Permission denied")
            result = validator._create_label("owner/repo", label)

        assert result is False
        captured = capsys.readouterr()
        assert "Error creating label" in captured.out


@pytest.mark.unit
class TestValidateRepository:
    """Test repository validation logic."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator with labels config."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [
                {"name": "bug", "color": "d73a4a", "description": "Bug report"},
                {"name": "feature", "color": "a2eeef", "description": "New feature"},
            ],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_all_labels_present_returns_success(self, validator):
        """Test returns success when all labels are present."""
        existing_labels = [
            {"name": "bug", "color": "d73a4a", "description": "Bug report"},
            {"name": "feature", "color": "a2eeef", "description": "New feature"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            success, missing, mismatched = validator.validate_repository("owner/repo")

        assert success is True
        assert missing == []
        assert mismatched == []

    def test_missing_labels_returned(self, validator):
        """Test returns missing labels when not present."""
        existing_labels = [
            {"name": "bug", "color": "d73a4a", "description": "Bug report"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            success, missing, mismatched = validator.validate_repository("owner/repo")

        assert success is False
        assert len(missing) == 1
        assert missing[0]["name"] == "feature"

    def test_mismatched_colors_returned(self, validator):
        """Test returns mismatched labels when colors differ."""
        existing_labels = [
            {"name": "bug", "color": "ffffff", "description": "Wrong color"},
            {"name": "feature", "color": "a2eeef", "description": "New feature"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            success, missing, mismatched = validator.validate_repository("owner/repo")

        assert success is False
        assert len(mismatched) == 1
        assert mismatched[0]["name"] == "bug"

    def test_returns_failure_when_api_fails(self, validator):
        """Test returns failure when API call fails."""
        with patch.object(validator, "_get_repo_labels", return_value=None):
            success, missing, mismatched = validator.validate_repository("owner/repo")

        assert success is False
        assert missing == []
        assert mismatched == []


@pytest.mark.unit
class TestFixRepository:
    """Test repository fixing logic."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator with fix mode enabled."""
        config = {"repositories": [], "labels": []}
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path, fix_mode=True)

    def test_returns_true_when_nothing_to_fix(self, validator):
        """Test returns True when no issues to fix."""
        result = validator.fix_repository("owner/repo", [], [])
        assert result is True

    def test_creates_missing_labels(self, validator):
        """Test creates all missing labels."""
        missing = [
            {"name": "bug", "color": "d73a4a", "description": "Bug"},
            {"name": "feature", "color": "a2eeef", "description": "Feature"},
        ]

        with patch.object(validator, "_create_label", return_value=True) as mock_create:
            result = validator.fix_repository("owner/repo", missing, [])

        assert result is True
        assert mock_create.call_count == 2

    def test_updates_mismatched_labels(self, validator):
        """Test updates labels with wrong colors."""
        mismatched = [
            {"name": "bug", "color": "d73a4a", "description": "Bug"},
        ]

        with patch.object(validator, "_create_label", return_value=True) as mock_create:
            result = validator.fix_repository("owner/repo", [], mismatched)

        assert result is True
        mock_create.assert_called_once()

    def test_returns_false_when_creation_fails(self, validator):
        """Test returns False when label creation fails."""
        missing = [{"name": "bug", "color": "d73a4a", "description": "Bug"}]

        with patch.object(validator, "_create_label", return_value=False):
            result = validator.fix_repository("owner/repo", missing, [])

        assert result is False


@pytest.mark.unit
class TestValidateAll:
    """Test full validation workflow."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator with config."""
        config = {
            "repositories": ["owner/repo1", "owner/repo2"],
            "labels": [
                {"name": "bug", "color": "d73a4a", "description": "Bug"},
            ],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        with patch("validate_labels.ensure_github_token"):
            return LabelValidator(config_path)

    def test_returns_false_when_no_repositories(self, validator, capsys):
        """Test returns False when no repositories configured."""
        validator.config["repositories"] = []

        result = validator.validate_all()

        assert result is False
        captured = capsys.readouterr()
        assert "No repositories" in captured.out

    def test_returns_false_when_no_labels(self, validator, capsys):
        """Test returns False when no labels configured."""
        validator.config["labels"] = []

        result = validator.validate_all()

        assert result is False
        captured = capsys.readouterr()
        assert "No labels" in captured.out

    def test_returns_true_when_all_pass(self, validator):
        """Test returns True when all repositories pass validation."""
        with patch.object(validator, "validate_repository", return_value=(True, [], [])):
            result = validator.validate_all()

        assert result is True

    def test_returns_false_when_any_fails(self, validator):
        """Test returns False when any repository fails validation."""
        with patch.object(
            validator,
            "validate_repository",
            return_value=(False, [{"name": "bug"}], []),
        ):
            result = validator.validate_all()

        assert result is False
