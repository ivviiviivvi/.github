#!/usr/bin/env python3
"""Unit tests for automation/scripts/check_auto_merge_eligibility.py
Focus: AutoMergeChecker safety checks, eligibility determination, confidence calculation.
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from check_auto_merge_eligibility import AutoMergeChecker
from models import AutoMergeConfig, AutoMergeSafetyChecks


class TestAutoMergeChecker:
    """Test AutoMergeChecker class."""

    @pytest.fixture
    def mock_client(self):
        """Create mock GitHub client."""
        client = MagicMock()
        return client

    @pytest.fixture
    def default_config(self):
        """Create default config."""
        return AutoMergeConfig()

    @pytest.fixture
    def checker(self, mock_client, default_config):
        """Create checker instance."""
        return AutoMergeChecker(mock_client, default_config)

    def test_initialization(self, mock_client, default_config):
        """Test checker initializes correctly."""
        checker = AutoMergeChecker(mock_client, default_config)
        assert checker.client == mock_client
        assert checker.config == default_config


class TestSafetyChecks:
    """Test individual safety check methods."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def checker(self, mock_client):
        config = AutoMergeConfig(
            min_reviews=2,
            coverage_threshold=80.0,
            required_checks=["ci", "lint"],
        )
        return AutoMergeChecker(mock_client, config)

    def test_check_tests_passed_success(self, checker, mock_client):
        """Test _check_tests_passed returns True when all pass."""
        # Mock commit status
        mock_client.get.side_effect = [
            {"state": "success"},  # commit status
            {
                "check_runs": [
                    {"name": "ci", "conclusion": "success"},
                    {"name": "lint", "conclusion": "success"},
                ]
            },
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_tests_passed("owner", "repo", pr)

        assert result is True

    def test_check_tests_passed_failure(self, checker, mock_client):
        """Test _check_tests_passed returns False when status fails."""
        mock_client.get.return_value = {"state": "failure"}

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_tests_passed("owner", "repo", pr)

        assert result is False

    def test_check_tests_passed_missing_required(self, checker, mock_client):
        """Test _check_tests_passed returns False when required check missing."""
        mock_client.get.side_effect = [
            {"state": "success"},
            {
                "check_runs": [
                    {"name": "ci", "conclusion": "success"},
                    # "lint" check is missing
                ]
            },
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_tests_passed("owner", "repo", pr)

        assert result is False

    def test_check_reviews_approved_success(self, checker, mock_client):
        """Test _check_reviews_approved returns True with enough approvals."""
        mock_client.get.return_value = [
            {"user": {"login": "user1"}, "state": "APPROVED"},
            {"user": {"login": "user2"}, "state": "APPROVED"},
        ]

        pr = {"number": 123}
        result = checker._check_reviews_approved("owner", "repo", pr)

        assert result is True

    def test_check_reviews_approved_insufficient(self, checker, mock_client):
        """Test _check_reviews_approved returns False with insufficient approvals."""
        mock_client.get.return_value = [
            {"user": {"login": "user1"}, "state": "APPROVED"},
            {"user": {"login": "user2"}, "state": "CHANGES_REQUESTED"},
        ]

        pr = {"number": 123}
        result = checker._check_reviews_approved("owner", "repo", pr)

        assert result is False

    def test_check_reviews_keeps_latest_per_reviewer(self, checker, mock_client):
        """Test only latest review per reviewer is counted."""
        mock_client.get.return_value = [
            {"user": {"login": "user1"}, "state": "CHANGES_REQUESTED"},
            {"user": {"login": "user1"}, "state": "APPROVED"},  # Latest
            {"user": {"login": "user2"}, "state": "APPROVED"},
        ]

        pr = {"number": 123}
        result = checker._check_reviews_approved("owner", "repo", pr)

        assert result is True

    def test_check_no_conflicts_mergeable(self, checker):
        """Test _check_no_conflicts returns True when mergeable."""
        pr = {"mergeable": True}
        result = checker._check_no_conflicts(pr)
        assert result is True

    def test_check_no_conflicts_not_mergeable(self, checker):
        """Test _check_no_conflicts returns False when not mergeable."""
        pr = {"mergeable": False}
        result = checker._check_no_conflicts(pr)
        assert result is False

    def test_check_no_conflicts_unknown(self, checker):
        """Test _check_no_conflicts returns False when mergeable is None."""
        pr = {"mergeable": None}
        result = checker._check_no_conflicts(pr)
        assert result is False

    def test_check_branch_up_to_date_clean(self, checker):
        """Test _check_branch_up_to_date returns True for clean state."""
        pr = {"mergeable_state": "clean"}
        result = checker._check_branch_up_to_date(pr)
        assert result is True

    def test_check_branch_up_to_date_behind(self, checker):
        """Test _check_branch_up_to_date returns False for behind state."""
        pr = {"mergeable_state": "behind"}
        result = checker._check_branch_up_to_date(pr)
        assert result is False

    def test_check_branch_up_to_date_dirty(self, checker):
        """Test _check_branch_up_to_date returns False for dirty state."""
        pr = {"mergeable_state": "dirty"}
        result = checker._check_branch_up_to_date(pr)
        assert result is False


class TestCoverageThreshold:
    """Test coverage threshold checking."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_coverage_from_status(self, mock_client):
        """Test extracts coverage from commit status."""
        config = AutoMergeConfig(coverage_threshold=80.0)
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"statuses": [{"context": "codecov/patch", "description": "Coverage: 85.5%"}]},
            {"check_runs": []},
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_coverage_threshold("owner", "repo", pr)

        assert result is True

    def test_coverage_below_threshold(self, mock_client):
        """Test returns False when coverage below threshold."""
        config = AutoMergeConfig(coverage_threshold=80.0)
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"statuses": [{"context": "codecov/patch", "description": "Coverage: 75.0%"}]},
            {"check_runs": []},
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_coverage_threshold("owner", "repo", pr)

        assert result is False

    def test_coverage_from_check_runs(self, mock_client):
        """Test extracts coverage from check runs."""
        config = AutoMergeConfig(coverage_threshold=80.0)
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"statuses": []},  # No status
            {
                "check_runs": [
                    {
                        "name": "Codecov Report",
                        "output": {"summary": "Total coverage: 90%"},
                    }
                ]
            },
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_coverage_threshold("owner", "repo", pr)

        assert result is True

    def test_coverage_zero_threshold_passes(self, mock_client):
        """Test zero coverage threshold always passes."""
        config = AutoMergeConfig(coverage_threshold=0)
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"statuses": []},
            {"check_runs": []},
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_coverage_threshold("owner", "repo", pr)

        assert result is True

    def test_coverage_handles_api_error(self, mock_client):
        """Test handles API error gracefully."""
        config = AutoMergeConfig(coverage_threshold=80.0)
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = Exception("API Error")

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_coverage_threshold("owner", "repo", pr)

        # Should fail safe
        assert result is False


class TestConfidenceCalculation:
    """Test confidence score calculation."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def checker(self, mock_client):
        return AutoMergeChecker(mock_client, AutoMergeConfig())

    def test_confidence_all_checks_passed(self, checker):
        """Test confidence with all checks passed."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )

        # Recent PR with few commits and files
        pr = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "commits": 3,
            "changed_files": 2,
        }

        confidence = checker._calculate_confidence(pr, checks)

        # Should have high confidence (> 0.5 at minimum from checks)
        assert confidence >= 0.5
        assert confidence <= 1.0

    def test_confidence_no_checks_passed(self, checker):
        """Test confidence with no checks passed."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=False,
            reviews_approved=False,
            no_conflicts=False,
            branch_up_to_date=False,
            coverage_threshold_met=False,
        )

        pr = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "commits": 50,
            "changed_files": 30,
        }

        confidence = checker._calculate_confidence(pr, checks)

        # Should have low confidence
        assert confidence < 0.5

    def test_confidence_increases_with_age(self, checker):
        """Test confidence increases with PR age."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )

        # Recent PR
        recent_pr = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "commits": 3,
            "changed_files": 2,
        }

        # Older PR (7 days)
        old_pr = {
            "created_at": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            "commits": 3,
            "changed_files": 2,
        }

        recent_confidence = checker._calculate_confidence(recent_pr, checks)
        old_confidence = checker._calculate_confidence(old_pr, checks)

        assert old_confidence > recent_confidence

    def test_confidence_decreases_with_commits(self, checker):
        """Test confidence decreases with more commits."""
        checks = AutoMergeSafetyChecks(
            all_tests_passed=True,
            reviews_approved=True,
            no_conflicts=True,
            branch_up_to_date=True,
            coverage_threshold_met=True,
        )

        few_commits = {
            "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "commits": 3,
            "changed_files": 2,
        }

        many_commits = {
            "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "commits": 50,
            "changed_files": 2,
        }

        few_confidence = checker._calculate_confidence(few_commits, checks)
        many_confidence = checker._calculate_confidence(many_commits, checks)

        assert few_confidence > many_confidence


class TestCheckEligibility:
    """Test full eligibility check flow."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def checker(self, mock_client):
        config = AutoMergeConfig(min_reviews=1, coverage_threshold=80.0)
        return AutoMergeChecker(mock_client, config)

    def test_eligible_pr(self, checker, mock_client):
        """Test PR that passes all checks is eligible."""
        # Mock all API calls in order they are made
        # Note: check_runs not fetched since required_checks is empty
        mock_client.get.side_effect = [
            # PR details
            {
                "number": 123,
                "head": {"sha": "abc123"},
                "mergeable": True,
                "mergeable_state": "clean",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "commits": 3,
                "changed_files": 2,
            },
            # Commit status for tests
            {"state": "success"},
            # Reviews
            [{"user": {"login": "user1"}, "state": "APPROVED"}],
            # Coverage status
            {"statuses": [{"context": "codecov/patch", "description": "Coverage: 85%"}]},
        ]

        result = checker.check_eligibility("owner", "repo", 123)

        assert result.eligible is True
        assert result.pr_number == 123
        assert result.repository == "owner/repo"
        assert len(result.reasons) == 0

    def test_ineligible_pr_failing_tests(self, checker, mock_client):
        """Test PR with failing tests is not eligible."""
        mock_client.get.side_effect = [
            # PR details
            {
                "number": 123,
                "head": {"sha": "abc123"},
                "mergeable": True,
                "mergeable_state": "clean",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "commits": 3,
                "changed_files": 2,
            },
            # Commit status - FAILING
            {"state": "failure"},
            # Reviews
            [{"user": {"login": "user1"}, "state": "APPROVED"}],
            # Coverage
            {"statuses": [{"context": "codecov/patch", "description": "Coverage: 85%"}]},
            {"check_runs": []},
        ]

        result = checker.check_eligibility("owner", "repo", 123)

        assert result.eligible is False
        assert "CI tests have not all passed" in result.reasons

    def test_ineligible_pr_missing_reviews(self, checker, mock_client):
        """Test PR with missing reviews is not eligible."""
        # Note: check_runs not fetched since required_checks is empty
        mock_client.get.side_effect = [
            # PR details
            {
                "number": 123,
                "head": {"sha": "abc123"},
                "mergeable": True,
                "mergeable_state": "clean",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "commits": 3,
                "changed_files": 2,
            },
            # Commit status
            {"state": "success"},
            # Reviews - NO APPROVALS
            [{"user": {"login": "user1"}, "state": "CHANGES_REQUESTED"}],
            # Coverage
            {"statuses": [{"context": "codecov/patch", "description": "Coverage: 85%"}]},
        ]

        result = checker.check_eligibility("owner", "repo", 123)

        assert result.eligible is False
        assert any("Missing required approvals" in r for r in result.reasons)

    def test_ineligible_pr_with_conflicts(self, checker, mock_client):
        """Test PR with merge conflicts is not eligible."""
        # Note: check_runs not fetched since required_checks is empty
        mock_client.get.side_effect = [
            # PR details - has conflicts
            {
                "number": 123,
                "head": {"sha": "abc123"},
                "mergeable": False,
                "mergeable_state": "dirty",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "commits": 3,
                "changed_files": 2,
            },
            # Commit status
            {"state": "success"},
            # Reviews
            [{"user": {"login": "user1"}, "state": "APPROVED"}],
            # Coverage
            {"statuses": [{"context": "codecov/patch", "description": "Coverage: 85%"}]},
        ]

        result = checker.check_eligibility("owner", "repo", 123)

        assert result.eligible is False
        assert "PR has merge conflicts" in result.reasons

    def test_multiple_failure_reasons(self, checker, mock_client):
        """Test PR with multiple issues reports all reasons."""
        mock_client.get.side_effect = [
            # PR details - conflicts and behind
            {
                "number": 123,
                "head": {"sha": "abc123"},
                "mergeable": False,
                "mergeable_state": "behind",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "commits": 3,
                "changed_files": 2,
            },
            # Commit status - failing
            {"state": "failure"},
            # Reviews - not approved
            [],
            # Coverage - missing
            {"statuses": []},
            {"check_runs": []},
        ]

        result = checker.check_eligibility("owner", "repo", 123)

        assert result.eligible is False
        assert len(result.reasons) >= 3  # Multiple reasons


