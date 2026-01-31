#!/usr/bin/env python3
"""Repository Health Score Calculator.

Calculates comprehensive health scores for repositories based on multiple metrics.

Usage:
    python3 calculate_health_score.py --repo owner/repo
    python3 calculate_health_score.py --org organization
    python3 calculate_health_score.py --all
"""

import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class HealthMetrics:
    """Health metrics for a repository."""

    activity_score: float  # Based on commit activity
    test_coverage_score: float  # Based on test coverage percentage
    issue_resolution_score: float  # Based on issue resolution rate
    pr_merge_rate_score: float  # Based on PR merge rate
    dependency_health_score: float  # Based on dependency freshness


@dataclass
class HealthScore:
    """Overall health score with breakdown."""

    total_score: float
    grade: str
    metrics: HealthMetrics
    recommendations: list[str]


class HealthScoreCalculator:
    """Calculate repository health scores."""

    # Weight configuration for each metric
    WEIGHTS = {
        "activity": 0.20,
        "test_coverage": 0.25,
        "issue_resolution": 0.20,
        "pr_merge_rate": 0.15,
        "dependency_health": 0.20,
    }

    # Grade thresholds
    GRADE_THRESHOLDS = [
        (90, "A"),
        (80, "B"),
        (70, "C"),
        (60, "D"),
        (0, "F"),
    ]

    def __init__(self):
        """Initialize the calculator."""
        self.cache: dict[str, HealthScore] = {}

    def calculate_activity_score(self, repo_data: dict[str, Any]) -> float:
        """Calculate score based on commit activity.

        Args:
            repo_data: Repository data including commit history

        Returns:
            Activity score from 0-100

        """
        commits_last_30_days = repo_data.get("commits_last_30_days", 0)
        commits_last_90_days = repo_data.get("commits_last_90_days", 0)

        # Score based on recent activity
        if commits_last_30_days >= 20:
            return 100.0
        elif commits_last_30_days >= 10:
            return 80.0
        elif commits_last_30_days >= 5:
            return 60.0
        elif commits_last_90_days >= 10:
            return 40.0
        elif commits_last_90_days > 0:
            return 20.0
        return 0.0

    def calculate_test_coverage_score(self, repo_data: dict[str, Any]) -> float:
        """Calculate score based on test coverage.

        Args:
            repo_data: Repository data including coverage metrics

        Returns:
            Test coverage score from 0-100

        """
        coverage = repo_data.get("test_coverage", 0)

        # Direct mapping with bonus for high coverage
        if coverage >= 90:
            return 100.0
        elif coverage >= 80:
            return 90.0
        elif coverage >= 70:
            return 80.0
        elif coverage >= 60:
            return 70.0
        elif coverage >= 50:
            return 60.0
        return max(0, coverage)

    def calculate_issue_resolution_score(self, repo_data: dict[str, Any]) -> float:
        """Calculate score based on issue resolution rate.

        Args:
            repo_data: Repository data including issue metrics

        Returns:
            Issue resolution score from 0-100

        """
        open_issues = repo_data.get("open_issues", 0)
        closed_issues = repo_data.get("closed_issues", 0)
        avg_resolution_days = repo_data.get("avg_issue_resolution_days", 30)

        total_issues = open_issues + closed_issues
        if total_issues == 0:
            return 80.0  # No issues = neutral score

        resolution_rate = closed_issues / total_issues
        time_factor = max(0, 1 - (avg_resolution_days / 60))  # Penalize slow resolution

        return min(100, (resolution_rate * 70) + (time_factor * 30))

    def calculate_pr_merge_rate_score(self, repo_data: dict[str, Any]) -> float:
        """Calculate score based on PR merge rate.

        Args:
            repo_data: Repository data including PR metrics

        Returns:
            PR merge rate score from 0-100

        """
        open_prs = repo_data.get("open_prs", 0)
        merged_prs = repo_data.get("merged_prs", 0)
        avg_merge_days = repo_data.get("avg_pr_merge_days", 7)

        total_prs = open_prs + merged_prs
        if total_prs == 0:
            return 80.0  # No PRs = neutral score

        merge_rate = merged_prs / total_prs
        time_factor = max(0, 1 - (avg_merge_days / 14))  # Penalize slow merges

        return min(100, (merge_rate * 60) + (time_factor * 40))

    def calculate_dependency_health_score(self, repo_data: dict[str, Any]) -> float:
        """Calculate score based on dependency health.

        Args:
            repo_data: Repository data including dependency metrics

        Returns:
            Dependency health score from 0-100

        """
        outdated_deps = repo_data.get("outdated_dependencies", 0)
        vulnerable_deps = repo_data.get("vulnerable_dependencies", 0)
        total_deps = repo_data.get("total_dependencies", 1)

        # Heavy penalty for vulnerabilities
        vuln_penalty = vulnerable_deps * 20
        outdated_penalty = (outdated_deps / max(1, total_deps)) * 30

        return max(0, 100 - vuln_penalty - outdated_penalty)

    def calculate(self, repo_data: dict[str, Any]) -> HealthScore:
        """Calculate comprehensive health score for a repository.

        Args:
            repo_data: Repository data with all metrics

        Returns:
            HealthScore with total, grade, and breakdown

        """
        metrics = HealthMetrics(
            activity_score=self.calculate_activity_score(repo_data),
            test_coverage_score=self.calculate_test_coverage_score(repo_data),
            issue_resolution_score=self.calculate_issue_resolution_score(repo_data),
            pr_merge_rate_score=self.calculate_pr_merge_rate_score(repo_data),
            dependency_health_score=self.calculate_dependency_health_score(repo_data),
        )

        # Calculate weighted total
        total = (
            metrics.activity_score * self.WEIGHTS["activity"]
            + metrics.test_coverage_score * self.WEIGHTS["test_coverage"]
            + metrics.issue_resolution_score * self.WEIGHTS["issue_resolution"]
            + metrics.pr_merge_rate_score * self.WEIGHTS["pr_merge_rate"]
            + metrics.dependency_health_score * self.WEIGHTS["dependency_health"]
        )

        # Determine grade
        grade = "F"
        for threshold, g in self.GRADE_THRESHOLDS:
            if total >= threshold:
                grade = g
                break

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics)

        return HealthScore(
            total_score=round(total, 1),
            grade=grade,
            metrics=metrics,
            recommendations=recommendations,
        )

    def _generate_recommendations(self, metrics: HealthMetrics) -> list[str]:
        """Generate improvement recommendations based on metrics.

        Args:
            metrics: The calculated health metrics

        Returns:
            List of recommendation strings

        """
        recommendations = []

        if metrics.activity_score < 60:
            recommendations.append(
                "Increase commit activity to maintain repository freshness"
            )

        if metrics.test_coverage_score < 70:
            recommendations.append("Improve test coverage to at least 70%")

        if metrics.issue_resolution_score < 60:
            recommendations.append(
                "Address open issues to improve issue resolution rate"
            )

        if metrics.pr_merge_rate_score < 60:
            recommendations.append(
                "Review and merge pending PRs to improve PR merge rate"
            )

        if metrics.dependency_health_score < 70:
            recommendations.append(
                "Update outdated dependencies and address vulnerabilities"
            )

        return recommendations


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Calculate repository health scores")
    parser.add_argument("--repo", type=str, help="Repository to analyze (owner/repo)")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")

    args = parser.parse_args()

    calculator = HealthScoreCalculator()

    if args.demo:
        # Demo with sample data
        demo_data = {
            "name": "demo/repo",
            "commits_last_30_days": 15,
            "commits_last_90_days": 45,
            "test_coverage": 75,
            "open_issues": 5,
            "closed_issues": 20,
            "avg_issue_resolution_days": 7,
            "open_prs": 2,
            "merged_prs": 15,
            "avg_pr_merge_days": 3,
            "outdated_dependencies": 3,
            "vulnerable_dependencies": 0,
            "total_dependencies": 25,
        }

        score = calculator.calculate(demo_data)
        print(f"Repository: {demo_data['name']}")
        print(f"Health Score: {score.total_score}/100 (Grade: {score.grade})")
        print("\nMetric Breakdown:")
        print(f"  Activity Score: {score.metrics.activity_score}")
        print(f"  Test Coverage Score: {score.metrics.test_coverage_score}")
        print(f"  Issue Resolution Score: {score.metrics.issue_resolution_score}")
        print(f"  PR Merge Rate Score: {score.metrics.pr_merge_rate_score}")
        print(f"  Dependency Health Score: {score.metrics.dependency_health_score}")

        if score.recommendations:
            print("\nRecommendations:")
            for rec in score.recommendations:
                print(f"  - {rec}")

        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
