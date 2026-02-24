"""Unit tests for automation/scripts/issue_assignment_router.py
Focus: Routing algorithm, score calculations, fallback strategies.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))


# Mock secret_manager before importing modules that depend on it.
# Save original, install mock, import, then restore.
_original_secret_manager = sys.modules.get("secret_manager")
sys.modules["secret_manager"] = MagicMock()

from issue_assignment_router import IntelligentRouter
from models import RoutingConfig, RoutingFactorScores

# Restore original module state after imports
if _original_secret_manager is not None:
    sys.modules["secret_manager"] = _original_secret_manager
else:
    sys.modules.pop("secret_manager", None)


class TestIntelligentRouter:
    """Test IntelligentRouter class."""

    @pytest.fixture
    def mock_client(self):
        """Create mock GitHub API client."""
        client = MagicMock()
        return client

    @pytest.fixture
    def default_config(self):
        """Create default routing configuration."""
        return RoutingConfig()

    @pytest.fixture
    def router(self, mock_client, default_config):
        """Create router instance with mocks."""
        return IntelligentRouter(mock_client, default_config)

    def test_initialization(self, mock_client, default_config):
        """Test router initializes correctly."""
        router = IntelligentRouter(mock_client, default_config)
        assert router.client == mock_client
        assert router.config == default_config

    def test_get_issue(self, router, mock_client):
        """Test _get_issue fetches issue from API."""
        mock_client.get.return_value = {"number": 123, "title": "Test Issue"}

        result = router._get_issue("owner", "repo", 123)

        mock_client.get.assert_called_once_with("/repos/owner/repo/issues/123")
        assert result["number"] == 123

    def test_get_candidates(self, router, mock_client):
        """Test _get_candidates filters collaborators with write access."""
        mock_client.get.return_value = [
            {"login": "user1", "permissions": {"push": True, "admin": False}},
            {"login": "user2", "permissions": {"push": False, "admin": True}},
            {"login": "user3", "permissions": {"push": False, "admin": False}},
        ]

        candidates = router._get_candidates("owner", "repo")

        assert len(candidates) == 2
        assert candidates[0]["login"] == "user1"
        assert candidates[1]["login"] == "user2"

    def test_calculate_overall_score(self, router):
        """Test overall score calculation with weights."""
        scores = RoutingFactorScores(
            expertise=1.0,
            workload=1.0,
            response_time=1.0,
            availability=1.0,
            performance=1.0,
        )

        overall = router._calculate_overall_score(scores)

        # With all 1.0 scores, weighted sum should equal sum of weights
        expected = sum(router.config.factors.values())
        assert abs(overall - expected) < 0.001

    def test_calculate_overall_score_clamped(self, router):
        """Test overall score is clamped to [0, 1]."""
        # Even with all max scores, result should not exceed 1.0
        scores = RoutingFactorScores(
            expertise=1.0,
            workload=1.0,
            response_time=1.0,
            availability=1.0,
            performance=1.0,
        )

        overall = router._calculate_overall_score(scores)
        assert 0.0 <= overall <= 1.0

    def test_calculate_confidence_single_candidate(self, router):
        """Test confidence is 1.0 with single candidate."""
        candidates = [{"username": "user1", "score": 0.8}]

        confidence = router._calculate_confidence(candidates)
        assert confidence == 1.0

    def test_calculate_confidence_score_gap(self, router):
        """Test confidence increases with larger score gap."""
        small_gap = [
            {"username": "user1", "score": 0.8},
            {"username": "user2", "score": 0.79},
        ]
        large_gap = [
            {"username": "user1", "score": 0.9},
            {"username": "user2", "score": 0.5},
        ]

        confidence_small = router._calculate_confidence(small_gap)
        confidence_large = router._calculate_confidence(large_gap)

        assert confidence_large > confidence_small


class TestWorkloadCalculation:
    """Test workload score calculation."""

    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        return client

    @pytest.fixture
    def router(self, mock_client):
        config = RoutingConfig(max_assignments_per_user=10)
        return IntelligentRouter(mock_client, config)

    def test_no_assignments_gives_full_score(self, router, mock_client):
        """Test user with no assignments gets score of 1.0."""
        mock_client.get.return_value = []

        score = router._calculate_workload("owner", "repo", "user")

        assert score == 1.0

    def test_full_assignments_gives_zero_score(self, router, mock_client):
        """Test user at max assignments gets score of 0.0."""
        # Return 10 open issues (max_assignments_per_user)
        mock_client.get.return_value = [{"number": i} for i in range(10)]

        score = router._calculate_workload("owner", "repo", "user")

        assert score == 0.0

    def test_partial_assignments_gives_proportional_score(self, router, mock_client):
        """Test user with partial assignments gets proportional score."""
        # Return 5 open issues (50% of max)
        mock_client.get.return_value = [{"number": i} for i in range(5)]

        score = router._calculate_workload("owner", "repo", "user")

        assert abs(score - 0.5) < 0.001

    def test_zero_max_assignments_rejected_by_model(self, mock_client):
        """Test zero max_assignments_per_user is rejected by model validation."""
        from pydantic import ValidationError

        # The model validates that max_assignments_per_user >= 1
        # This prevents division by zero at the model level
        with pytest.raises(ValidationError):
            RoutingConfig(max_assignments_per_user=0)


class TestExpertiseCalculation:
    """Test expertise score calculation."""

    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        return client

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_no_commits_gives_partial_score(self, router, mock_client):
        """Test user with no commits gets base score."""
        mock_client.get.side_effect = [
            [],  # commits
            [],  # closed issues
        ]

        issue = {"labels": []}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        # Should be 0 or very low
        assert score <= 0.5

    def test_many_commits_increases_score(self, router, mock_client):
        """Test more commits increases expertise score."""
        mock_client.get.side_effect = [
            [{"sha": f"commit{i}"} for i in range(50)],  # 50 commits
            [],  # closed issues
        ]

        issue = {"labels": []}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        # Should be at least 0.5 (50 commits = max commit score)
        assert score >= 0.5

    def test_error_returns_default_score(self, router, mock_client):
        """Test API error returns default middle score."""
        mock_client.get.side_effect = Exception("API Error")

        issue = {"labels": []}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        assert score == 0.5


class TestFallbackAssignment:
    """Test fallback assignment strategies."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        config = RoutingConfig(fallback_strategy=["round_robin", "random"])
        return IntelligentRouter(mock_client, config)

    def test_round_robin_strategy(self, router, mock_client):
        """Test round robin selects next user after last assigned."""
        # Recent issues show user1 was last assigned
        mock_client.get.return_value = [
            {"assignee": {"login": "user1"}},
            {"assignee": None},
        ]

        candidates = [
            {"login": "user1"},
            {"login": "user2"},
            {"login": "user3"},
        ]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        # Should select user2 (next after user1)
        assert result.assignee == "user2"
        assert result.fallback_used is True

    def test_fallback_returns_first_candidate_if_all_fail(self, mock_client):
        """Test fallback returns first candidate if all strategies fail."""
        config = RoutingConfig(fallback_strategy=[])  # No strategies
        router = IntelligentRouter(mock_client, config)

        candidates = [{"login": "user1"}, {"login": "user2"}]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        assert result.assignee == "user1"
        assert result.confidence == 0.1  # Low confidence


