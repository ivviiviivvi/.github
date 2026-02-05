#!/usr/bin/env python3
"""Tests for proactive_maintenance.py.

Tests the proactive maintenance scheduler with ML-based timing,
including activity pattern analysis and window prediction.
"""

import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "src/automation/scripts")

from src.automation.scripts.models import (MaintenanceConfig, MaintenanceTask,
                                           Priority, RiskLevel)
from src.automation.scripts.proactive_maintenance import (MaintenanceScheduler,
                                                          main)


@pytest.mark.unit
class TestMaintenanceSchedulerInit:
    """Test MaintenanceScheduler initialization."""

    def test_init_sets_properties(self):
        """Test initialization sets all properties."""
        mock_client = MagicMock()
        config = MaintenanceConfig()

        scheduler = MaintenanceScheduler(mock_client, config)

        assert scheduler.client == mock_client
        assert scheduler.config == config
        assert scheduler.logger is not None


@pytest.mark.unit
class TestScheduleMaintenance:
    """Test schedule_maintenance method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_schedule_maintenance_returns_window(self, scheduler):
        """Test schedule_maintenance returns optimal window."""
        with patch.object(scheduler, "_analyze_activity_patterns") as mock_analyze:
            with patch.object(scheduler, "_get_pending_tasks") as mock_tasks:
                with patch.object(scheduler, "_predict_maintenance_windows") as mock_predict:
                    mock_analyze.return_value = {
                        "hourly_patterns": {},
                        "daily_patterns": {},
                    }
                    mock_tasks.return_value = []

                    mock_window = MagicMock()
                    mock_window.scheduled_time.isoformat.return_value = "2024-01-15T02:00:00"
                    mock_window.impact_score = 0.2
                    mock_window.confidence = 0.85
                    mock_predict.return_value = [mock_window]

                    result = scheduler.schedule_maintenance("owner", "repo", "cleanup")

                    assert result == mock_window

    def test_schedule_maintenance_no_windows_raises(self, scheduler):
        """Test schedule_maintenance raises when no windows found."""
        with patch.object(scheduler, "_analyze_activity_patterns") as mock_analyze:
            with patch.object(scheduler, "_get_pending_tasks") as mock_tasks:
                with patch.object(scheduler, "_predict_maintenance_windows") as mock_predict:
                    mock_analyze.return_value = {}
                    mock_tasks.return_value = []
                    mock_predict.return_value = []

                    with pytest.raises(ValueError) as exc_info:
                        scheduler.schedule_maintenance("owner", "repo", "cleanup")

                    assert "No suitable maintenance windows" in str(exc_info.value)


@pytest.mark.unit
class TestAnalyzeActivityPatterns:
    """Test _analyze_activity_patterns method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_analyze_activity_patterns_structure(self, scheduler):
        """Test analyze returns expected data structure."""
        with patch.object(scheduler, "_get_commit_activity") as mock_commits:
            with patch.object(scheduler, "_get_workflow_activity") as mock_workflows:
                with patch.object(scheduler, "_get_issue_activity") as mock_issues:
                    mock_commits.return_value = []
                    mock_workflows.return_value = []
                    mock_issues.return_value = []

                    result = scheduler._analyze_activity_patterns("owner", "repo")

                    assert "hourly_patterns" in result
                    assert "daily_patterns" in result
                    assert "commit_activity" in result
                    assert "workflow_activity" in result
                    assert "issue_activity" in result


