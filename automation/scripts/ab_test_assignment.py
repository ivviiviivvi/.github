#!/usr/bin/env python3
"""A/B Test Assignment Script for Stale Grace Period Optimization.

Assigns repositories to control or experiment groups using consistent hashing.
Ensures 50/50 split and deterministic assignment based on repository name.

Usage:
    python3 ab_test_assignment.py --config ab-test-config.yml
    python3 ab_test_assignment.py --repo owner/repo
    python3 ab_test_assignment.py --all
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional, cast  # noqa: UP035

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(1)


class ABTestAssigner:
    """Assigns repositories to A/B test groups using consistent hashing."""

    def __init__(self, config_path: str = "automation/config/ab-test-config.yml"):
        """Initialize with configuration file."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.seed = self.config["split"]["seed"]

    def _load_config(self) -> dict:
        """Load A/B test configuration from YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path) as f:
            return cast(dict[Any, Any], yaml.safe_load(f))

    def _hash_repository(self, repo_name: str) -> int:
        """Generate consistent hash for repository name."""
        # Combine repo name with seed for consistent, deterministic hashing
        hash_input = f"{repo_name}:{self.seed}".encode()
        hash_digest = hashlib.sha256(hash_input).hexdigest()
        # Convert first 8 hex chars to integer
        return int(hash_digest[:8], 16)

    def assign_group(self, repo_name: str) -> str:
        """Assign repository to control or experiment group.

        Args:
            repo_name: Repository name (format: "owner/repo")

        Returns:
            Group name: "control" or "experiment"

        """
        # Check if repository is excluded
        if self._is_excluded(repo_name):
            return "excluded"

        # Hash repository name and use modulo for 50/50 split
        hash_value = self._hash_repository(repo_name)

        # Even hash = control, odd hash = experiment
        if hash_value % 2 == 0:
            return "control"
        else:
            return "experiment"

    def _is_excluded(self, repo_name: str) -> bool:
        """Check if repository is excluded from test."""
        excludes = self.config["repositories"].get("exclude", [])

        for pattern in excludes:
            if pattern == repo_name:
                return True
            # Handle wildcard patterns like "security/*"
            if "*" in pattern:
                prefix = pattern.replace("/*", "/")
                if repo_name.startswith(prefix):
                    return True

        return False

    def get_group_config(self, group: str) -> Optional[dict]:
        """Get configuration for a specific group."""
        if group == "excluded":
            return None
        return cast(Optional[dict[Any, Any]], self.config["groups"].get(group))

    def get_grace_period(self, repo_name: str) -> int:
        """Get grace period in days for a repository.

        Args:
            repo_name: Repository name (format: "owner/repo")

        Returns:
            Grace period in days (7 or 10)

        """
        group = self.assign_group(repo_name)
        if group == "excluded":
            return 7  # Default to control value

        group_config = self.get_group_config(group)
        if group_config is None:
            return 7
        return cast(int, group_config["gracePeriod"])

    def generate_workflow_config(self, repo_name: str) -> dict:
        """Generate workflow configuration for a repository.

        Args:
            repo_name: Repository name (format: "owner/repo")

        Returns:
            Dictionary with workflow configuration

        """
        group = self.assign_group(repo_name)

        if group == "excluded":
            return {
                "repository": repo_name,
                "group": "excluded",
                "reason": "Excluded from A/B test",
                "gracePeriod": 7,
                "closeAfter": 7,
            }

        group_config = self.get_group_config(group)
        if group_config is None:
            return {
                "repository": repo_name,
                "group": "unknown",
                "reason": "No configuration found",
                "gracePeriod": 7,
                "closeAfter": 7,
            }

        return {
            "repository": repo_name,
            "group": group,
            "groupName": str(group_config["name"]),
            "gracePeriod": int(group_config["gracePeriod"]),
            "closeAfter": int(group_config["closeAfter"]),
            "percentage": int(group_config["percentage"]),
        }

    def list_all_repositories(self) -> list[str]:
        """List all repositories in the organization using GitHub CLI."""
        try:
            result = subprocess.run(  # nosec B603 B607
                [
                    "gh",
                    "repo",
                    "list",
                    "--json",
                    "nameWithOwner",
                    "--limit",
                    "1000",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            repos = json.loads(result.stdout)
            return [repo["nameWithOwner"] for repo in repos]

        except subprocess.CalledProcessError as e:
            print(f"Error listing repositories: {e}", file=sys.stderr)
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing repository list: {e}", file=sys.stderr)
            return []

    def assign_all_repositories(self) -> dict[str, list[str]]:
        """Assign all repositories to groups.

        Returns:
            Dictionary with group assignments:
            {"control": [...], "experiment": [...], "excluded": [...]}

        """
        repos = self.list_all_repositories()

        assignments: dict[str, list[str]] = {
            "control": [],
            "experiment": [],
            "excluded": [],
        }

        for repo in repos:
            group = self.assign_group(repo)
            assignments[group].append(repo)

        return assignments

    def generate_report(self) -> dict:
        """Generate A/B test assignment report."""
        assignments = self.assign_all_repositories()

        control_count = len(assignments["control"])
        experiment_count = len(assignments["experiment"])
        excluded_count = len(assignments["excluded"])
        total_active = control_count + experiment_count

        report = {
            "testName": self.config["test"]["name"],
            "startDate": self.config["test"]["startDate"],
            "assignments": {
                "control": {
                    "count": control_count,
                    "percentage": (round(control_count / total_active * 100, 1) if total_active > 0 else 0),
                    "repositories": sorted(assignments["control"]),
                },
                "experiment": {
                    "count": experiment_count,
                    "percentage": (round(experiment_count / total_active * 100, 1) if total_active > 0 else 0),
                    "repositories": sorted(assignments["experiment"]),
                },
                "excluded": {
                    "count": excluded_count,
                    "repositories": sorted(assignments["excluded"]),
                },
            },
            "totalActive": total_active,
            "splitRatio": f"{control_count}:{experiment_count}",
        }

        return report


def print_table(data: list[list[str]], headers: list[str]):
    """Print data in table format."""
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Print header
    header_row = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_row)
    print("-" * len(header_row))

    # Print data
    for row in data:
        print(" | ".join(str(cell).ljust(w) for cell, w in zip(row, widths)))


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="A/B test assignment for stale grace period optimization")
    parser.add_argument(
        "--config",
        default="automation/config/ab-test-config.yml",
        help="Path to A/B test configuration file",
    )
    parser.add_argument(
        "--repo",
        help="Check assignment for specific repository (format: owner/repo)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Assign all repositories and generate report",
    )
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    try:
        assigner = ABTestAssigner(args.config)

        if args.repo:
            # Single repository assignment
            config = assigner.generate_workflow_config(args.repo)

            if args.json:
                print(json.dumps(config, indent=2))
            else:
                print(f"\nRepository: {config['repository']}")
                print(f"Group: {config['group']}")
                if config["group"] != "excluded":
                    print(f"Group Name: {config['groupName']}")
                    print(f"Grace Period: {config['gracePeriod']} days")
                    print(f"Close After: {config['closeAfter']} days")
                else:
                    print(f"Reason: {config['reason']}")

        elif args.all:
            # All repositories assignment
            report = assigner.generate_report()

            if args.json:
                print(json.dumps(report, indent=2))
            else:
                print(f"\nA/B Test: {report['testName']}")
                print(f"Start Date: {report['startDate']}")
                print("\nAssignment Summary:")
                control_count = report["assignments"]["control"]["count"]
                control_pct = report["assignments"]["control"]["percentage"]
                print(f"  Control Group: {control_count} repos ({control_pct}%)")
                exp_count = report["assignments"]["experiment"]["count"]
                exp_pct = report["assignments"]["experiment"]["percentage"]
                print(f"  Experiment Group: {exp_count} repos ({exp_pct}%)")
                print(
                    f"  Excluded: {report['assignments']['excluded']['count']} repos"  # noqa: E501
                )
                print(f"  Total Active: {report['totalActive']} repos")
                print(f"  Split Ratio: {report['splitRatio']}")

                print("\nControl Group Repositories:")
                for repo in report["assignments"]["control"]["repositories"][:10]:
                    print(f"  - {repo}")
                if len(report["assignments"]["control"]["repositories"]) > 10:
                    remaining = len(report["assignments"]["control"]["repositories"]) - 10
                    print(f"  ... and {remaining} more")

                print("\nExperiment Group Repositories:")
                for repo in report["assignments"]["experiment"]["repositories"][:10]:
                    print(f"  - {repo}")
                if len(report["assignments"]["experiment"]["repositories"]) > 10:
                    remaining = len(report["assignments"]["experiment"]["repositories"]) - 10
                    print(f"  ... and {remaining} more")

                if report["assignments"]["excluded"]["count"] > 0:
                    print("\nExcluded Repositories:")
                    for repo in report["assignments"]["excluded"]["repositories"]:
                        print(f"  - {repo}")
        else:
            # No arguments - show help
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
