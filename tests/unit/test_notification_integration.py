"""Tests for notification_integration.py.

Tests the backward-compatible notification wrapper that integrates
with the unified notification manager.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "src/automation/scripts")

from src.automation.scripts import notification_integration


@pytest.mark.unit
class TestGetNotificationManager:
    """Test global notification manager retrieval."""

    def test_get_notification_manager_creates_instance(self):
        """Test get_notification_manager creates instance on first call."""
        # Reset global
        notification_integration._notification_manager = None

        with patch.object(
            notification_integration,
            "NotificationManager",
        ) as MockManager:
            mock_instance = MagicMock()
            MockManager.return_value = mock_instance

            result = notification_integration.get_notification_manager()

            MockManager.assert_called_once()
            assert result == mock_instance

    def test_get_notification_manager_returns_cached(self):
        """Test get_notification_manager returns cached instance."""
        mock_manager = MagicMock()
        notification_integration._notification_manager = mock_manager

        result = notification_integration.get_notification_manager()

        assert result == mock_manager

        # Clean up
        notification_integration._notification_manager = None


@pytest.mark.unit
class TestSendNotification:
    """Test legacy send_notification function."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_basic(self, MockManager):
        """Test basic notification sending."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification("slack", "Test message")

        mock_instance.send.assert_called_once()
        call_args = mock_instance.send.call_args
        notification = call_args.args[0]
        assert notification.message == "Test message"
        assert "slack" in notification.channels

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_with_title(self, MockManager):
        """Test notification with custom title."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification(
            "email",
            "Message body",
            title="Custom Title",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.title == "Custom Title"

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_with_priority(self, MockManager):
        """Test notification with priority mapping."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification(
            "pagerduty",
            "Critical issue",
            priority="CRITICAL",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.CRITICAL

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_priority_case_insensitive(self, MockManager):
        """Test priority mapping is case insensitive."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification(
            "slack",
            "High priority",
            priority="high",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.HIGH

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_unknown_priority_defaults_medium(self, MockManager):
        """Test unknown priority defaults to MEDIUM."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification(
            "slack",
            "Message",
            priority="UNKNOWN",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_with_metadata(self, MockManager):
        """Test notification with metadata."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification(
            "slack",
            "Message",
            metadata={"key": "value"},
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.metadata == {"key": "value"}

    @patch.object(notification_integration, "NotificationManager")
    def test_send_notification_empty_channel(self, MockManager):
        """Test notification with empty channel."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.send_notification("", "Message")

        notification = mock_instance.send.call_args.args[0]
        assert notification.channels == []


@pytest.mark.unit
class TestNotifySLABreach:
    """Test SLA breach notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_sla_breach_p0(self, MockManager):
        """Test P0 SLA breach notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_sla_breach(
            item_type="issue",
            item_number="123",
            repository="owner/repo",
            breach_type="response_time",
            threshold="4h",
            actual="8h",
            priority="P0",
        )

        mock_instance.send.assert_called_once()
        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.CRITICAL
        assert "SLA Breach" in notification.title
        assert "P0" in notification.title
        assert notification.source == "sla-monitor"

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_sla_breach_p1(self, MockManager):
        """Test P1 SLA breach notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_sla_breach(
            item_type="pr",
            item_number="456",
            repository="owner/repo",
            breach_type="resolution_time",
            threshold="24h",
            actual="48h",
            priority="P1",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.HIGH

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_sla_breach_with_metadata(self, MockManager):
        """Test SLA breach with additional metadata."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_sla_breach(
            item_type="workflow",
            item_number="789",
            repository="owner/repo",
            breach_type="success_rate",
            threshold="95%",
            actual="80%",
            priority="P2",
            metadata={"workflow_name": "CI"},
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.metadata["workflow_name"] == "CI"
        assert notification.metadata["item_type"] == "workflow"


@pytest.mark.unit
class TestNotifySLACompliance:
    """Test SLA compliance notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_sla_compliance_below_90(self, MockManager):
        """Test compliance notification when below 90%."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_sla_compliance(
            repository="owner/repo",
            compliance_rate=0.85,
            period_days=30,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.HIGH

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_sla_compliance_below_95(self, MockManager):
        """Test compliance notification when below 95%."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_sla_compliance(
            repository="owner/repo",
            compliance_rate=0.92,
            period_days=7,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_sla_compliance_above_95(self, MockManager):
        """Test compliance notification when above 95%."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_sla_compliance(
            repository="owner/repo",
            compliance_rate=0.98,
            period_days=14,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.LOW


@pytest.mark.unit
class TestNotifyIncidentCreated:
    """Test incident creation notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_incident_created_sev1(self, MockManager):
        """Test SEV-1 incident notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_incident_created(
            incident_id="INC-001",
            severity="SEV-1",
            repository="owner/repo",
            description="Critical outage",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.CRITICAL
        assert "SEV-1" in notification.title
        assert notification.source == "incident-response"

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_incident_created_with_status(self, MockManager):
        """Test incident notification with custom status."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_incident_created(
            incident_id="INC-002",
            severity="SEV-2",
            repository="owner/repo",
            description="Degraded performance",
            status="INVESTIGATING",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.metadata["status"] == "INVESTIGATING"

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_incident_created_unknown_severity(self, MockManager):
        """Test incident with unknown severity defaults to MEDIUM."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_incident_created(
            incident_id="INC-003",
            severity="UNKNOWN",
            repository="owner/repo",
            description="Unknown severity issue",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM


@pytest.mark.unit
class TestNotifyIncidentResolved:
    """Test incident resolution notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_incident_resolved(self, MockManager):
        """Test incident resolved notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_incident_resolved(
            incident_id="INC-001",
            severity="SEV-1",
            duration_minutes=120,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.LOW
        assert "Resolved" in notification.title
        assert notification.metadata["duration_minutes"] == 120


@pytest.mark.unit
class TestNotifyValidationFailure:
    """Test validation failure notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_validation_failure(self, MockManager):
        """Test validation failure notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_validation_failure(
            capability="code-scanning",
            repository="owner/repo",
            errors=["Missing config", "Invalid schema"],
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM
        assert "Validation Failed" in notification.title
        assert notification.source == "validation-framework"
        assert notification.metadata["error_count"] == 2

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_validation_failure_with_warnings(self, MockManager):
        """Test validation failure with warnings."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_validation_failure(
            capability="dependency-review",
            repository="owner/repo",
            errors=["Error 1"],
            warnings=["Warning 1", "Warning 2"],
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.metadata["warning_count"] == 2


@pytest.mark.unit
class TestNotifyValidationSuccess:
    """Test validation success notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_validation_success(self, MockManager):
        """Test validation success notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_validation_success(
            repository="owner/repo",
            passed_count=10,
            total_count=10,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.LOW
        assert "10/10" in notification.title


@pytest.mark.unit
class TestNotifySelfHealingSuccess:
    """Test self-healing success notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_self_healing_success(self, MockManager):
        """Test self-healing success notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_self_healing_success(
            workflow_name="CI Build",
            run_id=12345,
            failure_type="transient",
            action_taken="retry",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.LOW
        assert "Self-Healing Success" in notification.title
        assert notification.source == "self-healing"
        assert notification.metadata["run_id"] == 12345


@pytest.mark.unit
class TestNotifySelfHealingFailure:
    """Test self-healing failure notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_self_healing_failure(self, MockManager):
        """Test self-healing failure notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_self_healing_failure(
            workflow_name="Deploy",
            run_id=67890,
            failure_type="permanent",
            attempts=3,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.HIGH
        assert "Self-Healing Failed" in notification.title
        assert notification.metadata["attempts"] == 3


@pytest.mark.unit
class TestNotifyMaintenanceScheduled:
    """Test maintenance scheduled notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_maintenance_scheduled(self, MockManager):
        """Test maintenance scheduled notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_maintenance_scheduled(
            task_name="Dependency Update",
            start_time="2024-01-15T02:00:00Z",
            end_time="2024-01-15T03:00:00Z",
            duration_minutes=60,
            impact="Minor service disruption",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM
        assert "Maintenance Scheduled" in notification.title
        assert notification.source == "maintenance-scheduler"


@pytest.mark.unit
class TestNotifyMaintenanceComplete:
    """Test maintenance complete notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_maintenance_complete_success(self, MockManager):
        """Test successful maintenance completion notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_maintenance_complete(
            task_name="Cleanup",
            duration_minutes=30,
            success=True,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.LOW

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_maintenance_complete_failure(self, MockManager):
        """Test failed maintenance completion notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_maintenance_complete(
            task_name="Update",
            duration_minutes=45,
            success=False,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.HIGH


@pytest.mark.unit
class TestNotifyModelAccuracyLow:
    """Test model accuracy low notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_model_accuracy_low(self, MockManager):
        """Test low model accuracy notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_model_accuracy_low(
            model_name="failure_predictor",
            accuracy=0.75,
            threshold=0.85,
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM
        assert "Model Accuracy" in notification.title
        assert notification.source == "analytics"
        assert notification.metadata["accuracy"] == 0.75


@pytest.mark.unit
class TestNotifyAutoMergeFailure:
    """Test auto-merge failure notification."""

    @pytest.fixture(autouse=True)
    def reset_manager(self):
        """Reset global manager before each test."""
        notification_integration._notification_manager = None
        yield
        notification_integration._notification_manager = None

    @patch.object(notification_integration, "NotificationManager")
    def test_notify_auto_merge_failure(self, MockManager):
        """Test auto-merge failure notification."""
        mock_instance = MagicMock()
        MockManager.return_value = mock_instance

        notification_integration.notify_auto_merge_failure(
            pr_number=123,
            repository="owner/repo",
            reason="Merge conflicts detected",
        )

        notification = mock_instance.send.call_args.args[0]
        assert notification.priority == notification_integration.Priority.MEDIUM
        assert "Auto-Merge Failed" in notification.title
        assert "#123" in notification.title
        assert notification.source == "auto-merge"
        assert notification.metadata["pr_number"] == 123
