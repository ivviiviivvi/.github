#!/usr/bin/env python3
"""
Unit tests for automation/scripts/notification_manager.py
Focus: Multi-channel notifications, rate limiting, deduplication, delivery tracking
"""

import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))

from notification_manager import (
    DeliveryRecord,
    Notification,
    NotificationManager,
    NotificationStatus,
    Priority,
)


class TestNotificationModel:
    """Test Notification model"""

    def test_default_priority(self):
        """Test default priority is MEDIUM"""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.priority == Priority.MEDIUM

    def test_default_timestamp(self):
        """Test timestamp is set automatically"""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.timestamp is not None
        assert isinstance(notification.timestamp, datetime)

    def test_empty_channels_default(self):
        """Test empty channels list by default"""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.channels == []

    def test_metadata_default(self):
        """Test empty metadata dict by default"""
        notification = Notification(
            title="Test",
            message="Test message",
            source="test",
        )
        assert notification.metadata == {}


class TestPriorityEnum:
    """Test Priority enum"""

    def test_priority_values(self):
        """Test all priority values exist"""
        assert Priority.CRITICAL == "CRITICAL"
        assert Priority.HIGH == "HIGH"
        assert Priority.MEDIUM == "MEDIUM"
        assert Priority.LOW == "LOW"
        assert Priority.INFO == "INFO"


class TestNotificationManager:
    """Test NotificationManager class"""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create manager with mocked config"""
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
    """Test channel selection based on priority"""

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
        """Test CRITICAL priority uses all channels"""
        channels = manager._get_channels_for_priority(Priority.CRITICAL)
        assert "slack" in channels
        assert "pagerduty" in channels
        assert "email" in channels

    def test_high_uses_slack_and_email(self, manager):
        """Test HIGH priority uses slack and email"""
        channels = manager._get_channels_for_priority(Priority.HIGH)
        assert "slack" in channels
        assert "email" in channels
        assert "pagerduty" not in channels

    def test_medium_uses_slack_only(self, manager):
        """Test MEDIUM priority uses slack only"""
        channels = manager._get_channels_for_priority(Priority.MEDIUM)
        assert channels == ["slack"]

    def test_info_uses_no_channels(self, manager):
        """Test INFO priority uses no channels"""
        channels = manager._get_channels_for_priority(Priority.INFO)
        assert channels == []


class TestRateLimiting:
    """Test rate limiting functionality"""

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
        """Test requests under limit are allowed"""
        assert manager._is_rate_limited("slack") is False

    def test_at_limit_blocks_request(self, manager):
        """Test requests at limit are blocked"""
        # Simulate 3 requests in last minute
        now = time.time()
        manager.rate_limits["slack"] = [now - 30, now - 20, now - 10]

        assert manager._is_rate_limited("slack") is True

    def test_old_requests_expire(self, manager):
        """Test old requests outside window don't count"""
        # Simulate old requests (> 60 seconds ago)
        old_time = time.time() - 120
        manager.rate_limits["slack"] = [old_time, old_time, old_time]

        assert manager._is_rate_limited("slack") is False

    def test_update_rate_limit(self, manager):
        """Test updating rate limit adds timestamp"""
        initial_count = len(manager.rate_limits["slack"])
        manager._update_rate_limit("slack")

        assert len(manager.rate_limits["slack"]) == initial_count + 1


class TestDeduplication:
    """Test notification deduplication"""

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
        """Test new notification is not a duplicate"""
        notification = Notification(
            title="Test Alert",
            message="Test",
            source="test-source",
        )
        assert manager._is_duplicate(notification) is False

    def test_recent_notification_is_duplicate(self, manager):
        """Test recent notification is detected as duplicate"""
        # Cache a notification
        manager.sent_cache["test-source:Test Alert"] = datetime.now(timezone.utc)

        notification = Notification(
            title="Test Alert",
            message="Different message",
            source="test-source",
        )
        assert manager._is_duplicate(notification) is True

    def test_old_notification_not_duplicate(self, manager):
        """Test old notification outside window is not duplicate"""
        # Cache an old notification
        manager.sent_cache["test-source:Test Alert"] = datetime.now(
            timezone.utc
        ) - timedelta(seconds=400)

        notification = Notification(
            title="Test Alert",
            message="Test",
            source="test-source",
        )
        assert manager._is_duplicate(notification) is False

    def test_cache_notification(self, manager):
        """Test caching notification for deduplication"""
        notification = Notification(
            title="Cache Test",
            message="Test",
            source="cache-source",
        )
        manager._cache_notification(notification)

        assert "cache-source:Cache Test" in manager.sent_cache


class TestIdGeneration:
    """Test notification ID generation"""

    @pytest.fixture
    def manager(self, tmp_path):
        manager = NotificationManager.__new__(NotificationManager)
        manager.config = {}
        return manager

    def test_generates_unique_ids(self, manager):
        """Test generates unique notification IDs"""
        id1 = manager._generate_id()
        time.sleep(0.001)  # Small delay to ensure uniqueness
        id2 = manager._generate_id()

        assert id1 != id2
        assert id1.startswith("NOTIF-")
        assert id2.startswith("NOTIF-")

    def test_id_format(self, manager):
        """Test ID follows expected format"""
        notification_id = manager._generate_id()

        # Format: NOTIF-YYYYMMDD_HHMMSS-NNN
        parts = notification_id.split("-")
        assert parts[0] == "NOTIF"
        assert len(parts) == 3


class TestDeliveryRecord:
    """Test DeliveryRecord model"""

    def test_default_values(self):
        """Test default values for delivery record"""
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
        """Test status can be updated"""
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
    """Test Slack message formatting"""

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
        """Test CRITICAL priority uses correct emoji"""
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
        """Test LOW priority uses correct emoji"""
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
    """Test send notification workflow"""

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
        """Test send generates notification ID"""
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
        """Test send skips duplicate notifications"""
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
        """Test send returns delivery records for each channel"""
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
    """Test default configuration"""

    @pytest.fixture
    def manager(self):
        manager = NotificationManager.__new__(NotificationManager)
        return manager

    def test_default_config_structure(self, manager):
        """Test default config has required structure"""
        config = manager._default_config()

        assert "channels" in config
        assert "priority_routing" in config
        assert "rate_limiting" in config
        assert "deduplication" in config

    def test_default_channels(self, manager):
        """Test default channels are configured"""
        config = manager._default_config()

        assert "slack" in config["channels"]
        assert "email" in config["channels"]
        assert "pagerduty" in config["channels"]

    def test_default_priority_routing(self, manager):
        """Test default priority routing"""
        config = manager._default_config()

        assert "CRITICAL" in config["priority_routing"]
        assert "pagerduty" in config["priority_routing"]["CRITICAL"]
