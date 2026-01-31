#!/usr/bin/env python3
"""Unit tests for automation/scripts/evaluate_repository.py

Focus: Repository evaluation for workflow deployment readiness.
"""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from evaluate_repository import (
    RepositoryEvaluator,
    RepositoryMetrics,
    evaluate_all_repos,
    main,
)


@pytest.mark.unit
class TestRepositoryMetrics:
    """Test RepositoryMetrics dataclass."""

    def test_creates_metrics(self):
        """Test creates metrics dataclass."""
        metrics = RepositoryMetrics(
            name="test/repo",
            stars=100,
            forks=20,
            open_issues=10,
            open_prs=5,
            activity_score=75.0,
            has_codeowners=True,
            has_contributing=True,
            has_labels=True,
            default_branch="main",
            visibility="PUBLIC",
            language="Python",
            weekly_commits=15,
            total_score=85.0,
            recommendation="EXCELLENT - Highly recommended for pilot",
        )

        assert metrics.name == "test/repo"
        assert metrics.stars == 100
        assert metrics.total_score == 85.0


@pytest.mark.unit
class TestRepositoryEvaluatorInit:
    """Test RepositoryEvaluator initialization."""

    def test_init_parses_repo(self):
        """Test initialization parses repository string."""
        evaluator = RepositoryEvaluator("owner/repo")

        assert evaluator.repo == "owner/repo"
        assert evaluator.owner == "owner"
        assert evaluator.repo_name == "repo"


@pytest.mark.unit
class TestRunGhCommand:
    """Test run_gh_command method."""

    def test_successful_command(self):
        """Test successful gh command execution."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout='{"name": "repo"}', returncode=0
            )

            result = evaluator.run_gh_command(["repo", "view", "test/repo"])

            assert result == {"name": "repo"}

    def test_command_error(self, capsys):
        """Test command error handling."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "gh")

            result = evaluator.run_gh_command(["repo", "view", "test/repo"])

            assert result is None

    def test_json_decode_error(self, capsys):
        """Test JSON decode error handling."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="not json", returncode=0)

            result = evaluator.run_gh_command(["repo", "view", "test/repo"])

            assert result is None


@pytest.mark.unit
class TestGetRepositoryInfo:
    """Test get_repository_info method."""

    def test_gets_repository_info(self):
        """Test gets repository information."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "run_gh_command") as mock_cmd:
            mock_cmd.return_value = {
                "name": "repo",
                "stargazerCount": 50,
                "forkCount": 10,
            }

            result = evaluator.get_repository_info()

            assert result["name"] == "repo"
            mock_cmd.assert_called_once()


@pytest.mark.unit
class TestGetOpenPrs:
    """Test get_open_prs method."""

    def test_gets_open_prs(self):
        """Test gets count of open PRs."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "run_gh_command") as mock_cmd:
            mock_cmd.return_value = [{"number": 1}, {"number": 2}, {"number": 3}]

            result = evaluator.get_open_prs()

            assert result == 3

    def test_returns_zero_on_error(self):
        """Test returns zero on error."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "run_gh_command") as mock_cmd:
            mock_cmd.return_value = None

            result = evaluator.get_open_prs()

            assert result == 0


@pytest.mark.unit
class TestCheckFileExists:
    """Test check_file_exists method."""

    def test_file_exists(self):
        """Test returns True when file exists."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            result = evaluator.check_file_exists("CODEOWNERS")

            assert result is True

    def test_file_not_exists(self):
        """Test returns False when file doesn't exist."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "gh")

            result = evaluator.check_file_exists("CODEOWNERS")

            assert result is False


@pytest.mark.unit
class TestGetCommitActivity:
    """Test get_commit_activity method."""

    def test_gets_commit_activity(self):
        """Test gets commit count."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "run_gh_command") as mock_cmd:
            mock_cmd.return_value = 10

            result = evaluator.get_commit_activity()

            assert result == 10

    def test_returns_zero_on_none(self):
        """Test returns zero when result is None."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "run_gh_command") as mock_cmd:
            mock_cmd.return_value = None

            result = evaluator.get_commit_activity()

            assert result == 0

    def test_returns_zero_on_non_int(self):
        """Test returns zero when result is not int."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "run_gh_command") as mock_cmd:
            mock_cmd.return_value = "not an int"

            result = evaluator.get_commit_activity()

            assert result == 0


@pytest.mark.unit
class TestGetDateWeekAgo:
    """Test _get_date_week_ago method."""

    def test_returns_iso_date(self):
        """Test returns ISO formatted date."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator._get_date_week_ago()

        assert "T" in result  # ISO format includes T


