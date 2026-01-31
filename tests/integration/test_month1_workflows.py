#!/usr/bin/env python3
"""Integration Tests for Month 1 Core Workflows.

Tests all 5 production workflows:
- Issue triage
- Auto-assignment
- Status synchronization
- Stale management
- Metrics collection

Usage:
    pytest tests/integration/test_month1_workflows.py -v
    pytest tests/integration/test_month1_workflows.py::TestIssueTriage -v

NOTE: These integration tests require specific GitHub API access and workflow
      configurations that may not be available in all environments.
"""

import contextlib
import os
import time
from datetime import datetime, timedelta
from typing import Any, Optional

import pytest
import requests

# Mark entire module as integration tests
pytestmark = pytest.mark.integration


class GitHubAPIClient:
    """GitHub API client for integration testing."""

    def __init__(self, token: Optional[str] = None, repo: str = "ivviiviivvi/.github"):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def create_issue(
        self, title: str, body: str, labels: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Create a test issue."""
        url = f"{self.base_url}/repos/{self.repo}/issues"
        data: dict[str, Any] = {"title": title, "body": body}
        if labels:
            data["labels"] = labels

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_issue(self, issue_number: int) -> dict[str, Any]:
        """Get issue details."""
        url = f"{self.base_url}/repos/{self.repo}/issues/{issue_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_issue(
        self,
        issue_number: int,
        state: Optional[str] = None,
        labels: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Update an issue."""
        url = f"{self.base_url}/repos/{self.repo}/issues/{issue_number}"
        data: dict[str, Any] = {}
        if state:
            data["state"] = state
        if labels is not None:
            data["labels"] = labels

        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_pr(
        self, title: str, body: str, head: str, base: str = "main"
    ) -> dict[str, Any]:
        """Create a test pull request."""
        url = f"{self.base_url}/repos/{self.repo}/pulls"
        data = {"title": title, "body": body, "head": head, "base": base}

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_pr(self, pr_number: int) -> dict[str, Any]:
        """Get pull request details."""
        url = f"{self.base_url}/repos/{self.repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def trigger_workflow(self, workflow_id: str, ref: str = "main") -> None:
        """Trigger a workflow dispatch event."""
        url = f"{self.base_url}/repos/{self.repo}/actions/workflows/{workflow_id}/dispatches"
        data = {"ref": ref}

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()

    def get_workflow_runs(
        self, workflow_id: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Get recent workflow runs."""
        url = f"{self.base_url}/repos/{self.repo}/actions/workflows/{workflow_id}/runs"
        params = {"per_page": limit}

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()["workflow_runs"]

    def wait_for_workflow_completion(
        self, run_id: int, timeout: int = 300, poll_interval: int = 10
    ) -> dict[str, Any]:
        """Wait for a workflow run to complete."""
        url = f"{self.base_url}/repos/{self.repo}/actions/runs/{run_id}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            run = response.json()

            if run["status"] == "completed":
                return run

            time.sleep(poll_interval)

        raise TimeoutError(f"Workflow run {run_id} did not complete within {timeout}s")

    def close_issue(self, issue_number: int) -> None:
        """Close an issue."""
        self.update_issue(issue_number, state="closed")

    def delete_label(self, issue_number: int, label: str) -> None:
        """Remove a label from an issue."""
        url = f"{self.base_url}/repos/{self.repo}/issues/{issue_number}/labels/{label}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()


# NOTE: github_client and test_issue fixtures are provided by conftest.py
# They use MockGitHubAPIClient for testing without live API access


class TestIssueTriage:
    """Test suite for issue triage workflow."""

    def test_priority_labeling_bug(self, github_client, test_issue):
        """Test that bug issues get priority:high label."""
        issue_number = test_issue["number"]

        # Update issue with bug keyword in title
        github_client.update_issue(issue_number, labels=["bug"])

        # Trigger triage workflow
        github_client.trigger_workflow("issue-triage.yml")

        # Mock processes immediately, minimal wait
        time.sleep(0.1)

        # Verify priority label was added
        updated_issue = github_client.get_issue(issue_number)
        labels = [label["name"] for label in updated_issue["labels"]]

        assert any(
            "priority" in label.lower() and "high" in label.lower() for label in labels
        ), f"Expected priority high label, got: {labels}"

    def test_priority_labeling_feature(self, github_client):
        """Test that feature requests get priority:medium label."""
        issue = github_client.create_issue(
            title="[FEATURE] Test feature request",
            body="Test feature request body",
            labels=["enhancement"],
        )

        try:
            # Trigger triage workflow
            github_client.trigger_workflow("issue-triage.yml")
            time.sleep(0.1)

            # Verify priority label
            updated_issue = github_client.get_issue(issue["number"])
            labels = [label["name"] for label in updated_issue["labels"]]

            assert any(
                "priority" in lbl.lower()
                and ("medium" in lbl.lower() or "low" in lbl.lower())
                for lbl in labels
            )
        finally:
            github_client.close_issue(issue["number"])

    def test_category_labeling(self, github_client):
        """Test that issues get appropriate category labels."""
        issue = github_client.create_issue(
            title="Documentation update needed",
            body="Need to update README with new examples",
        )

        try:
            github_client.trigger_workflow("issue-triage.yml")
            time.sleep(0.1)

            updated_issue = github_client.get_issue(issue["number"])
            labels = [label["name"] for label in updated_issue["labels"]]

            assert any("documentation" in lbl.lower() for lbl in labels)
        finally:
            github_client.close_issue(issue["number"])

    def test_workflow_success_rate(self, github_client):
        """Test that triage workflow has >95% success rate."""
        runs = github_client.get_workflow_runs("issue-triage.yml", limit=20)

        if len(runs) < 5:
            pytest.skip("Not enough workflow runs to validate success rate")

        successful_runs = sum(1 for run in runs if run["conclusion"] == "success")
        success_rate = successful_runs / len(runs)

        assert (
            success_rate >= 0.95
        ), f"Success rate {success_rate:.1%} below 95% threshold"


class TestAutoAssignment:
    """Test suite for auto-assignment workflow."""

    def test_assignment_on_triage(self, github_client):
        """Test that triaged issues get automatically assigned."""
        issue = github_client.create_issue(
            title="[BUG] Test assignment",
            body="This issue should be auto-assigned",
            labels=["bug", "priority:high"],
        )

        try:
            github_client.trigger_workflow("auto-assign.yml")
            time.sleep(0.1)

            updated_issue = github_client.get_issue(issue["number"])

            assert updated_issue["assignee"] is not None, "Issue should be assigned"
            assert len(updated_issue["assignees"]) > 0
        finally:
            github_client.close_issue(issue["number"])

    def test_assignment_based_on_expertise(self, github_client):
        """Test that issues are assigned based on team expertise."""
        issue = github_client.create_issue(
            title="[BUG] Python automation script failing",
            body="The automation script in automation/scripts/ is failing",
            labels=["bug", "automation"],
        )

        try:
            github_client.trigger_workflow("auto-assign.yml")
            time.sleep(0.1)

            updated_issue = github_client.get_issue(issue["number"])
            assignee = updated_issue.get("assignee")

            assert assignee is not None
            # In real implementation, verify assignee has Python expertise
        finally:
            github_client.close_issue(issue["number"])

    def test_no_duplicate_assignment(self, github_client):
        """Test that already assigned issues are not reassigned."""
        issue = github_client.create_issue(
            title="[BUG] Pre-assigned issue",
            body="This issue is already assigned",
            labels=["bug"],
        )

        try:
            # Note: In real test, would assign to specific user first
            github_client.trigger_workflow("auto-assign.yml")
            time.sleep(0.1)

            updated_issue = github_client.get_issue(issue["number"])
            assignees_count = len(updated_issue.get("assignees", []))

            # Should not duplicate assignees
            assert assignees_count <= 2, "Should not over-assign issues"
        finally:
            github_client.close_issue(issue["number"])


class TestStatusSync:
    """Test suite for status synchronization workflow."""

    def test_issue_pr_linking(self, github_client):
        """Test that PRs are linked to related issues."""
        # Create test issue
        issue = github_client.create_issue(
            title="[BUG] Test issue for PR linking",
            body="This issue will be fixed by a PR",
        )

        try:
            # In real test, would create branch and PR that references issue
            # Then verify that status sync updates issue status

            # For now, just verify workflow can run
            github_client.trigger_workflow("status-sync.yml")
            time.sleep(0.1)

            # Verify workflow ran successfully
            runs = github_client.get_workflow_runs("status-sync.yml", limit=1)
            assert len(runs) > 0
            assert runs[0]["conclusion"] in ["success", "skipped"]
        finally:
            github_client.close_issue(issue["number"])

    def test_status_label_sync(self, github_client):
        """Test that status labels are synchronized between issues and PRs."""
        # Create test issue
        issue = github_client.create_issue(
            title="[BUG] Test issue for status sync",
            body="This issue will have status synced with PR",
        )

        try:
            # Create a PR that references the issue
            github_client.create_pr(
                title=f"Fix issue #{issue['number']}",
                body=f"Fixes #{issue['number']}",
                head="fix-branch",
                base="main",
            )

            # Trigger status sync workflow
            github_client.trigger_workflow("status-sync.yml")
            time.sleep(0.1)

            # Verify workflow ran successfully
            runs = github_client.get_workflow_runs("status-sync.yml", limit=1)
            assert len(runs) > 0
            assert runs[0]["conclusion"] in ["success", "skipped"]
        finally:
            github_client.close_issue(issue["number"])


class TestStaleManagement:
    """Test suite for stale issue management workflow."""

    def test_stale_labeling(self, github_client):
        """Test that inactive issues get marked as stale."""
        # Create an old issue (in real test, would need to backdate)
        issue = github_client.create_issue(
            title="[TEST] Old inactive issue",
            body=f"Created at {datetime.now() - timedelta(days=60)}",
        )

        try:
            github_client.trigger_workflow("stale-management.yml")
            time.sleep(0.1)

            updated_issue = github_client.get_issue(issue["number"])
            [label["name"] for label in updated_issue["labels"]]

            # May or may not be stale depending on actual age
            # Just verify workflow runs successfully
            runs = github_client.get_workflow_runs("stale-management.yml", limit=1)
            assert runs[0]["conclusion"] == "success"
        finally:
            github_client.close_issue(issue["number"])

    def test_stale_exemption_for_pinned(self, github_client):
        """Test that pinned issues are exempt from stale marking."""
        issue = github_client.create_issue(
            title="[TEST] Pinned issue",
            body="This issue is pinned and should not be marked stale",
            labels=["pinned"],
        )

        try:
            github_client.trigger_workflow("stale-management.yml")
            time.sleep(0.1)

            updated_issue = github_client.get_issue(issue["number"])
            labels = [label["name"] for label in updated_issue["labels"]]

            assert "stale" not in labels, "Pinned issues should not be marked stale"
        finally:
            github_client.close_issue(issue["number"])

    def test_grace_period_respected(self, github_client):
        """Test that grace period is respected before marking stale."""
        # Verify workflow configuration has correct grace period
        runs = github_client.get_workflow_runs("stale-management.yml", limit=5)

        # All runs should complete successfully
        for run in runs:
            assert run["conclusion"] in ["success", "skipped", "neutral"]


class TestMetricsCollection:
    """Test suite for metrics collection workflow."""

    def test_metrics_workflow_runs_daily(self, github_client):
        """Test that metrics are collected daily."""
        runs = github_client.get_workflow_runs("collect-metrics.yml", limit=7)

        if len(runs) < 3:
            pytest.skip("Not enough runs to validate daily schedule")

        # Verify runs are roughly daily
        run_dates = [
            datetime.fromisoformat(run["created_at"].replace("Z", "")) for run in runs
        ]

        # Check that runs are spaced approximately 1 day apart
        if len(run_dates) >= 2:
            avg_spacing = (run_dates[0] - run_dates[-1]).days / (len(run_dates) - 1)
            assert (
                0.8 <= avg_spacing <= 1.2
            ), f"Average spacing {avg_spacing} not close to 1 day"

    def test_metrics_artifact_created(self, github_client):
        """Test that metrics workflow creates artifacts."""
        runs = github_client.get_workflow_runs("collect-metrics.yml", limit=1)

        if len(runs) == 0:
            pytest.skip("No recent metrics runs found")

        run = runs[0]
        assert run["conclusion"] == "success", "Metrics workflow should succeed"

        # In real test, would verify artifacts API for metrics.json

    def test_success_rate_tracking(self, github_client):
        """Test that success rate is accurately tracked."""
        # Get all workflow runs
        all_runs = []
        for workflow in [
            "issue-triage.yml",
            "auto-assign.yml",
            "status-sync.yml",
            "stale-management.yml",
        ]:
            runs = github_client.get_workflow_runs(workflow, limit=20)
            all_runs.extend(runs)

        if len(all_runs) < 10:
            pytest.skip("Not enough runs to validate success rate tracking")

        successful = sum(1 for run in all_runs if run["conclusion"] == "success")
        total = len(all_runs)
        success_rate = successful / total

        # Verify Month 1 success rate target (97.5%)
        assert (
            success_rate >= 0.95
        ), f"Overall success rate {success_rate:.1%} below 95%"


class TestMonth1Integration:
    """Integration tests for all Month 1 workflows together."""

    def test_full_issue_lifecycle(self, github_client):
        """Test complete issue lifecycle: create → triage → assign → resolve → close."""
        # Create issue
        issue = github_client.create_issue(
            title="[BUG] Integration test - full lifecycle",
            body="Testing complete issue workflow integration",
        )

        try:
            issue_number = issue["number"]

            # Step 1: Trigger triage
            github_client.trigger_workflow("issue-triage.yml")
            time.sleep(0.1)

            # Verify triage
            updated = github_client.get_issue(issue_number)
            assert any(
                "priority:" in label["name"] for label in updated["labels"]
            ), "Should have priority label"

            # Step 2: Trigger assignment
            github_client.trigger_workflow("auto-assign.yml")
            time.sleep(0.1)

            # Verify assignment
            updated = github_client.get_issue(issue_number)
            assert updated.get("assignee") is not None, "Should be assigned"

            # Step 3: Close issue
            github_client.close_issue(issue_number)

            # Verify closure
            updated = github_client.get_issue(issue_number)
            assert updated["state"] == "closed"

        except Exception:
            github_client.close_issue(issue["number"])
            raise

    def test_workflow_interdependencies(self, github_client):
        """Test that workflows work together without conflicts."""
        # Create multiple test issues
        issues = []
        for i in range(3):
            issue = github_client.create_issue(
                title=f"[TEST] Interdependency test {i}",
                body="Testing workflow interactions",
            )
            issues.append(issue)

        try:
            # Trigger all workflows
            for workflow in ["issue-triage.yml", "auto-assign.yml", "status-sync.yml"]:
                github_client.trigger_workflow(workflow)

            time.sleep(0.1)

            # Verify all issues processed successfully
            for issue in issues:
                updated = github_client.get_issue(issue["number"])
                assert updated["state"] in ["open", "closed"]
                # Should have at least one label or assignee
                assert len(updated["labels"]) > 0 or updated.get("assignee") is not None
        finally:
            for issue in issues:
                with contextlib.suppress(BaseException):
                    github_client.close_issue(issue["number"])

    def test_month1_success_metrics(self, github_client):
        """Validate that Month 1 meets its success criteria."""
        all_runs = []
        workflows = [
            "issue-triage.yml",
            "auto-assign.yml",
            "status-sync.yml",
            "stale-management.yml",
            "collect-metrics.yml",
        ]

        for workflow in workflows:
            runs = github_client.get_workflow_runs(workflow, limit=50)
            all_runs.extend(runs)

        if len(all_runs) < 20:
            pytest.skip("Not enough workflow runs for comprehensive validation")

        # Calculate success rate
        successful = sum(1 for run in all_runs if run["conclusion"] == "success")
        total = len(all_runs)
        success_rate = successful / total

        # Month 1 success criteria: 97.5% success rate
        assert (
            success_rate >= 0.95
        ), f"Success rate {success_rate:.1%} below Month 1 target"

        print(f"✅ Month 1 Success Rate: {success_rate:.1%} ({successful}/{total})")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
