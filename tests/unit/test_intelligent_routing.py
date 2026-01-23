#!/usr/bin/env python3
"""
Unit tests for automation/scripts/intelligent_routing.py
Focus: Routing algorithm, score calculations, fallback strategies
"""

import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "automation" / "scripts"))


@pytest.fixture(autouse=True, scope="module")
def mock_secret_manager():
    """Mock secret_manager to avoid import issues."""
    original = sys.modules.get("secret_manager")
    sys.modules["secret_manager"] = MagicMock()
    yield
    # Restore original module after all tests in this module
    if original is not None:
        sys.modules["secret_manager"] = original
    else:
        sys.modules.pop("secret_manager", None)


# These imports must happen after the mock fixture is set up
# But since autouse fixture runs at module import time, we need to mock first
_original_secret_manager = sys.modules.get("secret_manager")
sys.modules["secret_manager"] = MagicMock()

from intelligent_routing import IntelligentRouter
from models import RoutingConfig, RoutingFactorScores

# Restore after imports
if _original_secret_manager is not None:
    sys.modules["secret_manager"] = _original_secret_manager
else:
    sys.modules.pop("secret_manager", None)


class TestIntelligentRouter:
    """Test IntelligentRouter class"""

    @pytest.fixture
    def mock_client(self):
        """Create mock GitHub API client"""
        client = MagicMock()
        return client

    @pytest.fixture
    def default_config(self):
        """Create default routing configuration"""
        return RoutingConfig()

    @pytest.fixture
    def router(self, mock_client, default_config):
        """Create router instance with mocks"""
        return IntelligentRouter(mock_client, default_config)

    def test_initialization(self, mock_client, default_config):
        """Test router initializes correctly"""
        router = IntelligentRouter(mock_client, default_config)
        assert router.client == mock_client
        assert router.config == default_config

    def test_get_issue(self, router, mock_client):
        """Test _get_issue fetches issue from API"""
        mock_client.get.return_value = {"number": 123, "title": "Test Issue"}

        result = router._get_issue("owner", "repo", 123)

        mock_client.get.assert_called_once_with("/repos/owner/repo/issues/123")
        assert result["number"] == 123

    def test_get_candidates(self, router, mock_client):
        """Test _get_candidates filters collaborators with write access"""
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
        """Test overall score calculation with weights"""
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
        """Test overall score is clamped to [0, 1]"""
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
        """Test confidence is 1.0 with single candidate"""
        candidates = [{"username": "user1", "score": 0.8}]

        confidence = router._calculate_confidence(candidates)
        assert confidence == 1.0

    def test_calculate_confidence_score_gap(self, router):
        """Test confidence increases with larger score gap"""
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
    """Test workload score calculation"""

    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        return client

    @pytest.fixture
    def router(self, mock_client):
        config = RoutingConfig(max_assignments_per_user=10)
        return IntelligentRouter(mock_client, config)

    def test_no_assignments_gives_full_score(self, router, mock_client):
        """Test user with no assignments gets score of 1.0"""
        mock_client.get.return_value = []

        score = router._calculate_workload("owner", "repo", "user")

        assert score == 1.0

    def test_full_assignments_gives_zero_score(self, router, mock_client):
        """Test user at max assignments gets score of 0.0"""
        # Return 10 open issues (max_assignments_per_user)
        mock_client.get.return_value = [{"number": i} for i in range(10)]

        score = router._calculate_workload("owner", "repo", "user")

        assert score == 0.0

    def test_partial_assignments_gives_proportional_score(self, router, mock_client):
        """Test user with partial assignments gets proportional score"""
        # Return 5 open issues (50% of max)
        mock_client.get.return_value = [{"number": i} for i in range(5)]

        score = router._calculate_workload("owner", "repo", "user")

        assert abs(score - 0.5) < 0.001

    def test_zero_max_assignments_rejected_by_model(self, mock_client):
        """Test zero max_assignments_per_user is rejected by model validation"""
        from pydantic import ValidationError

        # The model validates that max_assignments_per_user >= 1
        # This prevents division by zero at the model level
        with pytest.raises(ValidationError):
            RoutingConfig(max_assignments_per_user=0)


class TestExpertiseCalculation:
    """Test expertise score calculation"""

    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        return client

    @pytest.fixture
    def router(self, mock_client):
        return IntelligentRouter(mock_client, RoutingConfig())

    def test_no_commits_gives_partial_score(self, router, mock_client):
        """Test user with no commits gets base score"""
        mock_client.get.side_effect = [
            [],  # commits
            [],  # closed issues
        ]

        issue = {"labels": []}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        # Should be 0 or very low
        assert score <= 0.5

    def test_many_commits_increases_score(self, router, mock_client):
        """Test more commits increases expertise score"""
        mock_client.get.side_effect = [
            [{"sha": f"commit{i}"} for i in range(50)],  # 50 commits
            [],  # closed issues
        ]

        issue = {"labels": []}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        # Should be at least 0.5 (50 commits = max commit score)
        assert score >= 0.5

    def test_error_returns_default_score(self, router, mock_client):
        """Test API error returns default middle score"""
        mock_client.get.side_effect = Exception("API Error")

        issue = {"labels": []}
        score = router._calculate_expertise("owner", "repo", "user", issue)

        assert score == 0.5


class TestFallbackAssignment:
    """Test fallback assignment strategies"""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    @pytest.fixture
    def router(self, mock_client):
        config = RoutingConfig(fallback_strategy=["round_robin", "random"])
        return IntelligentRouter(mock_client, config)

    def test_round_robin_strategy(self, router, mock_client):
        """Test round robin selects next user after last assigned"""
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
        """Test fallback returns first candidate if all strategies fail"""
        config = RoutingConfig(fallback_strategy=[])  # No strategies
        router = IntelligentRouter(mock_client, config)

        candidates = [{"login": "user1"}, {"login": "user2"}]
        issue = {"labels": []}

        result = router._fallback_assignment("owner", "repo", 123, issue, candidates)

        assert result.assignee == "user1"
        assert result.confidence == 0.1  # Low confidence


class TestRoutingDecision:
    """Test full routing decision flow"""

    @pytest.fixture
    def mock_client(self):
        return MagicMock()

    def test_exempt_label_triggers_fallback(self, mock_client):
        """Test issue with exempt label uses fallback strategy"""
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
        """Test raises error when no candidates available"""
        router = IntelligentRouter(mock_client, RoutingConfig())

        mock_client.get.side_effect = [
            {"number": 123, "labels": []},  # issue
            [],  # no collaborators
        ]

        with pytest.raises(ValueError, match="No candidates available"):
            router.calculate_assignment("owner", "repo", 123)
