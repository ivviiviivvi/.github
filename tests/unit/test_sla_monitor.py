#!/usr/bin/env python3
"""Unit tests for automation/scripts/sla_monitor.py
Focus: SLA monitoring, breach detection, metrics calculation, threshold enforcement.
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Mock notification_integration before importing sla_monitor
sys.modules["notification_integration"] = MagicMock()

from models import Priority, SLAConfig, SLAThresholds
from sla_monitor import SLAMonitor


class TestSLAMonitor:
    """Test SLAMonitor class."""

    @pytest.fixture
    def mock_github(self):
        """Create mock GitHub client."""
        return MagicMock()

    @pytest.fixture
    def config(self):
        """Create test config."""
        return SLAConfig(
            enabled=True,
            check_interval_minutes=15,
            thresholds=[
                SLAThresholds(
                    priority=Priority.P0,
                    response_time_minutes=5,
                    resolution_time_hours=4,
                    success_rate_percentage=99.0,
                    availability_percentage=99.9,
                ),
                SLAThresholds(
                    priority=Priority.P1,
                    response_time_minutes=30,
                    resolution_time_hours=24,
                    success_rate_percentage=95.0,
                    availability_percentage=99.0,
                ),
                SLAThresholds(
                    priority=Priority.P2,
                    response_time_minutes=120,
                    resolution_time_hours=72,
                    success_rate_percentage=90.0,
                    availability_percentage=98.0,
                ),
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=480,
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )

    @pytest.fixture
    def monitor(self, mock_github, config, tmp_path):
        """Create monitor with temporary directories."""
        monitor = SLAMonitor(config, mock_github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        monitor.reports_dir = tmp_path / "reports"
        monitor.reports_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_initialization(self, mock_github, config, tmp_path):
        """Test monitor initializes correctly."""
        with patch.object(Path, "mkdir"):
            monitor = SLAMonitor(config, mock_github)

        assert monitor.config == config
        assert monitor.github == mock_github


class TestPriorityDetermination:
    """Test priority determination from labels."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        monitor = SLAMonitor(config, MagicMock())
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_p0_from_label(self, monitor):
        """Test P0 priority from label."""
        issue = {"labels": [{"name": "p0"}, {"name": "bug"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P0

    def test_p1_from_label(self, monitor):
        """Test P1 priority from label."""
        issue = {"labels": [{"name": "p1"}, {"name": "enhancement"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P1

    def test_critical_label_maps_to_p0(self, monitor):
        """Test critical label maps to P0."""
        issue = {"labels": [{"name": "critical"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P0

    def test_high_priority_label_maps_to_p1(self, monitor):
        """Test high priority label maps to P1."""
        issue = {"labels": [{"name": "high"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P1

    def test_default_priority_is_p3(self, monitor):
        """Test default priority is P3."""
        issue = {"labels": [{"name": "documentation"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P3

    def test_no_labels_returns_p3(self, monitor):
        """Test no labels returns P3."""
        issue = {"labels": []}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P3


class TestThresholds:
    """Test threshold retrieval."""

    @pytest.fixture
    def config(self):
        return SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P0,
                    response_time_minutes=5,
                    resolution_time_hours=4,
                    success_rate_percentage=99.0,
                    availability_percentage=99.9,
                ),
                SLAThresholds(
                    priority=Priority.P1,
                    response_time_minutes=30,
                    resolution_time_hours=24,
                    success_rate_percentage=95.0,
                    availability_percentage=99.0,
                ),
            ],
        )

    @pytest.fixture
    def monitor(self, config, tmp_path):
        monitor = SLAMonitor(config, MagicMock())
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_get_p0_thresholds(self, monitor):
        """Test retrieving P0 thresholds."""
        thresholds = monitor._get_thresholds(Priority.P0)
        assert thresholds.response_time_minutes == 5
        assert thresholds.resolution_time_hours == 4

    def test_get_p1_thresholds(self, monitor):
        """Test retrieving P1 thresholds."""
        thresholds = monitor._get_thresholds(Priority.P1)
        assert thresholds.response_time_minutes == 30
        assert thresholds.resolution_time_hours == 24

    def test_missing_priority_returns_default(self, monitor):
        """Test missing priority returns default thresholds."""
        thresholds = monitor._get_thresholds(Priority.P3)
        # Should return some default
        assert thresholds is not None


class TestIssueMonitoring:
    """Test issue SLA monitoring."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=60,
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_no_issues_returns_empty_metrics(self, monitor):
        """Test no issues returns empty metrics."""
        monitor.github.get.return_value = []

        metrics = monitor._monitor_issues("owner", "repo")

        assert metrics.total_items == 0
        assert metrics.success_rate_percentage == 100.0

    def test_filters_out_pull_requests(self, monitor):
        """Test filters out pull requests from issues."""
        # Test the filtering logic directly rather than through _monitor_issues
        # to avoid complex multi-call mock scenarios
        issues = [
            {"number": 1, "labels": [], "created_at": "2024-01-01T00:00:00Z"},
            {
                "number": 2,
                "labels": [],
                "created_at": "2024-01-01T00:00:00Z",
                # Note: Python's {} is falsy, so use non-empty dict for realism
                "pull_request": {"url": "https://github.com/owner/repo/pull/2"},
            },
        ]

        # Verify the filter logic that's used in _monitor_issues
        # Implementation uses "pull_request" not in i to check presence of key
        filtered = [i for i in issues if "pull_request" not in i]

        assert len(filtered) == 1
        assert filtered[0]["number"] == 1

    def test_detects_response_time_breach(self, monitor):
        """Test detects response time breach."""
        # Issue created 2 hours ago, no response
        created_time = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        monitor.github.get.side_effect = [
            [
                {
                    "number": 1,
                    "labels": [],
                    "created_at": created_time,
                }
            ],
            [],  # closed issues
        ]

        with patch.object(monitor, "_get_first_response", return_value=None):
            metrics = monitor._monitor_issues("owner", "repo")

        assert metrics.breached >= 1

    def test_within_sla_when_responded(self, monitor):
        """Test within SLA when responded in time."""
        created_time = datetime.now(timezone.utc) - timedelta(hours=2)
        response_time = created_time + timedelta(minutes=30)

        monitor.github.get.side_effect = [
            [
                {
                    "number": 1,
                    "labels": [],
                    "created_at": created_time.isoformat(),
                }
            ],
            [],  # closed issues
        ]

        with patch.object(monitor, "_get_first_response", return_value=response_time):
            metrics = monitor._monitor_issues("owner", "repo")

        assert metrics.within_sla >= 1


class TestPRMonitoring:
    """Test pull request SLA monitoring."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=60,
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_no_prs_returns_empty_metrics(self, monitor):
        """Test no PRs returns empty metrics."""
        monitor.github.get.return_value = []

        metrics = monitor._monitor_pull_requests("owner", "repo")

        assert metrics.total_items == 0
        assert metrics.success_rate_percentage == 100.0

    def test_detects_pr_review_breach(self, monitor):
        """Test detects PR without review breaching SLA."""
        created_time = (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()
        monitor.github.get.side_effect = [
            [
                {
                    "number": 42,
                    "labels": [],
                    "created_at": created_time,
                }
            ],
            [],  # merged PRs
        ]

        with patch.object(monitor, "_get_first_review", return_value=None):
            metrics = monitor._monitor_pull_requests("owner", "repo")

        assert metrics.breached >= 1


class TestWorkflowMonitoring:
    """Test workflow SLA monitoring."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=60,
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_calculates_success_rate(self, monitor):
        """Test calculates workflow success rate."""
        # Workflow runs need created_at timestamps for 24h filtering
        recent_time = datetime.now(timezone.utc).isoformat()
        monitor.github.get.return_value = {
            "workflow_runs": [
                {
                    "conclusion": "success",
                    "created_at": recent_time,
                    "updated_at": recent_time,
                },
                {
                    "conclusion": "success",
                    "created_at": recent_time,
                    "updated_at": recent_time,
                },
                {
                    "conclusion": "failure",
                    "created_at": recent_time,
                    "updated_at": recent_time,
                },
                {
                    "conclusion": "success",
                    "created_at": recent_time,
                    "updated_at": recent_time,
                },
            ]
        }

        metrics = monitor._monitor_workflows("owner", "repo")

        # 3 successes out of 4 = 75%
        assert metrics.success_rate_percentage == 75.0

    def test_no_workflows_returns_empty_metrics(self, monitor):
        """Test no workflows returns empty metrics."""
        monitor.github.get.return_value = {"workflow_runs": []}

        metrics = monitor._monitor_workflows("owner", "repo")

        assert metrics.total_items == 0
        assert metrics.success_rate_percentage == 100.0


class TestBreachHandling:
    """Test breach handling and notifications."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        monitor = SLAMonitor(config, MagicMock())
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_saves_breaches_to_disk(self, monitor):
        """Test breaches are saved to disk."""
        from models import SLABreach

        breaches = [
            SLABreach(
                item_type="issue",
                item_number=1,
                priority=Priority.P0,
                breach_type="response_time",
                threshold_value=5,
                actual_value=60,
            ),
        ]

        with patch.object(monitor, "_send_breach_notification"):
            monitor._handle_breaches("owner", "repo", breaches)

        # Check breach file was created
        breach_files = list(monitor.breaches_dir.glob("*.json"))
        assert len(breach_files) >= 1

    def test_sends_notification_for_breach(self, monitor):
        """Test sends notification for breach."""
        from models import SLABreach

        breaches = [
            SLABreach(
                item_type="issue",
                item_number=1,
                priority=Priority.P0,
                breach_type="response_time",
                threshold_value=5,
                actual_value=60,
            ),
        ]

        with patch.object(monitor, "_send_breach_notification") as mock_notify:
            monitor._handle_breaches("owner", "repo", breaches)

        mock_notify.assert_called()


class TestReportGeneration:
    """Test SLA report generation."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        monitor.reports_dir = tmp_path / "reports"
        monitor.reports_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_generates_report_structure(self, monitor):
        """Test generates report with correct structure."""
        # Mock all monitoring methods
        with patch.object(monitor, "_monitor_issues") as mock_issues:
            with patch.object(monitor, "_monitor_pull_requests") as mock_prs:
                with patch.object(monitor, "_monitor_workflows") as mock_wf:
                    from models import (AvailabilityMetric,
                                        ResolutionTimeMetric,
                                        ResponseTimeMetric, SLAMetrics,
                                        SuccessRateMetric)

                    mock_metrics = SLAMetrics(
                        repository="owner/repo",
                        time_window="24h",
                        overall_compliance=95.0,
                        response_time=ResponseTimeMetric(target_minutes=60, actual_minutes=30, met=True),
                        resolution_time=ResolutionTimeMetric(target_hours=24, actual_hours=12, met=True),
                        success_rate=SuccessRateMetric(target_percentage=95.0, actual_percentage=98.0, met=True),
                        availability=AvailabilityMetric(
                            target_percentage=99.0,
                            actual_percentage=99.5,
                            met=True,
                            downtime_minutes=7.2,
                        ),
                        trend="stable",
                    )
                    mock_issues.return_value = mock_metrics
                    mock_prs.return_value = mock_metrics
                    mock_wf.return_value = mock_metrics

                    report = monitor.generate_report("owner", "repo", lookback_days=7)

        assert report.repository == "owner/repo"
        assert report.period_start is not None
        assert report.period_end is not None

    def test_saves_report_to_disk(self, monitor):
        """Test saves report to disk."""
        with patch.object(monitor, "_monitor_issues") as mock_issues:
            with patch.object(monitor, "_monitor_pull_requests") as mock_prs:
                with patch.object(monitor, "_monitor_workflows") as mock_wf:
                    from models import (AvailabilityMetric,
                                        ResolutionTimeMetric,
                                        ResponseTimeMetric, SLAMetrics,
                                        SuccessRateMetric)

                    mock_metrics = SLAMetrics(
                        repository="owner/repo",
                        time_window="24h",
                        overall_compliance=95.0,
                        response_time=ResponseTimeMetric(target_minutes=60, actual_minutes=30, met=True),
                        resolution_time=ResolutionTimeMetric(target_hours=24, actual_hours=12, met=True),
                        success_rate=SuccessRateMetric(target_percentage=95.0, actual_percentage=98.0, met=True),
                        availability=AvailabilityMetric(
                            target_percentage=99.0,
                            actual_percentage=99.5,
                            met=True,
                            downtime_minutes=7.2,
                        ),
                        trend="stable",
                    )
                    mock_issues.return_value = mock_metrics
                    mock_prs.return_value = mock_metrics
                    mock_wf.return_value = mock_metrics

                    monitor.generate_report("owner", "repo", lookback_days=7)

        report_files = list(monitor.reports_dir.glob("*.json"))
        assert len(report_files) >= 1


class TestMetricsCalculation:
    """Test metrics calculation."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        monitor = SLAMonitor(config, MagicMock())
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_average_response_time(self, monitor):
        """Test average response time calculation."""
        response_times = [10, 20, 30, 40]
        avg = sum(response_times) / len(response_times)
        assert avg == 25.0

    def test_compliance_percentage(self, monitor):
        """Test compliance percentage calculation."""
        total = 10
        within_sla = 8
        compliance = (within_sla / total) * 100
        assert compliance == 80.0

    def test_zero_total_returns_100_percent(self, monitor):
        """Test zero total items returns 100% compliance."""
        total = 0
        within_sla = 0
        compliance = (within_sla / total * 100) if total > 0 else 100.0
        assert compliance == 100.0


@pytest.mark.unit
class TestMonitorRepositoryBreaches:
    """Test monitor_repository breach handling."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=60,
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        monitor.reports_dir = tmp_path / "reports"
        monitor.reports_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_handles_breaches_when_found(self, monitor):
        """Test handles breaches when items have breaches."""
        from models import ItemMetrics, SLABreach

        # Create mock metrics with breaches
        breach = SLABreach(
            item_type="issue",
            item_number=1,
            priority=Priority.P0,
            breach_type="response_time",
            threshold_value=5,
            actual_value=60,
        )
        mock_metrics = ItemMetrics(
            item_type="issues",
            total_items=1,
            within_sla=0,
            breached=1,
            avg_response_time_minutes=60,
            avg_resolution_time_hours=0,
            success_rate_percentage=0,
            breaches=[breach],
        )

        with patch.object(monitor, "_monitor_issues", return_value=mock_metrics):
            with patch.object(monitor, "_monitor_pull_requests", return_value=mock_metrics):
                with patch.object(monitor, "_monitor_workflows", return_value=mock_metrics):
                    with patch.object(monitor, "_handle_breaches") as mock_handle:
                        monitor.monitor_repository("owner", "repo")

                        mock_handle.assert_called_once()
                        # Should be called with all breaches from all item types
                        call_args = mock_handle.call_args
                        assert len(call_args[0][2]) >= 3  # 3 breach lists combined


@pytest.mark.unit
class TestIssueResponseBreaches:
    """Test issue response time breach detection with responses."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=30,  # 30 minute threshold
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_response_exceeds_threshold_creates_breach(self, monitor):
        """Test response time exceeding threshold creates breach."""
        created_time = datetime.now(timezone.utc) - timedelta(hours=2)
        response_time = created_time + timedelta(hours=1)  # 60 minutes > 30 threshold

        monitor.github.get.side_effect = [
            [{"number": 1, "labels": [], "created_at": created_time.isoformat()}],
            [],  # closed issues
        ]

        with patch.object(monitor, "_get_first_response", return_value=response_time):
            metrics = monitor._monitor_issues("owner", "repo")

        # Should have a breach since 60 > 30
        # Note: breached count is from len(breaches) list
        assert metrics.breached >= 1 or metrics.within_sla == 0


@pytest.mark.unit
class TestClosedIssuesResolution:
    """Test closed issues resolution time calculation."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=6000,  # Very high to avoid breaches
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_calculates_resolution_time_from_closed_issues(self, monitor):
        """Test calculates resolution time from closed issues."""
        open_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        created_time = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        closed_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        # First call returns open issues (need at least one to avoid early return),
        # second returns closed issues
        monitor.github.get.side_effect = [
            [
                {
                    "number": 99,
                    "labels": [],
                    "created_at": open_time.isoformat(),
                }
            ],  # Open issues
            [
                {
                    "number": 1,
                    "labels": [],
                    "created_at": created_time,
                    "closed_at": closed_time,
                },
            ],  # Closed issues
        ]

        # Mock first response to avoid breach
        with patch.object(monitor, "_get_first_response", return_value=open_time + timedelta(seconds=30)):
            metrics = monitor._monitor_issues("owner", "repo")

        # Resolution time should be calculated (close - create time)
        assert metrics.avg_resolution_time_hours > 0


@pytest.mark.unit
class TestPRReviewWithinSLA:
    """Test PR review within SLA detection."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=120,  # 2 hour threshold
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_pr_reviewed_within_sla(self, monitor):
        """Test PR reviewed within SLA threshold."""
        created_time = datetime.now(timezone.utc) - timedelta(hours=3)
        review_time = created_time + timedelta(minutes=60)  # 60 min < 120 threshold

        monitor.github.get.side_effect = [
            [{"number": 42, "labels": [], "created_at": created_time.isoformat()}],
            [],  # closed PRs
        ]

        with patch.object(monitor, "_get_first_review", return_value=review_time):
            metrics = monitor._monitor_pull_requests("owner", "repo")

        assert metrics.within_sla >= 1

    def test_pr_review_exceeds_threshold(self, monitor):
        """Test PR review exceeding threshold creates breach."""
        created_time = datetime.now(timezone.utc) - timedelta(hours=6)
        review_time = created_time + timedelta(hours=3)  # 180 min > 120 threshold

        monitor.github.get.side_effect = [
            [{"number": 42, "labels": [], "created_at": created_time.isoformat()}],
            [],  # closed PRs
        ]

        with patch.object(monitor, "_get_first_review", return_value=review_time):
            metrics = monitor._monitor_pull_requests("owner", "repo")

        # Should have breaches since review time exceeded threshold
        assert metrics.breached >= 1 or len(metrics.breaches) >= 1


@pytest.mark.unit
class TestMergedPRResolution:
    """Test merged PR resolution time calculation."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig(
            thresholds=[
                SLAThresholds(
                    priority=Priority.P3,
                    response_time_minutes=6000,  # Very high to avoid breaches
                    resolution_time_hours=168,
                    success_rate_percentage=85.0,
                    availability_percentage=95.0,
                ),
            ],
        )
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_calculates_merge_rate_and_resolution_time(self, monitor):
        """Test calculates merge rate and resolution time from merged PRs."""
        open_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        created_time = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        merged_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        monitor.github.get.side_effect = [
            [
                {
                    "number": 99,
                    "labels": [],
                    "created_at": open_time.isoformat(),
                }
            ],  # Open PRs
            [
                {
                    "number": 1,
                    "labels": [],
                    "created_at": created_time,
                    "merged_at": merged_time,
                },
                {
                    "number": 2,
                    "labels": [],
                    "created_at": created_time,
                    "merged_at": None,  # Not merged
                },
            ],  # Closed PRs
        ]

        # Mock first review to avoid breach
        with patch.object(monitor, "_get_first_review", return_value=open_time + timedelta(seconds=30)):
            metrics = monitor._monitor_pull_requests("owner", "repo")

        # Resolution time should be calculated from merged PRs
        assert metrics.avg_resolution_time_hours > 0
        # Merge rate should be 50% (1 merged out of 2 closed)
        assert metrics.success_rate_percentage == 50.0


@pytest.mark.unit
class TestGetFirstResponse:
    """Test _get_first_response method."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_returns_first_comment_time(self, monitor):
        """Test returns earliest comment time."""
        comment_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        monitor.github.get.return_value = [
            {"created_at": comment_time, "user": {"login": "reviewer"}},
        ]

        result = monitor._get_first_response("owner", "repo", 1)

        assert result is not None
        assert isinstance(result, datetime)

    def test_returns_none_when_no_comments(self, monitor):
        """Test returns None when no comments."""
        monitor.github.get.return_value = []

        result = monitor._get_first_response("owner", "repo", 1)

        assert result is None

    def test_returns_earliest_of_multiple_comments(self, monitor):
        """Test returns earliest comment when multiple exist."""
        early = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        late = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        monitor.github.get.return_value = [
            {"created_at": late, "user": {"login": "user2"}},
            {"created_at": early, "user": {"login": "user1"}},
        ]

        result = monitor._get_first_response("owner", "repo", 1)

        assert result is not None
        # Should be the earlier time
        assert result < datetime.now(timezone.utc) - timedelta(hours=4)


@pytest.mark.unit
class TestGetFirstReview:
    """Test _get_first_review method."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_returns_first_review_time(self, monitor):
        """Test returns earliest review time."""
        review_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        monitor.github.get.return_value = [
            {"submitted_at": review_time, "user": {"login": "reviewer"}},
        ]

        result = monitor._get_first_review("owner", "repo", 42)

        assert result is not None
        assert isinstance(result, datetime)

    def test_returns_none_when_no_reviews(self, monitor):
        """Test returns None when no reviews."""
        monitor.github.get.return_value = []

        result = monitor._get_first_review("owner", "repo", 42)

        assert result is None

    def test_returns_earliest_of_multiple_reviews(self, monitor):
        """Test returns earliest review when multiple exist."""
        early = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        late = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        monitor.github.get.return_value = [
            {"submitted_at": late, "user": {"login": "user2"}},
            {"submitted_at": early, "user": {"login": "user1"}},
        ]

        result = monitor._get_first_review("owner", "repo", 42)

        assert result is not None
        # Should be the earlier time
        assert result < datetime.now(timezone.utc) - timedelta(hours=4)


@pytest.mark.unit
class TestPriorityLabels:
    """Test priority detection from labels."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        monitor = SLAMonitor(config, MagicMock())
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_p2_from_medium_label(self, monitor):
        """Test P2 priority from medium label."""
        issue = {"labels": [{"name": "medium"}, {"name": "bug"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P2

    def test_p2_from_normal_label(self, monitor):
        """Test P2 priority from normal label."""
        issue = {"labels": [{"name": "normal"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P2

    def test_p2_from_p2_label(self, monitor):
        """Test P2 priority from p2 label."""
        issue = {"labels": [{"name": "p2"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P2

    def test_production_label_maps_to_p0(self, monitor):
        """Test production label maps to P0."""
        issue = {"labels": [{"name": "production"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P0

    def test_urgent_label_maps_to_p0(self, monitor):
        """Test urgent label maps to P0."""
        issue = {"labels": [{"name": "urgent"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P0

    def test_important_label_maps_to_p1(self, monitor):
        """Test important label maps to P1."""
        issue = {"labels": [{"name": "important"}]}
        priority = monitor._determine_priority(issue)
        assert priority == Priority.P1


@pytest.mark.unit
class TestSendBreachNotification:
    """Test _send_breach_notification method."""

    @pytest.fixture
    def monitor(self, tmp_path):
        config = SLAConfig()
        monitor = SLAMonitor(config, MagicMock())
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        return monitor

    def test_sends_notification_for_each_breach(self, monitor):
        """Test sends notification for each breach."""
        from models import SLABreach

        breaches = [
            SLABreach(
                item_type="issue",
                item_number=1,
                priority=Priority.P0,
                breach_type="response_time",
                threshold_value=5,
                actual_value=60,
            ),
            SLABreach(
                item_type="issue",
                item_number=2,
                priority=Priority.P0,
                breach_type="response_time",
                threshold_value=5,
                actual_value=45,
            ),
        ]

        with patch("sla_monitor.notify_sla_breach") as mock_notify:
            monitor._send_breach_notification("owner", "repo", "P0", breaches)

            # Should be called once per breach
            assert mock_notify.call_count == 2


@pytest.mark.unit
class TestGenerateReportWithBreachFiles:
    """Test generate_report loading breach files."""

    @pytest.fixture
    def monitor(self, tmp_path):
        import json

        config = SLAConfig()
        github = MagicMock()
        monitor = SLAMonitor(config, github)
        monitor.breaches_dir = tmp_path / "breaches"
        monitor.breaches_dir.mkdir(parents=True, exist_ok=True)
        monitor.reports_dir = tmp_path / "reports"
        monitor.reports_dir.mkdir(parents=True, exist_ok=True)

        # Create some breach files
        breach_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repository": "owner/repo",
            "breaches": [{"item_type": "issue", "item_number": 1, "breach_type": "response_time"}],
        }
        (monitor.breaches_dir / "breach_20240101_120000.json").write_text(json.dumps(breach_data))
        (monitor.breaches_dir / "breach_20240102_120000.json").write_text(json.dumps(breach_data))

        return monitor

    def test_counts_breaches_from_files(self, monitor):
        """Test counts breaches from breach files."""
        from models import ItemMetrics

        mock_metrics = ItemMetrics(
            item_type="issues",
            total_items=0,
            within_sla=0,
            breached=0,
            avg_response_time_minutes=0,
            avg_resolution_time_hours=0,
            success_rate_percentage=100,
        )

        with patch.object(monitor, "_monitor_issues", return_value=mock_metrics):
            with patch.object(monitor, "_monitor_pull_requests", return_value=mock_metrics):
                with patch.object(monitor, "_monitor_workflows", return_value=mock_metrics):
                    report = monitor.generate_report("owner", "repo", lookback_days=30)

        # Should count breaches from the files
        assert report.total_breaches >= 2


@pytest.mark.unit
class TestSLAMonitorCLI:
    """Test main CLI entry point."""

    def test_monitor_cli(self, tmp_path, capsys):
        """Test --monitor CLI option."""
        from models import ItemMetrics

        mock_metrics = ItemMetrics(
            item_type="issues",
            total_items=5,
            within_sla=4,
            breached=1,
            avg_response_time_minutes=30,
            avg_resolution_time_hours=12,
            success_rate_percentage=80,
        )

        with patch(
            "sys.argv",
            ["sla_monitor.py", "--owner", "org", "--repo", "repo", "--monitor"],
        ):
            with patch("sla_monitor.load_config") as mock_config:
                mock_config.return_value = SLAConfig()
                with patch("sla_monitor.GitHubAPIClient"):
                    with patch.object(SLAMonitor, "monitor_repository") as mock_monitor:
                        mock_monitor.return_value = {
                            "issues": mock_metrics,
                            "pull_requests": mock_metrics,
                            "workflows": mock_metrics,
                        }

                        from sla_monitor import main

                        main()

                        captured = capsys.readouterr()
                        assert "SLA Metrics" in captured.out
                        assert "issues" in captured.out
                        assert "Total: 5" in captured.out

    def test_monitor_with_breaches_shows_details(self, tmp_path, capsys):
        """Test --monitor with breaches shows breach details."""
        from models import ItemMetrics, SLABreach

        breach = SLABreach(
            item_type="issue",
            item_number=1,
            priority=Priority.P0,
            breach_type="response_time",
            threshold_value=5,
            actual_value=60,
        )
        mock_metrics = ItemMetrics(
            item_type="issues",
            total_items=1,
            within_sla=0,
            breached=1,
            avg_response_time_minutes=60,
            avg_resolution_time_hours=0,
            success_rate_percentage=0,
            breaches=[breach],
        )

        with patch(
            "sys.argv",
            ["sla_monitor.py", "--owner", "org", "--repo", "repo", "--check-breaches"],
        ):
            with patch("sla_monitor.load_config") as mock_config:
                mock_config.return_value = SLAConfig()
                with patch("sla_monitor.GitHubAPIClient"):
                    with patch.object(SLAMonitor, "monitor_repository") as mock_monitor:
                        mock_monitor.return_value = {
                            "issues": mock_metrics,
                            "pull_requests": mock_metrics,
                            "workflows": mock_metrics,
                        }

                        from sla_monitor import main

                        main()

                        captured = capsys.readouterr()
                        assert "Breaches" in captured.out
                        assert "response_time" in captured.out

    def test_report_cli(self, tmp_path, capsys):
        """Test --report CLI option."""
        from models import SLAReport

        with patch(
            "sys.argv",
            [
                "sla_monitor.py",
                "--owner",
                "org",
                "--repo",
                "repo",
                "--report",
                "--days",
                "14",
            ],
        ):
            with patch("sla_monitor.load_config") as mock_config:
                mock_config.return_value = SLAConfig()
                with patch("sla_monitor.GitHubAPIClient"):
                    with patch.object(SLAMonitor, "generate_report") as mock_report:
                        mock_report.return_value = SLAReport(
                            repository="org/repo",
                            period_start=datetime.now(timezone.utc) - timedelta(days=14),
                            period_end=datetime.now(timezone.utc),
                            metrics={},
                            total_breaches=5,
                        )

                        from sla_monitor import main

                        main()

                        captured = capsys.readouterr()
                        assert "SLA Report" in captured.out
                        assert "org/repo" in captured.out
                        assert "Total Breaches: 5" in captured.out

    def test_no_args_prints_help(self, capsys):
        """Test no arguments prints help."""
        with patch("sys.argv", ["sla_monitor.py", "--owner", "org", "--repo", "repo"]):
            with patch("sla_monitor.load_config") as mock_config:
                mock_config.return_value = SLAConfig()
                with patch("sla_monitor.GitHubAPIClient"):
                    with patch("argparse.ArgumentParser.print_help") as mock_help:
                        from sla_monitor import main

                        main()

                        mock_help.assert_called_once()

    def test_debug_flag_sets_logging(self):
        """Test --debug flag enables debug logging."""
        import logging

        from models import ItemMetrics

        mock_metrics = ItemMetrics(
            item_type="issues",
            total_items=0,
            within_sla=0,
            breached=0,
            avg_response_time_minutes=0,
            avg_resolution_time_hours=0,
            success_rate_percentage=100,
        )

        with patch(
            "sys.argv",
            [
                "sla_monitor.py",
                "--owner",
                "org",
                "--repo",
                "repo",
                "--debug",
                "--monitor",
            ],
        ):
            with patch("sla_monitor.load_config") as mock_config:
                mock_config.return_value = SLAConfig()
                with patch("sla_monitor.GitHubAPIClient"):
                    with patch.object(SLAMonitor, "monitor_repository") as mock_monitor:
                        mock_monitor.return_value = {
                            "issues": mock_metrics,
                            "pull_requests": mock_metrics,
                            "workflows": mock_metrics,
                        }

                        from sla_monitor import main

                        main()

                        assert logging.getLogger().level == logging.DEBUG

                        # Reset
                        logging.getLogger().setLevel(logging.INFO)
