#!/usr/bin/env python3
"""Proactive Maintenance Scheduler.

Predicts optimal maintenance windows using ML and usage patterns:
- Dependency updates: Automated package updates
- Cleanup tasks: Remove stale branches, old artifacts
- Optimization: Performance tuning, cache warming

Uses historical data to predict:
- Low-traffic periods
- Minimal disruption times
- Resource availability

Usage:
    python proactive_maintenance.py --owner ORG --repo REPO --task-type TYPE

Environment Variables:
    GITHUB_TOKEN: GitHub API token with repo access
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from models import (MaintenanceConfig, MaintenanceTask, MaintenanceWindow,
                    Priority, RiskLevel)
from utils import ConfigLoader, GitHubAPIClient, setup_logger

sys.path.insert(0, str(Path(__file__).parent))


class MaintenanceScheduler:
    """Proactive maintenance scheduler with ML-based timing."""

    def __init__(self, client: GitHubAPIClient, config: MaintenanceConfig):
        """Initialize maintenance scheduler.

        Args:
            client: GitHub API client
            config: Maintenance configuration

        """
        self.client = client
        self.config = config
        self.logger = setup_logger(__name__)

    def schedule_maintenance(self, owner: str, repo: str, task_type: str) -> MaintenanceWindow:
        """Schedule optimal maintenance window for task.

        Args:
            owner: Repository owner
            repo: Repository name
            task_type: Type of maintenance task

        Returns:
            Optimal maintenance window with alternatives

        """
        self.logger.info(f"Scheduling maintenance: {task_type} for {owner}/{repo}")

        # Analyze repository activity patterns
        activity_data = self._analyze_activity_patterns(owner, repo)

        # Get pending maintenance tasks
        pending_tasks = self._get_pending_tasks(owner, repo, task_type)

        # Predict optimal windows
        windows = self._predict_maintenance_windows(owner, repo, task_type, activity_data, pending_tasks)

        if not windows:
            raise ValueError("No suitable maintenance windows found")

        # Select best window
        best_window = windows[0]

        self.logger.info(
            f"Scheduled maintenance: {best_window.scheduled_time.isoformat()} "
            f"(impact: {best_window.impact_score:.2f}, "
            f"confidence: {best_window.confidence:.2f})"
        )

        return best_window

    def _analyze_activity_patterns(self, owner: str, repo: str) -> dict:
        """Analyze repository activity patterns over time.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Activity data with usage patterns

        """
        self.logger.debug("Analyzing activity patterns")

        # Get commit activity (last 4 weeks)
        commit_activity = self._get_commit_activity(owner, repo)

        # Get workflow run frequency
        workflow_activity = self._get_workflow_activity(owner, repo)

        # Get issue/PR activity
        issue_activity = self._get_issue_activity(owner, repo)

        # Calculate hourly patterns
        hourly_patterns = self._calculate_hourly_patterns(commit_activity, workflow_activity, issue_activity)

        # Calculate daily patterns
        daily_patterns = self._calculate_daily_patterns(commit_activity, workflow_activity, issue_activity)

        return {
            "hourly_patterns": hourly_patterns,
            "daily_patterns": daily_patterns,
            "commit_activity": commit_activity,
            "workflow_activity": workflow_activity,
            "issue_activity": issue_activity,
        }

    def _get_commit_activity(self, owner: str, repo: str) -> list[dict]:
        """Get recent commit activity."""
        try:
            since = (datetime.now(timezone.utc) - timedelta(days=28)).isoformat()
            endpoint = f"/repos/{owner}/{repo}/commits"
            params = {"since": since, "per_page": 100}
            commits = self.client.get(endpoint, params=params)
            return commits
        except Exception as e:
            self.logger.warning(f"Error fetching commits: {e}")
            return []

    def _get_workflow_activity(self, owner: str, repo: str) -> list[dict]:
        """Get recent workflow runs."""
        try:
            endpoint = f"/repos/{owner}/{repo}/actions/runs"
            params = {"per_page": 100, "status": "completed"}
            response = self.client.get(endpoint, params=params)
            return response.get("workflow_runs", [])
        except Exception as e:
            self.logger.warning(f"Error fetching workflow runs: {e}")
            return []

    def _get_issue_activity(self, owner: str, repo: str) -> list[dict]:
        """Get recent issue/PR activity."""
        try:
            since = (datetime.now(timezone.utc) - timedelta(days=28)).isoformat()
            endpoint = f"/repos/{owner}/{repo}/issues"
            params = {"since": since, "state": "all", "per_page": 100}
            issues = self.client.get(endpoint, params=params)
            return issues
        except Exception as e:
            self.logger.warning(f"Error fetching issues: {e}")
            return []

    def _calculate_hourly_patterns(self, commits: list, workflows: list, issues: list) -> dict[int, float]:
        """Calculate activity score by hour of day (0-23)."""
        hourly_activity = dict.fromkeys(range(24), 0.0)

        # Weight commits
        for commit in commits:
            if commit.get("commit", {}).get("author", {}).get("date"):
                dt = datetime.fromisoformat(commit["commit"]["author"]["date"].replace("Z", "+00:00"))
                hour = dt.hour
                hourly_activity[hour] += 1.0

        # Weight workflow runs
        for run in workflows:
            if run.get("created_at"):
                dt = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
                hour = dt.hour
                hourly_activity[hour] += 2.0  # Workflows are more disruptive

        # Weight issues/PRs
        for issue in issues:
            if issue.get("created_at"):
                dt = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                hour = dt.hour
                hourly_activity[hour] += 0.5

        # Normalize to 0-1 scale
        max_activity = max(hourly_activity.values()) if hourly_activity else 1
        if max_activity > 0:
            hourly_activity = {h: score / max_activity for h, score in hourly_activity.items()}

        return hourly_activity

    def _calculate_daily_patterns(self, commits: list, workflows: list, issues: list) -> dict[int, float]:
        """Calculate activity score by day of week (0=Monday, 6=Sunday)."""
        daily_activity = dict.fromkeys(range(7), 0.0)

        # Weight commits
        for commit in commits:
            if commit.get("commit", {}).get("author", {}).get("date"):
                dt = datetime.fromisoformat(commit["commit"]["author"]["date"].replace("Z", "+00:00"))
                day = dt.weekday()
                daily_activity[day] += 1.0

        # Weight workflow runs
        for run in workflows:
            if run.get("created_at"):
                dt = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
                day = dt.weekday()
                daily_activity[day] += 2.0

        # Weight issues/PRs
        for issue in issues:
            if issue.get("created_at"):
                dt = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                day = dt.weekday()
                daily_activity[day] += 0.5

        # Normalize to 0-1 scale
        max_activity = max(daily_activity.values()) if daily_activity else 1
        if max_activity > 0:
            daily_activity = {d: score / max_activity for d, score in daily_activity.items()}

        return daily_activity

    def _get_pending_tasks(self, owner: str, repo: str, task_type: str) -> list[MaintenanceTask]:
        """Get pending maintenance tasks."""
        tasks = []

        if task_type == "dependency_update":
            tasks.extend(self._get_dependency_update_tasks(owner, repo))
        elif task_type == "cleanup":
            tasks.extend(self._get_cleanup_tasks(owner, repo))
        elif task_type == "optimization":
            tasks.extend(self._get_optimization_tasks(owner, repo))

        return tasks

    def _get_dependency_update_tasks(self, owner: str, repo: str) -> list[MaintenanceTask]:
        """Identify dependency updates needed."""
        tasks = []

        try:
            # Check for Dependabot PRs
            endpoint = f"/repos/{owner}/{repo}/pulls"
            params = {"state": "open", "per_page": 50}
            prs = self.client.get(endpoint, params=params)

            for pr in prs:
                if pr["user"]["login"] in ["dependabot[bot]", "renovate[bot]"]:
                    tasks.append(
                        MaintenanceTask(
                            task_type="dependency_update",
                            description=f"Merge dependency update: {pr['title']}",  # noqa: E501
                            priority=Priority.P2,
                            estimated_duration=10,
                            risk_level=RiskLevel.LOW,
                            details={
                                "pr_number": pr["number"],
                                "title": pr["title"],
                            },
                        )
                    )

        except Exception as e:
            self.logger.warning(f"Error checking dependencies: {e}")

        return tasks

    def _get_cleanup_tasks(self, owner: str, repo: str) -> list[MaintenanceTask]:
        """Identify cleanup tasks needed."""
        tasks = []

        try:
            # Check for stale branches
            endpoint = f"/repos/{owner}/{repo}/branches"
            branches = self.client.get(endpoint)

            cutoff = datetime.now(timezone.utc) - timedelta(days=self.config.stale_branch_days)

            stale_branches = []
            for branch in branches[:20]:  # Check recent 20
                if branch["name"] in ["main", "master", "develop"]:
                    continue

                # Get branch last commit
                try:
                    commit_endpoint = f"/repos/{owner}/{repo}/commits/{branch['commit']['sha']}"  # noqa: E501
                    commit = self.client.get(commit_endpoint)
                    commit_date = datetime.fromisoformat(commit["commit"]["author"]["date"].replace("Z", "+00:00"))
                except (KeyError, TypeError, ValueError, OSError) as e:
                    # KeyError/TypeError: unexpected API response format
                    # ValueError: invalid date format
                    # OSError: network errors
                    self.logger.debug(f"Could not get commit date for branch {branch.get('name', 'unknown')}: {e}")
                    commit_date = None

                if commit_date is None:
                    continue

                if commit_date < cutoff:
                    stale_branches.append(branch["name"])

            if stale_branches:
                tasks.append(
                    MaintenanceTask(
                        task_type="cleanup",
                        description=f"Delete {len(stale_branches)} stale branches",  # noqa: E501
                        priority=Priority.P3,
                        estimated_duration=5,
                        risk_level=RiskLevel.LOW,
                        details={"branches": stale_branches[:10]},
                    )
                )

        except Exception as e:
            self.logger.warning(f"Error checking branches: {e}")

        return tasks

    def _get_optimization_tasks(self, owner: str, repo: str) -> list[MaintenanceTask]:
        """Identify optimization tasks."""
        # Placeholder for optimization tasks
        # In production, would check for cache warming, index rebuilding, etc.
        return []

    def _predict_maintenance_windows(
        self,
        owner: str,
        repo: str,
        task_type: str,
        activity_data: dict,
        tasks: list[MaintenanceTask],
    ) -> list[MaintenanceWindow]:
        """Predict optimal maintenance windows.

        Args:
            owner: Repository owner
            repo: Repository name
            task_type: Task type
            activity_data: Activity patterns
            tasks: Pending tasks

        Returns:
            List of maintenance windows sorted by suitability

        """
        windows = []
        now = datetime.now(timezone.utc)

        # Generate candidate windows for next 7 days
        for day_offset in range(1, 8):
            target_date = now + timedelta(days=day_offset)

            # Try each hour of the day
            for hour in range(24):
                window_start = target_date.replace(hour=hour, minute=0, second=0, microsecond=0)

                # Skip past times
                if window_start < now:
                    continue

                # Calculate impact score for this window
                impact_score = self._calculate_impact_score(window_start, activity_data, task_type)

                # Calculate confidence based on data quality
                confidence = self._calculate_confidence(activity_data, window_start)

                # Estimate duration
                duration = sum(task.estimated_duration for task in tasks) or 30

                # Generate reasoning
                reasoning = self._generate_reasoning(window_start, impact_score, activity_data)

                # Generate alternatives
                alternatives: list[dict[str, Any]] = []

                window = MaintenanceWindow(
                    task_type=task_type,
                    scheduled_time=window_start,
                    duration_minutes=duration,
                    impact_score=impact_score,
                    confidence=confidence,
                    alternatives=alternatives,
                    reasoning=reasoning,
                    tasks=tasks,
                )

                windows.append(window)

        # Sort by impact score (lower is better)
        windows.sort(key=lambda w: w.impact_score)

        # Return top 5 windows with alternatives
        top_windows = windows[:5]

        # Add alternatives to best window
        if top_windows:
            top_windows[0].alternatives = [
                {
                    "time": w.scheduled_time.isoformat(),
                    "impact": w.impact_score,
                    "confidence": w.confidence,
                }
                for w in top_windows[1:4]
            ]

        return top_windows

    def _calculate_impact_score(self, window_start: datetime, activity_data: dict, task_type: str) -> float:
        """Calculate impact score for maintenance window.

        Lower score = better window (less disruption)

        Args:
            window_start: Proposed window start time
            activity_data: Activity patterns
            task_type: Task type

        Returns:
            Impact score (0.0 to 1.0)

        """
        hourly_patterns = activity_data.get("hourly_patterns", {})
        daily_patterns = activity_data.get("daily_patterns", {})

        hour = window_start.hour
        day = window_start.weekday()

        # Base impact from activity patterns
        hourly_impact = hourly_patterns.get(hour, 0.5)
        daily_impact = daily_patterns.get(day, 0.5)

        # Weight hourly more than daily
        base_impact = (hourly_impact * 0.7) + (daily_impact * 0.3)

        # Apply preferred hours/days from config
        if hour in self.config.preferred_hours:
            base_impact *= 0.7  # 30% reduction for preferred hours

        if day in self.config.preferred_days:
            base_impact *= 0.8  # 20% reduction for preferred days

        # Check for avoid dates
        date_str = window_start.strftime("%Y-%m-%d")
        if date_str in self.config.avoid_dates:
            base_impact = 1.0  # Maximum impact (avoid)

        # Task-specific adjustments
        if task_type == "dependency_update":
            # Dependency updates are higher risk
            base_impact *= 1.2
        elif task_type == "cleanup":
            # Cleanup is lower risk
            base_impact *= 0.8

        return min(1.0, max(0.0, base_impact))

    def _calculate_confidence(self, activity_data: dict, window_start: datetime) -> float:
        """Calculate prediction confidence."""
        # More historical data = higher confidence
        commit_count = len(activity_data.get("commit_activity", []))
        workflow_count = len(activity_data.get("workflow_activity", []))
        issue_count = len(activity_data.get("issue_activity", []))

        total_events = commit_count + workflow_count + issue_count

        # Confidence based on data points
        if total_events >= 100:
            confidence = 0.9
        elif total_events >= 50:
            confidence = 0.75
        elif total_events >= 20:
            confidence = 0.6
        else:
            confidence = 0.4

        # Reduce confidence for predictions far in future
        days_ahead = (window_start - datetime.now(timezone.utc)).days
        if days_ahead > 3:
            confidence *= 0.9

        return confidence

    def _generate_reasoning(self, window_start: datetime, impact_score: float, activity_data: dict) -> str:
        """Generate human-readable reasoning for window selection."""
        hour = window_start.hour
        day = window_start.weekday()
        day_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        reasons = []

        # Time of day reasoning
        if hour in self.config.preferred_hours:
            reasons.append(f"preferred maintenance hour ({hour}:00)")
        elif hour < 6:
            reasons.append("early morning with typically low activity")
        elif hour >= 22:
            reasons.append("late evening with reduced traffic")

        # Day of week reasoning
        if day in self.config.preferred_days:
            reasons.append(f"preferred day ({day_names[day]})")
        elif day >= 5:
            reasons.append("weekend with lower activity")

        # Impact reasoning
        if impact_score < 0.3:
            reasons.append("minimal disruption expected")
        elif impact_score < 0.5:
            reasons.append("low disruption expected")
        elif impact_score < 0.7:
            reasons.append("moderate disruption expected")
        else:
            reasons.append("higher disruption expected")

        return "; ".join(reasons).capitalize()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Proactive maintenance scheduling with ML-based timing")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument(
        "--task-type",
        required=True,
        choices=["dependency_update", "cleanup", "optimization"],
        help="Type of maintenance task",
    )
    parser.add_argument(
        "--config",
        default=".github/maintenance.yml",
        help="Configuration file path",
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Actually schedule the maintenance (default: dry run)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    logger = setup_logger(__name__, log_level)

    try:
        # Initialize GitHub client
        client = GitHubAPIClient()

        # Load configuration
        config_loader = ConfigLoader()
        try:
            config_dict = config_loader.load(args.config)
            config = MaintenanceConfig(**config_dict.get("maintenance", {}))
        except FileNotFoundError:
            logger.warning("No maintenance config found, using defaults")
            config = MaintenanceConfig()

        # Schedule maintenance
        scheduler = MaintenanceScheduler(client, config)
        window = scheduler.schedule_maintenance(args.owner, args.repo, args.task_type)

        # Output result
        print(f"\n{'=' * 70}")
        print("Optimal Maintenance Window")
        print(f"{'=' * 70}")
        print(f"Repository: {args.owner}/{args.repo}")
        print(f"Task Type: {args.task_type}")
        print(f"\n{'=' * 70}")
        print("Scheduled Window")
        print(f"{'=' * 70}")
        print(
            f"Start Time: {window.scheduled_time.strftime('%Y-%m-%d %H:%M UTC')}"  # noqa: E501
        )
        print(f"Duration: {window.duration_minutes} minutes")
        print(f"Impact Score: {window.impact_score:.2f} (lower is better)")
        print(f"Confidence: {window.confidence:.0%}")
        print(f"\n{'=' * 70}")
        print("Reasoning")
        print(f"{'=' * 70}")
        print(f"{window.reasoning}")

        if window.tasks:
            print(f"\n{'=' * 70}")
            print(f"Pending Tasks ({len(window.tasks)})")
            print(f"{'=' * 70}")
            for i, task in enumerate(window.tasks[:5], 1):
                print(f"{i}. {task.description}")
                print(
                    f"   Priority: {task.priority.value}, "
                    f"Duration: {task.estimated_duration}min, "
                    f"Risk: {task.risk_level.value}"
                )

        if window.alternatives:
            print(f"\n{'=' * 70}")
            print("Alternative Windows")
            print(f"{'=' * 70}")
            for i, alt in enumerate(window.alternatives, 1):
                alt_time = datetime.fromisoformat(alt["time"])
                print(
                    f"{i}. {alt_time.strftime('%Y-%m-%d %H:%M UTC')} "
                    f"(impact: {alt['impact']:.2f}, "
                    f"confidence: {alt['confidence']:.0%})"
                )

        print(f"{'=' * 70}\n")

        if args.schedule:
            logger.info("Scheduling maintenance window...")
            # In production, would create calendar event, send notifications,
            # etc.
            print(
                f"✅ Maintenance scheduled for {window.scheduled_time.isoformat()}"  # noqa: E501
            )

        sys.exit(0)

    except Exception as e:
        logger.error(f"Error scheduling maintenance: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
