#!/usr/bin/env python3
"""Unit tests for automation/scripts/calculate_health_score.py

Focus: Repository health score calculation with multiple metrics.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from calculate_health_score import (
    HealthMetrics,
    HealthScore,
    HealthScoreCalculator,
    main,
)


@pytest.mark.unit
class TestHealthMetrics:
    """Test HealthMetrics dataclass."""

    def test_creates_metrics(self):
        """Test creates metrics with all fields."""
        metrics = HealthMetrics(
            activity_score=80.0,
            test_coverage_score=75.0,
            issue_resolution_score=90.0,
            pr_merge_rate_score=85.0,
            dependency_health_score=70.0,
        )

        assert metrics.activity_score == 80.0
        assert metrics.test_coverage_score == 75.0
        assert metrics.issue_resolution_score == 90.0
        assert metrics.pr_merge_rate_score == 85.0
        assert metrics.dependency_health_score == 70.0


@pytest.mark.unit
class TestHealthScore:
    """Test HealthScore dataclass."""

    def test_creates_health_score(self):
        """Test creates health score with all fields."""
        metrics = HealthMetrics(80, 75, 90, 85, 70)
        score = HealthScore(
            total_score=80.5,
            grade="B",
            metrics=metrics,
            recommendations=["Improve test coverage"],
        )

        assert score.total_score == 80.5
        assert score.grade == "B"
        assert score.metrics == metrics
        assert len(score.recommendations) == 1


@pytest.mark.unit
class TestCalculateActivityScore:
    """Test calculate_activity_score method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_high_activity_returns_100(self, calculator):
        """Test 20+ commits in 30 days returns 100."""
        result = calculator.calculate_activity_score({"commits_last_30_days": 25})
        assert result == 100.0

    def test_medium_high_activity_returns_80(self, calculator):
        """Test 10-19 commits in 30 days returns 80."""
        result = calculator.calculate_activity_score({"commits_last_30_days": 15})
        assert result == 80.0

    def test_medium_activity_returns_60(self, calculator):
        """Test 5-9 commits in 30 days returns 60."""
        result = calculator.calculate_activity_score({"commits_last_30_days": 7})
        assert result == 60.0

    def test_low_activity_90_days_returns_40(self, calculator):
        """Test 10+ commits in 90 days returns 40."""
        result = calculator.calculate_activity_score({
            "commits_last_30_days": 0,
            "commits_last_90_days": 15,
        })
        assert result == 40.0

    def test_minimal_activity_returns_20(self, calculator):
        """Test 1-9 commits in 90 days returns 20."""
        result = calculator.calculate_activity_score({
            "commits_last_30_days": 0,
            "commits_last_90_days": 5,
        })
        assert result == 20.0

    def test_no_activity_returns_0(self, calculator):
        """Test no commits returns 0."""
        result = calculator.calculate_activity_score({
            "commits_last_30_days": 0,
            "commits_last_90_days": 0,
        })
        assert result == 0.0


@pytest.mark.unit
class TestCalculateTestCoverageScore:
    """Test calculate_test_coverage_score method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_90_plus_coverage_returns_100(self, calculator):
        """Test 90%+ coverage returns 100."""
        result = calculator.calculate_test_coverage_score({"test_coverage": 95})
        assert result == 100.0

    def test_80_coverage_returns_90(self, calculator):
        """Test 80-89% coverage returns 90."""
        result = calculator.calculate_test_coverage_score({"test_coverage": 85})
        assert result == 90.0

    def test_70_coverage_returns_80(self, calculator):
        """Test 70-79% coverage returns 80."""
        result = calculator.calculate_test_coverage_score({"test_coverage": 75})
        assert result == 80.0

    def test_60_coverage_returns_70(self, calculator):
        """Test 60-69% coverage returns 70."""
        result = calculator.calculate_test_coverage_score({"test_coverage": 65})
        assert result == 70.0

    def test_50_coverage_returns_60(self, calculator):
        """Test 50-59% coverage returns 60."""
        result = calculator.calculate_test_coverage_score({"test_coverage": 55})
        assert result == 60.0

    def test_low_coverage_returns_raw_value(self, calculator):
        """Test <50% coverage returns raw value."""
        result = calculator.calculate_test_coverage_score({"test_coverage": 30})
        assert result == 30.0

    def test_negative_coverage_returns_zero(self, calculator):
        """Test negative coverage returns 0."""
        result = calculator.calculate_test_coverage_score({"test_coverage": -10})
        assert result == 0.0


@pytest.mark.unit
class TestCalculateIssueResolutionScore:
    """Test calculate_issue_resolution_score method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_no_issues_returns_neutral(self, calculator):
        """Test no issues returns neutral score."""
        result = calculator.calculate_issue_resolution_score({
            "open_issues": 0,
            "closed_issues": 0,
        })
        assert result == 80.0

    def test_all_closed_fast_returns_high(self, calculator):
        """Test all issues closed quickly returns high score."""
        result = calculator.calculate_issue_resolution_score({
            "open_issues": 0,
            "closed_issues": 20,
            "avg_issue_resolution_days": 3,
        })
        assert result > 80

    def test_slow_resolution_penalized(self, calculator):
        """Test slow resolution is penalized."""
        fast = calculator.calculate_issue_resolution_score({
            "open_issues": 5,
            "closed_issues": 20,
            "avg_issue_resolution_days": 5,
        })
        slow = calculator.calculate_issue_resolution_score({
            "open_issues": 5,
            "closed_issues": 20,
            "avg_issue_resolution_days": 50,
        })
        assert fast > slow

    def test_many_open_issues_penalized(self, calculator):
        """Test many open issues are penalized."""
        few_open = calculator.calculate_issue_resolution_score({
            "open_issues": 2,
            "closed_issues": 20,
            "avg_issue_resolution_days": 10,
        })
        many_open = calculator.calculate_issue_resolution_score({
            "open_issues": 18,
            "closed_issues": 4,
            "avg_issue_resolution_days": 10,
        })
        assert few_open > many_open