@pytest.mark.unit
class TestGetCommitActivity:
    """Test _get_commit_activity method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_get_commit_activity_success(self, scheduler):
        """Test successful commit activity retrieval."""
        scheduler.client.get.return_value = [{"sha": "abc123", "commit": {"message": "Test"}}]

        result = scheduler._get_commit_activity("owner", "repo")

        assert len(result) == 1
        scheduler.client.get.assert_called_once()

    def test_get_commit_activity_error_returns_empty(self, scheduler):
        """Test commit activity returns empty on error."""
        scheduler.client.get.side_effect = Exception("API Error")

        result = scheduler._get_commit_activity("owner", "repo")

        assert result == []


@pytest.mark.unit
class TestGetWorkflowActivity:
    """Test _get_workflow_activity method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_get_workflow_activity_success(self, scheduler):
        """Test successful workflow activity retrieval."""
        scheduler.client.get.return_value = {"workflow_runs": [{"id": 1, "status": "completed"}]}

        result = scheduler._get_workflow_activity("owner", "repo")

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_get_workflow_activity_error_returns_empty(self, scheduler):
        """Test workflow activity returns empty on error."""
        scheduler.client.get.side_effect = Exception("API Error")

        result = scheduler._get_workflow_activity("owner", "repo")

        assert result == []


@pytest.mark.unit
class TestGetIssueActivity:
    """Test _get_issue_activity method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_get_issue_activity_success(self, scheduler):
        """Test successful issue activity retrieval."""
        scheduler.client.get.return_value = [{"number": 1, "title": "Test Issue"}]

        result = scheduler._get_issue_activity("owner", "repo")

        assert len(result) == 1

    def test_get_issue_activity_error_returns_empty(self, scheduler):
        """Test issue activity returns empty on error."""
        scheduler.client.get.side_effect = Exception("API Error")

        result = scheduler._get_issue_activity("owner", "repo")

        assert result == []


@pytest.mark.unit
class TestCalculateHourlyPatterns:
    """Test _calculate_hourly_patterns method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_calculate_hourly_patterns_empty(self, scheduler):
        """Test hourly patterns with no data."""
        result = scheduler._calculate_hourly_patterns([], [], [])

        assert len(result) == 24
        assert all(v == 0.0 for v in result.values())

    def test_calculate_hourly_patterns_with_commits(self, scheduler):
        """Test hourly patterns with commit data."""
        commits = [
            {"commit": {"author": {"date": "2024-01-15T10:00:00Z"}}},
            {"commit": {"author": {"date": "2024-01-15T10:30:00Z"}}},
            {"commit": {"author": {"date": "2024-01-15T14:00:00Z"}}},
        ]

        result = scheduler._calculate_hourly_patterns(commits, [], [])

        # Hour 10 should have highest activity (2 commits)
        assert result[10] == 1.0
        assert result[14] == 0.5

    def test_calculate_hourly_patterns_with_workflows(self, scheduler):
        """Test hourly patterns with workflow data."""
        workflows = [
            {"created_at": "2024-01-15T08:00:00Z"},
            {"created_at": "2024-01-15T08:30:00Z"},
        ]

        result = scheduler._calculate_hourly_patterns([], workflows, [])

        # Hour 8 has 2 workflows * 2 weight = 4 (normalized to 1.0)
        assert result[8] == 1.0

    def test_calculate_hourly_patterns_with_issues(self, scheduler):
        """Test hourly patterns with issue data."""
        issues = [
            {"created_at": "2024-01-15T16:00:00Z"},
        ]

        result = scheduler._calculate_hourly_patterns([], [], issues)

        assert result[16] == 1.0