@pytest.mark.unit
class TestRequiredChecksFailed:
    """Test required checks with failed status."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_required_check_failed(self, mock_client):
        """Test returns False when required check exists but failed."""
        config = AutoMergeConfig(
            min_reviews=1,
            coverage_threshold=0,
            required_checks=["ci", "lint"],
        )
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"state": "success"},  # commit status
            {
                "check_runs": [
                    {"name": "ci", "conclusion": "success"},
                    {"name": "lint", "conclusion": "failure"},  # FAILED
                ]
            },
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_tests_passed("owner", "repo", pr)

        assert result is False

    def test_required_check_skipped(self, mock_client):
        """Test returns False when required check was skipped."""
        config = AutoMergeConfig(
            min_reviews=1,
            coverage_threshold=0,
            required_checks=["ci"],
        )
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"state": "success"},
            {
                "check_runs": [
                    {"name": "ci", "conclusion": "skipped"},
                ]
            },
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_tests_passed("owner", "repo", pr)

        assert result is False

    def test_required_check_cancelled(self, mock_client):
        """Test returns False when required check was cancelled."""
        config = AutoMergeConfig(
            min_reviews=1,
            coverage_threshold=0,
            required_checks=["ci"],
        )
        checker = AutoMergeChecker(mock_client, config)

        mock_client.get.side_effect = [
            {"state": "success"},
            {
                "check_runs": [
                    {"name": "ci", "conclusion": "cancelled"},
                ]
            },
        ]

        pr = {"head": {"sha": "abc123"}}
        result = checker._check_tests_passed("owner", "repo", pr)

        assert result is False


@pytest.mark.unit
class TestMainCLI:
    """Test main CLI entry point."""

    @pytest.fixture
    def mock_pr_response(self):
        """Standard PR response for testing."""
        return {
            "number": 42,
            "head": {"sha": "abc123"},
            "mergeable": True,
            "mergeable_state": "clean",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "commits": 3,
            "changed_files": 2,
        }

    def test_main_eligible_pr(self, mock_pr_response, capsys):
        """Test CLI with eligible PR exits 0."""
        from unittest.mock import patch

        with patch("sys.argv", ["prog", "--owner", "org", "--repo", "repo", "--pr", "42"]):
            with patch("check_auto_merge_eligibility.GitHubAPIClient") as mock_client_class:
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client

                mock_client.get.side_effect = [
                    mock_pr_response,
                    {"state": "success"},  # tests
                    [{"user": {"login": "u1"}, "state": "APPROVED"}],  # reviews
                    {"statuses": [{"context": "codecov", "description": "85%"}]},  # coverage
                ]

                with patch("check_auto_merge_eligibility.ConfigLoader") as mock_config_loader:
                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from check_auto_merge_eligibility import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 0

                    captured = capsys.readouterr()
                    assert "Eligible: ✅ YES" in captured.out

    def test_main_ineligible_pr(self, mock_pr_response, capsys):
        """Test CLI with ineligible PR exits 1."""
        from unittest.mock import patch

        with patch("sys.argv", ["prog", "--owner", "org", "--repo", "repo", "--pr", "42"]):
            with patch("check_auto_merge_eligibility.GitHubAPIClient") as mock_client_class:
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client

                mock_client.get.side_effect = [
                    mock_pr_response,
                    {"state": "failure"},  # tests failed
                    [],  # no reviews
                    {"statuses": []},
                    {"check_runs": []},
                ]

                with patch("check_auto_merge_eligibility.ConfigLoader") as mock_config_loader:
                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from check_auto_merge_eligibility import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 1

                    captured = capsys.readouterr()
                    assert "Eligible: ❌ NO" in captured.out
                    assert "Reasons for ineligibility" in captured.out

    def test_main_with_custom_config(self, mock_pr_response, capsys):
        """Test CLI loads custom config."""
        from unittest.mock import patch

        with patch("sys.argv", ["prog", "--owner", "org", "--repo", "repo", "--pr", "42", "--config", "custom.yml"]):
            with patch("check_auto_merge_eligibility.GitHubAPIClient") as mock_client_class:
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client

                mock_client.get.side_effect = [
                    mock_pr_response,
                    {"state": "success"},
                    [{"user": {"login": "u1"}, "state": "APPROVED"}],
                    {"statuses": [{"context": "codecov", "description": "85%"}]},
                ]

                with patch("check_auto_merge_eligibility.ConfigLoader") as mock_config_loader:
                    mock_config_loader.return_value.load.return_value = {"auto_merge": {"min_reviews": 1}}

                    from check_auto_merge_eligibility import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 0

    def test_main_with_debug_flag(self, mock_pr_response, capsys):
        """Test CLI with debug flag runs successfully."""
        from unittest.mock import patch

        with patch("sys.argv", ["prog", "--owner", "org", "--repo", "repo", "--pr", "42", "--debug"]):
            with patch("check_auto_merge_eligibility.GitHubAPIClient") as mock_client_class:
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client

                mock_client.get.side_effect = [
                    mock_pr_response,
                    {"state": "success"},
                    [{"user": {"login": "u1"}, "state": "APPROVED"}],
                    {"statuses": [{"context": "codecov", "description": "85%"}]},
                ]

                with patch("check_auto_merge_eligibility.ConfigLoader") as mock_config_loader:
                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from check_auto_merge_eligibility import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    # Debug flag shouldn't affect the outcome
                    assert exc_info.value.code == 0

    def test_main_api_error_exits_2(self, capsys):
        """Test CLI exits with code 2 on API error."""
        from unittest.mock import patch

        with patch("sys.argv", ["prog", "--owner", "org", "--repo", "repo", "--pr", "42"]):
            with patch("check_auto_merge_eligibility.GitHubAPIClient") as mock_client_class:
                mock_client_class.return_value.get.side_effect = Exception("API Error")

                with patch("check_auto_merge_eligibility.ConfigLoader") as mock_config_loader:
                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from check_auto_merge_eligibility import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 2

    def test_main_outputs_all_check_results(self, mock_pr_response, capsys):
        """Test CLI outputs all safety check results."""
        from unittest.mock import patch

        with patch("sys.argv", ["prog", "--owner", "org", "--repo", "repo", "--pr", "42"]):
            with patch("check_auto_merge_eligibility.GitHubAPIClient") as mock_client_class:
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client

                mock_client.get.side_effect = [
                    mock_pr_response,
                    {"state": "success"},
                    [{"user": {"login": "u1"}, "state": "APPROVED"}],
                    {"statuses": [{"context": "codecov", "description": "85%"}]},
                ]

                with patch("check_auto_merge_eligibility.ConfigLoader") as mock_config_loader:
                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from check_auto_merge_eligibility import main

                    with pytest.raises(SystemExit):
                        main()

                    captured = capsys.readouterr()
                    assert "All tests passed" in captured.out
                    assert "Reviews approved" in captured.out
                    assert "No conflicts" in captured.out
                    assert "Branch up-to-date" in captured.out
                    assert "Coverage threshold met" in captured.out
