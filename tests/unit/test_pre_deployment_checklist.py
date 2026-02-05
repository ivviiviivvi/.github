#!/usr/bin/env python3
"""Tests for pre_deployment_checklist.py.

Tests the pre-deployment validation checklist including configuration
validation, GitHub CLI checks, and prerequisite verification.
"""

import json
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "src/automation/scripts")

from src.automation.scripts.pre_deployment_checklist import (
    CheckResult, PreDeploymentChecker, main)


@pytest.mark.unit
class TestCheckResult:
    """Test CheckResult class."""

    def test_check_result_passed(self):
        """Test passed check result."""
        result = CheckResult(
            name="Test Check",
            passed=True,
            message="Everything is fine",
        )

        assert result.name == "Test Check"
        assert result.passed is True
        assert result.message == "Everything is fine"
        assert result.details is None

    def test_check_result_failed_with_details(self):
        """Test failed check result with details."""
        result = CheckResult(
            name="Config Check",
            passed=False,
            message="Missing file",
            details="Expected at: /path/to/file",
        )

        assert result.passed is False
        assert result.details == "Expected at: /path/to/file"

    def test_check_result_str_passed(self):
        """Test string representation of passed result."""
        result = CheckResult(
            name="Test",
            passed=True,
            message="OK",
        )

        output = str(result)
        assert "✅" in output
        assert "Test" in output
        assert "OK" in output

    def test_check_result_str_failed(self):
        """Test string representation of failed result."""
        result = CheckResult(
            name="Test",
            passed=False,
            message="Failed",
        )

        output = str(result)
        assert "❌" in output

    def test_check_result_str_with_details(self):
        """Test string representation includes details."""
        result = CheckResult(
            name="Test",
            passed=True,
            message="OK",
            details="Additional info",
        )

        output = str(result)
        assert "Additional info" in output


@pytest.mark.unit
class TestPreDeploymentCheckerInit:
    """Test PreDeploymentChecker initialization."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_init_sets_properties(self, mock_token):
        """Test initialization sets all properties."""
        checker = PreDeploymentChecker(phase=1, skip_labels=True, verbose=True)

        assert checker.phase == 1
        assert checker.skip_labels is True
        assert checker.verbose is True
        assert checker.results == []
        assert checker.config is None

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_get_config_path_phase1(self, mock_token):
        """Test config path for phase 1."""
        checker = PreDeploymentChecker(phase=1)

        assert "phase1-pilot" in str(checker.config_path)

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_get_config_path_phase2(self, mock_token):
        """Test config path for phase 2."""
        checker = PreDeploymentChecker(phase=2)

        assert "phase2-expansion" in str(checker.config_path)

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_get_config_path_phase3(self, mock_token):
        """Test config path for phase 3."""
        checker = PreDeploymentChecker(phase=3)

        assert "phase3-final" in str(checker.config_path)


@pytest.mark.unit
class TestRunCommand:
    """Test _run_command method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_run_command_success(self, mock_token):
        """Test successful command execution."""
        checker = PreDeploymentChecker(phase=1)

        success, stdout, stderr = checker._run_command(["echo", "hello"])

        assert success is True
        assert "hello" in stdout

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_run_command_failure(self, mock_token):
        """Test failed command execution."""
        checker = PreDeploymentChecker(phase=1)

        success, stdout, stderr = checker._run_command(["false"])

        assert success is False

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    @patch("subprocess.run")
    def test_run_command_timeout(self, mock_run, mock_token):
        """Test command timeout handling."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=10)

        checker = PreDeploymentChecker(phase=1)
        success, stdout, stderr = checker._run_command(["sleep", "100"])

        assert success is False
        assert "timed out" in stderr

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    @patch("subprocess.run")
    def test_run_command_exception(self, mock_run, mock_token):
        """Test command exception handling."""
        mock_run.side_effect = Exception("Unexpected error")

        checker = PreDeploymentChecker(phase=1)
        success, stdout, stderr = checker._run_command(["test"])

        assert success is False
        assert "Unexpected error" in stderr


@pytest.mark.unit
class TestCheckConfigExists:
    """Test check_config_exists method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_config_exists(self, mock_token, tmp_path):
        """Test check passes when config exists."""
        checker = PreDeploymentChecker(phase=1)
        checker.config_path = tmp_path / "config.yml"
        checker.config_path.write_text("repositories: []")

        result = checker.check_config_exists()

        assert result.passed is True
        assert "Found" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_config_missing(self, mock_token, tmp_path):
        """Test check fails when config missing."""
        checker = PreDeploymentChecker(phase=1)
        checker.config_path = tmp_path / "missing.yml"

        result = checker.check_config_exists()

        assert result.passed is False
        assert "Missing" in result.message


