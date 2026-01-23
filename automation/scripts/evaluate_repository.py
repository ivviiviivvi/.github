#!/usr/bin/env python3
"""
Repository Evaluation Script
Evaluates potential pilot repositories for workflow deployment

Usage:
    python3 evaluate_repository.py <owner/repo>
    python3 evaluate_repository.py --all  # Evaluate all org repos
"""

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional


@dataclass
class RepositoryMetrics:
    """Repository evaluation metrics."""

    name: str
    stars: int
    forks: int
    open_issues: int
    open_prs: int
    activity_score: float
    has_codeowners: bool
    has_contributing: bool
    has_labels: bool
    default_branch: str
    visibility: str
    language: str
    weekly_commits: int
    total_score: float
    recommendation: str


class RepositoryEvaluator:
    """Evaluates repositories for workflow deployment readiness."""

    # Scoring weights
    WEIGHTS = {
        "activity": 0.30,
        "documentation": 0.20,
        "size": 0.15,
        "health": 0.15,
        "community": 0.10,
        "infrastructure": 0.10,
    }

    # Thresholds
    THRESHOLDS = {"excellent": 80, "good": 60, "fair": 40, "poor": 0}

    def __init__(self, repo: str):
        """Initialize evaluator for a repository.

        Args:
            repo: Repository in format 'owner/repo'
        """
        self.repo = repo
        self.owner, self.repo_name = repo.split("/")

    def run_gh_command(self, args: List[str]) -> Optional[Dict]:
        """Run gh CLI command and return JSON result."""
        try:
            cmd = ["gh"] + args
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}", file=sys.stderr)
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            return None

    def get_repository_info(self) -> Optional[Dict]:
        """Get basic repository information."""
        return self.run_gh_command(
            [
                "repo",
                "view",
                self.repo,
                "--json",
                "name,stargazerCount,forkCount,openIssues,language,"
                "defaultBranchRef,visibility,description",
            ]
        )

    def get_open_prs(self) -> int:
        """Count open pull requests."""
        result = self.run_gh_command(
            [
                "pr",
                "list",
                "--repo",
                self.repo,
                "--state",
                "open",
                "--json",
                "number",
                "--limit",
                "1000",
            ]
        )
        return len(result) if result else 0

    def check_file_exists(self, filepath: str) -> bool:
        """Check if a file exists in the repository."""
        try:
            subprocess.run(
                ["gh", "api", f"repos/{self.repo}/contents/{filepath}"],
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def get_commit_activity(self) -> int:
        """Get number of commits in the last week."""
        result = self.run_gh_command(
            [
                "api",
                f"repos/{self.repo}/commits",
                "--jq",
                "length",
                "-X",
                "GET",
                "-F",
                "since=" + self._get_date_week_ago(),
            ]
        )
        return result if result and isinstance(result, int) else 0

    def _get_date_week_ago(self) -> str:
        """Get ISO date string for one week ago."""
        from datetime import datetime, timedelta

        week_ago = datetime.now() - timedelta(days=7)
        return week_ago.isoformat()

    def calculate_activity_score(self, info: Dict, weekly_commits: int) -> float:
        """Calculate activity score (0-100)."""
        # Factors: commits, PRs, issues
        commit_score = min(weekly_commits * 5, 40)  # Max 40 points
        pr_score = min(info.get("openPRs", 0) * 3, 30)  # Max 30 points
        issue_score = min(info.get("openIssues", 0) * 2, 30)  # Max 30 points

        return commit_score + pr_score + issue_score

    def calculate_documentation_score(
        self, has_codeowners: bool, has_contributing: bool
    ) -> float:
        """Calculate documentation score (0-100)."""
        score = 0
        if has_codeowners:
            score += 50  # CODEOWNERS is critical
        if has_contributing:
            score += 50  # CONTRIBUTING.md is important
        return score

    def calculate_size_score(self, info: Dict) -> float:
        """Calculate repository size score (0-100)."""
        # Prefer medium-sized active repositories
        stars = info.get("stargazerCount", 0)
        forks = info.get("forkCount", 0)

        star_score = min(stars * 2, 50)  # Max 50 points
        fork_score = min(forks * 5, 50)  # Max 50 points

        return star_score + fork_score

    def calculate_health_score(self, info: Dict) -> float:
        """Calculate repository health score (0-100)."""
        # Balance between activity and manageability
        open_issues = info.get("openIssues", 0)
        open_prs = info.get("openPRs", 0)

        # Too many open items suggests maintenance issues
        # Sweet spot: 5-30 issues, 2-15 PRs
        issue_score = 50 if 5 <= open_issues <= 30 else 25
        pr_score = 50 if 2 <= open_prs <= 15 else 25

        return issue_score + pr_score

    def calculate_community_score(self, info: Dict) -> float:
        """Calculate community engagement score (0-100)."""
        stars = info.get("stargazerCount", 0)
        forks = info.get("forkCount", 0)

        # Higher stars/forks indicate active community
        if stars > 100 or forks > 20:
            return 100
        elif stars > 50 or forks > 10:
            return 75
        elif stars > 20 or forks > 5:
            return 50
        elif stars > 5 or forks > 2:
            return 25
        else:
            return 0

    def calculate_infrastructure_score(self, has_labels: bool) -> float:
        """Calculate infrastructure readiness score (0-100)."""
        # Check for existing workflow infrastructure
        score = 0

        if has_labels:
            score += 50  # Has label system

        # Check for .github directory
        if self.check_file_exists(".github/README.md"):
            score += 25

        # Check for workflows
        if self.check_file_exists(".github/workflows"):
            score += 25

        return score

    def calculate_total_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted total score."""
        total = 0
        for category, score in scores.items():
            weight = self.WEIGHTS.get(category, 0)
            total += score * weight
        return round(total, 1)

    def get_recommendation(self, total_score: float) -> str:
        """Get recommendation based on total score."""
        if total_score >= self.THRESHOLDS["excellent"]:
            return "EXCELLENT - Highly recommended for pilot"
        elif total_score >= self.THRESHOLDS["good"]:
            return "GOOD - Suitable for pilot"
        elif total_score >= self.THRESHOLDS["fair"]:
            return "FAIR - Consider after improvements"
        else:
            return "POOR - Not recommended"

    def evaluate(self) -> Optional[RepositoryMetrics]:
        """Evaluate repository and return metrics."""
        print(f"\n🔍 Evaluating repository: {self.repo}")
        print("=" * 60)

        # Gather data
        info = self.get_repository_info()
        if not info:
            print("❌ Failed to get repository information")
            return None

        open_prs = self.get_open_prs()
        info["openPRs"] = open_prs

        has_codeowners = self.check_file_exists(
            ".github/CODEOWNERS"
        ) or self.check_file_exists("CODEOWNERS")
        has_contributing = self.check_file_exists(
            ".github/CONTRIBUTING.md"
        ) or self.check_file_exists("CONTRIBUTING.md")
        has_labels = True  # Assume all repos have some labels

        weekly_commits = self.get_commit_activity()

        # Calculate scores
        scores = {
            "activity": self.calculate_activity_score(info, weekly_commits),
            "documentation": self.calculate_documentation_score(
                has_codeowners, has_contributing
            ),
            "size": self.calculate_size_score(info),
            "health": self.calculate_health_score(info),
            "community": self.calculate_community_score(info),
            "infrastructure": self.calculate_infrastructure_score(has_labels),
        }

        total_score = self.calculate_total_score(scores)
        recommendation = self.get_recommendation(total_score)

        # Create metrics object
        metrics = RepositoryMetrics(
            name=self.repo,
            stars=info.get("stargazerCount", 0),
            forks=info.get("forkCount", 0),
            open_issues=info.get("openIssues", {}).get("totalCount", 0),
            open_prs=open_prs,
            activity_score=scores["activity"],
            has_codeowners=has_codeowners,
            has_contributing=has_contributing,
            has_labels=has_labels,
            default_branch=info.get("defaultBranchRef", {}).get("name", "main"),
            visibility=info.get("visibility", "UNKNOWN"),
            language=info.get("language", {}).get("name", "Unknown"),
            weekly_commits=weekly_commits,
            total_score=total_score,
            recommendation=recommendation,
        )

        self.print_results(metrics, scores)
        return metrics

    def print_results(self, metrics: RepositoryMetrics, scores: Dict[str, float]):
        """Print evaluation results."""
        print("\n📊 Repository Metrics:")
        print(f"  Stars: {metrics.stars}")
        print(f"  Forks: {metrics.forks}")
        print(f"  Open Issues: {metrics.open_issues}")
        print(f"  Open PRs: {metrics.open_prs}")
        print(f"  Weekly Commits: {metrics.weekly_commits}")
        print(f"  Language: {metrics.language}")
        print(f"  Default Branch: {metrics.default_branch}")
        print(f"  Visibility: {metrics.visibility}")

        print("\n📋 Infrastructure:")
        print(f"  CODEOWNERS: {'✅ Yes' if metrics.has_codeowners else '❌ No'}")
        print(
            f"  CONTRIBUTING: {'✅ Yes' if metrics.has_contributing else '❌ No'}"  # noqa: E501
        )

        print("\n🎯 Category Scores:")
        for category, score in scores.items():
            bar = "█" * int(score / 5)
            print(f"  {category.capitalize():15} {score:5.1f}/100 {bar}")

        print(f"\n⭐ Total Score: {metrics.total_score}/100")
        print(f"📝 Recommendation: {metrics.recommendation}")
        print()


def evaluate_all_repos(org: str):
    """Evaluate all repositories in an organization."""
    print(f"🔍 Finding all repositories in organization: {org}")

    # Get all repos
    try:
        result = subprocess.run(
            ["gh", "repo", "list", org, "--json", "name", "--limit", "1000"],
            capture_output=True,
            text=True,
            check=True,
        )
        repos = json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Error listing repositories: {e}")
        return

    print(f"Found {len(repos)} repositories\n")

    results = []
    for repo in repos:
        repo_name = f"{org}/{repo['name']}"
        evaluator = RepositoryEvaluator(repo_name)
        metrics = evaluator.evaluate()
        if metrics:
            results.append(metrics)

    # Sort by score
    results.sort(key=lambda x: x.total_score, reverse=True)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    print(f"\n{'Repository':<40} {'Score':<10} {'Recommendation'}")
    print("-" * 60)
    for metrics in results:
        print(
            f"{metrics.name:<40} {metrics.total_score:<10.1f} {metrics.recommendation}"  # noqa: E501
        )

    # Save to JSON
    output_file = f"{org}_repository_evaluation.json"
    with open(output_file, "w") as f:
        json.dump([asdict(m) for m in results], f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 evaluate_repository.py <owner/repo>")
        print("  python3 evaluate_repository.py --all <org>")
        sys.exit(1)

    if sys.argv[1] == "--all":
        if len(sys.argv) < 3:
            print("Error: --all requires organization name")
            sys.exit(1)
        evaluate_all_repos(sys.argv[2])
    else:
        repo = sys.argv[1]
        evaluator = RepositoryEvaluator(repo)
        metrics = evaluator.evaluate()

        if metrics:
            # Save individual result
            output_file = f"{repo.replace('/', '_')}_evaluation.json"
            with open(output_file, "w") as f:
                json.dump(asdict(metrics), f, indent=2)
            print(f"💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()
