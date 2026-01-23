#!/usr/bin/env python3
"""
Auto-Merge Eligibility Checker

Checks if a pull request meets all safety criteria for automatic merging.
Implements comprehensive validation including:
- CI/CD status checks
- Code review requirements
- Merge conflict detection
- Branch currency verification
- Code coverage thresholds

Usage:
    python check_auto_merge_eligibility.py --owner ORG --repo REPO --pr PR_NUMBER  # noqa: E501

Environment Variables:
    GITHUB_TOKEN: GitHub API token with repo access
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict

from models import (
    AutoMergeConfig,
    AutoMergeEligibility,
    AutoMergeSafetyChecks,
)
from utils import ConfigLoader, GitHubAPIClient, setup_logger

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class AutoMergeChecker:
    """Check PR eligibility for auto-merge."""

    def __init__(self, client: GitHubAPIClient, config: AutoMergeConfig):
        """
        Initialize auto-merge checker.

        Args:
            client: GitHub API client
            config: Auto-merge configuration
        """
        self.client = client
        self.config = config
        self.logger = setup_logger(__name__)

    def check_eligibility(
        self, owner: str, repo: str, pr_number: int
    ) -> AutoMergeEligibility:
        """
        Check if PR is eligible for auto-merge.

        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number

        Returns:
            Auto-merge eligibility result
        """
        self.logger.info(
            f"Checking auto-merge eligibility for {owner}/{repo}#{pr_number}"
        )

        # Get PR details
        pr = self._get_pull_request(owner, repo, pr_number)

        # Run all safety checks
        checks = self._run_safety_checks(owner, repo, pr)

        # Determine eligibility
        eligible = all(
            [
                checks.all_tests_passed,
                checks.reviews_approved,
                checks.no_conflicts,
                checks.branch_up_to_date,
                checks.coverage_threshold_met,
            ]
        )

        # Build reasons list if not eligible
        reasons = []
        if not checks.all_tests_passed:
            reasons.append("CI tests have not all passed")
        if not checks.reviews_approved:
            reasons.append(
                f"Missing required approvals (need {self.config.min_reviews})"
            )
        if not checks.no_conflicts:
            reasons.append("PR has merge conflicts")
        if not checks.branch_up_to_date:
            reasons.append("Branch is not up-to-date with base")
        if not checks.coverage_threshold_met:
            reasons.append(
                f"Code coverage below threshold ({self.config.coverage_threshold}%)"  # noqa: E501
            )

        # Calculate confidence score
        confidence = self._calculate_confidence(pr, checks)

        result = AutoMergeEligibility(
            pr_number=pr_number,
            repository=f"{owner}/{repo}",
            eligible=eligible,
            checks_passed=checks,
            reasons=reasons,
            confidence=confidence,
        )

        self.logger.info(
            f"Eligibility check complete: eligible={eligible}, confidence={confidence:.2f}"  # noqa: E501
        )
        return result

    def _get_pull_request(self, owner: str, repo: str, pr_number: int) -> Dict:
        """Get pull request details from GitHub API."""
        endpoint = f"/repos/{owner}/{repo}/pulls/{pr_number}"
        return self.client.get(endpoint)

    def _run_safety_checks(
        self, owner: str, repo: str, pr: Dict
    ) -> AutoMergeSafetyChecks:
        """Run all safety checks on PR."""
        return AutoMergeSafetyChecks(
            all_tests_passed=self._check_tests_passed(owner, repo, pr),
            reviews_approved=self._check_reviews_approved(owner, repo, pr),
            no_conflicts=self._check_no_conflicts(pr),
            branch_up_to_date=self._check_branch_up_to_date(pr),
            coverage_threshold_met=self._check_coverage_threshold(owner, repo, pr),
        )

    def _check_tests_passed(self, owner: str, repo: str, pr: Dict) -> bool:
        """
        Check if all required tests have passed.

        Args:
            owner: Repository owner
            repo: Repository name
            pr: Pull request data

        Returns:
            True if all tests passed
        """
        head_sha = pr["head"]["sha"]

        # Get commit status
        endpoint = f"/repos/{owner}/{repo}/commits/{head_sha}/status"
        status = self.client.get(endpoint)

        # Overall status must be 'success'
        if status.get("state") != "success":
            self.logger.debug(f"Commit status: {status.get('state')}")
            return False

        # Check if all required checks have passed
        if self.config.required_checks:
            endpoint = f"/repos/{owner}/{repo}/commits/{head_sha}/check-runs"
            check_runs = self.client.get(endpoint)

            check_names = {
                run["name"]: run["conclusion"]
                for run in check_runs.get("check_runs", [])
            }

            for required_check in self.config.required_checks:
                if required_check not in check_names:
                    self.logger.debug(f"Required check '{required_check}' not found")
                    return False
                if check_names[required_check] != "success":
                    self.logger.debug(
                        f"Required check '{required_check}' status: {check_names[required_check]}"  # noqa: E501
                    )
                    return False

        return True

    def _check_reviews_approved(self, owner: str, repo: str, pr: Dict) -> bool:
        """
        Check if PR has required number of approvals.

        Args:
            owner: Repository owner
            repo: Repository name
            pr: Pull request data

        Returns:
            True if minimum reviews approved
        """
        pr_number = pr["number"]
        endpoint = f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        reviews = self.client.get(endpoint)

        # Count unique approved reviews (latest per reviewer)
        reviewer_states: Dict[str, str] = {}
        for review in reviews:
            reviewer = review["user"]["login"]
            # Keep only the latest review state per reviewer
            reviewer_states[reviewer] = review["state"]

        approved_count = sum(
            1 for state in reviewer_states.values() if state == "APPROVED"
        )

        self.logger.debug(
            f"Reviews: {approved_count} approved (need {self.config.min_reviews})"  # noqa: E501
        )
        return approved_count >= self.config.min_reviews

    def _check_no_conflicts(self, pr: Dict) -> bool:
        """
        Check if PR has no merge conflicts.

        Args:
            pr: Pull request data

        Returns:
            True if no conflicts
        """
        mergeable = pr.get("mergeable")
        if mergeable is None:
            # GitHub is still calculating, assume not ready
            self.logger.debug("Mergeable state not yet determined")
            return False

        return mergeable is True

    def _check_branch_up_to_date(self, pr: Dict) -> bool:
        """
        Check if PR branch is up-to-date with base.

        Args:
            pr: Pull request data

        Returns:
            True if branch is current
        """
        # mergeable_state provides detailed status
        mergeable_state = pr.get("mergeable_state", "")

        # States that indicate branch is current:
        # - 'clean': No conflicts, checks passed
        # - 'unstable': Checks failed but no conflicts
        # - 'has_hooks': Hooks exist but no conflicts
        #
        # States that indicate branch is NOT current:
        # - 'behind': Branch needs update
        # - 'dirty': Has conflicts
        # - 'blocked': Blocked by requirements

        acceptable_states = ["clean", "unstable", "has_hooks"]
        is_current = mergeable_state in acceptable_states

        self.logger.debug(f"Mergeable state: {mergeable_state}, current: {is_current}")
        return is_current

    def _check_coverage_threshold(self, owner: str, repo: str, pr: Dict) -> bool:
        """
        Check if code coverage meets minimum threshold.

        Args:
            owner: Repository owner
            repo: Repository name
            pr: Pull request data

        Returns:
            True if coverage threshold met
        """
        head_sha = pr["head"]["sha"]

        try:
            # Try to get coverage from commit status
            endpoint = f"/repos/{owner}/{repo}/commits/{head_sha}/status"
            status = self.client.get(endpoint)

            for status_check in status.get("statuses", []):
                # Look for coverage status (common patterns)
                context = status_check.get("context", "").lower()
                if "coverage" in context or "codecov" in context:
                    description = status_check.get("description", "")

                    # Try to extract percentage from description
                    # Common formats: "Coverage: 85.5%", "85.5% coverage",
                    # "Coverage is 85.5%"
                    match = re.search(r"(\d+(?:\.\d+)?)\s*%", description)
                    if match:
                        coverage = float(match.group(1))
                        self.logger.debug(
                            f"Coverage: {coverage}% (threshold: {self.config.coverage_threshold}%)"  # noqa: E501
                        )
                        return coverage >= self.config.coverage_threshold

            # If no coverage information found, try check runs
            endpoint = f"/repos/{owner}/{repo}/commits/{head_sha}/check-runs"
            check_runs = self.client.get(endpoint)

            for run in check_runs.get("check_runs", []):
                name = run.get("name", "").lower()
                if "coverage" in name or "codecov" in name:
                    output = run.get("output", {})
                    summary = output.get("summary", "")
                    match = re.search(r"(\d+(?:\.\d+)?)\s*%", summary)
                    if match:
                        coverage = float(match.group(1))
                        self.logger.debug(
                            f"Coverage: {coverage}% (threshold: {self.config.coverage_threshold}%)"  # noqa: E501
                        )
                        return coverage >= self.config.coverage_threshold

            # No coverage information found - log warning but don't fail
            self.logger.warning("No coverage information found in PR checks")

            # If coverage threshold is 0, pass by default
            if self.config.coverage_threshold == 0:
                return True

            # Otherwise, fail safe - require explicit coverage
            return False

        except Exception as e:
            self.logger.error(f"Error checking coverage: {e}")
            # Fail safe - if we can't check, assume not met
            return False

    def _calculate_confidence(self, pr: Dict, checks: AutoMergeSafetyChecks) -> float:
        """
        Calculate confidence score for auto-merge decision.

        Factors:
        - Age of PR (older = more confident)
        - Number of commits (fewer = more confident)
        - Number of changed files (fewer = more confident)
        - Author reputation (more merged PRs = more confident)

        Args:
            pr: Pull request data
            checks: Safety check results

        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.0

        # Base confidence from safety checks
        checks_passed = sum(
            [
                checks.all_tests_passed,
                checks.reviews_approved,
                checks.no_conflicts,
                checks.branch_up_to_date,
                checks.coverage_threshold_met,
            ]
        )
        confidence += (checks_passed / 5.0) * 0.5  # 50% weight for checks

        # PR age (older = more confident, up to 7 days)
        from datetime import datetime, timezone

        created_at = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
        age_hours = (datetime.now(timezone.utc) - created_at).total_seconds() / 3600
        age_score = min(1.0, age_hours / (7 * 24))  # Max confidence at 7 days
        confidence += age_score * 0.2  # 20% weight for age

        # Commit count (fewer = more confident)
        commits = pr.get("commits", 0)
        # Penalty after 20 commits
        commit_score = max(0.0, 1.0 - (commits / 20))
        confidence += commit_score * 0.15  # 15% weight for commits

        # Changed files (fewer = more confident)
        changed_files = pr.get("changed_files", 0)
        files_score = max(0.0, 1.0 - (changed_files / 10))  # Penalty after 10 files
        confidence += files_score * 0.15  # 15% weight for files

        return min(1.0, confidence)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check PR eligibility for auto-merge")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--pr", required=True, type=int, help="Pull request number")
    parser.add_argument(
        "--config",
        default=".github/auto-merge.yml",
        help="Path to auto-merge config file",
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
            config_dict = config_loader.load("auto-merge.yml")
            config = AutoMergeConfig(**config_dict.get("auto_merge", {}))
        except FileNotFoundError:
            logger.warning("No auto-merge config found, using defaults")
            config = AutoMergeConfig()

        # Check eligibility
        checker = AutoMergeChecker(client, config)
        result = checker.check_eligibility(args.owner, args.repo, args.pr)

        # Output result
        print(f"\n{'='*60}")
        print("Auto-Merge Eligibility Check")
        print(f"{'='*60}")
        print(f"Repository: {result.repository}")
        print(f"PR Number: {result.pr_number}")
        print(f"Timestamp: {result.timestamp.isoformat()}")
        print(f"\nEligible: {'✅ YES' if result.eligible else '❌ NO'}")
        print(f"Confidence: {result.confidence:.1%}")

        print("\nSafety Checks:")
        print(
            f"  • All tests passed: {'✅' if result.checks_passed.all_tests_passed else '❌'}"  # noqa: E501
        )
        print(
            f"  • Reviews approved: {'✅' if result.checks_passed.reviews_approved else '❌'}"  # noqa: E501
        )
        print(
            f"  • No conflicts: {'✅' if result.checks_passed.no_conflicts else '❌'}"  # noqa: E501
        )
        print(
            f"  • Branch up-to-date: {'✅' if result.checks_passed.branch_up_to_date else '❌'}"  # noqa: E501
        )
        print(
            f"  • Coverage threshold met: {'✅' if result.checks_passed.coverage_threshold_met else '❌'}"  # noqa: E501
        )

        if result.reasons:
            print("\nReasons for ineligibility:")
            for reason in result.reasons:
                print(f"  • {reason}")

        print(f"{'='*60}\n")

        # Exit with appropriate code
        sys.exit(0 if result.eligible else 1)

    except Exception as e:
        logger.error(f"Error checking eligibility: {e}", exc_info=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