@pytest.mark.unit
class TestCheckConfigValid:
    """Test check_config_valid method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_config_valid(self, mock_token, tmp_path):
        """Test check passes for valid config."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("""
repositories:
  - org/repo
workflows:
  - ci.yml
labels:
  bug:
    color: ff0000
""")

        checker = PreDeploymentChecker(phase=1)
        checker.config_path = config_file

        result = checker.check_config_valid()

        assert result.passed is True
        assert checker.config is not None

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_config_missing_keys(self, mock_token, tmp_path):
        """Test check fails for missing required keys."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("repositories: []")

        checker = PreDeploymentChecker(phase=1)
        checker.config_path = config_file

        result = checker.check_config_valid()

        assert result.passed is False
        assert "Missing" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_config_invalid_yaml(self, mock_token, tmp_path):
        """Test check fails for invalid YAML."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("invalid: yaml: syntax: :")

        checker = PreDeploymentChecker(phase=1)
        checker.config_path = config_file

        result = checker.check_config_valid()

        assert result.passed is False
        assert "Invalid YAML" in result.message


@pytest.mark.unit
class TestCheckGitHubCLI:
    """Test check_github_cli method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_github_cli_not_found(self, mock_token):
        """Test check fails when gh not installed."""
        checker = PreDeploymentChecker(phase=1)

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (False, "", "not found")

            result = checker.check_github_cli()

        assert result.passed is False
        assert "not found" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_github_cli_not_authenticated(self, mock_token):
        """Test check fails when not authenticated."""
        checker = PreDeploymentChecker(phase=1)

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.side_effect = [
                (True, "/usr/bin/gh", ""),  # which gh
                (False, "", "not authenticated"),  # gh auth status
            ]

            result = checker.check_github_cli()

        assert result.passed is False
        assert "Not authenticated" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_github_cli_authenticated(self, mock_token):
        """Test check passes when authenticated."""
        checker = PreDeploymentChecker(phase=1)

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.side_effect = [
                (True, "/usr/bin/gh", ""),
                (True, "Logged in as user", ""),
            ]

            result = checker.check_github_cli()

        assert result.passed is True


@pytest.mark.unit
class TestCheckPythonDependencies:
    """Test check_python_dependencies method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_dependencies_installed(self, mock_token):
        """Test check passes when dependencies installed."""
        checker = PreDeploymentChecker(phase=1)

        result = checker.check_python_dependencies()

        assert result.passed is True
        assert "pyyaml" in result.message


@pytest.mark.unit
class TestCheckWorkflowTemplates:
    """Test check_workflow_templates method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_no_config_loaded(self, mock_token):
        """Test check fails when config not loaded."""
        checker = PreDeploymentChecker(phase=1)
        checker.config = None

        result = checker.check_workflow_templates()

        assert result.passed is False
        assert "not loaded" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_workflow_templates_missing(self, mock_token):
        """Test check fails when templates missing."""
        checker = PreDeploymentChecker(phase=1)
        checker.config = {"workflows": ["missing-workflow.yml"]}

        result = checker.check_workflow_templates()

        assert result.passed is False
        assert "not found" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_workflow_templates_empty(self, mock_token):
        """Test check passes when no workflows specified."""
        checker = PreDeploymentChecker(phase=1)
        checker.config = {"workflows": []}

        result = checker.check_workflow_templates()

        assert result.passed is True