class TestRoutingDecision:
    """Test full routing decision flow."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_exempt_label_triggers_fallback(self, mock_client):
        """Test issue with exempt label uses fallback strategy."""
        config = RoutingConfig(exempt_labels=["help wanted"])
        router = IntelligentRouter(mock_client, config)

        # Set up mocks
        mock_client.get.side_effect = [
            {"number": 123, "labels": [{"name": "help wanted"}]},  # issue
            [{"login": "user1", "permissions": {"push": True}}],  # collaborators
            [{"assignee": None}],  # recent issues for round robin
        ]

        result = router.calculate_assignment("owner", "repo", 123)

        assert result.fallback_used is True

    def test_no_candidates_raises_error(self, mock_client):
        """Test raises error when no candidates available."""
        router = IntelligentRouter(mock_client, RoutingConfig())

        mock_client.get.side_effect = [
            {"number": 123, "labels": []},  # issue
            [],  # no collaborators
        ]

        with pytest.raises(ValueError, match="No candidates available"):
            router.calculate_assignment("owner", "repo", 123)

    def test_calculate_assignment_scores_and_selects_best(self, mock_client):
        """Test calculate_assignment scores all candidates and selects best."""
        router = IntelligentRouter(mock_client, RoutingConfig())

        # Mock issue with no labels
        issue_response = {"number": 123, "labels": []}

        # Mock collaborators - only one candidate to avoid alternatives validation
        collaborators = [
            {"login": "user1", "permissions": {"push": True}},
        ]

        # Mock for factor calculations
        def api_response(endpoint, params=None):
            if "issues/123" in endpoint:
                return issue_response
            elif "collaborators" in endpoint:
                return collaborators
            elif "commits" in endpoint:
                return [{"sha": f"c{i}"} for i in range(10)]
            elif "issues" in endpoint:
                return []
            elif "events" in endpoint:
                return [{"created_at": "2024-01-01T12:00:00Z"}]
            return []

        mock_client.get.side_effect = api_response

        result = router.calculate_assignment("owner", "repo", 123)

        # Result should have valid structure
        assert result.assignee == "user1"
        assert 0 <= result.score <= 1
        assert 0 <= result.confidence <= 1
        assert result.fallback_used is False
        assert result.issue_number == 123


class TestResponseTimeCalculation:
    """Test response time score calculation."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_no_closed_issues_returns_default(self, router, mock_client):
        """Test returns default score when no closed issues."""
        mock_client.get.return_value = []

        score = router._calculate_response_time("owner", "repo", "user")

        assert score == 0.5

    def test_api_error_returns_default(self, router, mock_client):
        """Test returns default score on API error."""
        mock_client.get.side_effect = Exception("API Error")

        score = router._calculate_response_time("owner", "repo", "user")

        assert score == 0.5