@pytest.mark.unit
class TestCalculateDailyPatterns:
    """Test _calculate_daily_patterns method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_calculate_daily_patterns_empty(self, scheduler):
        """Test daily patterns with no data."""
        result = scheduler._calculate_daily_patterns([], [], [])

        assert len(result) == 7
        assert all(v == 0.0 for v in result.values())

    def test_calculate_daily_patterns_with_commits(self, scheduler):
        """Test daily patterns with commit data."""
        # Monday = 0
        commits = [
            {"commit": {"author": {"date": "2024-01-15T10:00:00Z"}}},  # Monday
            {"commit": {"author": {"date": "2024-01-16T10:00:00Z"}}},  # Tuesday
        ]

        result = scheduler._calculate_daily_patterns(commits, [], [])

        assert result[0] == 1.0  # Monday
        assert result[1] == 1.0  # Tuesday


@pytest.mark.unit
class TestGetPendingTasks:
    """Test _get_pending_tasks method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_get_pending_tasks_dependency_update(self, scheduler):
        """Test pending tasks for dependency updates."""
        with patch.object(scheduler, "_get_dependency_update_tasks") as mock_deps:
            mock_deps.return_value = [
                MaintenanceTask(
                    task_type="dependency_update",
                    description="Update lodash",
                    priority=Priority.P2,
                    estimated_duration=10,
                    risk_level=RiskLevel.LOW,
                )
            ]

            result = scheduler._get_pending_tasks("owner", "repo", "dependency_update")

            assert len(result) == 1
            assert result[0].task_type == "dependency_update"

    def test_get_pending_tasks_cleanup(self, scheduler):
        """Test pending tasks for cleanup."""
        with patch.object(scheduler, "_get_cleanup_tasks") as mock_cleanup:
            mock_cleanup.return_value = []

            result = scheduler._get_pending_tasks("owner", "repo", "cleanup")

            mock_cleanup.assert_called_once()

    def test_get_pending_tasks_optimization(self, scheduler):
        """Test pending tasks for optimization."""
        with patch.object(scheduler, "_get_optimization_tasks") as mock_opt:
            mock_opt.return_value = []

            result = scheduler._get_pending_tasks("owner", "repo", "optimization")

            mock_opt.assert_called_once()


@pytest.mark.unit
class TestGetDependencyUpdateTasks:
    """Test _get_dependency_update_tasks method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_get_dependency_tasks_finds_dependabot(self, scheduler):
        """Test finding Dependabot PRs."""
        scheduler.client.get.return_value = [
            {
                "number": 1,
                "title": "Bump lodash from 4.17.20 to 4.17.21",
                "user": {"login": "dependabot[bot]"},
            },
            {
                "number": 2,
                "title": "Regular PR",
                "user": {"login": "developer"},
            },
        ]

        result = scheduler._get_dependency_update_tasks("owner", "repo")

        assert len(result) == 1
        assert "lodash" in result[0].description

    def test_get_dependency_tasks_finds_renovate(self, scheduler):
        """Test finding Renovate PRs."""
        scheduler.client.get.return_value = [
            {
                "number": 3,
                "title": "Update dependency axios",
                "user": {"login": "renovate[bot]"},
            },
        ]

        result = scheduler._get_dependency_update_tasks("owner", "repo")

        assert len(result) == 1

    def test_get_dependency_tasks_error_returns_empty(self, scheduler):
        """Test dependency tasks returns empty on error."""
        scheduler.client.get.side_effect = Exception("API Error")

        result = scheduler._get_dependency_update_tasks("owner", "repo")

        assert result == []


@pytest.mark.unit
class TestGetCleanupTasks:
    """Test _get_cleanup_tasks method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig(stale_branch_days=30)
        return MaintenanceScheduler(mock_client, config)

    def test_get_cleanup_tasks_finds_stale_branches(self, scheduler):
        """Test finding stale branches."""
        # 60 days ago
        stale_date = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()

        scheduler.client.get.side_effect = [
            # First call: get branches
            [
                {
                    "name": "feature-old",
                    "commit": {"sha": "abc123"},
                },
                {
                    "name": "main",
                    "commit": {"sha": "def456"},
                },
            ],
            # Second call: get commit for feature-old
            {"commit": {"author": {"date": stale_date}}},
        ]

        result = scheduler._get_cleanup_tasks("owner", "repo")

        assert len(result) == 1
        assert "stale branches" in result[0].description

    def test_get_cleanup_tasks_skips_protected_branches(self, scheduler):
        """Test cleanup skips main/master/develop branches."""
        scheduler.client.get.return_value = [
            {"name": "main", "commit": {"sha": "abc"}},
            {"name": "master", "commit": {"sha": "def"}},
            {"name": "develop", "commit": {"sha": "ghi"}},
        ]

        result = scheduler._get_cleanup_tasks("owner", "repo")

        # No stale branches found (all protected)
        assert result == []

    def test_get_cleanup_tasks_error_returns_empty(self, scheduler):
        """Test cleanup tasks returns empty on error."""
        scheduler.client.get.side_effect = Exception("API Error")

        result = scheduler._get_cleanup_tasks("owner", "repo")

        assert result == []

    def test_get_cleanup_tasks_handles_missing_commit_date(self, scheduler):
        """Test cleanup handles missing commit date gracefully."""
        scheduler.client.get.side_effect = [
            [{"name": "feature-x", "commit": {"sha": "abc"}}],
            # Return commit without proper date structure
            {"commit": {}},
        ]

        result = scheduler._get_cleanup_tasks("owner", "repo")

        # Should return empty since commit date couldn't be parsed
        assert result == []


