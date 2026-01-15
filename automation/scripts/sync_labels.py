#!/usr/bin/env python3
"""
GitHub Label Sync Script

Synchronizes standardized labels across all repositories in a GitHub organization
using the PyGithub library.

Usage:
    python sync_labels.py --org ORGANIZATION_NAME [--token TOKEN] [--dry-run]

Environment Variables:
    GITHUB_TOKEN: GitHub personal access token with repo scope

Requirements:
    pip install PyGithub
"""

import argparse
import os
import sys
from typing import Dict, List, Optional

try:
    from github import Github, GithubException
    from github.Label import Label
    from github.Repository import Repository
except ImportError:
    print("Error: PyGithub is not installed.")
    print("Install it with: pip install PyGithub")
    sys.exit(1)


# Label definitions with colors and descriptions
# These match the labels already created in ivviiviivvi/.github
LABEL_DEFINITIONS = {
    # Priority Labels
    "priority: critical": {
        "color": "d73a4a",  # Red
        "description": "Critical priority",
    },
    "priority: high": {
        "color": "ff6b6b",  # Light red/pink
        "description": "High priority",
    },
    "priority: medium": {"color": "ffa500", "description": "Medium priority"},  # Orange
    "priority: low": {"color": "0e8a16", "description": "Low priority"},  # Green
    # Type Labels (without prefix)
    "bug": {"color": "d73a4a", "description": "Something isn't working"},  # Red
    "enhancement": {
        "color": "a2eeef",  # Light blue
        "description": "New feature or request",
    },
    "documentation": {
        "color": "0075ca",  # Blue
        "description": "Improvements or additions to documentation",
    },
    "security": {"color": "d93f0b", "description": "Security related"},  # Orange-red
    "task": {"color": "d4c5f9", "description": "General task or work item"},  # Purple
    "question": {
        "color": "d876e3",  # Pink
        "description": "Further information is requested",
    },
    # Status Labels (without prefix)
    "triage": {"color": "fbca04", "description": "Needs triage"},  # Yellow
    "in-progress": {"color": "0052cc", "description": "Work in progress"},  # Blue
    "blocked": {"color": "b60205", "description": "Blocked by dependency"},  # Red
    "needs-review": {"color": "6f42c1", "description": "Ready for review"},  # Purple
    "approved": {
        "color": "0e8a16",  # Green
        "description": "Approved and ready to merge",
    },
    # Category Labels
    "category: github-actions": {
        "color": "2088ff",  # GitHub Actions blue
        "description": "Related to GitHub Actions workflows",
    },
    "category: configuration": {
        "color": "e99695",  # Light red
        "description": "Configuration files or settings",
    },
    "category: dependencies": {
        "color": "0366d6",  # Blue
        "description": "Dependency updates or issues",
    },
    "category: automated": {
        "color": "bfd4f2",  # Light blue
        "description": "Automated processes or bots",
    },
    # Additional useful labels
    "good first issue": {
        "color": "7057ff",  # Purple
        "description": "Good for newcomers",
    },
    "help wanted": {
        "color": "008672",  # Teal
        "description": "Extra attention is needed",
    },
    "wontfix": {
        "color": "ffffff",  # White
        "description": "This will not be worked on",
    },
    "duplicate": {
        "color": "cfd3d7",  # Gray
        "description": "This issue or pull request already exists",
    },
    "invalid": {"color": "e4e669", "description": "This doesn't seem right"},  # Yellow
}


