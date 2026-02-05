#!/usr/bin/env python3
"""Unit tests for automation/scripts/notification_manager.py
Focus: Multi-channel notifications, rate limiting, deduplication, delivery tracking.
"""

import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from notification_manager import (DeliveryRecord, Notification,
                                  NotificationManager, NotificationStatus,
                                  Priority)


class TestNotificationModel:
    """Test Notification model."""

    def test_default_priority(self):
        """Test default priority is MEDIUM."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.priority == Priority.MEDIUM

    def test_default_timestamp(self):
        """Test timestamp is set automatically."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.timestamp is not None
        assert isinstance(notification.timestamp, datetime)

    def test_empty_channels_default(self):
        """Test empty channels list by default."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.channels == []

    def test_metadata_default(self):
        """Test empty metadata dict by default."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.metadata == {}


class TestPriorityEnum:
    """Test Priority enum."""

    def test_priority_values(self):
        """Test all priority values exist."""
        assert Priority.CRITICAL == "CRITICAL"
        assert Priority.HIGH == "HIGH"
        assert Priority.MEDIUM == "MEDIUM"
        assert Priority.LOW == "LOW"
        assert Priority.INFO == "INFO"


class TestNotificationManager:
    """Test NotificationManager class."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create manager with mocked config."""
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "slack": {"webhook_url": "https://hooks.slack.com/test"},
                    "email": {"default_recipients": ["test@example.com"]},
                    "pagerduty": {"integration_key": "test-key"},
                },
                "priority_routing": {
                    "CRITICAL": ["slack", "pagerduty", "email"],
                    "HIGH": ["slack", "email"],
                    "MEDIUM": ["slack"],
                    "LOW": ["slack"],
                    "INFO": [],
                },
                "rate_limiting": {
                    "enabled": True,
                    "max_per_minute": {"slack": 10, "email": 5, "pagerduty": 5},
                },
                "deduplication": {"enabled": True, "window_seconds": 300},
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.delivery_log = tmp_path / "delivery_log"
            manager.delivery_log.mkdir(parents=True, exist_ok=True)
            manager.rate_limits = {}
            manager.sent_cache = {}
            return manager


class TestChannelSelection:
    """Test channel selection based on priority."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "priority_routing": {
                    "CRITICAL": ["slack", "pagerduty", "email"],
                    "HIGH": ["slack", "email"],
                    "MEDIUM": ["slack"],
                    "LOW": ["slack"],
                    "INFO": [],
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            return manager

    def test_critical_uses_all_channels(self, manager):
        """Test CRITICAL priority uses all channels."""
        channels = manager._get_channels_for_priority(Priority.CRITICAL)
        assert "slack" in channels
        assert "pagerduty" in channels
        assert "email" in channels

    def test_high_uses_slack_and_email(self, manager):
        """Test HIGH priority uses slack and email."""
        channels = manager._get_channels_for_priority(Priority.HIGH)
        assert "slack" in channels
        assert "email" in channels
        assert "pagerduty" not in channels

    def test_medium_uses_slack_only(self, manager):
        """Test MEDIUM priority uses slack only."""
        channels = manager._get_channels_for_priority(Priority.MEDIUM)
        assert channels == ["slack"]

    def test_info_uses_no_channels(self, manager):
        """Test INFO priority uses no channels."""
        channels = manager._get_channels_for_priority(Priority.INFO)
        assert channels == []


class TestRateLimiting:
    """Test rate limiting functionality."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "rate_limiting": {
                    "enabled": True,
                    "max_per_minute": {"slack": 3, "email": 2},
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.rate_limits = {"slack": [], "email": []}
            return manager

    def test_under_limit_allows_request(self, manager):
        """Test requests under limit are allowed."""
        assert manager._is_rate_limited("slack") is False

    def test_at_limit_blocks_request(self, manager):
        """Test requests at limit are blocked."""
        # Simulate 3 requests in last minute
        now = time.time()
        manager.rate_limits["slack"] = [now - 30, now - 20, now - 10]

        assert manager._is_rate_limited("slack") is True

    def test_old_requests_expire(self, manager):
        """Test old requests outside window don't count."""
        # Simulate old requests (> 60 seconds ago)
        old_time = time.time() - 120
        manager.rate_limits["slack"] = [old_time, old_time, old_time]

        assert manager._is_rate_limited("slack") is False

    def test_update_rate_limit(self, manager):
        """Test updating rate limit adds timestamp."""
        initial_count = len(manager.rate_limits["slack"])
        manager._update_rate_limit("slack")

        assert len(manager.rate_limits["slack"]) == initial_count + 1