@pytest.mark.unit
class TestCalculateActivityScore:
    """Test calculate_activity_score method."""

    def test_calculates_activity_score(self):
        """Test calculates activity score from commits, PRs, and issues."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"openPRs": 5, "openIssues": 10}

        result = evaluator.calculate_activity_score(info, weekly_commits=5)

        # 5*5 + 5*3 + 10*2 = 25 + 15 + 20 = 60
        assert result == 60

    def test_caps_scores_at_maximum(self):
        """Test caps individual scores at maximum."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"openPRs": 50, "openIssues": 50}

        result = evaluator.calculate_activity_score(info, weekly_commits=50)

        # Max is 40 + 30 + 30 = 100
        assert result == 100


@pytest.mark.unit
class TestCalculateComplexityScore:
    """Test calculate_complexity_score method."""

    def test_ideal_complexity(self):
        """Test ideal complexity for medium repos."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 50, "forkCount": 10}

        result = evaluator.calculate_complexity_score(info)

        assert result == 100

    def test_moderate_complexity(self):
        """Test moderate complexity."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 300, "forkCount": 30}

        result = evaluator.calculate_complexity_score(info)

        assert result == 75

    def test_medium_high_complexity(self):
        """Test medium-high complexity."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 700, "forkCount": 70}

        result = evaluator.calculate_complexity_score(info)

        assert result == 50

    def test_high_complexity(self):
        """Test high complexity for large repos."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 5000, "forkCount": 500}

        result = evaluator.calculate_complexity_score(info)

        assert result == 25


@pytest.mark.unit
class TestCalculateTeamScore:
    """Test calculate_team_score method."""

    def test_full_team_score(self):
        """Test full score with both files."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.calculate_team_score(
            has_codeowners=True, has_contributing=True
        )

        assert result == 100

    def test_partial_team_score(self):
        """Test partial score with one file."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.calculate_team_score(
            has_codeowners=True, has_contributing=False
        )

        assert result == 50

    def test_zero_team_score(self):
        """Test zero score with no files."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.calculate_team_score(
            has_codeowners=False, has_contributing=False
        )

        assert result == 0


@pytest.mark.unit
class TestCalculateMaintenanceScore:
    """Test calculate_maintenance_score method."""

    def test_ideal_maintenance(self):
        """Test ideal maintenance score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"openIssues": 15, "openPRs": 5}

        result = evaluator.calculate_maintenance_score(info)

        assert result == 100

    def test_low_activity(self):
        """Test low activity score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"openIssues": 2, "openPRs": 1}

        result = evaluator.calculate_maintenance_score(info)

        assert result == 80  # 40 + 40

    def test_high_backlog_penalty(self):
        """Test high backlog penalty."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"openIssues": 100, "openPRs": 50}

        result = evaluator.calculate_maintenance_score(info)

        # issue_score = max(0, 50 - 70) = 0
        # pr_score = max(0, 50 - 70) = 0
        assert result == 0


