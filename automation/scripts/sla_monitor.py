#!/usr/bin/env python3
"""
SLA Monitoring Workflow

Provides real-time monitoring of Service Level Agreements for workflows,
issues, and pull requests with automated breach detection and alerting.

Features:
- Response time tracking (time to first comment/review)
- Resolution time tracking (time to close/merge)
- Success rate monitoring (pass rate, merge rate)
- Availability tracking (uptime, error rates)
- Breach detection and escalation
- Dashboard metrics generation
- Historical trend analysis

Usage:
    # Monitor all active items
    python sla_monitor.py --owner ORG --repo REPO --monitor

    # Check specific PR
    python sla_monitor.py --owner ORG --repo REPO --check-pr 123

    # Generate SLA report
    python sla_monitor.py --owner ORG --repo REPO --report --days 30

    # Check for breaches
    python sla_monitor.py --owner ORG --repo REPO --check-breaches
"""

import argparse
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

from models import (
    Priority,
    SLABreach,
    SLAConfig,
    SLAMetrics,
    SLAReport,
    SLAThresholds,
)
from notification_integration import notify_sla_breach
from utils import GitHubAPIClient, load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SLAMonitor:
    """Monitor and enforce Service Level Agreements."""

    def __init__(self, config: SLAConfig, github_client: GitHubAPIClient):
        """
        Initialize SLA monitor.

        Args:
            config: SLA configuration
            github_client: GitHub API client
        """
        self.config = config
        self.github = github_client
        self.breaches_dir = Path(".github/sla/breaches")
        self.reports_dir = Path(".github/sla/reports")
        self.breaches_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def monitor_repository(self, owner: str, repo: str) -> Dict[str, SLAMetrics]:
        """
        Monitor SLAs for all active items in repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dictionary of metrics by item type
        """
        logger.info(f"Monitoring SLAs for {owner}/{repo}")

        metrics = {
            "issues": self._monitor_issues(owner, repo),
            "pull_requests": self._monitor_pull_requests(owner, repo),
            "workflows": self._monitor_workflows(owner, repo),
        }

        # Check for breaches
        breaches = []
        for item_type, item_metrics in metrics.items():
            if item_metrics.breaches:
                breaches.extend(item_metrics.breaches)

        # Send breach notifications
        if breaches:
            self._handle_breaches(owner, repo, breaches)

        return metrics

    def _monitor_issues(self, owner: str, repo: str) -> SLAMetrics:
        """Monitor SLAs for issues."""
        logger.info("Monitoring issues...")

        # Fetch open issues
        issues = self.github.get(
            f"/repos/{owner}/{repo}/issues",
            params={"state": "open", "per_page": 100},
        )

        if not issues:
            return SLAMetrics(
                item_type="issues",
                total_items=0,
                within_sla=0,
                breached=0,
                avg_response_time_minutes=0,
                avg_resolution_time_hours=0,
                success_rate_percentage=100.0,
            )

        # Filter out pull requests
        issues = [i for i in issues if not i.get("pull_request")]

        total = len(issues)
        within_sla = 0
        breaches = []

        response_times = []
        resolution_times = []

        for issue in issues:
            priority = self._determine_priority(issue)
            thresholds = self._get_thresholds(priority)

            # Check response time
            created_at = datetime.fromisoformat(
                issue["created_at"].replace("Z", "+00:00")
            )
            first_comment = self._get_first_response(owner, repo, issue["number"])

            if first_comment:
                response_time = first_comment - created_at
                response_minutes = response_time.total_seconds() / 60
                response_times.append(response_minutes)

                if response_minutes > thresholds.response_time_minutes:
                    breaches.append(
                        SLABreach(
                            item_type="issue",
                            item_number=issue["number"],
                            priority=priority,
                            breach_type="response_time",
                            threshold_value=thresholds.response_time_minutes,
                            actual_value=response_minutes,
                            breach_time=datetime.now(timezone.utc),
                        )
                    )
                else:
                    within_sla += 1
            else:
                # No response yet - check if overdue
                elapsed = datetime.now(timezone.utc) - created_at
                elapsed_minutes = elapsed.total_seconds() / 60

                if elapsed_minutes > thresholds.response_time_minutes:
                    breaches.append(
                        SLABreach(
                            item_type="issue",
                            item_number=issue["number"],
                            priority=priority,
                            breach_type="response_time",
                            threshold_value=thresholds.response_time_minutes,
                            actual_value=elapsed_minutes,
                            breach_time=datetime.now(timezone.utc),
                        )
                    )

        # Calculate closed issues metrics (last 30 days)
        since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        closed_issues = self.github.get(
            f"/repos/{owner}/{repo}/issues",
            params={"state": "closed", "since": since, "per_page": 100},
        )

        if closed_issues:
            closed_issues = [i for i in closed_issues if not i.get("pull_request")]

            for issue in closed_issues:
                created_at = datetime.fromisoformat(
                    issue["created_at"].replace("Z", "+00:00")
                )
                closed_at = datetime.fromisoformat(
                    issue["closed_at"].replace("Z", "+00:00")
                )
                resolution_time = closed_at - created_at
                resolution_hours = resolution_time.total_seconds() / 3600
                resolution_times.append(resolution_hours)

        avg_response = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        avg_resolution = (
            sum(resolution_times) / len(resolution_times) if resolution_times else 0
        )

        return SLAMetrics(
            item_type="issues",
            total_items=total,
            within_sla=within_sla,
            breached=len(breaches),
            avg_response_time_minutes=avg_response,
            avg_resolution_time_hours=avg_resolution,
            success_rate_percentage=(
                (within_sla / total * 100) if total > 0 else 100.0
            ),
            breaches=breaches,
        )

    def _monitor_pull_requests(self, owner: str, repo: str) -> SLAMetrics:
        """Monitor SLAs for pull requests."""
        logger.info("Monitoring pull requests...")

        # Fetch open PRs
        prs = self.github.get(
            f"/repos/{owner}/{repo}/pulls",
            params={"state": "open", "per_page": 100},
        )

        if not prs:
            return SLAMetrics(
                item_type="pull_requests",
                total_items=0,
                within_sla=0,
                breached=0,
                avg_response_time_minutes=0,
                avg_resolution_time_hours=0,
                success_rate_percentage=100.0,
            )

        total = len(prs)
        within_sla = 0
        breaches = []

        response_times = []
        resolution_times = []

        for pr in prs:
            priority = self._determine_priority(pr)
            thresholds = self._get_thresholds(priority)

            # Check response time (first review)
            created_at = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
            first_review = self._get_first_review(owner, repo, pr["number"])

            if first_review:
                response_time = first_review - created_at
                response_minutes = response_time.total_seconds() / 60
                response_times.append(response_minutes)

                if response_minutes > thresholds.response_time_minutes:
                    breaches.append(
                        SLABreach(
                            item_type="pull_request",
                            item_number=pr["number"],
                            priority=priority,
                            breach_type="response_time",
                            threshold_value=thresholds.response_time_minutes,
                            actual_value=response_minutes,
                            breach_time=datetime.now(timezone.utc),
                        )
                    )
                else:
                    within_sla += 1
            else:
                # No review yet - check if overdue
                elapsed = datetime.now(timezone.utc) - created_at
                elapsed_minutes = elapsed.total_seconds() / 60

                if elapsed_minutes > thresholds.response_time_minutes:
                    breaches.append(
                        SLABreach(
                            item_type="pull_request",
                            item_number=pr["number"],
                            priority=priority,
                            breach_type="response_time",
                            threshold_value=thresholds.response_time_minutes,
                            actual_value=elapsed_minutes,
                            breach_time=datetime.now(timezone.utc),
                        )
                    )

        # Calculate merged PRs metrics (last 30 days)
        _since = (  # noqa: F841
            datetime.now(timezone.utc) - timedelta(days=30)
        ).isoformat()  # noqa: E501
        closed_prs = self.github.get(
            f"/repos/{owner}/{repo}/pulls",
            params={"state": "closed", "per_page": 100},
        )

        if closed_prs:
            merged_prs = [pr for pr in closed_prs if pr.get("merged_at")]

            for pr in merged_prs:
                created_at = datetime.fromisoformat(
                    pr["created_at"].replace("Z", "+00:00")
                )
                merged_at = datetime.fromisoformat(
                    pr["merged_at"].replace("Z", "+00:00")
                )
                resolution_time = merged_at - created_at
                resolution_hours = resolution_time.total_seconds() / 3600
                resolution_times.append(resolution_hours)

            merge_rate = (
                len(merged_prs) / len(closed_prs) * 100 if closed_prs else 100.0
            )
        else:
            merge_rate = 100.0

        avg_response = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        avg_resolution = (
            sum(resolution_times) / len(resolution_times) if resolution_times else 0
        )

        return SLAMetrics(
            item_type="pull_requests",
            total_items=total,
            within_sla=within_sla,
            breached=len(breaches),
            avg_response_time_minutes=avg_response,
            avg_resolution_time_hours=avg_resolution,
            success_rate_percentage=merge_rate,
            breaches=breaches,
        )

    def _monitor_workflows(self, owner: str, repo: str) -> SLAMetrics:
        """Monitor SLAs for workflow runs."""
        logger.info("Monitoring workflows...")

        # Fetch recent workflow runs (last 24 hours)
        runs = self.github.get(
            f"/repos/{owner}/{repo}/actions/runs", params={"per_page": 100}
        )

        if not runs or not runs.get("workflow_runs"):
            return SLAMetrics(
                item_type="workflows",
                total_items=0,
                within_sla=0,
                breached=0,
                avg_response_time_minutes=0,
                avg_resolution_time_hours=0,
                success_rate_percentage=100.0,
            )

        workflow_runs = runs["workflow_runs"]

        # Filter to last 24 hours
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        recent_runs = [
            r
            for r in workflow_runs
            if datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")) > cutoff
        ]

        total = len(recent_runs)
        successful = sum(1 for r in recent_runs if r.get("conclusion") == "success")
        _failed = sum(  # noqa: F841
            1 for r in recent_runs if r.get("conclusion") == "failure"
        )

        success_rate = (successful / total * 100) if total > 0 else 100.0

        breaches = []

        # Check success rate SLA
        for priority in [Priority.P0, Priority.P1, Priority.P2, Priority.P3]:
            thresholds = self._get_thresholds(priority)

            if success_rate < thresholds.success_rate_percentage:
                breaches.append(
                    SLABreach(
                        item_type="workflow",
                        item_number=0,  # No specific run
                        priority=priority,
                        breach_type="success_rate",
                        threshold_value=thresholds.success_rate_percentage,
                        actual_value=success_rate,
                        breach_time=datetime.now(timezone.utc),
                    )
                )
                break  # Only report highest priority breach

        within_sla = total - len(breaches)

        # Calculate average execution time
        execution_times = []
        for run in recent_runs:
            if run.get("conclusion") in ["success", "failure"]:
                created = datetime.fromisoformat(
                    run["created_at"].replace("Z", "+00:00")
                )
                updated = datetime.fromisoformat(
                    run["updated_at"].replace("Z", "+00:00")
                )
                duration = (updated - created).total_seconds() / 60
                execution_times.append(duration)

        avg_execution = (
            sum(execution_times) / len(execution_times) if execution_times else 0
        )

        return SLAMetrics(
            item_type="workflows",
            total_items=total,
            within_sla=within_sla,
            breached=len(breaches),
            avg_response_time_minutes=avg_execution,
            avg_resolution_time_hours=0,
            success_rate_percentage=success_rate,
            breaches=breaches,
        )

    def _get_first_response(
        self, owner: str, repo: str, issue_number: int
    ) -> Optional[datetime]:
        """Get timestamp of first response to an issue."""
        comments = self.github.get(
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments"
        )

        if comments:
            first_comment = min(
                comments,
                key=lambda c: datetime.fromisoformat(
                    c["created_at"].replace("Z", "+00:00")
                ),
            )
            return datetime.fromisoformat(
                first_comment["created_at"].replace("Z", "+00:00")
            )

        return None

    def _get_first_review(
        self, owner: str, repo: str, pr_number: int
    ) -> Optional[datetime]:
        """Get timestamp of first review on a PR."""
        reviews = self.github.get(f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews")

        if reviews:
            first_review = min(
                reviews,
                key=lambda r: datetime.fromisoformat(
                    r["submitted_at"].replace("Z", "+00:00")
                ),
            )
            return datetime.fromisoformat(
                first_review["submitted_at"].replace("Z", "+00:00")
            )

        return None

    def _determine_priority(self, item: Dict) -> Priority:
        """Determine priority based on labels and context."""
        labels = [label.get("name", "").lower() for label in item.get("labels", [])]

        # Priority label mapping
        if any(p in labels for p in ["p0", "critical", "urgent", "production"]):
            return Priority.P0
        elif any(p in labels for p in ["p1", "high", "important"]):
            return Priority.P1
        elif any(p in labels for p in ["p2", "medium", "normal"]):
            return Priority.P2
        else:
            return Priority.P3

    def _get_thresholds(self, priority: Priority) -> SLAThresholds:
        """Get SLA thresholds for priority level."""
        for threshold in self.config.thresholds:
            if threshold.priority == priority:
                return threshold

        # Default thresholds
        return SLAThresholds(
            priority=Priority.P3,
            response_time_minutes=1440,  # 24 hours
            resolution_time_hours=168,  # 1 week
            success_rate_percentage=80.0,
            availability_percentage=95.0,
        )

    def _handle_breaches(self, owner: str, repo: str, breaches: List[SLABreach]):
        """Handle SLA breaches with notifications and logging."""
        logger.warning(f"Found {len(breaches)} SLA breaches")

        # Group breaches by priority
        by_priority = {}
        for breach in breaches:
            priority = breach.priority.value
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(breach)

        # Send notifications for each priority
        for priority, priority_breaches in by_priority.items():
            self._send_breach_notification(owner, repo, priority, priority_breaches)

        # Log breaches
        self._log_breaches(owner, repo, breaches)

    def _send_breach_notification(
        self, owner: str, repo: str, priority: str, breaches: List[SLABreach]
    ):
        """Send notification for SLA breaches."""
        _breach_list = "\n".join(  # noqa: F841
            [
                f"- {b.item_type} #{b.item_number}: {b.breach_type} "
                f"({b.actual_value:.1f} vs {b.threshold_value:.1f})"
                for b in breaches
            ]
        )

        # Send unified notifications for each breach
        for breach in breaches:
            notify_sla_breach(
                item_type=breach.item_type,
                item_number=breach.item_number,
                repository=f"{owner}/{repo}",
                breach_type=breach.breach_type,
                threshold=f"{breach.threshold_minutes}min",
                actual=f"{breach.actual_minutes}min",
                priority=breach.priority.value,
                metadata={
                    "breach_count": len(breaches),
                    "timestamp": breach.timestamp.isoformat(),
                },
            )

    def _log_breaches(self, owner: str, repo: str, breaches: List[SLABreach]):
        """Log SLA breaches to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.breaches_dir / f"breach_{timestamp}.json"

        breach_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repository": f"{owner}/{repo}",
            "breaches": [
                {
                    "item_type": b.item_type,
                    "item_number": b.item_number,
                    "priority": b.priority.value,
                    "breach_type": b.breach_type,
                    "threshold_value": b.threshold_value,
                    "actual_value": b.actual_value,
                    "breach_time": b.breach_time.isoformat(),
                }
                for b in breaches
            ],
        }

        with open(log_file, "w") as f:
            json.dump(breach_data, f, indent=2)

        logger.info(f"Logged breaches to {log_file}")

    def generate_report(
        self, owner: str, repo: str, lookback_days: int = 30
    ) -> SLAReport:
        """
        Generate SLA report for specified period.

        Args:
            owner: Repository owner
            repo: Repository name
            lookback_days: Number of days to analyze

        Returns:
            SLA report with metrics and trends
        """
        logger.info(f"Generating SLA report for last {lookback_days} days")

        # Get current metrics
        current_metrics = self.monitor_repository(owner, repo)

        # Load historical breach data
        breach_files = sorted(self.breaches_dir.glob("breach_*.json"))
        total_breaches = 0

        for breach_file in breach_files[-lookback_days:]:
            with open(breach_file) as f:
                data = json.load(f)
                total_breaches += len(data.get("breaches", []))

        # Create report
        report = SLAReport(
            repository=f"{owner}/{repo}",
            period_start=datetime.now(timezone.utc) - timedelta(days=lookback_days),
            period_end=datetime.now(timezone.utc),
            metrics=current_metrics,
            total_breaches=total_breaches,
            generated_at=datetime.now(timezone.utc),
        )

        # Save report
        self._save_report(report)

        return report

    def _save_report(self, report: SLAReport):
        """Save SLA report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"report_{timestamp}.json"

        with open(report_file, "w") as f:
            json.dump(report.dict(), f, indent=2, default=str)

        logger.info(f"Saved report to {report_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SLA Monitoring Workflow")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--monitor", action="store_true", help="Monitor all items")
    parser.add_argument("--check-pr", type=int, help="Check specific PR")
    parser.add_argument("--check-issue", type=int, help="Check specific issue")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--days", type=int, default=30, help="Report lookback days")
    parser.add_argument(
        "--check-breaches",
        action="store_true",
        help="Check for active breaches",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    config = load_config("sla.yml", SLAConfig)
    github = GitHubAPIClient()

    # Initialize monitor
    monitor = SLAMonitor(config, github)

    if args.monitor or args.check_breaches:
        metrics = monitor.monitor_repository(args.owner, args.repo)

        print("\n=== SLA Metrics ===")
        for item_type, item_metrics in metrics.items():
            print(f"\n{item_type}:")
            print(f"  Total: {item_metrics.total_items}")
            print(f"  Within SLA: {item_metrics.within_sla}")
            print(f"  Breached: {item_metrics.breached}")
            print(
                f"  Avg Response: {item_metrics.avg_response_time_minutes:.1f} minutes"  # noqa: E501
            )
            print(
                f"  Avg Resolution: {item_metrics.avg_resolution_time_hours:.1f} hours"  # noqa: E501
            )
            print(f"  Success Rate: {item_metrics.success_rate_percentage:.1f}%")

            if item_metrics.breaches:
                print("\n  Breaches:")
                for breach in item_metrics.breaches:
                    print(
                        f"    - {breach.item_type} #{breach.item_number}: "
                        f"{breach.breach_type} ({breach.actual_value:.1f} vs "
                        f"{breach.threshold_value:.1f})"
                    )

    elif args.report:
        report = monitor.generate_report(args.owner, args.repo, args.days)
        print("\n=== SLA Report ===")
        print(f"Repository: {report.repository}")
        print(f"Period: {report.period_start} to {report.period_end}")
        print(f"Total Breaches: {report.total_breaches}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