class TestDeduplication:
    """Test notification deduplication."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "deduplication": {"enabled": True, "window_seconds": 300},
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.sent_cache = {}
            return manager

    def test_new_notification_not_duplicate(self, manager):
        """Test new notification is not a duplicate."""
        notification = Notification(
            title="Test Alert",
            message="Test",
            source="test-source",
        )
        assert manager._is_duplicate(notification) is False

    def test_recent_notification_is_duplicate(self, manager):
        """Test recent notification is detected as duplicate."""
        # Cache a notification
        manager.sent_cache["test-source:Test Alert"] = datetime.now(timezone.utc)

        notification = Notification(
            title="Test Alert",
            message="Different message",
            source="test-source",
        )
        assert manager._is_duplicate(notification) is True

    def test_old_notification_not_duplicate(self, manager):
        """Test old notification outside window is not duplicate."""
        # Cache an old notification
        manager.sent_cache["test-source:Test Alert"] = datetime.now(timezone.utc) - timedelta(seconds=400)

        notification = Notification(
            title="Test Alert",
            message="Test",
            source="test-source",
        )
        assert manager._is_duplicate(notification) is False

    def test_cache_notification(self, manager):
        """Test caching notification for deduplication."""
        notification = Notification(
            title="Cache Test",
            message="Test",
            source="cache-source",
        )
        manager._cache_notification(notification)

        assert "cache-source:Cache Test" in manager.sent_cache


class TestIdGeneration:
    """Test notification ID generation."""

    @pytest.fixture
    def manager(self, tmp_path):
        manager = NotificationManager.__new__(NotificationManager)
        manager.config = {}
        return manager

    def test_generates_unique_ids(self, manager):
        """Test generates unique notification IDs."""
        id1 = manager._generate_id()
        time.sleep(1.1)  # Wait for timestamp to change (second-precision)
        id2 = manager._generate_id()

        assert id1 != id2
        assert id1.startswith("NOTIF-")
        assert id2.startswith("NOTIF-")

    def test_id_format(self, manager):
        """Test ID follows expected format."""
        notification_id = manager._generate_id()

        # Format: NOTIF-YYYYMMDD_HHMMSS-NNN
        parts = notification_id.split("-")
        assert parts[0] == "NOTIF"
        assert len(parts) == 3


class TestDeliveryRecord:
    """Test DeliveryRecord model."""

    def test_default_values(self):
        """Test default values for delivery record."""
        record = DeliveryRecord(
            notification_id="NOTIF-001",
            channel="slack",
            status=NotificationStatus.PENDING,
        )
        assert record.attempts == 0
        assert record.last_attempt is None
        assert record.delivered_at is None
        assert record.error is None

    def test_status_tracking(self):
        """Test status can be updated."""
        record = DeliveryRecord(
            notification_id="NOTIF-001",
            channel="slack",
            status=NotificationStatus.PENDING,
        )
        record.status = NotificationStatus.SENT
        record.delivered_at = datetime.now(timezone.utc)

        assert record.status == NotificationStatus.SENT
        assert record.delivered_at is not None


class TestSlackFormatting:
    """Test Slack message formatting."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "slack": {"webhook_url": "https://hooks.slack.com/test"},
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            return manager

    def test_critical_emoji(self, manager):
        """Test CRITICAL priority uses correct emoji."""
        notification = Notification(
            title="Critical Alert",
            message="Test",
            source="test",
            priority=Priority.CRITICAL,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack")

            call_args = mock_post.call_args
            message = call_args[1]["json"]
            assert "🚨" in message["text"]

    def test_low_emoji(self, manager):
        """Test LOW priority uses correct emoji."""
        notification = Notification(
            title="Success",
            message="Test",
            source="test",
            priority=Priority.LOW,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack")

            call_args = mock_post.call_args
            message = call_args[1]["json"]
            assert "✅" in message["text"]


class TestSendNotification:
    """Test send notification workflow."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "slack": {"webhook_url": "https://hooks.slack.com/test"},
                },
                "priority_routing": {
                    "MEDIUM": ["slack"],
                },
                "rate_limiting": {
                    "enabled": True,
                    "max_per_minute": {"slack": 10},
                },
                "deduplication": {"enabled": True, "window_seconds": 300},
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.delivery_log = tmp_path / "delivery_log"
            manager.delivery_log.mkdir(parents=True, exist_ok=True)
            manager.rate_limits = {"slack": []}
            manager.sent_cache = {}
            return manager

    def test_send_generates_id(self, manager):
        """Test send generates notification ID."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            channels=["slack"],
        )

        with patch.object(manager, "_send_to_channel") as mock_send:
            mock_send.return_value = DeliveryRecord(
                notification_id="test",
                channel="slack",
                status=NotificationStatus.SENT,
            )

            manager.send(notification)

        assert notification.notification_id is not None
        assert notification.notification_id.startswith("NOTIF-")

    def test_send_skips_duplicate(self, manager):
        """Test send skips duplicate notifications."""
        # Pre-cache the notification
        manager.sent_cache["test:Duplicate Test"] = datetime.now(timezone.utc)

        notification = Notification(
            title="Duplicate Test",
            message="Test",
            source="test",
            channels=["slack"],
        )

        with patch.object(manager, "_send_to_channel") as mock_send:
            records = manager.send(notification)

        assert records == {}
        mock_send.assert_not_called()

    def test_send_returns_delivery_records(self, manager):
        """Test send returns delivery records for each channel."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            channels=["slack"],
        )

        with patch.object(manager, "_send_to_channel") as mock_send:
            mock_send.return_value = DeliveryRecord(
                notification_id="test",
                channel="slack",
                status=NotificationStatus.SENT,
            )

            records = manager.send(notification)

        assert "slack" in records
        assert records["slack"].status == NotificationStatus.SENT


class TestDefaultConfig:
    """Test default configuration."""

    @pytest.fixture
    def manager(self):
        manager = NotificationManager.__new__(NotificationManager)
        return manager

    def test_default_config_structure(self, manager):
        """Test default config has required structure."""
        config = manager._default_config()

        assert "channels" in config
        assert "priority_routing" in config
        assert "rate_limiting" in config
        assert "deduplication" in config

    def test_default_channels(self, manager):
        """Test default channels are configured."""
        config = manager._default_config()

        assert "slack" in config["channels"]
        assert "email" in config["channels"]
        assert "pagerduty" in config["channels"]

    def test_default_priority_routing(self, manager):
        """Test default priority routing."""
        config = manager._default_config()

        assert "CRITICAL" in config["priority_routing"]
        assert "pagerduty" in config["priority_routing"]["CRITICAL"]


@pytest.mark.unit
class TestNotificationManagerInit:
    """Test NotificationManager initialization."""

    def test_init_with_valid_config(self, tmp_path):
        """Test initialization with valid config file."""
        config_file = tmp_path / "notifications.yml"
        config_file.write_text(
            """
channels:
  slack:
    webhook_url: https://hooks.slack.com/test
priority_routing:
  CRITICAL: [slack]
rate_limiting:
  enabled: true
deduplication:
  enabled: true
"""
        )

        manager = NotificationManager(str(config_file))

        assert manager.config is not None
        assert "channels" in manager.config
        assert manager.delivery_log.exists()

    def test_init_with_missing_config(self, tmp_path):
        """Test initialization with missing config uses defaults."""
        manager = NotificationManager(str(tmp_path / "nonexistent.yml"))

        assert manager.config is not None
        # Should have default config structure
        assert "channels" in manager.config
        assert "priority_routing" in manager.config


@pytest.mark.unit
class TestLoadConfig:
    """Test config loading functionality."""

    def test_load_valid_config_file(self, tmp_path):
        """Test loading a valid YAML config file."""
        config_file = tmp_path / "test_config.yml"
        config_file.write_text(
            """
channels:
  slack:
    webhook_url: https://test.slack.com
rate_limiting:
  max_per_minute:
    slack: 20
"""
        )

        manager = NotificationManager.__new__(NotificationManager)
        config = manager._load_config(str(config_file))

        assert config["channels"]["slack"]["webhook_url"] == "https://test.slack.com"
        assert config["rate_limiting"]["max_per_minute"]["slack"] == 20

    def test_load_missing_config_returns_defaults(self):
        """Test missing config file returns default config."""
        manager = NotificationManager.__new__(NotificationManager)
        config = manager._load_config("/nonexistent/path/config.yml")

        assert "channels" in config
        assert "priority_routing" in config


@pytest.mark.unit
class TestSendToChannel:
    """Test _send_to_channel method."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "slack": {"webhook_url": "https://hooks.slack.com/test"},
                    "email": {"default_recipients": ["test@example.com"]},
                    "pagerduty": {"integration_key": "test-pd-key"},  # allow-secret
                    "webhooks": {
                        "custom": {"url": "https://webhook.example.com/notify"},
                    },
                },
                "rate_limiting": {
                    "enabled": True,
                    "max_per_minute": {"slack": 10, "email": 5},
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.rate_limits = defaultdict(list)
            return manager

    def test_send_to_slack_channel(self, manager):
        """Test sending to slack channel."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
            notification_id="NOTIF-001",
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            record = manager._send_to_channel(notification, "slack")

        assert record.status == NotificationStatus.SENT
        assert record.attempts == 1
        assert record.delivered_at is not None

    def test_send_to_channel_rate_limited(self, manager):
        """Test channel is rate limited."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            notification_id="NOTIF-001",
        )

        # Pre-fill rate limit with timestamps within last minute
        now = time.time()
        for i in range(10):
            manager.rate_limits["slack"].append(now - i)

        record = manager._send_to_channel(notification, "slack")

        assert record.status == NotificationStatus.RATE_LIMITED
        assert record.attempts == 0

    def test_send_to_channel_failure(self, manager):
        """Test handling channel send failure."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            notification_id="NOTIF-001",
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.side_effect = Exception("Connection failed")

            record = manager._send_to_channel(notification, "slack")

        assert record.status == NotificationStatus.FAILED
        assert record.error == "Connection failed"
        assert record.attempts == 1

    def test_send_to_unknown_channel_fails(self, manager):
        """Test unknown channel type raises error."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            notification_id="NOTIF-001",
        )

        record = manager._send_to_channel(notification, "unknown_channel")

        assert record.status == NotificationStatus.FAILED
        assert "Unknown channel type" in record.error

    def test_send_to_email_channel(self, manager):
        """Test sending to email channel."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            notification_id="NOTIF-001",
        )

        record = manager._send_to_channel(notification, "email")

        assert record.status == NotificationStatus.SENT
        assert record.attempts == 1

    def test_send_to_pagerduty_channel(self, manager):
        """Test sending to pagerduty channel."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            notification_id="NOTIF-001",
            priority=Priority.CRITICAL,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            record = manager._send_to_channel(notification, "pagerduty")

        assert record.status == NotificationStatus.SENT

    def test_send_to_webhook_channel(self, manager):
        """Test sending to custom webhook channel."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            notification_id="NOTIF-001",
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            record = manager._send_to_channel(notification, "webhook:custom")

        assert record.status == NotificationStatus.SENT


@pytest.mark.unit
class TestSendSlackExtended:
    """Extended tests for Slack notifications."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "slack": {
                        "webhook_url": "https://hooks.slack.com/default",
                        "channels": {
                            "#incidents": {"webhook_url": "https://hooks.slack.com/incidents"},
                            "#alerts": {"webhook_url": "https://hooks.slack.com/alerts"},
                        },
                    },
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            return manager

    def test_send_to_specific_slack_channel(self, manager):
        """Test sending to a specific Slack channel."""
        notification = Notification(
            title="Incident Alert",
            message="Critical issue detected",
            source="monitoring",
            priority=Priority.HIGH,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack:#incidents")

            # Verify correct webhook was used
            mock_post.assert_called_once()
            call_url = mock_post.call_args[0][0]
            assert call_url == "https://hooks.slack.com/incidents"

    def test_send_slack_missing_webhook_raises_error(self, manager):
        """Test missing webhook URL raises ValueError."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
        )

        # Remove webhook URL
        manager.config["channels"]["slack"]["webhook_url"] = None

        with pytest.raises(ValueError, match="No webhook URL configured"):
            manager._send_slack(notification, "slack")

    def test_send_slack_with_metadata(self, manager):
        """Test Slack message includes metadata block."""
        notification = Notification(
            title="Alert",
            message="Test message",
            source="test",
            metadata={"environment": "production", "severity": "high"},
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack")

            call_args = mock_post.call_args
            message = call_args[1]["json"]
            blocks = message["blocks"]

            # Check metadata block exists
            metadata_blocks = [b for b in blocks if b.get("type") == "section"]
            assert len(metadata_blocks) >= 2  # Fields + message + metadata

    def test_send_slack_high_priority_emoji(self, manager):
        """Test HIGH priority uses warning emoji."""
        notification = Notification(
            title="Warning",
            message="Test",
            source="test",
            priority=Priority.HIGH,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack")

            call_args = mock_post.call_args
            message = call_args[1]["json"]
            assert "⚠️" in message["text"]

    def test_send_slack_medium_priority_emoji(self, manager):
        """Test MEDIUM priority uses info emoji."""
        notification = Notification(
            title="Info",
            message="Test",
            source="test",
            priority=Priority.MEDIUM,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack")

            call_args = mock_post.call_args
            message = call_args[1]["json"]
            assert "ℹ️" in message["text"]

    def test_send_slack_info_priority_emoji(self, manager):
        """Test INFO priority uses announcement emoji."""
        notification = Notification(
            title="Info",
            message="Test",
            source="test",
            priority=Priority.INFO,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_slack(notification, "slack")

            call_args = mock_post.call_args
            message = call_args[1]["json"]
            assert "📢" in message["text"]


@pytest.mark.unit
class TestSendEmail:
    """Test email sending functionality."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "email": {
                        "default_recipients": ["default@example.com"],
                        "recipients": {
                            "team": ["team1@example.com", "team2@example.com"],
                            "management": ["cto@example.com", "ceo@example.com"],
                        },
                    },
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            return manager

    def test_send_email_to_default_recipients(self, manager):
        """Test sending email to default recipients."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )

        # Should not raise - just logs
        manager._send_email(notification, "email")

    def test_send_email_to_specific_group(self, manager):
        """Test sending email to specific recipient group."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )

        # Should not raise - just logs
        manager._send_email(notification, "email:team")

    def test_send_email_missing_recipients_raises_error(self, manager):
        """Test missing recipients raises ValueError."""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )

        with pytest.raises(ValueError, match="No recipients configured"):
            manager._send_email(notification, "email:nonexistent")


