#!/usr/bin/env python3
"""Validate that required labels exist in target repositories before deployment.

This script checks if all required labels (from a config file) exist in the
specified repositories, providing a pre-flight check before workflow deployment.  # noqa: E501

Usage:
    python3 validate_labels.py --config batch-onboard-week11-phase1-pilot.yml
    python3 validate_labels.py --config batch-onboard-week11-phase1-pilot.yml --fix  # noqa: E501
"""

import argparse
import json
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any, Optional, cast

import yaml
from secret_manager import ensure_github_token


class LabelValidator:
    """Validates label existence in GitHub repositories."""

    def __init__(self, config_path: Path, fix_mode: bool = False):
        """Initialize the validator.

        Args:
            config_path: Path to the configuration YAML file
            fix_mode: If True, create missing labels instead of just reporting

        """
        self.config_path = config_path
        self.fix_mode = fix_mode
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load and parse the configuration file."""
        try:
            with open(self.config_path) as f:
                config = yaml.safe_load(f)

            # Convert dict format labels to list format
            if isinstance(config.get("labels"), dict):
                labels_dict = config["labels"]
                config["labels"] = [
                    {
                        "name": name,
                        "color": props.get("color", ""),
                        "description": props.get("description", ""),
                    }
                    for name, props in labels_dict.items()
                ]

            return cast(dict[Any, Any], config)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            sys.exit(1)

    def _get_repo_labels(self, repo: str) -> Optional[list[dict]]:
        """Fetch existing labels from a repository.

        Args:
            repo: Repository in format "owner/repo"

        Returns:
            List of label dictionaries or None on error

        """
        try:
            result = subprocess.run(  # nosec B603 B607
                [
                    "gh",
                    "label",
                    "list",
                    "--repo",
                    repo,
                    "--json",
                    "name,color,description",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return cast(list[dict[Any, Any]], json.loads(result.stdout))
        except subprocess.CalledProcessError as e:
            print(f"❌ Error fetching labels from {repo}: {e.stderr}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing label data from {repo}: {e}")
            return None

    def _create_label(self, repo: str, label: dict) -> bool:
        """Create a label in a repository.

        Args:
            repo: Repository in format "owner/repo"
            label: Label dictionary with name, color, and description

        Returns:
            True if successful, False otherwise

        """
        try:
            cmd = [
                "gh",
                "label",
                "create",
                label["name"],
                "--repo",
                repo,
                "--color",
                label["color"],
                "--description",
                label.get("description", ""),
                "--force",  # Update if exists
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True)  # nosec B603
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating label {label['name']} in {repo}: {e.stderr}")
            return False

    def _normalize_color(self, color: str) -> str:
        """Remove # prefix from color if present."""
        return color.lstrip("#").lower()

    def _labels_match(self, existing: dict, required: dict) -> bool:
        """Check if an existing label matches the required specification.

        Args:
            existing: Existing label from repository
            required: Required label from config

        Returns:
            True if labels match (name and color)

        """
        return existing["name"] == required["name"] and self._normalize_color(
            existing["color"]
        ) == self._normalize_color(required["color"])

    def validate_repository(self, repo: str) -> tuple[bool, list[dict], list[dict]]:
        """Validate labels for a single repository.

        Args:
            repo: Repository in format "owner/repo"

        Returns:
            Tuple of (success, missing_labels, mismatched_labels)

        """
        print(f"\n🔍 Validating {repo}...")

        # Fetch existing labels
        existing_labels = self._get_repo_labels(repo)
        if existing_labels is None:
            return False, [], []

        # Check each required label
        required_labels = self.config.get("labels", [])
        missing_labels = []
        mismatched_labels = []

        for required in required_labels:
            # Find matching label by name
            existing = next(
                (label for label in existing_labels if label["name"] == required["name"]),
                None,
            )

            if existing is None:
                missing_labels.append(required)
                print(f"  ❌ Missing: {required['name']}")
            elif not self._labels_match(existing, required):
                mismatched_labels.append(required)
                print(f"  ⚠️  Mismatch: {required['name']} (expected #{required['color']}, found #{existing['color']})")  # noqa: E501
            else:
                print(f"  ✅ Found: {required['name']}")

        # Summary for this repository
        if not missing_labels and not mismatched_labels:
            print(f"✅ All {len(required_labels)} labels validated for {repo}")
            return True, [], []
        else:
            total_issues = len(missing_labels) + len(mismatched_labels)
            print(f"❌ {total_issues} label issues found in {repo}")
            return False, missing_labels, mismatched_labels

    def fix_repository(self, repo: str, missing: list[dict], mismatched: list[dict]) -> bool:
        """Fix label issues in a repository by creating/updating labels.

        Args:
            repo: Repository in format "owner/repo"
            missing: List of missing label specifications
            mismatched: List of mismatched label specifications

        Returns:
            True if all fixes successful, False otherwise

        """
        if not missing and not mismatched:
            return True

        print(f"\n🔧 Fixing labels in {repo}...")
        all_success = True

        # Create missing labels
        for label in missing:
            if self._create_label(repo, label):
                print(f"  ✅ Created: {label['name']}")
            else:
                print(f"  ❌ Failed to create: {label['name']}")
                all_success = False

        # Update mismatched labels
        for label in mismatched:
            if self._create_label(repo, label):
                print(f"  ✅ Updated: {label['name']}")
            else:
                print(f"  ❌ Failed to update: {label['name']}")
                all_success = False

        return all_success

    def validate_all(self) -> bool:
        """Validate labels across all repositories in the configuration.

        Returns:
            True if all validations pass, False otherwise

        """
        repositories = self.config.get("repositories", [])
        if not repositories:
            print("❌ No repositories found in configuration")
            return False

        required_labels = self.config.get("labels", [])
        if not required_labels:
            print("❌ No labels found in configuration")
            return False

        print(
            f"📋 Validating {len(required_labels)} labels across {len(repositories)} repositories"  # noqa: E501
        )
        print(
            f"{'🔧 FIX MODE ENABLED' if self.fix_mode else '👀 VALIDATION MODE'}\n"  # noqa: E501
        )

        all_success = True
        results = {}

        for repo in repositories:
            success, missing, mismatched = self.validate_repository(repo)

            if self.fix_mode and (missing or mismatched):
                fix_success = self.fix_repository(repo, missing, mismatched)
                success = success or fix_success

            results[repo] = {
                "success": success,
                "missing_count": len(missing),
                "mismatched_count": len(mismatched),
            }

            if not success:
                all_success = False

        # Final summary
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)

        for repo, result in results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            issues = result["missing_count"] + result["mismatched_count"]
            print(f"{status} {repo:50} ({issues} issues)")

        print("=" * 80)

        if all_success:
            print("✅ All repositories validated successfully!")
            return True
        else:
            failed_count = sum(1 for r in results.values() if not r["success"])
            print(
                f"❌ {failed_count}/{len(repositories)} repositories have label issues"  # noqa: E501
            )
            if not self.fix_mode:
                print(
                    "\n💡 Tip: Run with --fix to automatically create/update labels"  # noqa: E501
                )
            return False


def main():
    """Main entry point."""
    # Ensure GitHub token is available (from 1Password or env)
    _ = ensure_github_token("org-label-sync-token")  # noqa: F841

    parser = argparse.ArgumentParser(description="Validate labels in repositories before workflow deployment")  # noqa: E501
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to configuration YAML file",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Create/update missing or mismatched labels instead of just reporting",  # noqa: E501
    )

    args = parser.parse_args()

    # Ensure config file exists
    if not args.config.exists():
        print(f"❌ Config file not found: {args.config}")
        sys.exit(1)

    # Run validation
    validator = LabelValidator(args.config, fix_mode=args.fix)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
