#!/usr/bin/env python3
"""Comprehensive unit tests for automation/scripts/self_healing.py

Focus: Self-healing workflow failure detection, classification, and recovery.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from models import (
    FailureClassification,
    FailureType,
    Priority,
    SelfHealingConfig,
    SelfHealingResult,
)
from self_healing import SelfHealingEngine, main


@pytest.fixture
def mock_client():
    """Mock GitHub API client."""
    return MagicMock()


@pytest.fixture
def config():
    """Default self-healing configuration."""
    return SelfHealingConfig(
        enabled=True,
        max_retry_attempts=3,
        initial_retry_delay=10,
        retry_backoff_multiplier=2.0,
        max_consecutive_failures=2,
        dependency_wait_time=60,
        enable_auto_retry=True,
        create_issues_for_failures=True,
        send_notifications=True,
    )


@pytest.fixture
def engine(mock_client, config):
    """Create SelfHealingEngine with mocks."""
    return SelfHealingEngine(mock_client, config)


@pytest.fixture
def failed_run():
    """Sample failed workflow run."""
    return {
        "id": 12345,
        "name": "CI Build",
        "status": "completed",
        "conclusion": "failure",
        "head_branch": "main",
        "event": "push",
        "html_url": "https://github.com/org/repo/actions/runs/12345",
        "workflow_id": 100,
        "run_attempt": 1,
        "repository": {"full_name": "org/repo"},
    }


@pytest.fixture
def failed_jobs():
    """Sample failed workflow jobs."""
    return [
        {
            "id": 1,
            "name": "build",
            "conclusion": "failure",
            "steps": [
                {"name": "Checkout", "conclusion": "success"},
                {"name": "Install dependencies", "conclusion": "success"},
                {"name": "Run tests", "conclusion": "failure"},
            ],
        },
        {
            "id": 2,
            "name": "lint",
            "conclusion": "success",
            "steps": [
                {"name": "Checkout", "conclusion": "success"},
                {"name": "Run linter", "conclusion": "success"},
            ],
        },
    ]


@pytest.fixture
def classification():
    """Sample failure classification."""
    return FailureClassification(
        run_id=12345,
        workflow_name="CI Build",
        failure_type=FailureType.TRANSIENT,
        confidence=0.8,
        reason="Timeout",
        priority=Priority.P2,
        failed_jobs=["build"],
        timestamp=datetime.now(timezone.utc),
    )


@pytest.mark.unit
class TestSelfHealingEngineInit:
    """Test SelfHealingEngine initialization."""

    def test_initializes_with_client_and_config(self, mock_client, config):
        """Test engine initializes with client and config."""
        engine = SelfHealingEngine(mock_client, config)

        assert engine.client == mock_client
        assert engine.config == config
        assert engine.logger is not None


@pytest.mark.unit
class TestGetWorkflowRun:
    """Test _get_workflow_run method."""

    def test_fetches_workflow_run(self, engine, failed_run):
        """Test fetches workflow run from API."""
        engine.client.get.return_value = failed_run

        result = engine._get_workflow_run("org", "repo", 12345)

        engine.client.get.assert_called_once_with(
            "/repos/org/repo/actions/runs/12345"
        )
        assert result == failed_run


@pytest.mark.unit
class TestGetWorkflowJobs:
    """Test _get_workflow_jobs method."""

    def test_fetches_workflow_jobs(self, engine, failed_jobs):
        """Test fetches workflow jobs from API."""
        engine.client.get.return_value = {"jobs": failed_jobs}

        result = engine._get_workflow_jobs("org", "repo", 12345)

        engine.client.get.assert_called_once_with(
            "/repos/org/repo/actions/runs/12345/jobs"
        )
        assert result == failed_jobs

    def test_returns_empty_list_if_no_jobs(self, engine):
        """Test returns empty list if no jobs key."""
        engine.client.get.return_value = {}

        result = engine._get_workflow_jobs("org", "repo", 12345)

        assert result == []


@pytest.mark.unit
class TestClassifyFailure:
    """Test _classify_failure method."""

    def test_classifies_timeout_as_transient(self, engine):
        """Test timed out runs classified as transient."""
        run = {
            "id": 123,
            "name": "CI",
            "conclusion": "timed_out",
            "repository": {"full_name": "org/repo"},
        }

        classification = engine._classify_failure(run, [])

        assert classification.failure_type == FailureType.TRANSIENT
        assert classification.confidence == 0.8
        assert "timed out" in classification.reason.lower()

    def test_classifies_consecutive_failures_as_permanent(self, engine, failed_run):
        """Test multiple consecutive failures classified as permanent."""
        with patch.object(engine, "_has_consecutive_failures", return_value=True):
            classification = engine._classify_failure(failed_run, [])

        assert classification.failure_type == FailureType.PERMANENT
        assert classification.confidence == 0.7
        assert "consecutive" in classification.reason.lower()

    def test_classifies_transient_pattern_in_step(self, engine, failed_run):
        """Test transient patterns in step name are classified correctly."""
        jobs = [
            {
                "name": "build",
                "conclusion": "failure",
                "steps": [
                    {"name": "Connection timeout during install", "conclusion": "failure"}
                ],
            }
        ]

        with patch.object(engine, "_has_consecutive_failures", return_value=False):
            classification = engine._classify_failure(failed_run, jobs)

        assert classification.failure_type == FailureType.TRANSIENT
        assert classification.confidence == 0.75

    def test_classifies_dependency_pattern_in_step(self, engine, failed_run):
        """Test dependency patterns in step name are classified correctly."""
        jobs = [
            {
                "name": "build",
                "conclusion": "failure",
                "steps": [
                    {"name": "Waiting for upstream dependency", "conclusion": "failure"}
                ],
            }
        ]

        with patch.object(engine, "_has_consecutive_failures", return_value=False):
            classification = engine._classify_failure(failed_run, jobs)

        assert classification.failure_type == FailureType.DEPENDENCY
        assert classification.confidence == 0.7

    def test_classifies_permanent_pattern_in_step(self, engine, failed_run):
        """Test permanent failure patterns in step name are classified correctly."""
        jobs = [
            {
                "name": "build",
                "conclusion": "failure",
                "steps": [
                    {"name": "Test failed - assertion error", "conclusion": "failure"}
                ],
            }
        ]

        with patch.object(engine, "_has_consecutive_failures", return_value=False):
            classification = engine._classify_failure(failed_run, jobs)

        assert classification.failure_type == FailureType.PERMANENT
        assert classification.confidence == 0.8

    def test_default_classification_is_transient(self, engine, failed_run):
        """Test unknown failures default to transient."""
        with patch.object(engine, "_has_consecutive_failures", return_value=False):
            classification = engine._classify_failure(failed_run, [])

        assert classification.failure_type == FailureType.TRANSIENT
        assert classification.confidence == 0.5


@pytest.mark.unit
class TestHasConsecutiveFailures:
    """Test _has_consecutive_failures method."""

    def test_returns_true_when_threshold_exceeded(self, engine, failed_run, config):
        """Test returns true when consecutive failures exceed threshold."""
        engine.client.get.return_value = {
            "workflow_runs": [
                {"id": 12346, "conclusion": "failure"},
                {"id": 12347, "conclusion": "failure"},
                {"id": 12348, "conclusion": "success"},
            ]
        }

        result = engine._has_consecutive_failures(failed_run)

        assert result is True

    def test_returns_false_when_under_threshold(self, engine, failed_run):
        """Test returns false when consecutive failures under threshold."""
        engine.client.get.return_value = {
            "workflow_runs": [
                {"id": 12346, "conclusion": "failure"},
                {"id": 12347, "conclusion": "success"},
            ]
        }

        result = engine._has_consecutive_failures(failed_run)

        assert result is False

    def test_skips_current_run(self, engine, failed_run):
        """Test skips the current run when counting."""
        engine.client.get.return_value = {
            "workflow_runs": [
                {"id": 12345, "conclusion": "failure"},  # Current run
                {"id": 12346, "conclusion": "success"},
            ]
        }

        result = engine._has_consecutive_failures(failed_run)

        assert result is False

    def test_handles_api_error_gracefully(self, engine, failed_run):
        """Test handles API errors gracefully."""
        engine.client.get.side_effect = Exception("API error")

        result = engine._has_consecutive_failures(failed_run)

        assert result is False


@pytest.mark.unit
class TestDeterminePriority:
    """Test _determine_priority method."""

    def test_p0_for_production_permanent_failure(self, engine):
        """Test P0 for production workflow with permanent failure."""
        run = {"name": "Production Deploy", "head_branch": "main"}

        priority = engine._determine_priority(run, FailureType.PERMANENT)

        assert priority == Priority.P0

    def test_p1_for_production_transient_failure(self, engine):
        """Test P1 for production workflow with transient failure."""
        run = {"name": "Production Deploy", "head_branch": "main"}

        priority = engine._determine_priority(run, FailureType.TRANSIENT)

        assert priority == Priority.P1

    def test_p1_for_main_branch(self, engine):
        """Test P1 for main branch failures."""
        run = {"name": "CI Build", "head_branch": "main"}

        priority = engine._determine_priority(run, FailureType.TRANSIENT)

        assert priority == Priority.P1

    def test_p2_for_transient_non_main(self, engine):
        """Test P2 for transient failures on non-main branches."""
        run = {"name": "CI Build", "head_branch": "feature-x"}

        priority = engine._determine_priority(run, FailureType.TRANSIENT)

        assert priority == Priority.P2

    def test_p3_for_other_failures(self, engine):
        """Test P3 for other failures."""
        run = {"name": "CI Build", "head_branch": "feature-x"}

        priority = engine._determine_priority(run, FailureType.PERMANENT)

        assert priority == Priority.P3


@pytest.mark.unit
class TestDetermineStrategy:
    """Test _determine_strategy method."""

    def test_retry_for_transient(self, engine):
        """Test retry strategy for transient failures."""
        classification = MagicMock()
        classification.failure_type = FailureType.TRANSIENT

        strategy = engine._determine_strategy(classification)

        assert strategy == "retry_exponential"

    def test_wait_for_dependency(self, engine):
        """Test wait strategy for dependency failures."""
        classification = MagicMock()
        classification.failure_type = FailureType.DEPENDENCY

        strategy = engine._determine_strategy(classification)

        assert strategy == "wait_and_retry"

    def test_alert_for_permanent(self, engine):
        """Test alert strategy for permanent failures."""
        classification = MagicMock()
        classification.failure_type = FailureType.PERMANENT

        strategy = engine._determine_strategy(classification)

        assert strategy == "alert_and_escalate"

    def test_manual_for_unknown(self, engine):
        """Test manual strategy for unknown failures."""
        classification = MagicMock()
        classification.failure_type = None

        strategy = engine._determine_strategy(classification)

        assert strategy == "manual_intervention"


@pytest.mark.unit
class TestExecuteStrategy:
    """Test _execute_strategy method."""

    def test_executes_retry_exponential(self, engine, failed_run, classification):
        """Test executes retry_exponential strategy."""
        with patch.object(engine, "_retry_exponential") as mock_retry:
            mock_retry.return_value = MagicMock()
            engine._execute_strategy(
                "org", "repo", failed_run, classification, "retry_exponential"
            )

        mock_retry.assert_called_once()

    def test_executes_wait_and_retry(self, engine, failed_run, classification):
        """Test executes wait_and_retry strategy."""
        with patch.object(engine, "_wait_and_retry") as mock_wait:
            mock_wait.return_value = MagicMock()
            engine._execute_strategy(
                "org", "repo", failed_run, classification, "wait_and_retry"
            )

        mock_wait.assert_called_once()

    def test_executes_alert_and_escalate(self, engine, failed_run, classification):
        """Test executes alert_and_escalate strategy."""
        with patch.object(engine, "_alert_and_escalate") as mock_alert:
            mock_alert.return_value = MagicMock()
            engine._execute_strategy(
                "org", "repo", failed_run, classification, "alert_and_escalate"
            )

        mock_alert.assert_called_once()

    def test_executes_manual_intervention_for_unknown(self, engine, failed_run, classification):
        """Test executes manual_intervention for unknown strategy."""
        with patch.object(engine, "_manual_intervention") as mock_manual:
            mock_manual.return_value = MagicMock()
            engine._execute_strategy(
                "org", "repo", failed_run, classification, "unknown_strategy"
            )

        mock_manual.assert_called_once()


@pytest.mark.unit
class TestRetryExponential:
    """Test _retry_exponential method."""

    def test_retries_when_under_max_attempts(self, engine, failed_run, classification):
        """Test retries when under max attempts."""
        with patch.object(engine, "_get_retry_count", return_value=0):
            with patch.object(engine, "_rerun_workflow", return_value=True):
                with patch(
                    "self_healing.notify_self_healing_success"
                ) as mock_notify:
                    result = engine._retry_exponential(
                        "org", "repo", failed_run, classification
                    )

        assert result.healed is True
        assert result.strategy == "retry_exponential"
        assert result.retry_count == 1
        mock_notify.assert_called_once()

    def test_fails_when_max_attempts_reached(self, engine, failed_run, classification):
        """Test fails when max attempts reached."""
        with patch.object(engine, "_get_retry_count", return_value=3):
            result = engine._retry_exponential(
                "org", "repo", failed_run, classification
            )

        assert result.healed is False
        assert "Max retry attempts" in result.resolution

    def test_sends_failure_notification_on_failed_retry(self, engine, failed_run, classification):
        """Test sends failure notification when retry fails."""
        with patch.object(engine, "_get_retry_count", return_value=0):
            with patch.object(engine, "_rerun_workflow", return_value=False):
                with patch(
                    "self_healing.notify_self_healing_failure"
                ) as mock_notify:
                    result = engine._retry_exponential(
                        "org", "repo", failed_run, classification
                    )

        assert result.healed is False
        mock_notify.assert_called_once()

    def test_skips_retry_when_disabled(self, engine, failed_run, classification):
        """Test skips retry when auto-retry disabled."""
        engine.config.enable_auto_retry = False

        with patch.object(engine, "_get_retry_count", return_value=0):
            result = engine._retry_exponential(
                "org", "repo", failed_run, classification
            )

        assert result.healed is False
        assert "Auto-retry disabled" in result.resolution


@pytest.mark.unit
class TestWaitAndRetry:
    """Test _wait_and_retry method."""

    def test_waits_and_retries_successfully(self, engine, failed_run):
        """Test waits for dependencies and retries."""
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.DEPENDENCY,
            confidence=0.7,
            reason="Dependency failure",
            priority=Priority.P2,
            failed_jobs=["build"],
            timestamp=datetime.now(timezone.utc),
        )

        with patch.object(engine, "_rerun_workflow", return_value=True):
            with patch("self_healing.notify_self_healing_success") as mock_notify:
                with patch("self_healing.time.sleep"):
                    result = engine._wait_and_retry(
                        "org", "repo", failed_run, classification
                    )

        assert result.healed is True
        assert result.strategy == "wait_and_retry"
        mock_notify.assert_called_once()

    def test_sends_failure_notification_on_failed_retry(self, engine, failed_run):
        """Test sends failure notification when retry fails."""
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.DEPENDENCY,
            confidence=0.7,
            reason="Dependency failure",
            priority=Priority.P2,
            failed_jobs=["build"],
            timestamp=datetime.now(timezone.utc),
        )

        with patch.object(engine, "_rerun_workflow", return_value=False):
            with patch("self_healing.notify_self_healing_failure") as mock_notify:
                with patch("self_healing.time.sleep"):
                    result = engine._wait_and_retry(
                        "org", "repo", failed_run, classification
                    )

        assert result.healed is False
        mock_notify.assert_called_once()

    def test_skips_retry_when_disabled(self, engine, failed_run):
        """Test skips retry when auto-retry disabled."""
        engine.config.enable_auto_retry = False
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.DEPENDENCY,
            confidence=0.7,
            reason="Dependency failure",
            priority=Priority.P2,
            failed_jobs=["build"],
            timestamp=datetime.now(timezone.utc),
        )

        result = engine._wait_and_retry("org", "repo", failed_run, classification)

        assert result.healed is False
        assert "Auto-retry disabled" in result.resolution


@pytest.mark.unit
class TestAlertAndEscalate:
    """Test _alert_and_escalate method."""

    def test_creates_issue_and_sends_notification(self, engine, failed_run):
        """Test creates issue and sends notification for permanent failure."""
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.PERMANENT,
            confidence=0.8,
            reason="Test failure",
            priority=Priority.P0,
            failed_jobs=["build"],
            timestamp=datetime.now(timezone.utc),
        )

        with patch.object(engine, "_create_failure_issue", return_value=42):
            with patch("self_healing.notify_self_healing_failure") as mock_notify:
                result = engine._alert_and_escalate(
                    "org", "repo", failed_run, classification
                )

        assert result.healed is False
        assert result.strategy == "alert_and_escalate"
        assert any("issue #42" in action for action in result.actions_taken)
        mock_notify.assert_called_once()

    def test_skips_issue_when_disabled(self, engine, failed_run):
        """Test skips issue creation when disabled."""
        engine.config.create_issues_for_failures = False
        classification = FailureClassification(
            run_id=12345,
            workflow_name="CI",
            failure_type=FailureType.PERMANENT,
            confidence=0.8,
            reason="Test failure",
            priority=Priority.P0,
            failed_jobs=["build"],
            timestamp=datetime.now(timezone.utc),
        )

        with patch("self_healing.notify_self_healing_failure"):
            result = engine._alert_and_escalate(
                "org", "repo", failed_run, classification
            )

        assert not any("issue" in action.lower() for action in result.actions_taken)


@pytest.mark.unit
class TestManualIntervention:
    """Test _manual_intervention method."""

    def test_returns_manual_intervention_result(self, engine, failed_run, classification):
        """Test returns manual intervention result."""
        result = engine._manual_intervention(
            "org", "repo", failed_run, classification
        )

        assert result.healed is False
        assert result.strategy == "manual_intervention"
        assert "manual" in result.resolution.lower()


@pytest.mark.unit
class TestGetRetryCount:
    """Test _get_retry_count method."""

    def test_returns_retry_count_from_run(self, engine, failed_run):
        """Test returns retry count from run_attempt."""
        failed_run["run_attempt"] = 3
        engine.client.get.return_value = failed_run

        count = engine._get_retry_count("org", "repo", 12345)

        assert count == 2  # run_attempt - 1

    def test_returns_zero_on_error(self, engine):
        """Test returns zero on API error."""
        engine.client.get.side_effect = OSError("Network error")

        count = engine._get_retry_count("org", "repo", 12345)

        assert count == 0

    def test_returns_zero_on_key_error(self, engine):
        """Test returns zero on missing run_attempt key."""
        engine.client.get.return_value = {}

        count = engine._get_retry_count("org", "repo", 12345)

        assert count == 0


@pytest.mark.unit
class TestRerunWorkflow:
    """Test _rerun_workflow method."""

    def test_reruns_workflow_successfully(self, engine):
        """Test successfully re-runs workflow."""
        engine.client.post.return_value = {}

        result = engine._rerun_workflow("org", "repo", 12345)

        assert result is True
        engine.client.post.assert_called_once_with(
            "/repos/org/repo/actions/runs/12345/rerun"
        )

    def test_returns_false_on_error(self, engine):
        """Test returns false on API error."""
        engine.client.post.side_effect = Exception("API error")

        result = engine._rerun_workflow("org", "repo", 12345)

        assert result is False


@pytest.mark.unit
class TestCreateFailureIssue:
    """Test _create_failure_issue method."""

    def test_creates_issue_successfully(self, engine, failed_run):
        """Test creates GitHub issue for failure."""
        classification = MagicMock()
        classification.failure_type = FailureType.PERMANENT
        classification.priority = Priority.P0
        classification.confidence = 0.8
        classification.reason = "Test failure"
        classification.failed_jobs = ["build"]

        engine.client.post.return_value = {"number": 42}

        issue_number = engine._create_failure_issue(
            "org", "repo", failed_run, classification
        )

        assert issue_number == 42
        engine.client.post.assert_called_once()

    def test_returns_none_on_error(self, engine, failed_run):
        """Test returns None on API error."""
        classification = MagicMock()
        classification.failure_type = FailureType.PERMANENT
        classification.priority = Priority.P0
        classification.confidence = 0.8
        classification.reason = "Test failure"
        classification.failed_jobs = []

        engine.client.post.side_effect = Exception("API error")

        issue_number = engine._create_failure_issue(
            "org", "repo", failed_run, classification
        )

        assert issue_number is None


@pytest.mark.unit
class TestAnalyzeAndHeal:
    """Test analyze_and_heal method."""

    def test_full_healing_workflow(self, engine, failed_run, failed_jobs):
        """Test complete healing workflow."""
        # Mock _get_retry_count to avoid additional API calls
        def mock_get(*args, **kwargs):
            endpoint = args[0] if args else ""
            if "runs/12345/jobs" in endpoint:
                return {"jobs": failed_jobs}
            elif "runs/12345" in endpoint:
                return failed_run
            elif "workflows/" in endpoint:
                return {"workflow_runs": []}
            return failed_run

        engine.client.get.side_effect = mock_get

        with patch.object(engine, "_rerun_workflow", return_value=True):
            with patch("self_healing.notify_self_healing_success"):
                result = engine.analyze_and_heal("org", "repo", 12345)

        assert isinstance(result, SelfHealingResult)
        assert result.repository == "org/repo"

    def test_raises_for_non_failed_run(self, engine):
        """Test raises error for non-failed run."""
        engine.client.get.return_value = {
            "id": 12345,
            "status": "completed",
            "conclusion": "success",
        }

        with pytest.raises(ValueError, match="not a failed run"):
            engine.analyze_and_heal("org", "repo", 12345)

    def test_raises_for_in_progress_run(self, engine):
        """Test raises error for in-progress run."""
        engine.client.get.return_value = {
            "id": 12345,
            "status": "in_progress",
            "conclusion": None,
        }

        with pytest.raises(ValueError, match="not a failed run"):
            engine.analyze_and_heal("org", "repo", 12345)


@pytest.mark.unit
class TestMainFunction:
    """Test main() function."""

    def test_main_successful_healing(self, capsys):
        """Test main with successful healing."""
        mock_result = SelfHealingResult(
            run_id=12345,
            repository="org/repo",
            classification=FailureClassification(
                run_id=12345,
                workflow_name="CI",
                failure_type=FailureType.TRANSIENT,
                confidence=0.8,
                reason="Timeout",
                priority=Priority.P2,
                failed_jobs=["build"],
                timestamp=datetime.now(timezone.utc),
            ),
            strategy="retry_exponential",
            healed=True,
            resolution="Workflow re-run initiated",
            retry_count=1,
            actions_taken=["Retry succeeded"],
            timestamp=datetime.now(timezone.utc),
        )

        with patch(
            "sys.argv",
            ["self_healing.py", "--owner", "org", "--repo", "repo", "--run-id", "12345"],
        ):
            with patch("self_healing.GitHubAPIClient"):
                with patch("self_healing.ConfigLoader") as mock_loader:
                    mock_loader.return_value.load.side_effect = FileNotFoundError()
                    with patch.object(
                        SelfHealingEngine, "analyze_and_heal", return_value=mock_result
                    ):
                        with pytest.raises(SystemExit) as exc_info:
                            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Healed: ✅ Yes" in captured.out

    def test_main_failed_healing(self, capsys):
        """Test main with failed healing."""
        mock_result = SelfHealingResult(
            run_id=12345,
            repository="org/repo",
            classification=FailureClassification(
                run_id=12345,
                workflow_name="CI",
                failure_type=FailureType.PERMANENT,
                confidence=0.8,
                reason="Test failure",
                priority=Priority.P1,
                failed_jobs=["build"],
                timestamp=datetime.now(timezone.utc),
            ),
            strategy="alert_and_escalate",
            healed=False,
            resolution="Manual intervention required",
            retry_count=0,
            actions_taken=["Alerted team"],
            timestamp=datetime.now(timezone.utc),
        )

        with patch(
            "sys.argv",
            ["self_healing.py", "--owner", "org", "--repo", "repo", "--run-id", "12345"],
        ):
            with patch("self_healing.GitHubAPIClient"):
                with patch("self_healing.ConfigLoader") as mock_loader:
                    mock_loader.return_value.load.return_value = {"self_healing": {}}
                    with patch.object(
                        SelfHealingEngine, "analyze_and_heal", return_value=mock_result
                    ):
                        with pytest.raises(SystemExit) as exc_info:
                            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Healed: ❌ No" in captured.out

    def test_main_with_debug_flag(self, capsys):
        """Test main with debug flag."""
        with patch(
            "sys.argv",
            [
                "self_healing.py",
                "--owner", "org",
                "--repo", "repo",
                "--run-id", "12345",
                "--debug",
            ],
        ):
            with patch("self_healing.GitHubAPIClient"):
                with patch("self_healing.ConfigLoader") as mock_loader:
                    mock_loader.return_value.load.side_effect = FileNotFoundError()
                    with patch.object(
                        SelfHealingEngine, "analyze_and_heal"
                    ) as mock_heal:
                        mock_heal.return_value = MagicMock(
                            healed=True,
                            run_id=12345,
                            repository="org/repo",
                            timestamp=datetime.now(timezone.utc),
                            classification=MagicMock(
                                failure_type=FailureType.TRANSIENT,
                                confidence=0.8,
                                priority=Priority.P2,
                                reason="Test",
                            ),
                            strategy="retry",
                            resolution="Done",
                            retry_count=1,
                            actions_taken=["Test"],
                        )
                        with pytest.raises(SystemExit) as exc_info:
                            main()

        assert exc_info.value.code == 0

    def test_main_exception_handling(self, capsys):
        """Test main handles exceptions."""
        with patch(
            "sys.argv",
            ["self_healing.py", "--owner", "org", "--repo", "repo", "--run-id", "12345"],
        ):
            with patch("self_healing.GitHubAPIClient") as mock_client:
                mock_client.side_effect = Exception("Connection failed")
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 2