@pytest.mark.unit
class TestSendPagerDuty:
    """Test PagerDuty sending functionality."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "pagerduty": {
                        "integration_key": "test-integration-key",  # allow-secret
                    },
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            return manager

    def test_send_pagerduty_critical_severity(self, manager):
        """Test PagerDuty with CRITICAL priority maps to critical severity."""
        notification = Notification(
            title="Critical Issue",
            message="System down",
            source="monitoring",
            priority=Priority.CRITICAL,
            metadata={"host": "server-01"},
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_pagerduty(notification)

            call_args = mock_post.call_args
            event = call_args[1]["json"]

            assert event["payload"]["severity"] == "critical"
            assert event["event_action"] == "trigger"

    def test_send_pagerduty_high_severity(self, manager):
        """Test PagerDuty with HIGH priority maps to error severity."""
        notification = Notification(
            title="High Issue",
            message="Service degraded",
            source="monitoring",
            priority=Priority.HIGH,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_pagerduty(notification)

            call_args = mock_post.call_args
            event = call_args[1]["json"]

            assert event["payload"]["severity"] == "error"

    def test_send_pagerduty_medium_severity(self, manager):
        """Test PagerDuty with MEDIUM priority maps to warning severity."""
        notification = Notification(
            title="Medium Issue",
            message="Warning condition",
            source="monitoring",
            priority=Priority.MEDIUM,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_pagerduty(notification)

            call_args = mock_post.call_args
            event = call_args[1]["json"]

            assert event["payload"]["severity"] == "warning"

    def test_send_pagerduty_low_severity(self, manager):
        """Test PagerDuty with LOW priority maps to info severity."""
        notification = Notification(
            title="Low Issue",
            message="Info",
            source="monitoring",
            priority=Priority.LOW,
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_pagerduty(notification)

            call_args = mock_post.call_args
            event = call_args[1]["json"]

            assert event["payload"]["severity"] == "info"

    def test_send_pagerduty_missing_key_raises_error(self, manager):
        """Test missing integration key raises ValueError."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
        )

        manager.config["channels"]["pagerduty"]["integration_key"] = None

        with pytest.raises(ValueError, match="integration key not configured"):
            manager._send_pagerduty(notification)


