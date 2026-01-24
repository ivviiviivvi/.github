#!/usr/bin/env python3
"""
Update GitHub Action SHA pins to latest versions.

This script resolves version tags (e.g., v4) to their full commit SHAs
and updates workflow files while preserving ratchet comments.

Usage:
    python scripts/update-action-pins.py [--dry-run] [--verbose]

Requirements:
    - requests
    - PyYAML

Environment:
    - GITHUB_TOKEN: Optional, but recommended to avoid rate limits
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import requests
except ImportError:
    print("Error: requests package required. Install with: pip install requests")
    sys.exit(1)


class ActionRef(NamedTuple):
    """Represents a GitHub Action reference."""
    owner: str
    repo: str
    version: str  # Can be SHA, tag, or branch


# Canonical action versions to pin
# Format: "owner/repo" -> "version_tag"
CANONICAL_VERSIONS: dict[str, str] = {
    "actions/checkout": "v4",
    "actions/setup-python": "v5",
    "actions/setup-node": "v4",
    "actions/setup-go": "v5",
    "actions/cache": "v4",
    "actions/upload-artifact": "v4",
    "actions/download-artifact": "v4",
    "actions/github-script": "v7",
    "actions/configure-pages": "v5",
    "actions/deploy-pages": "v4",
    "actions/upload-pages-artifact": "v3",
    "actions/dependency-review-action": "v4",
    "actions/labeler": "v5",
    "actions/stale": "v9",
    "actions/first-interaction": "v1",
    "actions/create-github-app-token": "v2",
    "docker/setup-buildx-action": "v3",
    "docker/build-push-action": "v6",
    "docker/login-action": "v3",
    "docker/metadata-action": "v5",
    "docker/setup-qemu-action": "v3",
    "github/codeql-action": "v3",
    "github/combine-prs": "v5",
    "codecov/codecov-action": "v4",
    "peter-evans/create-pull-request": "v6",
    "stefanzweifel/git-auto-commit-action": "v5",
    "anthropics/claude-code-action": "v1",
    "slackapi/slack-github-action": "v1",
}


def get_github_token() -> str | None:
    """Get GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def resolve_tag_to_sha(owner: str, repo: str, tag: str, token: str | None = None) -> str | None:  # allow-secret
    """Resolve a Git tag to its commit SHA."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Try as a tag first
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/tags/{tag}"
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        # Handle both lightweight and annotated tags
        if data["object"]["type"] == "tag":
            # Annotated tag - need to resolve to commit
            tag_url = data["object"]["url"]
            tag_response = requests.get(tag_url, headers=headers, timeout=10)
            if tag_response.status_code == 200:
                return tag_response.json()["object"]["sha"]
        return data["object"]["sha"]

    # Try as a branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{tag}"
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()["object"]["sha"]

    return None


def parse_action_line(line: str) -> tuple[str, str, str] | None:
    """
    Parse a workflow line with an action reference.
    Returns (action, current_ref, ratchet_version) or None.
    """
    # Match: uses: owner/repo@ref  # ratchet:owner/repo@version
    match = re.search(
        r'uses:\s*([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)@([a-f0-9]{40}|v[\d.]+)\s*#\s*ratchet:([^\s]+)',
        line
    )
    if match:
        return match.group(1), match.group(2), match.group(3)

    # Match without ratchet comment
    match = re.search(
        r'uses:\s*([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)@([a-f0-9]{40}|v[\d.]+)',
        line
    )
    if match:
        return match.group(1), match.group(2), None

    return None


def update_workflow_file(
    filepath: Path,
    sha_cache: dict[str, str],
    dry_run: bool = False,
    verbose: bool = False
) -> int:
    """
    Update action pins in a workflow file.
    Returns number of lines updated.
    """
    content = filepath.read_text()
    lines = content.split('\n')
    updated_lines = []
    updates = 0

    for line in lines:
        parsed = parse_action_line(line)
        if not parsed:
            updated_lines.append(line)
            continue

        action, current_ref, ratchet = parsed
        owner, repo = action.split('/')

        # Get canonical version for this action
        canonical_version = CANONICAL_VERSIONS.get(action)
        if not canonical_version:
            updated_lines.append(line)
            continue

        # Get SHA for canonical version
        cache_key = f"{action}@{canonical_version}"
        if cache_key not in sha_cache:
            if verbose:
                print(f"  Resolving {cache_key}...")
            sha = resolve_tag_to_sha(owner, repo, canonical_version, get_github_token())
            if sha:
                sha_cache[cache_key] = sha
            else:
                print(f"  Warning: Could not resolve {cache_key}")
                updated_lines.append(line)
                continue

        new_sha = sha_cache[cache_key]

        # Check if update needed
        if current_ref == new_sha:
            updated_lines.append(line)
            continue

        # Build updated line
        indent = re.match(r'^(\s*)', line).group(1)
        if 'uses:' in line:
            # Preserve any leading dash for list items
            prefix_match = re.match(r'^(\s*-\s*)', line)
            if prefix_match:
                new_line = f"{prefix_match.group(1)}uses: {action}@{new_sha}  # ratchet:{action}@{canonical_version}"
            else:
                new_line = f"{indent}uses: {action}@{new_sha}  # ratchet:{action}@{canonical_version}"

            if verbose:
                print(f"  {action}: {current_ref[:12]}... -> {new_sha[:12]}...")

            updated_lines.append(new_line)
            updates += 1
        else:
            updated_lines.append(line)

    if updates > 0 and not dry_run:
        filepath.write_text('\n'.join(updated_lines))

    return updates


def main():
    parser = argparse.ArgumentParser(description="Update GitHub Action SHA pins")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated without making changes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--workflow", "-w", help="Update only a specific workflow file")
    args = parser.parse_args()

    # Find workflows directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    workflows_dir = repo_root / ".github" / "workflows"

    if not workflows_dir.exists():
        print(f"Error: Workflows directory not found: {workflows_dir}")
        sys.exit(1)

    # SHA resolution cache
    sha_cache: dict[str, str] = {}

    # Find workflow files
    if args.workflow:
        workflow_files = [workflows_dir / args.workflow]
        if not workflow_files[0].exists():
            print(f"Error: Workflow file not found: {workflow_files[0]}")
            sys.exit(1)
    else:
        workflow_files = list(workflows_dir.glob("*.yml"))

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Updating {len(workflow_files)} workflow files...")

    total_updates = 0
    files_updated = 0

    for workflow in sorted(workflow_files):
        updates = update_workflow_file(workflow, sha_cache, args.dry_run, args.verbose)
        if updates > 0:
            print(f"  {workflow.name}: {updates} action(s) updated")
            total_updates += updates
            files_updated += 1

    print(f"\nSummary: {total_updates} action(s) updated in {files_updated} file(s)")

    if args.dry_run and total_updates > 0:
        print("\nRun without --dry-run to apply changes")


if __name__ == "__main__":
    main()