class LabelSyncManager:
    """Manages label synchronization across GitHub repositories."""

    def __init__(self, github_token: str, dry_run: bool = False):
        """
        Initialize the label sync manager.

        Args:
            github_token: GitHub personal access token
            dry_run: If True, only show what would be done without making changes
        """
        self.github = Github(github_token)
        self.dry_run = dry_run

    def get_repositories(self, org_name: str) -> List[Repository]:
        """
        Get all repositories for an organization.

        Args:
            org_name: GitHub organization name

        Returns:
            List of Repository objects
        """
        try:
            org = self.github.get_organization(org_name)
            repos = list(org.get_repos())
            print(f"Found {len(repos)} repositories in organization '{org_name}'")
            return repos
        except GithubException as e:
            print(f"Error accessing organization '{org_name}': {e}")
            sys.exit(1)

    def get_existing_labels(self, repo: Repository) -> Dict[str, Label]:
        """
        Get existing labels from a repository.

        Args:
            repo: Repository object

        Returns:
            Dictionary mapping label names to Label objects
        """
        try:
            labels = {label.name: label for label in repo.get_labels()}
            return labels
        except GithubException as e:
            print(f"  ⚠️  Error getting labels from {repo.name}: {e}")
            return {}

    def sync_labels(self, repo: Repository) -> Dict[str, int]:
        """
        Sync labels for a single repository.

        Args:
            repo: Repository object

        Returns:
            Dictionary with sync statistics
        """
        stats = {"created": 0, "updated": 0, "unchanged": 0, "errors": 0}

        existing_labels = self.get_existing_labels(repo)

        for label_name, label_config in LABEL_DEFINITIONS.items():
            try:
                if label_name in existing_labels:
                    # Label exists - check if update needed
                    existing_label = existing_labels[label_name]
                    needs_update = (
                        existing_label.color.lower() != label_config["color"].lower()
                        or (existing_label.description or "").strip()
                        != (label_config["description"] or "").strip()
                    )

                    if needs_update:
                        if self.dry_run:
                            print(f"  Would update: {label_name}")
                            stats["updated"] += 1
                        else:
                            existing_label.edit(
                                name=label_name,
                                color=label_config["color"],
                                description=label_config["description"],
                            )
                            print(f"  ✓ Updated: {label_name}")
                            stats["updated"] += 1
                    else:
                        stats["unchanged"] += 1
                else:
                    # Label doesn't exist - create it
                    if self.dry_run:
                        print(f"  Would create: {label_name}")
                        stats["created"] += 1
                    else:
                        repo.create_label(
                            name=label_name,
                            color=label_config["color"],
                            description=label_config["description"],
                        )
                        print(f"  ✓ Created: {label_name}")
                        stats["created"] += 1

            except GithubException as e:
                print(f"  ✗ Error with label '{label_name}': {e}")
                stats["errors"] += 1

        return stats

    def sync_organization(
        self, org_name: str, exclude_repos: Optional[List[str]] = None
    ) -> None:
        """
        Sync labels across all repositories in an organization.

        Args:
            org_name: GitHub organization name
            exclude_repos: List of repository names to exclude
        """
        exclude_repos = exclude_repos or []

        if self.dry_run:
            print("\n🔍 DRY RUN MODE - No changes will be made\n")

        repos = self.get_repositories(org_name)

        total_stats = {
            "repos_processed": 0,
            "repos_skipped": 0,
            "created": 0,
            "updated": 0,
            "unchanged": 0,
            "errors": 0,
        }

        for repo in repos:
            if repo.name in exclude_repos:
                print(f"\n⏭️  Skipping {repo.name} (excluded)")
                total_stats["repos_skipped"] += 1
                continue

            if repo.archived:
                print(f"\n⏭️  Skipping {repo.name} (archived)")
                total_stats["repos_skipped"] += 1
                continue

            print(f"\n📦 Processing {repo.name}...")

            try:
                stats = self.sync_labels(repo)
                total_stats["repos_processed"] += 1
                total_stats["created"] += stats["created"]
                total_stats["updated"] += stats["updated"]
                total_stats["unchanged"] += stats["unchanged"]
                total_stats["errors"] += stats["errors"]

                if (
                    stats["created"] == 0
                    and stats["updated"] == 0
                    and stats["errors"] == 0
                ):
                    print(f"  ✓ All labels up to date")

            except Exception as e:
                print(f"  ✗ Error processing repository: {e}")
                total_stats["errors"] += 1

        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Repositories processed: {total_stats['repos_processed']}")
        print(f"Repositories skipped:   {total_stats['repos_skipped']}")
        print(f"Labels created:         {total_stats['created']}")
        print(f"Labels updated:         {total_stats['updated']}")
        print(f"Labels unchanged:       {total_stats['unchanged']}")
        print(f"Errors:                 {total_stats['errors']}")
        print("=" * 60)

        if self.dry_run:
            print("\n💡 Run without --dry-run to apply these changes")


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Sync GitHub labels across repositories in an organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (show what would be done)
  python sync_labels.py --org myorg --dry-run

  # Actually sync labels
  python sync_labels.py --org myorg --token ghp_xxxxx

  # Use token from environment variable
  export GITHUB_TOKEN=ghp_xxxxx
  python sync_labels.py --org myorg

  # Exclude specific repositories
  python sync_labels.py --org myorg --exclude repo1 repo2
        """,
    )

    parser.add_argument("--org", required=True, help="GitHub organization name")

    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub personal access token (or set GITHUB_TOKEN env var)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    parser.add_argument(
        "--exclude", nargs="+", default=[], help="Repository names to exclude from sync"
    )

    parser.add_argument(
        "--list-labels", action="store_true", help="List all label definitions and exit"
    )

    args = parser.parse_args()

    # List labels if requested
    if args.list_labels:
        print("Label Definitions:")
        print("=" * 60)
        for name, config in LABEL_DEFINITIONS.items():
            print(f"\n{name}")
            print(f"  Color: #{config['color']}")
            print(f"  Description: {config['description']}")
        sys.exit(0)

    # Validate token
    if not args.token:
        print("Error: GitHub token is required.")
        print("Provide it with --token or set the GITHUB_TOKEN environment variable.")
        sys.exit(1)

    # Run sync
    try:
        manager = LabelSyncManager(args.token, dry_run=args.dry_run)
        manager.sync_organization(args.org, exclude_repos=args.exclude)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