@pytest.mark.unit
class TestCalculatePrMergeRateScore:
    """Test calculate_pr_merge_rate_score method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_no_prs_returns_neutral(self, calculator):
        """Test no PRs returns neutral score."""
        result = calculator.calculate_pr_merge_rate_score({
            "open_prs": 0,
            "merged_prs": 0,
        })
        assert result == 80.0

    def test_all_merged_fast_returns_high(self, calculator):
        """Test all PRs merged quickly returns high score."""
        result = calculator.calculate_pr_merge_rate_score({
            "open_prs": 0,
            "merged_prs": 20,
            "avg_pr_merge_days": 1,
        })
        # Score is capped at 100 but formula may yield slightly under
        assert result >= 95.0

    def test_slow_merge_penalized(self, calculator):
        """Test slow merges are penalized."""
        fast = calculator.calculate_pr_merge_rate_score({
            "open_prs": 2,
            "merged_prs": 15,
            "avg_pr_merge_days": 2,
        })
        slow = calculator.calculate_pr_merge_rate_score({
            "open_prs": 2,
            "merged_prs": 15,
            "avg_pr_merge_days": 12,
        })
        assert fast > slow


@pytest.mark.unit
class TestCalculateDependencyHealthScore:
    """Test calculate_dependency_health_score method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_no_issues_returns_100(self, calculator):
        """Test no outdated or vulnerable deps returns 100."""
        result = calculator.calculate_dependency_health_score({
            "outdated_dependencies": 0,
            "vulnerable_dependencies": 0,
            "total_dependencies": 30,
        })
        assert result == 100.0

    def test_vulnerabilities_heavily_penalized(self, calculator):
        """Test vulnerabilities are heavily penalized."""
        result = calculator.calculate_dependency_health_score({
            "outdated_dependencies": 0,
            "vulnerable_dependencies": 2,
            "total_dependencies": 30,
        })
        assert result == 60.0  # 100 - (2 * 20)

    def test_outdated_deps_penalized(self, calculator):
        """Test outdated dependencies are penalized."""
        none_outdated = calculator.calculate_dependency_health_score({
            "outdated_dependencies": 0,
            "vulnerable_dependencies": 0,
            "total_dependencies": 30,
        })
        some_outdated = calculator.calculate_dependency_health_score({
            "outdated_dependencies": 15,
            "vulnerable_dependencies": 0,
            "total_dependencies": 30,
        })
        assert none_outdated > some_outdated

    def test_score_never_negative(self, calculator):
        """Test score never goes below 0."""
        result = calculator.calculate_dependency_health_score({
            "outdated_dependencies": 100,
            "vulnerable_dependencies": 10,
            "total_dependencies": 10,
        })
        assert result == 0.0


