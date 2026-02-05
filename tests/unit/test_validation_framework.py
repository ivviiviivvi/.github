#!/usr/bin/env python3
"""Unit tests for automation/scripts/validation_framework.py
Focus: ValidationFramework class, capability validations, report generation.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock notification_integration before importing validation_framework
sys.modules["notification_integration"] = MagicMock()

from models import ValidationResult
from validation_framework import ValidationFramework


class TestValidationFramework:
    """Test ValidationFramework class."""

    @pytest.fixture
    def mock_github_client(self):
        """Create mock GitHub client."""
        client = MagicMock()
        return client

    @pytest.fixture
    def framework(self, mock_github_client, tmp_path):
        """Create ValidationFramework instance."""
        with patch.object(
            ValidationFramework,
            "__init__",
            lambda self, client: setattr(self, "github", client)
            or setattr(self, "results", [])
            or setattr(self, "validation_dir", tmp_path / ".github" / "validation"),
        ):
            fw = ValidationFramework.__new__(ValidationFramework)
            fw.github = mock_github_client
            fw.results = []
            fw.validation_dir = tmp_path / ".github" / "validation"
            fw.validation_dir.mkdir(parents=True, exist_ok=True)
            return fw


class TestAutoMergeValidation:
    """Test auto-merge validation."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def framework(self, mock_client, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = mock_client
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_fails_when_config_missing(self, framework):
        """Test validation fails when config file is missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_auto_merge("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_passes_with_config_and_prs(self, framework, mock_client, tmp_path):
        """Test validation passes with config and merged PRs."""
        # Create config file
        config_path = Path(".github/auto-merge.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true\nmin_reviews: 1")

        # Mock API response with merged PRs
        mock_client.get.return_value = [
            {"number": 1, "merged_at": "2024-01-01T00:00:00Z"},
            {"number": 2, "merged_at": "2024-01-02T00:00:00Z"},
            {"number": 3, "merged_at": None},
        ]

        result = framework.validate_auto_merge("owner", "repo")

        assert result.passed is True
        assert result.capability == "auto-merge"
        assert result.metrics.get("tested_prs") == 2
        assert result.metrics.get("merge_rate") == pytest.approx(2 / 3)

        # Cleanup
        config_path.unlink()

    def test_warns_when_no_merged_prs(self, framework, mock_client):
        """Test warns when no merged PRs found."""
        config_path = Path(".github/auto-merge.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        mock_client.get.return_value = [
            {"number": 1, "merged_at": None},
            {"number": 2, "merged_at": None},
        ]

        result = framework.validate_auto_merge("owner", "repo")

        assert result.passed is True
        assert "No merged PRs found for testing" in result.warnings

        config_path.unlink()

    def test_handles_api_error(self, framework, mock_client):
        """Test handles API error gracefully."""
        config_path = Path(".github/auto-merge.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        mock_client.get.side_effect = Exception("API Error")

        result = framework.validate_auto_merge("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

        config_path.unlink()


class TestRoutingValidation:
    """Test intelligent routing validation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_fails_when_config_missing(self, framework):
        """Test validation fails when config file is missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_routing("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_passes_with_assigned_prs(self, framework):
        """Test validation passes with assigned PRs."""
        config_path = Path(".github/routing.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        framework.github.get.return_value = [
            {"number": 1, "requested_reviewers": [{"login": "user1"}]},
            {"number": 2, "requested_reviewers": [{"login": "user2"}]},
            {"number": 3, "requested_reviewers": [{"login": "user1"}]},
            {"number": 4, "requested_reviewers": []},
        ]

        result = framework.validate_routing("owner", "repo")

        assert result.passed is True
        assert result.metrics.get("assigned_prs") == 3
        assert result.metrics.get("unique_reviewers") == 2
        assert result.metrics.get("avg_prs_per_reviewer") == pytest.approx(1.5)

        config_path.unlink()


class TestSelfHealingValidation:
    """Test self-healing validation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_calculates_failure_rate(self, framework):
        """Test calculates failure rate from workflow runs."""
        config_path = Path(".github/self-healing.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        framework.github.get.return_value = {
            "workflow_runs": [
                {"conclusion": "success"},
                {"conclusion": "failure"},
                {"conclusion": "success"},
                {"conclusion": "success"},
                {"conclusion": "failure"},
            ]
        }

        result = framework.validate_self_healing("owner", "repo")

        assert result.passed is True
        assert result.metrics.get("total_runs") == 5
        assert result.metrics.get("failed_runs") == 2
        assert result.metrics.get("failure_rate") == pytest.approx(0.4)

        config_path.unlink()


