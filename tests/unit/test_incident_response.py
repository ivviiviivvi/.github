#!/usr/bin/env python3
"""
Unit tests for automation/scripts/incident_response.py
Focus: Incident creation, severity classification, runbook execution, status updates
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))

# Mock notification_integration before importing incident_response
sys.modules["notification_integration"] = MagicMock()

from incident_response import IncidentResponseEngine
from models import (
    Incident,
    IncidentConfig,
    IncidentSeverity,
    IncidentStatus,
    RunbookStep,
)


class TestIncidentResponseEngine:
    """Test IncidentResponseEngine class"""

    @pytest.fixture
    def mock_github(self):
        """Create mock GitHub client"""
        return MagicMock()

    @pytest.fixture
    def config(self):
        """Create test config"""
        return IncidentConfig(
            enabled=True,
            create_github_issues=True,
            auto_execute_runbooks=True,
        )

    @pytest.fixture
    def engine(self, mock_github, config, tmp_path):
        """Create engine with temporary directories"""
        engine = IncidentResponseEngine(config, mock_github)
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        engine.runbooks_dir = tmp_path / "runbooks"
        engine.runbooks_dir.mkdir(parents=True, exist_ok=True)
        return engine

    def test_initialization(self, mock_github, config, tmp_path):
        """Test engine initializes correctly"""
        with patch.object(Path, "mkdir"):
            engine = IncidentResponseEngine(config, mock_github)

        assert engine.config == config
        assert engine.github == mock_github


class TestSeverityClassification:
    """Test incident severity classification"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig()
        engine = IncidentResponseEngine(config, MagicMock())
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    def test_sev1_production_down(self, engine):
        """Test SEV-1 classification for production down"""
        severity = engine._classify_severity(
            "Production API Down", "All users affected by outage", "manual"
        )
        assert severity == IncidentSeverity.SEV1

    def test_sev1_security_breach(self, engine):
        """Test SEV-1 classification for security breach"""
        severity = engine._classify_severity(
            "Security Breach Detected", "Unauthorized access to data", "manual"
        )
        assert severity == IncidentSeverity.SEV1

    def test_sev1_data_loss(self, engine):
        """Test SEV-1 classification for data loss"""
        severity = engine._classify_severity(
            "Database Corruption", "Critical data loss detected", "manual"
        )
        assert severity == IncidentSeverity.SEV1

    def test_sev2_major_failure(self, engine):
        """Test SEV-2 classification for major failure"""
        severity = engine._classify_severity(
            "Major Feature Broken", "Main feature affecting multiple users", "manual"
        )
        assert severity == IncidentSeverity.SEV2

    def test_sev2_from_sla_breach(self, engine):
        """Test SEV-2 classification from SLA breach source"""
        severity = engine._classify_severity(
            "Response Time SLA Breach",
            "Issue response exceeded threshold",
            "sla_breach",
        )
        assert severity == IncidentSeverity.SEV2

    def test_sev3_minor_issue(self, engine):
        """Test SEV-3 classification for minor issue"""
        severity = engine._classify_severity(
            "Minor Bug", "Minor issue with workaround available", "manual"
        )
        assert severity == IncidentSeverity.SEV3

    def test_sev3_from_workflow(self, engine):
        """Test SEV-3 classification from workflow source"""
        severity = engine._classify_severity(
            "Build Failed", "CI pipeline test failure", "workflow"
        )
        assert severity == IncidentSeverity.SEV3

    def test_sev4_default(self, engine):
        """Test SEV-4 as default classification"""
        severity = engine._classify_severity(
            "Cosmetic Issue", "Button color is wrong", "manual"
        )
        assert severity == IncidentSeverity.SEV4