@pytest.mark.unit
class TestCheckRepositoryAccess:
    """Test check_repository_access method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_no_config_loaded(self, mock_token):
        """Test check fails when config not loaded."""
        checker = PreDeploymentChecker(phase=1)
        checker.config = None

        result = checker.check_repository_access()

        assert result.passed is False

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_repositories_accessible(self, mock_token):
        """Test check passes when repos accessible."""
        checker = PreDeploymentChecker(phase=1)
        checker.config = {"repositories": ["org/repo1", "org/repo2"]}

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (True, '{"name": "repo"}', "")

            result = checker.check_repository_access()

        assert result.passed is True

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_repository_inaccessible(self, mock_token):
        """Test check fails when repo inaccessible."""
        checker = PreDeploymentChecker(phase=1)
        checker.config = {"repositories": ["org/private"]}

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (False, "", "not found")

            result = checker.check_repository_access()

        assert result.passed is False


@pytest.mark.unit
class TestCheckLabelsDeployed:
    """Test check_labels_deployed method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_skip_labels_flag(self, mock_token):
        """Test check skipped with flag."""
        checker = PreDeploymentChecker(phase=1, skip_labels=True)

        result = checker.check_labels_deployed()

        assert result.passed is True
        assert "Skipped" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_no_config_loaded(self, mock_token):
        """Test check fails when config not loaded."""
        checker = PreDeploymentChecker(phase=1, skip_labels=False)
        checker.config = None

        result = checker.check_labels_deployed()

        assert result.passed is False

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_labels_present_dict_format(self, mock_token):
        """Test check passes when labels present (dict format)."""
        checker = PreDeploymentChecker(phase=1, skip_labels=False)
        checker.config = {
            "repositories": ["org/repo"],
            "labels": {"bug": {"color": "ff0000"}},
        }

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (True, json.dumps([{"name": "bug"}]), "")

            result = checker.check_labels_deployed()

        assert result.passed is True

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_labels_present_list_format(self, mock_token):
        """Test check passes when labels present (list format)."""
        checker = PreDeploymentChecker(phase=1, skip_labels=False)
        checker.config = {
            "repositories": ["org/repo"],
            "labels": [{"name": "bug", "color": "ff0000"}],
        }

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (True, json.dumps([{"name": "bug"}]), "")

            result = checker.check_labels_deployed()

        assert result.passed is True

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_labels_missing(self, mock_token):
        """Test check fails when labels missing."""
        checker = PreDeploymentChecker(phase=1, skip_labels=False)
        checker.config = {
            "repositories": ["org/repo"],
            "labels": {"bug": {}, "feature": {}},
        }

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (True, json.dumps([{"name": "bug"}]), "")

            result = checker.check_labels_deployed()

        assert result.passed is False
        assert "missing" in result.message.lower()

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_labels_invalid_config_format(self, mock_token):
        """Test check fails for invalid labels config format."""
        checker = PreDeploymentChecker(phase=1, skip_labels=False)
        checker.config = {
            "repositories": ["org/repo"],
            "labels": "invalid",
        }

        result = checker.check_labels_deployed()

        assert result.passed is False
        assert "Invalid labels" in result.message

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_labels_json_decode_error(self, mock_token):
        """Test check handles JSON decode error."""
        checker = PreDeploymentChecker(phase=1, skip_labels=False)
        checker.config = {
            "repositories": ["org/repo"],
            "labels": {"bug": {}},
        }

        with patch.object(checker, "_run_command") as mock_run:
            mock_run.return_value = (True, "invalid json", "")

            result = checker.check_labels_deployed()

        assert result.passed is False


