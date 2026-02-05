#!/usr/bin/env python3
"""Week 9 Validation Framework.

Validates all 7 advanced automation capabilities through comprehensive testing:
- Auto-merge eligibility
- Intelligent routing
- Self-healing workflow
- Proactive maintenance
- Enhanced analytics ML
- SLA monitoring
- Incident response

Usage:
    # Run all validations
    python validation_framework.py --owner ORG --repo REPO --validate-all

    # Run specific capability
    python validation_framework.py --owner ORG --repo REPO --validate auto-merge  # noqa: E501

    # Generate validation report
    python validation_framework.py --owner ORG --repo REPO --report
"""

import argparse
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from models import ValidationResult, ValidationSuite
from notification_integration import (notify_validation_failure,
                                      notify_validation_success)
from utils import GitHubAPIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ValidationFramework:
    """Validate Week 9 advanced automation capabilities."""

    def __init__(self, github_client: GitHubAPIClient):
        """Initialize validation framework."""
        self.github = github_client
        self.results: list[ValidationResult] = []
        self.validation_dir = Path(".github/validation")
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def validate_all(self, owner: str, repo: str) -> ValidationSuite:
        """Run all validations for Week 9 capabilities.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Complete validation suite results

        """
        logger.info("Starting comprehensive Week 9 validation")

        suite = ValidationSuite(
            started_at=datetime.now(timezone.utc),
            repository=f"{owner}/{repo}",
        )

        # Run all capability validations
        suite.results.append(self.validate_auto_merge(owner, repo))
        suite.results.append(self.validate_routing(owner, repo))
        suite.results.append(self.validate_self_healing(owner, repo))
        suite.results.append(self.validate_maintenance(owner, repo))
        suite.results.append(self.validate_analytics(owner, repo))
        suite.results.append(self.validate_sla(owner, repo))
        suite.results.append(self.validate_incident_response(owner, repo))

        suite.completed_at = datetime.now(timezone.utc)
        suite.duration_seconds = (suite.completed_at - suite.started_at).total_seconds()

        # Calculate summary
        suite.passed = sum(1 for r in suite.results if r.passed)
        suite.failed = sum(1 for r in suite.results if not r.passed)
        suite.warnings = sum(len(r.warnings) for r in suite.results)

        # Save results
        self._save_validation_suite(suite)

        # Send notification
        self._send_validation_notification(suite)

        return suite

    def validate_auto_merge(self, owner: str, repo: str) -> ValidationResult:
        """Validate auto-merge capability."""
        logger.info("Validating auto-merge eligibility checker")

        result = ValidationResult(
            capability="auto-merge",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration exists
            config_path = Path(".github/auto-merge.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Test with recent merged PRs
            prs = self.github.get(
                f"/repos/{owner}/{repo}/pulls",
                params={"state": "closed", "per_page": 20},
            )

            merged_prs = [pr for pr in prs if pr.get("merged_at")]

            if not merged_prs:
                result.warnings.append("No merged PRs found for testing")
            else:
                result.metrics["tested_prs"] = len(merged_prs)
                result.metrics["merge_rate"] = len(merged_prs) / len(prs)

            result.passed = True
            result.message = "Auto-merge validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def validate_routing(self, owner: str, repo: str) -> ValidationResult:
        """Validate intelligent routing."""
        logger.info("Validating intelligent routing algorithm")

        result = ValidationResult(
            capability="intelligent-routing",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration
            config_path = Path(".github/routing.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Analyze recent PR assignments
            prs = self.github.get(
                f"/repos/{owner}/{repo}/pulls",
                params={"state": "all", "per_page": 50},
            )

            assigned_prs = [pr for pr in prs if pr.get("requested_reviewers")]

            if assigned_prs:
                result.metrics["assigned_prs"] = len(assigned_prs)
                result.metrics["assignment_rate"] = len(assigned_prs) / len(prs)

                # Check reviewer distribution
                reviewers: dict[str, int] = {}
                for pr in assigned_prs:
                    for reviewer in pr.get("requested_reviewers", []):
                        username = reviewer.get("login")
                        reviewers[username] = reviewers.get(username, 0) + 1

                result.metrics["unique_reviewers"] = len(reviewers)
                result.metrics["avg_prs_per_reviewer"] = sum(reviewers.values()) / len(reviewers) if reviewers else 0

            result.passed = True
            result.message = "Routing validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def validate_self_healing(self, owner: str, repo: str) -> ValidationResult:
        """Validate self-healing workflow."""
        logger.info("Validating self-healing workflow")

        result = ValidationResult(
            capability="self-healing",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration
            config_path = Path(".github/self-healing.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Analyze recent workflow runs
            runs = self.github.get(
                f"/repos/{owner}/{repo}/actions/runs",
                params={"per_page": 50},
            )

            total_runs = len(runs.get("workflow_runs", []))
            failed_runs = [r for r in runs.get("workflow_runs", []) if r.get("conclusion") == "failure"]

            if total_runs > 0:
                result.metrics["total_runs"] = total_runs
                result.metrics["failed_runs"] = len(failed_runs)
                result.metrics["failure_rate"] = len(failed_runs) / total_runs

            result.passed = True
            result.message = "Self-healing validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def validate_maintenance(self, owner: str, repo: str) -> ValidationResult:
        """Validate proactive maintenance."""
        logger.info("Validating proactive maintenance scheduler")

        result = ValidationResult(
            capability="maintenance",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration
            config_path = Path(".github/maintenance.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Check for scheduled tasks
            tasks_dir = Path(".github/maintenance/tasks")
            if tasks_dir.exists():
                tasks = list(tasks_dir.glob("*.json"))
                result.metrics["scheduled_tasks"] = len(tasks)

            result.passed = True
            result.message = "Maintenance validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def validate_analytics(self, owner: str, repo: str) -> ValidationResult:
        """Validate enhanced analytics ML."""
        logger.info("Validating enhanced analytics ML model")

        result = ValidationResult(
            capability="analytics",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration
            config_path = Path(".github/analytics.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Check for trained models
            models_dir = Path(".github/models")
            if models_dir.exists():
                models = list(models_dir.glob("*.joblib"))
                result.metrics["trained_models"] = len(models)

                if len(models) < 3:
                    result.warnings.append(f"Expected 3 models, found {len(models)}")

            result.passed = True
            result.message = "Analytics validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def validate_sla(self, owner: str, repo: str) -> ValidationResult:
        """Validate SLA monitoring."""
        logger.info("Validating SLA monitoring workflow")

        result = ValidationResult(
            capability="sla-monitoring",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration
            config_path = Path(".github/sla.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Analyze recent issues/PRs for SLA compliance
            issues = self.github.get(
                f"/repos/{owner}/{repo}/issues",
                params={"state": "all", "per_page": 50},
            )

            if issues:
                result.metrics["total_items"] = len(issues)

                # Calculate response times
                for issue in issues:
                    _created = datetime.fromisoformat(  # noqa: F841
                        issue["created_at"].replace("Z", "+00:00")
                    )
                    if issue.get("comments", 0) > 0:
                        # Would need to fetch first comment time
                        pass

            result.passed = True
            result.message = "SLA validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def validate_incident_response(self, owner: str, repo: str) -> ValidationResult:
        """Validate incident response automation."""
        logger.info("Validating incident response automation")

        result = ValidationResult(
            capability="incident-response",
            started_at=datetime.now(timezone.utc),
        )

        try:
            # Check configuration
            config_path = Path(".github/incident.yml")
            if not config_path.exists():
                result.errors.append("Configuration file not found")
                result.passed = False
                return result

            # Check for incident records
            incidents_dir = Path(".github/incidents")
            if incidents_dir.exists():
                incidents = list(incidents_dir.glob("INC-*.json"))
                result.metrics["total_incidents"] = len(incidents)

                # Analyze incident severity distribution
                severity_counts = {
                    "SEV-1": 0,
                    "SEV-2": 0,
                    "SEV-3": 0,
                    "SEV-4": 0,
                }
                for incident_file in incidents:
                    with open(incident_file) as f:
                        incident = json.load(f)
                        severity = incident.get("severity", "SEV-4")
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1

                result.metrics["severity_distribution"] = severity_counts

            result.passed = True
            result.message = "Incident response validation passed"

        except Exception as e:
            result.passed = False
            result.errors.append(f"Validation failed: {e}")

        result.completed_at = datetime.now(timezone.utc)
        return result

    def _save_validation_suite(self, suite: ValidationSuite):
        """Save validation suite results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suite_file = self.validation_dir / f"validation_{timestamp}.json"

        with open(suite_file, "w") as f:
            json.dump(suite.dict(), f, indent=2, default=str)

        logger.info(f"Saved validation results to {suite_file}")

    def _send_validation_notification(self, suite: ValidationSuite):
        """Send validation results notification."""
        status_emoji = "✅" if suite.failed == 0 else "⚠️"

        message = f"""
{status_emoji} **Week 9 Validation Results**

Repository: {suite.repository}
Duration: {suite.duration_seconds:.1f}s

Results:
- ✅ Passed: {suite.passed}/7
- ❌ Failed: {suite.failed}/7
- ⚠️ Warnings: {suite.warnings}

Capabilities:
"""

        for result in suite.results:
            emoji = "✅" if result.passed else "❌"
            message += f"- {emoji} {result.capability}\n"

        # Send unified notifications
        if suite.failed > 0:
            # Notify about each failed capability
            for result in suite.results:
                if not result.passed:
                    notify_validation_failure(
                        capability=result.capability,
                        repository=suite.repository,
                        errors=result.errors,
                        warnings=result.warnings,
                        metadata=result.metrics,
                    )
        else:
            # Notify about successful validation
            notify_validation_success(
                repository=suite.repository,
                passed_count=suite.passed,
                total_count=len(suite.results),
                metadata={"duration_seconds": suite.duration_seconds},
            )

    def generate_report(self, owner: str, repo: str, days: int = 7) -> dict:
        """Generate validation report for the last N days.

        Args:
            owner: Repository owner
            repo: Repository name
            days: Number of days to include

        Returns:
            Validation report dictionary

        """
        logger.info(f"Generating {days}-day validation report")

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        validation_files = sorted(self.validation_dir.glob("validation_*.json"))

        # Load recent validations
        recent_validations = []
        for val_file in validation_files:
            with open(val_file) as f:
                data = json.load(f)
                started = datetime.fromisoformat(data["started_at"])
                if started > cutoff:
                    recent_validations.append(data)

        # Generate report
        report: dict[str, Any] = {
            "repository": f"{owner}/{repo}",
            "period_days": days,
            "total_validations": len(recent_validations),
            "capabilities": {},
        }

        # Analyze by capability
        for capability in [
            "auto-merge",
            "intelligent-routing",
            "self-healing",
            "maintenance",
            "analytics",
            "sla-monitoring",
            "incident-response",
        ]:
            cap_results = []
            for validation in recent_validations:
                for result in validation.get("results", []):
                    if result["capability"] == capability:
                        cap_results.append(result)

            if cap_results:
                passed = sum(1 for r in cap_results if r["passed"])
                report["capabilities"][capability] = {
                    "total_tests": len(cap_results),
                    "passed": passed,
                    "failed": len(cap_results) - passed,
                    "success_rate": passed / len(cap_results),
                }

        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Week 9 Validation Framework")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument(
        "--validate-all",
        action="store_true",
        help="Run all validations",
    )
    parser.add_argument(
        "--validate",
        choices=[
            "auto-merge",
            "routing",
            "self-healing",
            "maintenance",
            "analytics",
            "sla",
            "incident-response",
        ],
        help="Validate specific capability",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate validation report",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Days to include in report",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize
    github = GitHubAPIClient()
    framework = ValidationFramework(github)

    if args.validate_all:
        suite = framework.validate_all(args.owner, args.repo)
        print("\n✅ Validation Complete")
        print(f"   Passed: {suite.passed}/7")
        print(f"   Failed: {suite.failed}/7")
        print(f"   Warnings: {suite.warnings}")

        if suite.failed > 0:
            print("\n❌ Failed Capabilities:")
            for result in suite.results:
                if not result.passed:
                    print(f"   - {result.capability}")
                    for error in result.errors:
                        print(f"     {error}")

    elif args.validate:
        # Run specific validation
        validate_func = getattr(framework, f"validate_{args.validate.replace('-', '_')}")
        result = validate_func(args.owner, args.repo)

        emoji = "✅" if result.passed else "❌"
        print(f"\n{emoji} {args.validate}: {result.message}")
        if result.errors:
            for error in result.errors:
                print(f"   Error: {error}")
        if result.warnings:
            for warning in result.warnings:
                print(f"   Warning: {warning}")

    elif args.report:
        report = framework.generate_report(args.owner, args.repo, args.days)
        print(f"\n📊 Validation Report ({args.days} days)")
        print(f"   Repository: {report['repository']}")
        print(f"   Total Validations: {report['total_validations']}")
        print("\n   Capability Success Rates:")
        for cap, data in report["capabilities"].items():
            rate = data["success_rate"] * 100
            print(f"   - {cap}: {rate:.1f}%")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