class TestRunbookExecution:
    """Test runbook execution"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig()
        github = MagicMock()
        engine = IncidentResponseEngine(config, github)
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    def test_sev1_runbook_steps(self, engine):
        """Test SEV-1 runbook has correct steps"""
        runbook = engine._get_runbook(IncidentSeverity.SEV1)

        assert len(runbook) == 3
        assert runbook[0].action == "notify"
        assert runbook[0].params.get("priority") == "critical"
        assert runbook[1].action == "create_issue"
        assert "war-room" in runbook[1].params.get("labels", [])

    def test_sev2_runbook_steps(self, engine):
        """Test SEV-2 runbook has correct steps"""
        runbook = engine._get_runbook(IncidentSeverity.SEV2)

        assert len(runbook) == 2
        assert runbook[0].action == "notify"
        assert runbook[0].params.get("priority") == "high"

    def test_sev3_runbook_steps(self, engine):
        """Test SEV-3 runbook has correct steps"""
        runbook = engine._get_runbook(IncidentSeverity.SEV3)

        assert len(runbook) == 1
        assert runbook[0].action == "notify"
        assert runbook[0].params.get("priority") == "normal"

    def test_sev4_runbook_steps(self, engine):
        """Test SEV-4 runbook has correct steps"""
        runbook = engine._get_runbook(IncidentSeverity.SEV4)

        assert len(runbook) == 1
        assert runbook[0].action == "update_status"

    def test_runbook_execution_marks_steps_completed(self, engine):
        """Test runbook execution marks steps as completed"""
        incident = Incident(
            incident_id="INC-001",
            title="Test Incident",
            description="Test",
            severity=IncidentSeverity.SEV4,
            status=IncidentStatus.OPEN,
            source="manual",
            repository="owner/repo",
            created_at=datetime.now(timezone.utc),
        )

        with patch.object(engine, "_save_incident"):
            steps = engine._execute_runbook(incident)

        assert len(steps) == 1
        assert steps[0].executed is True
        assert steps[0].executed_at is not None

    def test_runbook_handles_step_failure(self, engine):
        """Test runbook handles step failure gracefully"""
        incident = Incident(
            incident_id="INC-001",
            title="Test Incident",
            description="Test",
            severity=IncidentSeverity.SEV2,
            status=IncidentStatus.OPEN,
            source="manual",
            repository="owner/repo",
            created_at=datetime.now(timezone.utc),
        )

        # Mock notification to fail - the runbook continues with subsequent steps
        # Only successful steps are returned in the executed_steps list
        with patch.object(
            engine,
            "_execute_notify_action",
            side_effect=Exception("Notification failed"),
        ):
            with patch.object(engine, "_save_incident"):
                steps = engine._execute_runbook(incident)

        # Failed notify step is not included in returned steps
        # Only successful steps (like create_issue) are returned
        # SEV2 runbook has 2 steps: notify (fails) then create_issue (succeeds)
        assert len(steps) == 1
        assert steps[0].name == "Create tracking issue"
        assert steps[0].executed is True


class TestIncidentCreation:
    """Test incident creation"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig(
            create_github_issues=False,  # Disable for simpler tests
            auto_execute_runbooks=False,
        )
        github = MagicMock()
        engine = IncidentResponseEngine(config, github)
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    def test_creates_incident_with_id(self, engine):
        """Test creates incident with unique ID"""
        with patch.object(engine, "_send_incident_notification"):
            incident = engine.create_incident(
                "owner", "repo", "Test Incident", "Test description", "manual"
            )

        assert incident.incident_id.startswith("INC-")
        assert incident.title == "Test Incident"
        assert incident.repository == "owner/repo"

    def test_creates_incident_with_correct_severity(self, engine):
        """Test creates incident with classified severity"""
        with patch.object(engine, "_send_incident_notification"):
            incident = engine.create_incident(
                "owner", "repo", "Production Outage", "All users affected", "manual"
            )

        assert incident.severity == IncidentSeverity.SEV1

    def test_creates_incident_with_open_status(self, engine):
        """Test creates incident with OPEN status"""
        with patch.object(engine, "_send_incident_notification"):
            incident = engine.create_incident("owner", "repo", "Test", "Test", "manual")

        assert incident.status == IncidentStatus.OPEN

    def test_saves_incident_to_disk(self, engine, tmp_path):
        """Test saves incident to disk"""
        with patch.object(engine, "_send_incident_notification"):
            incident = engine.create_incident("owner", "repo", "Test", "Test", "manual")

        incident_file = engine.incidents_dir / f"{incident.incident_id}.json"
        assert incident_file.exists()

        with open(incident_file) as f:
            data = json.load(f)
        assert data["title"] == "Test"

    def test_creates_github_issue_when_enabled(self, tmp_path):
        """Test creates GitHub issue when configured"""
        config = IncidentConfig(
            create_github_issues=True,
            auto_execute_runbooks=False,
        )
        github = MagicMock()
        github.post.return_value = {"number": 42}

        engine = IncidentResponseEngine(config, github)
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)

        with patch.object(engine, "_send_incident_notification"):
            incident = engine.create_incident("owner", "repo", "Test", "Test", "manual")

        assert incident.github_issue_number == 42
        github.post.assert_called()