@pytest.mark.unit
class TestSendWebhook:
    """Test custom webhook sending functionality."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "webhooks": {
                        "custom-hook": {"url": "https://custom.example.com/webhook"},
                        "alerting": {"url": "https://alerts.example.com/notify"},
                    },
                },
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            return manager

    def test_send_webhook_success(self, manager):
        """Test sending to custom webhook."""
        notification = Notification(
            title="Webhook Test",
            message="Test message",
            source="test",
        )

        with patch("notification_manager.requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()

            manager._send_webhook(notification, "webhook:custom-hook")

            mock_post.assert_called_once()
            call_url = mock_post.call_args[0][0]
            assert call_url == "https://custom.example.com/webhook"

    def test_send_webhook_missing_raises_error(self, manager):
        """Test missing webhook configuration raises ValueError."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
        )

        with pytest.raises(ValueError, match="not configured"):
            manager._send_webhook(notification, "webhook:nonexistent")


@pytest.mark.unit
class TestDeduplicationDisabled:
    """Test deduplication when disabled."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "deduplication": {"enabled": False, "window_seconds": 300},
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.sent_cache = {}
            return manager

    def test_deduplication_disabled_allows_duplicates(self, manager):
        """Test duplicates are allowed when deduplication is disabled."""
        # Pre-cache a notification
        manager.sent_cache["test:Same Title"] = datetime.now(timezone.utc)

        notification = Notification(
            title="Same Title",
            message="Different message",
            source="test",
        )

        # Should return False even though it's in cache
        assert manager._is_duplicate(notification) is False


@pytest.mark.unit
class TestLogDelivery:
    """Test delivery logging functionality."""

    @pytest.fixture
    def manager(self, tmp_path):
        manager = NotificationManager.__new__(NotificationManager)
        manager.config = {}
        manager.delivery_log = tmp_path / "delivery_log"
        manager.delivery_log.mkdir(parents=True, exist_ok=True)
        return manager

    def test_log_delivery_creates_file(self, manager):
        """Test logging delivery creates log file."""
        record = DeliveryRecord(
            notification_id="NOTIF-TEST-001",
            channel="slack",
            status=NotificationStatus.SENT,
            attempts=1,
            delivered_at=datetime.now(timezone.utc),
        )

        manager._log_delivery(record)

        log_file = manager.delivery_log / "NOTIF-TEST-001.json"
        assert log_file.exists()

        import json

        with open(log_file) as f:
            content = f.read()
            log_entry = json.loads(content.strip())

        assert log_entry["notification_id"] == "NOTIF-TEST-001"
        assert log_entry["channel"] == "slack"
        assert log_entry["status"] == "SENT"


@pytest.mark.unit
class TestSendWithChannelSelection:
    """Test send method with automatic channel selection."""

    @pytest.fixture
    def manager(self, tmp_path):
        with patch.object(NotificationManager, "_load_config") as mock_load:
            mock_load.return_value = {
                "channels": {
                    "slack": {"webhook_url": "https://hooks.slack.com/test"},
                    "pagerduty": {"integration_key": "test-key"},  # allow-secret
                    "email": {"default_recipients": ["test@example.com"]},
                },
                "priority_routing": {
                    "CRITICAL": ["slack", "pagerduty", "email"],
                    "HIGH": ["slack", "email"],
                    "MEDIUM": ["slack"],
                    "LOW": ["slack"],
                    "INFO": [],
                },
                "rate_limiting": {"max_per_minute": {"slack": 10}},
                "deduplication": {"enabled": True, "window_seconds": 300},
            }
            manager = NotificationManager.__new__(NotificationManager)
            manager.config = mock_load.return_value
            manager.delivery_log = tmp_path / "delivery_log"
            manager.delivery_log.mkdir(parents=True, exist_ok=True)
            manager.rate_limits = {}
            manager.sent_cache = {}
            return manager

    def test_send_selects_channels_by_priority(self, manager):
        """Test send auto-selects channels based on priority."""
        notification = Notification(
            title="Test",
            message="Test",
            source="test",
            priority=Priority.CRITICAL,
            # No channels specified
        )

        with patch.object(manager, "_send_to_channel") as mock_send:
            mock_send.return_value = DeliveryRecord(
                notification_id="test",
                channel="slack",
                status=NotificationStatus.SENT,
            )

            records = manager.send(notification)

        # Should have called for slack, pagerduty, email
        assert mock_send.call_count == 3


@pytest.mark.unit
class TestMainCLI:
    """Test main CLI function."""

    def test_main_with_required_args(self, tmp_path, capsys):
        """Test main CLI with required arguments."""
        import sys

        # Create minimal config
        config_file = tmp_path / "notifications.yml"
        config_file.write_text(
            """