@pytest.mark.unit
class TestCalculateReadinessScore:
    """Test calculate_readiness_score method."""

    def test_full_readiness(self):
        """Test full readiness score."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "check_file_exists") as mock_check:
            mock_check.return_value = True

            result = evaluator.calculate_readiness_score(has_labels=True)

            # 50 (labels) + 25 (.github/README.md) + 25 (.github/workflows)
            assert result == 100

    def test_partial_readiness(self):
        """Test partial readiness score."""
        evaluator = RepositoryEvaluator("test/repo")

        with patch.object(evaluator, "check_file_exists") as mock_check:
            mock_check.return_value = False

            result = evaluator.calculate_readiness_score(has_labels=True)

            assert result == 50


@pytest.mark.unit
class TestCalculateHealthScore:
    """Test calculate_health_score method."""

    def test_high_health(self):
        """Test high health score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 200, "forkCount": 50}

        result = evaluator.calculate_health_score(info)

        assert result == 100

    def test_moderate_health(self):
        """Test moderate health score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 60, "forkCount": 5}

        result = evaluator.calculate_health_score(info)

        assert result == 75

    def test_medium_health(self):
        """Test medium health score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 30, "forkCount": 3}

        result = evaluator.calculate_health_score(info)

        assert result == 50

    def test_low_health(self):
        """Test low health score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 8, "forkCount": 3}

        result = evaluator.calculate_health_score(info)

        assert result == 25

    def test_no_health(self):
        """Test zero health score."""
        evaluator = RepositoryEvaluator("test/repo")
        info = {"stargazerCount": 0, "forkCount": 0}

        result = evaluator.calculate_health_score(info)

        assert result == 0


@pytest.mark.unit
class TestCalculateTotalScore:
    """Test calculate_total_score method."""

    def test_calculates_weighted_total(self):
        """Test calculates weighted total score."""
        evaluator = RepositoryEvaluator("test/repo")
        scores = {
            "complexity": 100,
            "activity": 100,
            "health": 100,
            "team": 100,
            "maintenance": 100,
            "readiness": 100,
        }

        result = evaluator.calculate_total_score(scores)

        assert result == 100.0

    def test_handles_missing_categories(self):
        """Test handles missing score categories."""
        evaluator = RepositoryEvaluator("test/repo")
        scores = {"complexity": 100}  # Missing other categories

        result = evaluator.calculate_total_score(scores)

        # Should only use complexity weight: 100 * 0.15 = 15
        assert result == 15.0


@pytest.mark.unit
class TestGetRecommendation:
    """Test get_recommendation method."""

    def test_excellent_recommendation(self):
        """Test excellent recommendation."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.get_recommendation(85.0)

        assert "EXCELLENT" in result

    def test_good_recommendation(self):
        """Test good recommendation."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.get_recommendation(70.0)

        assert "GOOD" in result

    def test_fair_recommendation(self):
        """Test fair recommendation."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.get_recommendation(50.0)

        assert "FAIR" in result

    def test_poor_recommendation(self):
        """Test poor recommendation."""
        evaluator = RepositoryEvaluator("test/repo")

        result = evaluator.get_recommendation(30.0)

        assert "POOR" in result


@pytest.mark.unit
class TestEvaluate:
    """Test evaluate method."""

    @pytest.fixture
    def mock_evaluator(self):
        """Create evaluator with mocked methods."""
        evaluator = RepositoryEvaluator("test/repo")
        return evaluator

    def test_successful_evaluation(self, mock_evaluator, capsys):
        """Test successful repository evaluation."""
        with patch.object(mock_evaluator, "get_repository_info") as mock_info:
            # Note: openIssues is returned as dict with totalCount from GitHub API
            mock_info.return_value = {
                "stargazerCount": 50,
                "forkCount": 10,
                "openIssues": {"totalCount": 5},
                "defaultBranchRef": {"name": "main"},
                "visibility": "PUBLIC",
                "language": {"name": "Python"},
            }

            with patch.object(mock_evaluator, "get_open_prs", return_value=3):
                with patch.object(mock_evaluator, "check_file_exists", return_value=True):
                    with patch.object(mock_evaluator, "get_commit_activity", return_value=10):
                        # Mock all score calculations since openIssues format varies
                        with patch.object(
                            mock_evaluator, "calculate_activity_score", return_value=75.0
                        ):
                            with patch.object(
                                mock_evaluator, "calculate_maintenance_score", return_value=80.0
                            ):
                                result = mock_evaluator.evaluate()

        assert result is not None
        assert result.name == "test/repo"
        assert result.stars == 50

    def test_failed_evaluation(self, mock_evaluator, capsys):
        """Test failed evaluation when repo info unavailable."""
        with patch.object(mock_evaluator, "get_repository_info") as mock_info:
            mock_info.return_value = None

            result = mock_evaluator.evaluate()

        assert result is None
        captured = capsys.readouterr()
        assert "Failed to get repository" in captured.out