class TestStatusUpdates:
    """Test incident status updates"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig()
        engine = IncidentResponseEngine(config, MagicMock())
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    @pytest.fixture
    def existing_incident(self, engine):
        """Create existing incident for updates"""
        incident = Incident(
            incident_id="INC-TEST-001",
            title="Test Incident",
            description="Test",
            severity=IncidentSeverity.SEV3,
            status=IncidentStatus.OPEN,
            source="manual",
            repository="owner/repo",
            created_at=datetime.now(timezone.utc) - timedelta(hours=2),
        )
        engine._save_incident(incident)
        return incident

    def test_updates_status(self, engine, existing_incident):
        """Test updates incident status"""
        with patch.object(engine, "_send_incident_notification"):
            updated = engine.update_incident_status(
                existing_incident.incident_id,
                IncidentStatus.INVESTIGATING,
            )

        assert updated.status == IncidentStatus.INVESTIGATING

    def test_resolved_sets_timestamp(self, engine, existing_incident):
        """Test resolved status sets timestamp"""
        with patch.object(engine, "_send_incident_notification"):
            updated = engine.update_incident_status(
                existing_incident.incident_id,
                IncidentStatus.RESOLVED,
                "Fixed the issue",
            )

        assert updated.status == IncidentStatus.RESOLVED
        assert updated.resolved_at is not None
        assert updated.resolution == "Fixed the issue"

    def test_resolved_calculates_ttr(self, engine, existing_incident):
        """Test resolved status calculates time to resolution"""
        with patch.object(engine, "_send_incident_notification"):
            updated = engine.update_incident_status(
                existing_incident.incident_id,
                IncidentStatus.RESOLVED,
            )

        # TTR should be approximately 2 hours (120 minutes)
        assert updated.time_to_resolution_minutes is not None
        assert updated.time_to_resolution_minutes >= 119  # Allow some tolerance


class TestPostIncidentReport:
    """Test post-incident report generation"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig()
        engine = IncidentResponseEngine(config, MagicMock())
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    @pytest.fixture
    def resolved_incident(self, engine):
        """Create resolved incident for report"""
        incident = Incident(
            incident_id="INC-REPORT-001",
            title="Test Incident",
            description="Test",
            severity=IncidentSeverity.SEV2,
            status=IncidentStatus.RESOLVED,
            source="workflow",
            repository="owner/repo",
            created_at=datetime.now(timezone.utc) - timedelta(hours=5),
            resolved_at=datetime.now(timezone.utc),
            resolution="Fixed",
            time_to_resolution_minutes=300,
        )
        engine._save_incident(incident)
        return incident

    def test_generates_report(self, engine, resolved_incident):
        """Test generates post-incident report"""
        report = engine.generate_post_incident_report(resolved_incident.incident_id)

        assert report.incident_id == resolved_incident.incident_id
        assert report.incident is not None
        assert report.generated_at is not None

    def test_report_includes_timeline(self, engine, resolved_incident):
        """Test report includes timeline"""
        report = engine.generate_post_incident_report(resolved_incident.incident_id)

        assert len(report.timeline) >= 2  # At least created and resolved
        assert report.timeline[0]["event"] == "Incident created"

    def test_report_includes_root_cause(self, engine, resolved_incident):
        """Test report includes root cause analysis"""
        report = engine.generate_post_incident_report(resolved_incident.incident_id)

        assert report.root_cause is not None
        assert len(report.root_cause) > 0

    def test_report_includes_action_items(self, engine, resolved_incident):
        """Test report includes action items"""
        report = engine.generate_post_incident_report(resolved_incident.incident_id)

        assert len(report.action_items) >= 1
        # High severity should have monitoring action
        assert any(
            "monitoring" in item["action"].lower() for item in report.action_items
        )

    def test_report_includes_lessons_learned(self, engine, resolved_incident):
        """Test report includes lessons learned"""
        report = engine.generate_post_incident_report(resolved_incident.incident_id)

        assert len(report.lessons_learned) >= 1

    def test_saves_report_to_disk(self, engine, resolved_incident):
        """Test saves report to disk"""
        report = engine.generate_post_incident_report(resolved_incident.incident_id)

        report_file = engine.incidents_dir / f"{report.incident_id}_report.json"
        assert report_file.exists()


