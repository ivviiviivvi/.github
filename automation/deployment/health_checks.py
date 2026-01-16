#!/usr/bin/env python3
"""
Post-Deployment Health Checks

Validates that deployed workflows are functioning correctly.

Usage:
    ./health_checks.py --env production --deployment-id 20250101_120000
    ./health_checks.py --repo org/repo --workflows issue-triage,auto-assign
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


class HealthChecker:
    """Performs health checks on deployed workflows."""

    def __init__(self, github_token: str):
        """
        Initialize health checker.

        Args:
            github_token: GitHub API token
        """
        self.github_token = github_token
        self.api_base = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def check_repository(self, repo: str, workflows: Optional[List[str]] = None) -> Dict:
        """
        Check health of workflows in repository.

        Args:
            repo: Repository name (org/repo)
            workflows: List of workflow names to check (None = all)

        Returns:
            Dictionary with health check results
        """
        print(f"\n🏥 Health check: {repo}")

        results = {
            "repo": repo,
            "timestamp": datetime.now().isoformat(),
            "overall_health": "healthy",
            "workflows": {},
            "metrics": {},
        }

        # Get workflow runs
        try:
            response = self.session.get(
                f"{self.api_base}/repos/{repo}/actions/runs",
                params={"per_page": 50}
            )

            if response.status_code != 200:
                results["overall_health"] = "error"
                results["error"] = f"API error: {response.status_code}"
                return results

            runs = response.json().get("workflow_runs", [])

            # Filter recent runs (last 24 hours)
            cutoff = datetime.now() - timedelta(hours=24)
            recent_runs = [
                run for run in runs
                if datetime.fromisoformat(run["created_at"].replace("Z", "+00:00")) > cutoff
            ]

            # Group by workflow
            workflow_runs = {}
            for run in recent_runs:
                workflow_name = run["name"]
                if workflows and workflow_name not in workflows:
                    continue

                if workflow_name not in workflow_runs:
                    workflow_runs[workflow_name] = []
                workflow_runs[workflow_name].append(run)

            # Analyze each workflow
            for workflow_name, runs in workflow_runs.items():
                workflow_health = self._analyze_workflow_health(
                    workflow_name, runs)
                results["workflows"][workflow_name] = workflow_health

                if workflow_health["status"] != "healthy":
                    results["overall_health"] = "degraded"

            # Calculate overall metrics
            results["metrics"] = self._calculate_metrics(recent_runs)

            # Determine overall health
            if results["metrics"]["success_rate"] < 0.80:
                results["overall_health"] = "unhealthy"
            elif results["metrics"]["success_rate"] < 0.90:
                results["overall_health"] = "degraded"

            # Display summary
            self._display_results(results)

            return results

        except Exception as e:
            results["overall_health"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
            return results

    def _analyze_workflow_health(self, workflow_name: str, runs: List[Dict]) -> Dict:
        """Analyze health of a single workflow."""
        if not runs:
            return {
                "status": "unknown",
                "message": "No recent runs",
                "runs": 0,
            }

        total_runs = len(runs)
        successful_runs = sum(
            1 for run in runs if run.get("conclusion") == "success")
        failed_runs = sum(1 for run in runs if run.get(
            "conclusion") == "failure")

        success_rate = successful_runs / total_runs if total_runs > 0 else 0

        # Calculate average duration
        durations = []
        for run in runs:
            if run.get("conclusion") in ["success", "failure"]:
                start = datetime.fromisoformat(
                    run["created_at"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(
                    run["updated_at"].replace("Z", "+00:00"))
                duration = (end - start).total_seconds()
                durations.append(duration)

        avg_duration = sum(durations) / len(durations) if durations else 0

        # Determine status
        if success_rate >= 0.95:
            status = "healthy"
        elif success_rate >= 0.85:
            status = "degraded"
        else:
            status = "unhealthy"

        return {
            "status": status,
            "runs": total_runs,
            "successful": successful_runs,
            "failed": failed_runs,
            "success_rate": success_rate,
            "avg_duration_seconds": round(avg_duration, 1),
        }

    def _calculate_metrics(self, runs: List[Dict]) -> Dict:
        """Calculate overall metrics from runs."""
        if not runs:
            return {
                "total_runs": 0,
                "success_rate": 0,
                "avg_duration_seconds": 0,
            }

        total_runs = len(runs)
        successful = sum(1 for run in runs if run.get(
            "conclusion") == "success")
        success_rate = successful / total_runs if total_runs > 0 else 0

        # Calculate average duration
        durations = []
        for run in runs:
            if run.get("conclusion") in ["success", "failure"]:
                start = datetime.fromisoformat(
                    run["created_at"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(
                    run["updated_at"].replace("Z", "+00:00"))
                duration = (end - start).total_seconds()
                durations.append(duration)

        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_runs": total_runs,
            "successful_runs": successful,
            "success_rate": success_rate,
            "avg_duration_seconds": round(avg_duration, 1),
        }

    def _display_results(self, results: Dict):
        """Display health check results."""
        overall = results["overall_health"]

        status_emoji = {
            "healthy": "✅",
            "degraded": "⚠️",
            "unhealthy": "❌",
            "error": "💥",
            "unknown": "❓",
        }

        print(
            f"\n   Overall: {status_emoji.get(overall, '❓')} {overall.upper()}")

        # Display metrics
        metrics = results.get("metrics", {})
        if metrics:
            print(f"\n   📊 Metrics (last 24 hours):")
            print(f"      Total runs: {metrics['total_runs']}")
            print(f"      Success rate: {metrics['success_rate']:.1%}")
            print(
                f"      Avg duration: {metrics['avg_duration_seconds']:.1f}s")

        # Display workflow details
        workflows = results.get("workflows", {})
        if workflows:
            print(f"\n   🔧 Workflows:")
            for name, health in workflows.items():
                status = health["status"]
                emoji = status_emoji.get(status, "❓")
                print(f"      {emoji} {name}")
                print(
                    f"         {health['runs']} runs, {health['success_rate']:.1%} success")

    def check_all_repositories(self, repos: List[str]) -> Dict[str, Dict]:
        """
        Check health of multiple repositories.

        Args:
            repos: List of repository names

        Returns:
            Dictionary mapping repo to health results
        """
        print(f"\n🏥 Checking health of {len(repos)} repositories...\n")

        results = {}
        for repo in repos:
            results[repo] = self.check_repository(repo)
            time.sleep(1)  # Rate limiting

        # Summary
        print("\n" + "=" * 60)
        print("HEALTH CHECK SUMMARY")
        print("=" * 60)

        healthy = sum(1 for r in results.values()
                      if r["overall_health"] == "healthy")
        degraded = sum(1 for r in results.values()
                       if r["overall_health"] == "degraded")
        unhealthy = sum(1 for r in results.values()
                        if r["overall_health"] == "unhealthy")

        print(f"\n✅ Healthy: {healthy}/{len(repos)}")
        print(f"⚠️  Degraded: {degraded}/{len(repos)}")
        print(f"❌ Unhealthy: {unhealthy}/{len(repos)}")

        overall_health = "healthy" if unhealthy == 0 and degraded == 0 else "degraded" if unhealthy == 0 else "unhealthy"

        print(f"\nOverall system health: {overall_health.upper()}")

        return results

    def save_results(self, results: Dict, output_file: str):
        """Save health check results to file."""
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n📄 Results saved: {output_file}")


def main():
    """Main health check execution."""
    parser = argparse.ArgumentParser(
        description="Health check for deployed workflows")
    parser.add_argument("--repo", type=str,
                        help="Repository to check (org/repo)")
    parser.add_argument("--env", choices=["staging", "production", "development"],
                        help="Environment to check (checks all repos in env)")
    parser.add_argument("--workflows", type=str,
                        help="Comma-separated workflow names")
    parser.add_argument("--output", type=str, default="health-check-results.json",
                        help="Output file for results")

    args = parser.parse_args()

    # Get GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set!")
        sys.exit(1)

    # Initialize health checker
    checker = HealthChecker(github_token)

    # Parse workflows
    workflows = None
    if args.workflows:
        workflows = [w.strip() for w in args.workflows.split(",")]

    # Perform health checks
    if args.repo:
        results = checker.check_repository(args.repo, workflows)
    elif args.env:
        # Load environment config
        import yaml
        config_path = Path("automation/deployment/environments.yml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        repos = config[args.env]["repositories"]
        results = checker.check_all_repositories(repos)
    else:
        print("❌ Must specify --repo or --env")
        sys.exit(1)

    # Save results
    checker.save_results(results, args.output)

    # Exit with appropriate code
    if isinstance(results, dict):
        if "overall_health" in results:
            # Single repo
            sys.exit(0 if results["overall_health"]
                     in ["healthy", "degraded"] else 1)
        else:
            # Multiple repos
            any_unhealthy = any(r["overall_health"] ==
                                "unhealthy" for r in results.values())
            sys.exit(1 if any_unhealthy else 0)


if __name__ == "__main__":
    main()