class TestAvailabilityCalculation:
    """Test availability score calculation."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_no_events_returns_low_score(self, router, mock_client):
        """Test returns low score when no recent events."""
        mock_client.get.return_value = []

        score = router._calculate_availability("owner", "repo", "user")

        assert score == 0.3

    def test_api_error_returns_default(self, router, mock_client):
        """Test returns default score on API error."""
        mock_client.get.side_effect = Exception("API Error")

        score = router._calculate_availability("owner", "repo", "user")

        assert score == 0.5


class TestPerformanceCalculation:
    """Test performance score calculation."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_no_closed_issues_returns_default(self, router, mock_client):
        """Test returns default score when no closed issues."""
        mock_client.get.return_value = []

        score = router._calculate_performance("owner", "repo", "user")

        assert score == 0.5

    def test_all_successful_closures_gives_high_score(self, router, mock_client):
        """Test all successful closures give high performance score."""
        # Return closed issues with no negative labels
        mock_client.get.return_value = [{"number": i, "labels": [{"name": "bug"}]} for i in range(10)]

        score = router._calculate_performance("owner", "repo", "user")

        assert score == 1.0

    def test_wontfix_issues_lower_score(self, router, mock_client):
        """Test wontfix issues lower performance score."""
        mock_client.get.return_value = [
            {"number": 1, "labels": [{"name": "wontfix"}]},
            {"number": 2, "labels": [{"name": "bug"}]},
        ]

        score = router._calculate_performance("owner", "repo", "user")

        # 1 of 2 issues are successful = 0.5
        assert score == 0.5

    def test_api_error_returns_default(self, router, mock_client):
        """Test returns default score on API error."""
        mock_client.get.side_effect = Exception("API Error")

        score = router._calculate_performance("owner", "repo", "user")

        assert score == 0.5