@pytest.mark.unit
class TestGetOptimizationTasks:
    """Test _get_optimization_tasks method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_get_optimization_tasks_returns_empty(self, scheduler):
        """Test optimization tasks placeholder returns empty."""
        result = scheduler._get_optimization_tasks("owner", "repo")

        assert result == []


@pytest.mark.unit
class TestPredictMaintenanceWindows:
    """Test _predict_maintenance_windows method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig(preferred_hours=[2, 3, 4])
        return MaintenanceScheduler(mock_client, config)

    def test_predict_windows_returns_sorted_list(self, scheduler):
        """Test windows are sorted by impact score."""
        activity_data = {
            "hourly_patterns": dict.fromkeys(range(24), 0.5),
            "daily_patterns": dict.fromkeys(range(7), 0.5),
            "commit_activity": [],
            "workflow_activity": [],
            "issue_activity": [],
        }
        tasks = []

        result = scheduler._predict_maintenance_windows("owner", "repo", "cleanup", activity_data, tasks)

        assert len(result) > 0
        # Verify sorted by impact score
        for i in range(len(result) - 1):
            assert result[i].impact_score <= result[i + 1].impact_score

    def test_predict_windows_adds_alternatives(self, scheduler):
        """Test alternatives are added to best window."""
        activity_data = {
            "hourly_patterns": dict.fromkeys(range(24), 0.5),
            "daily_patterns": dict.fromkeys(range(7), 0.5),
            "commit_activity": [],
            "workflow_activity": [],
            "issue_activity": [],
        }

        result = scheduler._predict_maintenance_windows("owner", "repo", "cleanup", activity_data, [])

        if len(result) > 1:
            assert len(result[0].alternatives) > 0


