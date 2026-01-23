#!/usr/bin/env python3
"""
Unit tests for automation/scripts/validation_framework.py
Focus: ValidationFramework class, capability validations, report generation
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))

# Mock notification_integration before importing validation_framework
sys.modules["notification_integration"] = MagicMock()

from models import ValidationResult, ValidationSuite
from validation_framework import ValidationFramework


class TestValidationFramework:
    """Test ValidationFramework class"""

    @pytest.fixture
    def mock_github_client(self):
        """Create mock GitHub client"""
        client = MagicMock()
        return client

    @pytest.fixture
    def framework(self, mock_github_client, tmp_path):
        """Create ValidationFramework instance"""
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
    """Test auto-merge validation"""

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
        """Test validation fails when config file is missing"""
        result = framework.validate_auto_merge("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_passes_with_config_and_prs(self, framework, mock_client, tmp_path):
        """Test validation passes with config and merged PRs"""
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
        """Test warns when no merged PRs found"""
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
        """Test handles API error gracefully"""
        config_path = Path(".github/auto-merge.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("enabled: true")

        mock_client.get.side_effect = Exception("API Error")

        result = framework.validate_auto_merge("owner", "repo")

        assert result.passed is False
        assert any("Validation failed" in e for e in result.errors)

        config_path.unlink()


class TestRoutingValidation:
    """Test intelligent routing validation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_fails_when_config_missing(self, framework):
        """Test validation fails when config file is missing"""
        result = framework.validate_routing("owner", "repo")

        assert result.passed is False
        assert "Configuration file not found" in result.errors

    def test_passes_with_assigned_prs(self, framework):
        """Test validation passes with assigned PRs"""
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
    """Test self-healing validation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_calculates_failure_rate(self, framework):
        """Test calculates failure rate from workflow runs"""
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
    """Test maintenance validation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_counts_scheduled_tasks(self, framework):
        """Test counts scheduled maintenance tasks"""
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
    """Test analytics ML validation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_counts_trained_models(self, framework):
        """Test counts trained ML models"""
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
    """Test SLA monitoring validation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_counts_issues(self, framework):
        """Test counts issues for SLA analysis"""
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
    """Test incident response validation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_analyzes_incident_severity(self, framework):
        """Test analyzes incident severity distribution"""
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

        # Cleanup
        for f in incidents_dir.glob("*.json"):
            f.unlink()
        incidents_dir.rmdir()
        config_path.unlink()


class TestValidateAll:
    """Test validate_all method"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_runs_all_validations(self, framework):
        """Test runs all 7 validations"""
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
        """Test counts failures correctly in suite"""
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
    """Test report generation"""

    @pytest.fixture
    def framework(self, tmp_path):
        fw = ValidationFramework.__new__(ValidationFramework)
        fw.github = MagicMock()
        fw.results = []
        fw.validation_dir = tmp_path / ".github" / "validation"
        fw.validation_dir.mkdir(parents=True, exist_ok=True)
        return fw

    def test_generates_report_from_files(self, framework, tmp_path):
        """Test generates report from validation files"""
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

        (validation_dir / "validation_20240101_120000.json").write_text(
            json.dumps(validation_data)
        )

        report = framework.generate_report("owner", "repo", days=30)

        assert report["repository"] == "owner/repo"
        assert report["total_validations"] >= 1

    def test_empty_report_when_no_files(self, framework, tmp_path):
        """Test generates empty report when no validation files"""
        validation_dir = tmp_path / ".github" / "validation"
        validation_dir.mkdir(parents=True, exist_ok=True)
        framework.validation_dir = validation_dir

        report = framework.generate_report("owner", "repo", days=7)

        assert report["total_validations"] == 0
        assert report["capabilities"] == {}
