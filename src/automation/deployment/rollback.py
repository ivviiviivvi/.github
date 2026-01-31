#!/usr/bin/env python3
"""Rollback Automation.

Quickly rollback deployments to previous working state.

Usage:
    ./rollback.py --deployment-id 20250101_120000 --dry-run
    ./rollback.py --deployment-id 20250101_120000 --execute
    ./rollback.py --repo org/repo --to-commit abc123
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests


class RollbackManager:
    """Manages rollback operations for workflow deployments."""

    def __init__(self, github_token: str):
        """Initialize rollback manager.

        Args:
            github_token: GitHub API token

        """
        self.github_token = github_token
        self.api_base = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    def load_deployment_log(self, deployment_id: str) -> dict:
        """Load deployment log file.

        Args:
            deployment_id: Deployment identifier

        Returns:
            Deployment log data

        """
        log_file = Path(f"automation/deployment/logs/{deployment_id}.json")

        if not log_file.exists():
            raise FileNotFoundError(f"Deployment log not found: {log_file}")

        with open(log_file) as f:
            return json.load(f)

    def rollback_deployment(self, deployment_id: str, dry_run: bool = True) -> bool:
        """Rollback entire deployment.

        Args:
            deployment_id: Deployment identifier
            dry_run: If True, only show what would be done

        Returns:
            True if rollback succeeded

        """
        print(
            f"\n⏪ {'[DRY RUN] ' if dry_run else ''}Rolling back deployment: {deployment_id}"
        )

        # Load deployment log
        try:
            log = self.load_deployment_log(deployment_id)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return False

        deployments = log.get("deployments", [])
        print(f"   Found {len(deployments)} repositories to rollback")

        # Rollback each repository
        success_count = 0
        for deployment in deployments:
            repo = deployment["repo"]
            month = deployment["month"]

            print(f"\n   Rolling back: {repo} (Month {month})")

            if dry_run:
                print(f"      [DRY RUN] Would rollback workflows for Month {month}")
                success_count += 1
            else:
                if self._rollback_repository(repo, month):
                    print("      ✅ Rollback successful")
                    success_count += 1
                else:
                    print("      ❌ Rollback failed")

        # Summary
        print(
            f"\n{'[DRY RUN] ' if dry_run else ''}Rollback complete: {success_count}/{len(deployments)} successful"
        )

        if not dry_run:
            # Save rollback log
            self._save_rollback_log(deployment_id, deployments, success_count)

        return success_count == len(deployments)

    def _rollback_repository(self, repo: str, month: int) -> bool:
        """Rollback workflows in a single repository.

        Args:
            repo: Repository name (org/repo)
            month: Month that was deployed

        Returns:
            True if rollback succeeded

        """
        try:
            # Get workflow files for month
            workflows = self._get_workflows_for_month(month)

            # Find previous version for each workflow
            for workflow_file in workflows:
                # Get file history
                file_path = f".github/workflows/{workflow_file}"

                response = self.session.get(
                    f"{self.api_base}/repos/{repo}/commits",
                    params={"path": file_path, "per_page": "5"},
                )

                if response.status_code != 200:
                    print(f"         Error getting history for {file_path}")
                    continue

                commits = response.json()

                # Find commit before deployment
                if len(commits) < 2:
                    print(f"         No previous version for {file_path}")
                    continue

                previous_commit = commits[1]  # Second most recent
                previous_sha = previous_commit["sha"]

                # Revert to previous version
                if not self._revert_file(repo, file_path, previous_sha):
                    return False

            return True

        except Exception as e:
            print(f"         Error: {e}")
            return False

    def _revert_file(self, repo: str, file_path: str, commit_sha: str) -> bool:
        """Revert file to specific commit."""
        try:
            # Get file content at commit
            response = self.session.get(
                f"{self.api_base}/repos/{repo}/contents/{file_path}",
                params={"ref": commit_sha},
            )

            if response.status_code != 200:
                return False

            file_data = response.json()
            content = file_data["content"]

            # Get current file SHA
            current_response = self.session.get(
                f"{self.api_base}/repos/{repo}/contents/{file_path}"
            )

            if current_response.status_code != 200:
                return False

            current_sha = current_response.json()["sha"]

            # Update file
            update_response = self.session.put(
                f"{self.api_base}/repos/{repo}/contents/{file_path}",
                json={
                    "message": f"Rollback: revert {file_path} to {commit_sha[:7]}",
                    "content": content,
                    "sha": current_sha,
                },
            )

            return update_response.status_code in [200, 201]

        except Exception as e:
            print(f"         Error reverting file: {e}")
            return False

    def rollback_repository_to_commit(
        self, repo: str, commit_sha: str, dry_run: bool = True
    ) -> bool:
        """Rollback repository workflows to specific commit.

        Args:
            repo: Repository name (org/repo)
            commit_sha: Target commit SHA
            dry_run: If True, only show what would be done

        Returns:
            True if rollback succeeded

        """
        print(
            f"\n⏪ {'[DRY RUN] ' if dry_run else ''}Rolling back {repo} to {commit_sha[:7]}"
        )

        if dry_run:
            print("   [DRY RUN] Would revert all workflow files to specified commit")
            return True

        # Get all workflow files
        try:
            response = self.session.get(
                f"{self.api_base}/repos/{repo}/contents/.github/workflows"
            )

            if response.status_code != 200:
                print("   ❌ Failed to get workflow files")
                return False

            files = response.json()

            # Revert each file
            success_count = 0
            for file_info in files:
                if file_info["name"].endswith(".yml") or file_info["name"].endswith(
                    ".yaml"
                ):
                    file_path = file_info["path"]
                    print(f"   Reverting: {file_path}...", end=" ")

                    if self._revert_file(repo, file_path, commit_sha):
                        print("✅")
                        success_count += 1
                    else:
                        print("❌")

            print(f"\n   Rollback complete: {success_count}/{len(files)} files")
            return success_count == len(files)

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def _get_workflows_for_month(self, month: int) -> list[str]:
        """Get workflow files for specific month."""
        # Month 1 workflows
        month1_workflows = [
            "issue-triage.yml",
            "auto-assign.yml",
            "status-sync.yml",
            "stale-management.yml",
            "collect-metrics.yml",
        ]

        # Month 2 workflows
        month2_workflows = [
            "slack-daily-summary.yml",
            "stale-management-ab.yml",
            "email-digest.yml",
        ]

        # Month 3 workflows
        month3_workflows = [
            "auto-merge.yml",
            "self-healing.yml",
            "proactive-maintenance.yml",
            "sla-monitoring.yml",
            "incident-response.yml",
        ]

        workflow_map = {
            1: month1_workflows,
            2: month2_workflows,
            3: month3_workflows,
        }

        return workflow_map.get(month, [])

    def _save_rollback_log(
        self, deployment_id: str, deployments: list[dict], success_count: int
    ):
        """Save rollback log."""
        log_file = Path(f"automation/deployment/logs/rollback_{deployment_id}.json")

        with open(log_file, "w") as f:
            json.dump(
                {
                    "deployment_id": deployment_id,
                    "rollback_timestamp": datetime.now().isoformat(),
                    "repositories": len(deployments),
                    "successful": success_count,
                    "deployments": deployments,
                },
                f,
                indent=2,
            )

        print(f"\n📝 Rollback log saved: {log_file}")


def main():
    """Main rollback execution."""
    parser = argparse.ArgumentParser(description="Rollback workflow deployments")
    parser.add_argument("--deployment-id", type=str, help="Deployment ID to rollback")
    parser.add_argument("--repo", type=str, help="Repository to rollback (org/repo)")
    parser.add_argument("--to-commit", type=str, help="Commit SHA to rollback to")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )
    parser.add_argument("--execute", action="store_true", help="Execute rollback")

    args = parser.parse_args()

    # Validate arguments
    if not args.dry_run and not args.execute:
        print("❌ Must specify --dry-run or --execute")
        sys.exit(1)

    dry_run = args.dry_run

    # Get GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set!")
        sys.exit(1)

    # Initialize rollback manager
    manager = RollbackManager(github_token)

    # Perform rollback
    success = False

    if args.deployment_id:
        # Rollback entire deployment
        success = manager.rollback_deployment(args.deployment_id, dry_run)
    elif args.repo and args.to_commit:
        # Rollback specific repository to commit
        success = manager.rollback_repository_to_commit(
            args.repo, args.to_commit, dry_run
        )
    else:
        print("❌ Must specify --deployment-id or (--repo and --to-commit)")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