@pytest.mark.unit
class TestCalculateImpactScore:
    """Test _calculate_impact_score method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig(
            preferred_hours=[2, 3],
            preferred_days=[5, 6],
            avoid_dates=["2024-12-25"],
        )
        return MaintenanceScheduler(mock_client, config)

    def test_impact_score_preferred_hour_reduction(self, scheduler):
        """Test preferred hours reduce impact score."""
        activity_data = {
            "hourly_patterns": dict.fromkeys(range(24), 0.5),
            "daily_patterns": dict.fromkeys(range(7), 0.5),
        }

        # Preferred hour (2:00)
        window_time = datetime(2024, 1, 15, 2, 0, tzinfo=timezone.utc)
        score_preferred = scheduler._calculate_impact_score(window_time, activity_data, "cleanup")

        # Non-preferred hour (12:00)
        window_time_non = datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)
        score_non_preferred = scheduler._calculate_impact_score(window_time_non, activity_data, "cleanup")

        assert score_preferred < score_non_preferred

    def test_impact_score_avoid_dates_maximum(self, scheduler):
        """Test avoid dates get maximum impact score."""
        activity_data = {
            "hourly_patterns": dict.fromkeys(range(24), 0.1),
            "daily_patterns": dict.fromkeys(range(7), 0.1),
        }

        window_time = datetime(2024, 12, 25, 2, 0, tzinfo=timezone.utc)
        # Use dependency_update which doesn't reduce the impact
        score = scheduler._calculate_impact_score(window_time, activity_data, "dependency_update")

        # Avoid dates set base_impact to 1.0, dependency_update multiplies by 1.2
        # but result is capped at 1.0
        assert score == 1.0

    def test_impact_score_task_type_adjustment(self, scheduler):
        """Test task type adjusts impact score."""
        activity_data = {
            "hourly_patterns": dict.fromkeys(range(24), 0.5),
            "daily_patterns": dict.fromkeys(range(7), 0.5),
        }
        window_time = datetime(2024, 1, 16, 10, 0, tzinfo=timezone.utc)

        dep_score = scheduler._calculate_impact_score(window_time, activity_data, "dependency_update")
        cleanup_score = scheduler._calculate_impact_score(window_time, activity_data, "cleanup")

        # dependency_update should have higher impact
        assert dep_score > cleanup_score


@pytest.mark.unit
class TestCalculateConfidence:
    """Test _calculate_confidence method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig()
        return MaintenanceScheduler(mock_client, config)

    def test_confidence_high_with_many_events(self, scheduler):
        """Test high confidence with many data points."""
        activity_data = {
            "commit_activity": [{"id": i} for i in range(50)],
            "workflow_activity": [{"id": i} for i in range(30)],
            "issue_activity": [{"id": i} for i in range(25)],
        }
        window = datetime.now(timezone.utc) + timedelta(days=1)

        confidence = scheduler._calculate_confidence(activity_data, window)

        assert confidence >= 0.9

    def test_confidence_medium_with_moderate_events(self, scheduler):
        """Test medium confidence with moderate data points."""
        activity_data = {
            "commit_activity": [{"id": i} for i in range(20)],
            "workflow_activity": [{"id": i} for i in range(15)],
            "issue_activity": [{"id": i} for i in range(15)],
        }
        window = datetime.now(timezone.utc) + timedelta(days=1)

        confidence = scheduler._calculate_confidence(activity_data, window)

        assert 0.6 <= confidence < 0.9

    def test_confidence_low_with_few_events(self, scheduler):
        """Test low confidence with few data points."""
        activity_data = {
            "commit_activity": [{"id": 1}],
            "workflow_activity": [],
            "issue_activity": [],
        }
        window = datetime.now(timezone.utc) + timedelta(days=1)

        confidence = scheduler._calculate_confidence(activity_data, window)

        assert confidence < 0.6

    def test_confidence_reduced_for_far_future(self, scheduler):
        """Test confidence reduced for predictions far in future."""
        activity_data = {
            "commit_activity": [{"id": i} for i in range(100)],
            "workflow_activity": [],
            "issue_activity": [],
        }

        window_near = datetime.now(timezone.utc) + timedelta(days=1)
        window_far = datetime.now(timezone.utc) + timedelta(days=7)

        confidence_near = scheduler._calculate_confidence(activity_data, window_near)
        confidence_far = scheduler._calculate_confidence(activity_data, window_far)

        assert confidence_far < confidence_near


@pytest.mark.unit
class TestGenerateReasoning:
    """Test _generate_reasoning method."""

    @pytest.fixture
    def scheduler(self):
        """Create scheduler fixture."""
        mock_client = MagicMock()
        config = MaintenanceConfig(
            preferred_hours=[2, 3, 4],
            preferred_days=[5, 6],
        )
        return MaintenanceScheduler(mock_client, config)

    def test_reasoning_for_preferred_hour(self, scheduler):
        """Test reasoning mentions preferred hour."""
        activity_data = {"hourly_patterns": {}, "daily_patterns": {}}
        window = datetime(2024, 1, 15, 2, 0, tzinfo=timezone.utc)

        reasoning = scheduler._generate_reasoning(window, 0.3, activity_data)

        assert "preferred maintenance hour" in reasoning.lower()

    def test_reasoning_for_weekend(self, scheduler):
        """Test reasoning mentions weekend or preferred day."""
        activity_data = {"hourly_patterns": {}, "daily_patterns": {}}
        # Saturday = day 5 which is in preferred_days
        window = datetime(2024, 1, 13, 10, 0, tzinfo=timezone.utc)

        reasoning = scheduler._generate_reasoning(window, 0.3, activity_data)

        # Saturday is in preferred_days, so it mentions preferred day or weekend
        assert "weekend" in reasoning.lower() or "preferred day" in reasoning.lower() or "saturday" in reasoning.lower()

    def test_reasoning_for_early_morning(self, scheduler):
        """Test reasoning mentions early morning."""
        activity_data = {"hourly_patterns": {}, "daily_patterns": {}}
        window = datetime(2024, 1, 15, 4, 0, tzinfo=timezone.utc)

        reasoning = scheduler._generate_reasoning(window, 0.3, activity_data)

        assert "morning" in reasoning.lower() or "preferred" in reasoning.lower()

    def test_reasoning_for_high_impact(self, scheduler):
        """Test reasoning mentions higher disruption."""
        activity_data = {"hourly_patterns": {}, "daily_patterns": {}}
        window = datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)

        reasoning = scheduler._generate_reasoning(window, 0.8, activity_data)

        assert "higher disruption" in reasoning.lower()