channels:
  slack:
    webhook_url: https://hooks.slack.com/test
priority_routing:
  MEDIUM: [slack]
rate_limiting:
  max_per_minute:
    slack: 10
deduplication:
  enabled: true
  window_seconds: 300
"""
        )

        # Mock sys.argv
        original_argv = sys.argv
        sys.argv = [
            "notification_manager.py",
            "--title",
            "Test Alert",
            "--message",
            "This is a test",
            "--source",
            "cli-test",
            "--priority",
            "MEDIUM",
        ]

        try:
            with patch("notification_manager.requests.post") as mock_post:
                mock_post.return_value.raise_for_status = MagicMock()

                # Mock NotificationManager to use our config
                with patch.object(NotificationManager, "_load_config") as mock_load_config:
                    mock_load_config.return_value = {
                        "channels": {"slack": {"webhook_url": "https://hooks.slack.com/test"}},
                        "priority_routing": {"MEDIUM": ["slack"]},
                        "rate_limiting": {"max_per_minute": {"slack": 10}},
                        "deduplication": {"enabled": True, "window_seconds": 300},
                    }

                    from notification_manager import main

                    main()

            captured = capsys.readouterr()
            assert "Sent notification" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_with_channels_arg(self, tmp_path, capsys):
        """Test main CLI with explicit channels."""
        import sys

        original_argv = sys.argv
        sys.argv = [
            "notification_manager.py",
            "--title",
            "Test",
            "--message",
            "Test message",
            "--source",
            "test",
            "--channels",
            "slack",
            "email",
        ]

        try:
            with patch.object(NotificationManager, "_load_config") as mock_load:
                mock_load.return_value = {
                    "channels": {
                        "slack": {"webhook_url": "https://hooks.slack.com/test"},
                        "email": {"default_recipients": ["test@example.com"]},
                    },
                    "priority_routing": {},
                    "rate_limiting": {"max_per_minute": {"slack": 10, "email": 5}},
                    "deduplication": {"enabled": True, "window_seconds": 300},
                }

                with patch("notification_manager.requests.post") as mock_post:
                    mock_post.return_value.raise_for_status = MagicMock()

                    from notification_manager import main

                    main()

            captured = capsys.readouterr()
            assert "Sent notification" in captured.out
        finally:
            sys.argv = original_argv
