"""Mock fixtures for Month 1 workflow integration tests.

These fixtures enable tests to run without live GitHub API access by providing
mock implementations and sample data.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import pytest


class MockGitHubAPIClient:
    """Mock GitHub API client for integration testing without live API."""

    def __init__(self, token: Optional[str] = None, repo: str = "ivviiviivvi/.github"):
        # "mock_token" is for testing only - not used for real API calls
        self.token = token or "mock_token"
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        # Internal storage for mock issues and PRs
        self._issues: dict[int, dict[str, Any]] = {}
        self._prs: dict[int, dict[str, Any]] = {}
        self._issue_counter = 100
        # Store workflow runs
        self._workflow_runs: dict[str, list[dict[str, Any]]] = {}
        self._setup_default_workflow_runs()

    def _setup_default_workflow_runs(self):
        """Set up default workflow runs for testing."""
        now = datetime.now(timezone.utc)

        # Create successful workflow runs for each workflow
        workflows = [
            "issue-triage.yml",
            "auto-assign.yml",
            "status-sync.yml",
            "stale-management.yml",
            "collect-metrics.yml",
        ]

        for workflow_index, workflow in enumerate(workflows):
            runs = []
            for i in range(25):
                run_time = now - timedelta(days=i)
                runs.append(
                    {
                        "id": workflow_index * 1000 + i,
                        "name": workflow.replace(".yml", "").replace("-", " ").title(),
                        "status": "completed",
                        "conclusion": "success",
                        "created_at": run_time.isoformat(),
                        "updated_at": run_time.isoformat(),
                        "head_branch": "main",
                        "head_sha": f"abc123{i}",
                    }
                )
            self._workflow_runs[workflow] = runs

    def create_issue(self, title: str, body: str, labels: Optional[list[str]] = None) -> dict[str, Any]:
        """Create a mock test issue."""
        self._issue_counter += 1
        issue_number = self._issue_counter

        label_objects = []
        if labels:
            for label in labels:
                label_objects.append({"name": label, "color": "ededed"})

        issue = {
            "number": issue_number,
            "title": title,
            "body": body,
            "labels": label_objects,
            "state": "open",
            "assignee": None,
            "assignees": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "html_url": (f"https://github.com/{self.repo}/issues/{issue_number}"),
        }

        self._issues[issue_number] = issue
        return issue

    def get_issue(self, issue_number: int) -> dict[str, Any]:
        """Get mock issue details."""
        if issue_number not in self._issues:
            raise ValueError(f"Issue {issue_number} not found")
        return self._issues[issue_number]

    def update_issue(
        self,
        issue_number: int,
        state: Optional[str] = None,
        labels: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Update a mock issue."""
        if issue_number not in self._issues:
            raise ValueError(f"Issue {issue_number} not found")

        issue = self._issues[issue_number]

        if state:
            issue["state"] = state
        if labels is not None:
            issue["labels"] = [{"name": lbl, "color": "ededed"} for lbl in labels]

        issue["updated_at"] = datetime.now(timezone.utc).isoformat()
        return issue

    def create_pr(self, title: str, body: str, head: str, base: str = "main") -> dict[str, Any]:
        """Create a mock test pull request."""
        self._issue_counter += 1
        pr_number = self._issue_counter

        pr = {
            "number": pr_number,
            "title": title,
            "body": body,
            "head": {"ref": head},
            "base": {"ref": base},
            "state": "open",
            "merged": False,
            "html_url": f"https://github.com/{self.repo}/pull/{pr_number}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._prs[pr_number] = pr
        return pr

    def get_pr(self, pr_number: int) -> dict[str, Any]:
        """Get mock pull request details."""
        if pr_number not in self._prs:
            # Return a default mock PR if not found
            return {
                "number": pr_number,
                "title": f"Mock PR #{pr_number}",
                "body": "Mock PR body",
                "state": "open",
                "merged": False,
            }
        return self._prs[pr_number]

    def trigger_workflow(self, workflow_id: str, ref: str = "main") -> None:
        """Mock trigger a workflow dispatch event."""
        # Simulate workflow triggering by processing the relevant issues
        self._process_workflow(workflow_id)

    def _process_workflow(self, workflow_id: str) -> None:
        """Simulate workflow processing on issues."""
        if workflow_id == "issue-triage.yml":
            self._process_triage()
        elif workflow_id == "auto-assign.yml":
            self._process_auto_assign()
        elif workflow_id == "status-sync.yml":
            self._process_status_sync()
        elif workflow_id == "stale-management.yml":
            self._process_stale_management()

    def _process_triage(self) -> None:
        """Simulate issue triage workflow."""
        for _issue_number, issue in self._issues.items():
            labels = [lbl["name"] for lbl in issue.get("labels", [])]
            new_labels = labels.copy()
            title_lower = issue["title"].lower()

            # Add priority labels based on existing labels or title
            is_bug = "bug" in labels or "[bug]" in title_lower
            is_enhancement = "enhancement" in labels or "[feature]" in title_lower

            if is_bug:
                if "priority:high" not in labels:
                    new_labels.append("priority:high")
            elif is_enhancement and not any("priority:" in lbl for lbl in labels):
                new_labels.append("priority:medium")

            # Add category labels based on title
            if "documentation" in title_lower or "readme" in title_lower:
                if "documentation" not in labels:
                    new_labels.append("documentation")

            # Update issue labels
            issue["labels"] = [{"name": lbl, "color": "ededed"} for lbl in new_labels]

    def _process_auto_assign(self) -> None:
        """Simulate auto-assignment workflow."""
        for _issue_number, issue in self._issues.items():
            # Auto-assign unassigned issues
            if issue.get("assignee") is None:
                labels = [lbl["name"] for lbl in issue.get("labels", [])]

                # Assign based on labels/expertise
                if "automation" in labels:
                    assignee = "automation-expert"
                elif "bug" in labels:
                    assignee = "bug-triager"
                else:
                    assignee = "default-assignee"

                issue["assignee"] = {"login": assignee}
                issue["assignees"] = [{"login": assignee}]

    def _process_status_sync(self) -> None:
        """Simulate status synchronization workflow."""
        # This workflow syncs PR and issue statuses
        pass

    def _process_stale_management(self) -> None:
        """Simulate stale management workflow."""
        for _issue_number, issue in self._issues.items():
            labels = [lbl["name"] for lbl in issue.get("labels", [])]

            # Don't mark pinned issues as stale
            if "pinned" in labels:
                continue

            # Stale logic would check last update time
            # For testing, we don't add stale label automatically

    def get_workflow_runs(self, workflow_id: str, limit: int = 10) -> list[dict[str, Any]]:
        """Get mock recent workflow runs."""
        if workflow_id not in self._workflow_runs:
            return []
        return self._workflow_runs[workflow_id][:limit]

    def wait_for_workflow_completion(self, run_id: int, timeout: int = 300, poll_interval: int = 10) -> dict[str, Any]:
        """Mock wait for a workflow run to complete."""
        return {
            "id": run_id,
            "status": "completed",
            "conclusion": "success",
        }

    def close_issue(self, issue_number: int) -> None:
        """Close a mock issue."""
        self.update_issue(issue_number, state="closed")

    def delete_label(self, issue_number: int, label: str) -> None:
        """Remove a label from a mock issue."""
        if issue_number in self._issues:
            issue = self._issues[issue_number]
            issue["labels"] = [lbl for lbl in issue["labels"] if lbl["name"] != label]


@pytest.fixture
def mock_github_client():
    """Mock GitHubAPIClient for integration tests."""
    return MockGitHubAPIClient()


@pytest.fixture
def github_client():
    """Pytest fixture for GitHub API client - uses mock for testing."""
    return MockGitHubAPIClient()


@pytest.fixture
def mock_issue_data():
    """Sample issue data for testing."""
    return {
        "number": 42,
        "title": "[BUG] Test issue for mock data",
        "body": "This is a mock issue body for testing purposes",
        "labels": [
            {"name": "bug", "color": "d73a4a"},
            {"name": "priority:high", "color": "ff0000"},
        ],
        "state": "open",
        "assignee": {"login": "test-user"},
        "assignees": [{"login": "test-user"}],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "html_url": "https://github.com/ivviiviivvi/.github/issues/42",
    }


@pytest.fixture
def mock_workflow_runs():
    """Mock workflow run data."""
    now = datetime.now(timezone.utc)
    runs = []

    for i in range(20):
        run_time = now - timedelta(days=i)
        runs.append(
            {
                "id": 1000 + i,
                "name": "Test Workflow",
                "status": "completed",
                "conclusion": "success",
                "created_at": run_time.isoformat(),
                "updated_at": run_time.isoformat(),
                "head_branch": "main",
                "head_sha": f"abc123{i}",
            }
        )

    return runs


@pytest.fixture
def mock_metrics_data():
    """Mock metrics collection results."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "workflows": {
            "issue-triage": {"runs": 100, "success": 98, "failure": 2},
            "auto-assign": {"runs": 100, "success": 99, "failure": 1},
            "status-sync": {"runs": 100, "success": 100, "failure": 0},
            "stale-management": {"runs": 100, "success": 97, "failure": 3},
            "collect-metrics": {"runs": 30, "success": 30, "failure": 0},
        },
        "overall_success_rate": 0.978,
        "month1_target": 0.975,
        "status": "passing",
    }


@pytest.fixture
def mock_test_issue(mock_github_client):
    """Create a mock test issue and clean up after test."""
    issue = mock_github_client.create_issue(
        title=f"[TEST] Integration test issue {datetime.now(timezone.utc).isoformat()}",
        body="Test issue created by integration tests. Will be deleted.",
    )

    yield issue

    # Cleanup - ignore errors since this is test teardown
    try:
        mock_github_client.close_issue(issue["number"])
    except Exception:  # noqa: S110 - cleanup failure shouldn't fail tests
        pass


@pytest.fixture
def test_issue(github_client):
    """Create a test issue and clean up after test."""
    issue = github_client.create_issue(
        title=f"[TEST] Integration test issue {datetime.now(timezone.utc).isoformat()}",
        body="Test issue created by integration tests. Will be deleted.",
    )

    yield issue

    # Cleanup - ignore errors since this is test teardown
    try:
        github_client.close_issue(issue["number"])
    except Exception:  # noqa: S110 - cleanup failure shouldn't fail tests
        pass