@pytest.mark.unit
class TestMainFunction:
    """Test main function CLI behavior."""

    @patch("src.automation.scripts.proactive_maintenance.MaintenanceScheduler")
    @patch("src.automation.scripts.proactive_maintenance.ConfigLoader")
    @patch("src.automation.scripts.proactive_maintenance.GitHubAPIClient")
    def test_main_success(self, MockClient, MockLoader, MockScheduler):
        """Test successful main execution."""
        mock_scheduler = MagicMock()
        mock_window = MagicMock()
        mock_window.scheduled_time = datetime(2024, 1, 15, 2, 0, tzinfo=timezone.utc)
        mock_window.duration_minutes = 30
        mock_window.impact_score = 0.2
        mock_window.confidence = 0.85
        mock_window.reasoning = "Low activity period"
        mock_window.tasks = []
        mock_window.alternatives = []
        mock_scheduler.schedule_maintenance.return_value = mock_window
        MockScheduler.return_value = mock_scheduler

        mock_loader = MagicMock()
        mock_loader.load.return_value = {"maintenance": {}}
        MockLoader.return_value = mock_loader

        with patch(
            "sys.argv",
            [
                "proactive_maintenance.py",
                "--owner",
                "test-org",
                "--repo",
                "test-repo",
                "--task-type",
                "cleanup",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    @patch("src.automation.scripts.proactive_maintenance.MaintenanceScheduler")
    @patch("src.automation.scripts.proactive_maintenance.ConfigLoader")
    @patch("src.automation.scripts.proactive_maintenance.GitHubAPIClient")
    def test_main_with_tasks(self, MockClient, MockLoader, MockScheduler):
        """Test main output with pending tasks."""
        mock_scheduler = MagicMock()
        mock_window = MagicMock()
        mock_window.scheduled_time = datetime(2024, 1, 15, 2, 0, tzinfo=timezone.utc)
        mock_window.duration_minutes = 30
        mock_window.impact_score = 0.2
        mock_window.confidence = 0.85
        mock_window.reasoning = "Low activity period"
        mock_window.tasks = [
            MaintenanceTask(
                task_type="cleanup",
                description="Delete stale branches",
                priority=Priority.P3,
                estimated_duration=5,
                risk_level=RiskLevel.LOW,
            )
        ]
        mock_window.alternatives = []
        mock_scheduler.schedule_maintenance.return_value = mock_window
        MockScheduler.return_value = mock_scheduler

        mock_loader = MagicMock()
        mock_loader.load.return_value = {"maintenance": {}}
        MockLoader.return_value = mock_loader

        with patch(
            "sys.argv",
            [
                "proactive_maintenance.py",
                "--owner",
                "test",
                "--repo",
                "test",
                "--task-type",
                "cleanup",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    @patch("src.automation.scripts.proactive_maintenance.MaintenanceScheduler")
    @patch("src.automation.scripts.proactive_maintenance.ConfigLoader")
    @patch("src.automation.scripts.proactive_maintenance.GitHubAPIClient")
    def test_main_config_not_found(self, MockClient, MockLoader, MockScheduler):
        """Test main handles missing config file."""
        mock_scheduler = MagicMock()
        mock_window = MagicMock()
        mock_window.scheduled_time = datetime.now(timezone.utc)
        mock_window.duration_minutes = 30
        mock_window.impact_score = 0.3
        mock_window.confidence = 0.7
        mock_window.reasoning = "Default config"
        mock_window.tasks = []
        mock_window.alternatives = []
        mock_scheduler.schedule_maintenance.return_value = mock_window
        MockScheduler.return_value = mock_scheduler

        mock_loader = MagicMock()
        mock_loader.load.side_effect = FileNotFoundError()
        MockLoader.return_value = mock_loader

        with patch(
            "sys.argv",
            [
                "proactive_maintenance.py",
                "--owner",
                "test",
                "--repo",
                "test",
                "--task-type",
                "dependency_update",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

    @patch("src.automation.scripts.proactive_maintenance.GitHubAPIClient")
    def test_main_error_exits_1(self, MockClient):
        """Test main exits with code 1 on error."""
        MockClient.side_effect = Exception("API Error")

        with patch(
            "sys.argv",
            [
                "proactive_maintenance.py",
                "--owner",
                "test",
                "--repo",
                "test",
                "--task-type",
                "cleanup",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    @patch("src.automation.scripts.proactive_maintenance.MaintenanceScheduler")
    @patch("src.automation.scripts.proactive_maintenance.ConfigLoader")
    @patch("src.automation.scripts.proactive_maintenance.GitHubAPIClient")
    def test_main_schedule_flag(self, MockClient, MockLoader, MockScheduler, capsys):
        """Test main with --schedule flag."""
        mock_scheduler = MagicMock()
        mock_window = MagicMock()
        mock_window.scheduled_time = datetime(2024, 1, 15, 2, 0, tzinfo=timezone.utc)
        mock_window.duration_minutes = 30
        mock_window.impact_score = 0.2
        mock_window.confidence = 0.85
        mock_window.reasoning = "Low activity"
        mock_window.tasks = []
        mock_window.alternatives = []
        mock_scheduler.schedule_maintenance.return_value = mock_window
        MockScheduler.return_value = mock_scheduler

        mock_loader = MagicMock()
        mock_loader.load.return_value = {"maintenance": {}}
        MockLoader.return_value = mock_loader

        with patch(
            "sys.argv",
            [
                "proactive_maintenance.py",
                "--owner",
                "test",
                "--repo",
                "test",
                "--task-type",
                "cleanup",
                "--schedule",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "Maintenance scheduled" in captured.out

    @patch("src.automation.scripts.proactive_maintenance.MaintenanceScheduler")
    @patch("src.automation.scripts.proactive_maintenance.ConfigLoader")
    @patch("src.automation.scripts.proactive_maintenance.GitHubAPIClient")
    def test_main_with_alternatives(self, MockClient, MockLoader, MockScheduler, capsys):
        """Test main output includes alternatives."""
        mock_scheduler = MagicMock()
        mock_window = MagicMock()
        mock_window.scheduled_time = datetime(2024, 1, 15, 2, 0, tzinfo=timezone.utc)
        mock_window.duration_minutes = 30
        mock_window.impact_score = 0.2
        mock_window.confidence = 0.85
        mock_window.reasoning = "Low activity"
        mock_window.tasks = []
        mock_window.alternatives = [
            {
                "time": "2024-01-16T02:00:00+00:00",
                "impact": 0.25,
                "confidence": 0.8,
            }
        ]
        mock_scheduler.schedule_maintenance.return_value = mock_window
        MockScheduler.return_value = mock_scheduler

        mock_loader = MagicMock()
        mock_loader.load.return_value = {"maintenance": {}}
        MockLoader.return_value = mock_loader

        with patch(
            "sys.argv",
            [
                "proactive_maintenance.py",
                "--owner",
                "test",
                "--repo",
                "test",
                "--task-type",
                "cleanup",
            ],
        ):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Alternative Windows" in captured.out