class TestNotificationChannels:
    """Test notification channel selection"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig()
        engine = IncidentResponseEngine(config, MagicMock())
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    def test_sev1_uses_all_channels(self, engine):
        """Test SEV-1 uses all notification channels"""
        channels = engine._get_notification_channels(IncidentSeverity.SEV1)

        assert "slack" in channels
        assert "pagerduty" in channels
        assert "email" in channels

    def test_sev2_uses_slack_and_email(self, engine):
        """Test SEV-2 uses Slack and email"""
        channels = engine._get_notification_channels(IncidentSeverity.SEV2)

        assert "slack" in channels
        assert "email" in channels
        assert "pagerduty" not in channels

    def test_sev3_uses_slack_only(self, engine):
        """Test SEV-3 uses Slack only"""
        channels = engine._get_notification_channels(IncidentSeverity.SEV3)

        assert channels == ["slack"]

    def test_sev4_uses_no_channels(self, engine):
        """Test SEV-4 uses no notification channels"""
        channels = engine._get_notification_channels(IncidentSeverity.SEV4)

        assert channels == []


class TestIncidentIdGeneration:
    """Test incident ID generation"""

    @pytest.fixture
    def engine(self, tmp_path):
        config = IncidentConfig()
        engine = IncidentResponseEngine(config, MagicMock())
        engine.incidents_dir = tmp_path / "incidents"
        engine.incidents_dir.mkdir(parents=True, exist_ok=True)
        return engine

    def test_generates_unique_ids(self, engine):
        """Test generates unique incident IDs"""
        id1 = engine._generate_incident_id()
        # Create a file to simulate existing incident
        (engine.incidents_dir / f"{id1}.json").write_text("{}")
        id2 = engine._generate_incident_id()

        assert id1 != id2
        assert id1.startswith("INC-")
        assert id2.startswith("INC-")

    def test_id_includes_date(self, engine):
        """Test ID includes current date"""
        incident_id = engine._generate_incident_id()

        today = datetime.now().strftime("%Y%m%d")
        assert today in incident_id

    def test_id_increments_sequence(self, engine):
        """Test ID sequence number increments"""
        # Create some existing incidents
        today = datetime.now().strftime("%Y%m%d")
        (engine.incidents_dir / f"INC-{today}-001.json").write_text("{}")
        (engine.incidents_dir / f"INC-{today}-002.json").write_text("{}")

        new_id = engine._generate_incident_id()

        assert new_id.endswith("-003")