@pytest.mark.unit
class TestCalculate:
    """Test calculate method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_calculates_weighted_score(self, calculator):
        """Test calculates weighted total score."""
        repo_data = {
            "commits_last_30_days": 20,  # 100 * 0.20 = 20
            "test_coverage": 90,  # 100 * 0.25 = 25
            "open_issues": 0,
            "closed_issues": 10,  # ~neutral = 80 * 0.20 = 16
            "open_prs": 0,
            "merged_prs": 10,  # ~neutral = 80 * 0.15 = 12
            "outdated_dependencies": 0,
            "vulnerable_dependencies": 0,  # 100 * 0.20 = 20
        }

        result = calculator.calculate(repo_data)

        assert result.total_score > 80
        assert result.grade in ["A", "B"]

    def test_assigns_correct_grade_a(self, calculator):
        """Test assigns grade A for 90+."""
        repo_data = {
            "commits_last_30_days": 25,
            "test_coverage": 95,
            "open_issues": 0,
            "closed_issues": 20,
            "avg_issue_resolution_days": 3,
            "open_prs": 0,
            "merged_prs": 20,
            "avg_pr_merge_days": 1,
            "outdated_dependencies": 0,
            "vulnerable_dependencies": 0,
        }

        result = calculator.calculate(repo_data)

        assert result.grade == "A"

    def test_assigns_correct_grade_f(self, calculator):
        """Test assigns grade F for <60."""
        repo_data = {
            "commits_last_30_days": 0,
            "commits_last_90_days": 0,
            "test_coverage": 10,
            "open_issues": 50,
            "closed_issues": 5,
            "open_prs": 20,
            "merged_prs": 2,
            "outdated_dependencies": 50,
            "vulnerable_dependencies": 5,
            "total_dependencies": 50,
        }

        result = calculator.calculate(repo_data)

        assert result.grade == "F"


@pytest.mark.unit
class TestGenerateRecommendations:
    """Test _generate_recommendations method."""

    @pytest.fixture
    def calculator(self):
        return HealthScoreCalculator()

    def test_recommends_activity_improvement(self, calculator):
        """Test recommends activity improvement."""
        metrics = HealthMetrics(
            activity_score=50,
            test_coverage_score=80,
            issue_resolution_score=80,
            pr_merge_rate_score=80,
            dependency_health_score=80,
        )

        result = calculator._generate_recommendations(metrics)

        assert any("activity" in r.lower() for r in result)

    def test_recommends_coverage_improvement(self, calculator):
        """Test recommends test coverage improvement."""
        metrics = HealthMetrics(
            activity_score=80,
            test_coverage_score=50,
            issue_resolution_score=80,
            pr_merge_rate_score=80,
            dependency_health_score=80,
        )

        result = calculator._generate_recommendations(metrics)

        assert any("coverage" in r.lower() for r in result)

    def test_recommends_issue_resolution_improvement(self, calculator):
        """Test recommends issue resolution improvement."""
        metrics = HealthMetrics(
            activity_score=80,
            test_coverage_score=80,
            issue_resolution_score=50,
            pr_merge_rate_score=80,
            dependency_health_score=80,
        )

        result = calculator._generate_recommendations(metrics)

        assert any("issue" in r.lower() for r in result)

    def test_recommends_pr_merge_improvement(self, calculator):
        """Test recommends PR merge rate improvement."""
        metrics = HealthMetrics(
            activity_score=80,
            test_coverage_score=80,
            issue_resolution_score=80,
            pr_merge_rate_score=50,
            dependency_health_score=80,
        )

        result = calculator._generate_recommendations(metrics)

        assert any("pr" in r.lower() for r in result)

    def test_recommends_dependency_improvement(self, calculator):
        """Test recommends dependency health improvement."""
        metrics = HealthMetrics(
            activity_score=80,
            test_coverage_score=80,
            issue_resolution_score=80,
            pr_merge_rate_score=80,
            dependency_health_score=50,
        )

        result = calculator._generate_recommendations(metrics)

        assert any("dependenc" in r.lower() for r in result)

    def test_no_recommendations_for_healthy_repo(self, calculator):
        """Test no recommendations when all metrics are good."""
        metrics = HealthMetrics(
            activity_score=90,
            test_coverage_score=90,
            issue_resolution_score=90,
            pr_merge_rate_score=90,
            dependency_health_score=90,
        )

        result = calculator._generate_recommendations(metrics)

        assert len(result) == 0


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_with_demo_flag(self, monkeypatch, capsys):
        """Test main with --demo flag."""
        monkeypatch.setattr(
            sys, "argv", ["calculate_health_score.py", "--demo"]
        )

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "demo/repo" in captured.out
        assert "Health Score" in captured.out

    def test_main_without_args_shows_help(self, monkeypatch, capsys):
        """Test main without args shows help."""
        monkeypatch.setattr(sys, "argv", ["calculate_health_score.py"])

        result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "--repo" in captured.out or "--demo" in captured.out

    def test_main_demo_shows_breakdown(self, monkeypatch, capsys):
        """Test demo mode shows metric breakdown."""
        monkeypatch.setattr(
            sys, "argv", ["calculate_health_score.py", "--demo"]
        )

        main()

        captured = capsys.readouterr()
        assert "Activity Score" in captured.out
        assert "Test Coverage Score" in captured.out
        assert "Issue Resolution Score" in captured.out
        assert "PR Merge Rate Score" in captured.out
        assert "Dependency Health Score" in captured.out


@pytest.mark.unit
class TestWeights:
    """Test weight configuration."""

    def test_weights_sum_to_one(self):
        """Test weights sum to 1.0."""
        total = sum(HealthScoreCalculator.WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_all_weights_positive(self):
        """Test all weights are positive."""
        for weight in HealthScoreCalculator.WEIGHTS.values():
            assert weight > 0


@pytest.mark.unit
class TestGradeThresholds:
    """Test grade threshold configuration."""

    def test_thresholds_descending(self):
        """Test thresholds are in descending order."""
        thresholds = [t[0] for t in HealthScoreCalculator.GRADE_THRESHOLDS]
        assert thresholds == sorted(thresholds, reverse=True)

    def test_all_grades_present(self):
        """Test all grades A-F are present."""
        grades = {t[1] for t in HealthScoreCalculator.GRADE_THRESHOLDS}
        assert grades == {"A", "B", "C", "D", "F"}