class TestMaintenanceValidation:
    """Test maintenance validation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_counts_scheduled_tasks(self, framework):
        """Test counts scheduled maintenance tasks."""
        config_path = Path(".github/maintenance.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        tasks_dir = Path(".github/maintenance/tasks")
        tasks_dir.mkdir(parents=True, exist_ok=True)
        (tasks_dir / "task1.json").write_text('{"type": "cleanup"}')
        (tasks_dir / "task2.json").write_text('{"type": "update"}')

        result = framework.validate_maintenance("owner", "repo")

        assert result.passed is True
        assert result.metrics.get("scheduled_tasks") == 2

        # Cleanup
        (tasks_dir / "task1.json").unlink()
        (tasks_dir / "task2.json").unlink()
        tasks_dir.rmdir()
        config_path.unlink()


class TestAnalyticsValidation:
    """Test analytics ML validation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_counts_trained_models(self, framework):
        """Test counts trained ML models."""
        config_path = Path(".github/analytics.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        models_dir = Path(".github/models")
        models_dir.mkdir(parents=True, exist_ok=True)
        (models_dir / "model1.joblib").write_bytes(b"fake model")
        (models_dir / "model2.joblib").write_bytes(b"fake model")

        result = framework.validate_analytics("owner", "repo")

        assert result.passed is True
        assert result.metrics.get("trained_models") == 2
        # Should warn if < 3 models
        assert any("Expected 3 models" in w for w in result.warnings)

        # Cleanup
        (models_dir / "model1.joblib").unlink()
        (models_dir / "model2.joblib").unlink()
        models_dir.rmdir()
        config_path.unlink()


class TestSLAValidation:
    """Test SLA monitoring validation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_counts_issues(self, framework):
        """Test counts issues for SLA analysis."""
        config_path = Path(".github/sla.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        framework.github.get.return_value = [
            {"number": 1, "created_at": "2024-01-01T00:00:00Z", "comments": 2},
            {"number": 2, "created_at": "2024-01-02T00:00:00Z", "comments": 0},
        ]

        result = framework.validate_sla("owner", "repo")

        assert result.passed is True
        assert result.metrics.get("total_items") == 2

        config_path.unlink()


class TestIncidentResponseValidation:
    """Test incident response validation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_analyzes_incident_severity(self, framework, tmp_path, monkeypatch):
        """Test analyzes incident severity distribution."""
        # Use temp directory to avoid conflicts with existing files
        monkeypatch.chdir(tmp_path)

        config_path = Path(".github/incident.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        incidents_dir = Path(".github/incidents")
        incidents_dir.mkdir(parents=True, exist_ok=True)
        (incidents_dir / "INC-001.json").write_text('{"severity": "SEV-1"}')
        (incidents_dir / "INC-002.json").write_text('{"severity": "SEV-2"}')
        (incidents_dir / "INC-003.json").write_text('{"severity": "SEV-2"}')

        result = framework.validate_incident_response("owner", "repo")

        assert result.passed is True
        assert result.metrics.get("total_incidents") == 3
        dist = result.metrics.get("severity_distribution")
        assert dist["SEV-1"] == 1
        assert dist["SEV-2"] == 2


class TestValidateAll:
    """Test validate_all method."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_runs_all_validations(self, framework):
        """Test runs all 7 validations."""
        # Mock all validation methods to return passed results
        for capability in [
            "auto_merge",
            "routing",
            "self_healing",
            "maintenance",
            "analytics",
            "sla",
            "incident_response",
        ]:
            method = f"validate_{capability}"
            setattr(
                framework,
                method,
                MagicMock(
                    return_value=ValidationResult(
                        capability=capability.replace("_", "-"),
                        started_at=datetime.now(timezone.utc),
                        passed=True,
                        message="Passed",
                    )
                ),
            )

        # Mock save and notification methods
        framework._save_validation_suite = MagicMock()
        framework._send_validation_notification = MagicMock()

        suite = framework.validate_all("owner", "repo")

        assert len(suite.results) == 7
        assert suite.passed == 7
        assert suite.failed == 0
        assert framework._save_validation_suite.called
        assert framework._send_validation_notification.called

    def test_counts_failures_correctly(self, framework):
        """Test counts failures correctly in suite."""
        # Mock 4 pass, 3 fail
        results = []
        for i, capability in enumerate(
            [
                "auto-merge",
                "routing",
                "self-healing",
                "maintenance",
                "analytics",
                "sla",
                "incident-response",
            ]
        ):
            results.append(
                ValidationResult(
                    capability=capability,
                    started_at=datetime.now(timezone.utc),
                    passed=i < 4,  # First 4 pass
                    message="Test",
                )
            )

        framework.validate_auto_merge = MagicMock(return_value=results[0])
        framework.validate_routing = MagicMock(return_value=results[1])
        framework.validate_self_healing = MagicMock(return_value=results[2])
        framework.validate_maintenance = MagicMock(return_value=results[3])
        framework.validate_analytics = MagicMock(return_value=results[4])
        framework.validate_sla = MagicMock(return_value=results[5])
        framework.validate_incident_response = MagicMock(return_value=results[6])
        framework._save_validation_suite = MagicMock()
        framework._send_validation_notification = MagicMock()

        suite = framework.validate_all("owner", "repo")

        assert suite.passed == 4
        assert suite.failed == 3


class TestReportGeneration:
    """Test report generation."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_generates_report_from_files(self, framework, tmp_path):
        """Test generates report from validation files."""
        validation_dir = tmp_path / ".github" / "validation"
        validation_dir.mkdir(parents=True, exist_ok=True)
        framework.validation_dir = validation_dir

        # Create validation files
        recent = datetime.now(timezone.utc)
        validation_data = {
            "started_at": recent.isoformat(),
            "repository": "owner/repo",
            "results": [
                {"capability": "auto-merge", "passed": True},
                {"capability": "routing", "passed": False},
            ],
        }

        (validation_dir / "validation_20240101_120000.json").write_text(json.dumps(validation_data))

        report = framework.generate_report("owner", "repo", days=30)

        assert report["repository"] == "owner/repo"
        assert report["total_validations"] >= 1

    def test_empty_report_when_no_files(self, framework, tmp_path):
        """Test generates empty report when no validation files."""
        validation_dir = tmp_path / ".github" / "validation"
        validation_dir.mkdir(parents=True, exist_ok=True)
        framework.validation_dir = validation_dir

        report = framework.generate_report("owner", "repo", days=7)

        assert report["total_validations"] == 0
        assert report["capabilities"] == {}


@pytest.mark.unit
class TestValidationFrameworkInit:
    """Test ValidationFramework initialization."""

    def test_init_creates_validation_dir(self, tmp_path):
        """Test __init__ creates validation directory."""
        mock_client = MagicMock()

        with patch("validation_framework.Path") as mock_path_class:
            mock_dir = MagicMock()
            mock_path_class.return_value = mock_dir

            fw = ValidationFramework(mock_client)

            assert fw.github == mock_client
            assert fw.results == []
            mock_dir.mkdir.assert_called_with(parents=True, exist_ok=True)


@pytest.mark.unit
class TestValidationExceptionHandling:
    """Test exception handling in validation methods."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_routing_exception_handling(self, framework):
        """Test routing validation handles exceptions."""
        config_path = Path(".github/routing.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        framework.github.get.side_effect = Exception("API Error")

        result = framework.validate_routing("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

        config_path.unlink()

    def test_self_healing_config_missing(self, framework):
        """Test self-healing validation fails when config missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_self_healing("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_self_healing_exception_handling(self, framework):
        """Test self-healing validation handles exceptions."""
        config_path = Path(".github/self-healing.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        framework.github.get.side_effect = Exception("API Error")

        result = framework.validate_self_healing("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

        config_path.unlink()

    def test_maintenance_config_missing(self, framework):
        """Test maintenance validation fails when config missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_maintenance("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_maintenance_exception_handling(self, framework):
        """Test maintenance validation handles exceptions."""
        # Use side_effect to have config_path.exists() return True first,
        # then raise an exception on tasks_dir operations
        call_count = [0]

        def mock_exists(self):
            call_count[0] += 1
            if call_count[0] == 1:
                return True  # Config file exists
            raise Exception("IO Error")  # Tasks dir check raises

        with patch.object(Path, "exists", mock_exists):
            result = framework.validate_maintenance("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

    def test_analytics_config_missing(self, framework):
        """Test analytics validation fails when config missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_analytics("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_analytics_exception_handling(self, framework):
        """Test analytics validation handles exceptions."""
        # Use side_effect to have config_path.exists() return True first,
        # then raise an exception on models_dir operations
        call_count = [0]

        def mock_exists(self):
            call_count[0] += 1
            if call_count[0] == 1:
                return True  # Config file exists
            raise Exception("IO Error")  # Models dir check raises

        with patch.object(Path, "exists", mock_exists):
            result = framework.validate_analytics("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

    def test_sla_config_missing(self, framework):
        """Test SLA validation fails when config missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_sla("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_sla_exception_handling(self, framework):
        """Test SLA validation handles exceptions."""
        config_path = Path(".github/sla.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        framework.github.get.side_effect = Exception("API Error")

        result = framework.validate_sla("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

        config_path.unlink()

    def test_incident_response_config_missing(self, framework):
        """Test incident response validation fails when config missing."""
        with patch("pathlib.Path.exists", return_value=False):
            result = framework.validate_incident_response("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_incident_response_exception_handling(self, framework, tmp_path, monkeypatch):
        """Test incident response validation handles exceptions."""
        # Use temp directory to avoid conflicts with existing files
        monkeypatch.chdir(tmp_path)

        config_path = Path(".github/incident.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        incidents_dir = Path(".github/incidents")
        incidents_dir.mkdir(parents=True, exist_ok=True)
        # Create a malformed JSON file to trigger exception
        (incidents_dir / "INC-001.json").write_text("{invalid json}")

        result = framework.validate_incident_response("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)


@pytest.mark.unit
class TestSaveValidationSuite:
    """Test _save_validation_suite method."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_saves_suite_to_json_file(self, framework, tmp_path):
        """Test saves validation suite to JSON file."""
        from models import ValidationSuite

        suite = ValidationSuite(
            started_at=datetime.now(timezone.utc),
            repository="owner/repo",
        )
        suite.passed = 5
        suite.failed = 2
        suite.warnings = 1
        suite.completed_at = datetime.now(timezone.utc)
        suite.duration_seconds = 10.5

        framework._save_validation_suite(suite)

        # Check file was created
        files = list(framework.validation_dir.glob("validation_*.json"))
        assert len(files) == 1

        # Verify content
        with open(files[0]) as f:
            data = json.load(f)
            assert data["repository"] == "owner/repo"
            assert data["passed"] == 5
            assert data["failed"] == 2


@pytest.mark.unit
class TestSendValidationNotification:
    """Test _send_validation_notification method."""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_sends_success_notification_when_all_pass(self, framework):
        """Test sends success notification when all validations pass."""
        from models import ValidationSuite

        suite = ValidationSuite(
            started_at=datetime.now(timezone.utc),
            repository="owner/repo",
        )
        suite.passed = 7
        suite.failed = 0
        suite.warnings = 0
        suite.completed_at = datetime.now(timezone.utc)
        suite.duration_seconds = 10.5
        suite.results = [
            ValidationResult(
                capability="auto-merge",
                started_at=datetime.now(timezone.utc),
                passed=True,
            )
        ]

        with (
            patch("validation_framework.notify_validation_success") as mock_success,
            patch("validation_framework.notify_validation_failure") as mock_failure,
        ):
            framework._send_validation_notification(suite)

            mock_success.assert_called_once()
            mock_failure.assert_not_called()

    def test_sends_failure_notification_for_each_failed(self, framework):
        """Test sends failure notification for each failed capability."""
        from models import ValidationSuite

        suite = ValidationSuite(
            started_at=datetime.now(timezone.utc),
            repository="owner/repo",
        )
        suite.passed = 5
        suite.failed = 2
        suite.warnings = 1
        suite.completed_at = datetime.now(timezone.utc)
        suite.duration_seconds = 10.5
        suite.results = [
            ValidationResult(
                capability="auto-merge",
                started_at=datetime.now(timezone.utc),
                passed=False,
                errors=["Config missing"],
            ),
            ValidationResult(
                capability="routing",
                started_at=datetime.now(timezone.utc),
                passed=True,
            ),
            ValidationResult(
                capability="self-healing",
                started_at=datetime.now(timezone.utc),
                passed=False,
                errors=["API Error"],
            ),
        ]

        with (
            patch("validation_framework.notify_validation_success") as mock_success,
            patch("validation_framework.notify_validation_failure") as mock_failure,
        ):
            framework._send_validation_notification(suite)

            # Should be called twice for the two failed capabilities
            assert mock_failure.call_count == 2
            mock_success.assert_not_called()


@pytest.mark.unit
class TestMainCLI:
    """Test main CLI entry point."""

    @pytest.fixture
    def mock_github(self):
        with patch("validation_framework.GitHubAPIClient") as mock:
            yield mock.return_value

    def test_validate_all_cli(self, mock_github, tmp_path, capsys):
        """Test --validate-all CLI option."""
        from models import ValidationSuite

        with patch("sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo", "--validate-all"]):
            with patch.object(ValidationFramework, "validate_all") as mock_validate:
                suite = ValidationSuite(
                    started_at=datetime.now(timezone.utc),
                    repository="org/repo",
                )
                suite.passed = 7
                suite.failed = 0
                suite.warnings = 0
                suite.results = []
                mock_validate.return_value = suite

                from validation_framework import main

                main()

                captured = capsys.readouterr()
                assert "Validation Complete" in captured.out
                assert "Passed: 7/7" in captured.out

    def test_validate_all_with_failures(self, mock_github, capsys):
        """Test --validate-all with failures shows failed capabilities."""
        from models import ValidationSuite

        with patch("sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo", "--validate-all"]):
            with patch.object(ValidationFramework, "validate_all") as mock_validate:
                suite = ValidationSuite(
                    started_at=datetime.now(timezone.utc),
                    repository="org/repo",
                )
                suite.passed = 5
                suite.failed = 2
                suite.warnings = 0
                suite.results = [
                    ValidationResult(
                        capability="auto-merge",
                        started_at=datetime.now(timezone.utc),
                        passed=False,
                        errors=["Config missing"],
                    ),
                ]
                mock_validate.return_value = suite

                from validation_framework import main

                main()

                captured = capsys.readouterr()
                assert "Failed Capabilities" in captured.out
                assert "auto-merge" in captured.out
                assert "Config missing" in captured.out

    def test_validate_single_capability(self, mock_github, capsys):
        """Test --validate single capability."""
        with patch(
            "sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo", "--validate", "routing"]
        ):
            with patch.object(ValidationFramework, "validate_routing") as mock_validate:
                mock_validate.return_value = ValidationResult(
                    capability="routing",
                    started_at=datetime.now(timezone.utc),
                    passed=True,
                    message="Routing validation passed",
                )

                from validation_framework import main

                main()

                captured = capsys.readouterr()
                assert "routing" in captured.out
                assert "Routing validation passed" in captured.out

    def test_validate_single_with_errors(self, mock_github, capsys):
        """Test --validate single capability with errors."""
        with patch("sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo", "--validate", "sla"]):
            with patch.object(ValidationFramework, "validate_sla") as mock_validate:
                mock_validate.return_value = ValidationResult(
                    capability="sla",
                    started_at=datetime.now(timezone.utc),
                    passed=False,
                    message="SLA validation failed",
                    errors=["API Error"],
                    warnings=["Low sample size"],
                )

                from validation_framework import main

                main()

                captured = capsys.readouterr()
                assert "sla" in captured.out
                assert "Error: API Error" in captured.out
                assert "Warning: Low sample size" in captured.out

    def test_report_cli(self, mock_github, capsys):
        """Test --report CLI option."""
        with patch(
            "sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo", "--report", "--days", "14"]
        ):
            with patch.object(ValidationFramework, "generate_report") as mock_report:
                mock_report.return_value = {
                    "repository": "org/repo",
                    "total_validations": 10,
                    "capabilities": {
                        "auto-merge": {"success_rate": 0.9},
                        "routing": {"success_rate": 0.85},
                    },
                }

                from validation_framework import main

                main()

                captured = capsys.readouterr()
                assert "Validation Report" in captured.out
                assert "14 days" in captured.out
                assert "org/repo" in captured.out
                assert "auto-merge: 90.0%" in captured.out

    def test_no_args_prints_help(self, mock_github, capsys):
        """Test no arguments prints help."""
        with patch("sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo"]):
            with patch("argparse.ArgumentParser.print_help") as mock_help:
                from validation_framework import main

                main()

                mock_help.assert_called_once()

    def test_debug_flag_sets_debug_logging(self, mock_github):
        """Test --debug flag enables debug logging."""
        import logging

        with patch("sys.argv", ["validation_framework.py", "--owner", "org", "--repo", "repo", "--debug", "--report"]):
            with patch.object(ValidationFramework, "generate_report") as mock_report:
                mock_report.return_value = {
                    "repository": "org/repo",
                    "total_validations": 0,
                    "capabilities": {},
                }

                from validation_framework import main

                main()

                # Check that debug logging was enabled
                assert logging.getLogger().level == logging.DEBUG

                # Reset logging level
                logging.getLogger().setLevel(logging.INFO)