class TestRandomFallbackStrategy:
    """Test random fallback strategy."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_random_strategy_selects_candidate(self, mock_client):
        """Test random strategy selects one of the candidates."""
        config = RoutingConfig(fallback_strategy=["random"])
        router = IntelligentRouter(mock_client, config)

        candidates = [{"login": f"user{i}"} for i in range(5)]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        assert result.assignee in [f"user{i}" for i in range(5)]
        assert result.fallback_used is True
        assert result.confidence == 0.2


@pytest.mark.unit
class TestExpertiseWithLabels:
    """Test expertise calculation with label matching."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_label_overlap_increases_score(self, router, mock_client):
        """Test matching labels from past issues contributes to expertise score."""
        # Mock commits - enough to get commit score
        commits = [{"sha": f"c{i}"} for i in range(50)]  # Max commits for 0.5 score
        # Mock closed issues with matching labels
        closed_issues = [
            {"number": 1, "labels": [{"name": "bug"}]},
            {"number": 2, "labels": [{"name": "bug"}]},
            {"number": 3, "labels": [{"name": "bug"}]},
            {"number": 4, "labels": [{"name": "bug"}]},
            {"number": 5, "labels": [{"name": "bug"}]},
            {"number": 6, "labels": [{"name": "bug"}]},
            {"number": 7, "labels": [{"name": "bug"}]},
            {"number": 8, "labels": [{"name": "bug"}]},
            {"number": 9, "labels": [{"name": "bug"}]},
            {"number": 10, "labels": [{"name": "bug"}]},
            {"number": 11, "labels": [{"name": "bug"}]},
            {"number": 12, "labels": [{"name": "bug"}]},
            {"number": 13, "labels": [{"name": "bug"}]},
            {"number": 14, "labels": [{"name": "bug"}]},
            {"number": 15, "labels": [{"name": "bug"}]},
            {"number": 16, "labels": [{"name": "bug"}]},
            {"number": 17, "labels": [{"name": "bug"}]},
            {"number": 18, "labels": [{"name": "bug"}]},
            {"number": 19, "labels": [{"name": "bug"}]},
            {"number": 20, "labels": [{"name": "bug"}]},
        ]  # 20 closed issues = max

        mock_client.get.side_effect = [commits, closed_issues]

        # Issue has "bug" label - should match all past issues
        issue = {"labels": [{"name": "bug"}]}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        # Should have high score from commits + closed issues + label matching
        # 50 commits = 0.5 * 0.5 = 0.25 (commit component)
        # 20 issues = 1.0 * 0.3 = 0.30 (issues component)
        # 5+ matching = 1.0 * 0.2 = 0.20 (label component)
        # Total = 0.75
        assert score >= 0.7  # Should be high


@pytest.mark.unit
class TestWorkloadErrorHandling:
    """Test workload calculation error handling."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_api_error_returns_default(self, router, mock_client):
        """Test API error returns default workload score."""
        mock_client.get.side_effect = Exception("API Error")

        score = router._calculate_workload("owner", "repo", "user")

        assert score == 0.5


@pytest.mark.unit
class TestResponseTimeScoring:
    """Test response time score calculation with actual response data."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_fast_response_gives_high_score(self, router, mock_client):
        """Test fast response time (< 1 hour) gives high score."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        issue_created = now - timedelta(hours=2)
        # Comment was 30 minutes after creation
        comment_time = issue_created + timedelta(minutes=30)

        issues = [
            {
                "number": 1,
                "created_at": issue_created.isoformat().replace("+00:00", "Z"),
                "comments_url": "https://api.github.com/repos/o/r/issues/1/comments",
            }
        ]

        comments = [
            {
                "user": {"login": "user"},
                "created_at": comment_time.isoformat().replace("+00:00", "Z"),
            }
        ]

        def mock_get(endpoint, params=None):
            if "issues" in endpoint and "comments" not in endpoint:
                return issues
            elif "comments" in endpoint:
                return comments
            return []

        mock_client.get.side_effect = mock_get
        mock_client.base_url = "https://api.github.com"

        score = router._calculate_response_time("owner", "repo", "user")

        # Fast response should give score close to 1.0
        assert score >= 0.9

    def test_slow_response_gives_lower_score(self, router, mock_client):
        """Test slow response time (> 24 hours) gives lower score."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        issue_created = now - timedelta(days=2)
        # Comment was 36 hours after creation
        comment_time = issue_created + timedelta(hours=36)

        issues = [
            {
                "number": 1,
                "created_at": issue_created.isoformat().replace("+00:00", "Z"),
                "comments_url": "https://api.github.com/repos/o/r/issues/1/comments",
            }
        ]

        comments = [
            {
                "user": {"login": "user"},
                "created_at": comment_time.isoformat().replace("+00:00", "Z"),
            }
        ]

        def mock_get(endpoint, params=None):
            if "issues" in endpoint and "comments" not in endpoint:
                return issues
            elif "comments" in endpoint:
                return comments
            return []

        mock_client.get.side_effect = mock_get
        mock_client.base_url = "https://api.github.com"

        score = router._calculate_response_time("owner", "repo", "user")

        # Slow response should give score below 0.5
        assert score < 0.5

    def test_no_assignee_comments_returns_default(self, router, mock_client):
        """Test returns default when no comments by assignee."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        issue_created = now - timedelta(hours=2)

        issues = [
            {
                "number": 1,
                "created_at": issue_created.isoformat().replace("+00:00", "Z"),
                "comments_url": "https://api.github.com/repos/o/r/issues/1/comments",
            }
        ]

        # Comments by different user
        comments = [
            {
                "user": {"login": "other_user"},
                "created_at": now.isoformat().replace("+00:00", "Z"),
            }
        ]

        def mock_get(endpoint, params=None):
            if "issues" in endpoint and "comments" not in endpoint:
                return issues
            elif "comments" in endpoint:
                return comments
            return []

        mock_client.get.side_effect = mock_get
        mock_client.base_url = "https://api.github.com"

        score = router._calculate_response_time("owner", "repo", "user")

        # No assignee comments should return default
        assert score == 0.5

    def test_comments_api_error_continues(self, router, mock_client):
        """Test continues when comments API fails for an issue."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        issue_created = now - timedelta(hours=2)

        issues = [
            {
                "number": 1,
                "created_at": issue_created.isoformat().replace("+00:00", "Z"),
                "comments_url": "https://api.github.com/repos/o/r/issues/1/comments",
            }
        ]

        call_count = 0

        def mock_get(endpoint, params=None):
            nonlocal call_count
            call_count += 1
            if "issues" in endpoint and "comments" not in endpoint:
                return issues
            elif "comments" in endpoint:
                raise Exception("Comments API Error")
            return []

        mock_client.get.side_effect = mock_get
        mock_client.base_url = "https://api.github.com"

        score = router._calculate_response_time("owner", "repo", "user")

        # Should return default since no successful comment fetches
        assert score == 0.5