@pytest.mark.unit
class TestPrintResults:
    """Test print_results method."""

    def test_prints_results(self, capsys):
        """Test prints evaluation results."""
        evaluator = RepositoryEvaluator("test/repo")
        metrics = RepositoryMetrics(
            name="test/repo",
            stars=50,
            forks=10,
            open_issues=5,
            open_prs=3,
            activity_score=75.0,
            has_codeowners=True,
            has_contributing=False,
            has_labels=True,
            default_branch="main",
            visibility="PUBLIC",
            language="Python",
            weekly_commits=10,
            total_score=70.0,
            recommendation="GOOD - Suitable for pilot",
        )
        scores = {
            "complexity": 100,
            "activity": 75,
            "health": 75,
            "team": 50,
            "maintenance": 80,
            "readiness": 75,
        }

        evaluator.print_results(metrics, scores)

        captured = capsys.readouterr()
        assert "Stars: 50" in captured.out
        assert "CODEOWNERS" in captured.out
        assert "Total Score" in captured.out


@pytest.mark.unit
class TestEvaluateAllRepos:
    """Test evaluate_all_repos function."""

    def test_evaluates_all_repos(self, tmp_path, capsys):
        """Test evaluates all org repositories."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout='[{"name": "repo1"}, {"name": "repo2"}]',
                returncode=0,
            )

            with patch.object(
                RepositoryEvaluator, "evaluate"
            ) as mock_eval:
                mock_eval.return_value = RepositoryMetrics(
                    name="org/repo1",
                    stars=50,
                    forks=10,
                    open_issues=5,
                    open_prs=3,
                    activity_score=75.0,
                    has_codeowners=True,
                    has_contributing=True,
                    has_labels=True,
                    default_branch="main",
                    visibility="PUBLIC",
                    language="Python",
                    weekly_commits=10,
                    total_score=80.0,
                    recommendation="EXCELLENT",
                )

                # Change to tmp_path to write output file
                import os
                original_dir = os.getcwd()
                os.chdir(tmp_path)
                try:
                    evaluate_all_repos("test-org")
                finally:
                    os.chdir(original_dir)

        captured = capsys.readouterr()
        assert "EVALUATION SUMMARY" in captured.out

    def test_handles_error(self, capsys):
        """Test handles errors listing repos."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("API error")

            evaluate_all_repos("test-org")

        captured = capsys.readouterr()
        assert "Error listing repositories" in captured.out


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_no_args(self, capsys):
        """Test main with no arguments."""
        with patch.object(sys, "argv", ["evaluate_repository.py"]):
            with pytest.raises(SystemExit) as exc:
                main()

            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_main_all_without_org(self, capsys):
        """Test main with --all but no org."""
        with patch.object(sys, "argv", ["evaluate_repository.py", "--all"]):
            with pytest.raises(SystemExit) as exc:
                main()

            assert exc.value.code == 1

        captured = capsys.readouterr()
        assert "requires organization name" in captured.out

    def test_main_all_with_org(self, tmp_path, capsys):
        """Test main with --all and org name."""
        with patch.object(sys, "argv", ["evaluate_repository.py", "--all", "test-org"]):
            with patch("evaluate_repository.evaluate_all_repos") as mock_eval:
                main()

            mock_eval.assert_called_once_with("test-org")

    def test_main_single_repo(self, tmp_path, capsys):
        """Test main with single repo."""
        with patch.object(sys, "argv", ["evaluate_repository.py", "test/repo"]):
            with patch.object(
                RepositoryEvaluator, "evaluate"
            ) as mock_eval:
                mock_eval.return_value = RepositoryMetrics(
                    name="test/repo",
                    stars=50,
                    forks=10,
                    open_issues=5,
                    open_prs=3,
                    activity_score=75.0,
                    has_codeowners=True,
                    has_contributing=True,
                    has_labels=True,
                    default_branch="main",
                    visibility="PUBLIC",
                    language="Python",
                    weekly_commits=10,
                    total_score=80.0,
                    recommendation="EXCELLENT",
                )

                # Change to tmp_path to write output file
                import os
                original_dir = os.getcwd()
                os.chdir(tmp_path)
                try:
                    main()
                finally:
                    os.chdir(original_dir)

        captured = capsys.readouterr()
        assert "Results saved" in captured.out

    def test_main_single_repo_failed(self, capsys):
        """Test main with single repo that fails evaluation."""
        with patch.object(sys, "argv", ["evaluate_repository.py", "test/repo"]):
            with patch.object(
                RepositoryEvaluator, "evaluate"
            ) as mock_eval:
                mock_eval.return_value = None

                main()

        # No "Results saved" since evaluation failed
        captured = capsys.readouterr()
        assert "Results saved" not in captured.out
