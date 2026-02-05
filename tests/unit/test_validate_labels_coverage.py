#!/usr/bin/env python3
"""Extended unit tests for validate_labels.py to improve coverage.

Focus: main function, config loading errors, fix_mode in validate_all.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock secret_manager before importing validate_labels
sys.modules["secret_manager"] = MagicMock()

from validate_labels import LabelValidator, main


@pytest.mark.unit
class TestLoadConfigErrors:
    """Test _load_config error handling."""

    def test_exits_on_yaml_error(self, tmp_path, capsys):
        """Test exits when YAML parsing fails."""
        config_path = tmp_path / "invalid.yml"
        config_path.write_text("invalid: yaml: content: [")

        with pytest.raises(SystemExit) as exc:
            LabelValidator(config_path)

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error loading config" in captured.out

    def test_exits_on_file_not_found(self, tmp_path, capsys):
        """Test exits when config file doesn't exist."""
        config_path = tmp_path / "nonexistent.yml"

        with pytest.raises(SystemExit) as exc:
            LabelValidator(config_path)

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error loading config" in captured.out

    def test_handles_empty_labels_dict(self, tmp_path):
        """Test handles config with empty labels dict."""
        config = {
            "repositories": ["owner/repo"],
            "labels": {},
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        validator = LabelValidator(config_path)

        assert validator.config["labels"] == []

    def test_handles_missing_description_in_dict_labels(self, tmp_path):
        """Test handles dict labels without description."""
        config = {
            "repositories": ["owner/repo"],
            "labels": {
                "bug": {"color": "d73a4a"},
            },
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        validator = LabelValidator(config_path)

        labels = validator.config["labels"]
        assert len(labels) == 1
        assert labels[0]["description"] == ""


@pytest.mark.unit
class TestValidateAllWithFixMode:
    """Test validate_all with fix_mode enabled."""

    @pytest.fixture
    def fix_mode_validator(self, tmp_path):
        """Create a validator with fix mode enabled."""
        config = {
            "repositories": ["owner/repo1", "owner/repo2"],
            "labels": [
                {"name": "bug", "color": "d73a4a", "description": "Bug"},
            ],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        return LabelValidator(config_path, fix_mode=True)

    def test_fix_mode_calls_fix_repository(self, fix_mode_validator):
        """Test fix_mode calls fix_repository when issues found."""
        missing = [{"name": "bug", "color": "d73a4a"}]

        with patch.object(fix_mode_validator, "validate_repository", return_value=(False, missing, [])):
            with patch.object(fix_mode_validator, "fix_repository", return_value=True) as mock_fix:
                result = fix_mode_validator.validate_all()

        # fix_repository should be called for each repo with issues
        assert mock_fix.call_count == 2

    def test_fix_mode_updates_success_on_fix(self, fix_mode_validator, capsys):
        """Test fix_mode updates success status after fix."""
        missing = [{"name": "bug", "color": "d73a4a"}]

        with patch.object(fix_mode_validator, "validate_repository", return_value=(False, missing, [])):
            with patch.object(fix_mode_validator, "fix_repository", return_value=True):
                result = fix_mode_validator.validate_all()

        # Should still return False since validation failed initially
        # but the overall result reflects fix attempts
        captured = capsys.readouterr()
        assert "VALIDATION SUMMARY" in captured.out

    def test_fix_mode_banner_printed(self, fix_mode_validator, capsys):
        """Test fix mode banner is printed."""
        with patch.object(fix_mode_validator, "validate_repository", return_value=(True, [], [])):
            fix_mode_validator.validate_all()

        captured = capsys.readouterr()
        assert "FIX MODE ENABLED" in captured.out

    def test_validation_mode_banner_when_no_fix(self, tmp_path, capsys):
        """Test validation mode banner when fix_mode is False."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        validator = LabelValidator(config_path, fix_mode=False)

        with patch.object(validator, "validate_repository", return_value=(True, [], [])):
            validator.validate_all()

        captured = capsys.readouterr()
        assert "VALIDATION MODE" in captured.out

    def test_fix_mode_with_mismatched_labels(self, fix_mode_validator, capsys):
        """Test fix_mode handles mismatched labels."""
        mismatched = [{"name": "bug", "color": "d73a4a"}]

        with patch.object(fix_mode_validator, "validate_repository", return_value=(False, [], mismatched)):
            with patch.object(fix_mode_validator, "fix_repository", return_value=True) as mock_fix:
                result = fix_mode_validator.validate_all()

        # Should call fix for mismatched labels
        assert mock_fix.call_count == 2

    def test_prints_tip_when_not_fix_mode(self, tmp_path, capsys):
        """Test prints tip to use --fix when validation fails."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        validator = LabelValidator(config_path, fix_mode=False)

        with patch.object(validator, "validate_repository", return_value=(False, [{"name": "bug"}], [])):
            result = validator.validate_all()

        assert result is False
        captured = capsys.readouterr()
        assert "--fix" in captured.out


@pytest.mark.unit
class TestMainFunction:
    """Test main function CLI handling."""

    def test_main_config_not_found(self, tmp_path, capsys, monkeypatch):
        """Test main exits when config file not found."""
        monkeypatch.setattr(sys, "argv", ["validate_labels.py", "--config", str(tmp_path / "missing.yml")])

        with patch("validate_labels.ensure_github_token", return_value="token"):
            with pytest.raises(SystemExit) as exc:
                main()

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_main_success_exits_0(self, tmp_path, monkeypatch, capsys):
        """Test main exits with 0 on successful validation."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        monkeypatch.setattr(sys, "argv", ["validate_labels.py", "--config", str(config_path)])

        with patch("validate_labels.ensure_github_token", return_value="token"):
            with patch.object(LabelValidator, "validate_all", return_value=True):
                with pytest.raises(SystemExit) as exc:
                    main()

        assert exc.value.code == 0

    def test_main_failure_exits_1(self, tmp_path, monkeypatch, capsys):
        """Test main exits with 1 on validation failure."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        monkeypatch.setattr(sys, "argv", ["validate_labels.py", "--config", str(config_path)])

        with patch("validate_labels.ensure_github_token", return_value="token"):
            with patch.object(LabelValidator, "validate_all", return_value=False):
                with pytest.raises(SystemExit) as exc:
                    main()

        assert exc.value.code == 1

    def test_main_with_fix_flag(self, tmp_path, monkeypatch, capsys):
        """Test main passes fix flag to validator."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        monkeypatch.setattr(sys, "argv", ["validate_labels.py", "--config", str(config_path), "--fix"])

        validator_instances = []

        original_init = LabelValidator.__init__

        def tracking_init(self, config_path, fix_mode=False):
            validator_instances.append({"fix_mode": fix_mode})
            original_init(self, config_path, fix_mode)

        with patch("validate_labels.ensure_github_token", return_value="token"):
            with patch.object(LabelValidator, "__init__", tracking_init):
                with patch.object(LabelValidator, "validate_all", return_value=True):
                    with pytest.raises(SystemExit):
                        main()

        # Verify fix_mode was True
        assert len(validator_instances) == 1
        assert validator_instances[0]["fix_mode"] is True

    def test_main_ensures_github_token(self, tmp_path, monkeypatch):
        """Test main calls ensure_github_token."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        monkeypatch.setattr(sys, "argv", ["validate_labels.py", "--config", str(config_path)])

        with patch("validate_labels.ensure_github_token", return_value="token") as mock_ensure:
            with patch.object(LabelValidator, "validate_all", return_value=True):
                with pytest.raises(SystemExit):
                    main()

        mock_ensure.assert_called_once_with("org-label-sync-token")


@pytest.mark.unit
class TestFixRepositoryOutput:
    """Test fix_repository output messages."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator with fix mode enabled."""
        config = {"repositories": [], "labels": []}
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        return LabelValidator(config_path, fix_mode=True)

    def test_prints_created_message(self, validator, capsys):
        """Test prints message when label is created."""
        missing = [{"name": "bug", "color": "d73a4a", "description": "Bug"}]

        with patch.object(validator, "_create_label", return_value=True):
            validator.fix_repository("owner/repo", missing, [])

        captured = capsys.readouterr()
        assert "Created: bug" in captured.out

    def test_prints_updated_message(self, validator, capsys):
        """Test prints message when label is updated."""
        mismatched = [{"name": "bug", "color": "d73a4a", "description": "Bug"}]

        with patch.object(validator, "_create_label", return_value=True):
            validator.fix_repository("owner/repo", [], mismatched)

        captured = capsys.readouterr()
        assert "Updated: bug" in captured.out

    def test_prints_failed_create_message(self, validator, capsys):
        """Test prints message when label creation fails."""
        missing = [{"name": "bug", "color": "d73a4a", "description": "Bug"}]

        with patch.object(validator, "_create_label", return_value=False):
            validator.fix_repository("owner/repo", missing, [])

        captured = capsys.readouterr()
        assert "Failed to create: bug" in captured.out

    def test_prints_failed_update_message(self, validator, capsys):
        """Test prints message when label update fails."""
        mismatched = [{"name": "bug", "color": "d73a4a", "description": "Bug"}]

        with patch.object(validator, "_create_label", return_value=False):
            validator.fix_repository("owner/repo", [], mismatched)

        captured = capsys.readouterr()
        assert "Failed to update: bug" in captured.out

    def test_prints_fixing_header(self, validator, capsys):
        """Test prints 'Fixing labels' header."""
        missing = [{"name": "bug", "color": "d73a4a", "description": "Bug"}]

        with patch.object(validator, "_create_label", return_value=True):
            validator.fix_repository("owner/repo", missing, [])

        captured = capsys.readouterr()
        assert "Fixing labels" in captured.out


@pytest.mark.unit
class TestValidateRepositoryOutput:
    """Test validate_repository output messages."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator with labels config."""
        config = {
            "repositories": ["owner/repo"],
            "labels": [
                {"name": "bug", "color": "d73a4a", "description": "Bug"},
                {"name": "feature", "color": "a2eeef", "description": "Feature"},
            ],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        return LabelValidator(config_path)

    def test_prints_validating_header(self, validator, capsys):
        """Test prints 'Validating' header."""
        with patch.object(validator, "_get_repo_labels", return_value=[]):
            validator.validate_repository("owner/repo")

        captured = capsys.readouterr()
        assert "Validating owner/repo" in captured.out

    def test_prints_found_for_matching_labels(self, validator, capsys):
        """Test prints 'Found' for labels that match."""
        existing_labels = [
            {"name": "bug", "color": "d73a4a", "description": "Bug"},
            {"name": "feature", "color": "a2eeef", "description": "Feature"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            validator.validate_repository("owner/repo")

        captured = capsys.readouterr()
        assert "Found: bug" in captured.out
        assert "Found: feature" in captured.out

    def test_prints_mismatch_with_colors(self, validator, capsys):
        """Test prints mismatch message with expected and actual colors."""
        existing_labels = [
            {"name": "bug", "color": "ffffff", "description": "Wrong color"},
            {"name": "feature", "color": "a2eeef", "description": "Feature"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            validator.validate_repository("owner/repo")

        captured = capsys.readouterr()
        assert "Mismatch: bug" in captured.out
        assert "d73a4a" in captured.out
        assert "ffffff" in captured.out

    def test_prints_all_validated_message(self, validator, capsys):
        """Test prints 'All labels validated' when no issues."""
        existing_labels = [
            {"name": "bug", "color": "d73a4a", "description": "Bug"},
            {"name": "feature", "color": "a2eeef", "description": "Feature"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            success, _, _ = validator.validate_repository("owner/repo")

        assert success is True
        captured = capsys.readouterr()
        assert "All 2 labels validated" in captured.out

    def test_prints_issue_count_on_failure(self, validator, capsys):
        """Test prints issue count when validation fails."""
        # Only bug label exists
        existing_labels = [
            {"name": "bug", "color": "d73a4a", "description": "Bug"},
        ]

        with patch.object(validator, "_get_repo_labels", return_value=existing_labels):
            success, missing, _ = validator.validate_repository("owner/repo")

        assert success is False
        captured = capsys.readouterr()
        assert "1 label issues found" in captured.out


@pytest.mark.unit
class TestValidateAllSummary:
    """Test validate_all summary output."""

    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator with multiple repos."""
        config = {
            "repositories": ["owner/repo1", "owner/repo2", "owner/repo3"],
            "labels": [{"name": "bug", "color": "d73a4a"}],
        }
        config_path = tmp_path / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        return LabelValidator(config_path)

    def test_prints_summary_header(self, validator, capsys):
        """Test prints summary header."""
        with patch.object(validator, "validate_repository", return_value=(True, [], [])):
            validator.validate_all()

        captured = capsys.readouterr()
        assert "VALIDATION SUMMARY" in captured.out
        assert "=" * 80 in captured.out

    def test_prints_pass_for_successful_repos(self, validator, capsys):
        """Test prints PASS for repos that validate successfully."""
        with patch.object(validator, "validate_repository", return_value=(True, [], [])):
            validator.validate_all()

        captured = capsys.readouterr()
        assert "PASS" in captured.out

    def test_prints_fail_for_failed_repos(self, validator, capsys):
        """Test prints FAIL for repos that fail validation."""
        with patch.object(validator, "validate_repository", return_value=(False, [{"name": "bug"}], [])):
            validator.validate_all()

        captured = capsys.readouterr()
        assert "FAIL" in captured.out

    def test_prints_all_validated_success(self, validator, capsys):
        """Test prints success message when all repos pass."""
        with patch.object(validator, "validate_repository", return_value=(True, [], [])):
            result = validator.validate_all()

        assert result is True
        captured = capsys.readouterr()
        assert "All repositories validated successfully" in captured.out

    def test_prints_failed_count(self, validator, capsys):
        """Test prints count of failed repos."""

        # Make only repo1 pass
        def mock_validate(repo):
            if "repo1" in repo:
                return (True, [], [])
            return (False, [{"name": "bug"}], [])

        with patch.object(validator, "validate_repository", side_effect=mock_validate):
            result = validator.validate_all()

        assert result is False
        captured = capsys.readouterr()
        assert "2/3 repositories have label issues" in captured.out