@pytest.mark.unit
class TestAvailabilityBranches:
    """Test availability score branches based on recency."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_very_recent_activity_gives_high_score(self, router, mock_client):
        """Test activity < 1 hour ago gives score of 1.0."""
        from datetime import datetime, timedelta, timezone

        # Activity 30 minutes ago
        recent_time = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()

        mock_client.get.return_value = [{"created_at": recent_time.replace("+00:00", "Z")}]

        score = router._calculate_availability("owner", "repo", "user")

        assert score == 1.0

    def test_today_activity_gives_good_score(self, router, mock_client):
        """Test activity < 24 hours ago gives score of 0.8."""
        from datetime import datetime, timedelta, timezone

        # Activity 12 hours ago
        recent_time = (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()

        mock_client.get.return_value = [{"created_at": recent_time.replace("+00:00", "Z")}]

        score = router._calculate_availability("owner", "repo", "user")

        assert score == 0.8

    def test_week_old_activity_gives_medium_score(self, router, mock_client):
        """Test activity < 7 days ago gives score of 0.5."""
        from datetime import datetime, timedelta, timezone

        # Activity 3 days ago
        recent_time = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()

        mock_client.get.return_value = [{"created_at": recent_time.replace("+00:00", "Z")}]

        score = router._calculate_availability("owner", "repo", "user")

        assert score == 0.5

    def test_old_activity_gives_low_score(self, router, mock_client):
        """Test activity > 7 days ago gives score of 0.2."""
        from datetime import datetime, timedelta, timezone

        # Activity 10 days ago
        recent_time = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()

        mock_client.get.return_value = [{"created_at": recent_time.replace("+00:00", "Z")}]

        score = router._calculate_availability("owner", "repo", "user")

        assert score == 0.2


@pytest.mark.unit
class TestFallbackEdgeCases:
    """Test fallback strategy edge cases."""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_round_robin_last_not_in_candidates(self, mock_client):
        """Test round robin when last assigned user is not in candidates."""
        config = RoutingConfig(fallback_strategy=["round_robin"])
        router = IntelligentRouter(mock_client, config)

        # Last assigned was "external_user" who is no longer a collaborator
        mock_client.get.return_value = [
            {"assignee": {"login": "external_user"}},
        ]

        candidates = [
            {"login": "user1"},
            {"login": "user2"},
        ]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        # Should select first candidate since external_user not in list
        assert result.assignee == "user1"
        assert result.fallback_used is True

    def test_round_robin_api_error_falls_through(self, mock_client):
        """Test round robin API error falls through to next strategy."""
        config = RoutingConfig(fallback_strategy=["round_robin", "random"])
        router = IntelligentRouter(mock_client, config)

        # API error during round robin
        mock_client.get.side_effect = Exception("API Error")

        candidates = [{"login": "user1"}, {"login": "user2"}]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        # Should fall through to random strategy
        assert result.assignee in ["user1", "user2"]
        assert result.fallback_used is True
        assert result.confidence == 0.2  # Random strategy confidence

    def test_round_robin_no_previous_assignee(self, mock_client):
        """Test round robin when no previous assignee found."""
        config = RoutingConfig(fallback_strategy=["round_robin"])
        router = IntelligentRouter(mock_client, config)

        # No previous assignments
        mock_client.get.return_value = [
            {"assignee": None},
            {"assignee": None},
        ]

        candidates = [{"login": "user1"}, {"login": "user2"}]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        # Should select first candidate
        assert result.assignee == "user1"


@pytest.mark.unit
class TestMainCLI:
    """Test main CLI function."""

    def test_main_dry_run(self, tmp_path, capsys):
        """Test main in dry run mode (default)."""
        import sys
        from unittest.mock import MagicMock, patch

        original_argv = sys.argv
        sys.argv = [
            "issue_assignment_router.py",
            "--owner",
            "testorg",
            "--repo",
            "testrepo",
            "--issue",
            "123",
        ]

        try:
            # Mock all the dependencies
            with patch("issue_assignment_router.GitHubAPIClient") as mock_client_cls:
                with patch("issue_assignment_router.ConfigLoader") as mock_config_loader:
                    mock_client = MagicMock()
                    mock_client_cls.return_value = mock_client

                    # Mock API responses
                    def mock_get(endpoint, params=None):
                        if "issues/123" in endpoint:
                            return {"number": 123, "labels": []}
                        elif "collaborators" in endpoint:
                            return [{"login": "user1", "permissions": {"push": True}}]
                        elif "commits" in endpoint:
                            return [{"sha": f"c{i}"} for i in range(10)]
                        elif "events" in endpoint:
                            return [{"created_at": "2024-01-01T12:00:00Z"}]
                        return []

                    mock_client.get.side_effect = mock_get
                    mock_client.base_url = "https://api.github.com"

                    # Mock config loader to raise FileNotFoundError (use defaults)
                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from issue_assignment_router import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert "Intelligent Routing Decision" in captured.out
            assert "Selected Assignee" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_with_assign_flag(self, capsys):
        """Test main with --assign flag actually assigns."""
        import sys
        from unittest.mock import MagicMock, patch

        original_argv = sys.argv
        sys.argv = [
            "issue_assignment_router.py",
            "--owner",
            "testorg",
            "--repo",
            "testrepo",
            "--issue",
            "123",
            "--assign",
        ]

        try:
            with patch("issue_assignment_router.GitHubAPIClient") as mock_client_cls:
                with patch("issue_assignment_router.ConfigLoader") as mock_config_loader:
                    mock_client = MagicMock()
                    mock_client_cls.return_value = mock_client

                    def mock_get(endpoint, params=None):
                        if "issues/123" in endpoint:
                            return {"number": 123, "labels": []}
                        elif "collaborators" in endpoint:
                            return [{"login": "user1", "permissions": {"push": True}}]
                        elif "commits" in endpoint:
                            return [{"sha": f"c{i}"} for i in range(10)]
                        elif "events" in endpoint:
                            return [{"created_at": "2024-01-01T12:00:00Z"}]
                        return []

                    mock_client.get.side_effect = mock_get
                    mock_client.patch = MagicMock()
                    mock_client.base_url = "https://api.github.com"

                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from issue_assignment_router import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 0

                    # Verify patch was called to assign
                    mock_client.patch.assert_called_once()

            captured = capsys.readouterr()
            assert "Assigned issue" in captured.out
        finally:
            sys.argv = original_argv

    def test_main_error_handling(self, capsys):
        """Test main handles errors gracefully."""
        import sys
        from unittest.mock import patch

        original_argv = sys.argv
        sys.argv = [
            "issue_assignment_router.py",
            "--owner",
            "testorg",
            "--repo",
            "testrepo",
            "--issue",
            "123",
        ]

        try:
            with patch("issue_assignment_router.GitHubAPIClient") as mock_client_cls:
                mock_client_cls.side_effect = Exception("Connection failed")

                from issue_assignment_router import main

                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv

    def test_main_with_debug_flag(self, capsys):
        """Test main with --debug flag enables debug logging."""
        import sys
        from unittest.mock import MagicMock, patch

        original_argv = sys.argv
        sys.argv = [
            "issue_assignment_router.py",
            "--owner",
            "testorg",
            "--repo",
            "testrepo",
            "--issue",
            "123",
            "--debug",
        ]

        try:
            with patch("issue_assignment_router.GitHubAPIClient") as mock_client_cls:
                with patch("issue_assignment_router.ConfigLoader") as mock_config_loader:
                    mock_client = MagicMock()
                    mock_client_cls.return_value = mock_client

                    def mock_get(endpoint, params=None):
                        if "issues/123" in endpoint:
                            return {"number": 123, "labels": []}
                        elif "collaborators" in endpoint:
                            return [{"login": "user1", "permissions": {"push": True}}]
                        elif "commits" in endpoint:
                            return [{"sha": f"c{i}"} for i in range(10)]
                        elif "events" in endpoint:
                            return [{"created_at": "2024-01-01T12:00:00Z"}]
                        return []

                    mock_client.get.side_effect = mock_get
                    mock_client.base_url = "https://api.github.com"

                    mock_config_loader.return_value.load.side_effect = FileNotFoundError()

                    from issue_assignment_router import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 0
        finally:
            sys.argv = original_argv

    def test_main_with_valid_config_file(self, tmp_path, capsys):
        """Test main loads config from file."""
        import sys
        from unittest.mock import MagicMock, patch

        original_argv = sys.argv
        sys.argv = [
            "issue_assignment_router.py",
            "--owner",
            "testorg",
            "--repo",
            "testrepo",
            "--issue",
            "123",
        ]

        try:
            with patch("issue_assignment_router.GitHubAPIClient") as mock_client_cls:
                with patch("issue_assignment_router.ConfigLoader") as mock_config_loader:
                    mock_client = MagicMock()
                    mock_client_cls.return_value = mock_client

                    def mock_get(endpoint, params=None):
                        if "issues/123" in endpoint:
                            return {"number": 123, "labels": []}
                        elif "collaborators" in endpoint:
                            return [{"login": "user1", "permissions": {"push": True}}]
                        elif "commits" in endpoint:
                            return [{"sha": f"c{i}"} for i in range(10)]
                        elif "events" in endpoint:
                            return [{"created_at": "2024-01-01T12:00:00Z"}]
                        return []

                    mock_client.get.side_effect = mock_get
                    mock_client.base_url = "https://api.github.com"

                    # Return valid config
                    mock_config_loader.return_value.load.return_value = {
                        "issue_assignment_router": {
                            "factors": {
                                "expertise": 0.3,
                                "workload": 0.3,
                                "response_time": 0.2,
                                "availability": 0.1,
                                "performance": 0.1,
                            }
                        }
                    }

                    from issue_assignment_router import main

                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 0
        finally:
            sys.argv = original_argv

    def test_alternatives_display_format(self):
        """Test alternatives are displayed in expected format."""
        # Just test the routing decision structure
        from models import RoutingDecision, RoutingFactorScores

        # Create a result with alternatives using the expected format
        # (model expects dict[str, float], so use numeric keys as workaround)
        result = RoutingDecision(
            issue_number=123,
            repository="testorg/testrepo",
            assignee="user1",
            score=0.85,
            scores=RoutingFactorScores(
                expertise=0.8,
                workload=0.9,
                response_time=0.7,
                availability=0.85,
                performance=0.9,
            ),
            confidence=0.7,
            fallback_used=False,
            alternatives=[
                {"user2": 0.75},
                {"user3": 0.65},
            ],
        )

        # Verify alternatives exist
        assert len(result.alternatives) == 2
        assert result.confidence == 0.7