@pytest.mark.unit
class TestCheckPhasePrerequisites:
    """Test check_phase_prerequisites method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_phase1_no_prerequisites(self, mock_token):
        """Test phase 1 has no prerequisites."""
        checker = PreDeploymentChecker(phase=1)

        result = checker.check_phase_prerequisites()

        assert result.passed is True
        assert "initial" in result.message.lower()

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_phase2_prerequisites(self, mock_token):
        """Test phase 2 mentions phase 1."""
        checker = PreDeploymentChecker(phase=2)

        result = checker.check_phase_prerequisites()

        assert result.passed is True
        assert "Phase 1" in result.message or "Phase 1" in (result.details or "")

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_phase3_prerequisites(self, mock_token):
        """Test phase 3 mentions phase 2."""
        checker = PreDeploymentChecker(phase=3)

        result = checker.check_phase_prerequisites()

        assert result.passed is True


@pytest.mark.unit
class TestRunAllChecks:
    """Test run_all_checks method."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_run_all_checks_all_pass(self, mock_token, tmp_path, capsys):
        """Test run_all_checks returns True when all pass."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("""
repositories: []
workflows: []
labels: []
""")

        checker = PreDeploymentChecker(phase=1, skip_labels=True)
        checker.config_path = config_file

        with patch.object(checker, "check_github_cli") as mock_gh:
            with patch.object(checker, "check_repository_access") as mock_repo:
                mock_gh.return_value = CheckResult("GH CLI", True, "OK")
                mock_repo.return_value = CheckResult("Repo Access", True, "OK")

                result = checker.run_all_checks()

        assert result is True
        captured = capsys.readouterr()
        assert "ALL CHECKS PASSED" in captured.out

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_run_all_checks_some_fail(self, mock_token, tmp_path, capsys):
        """Test run_all_checks returns False when some fail."""
        checker = PreDeploymentChecker(phase=1)
        checker.config_path = tmp_path / "missing.yml"  # Missing config

        result = checker.run_all_checks()

        assert result is False
        captured = capsys.readouterr()
        assert "FAILED" in captured.out

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    def test_run_all_checks_handles_exception(self, mock_token, tmp_path, capsys):
        """Test run_all_checks handles exceptions in checks."""
        config_file = tmp_path / "config.yml"
        config_file.write_text("repositories: []\nworkflows: []\nlabels: []")

        checker = PreDeploymentChecker(phase=1, skip_labels=True)
        checker.config_path = config_file

        with patch.object(checker, "check_github_cli") as mock_gh:
            mock_gh.side_effect = Exception("Unexpected error")

            result = checker.run_all_checks()

        # Should handle exception and continue
        assert result is False


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    @patch("src.automation.scripts.pre_deployment_checklist.PreDeploymentChecker")
    def test_main_all_pass(self, MockChecker, mock_token):
        """Test main exits 0 when all checks pass."""
        mock_instance = MagicMock()
        mock_instance.run_all_checks.return_value = True
        MockChecker.return_value = mock_instance

        with patch("sys.argv", ["checklist.py", "--phase", "1"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    @patch("src.automation.scripts.pre_deployment_checklist.PreDeploymentChecker")
    def test_main_some_fail(self, MockChecker, mock_token):
        """Test main exits 1 when checks fail."""
        mock_instance = MagicMock()
        mock_instance.run_all_checks.return_value = False
        MockChecker.return_value = mock_instance

        with patch("sys.argv", ["checklist.py", "--phase", "2"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    @patch("src.automation.scripts.pre_deployment_checklist.ensure_github_token")
    @patch("src.automation.scripts.pre_deployment_checklist.PreDeploymentChecker")
    def test_main_with_flags(self, MockChecker, mock_token):
        """Test main passes flags to checker."""
        mock_instance = MagicMock()
        mock_instance.run_all_checks.return_value = True
        MockChecker.return_value = mock_instance

        with patch(
            "sys.argv",
            ["checklist.py", "--phase", "3", "--skip-labels", "--verbose"],
        ):
            with pytest.raises(SystemExit):
                main()

        MockChecker.assert_called_once_with(
            phase=3,
            skip_labels=True,
            verbose=True,
        )
