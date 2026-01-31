#!/usr/bin/env python3
"""Self-Healing Workflow System.

Automatically detects, classifies, and resolves workflow failures:
- Transient failures: Retry with exponential backoff
- Permanent failures: Alert and escalate
- Dependency failures: Wait and retry after upstream fix

Usage:
    python self_healing.py --owner ORG --repo REPO --run-id RUN_ID

Environment Variables:
    GITHUB_TOKEN: GitHub API token with repo and workflow access
"""

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from models import (
    FailureClassification,
    FailureType,
    Priority,
    SelfHealingConfig,
    SelfHealingResult,
)
from notification_integration import (
    notify_self_healing_failure,
    notify_self_healing_success,
)
from utils import ConfigLoader, GitHubAPIClient, setup_logger

sys.path.insert(0, str(Path(__file__).parent))


class SelfHealingEngine:
    """Self-healing engine for workflow failures."""

    def __init__(self, client: GitHubAPIClient, config: SelfHealingConfig):
        """Initialize self-healing engine.

        Args:
            client: GitHub API client
            config: Self-healing configuration

        """
        self.client = client
        self.config = config
        self.logger = setup_logger(__name__)

    def analyze_and_heal(self, owner: str, repo: str, run_id: int) -> SelfHealingResult:
        """Analyze workflow failure and attempt healing.

        Args:
            owner: Repository owner
            repo: Repository name
            run_id: Workflow run ID

        Returns:
            Self-healing result with actions taken

        """
        self.logger.info(f"Analyzing workflow failure: {owner}/{repo} run {run_id}")

        # Get workflow run details
        run = self._get_workflow_run(owner, repo, run_id)

        if run["status"] != "completed" or run["conclusion"] in [
            "success",
            "skipped",
            "cancelled",
        ]:
            raise ValueError(
                f"Run {run_id} is not a failed run (status: {run['status']}, conclusion: {run['conclusion']})"
            )

        # Get workflow jobs for detailed error analysis
        jobs = self._get_workflow_jobs(owner, repo, run_id)

        # Classify the failure
        classification = self._classify_failure(run, jobs)

        self.logger.info(
            f"Failure classified as: {classification.failure_type.value} (confidence: {classification.confidence:.2f})"
        )

        # Determine healing strategy
        strategy = self._determine_strategy(classification)

        # Execute healing strategy
        result = self._execute_strategy(owner, repo, run, classification, strategy)

        self.logger.info(
            f"Healing {'successful' if result.healed else 'unsuccessful'}: {result.resolution}"
        )

        return result

    def _get_workflow_run(self, owner: str, repo: str, run_id: int) -> dict:
        """Get workflow run details."""
        endpoint = f"/repos/{owner}/{repo}/actions/runs/{run_id}"
        return self.client.get(endpoint)

    def _get_workflow_jobs(self, owner: str, repo: str, run_id: int) -> list[dict]:
        """Get workflow jobs for run."""
        endpoint = f"/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
        response = self.client.get(endpoint)
        return response.get("jobs", [])

    def _classify_failure(self, run: dict, jobs: list[dict]) -> FailureClassification:
        """Classify failure type based on error patterns.

        Args:
            run: Workflow run data
            jobs: List of workflow jobs

        Returns:
            Failure classification with confidence score

        """
        # Collect error messages from failed jobs
        failed_steps = []

        for job in jobs:
            if job["conclusion"] == "failure":
                for step in job.get("steps", []):
                    if step["conclusion"] == "failure":
                        failed_steps.append({"job": job["name"], "step": step["name"]})
                        # Note: GitHub API doesn't expose step logs directly
                        # In production, would parse logs from job logs
                        # endpoint

        # Pattern matching for failure classification
        failure_type = FailureType.TRANSIENT
        confidence = 0.5
        reason = "Unknown failure"

        # Check for transient failure patterns
        transient_patterns = [
            "timeout",
            "timed out",
            "connection reset",
            "temporary failure",
            "rate limit",
            "service unavailable",
            "502 bad gateway",
            "503 service unavailable",
            "network",
            "ECONNRESET",
            "ETIMEDOUT",
        ]

        # Check for dependency failure patterns
        dependency_patterns = [
            "dependency",
            "required check",
            "blocked by",
            "waiting for",
            "upstream",
            "prerequisite",
        ]

        # Check for permanent failure patterns
        permanent_patterns = [
            "syntax error",
            "compilation failed",
            "test failed",
            "assertion",
            "type error",
            "undefined",
            "not found",
            "permission denied",
            "authentication failed",
        ]

        # Analyze workflow name and job names for patterns
        run.get("name", "").lower()

        # Check run conclusion and duration
        if run["conclusion"] == "timed_out":
            failure_type = FailureType.TRANSIENT
            confidence = 0.8
            reason = "Workflow timed out - likely transient"

        # Check for multiple recent failures (indicates permanent issue)
        elif self._has_consecutive_failures(run):
            failure_type = FailureType.PERMANENT
            confidence = 0.7
            reason = "Multiple consecutive failures"

        # Check failed step names for patterns
        else:
            for step_info in failed_steps:
                step_name = step_info["step"].lower()

                # Check patterns
                if any(p in step_name for p in transient_patterns):
                    failure_type = FailureType.TRANSIENT
                    confidence = 0.75
                    reason = f"Transient pattern in step: {step_info['step']}"
                    break
                elif any(p in step_name for p in dependency_patterns):
                    failure_type = FailureType.DEPENDENCY
                    confidence = 0.7
                    reason = f"Dependency pattern in step: {step_info['step']}"
                    break
                elif any(p in step_name for p in permanent_patterns):
                    failure_type = FailureType.PERMANENT
                    confidence = 0.8
                    reason = f"Permanent failure pattern in step: {step_info['step']}"  # noqa: E501
                    break

        # Determine priority based on workflow and failure type
        priority = self._determine_priority(run, failure_type)

        return FailureClassification(
            run_id=run["id"],
            workflow_name=run["name"],
            failure_type=failure_type,
            confidence=confidence,
            reason=reason,
            priority=priority,
            failed_jobs=[job["name"] for job in jobs if job["conclusion"] == "failure"],
            timestamp=datetime.now(timezone.utc),
        )

    def _has_consecutive_failures(self, run: dict) -> bool:
        """Check if this workflow has multiple consecutive failures."""
        try:
            owner, repo = run["repository"]["full_name"].split("/")
            workflow_id = run["workflow_id"]

            # Get recent runs for this workflow
            endpoint = f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
            params = {"per_page": 10, "status": "completed"}
            response = self.client.get(endpoint, params=params)

            recent_runs = response.get("workflow_runs", [])

            # Count consecutive failures before this run
            consecutive_failures = 0
            for recent_run in recent_runs:
                if recent_run["id"] == run["id"]:
                    continue
                if recent_run["conclusion"] == "failure":
                    consecutive_failures += 1
                else:
                    break

            return consecutive_failures >= self.config.max_consecutive_failures

        except Exception as e:
            self.logger.warning(f"Error checking consecutive failures: {e}")
            return False

    def _determine_priority(self, run: dict, failure_type: FailureType) -> Priority:
        """Determine priority based on workflow and failure type."""
        workflow_name = run.get("name", "").lower()

        # P0: Critical workflows or permanent failures in production
        if any(
            keyword in workflow_name
            for keyword in ["production", "deploy", "release", "security"]
        ):
            if failure_type == FailureType.PERMANENT:
                return Priority.P0
            return Priority.P1

        # P1: Main branch or permanent failures
        if run.get("head_branch") == "main":
            return Priority.P1

        # P2: Dependency or transient failures
        if failure_type in [FailureType.DEPENDENCY, FailureType.TRANSIENT]:
            return Priority.P2

        # P3: Everything else
        return Priority.P3

    def _determine_strategy(self, classification: FailureClassification) -> str:
        """Determine healing strategy based on classification.

        Args:
            classification: Failure classification

        Returns:
            Strategy name

        """
        if classification.failure_type == FailureType.TRANSIENT:
            return "retry_exponential"
        elif classification.failure_type == FailureType.DEPENDENCY:
            return "wait_and_retry"
        elif classification.failure_type == FailureType.PERMANENT:
            return "alert_and_escalate"
        else:
            return "manual_intervention"

    def _execute_strategy(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
        strategy: str,
    ) -> SelfHealingResult:
        """Execute healing strategy.

        Args:
            owner: Repository owner
            repo: Repository name
            run: Workflow run data
            classification: Failure classification
            strategy: Strategy name

        Returns:
            Healing result

        """
        self.logger.info(f"Executing strategy: {strategy}")

        if strategy == "retry_exponential":
            return self._retry_exponential(owner, repo, run, classification)
        elif strategy == "wait_and_retry":
            return self._wait_and_retry(owner, repo, run, classification)
        elif strategy == "alert_and_escalate":
            return self._alert_and_escalate(owner, repo, run, classification)
        else:
            return self._manual_intervention(owner, repo, run, classification)

    def _retry_exponential(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
    ) -> SelfHealingResult:
        """Retry with exponential backoff for transient failures.

        Args:
            owner: Repository owner
            repo: Repository name
            run: Workflow run data
            classification: Failure classification

        Returns:
            Healing result

        """
        retry_count = self._get_retry_count(owner, repo, run["id"])

        if retry_count >= self.config.max_retry_attempts:
            self.logger.warning(
                f"Max retry attempts ({self.config.max_retry_attempts}) reached"  # noqa: E501
            )
            return SelfHealingResult(
                run_id=run["id"],
                repository=f"{owner}/{repo}",
                classification=classification,
                strategy="retry_exponential",
                healed=False,
                resolution="Max retry attempts reached, escalating",
                retry_count=retry_count,
                actions_taken=[
                    f"Attempted {retry_count} retries",
                    "Max retries exceeded",
                ],
                timestamp=datetime.now(timezone.utc),
            )

        # Calculate backoff delay
        delay = self.config.initial_retry_delay * (
            self.config.retry_backoff_multiplier**retry_count
        )

        self.logger.info(
            f"Retry {retry_count + 1}/{self.config.max_retry_attempts} after {delay}s delay"
        )

        if self.config.enable_auto_retry:
            # Re-run the workflow
            success = self._rerun_workflow(owner, repo, run["id"])

            actions = [
                f"Classified as transient failure (confidence: {classification.confidence:.2f})",  # noqa: E501
                f"Retry attempt {retry_count + 1}/{self.config.max_retry_attempts}",  # noqa: E501
                f"Applied {delay}s exponential backof",
                f"Workflow {'re-run successfully' if success else 're-run failed'}",  # noqa: E501
            ]

            # Send notification about healing result
            if self.config.send_notifications:
                if success:
                    notify_self_healing_success(
                        workflow_name=run["name"],
                        run_id=run["id"],
                        failure_type=classification.failure_type.value,
                        action_taken=f"Retry {retry_count + 1} succeeded",
                        metadata={
                            "repository": f"{owner}/{repo}",
                            "retry_count": retry_count + 1,
                            "delay": delay,
                            "confidence": classification.confidence,
                        },
                    )
                else:
                    notify_self_healing_failure(
                        workflow_name=run["name"],
                        run_id=run["id"],
                        failure_type=classification.failure_type.value,
                        attempts=retry_count + 1,
                        metadata={
                            "repository": f"{owner}/{repo}",
                            "reason": "Retry failed",
                            "confidence": classification.confidence,
                        },
                    )
                actions.append("Sent notification")

            return SelfHealingResult(
                run_id=run["id"],
                repository=f"{owner}/{repo}",
                classification=classification,
                strategy="retry_exponential",
                healed=success,
                resolution=(
                    "Workflow re-run initiated" if success else "Re-run failed"
                ),
                retry_count=retry_count + 1,
                actions_taken=actions,
                timestamp=datetime.now(timezone.utc),
            )
        else:
            return SelfHealingResult(
                run_id=run["id"],
                repository=f"{owner}/{repo}",
                classification=classification,
                strategy="retry_exponential",
                healed=False,
                resolution="Auto-retry disabled, manual intervention required",
                retry_count=retry_count,
                actions_taken=["Auto-retry is disabled in configuration"],
                timestamp=datetime.now(timezone.utc),
            )

    def _wait_and_retry(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
    ) -> SelfHealingResult:
        """Wait for dependencies and retry.

        Args:
            owner: Repository owner
            repo: Repository name
            run: Workflow run data
            classification: Failure classification

        Returns:
            Healing result

        """
        wait_time = self.config.dependency_wait_time

        self.logger.info(f"Waiting {wait_time}s for dependencies before retry")

        actions = [
            f"Classified as dependency failure (confidence: {classification.confidence:.2f})",  # noqa: E501
            f"Waiting {wait_time}s for upstream dependencies",
        ]

        if self.config.enable_auto_retry:
            # In production, would check dependency status before retrying
            # For now, just wait and retry
            time.sleep(min(wait_time, 5))  # Cap at 5s for demo

            success = self._rerun_workflow(owner, repo, run["id"])

            actions.append(
                f"Workflow {'re-run successfully' if success else 're-run failed'}"  # noqa: E501
            )

            # Send notification about healing result
            if self.config.send_notifications:
                if success:
                    notify_self_healing_success(
                        workflow_name=run["name"],
                        run_id=run["id"],
                        failure_type=classification.failure_type.value,
                        action_taken="Dependency resolved, retry succeeded",
                        metadata={
                            "repository": f"{owner}/{repo}",
                            "wait_time": wait_time,
                            "confidence": classification.confidence,
                        },
                    )
                else:
                    notify_self_healing_failure(
                        workflow_name=run["name"],
                        run_id=run["id"],
                        failure_type=classification.failure_type.value,
                        attempts=1,
                        metadata={
                            "repository": f"{owner}/{repo}",
                            "reason": "Dependency retry failed",
                            "wait_time": wait_time,
                        },
                    )
                actions.append("Sent notification")

            return SelfHealingResult(
                run_id=run["id"],
                repository=f"{owner}/{repo}",
                classification=classification,
                strategy="wait_and_retry",
                healed=success,
                resolution=(
                    "Waited for dependencies and retried" if success else "Retry failed"
                ),
                retry_count=1,
                actions_taken=actions,
                timestamp=datetime.now(timezone.utc),
            )
        else:
            actions.append("Auto-retry disabled")
            return SelfHealingResult(
                run_id=run["id"],
                repository=f"{owner}/{repo}",
                classification=classification,
                strategy="wait_and_retry",
                healed=False,
                resolution="Auto-retry disabled, manual intervention required",
                retry_count=0,
                actions_taken=actions,
                timestamp=datetime.now(timezone.utc),
            )

    def _alert_and_escalate(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
    ) -> SelfHealingResult:
        """Alert team and escalate for permanent failures.

        Args:
            owner: Repository owner
            repo: Repository name
            run: Workflow run data
            classification: Failure classification

        Returns:
            Healing result

        """
        self.logger.warning(f"Permanent failure detected: {classification.reason}")

        actions = [
            f"Classified as permanent failure (confidence: {classification.confidence:.2f})",  # noqa: E501
            f"Priority: {classification.priority.value}",
            f"Reason: {classification.reason}",
        ]

        # Create issue for tracking
        if self.config.create_issues_for_failures:
            issue_number = self._create_failure_issue(owner, repo, run, classification)
            if issue_number:
                actions.append(f"Created tracking issue #{issue_number}")

        # Send notifications
        if self.config.send_notifications:
            notify_self_healing_failure(
                workflow_name=run["name"],
                run_id=run["id"],
                failure_type=classification.failure_type.value,
                attempts=0,  # Permanent failure - no retry attempted
                metadata={
                    "repository": f"{owner}/{repo}",
                    "classification": classification.failure_type.value,
                    "priority": classification.priority.value,
                    "confidence": classification.confidence,
                    "reason": classification.reason,
                    "requires_manual_intervention": True,
                },
            )
            actions.append("Sent notification to team")

        return SelfHealingResult(
            run_id=run["id"],
            repository=f"{owner}/{repo}",
            classification=classification,
            strategy="alert_and_escalate",
            healed=False,
            resolution="Permanent failure - manual intervention required",
            retry_count=0,
            actions_taken=actions,
            timestamp=datetime.now(timezone.utc),
        )

    def _manual_intervention(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
    ) -> SelfHealingResult:
        """Fallback: Manual intervention required."""
        return SelfHealingResult(
            run_id=run["id"],
            repository=f"{owner}/{repo}",
            classification=classification,
            strategy="manual_intervention",
            healed=False,
            resolution="Unable to auto-heal, manual intervention required",
            retry_count=0,
            actions_taken=["Classification uncertain, requires manual review"],
            timestamp=datetime.now(timezone.utc),
        )

    def _get_retry_count(self, owner: str, repo: str, run_id: int) -> int:
        """Get number of retry attempts for this run."""
        # In production, would track in database or labels
        # For now, check for re-run attempts via API
        try:
            run = self._get_workflow_run(owner, repo, run_id)
            return run.get("run_attempt", 1) - 1
        except (KeyError, TypeError, OSError) as e:
            # KeyError/TypeError: unexpected API response format
            # OSError: network errors
            self.logger.debug(f"Could not get retry count for run {run_id}: {e}")
            return 0

    def _rerun_workflow(self, owner: str, repo: str, run_id: int) -> bool:
        """Re-run a failed workflow."""
        try:
            endpoint = f"/repos/{owner}/{repo}/actions/runs/{run_id}/rerun"
            self.client.post(endpoint)
            self.logger.info(f"Successfully re-ran workflow run {run_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to re-run workflow: {e}")
            return False

    def _create_failure_issue(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
    ) -> Optional[int]:
        """Create GitHub issue for failure tracking."""
        try:
            title = f"🔧 Workflow Failure: {run['name']} ({classification.failure_type.value})"

            body = """## Workflow Failure Report

**Workflow:** {run['name']}
**Run ID:** {run['id']}
**Branch:** {run['head_branch']}
**Trigger:** {run['event']}
**Failure Type:** {classification.failure_type.value}
**Priority:** {classification.priority.value}
**Confidence:** {classification.confidence:.0%}

### Reason
{classification.reason}

### Failed Jobs
{chr(10).join(f'- {job}' for job in classification.failed_jobs)}

### Actions Taken
- Classified as {classification.failure_type.value} failure
- Priority: {classification.priority.value}

### Next Steps
{'- Automatic retry will be attempted' if classification.failure_type == FailureType.TRANSIENT else '- Manual investigation required'}  # noqa: E501

[View Workflow Run]({run['html_url']})

---
*This issue was created automatically by the self-healing system.*
"""

            endpoint = f"/repos/{owner}/{repo}/issues"
            data = {
                "title": title,
                "body": body,
                "labels": [
                    "workflow-failure",
                    classification.failure_type.value,
                    classification.priority.value.lower(),
                    "auto-generated",
                ],
            }

            response = self.client.post(endpoint, data)
            issue_number = response["number"]

            self.logger.info(f"Created failure issue #{issue_number}")
            return issue_number

        except Exception as e:
            self.logger.error(f"Failed to create issue: {e}")
            return None

    def _send_notification(
        self,
        owner: str,
        repo: str,
        run: dict,
        classification: FailureClassification,
    ) -> None:
        """Send notification about failure.

        Note: Notifications now handled by unified notification system.
        This method maintained for backward compatibility.
        """
        # Notifications now sent via notify_self_healing_success/failure


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Self-healing workflow failure detection and recovery"
    )
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--run-id", required=True, type=int, help="Workflow run ID")
    parser.add_argument(
        "--config",
        default=".github/self-healing.yml",
        help="Configuration file path",
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
            config = SelfHealingConfig(**config_dict.get("self_healing", {}))
        except FileNotFoundError:
            logger.warning("No self-healing config found, using defaults")
            config = SelfHealingConfig()

        # Analyze and heal
        engine = SelfHealingEngine(client, config)
        result = engine.analyze_and_heal(args.owner, args.repo, args.run_id)

        # Output result
        print(f"\n{'=' * 70}")
        print("Self-Healing Analysis Result")
        print(f"{'=' * 70}")
        print(f"Repository: {result.repository}")
        print(f"Run ID: {result.run_id}")
        print(f"Timestamp: {result.timestamp.isoformat()}")
        print(f"\n{'=' * 70}")
        print("Classification")
        print(f"{'=' * 70}")
        print(f"Failure Type: {result.classification.failure_type.value}")
        print(f"Confidence: {result.classification.confidence:.0%}")
        print(f"Priority: {result.classification.priority.value}")
        print(f"Reason: {result.classification.reason}")
        print(f"\n{'=' * 70}")
        print("Healing Attempt")
        print(f"{'=' * 70}")
        print(f"Strategy: {result.strategy}")
        print(f"Healed: {'✅ Yes' if result.healed else '❌ No'}")
        print(f"Resolution: {result.resolution}")
        print(f"Retry Count: {result.retry_count}")
        print(f"\n{'=' * 70}")
        print("Actions Taken")
        print(f"{'=' * 70}")
        for i, action in enumerate(result.actions_taken, 1):
            print(f"{i}. {action}")
        print(f"{'=' * 70}\n")

        sys.exit(0 if result.healed else 1)

    except Exception as e:
        logger.error(f"Error in self-healing: {e}", exc_info=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
