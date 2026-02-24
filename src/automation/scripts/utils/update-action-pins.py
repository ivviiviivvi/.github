#!/usr/bin/env python3
"""Update GitHub Action SHA pins to latest versions.

This script resolves version tags (e.g., v4) to their full commit SHAs
and updates workflow files while preserving ratchet comments.

Usage:
    python scripts/update-action-pins.py [--dry-run] [--verbose]

Requirements:
    - requests

Environment:
    - GITHUB_TOKEN: Optional, but recommended to avoid rate limits
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import NamedTuple

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Error: requests package required. Install with: pip install requests")
    sys.exit(1)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ActionRef(NamedTuple):
    """Represents a GitHub Action reference."""

    owner: str
    repo: str
    path: str  # Subpath for actions like codeql-action/init
    version: str  # Can be SHA, tag, or branch


# Canonical action versions to pin
# Format: "owner/repo" or "owner/repo/subpath" -> "version_tag"
CANONICAL_VERSIONS: dict[str, str] = {
    # Core GitHub Actions
    "actions/checkout": "v4",
    "actions/setup-python": "v5",
    "actions/setup-node": "v4",
    "actions/setup-go": "v5",
    "actions/setup-java": "v4",
    "actions/setup-dotnet": "v4",
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
    # Docker Actions
    "docker/setup-buildx-action": "v3",
    "docker/build-push-action": "v6",
    "docker/login-action": "v3",
    "docker/metadata-action": "v5",
    "docker/setup-qemu-action": "v3",
    # GitHub CodeQL Actions (with subpaths)
    "github/codeql-action": "v3",
    "github/codeql-action/init": "v3",
    "github/codeql-action/autobuild": "v3",
    "github/codeql-action/analyze": "v3",
    "github/codeql-action/upload-sarif": "v3",
    "github/combine-prs": "v5",
    "github/issue-metrics": "v3",
    "github/issue-parser": "v3",
    # Third-party Actions
    "1password/install-cli-action": "v1",
    "8398a7/action-slack": "v3",
    "amannn/action-semantic-pull-request": "v5",
    "anchore/sbom-action": "v0",
    "anthropics/claude-code-action": "v1",
    "aquasecurity/trivy-action": "v0",
    "benchmark-action/github-action-benchmark": "v1",
    "codecov/codecov-action": "v4",
    "codelytv/pr-size-labeler": "v1",
    "dawidd6/action-send-mail": "v3",
    "dessant/lock-threads": "v5",
    "dorny/test-reporter": "v1",
    "gaurav-nelson/github-action-markdown-link-check": "v1",
    "google-github-actions/run-gemini-cli": "v0",
    "goreleaser/goreleaser-action": "v5",
    "grafana/k6-action": "v0",
    "lycheeverse/lychee-action": "v1",
    "metcalfc/changelog-generator": "v4",
    "peter-evans/create-pull-request": "v6",
    "py-cov-action/python-coverage-comment-action": "v3",
    "returntocorp/semgrep-action": "v1",
    "rhysd/changelog-from-release": "v3",
    "ruby/setup-ruby": "v1",
    "slackapi/slack-github-action": "v1",
    "softprops/action-gh-release": "v1",
    "stefanzweifel/git-auto-commit-action": "v5",
    "tj-actions/changed-files": "v41",
    "treosh/lighthouse-ci-action": "v11",
}


def create_session_with_retries() -> requests.Session:
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=1,  # 1s, 2s, 4s between retries
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_github_token() -> str | None:
    """Get GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def resolve_tag_to_sha(
    owner: str,
    repo: str,
    tag: str,
    session: requests.Session,
    token: str | None = None,  # allow-secret
) -> str | None:
    """Resolve a Git tag to its commit SHA with retry logic."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Try as a tag first
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/tags/{tag}"

    try:
        response = session.get(url, headers=headers, timeout=30)

        # Handle rate limiting
        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining", "unknown")
            reset_time = response.headers.get("X-RateLimit-Reset", "unknown")
            logger.warning(f"Rate limited. Remaining: {remaining}, Reset: {reset_time}")
            if remaining == "0" and reset_time != "unknown":
                wait_time = int(reset_time) - int(time.time()) + 5
                if wait_time > 0 and wait_time < 300:  # Max 5 min wait
                    logger.info(f"Waiting {wait_time}s for rate limit reset...")
                    time.sleep(wait_time)
                    response = session.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Handle list response (multiple matching refs when tag is a prefix)
            if isinstance(data, list):
                if not data:
                    return None
                data = data[0]  # Use first (exact) match

            # Handle both lightweight and annotated tags
            if data["object"]["type"] == "tag":
                # Annotated tag - need to resolve to commit
                tag_url = data["object"]["url"]
                tag_response = session.get(tag_url, headers=headers, timeout=30)
                if tag_response.status_code == 200:
                    return tag_response.json()["object"]["sha"]
            return data["object"]["sha"]

        # Try as a branch
        url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{tag}"
        response = session.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Handle list response (multiple matching refs)
            if isinstance(data, list):
                if not data:
                    return None
                data = data[0]

            return data["object"]["sha"]

        logger.debug(f"Could not resolve {owner}/{repo}@{tag}: HTTP {response.status_code}")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error resolving {owner}/{repo}@{tag}: {e}")
        return None


def parse_action_line(line: str) -> tuple[str, str, str | None] | None:
    """Parse a workflow line with an action reference.
    Returns (action, current_ref, ratchet_version) or None.

    Handles both simple actions (owner/repo) and subpath actions (owner/repo/path).
    """
    # Match: uses: owner/repo[/subpath]@ref  # ratchet:owner/repo[/subpath]@version
    match = re.search(
        r"uses:\s*([a-zA-Z0-9_-]+/[a-zA-Z0-9_/-]+)@([a-f0-9]{40}|v[\d.]+)\s*#\s*ratchet:([^\s]+)",
        line,
    )
    if match:
        return match.group(1), match.group(2), match.group(3)

    # Match without ratchet comment
    match = re.search(r"uses:\s*([a-zA-Z0-9_-]+/[a-zA-Z0-9_/-]+)@([a-f0-9]{40}|v[\d.]+)", line)
    if match:
        return match.group(1), match.group(2), None

    return None


def get_base_action(action: str) -> tuple[str, str]:
    """Extract the base owner/repo from an action path.
    For 'github/codeql-action/init' returns ('github', 'codeql-action').
    """
    parts = action.split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return action, ""


def update_workflow_file(
    filepath: Path,
    sha_cache: dict[str, str],
    session: requests.Session,
    dry_run: bool = False,
    verbose: bool = False,
) -> int:
    """Update action pins in a workflow file.
    Returns number of lines updated.
    """
    try:
        content = filepath.read_text()
    except Exception as e:
        logger.error(f"Failed to read {filepath}: {e}")
        return 0

    lines = content.split("\n")
    updated_lines = []
    updates = 0

    for line in lines:
        parsed = parse_action_line(line)
        if not parsed:
            updated_lines.append(line)
            continue

        action, current_ref, ratchet = parsed
        owner, repo = get_base_action(action)

        # Get canonical version for this action (try full path first, then base)
        canonical_version = CANONICAL_VERSIONS.get(action)
        if not canonical_version:
            base_action = f"{owner}/{repo}"
            canonical_version = CANONICAL_VERSIONS.get(base_action)

        if not canonical_version:
            if verbose:
                logger.debug(f"No canonical version for {action}")
            updated_lines.append(line)
            continue

        # Get SHA for canonical version
        cache_key = f"{owner}/{repo}@{canonical_version}"
        if cache_key not in sha_cache:
            if verbose:
                logger.info(f"  Resolving {cache_key}...")
            sha = resolve_tag_to_sha(owner, repo, canonical_version, session, get_github_token())
            if sha:
                sha_cache[cache_key] = sha
            else:
                logger.warning(f"  Could not resolve {cache_key}")
                updated_lines.append(line)
                continue

        new_sha = sha_cache[cache_key]

        # Check if update needed
        if current_ref == new_sha:
            updated_lines.append(line)
            continue

        # Build updated line
        if "uses:" in line:
            # Preserve any leading dash for list items
            prefix_match = re.match(r"^(\s*-\s*)", line)
            if prefix_match:
                new_line = f"{prefix_match.group(1)}uses: {action}@{new_sha}  # ratchet:{action}@{canonical_version}"
            else:
                indent_match = re.match(r"^(\s*)", line)
                indent = indent_match.group(1) if indent_match else ""
                new_line = f"{indent}uses: {action}@{new_sha}  # ratchet:{action}@{canonical_version}"

            if verbose:
                logger.info(f"  {action}: {current_ref[:12]}... -> {new_sha[:12]}...")

            updated_lines.append(new_line)
            updates += 1
        else:
            updated_lines.append(line)

    if updates > 0 and not dry_run:
        try:
            filepath.write_text("\n".join(updated_lines))
        except Exception as e:
            logger.error(f"Failed to write {filepath}: {e}")
            return 0

    return updates


def main() -> None:
    """Main entry point for updating action pins."""
    parser = argparse.ArgumentParser(description="Update GitHub Action SHA pins to latest versions")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--workflow", "-w", help="Update only a specific workflow file")
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Search for workflows in subdirectories",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Find workflows directory by searching upward from script location
    script_dir = Path(__file__).parent.resolve()
    workflows_dir = None

    # Search upward for .github/workflows directory
    current = script_dir
    for _ in range(10):  # Limit search depth
        candidate = current / ".github" / "workflows"
        if candidate.exists():
            workflows_dir = candidate
            break
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent

    if not workflows_dir or not workflows_dir.exists():
        logger.error(f"Workflows directory not found searching from: {script_dir}")
        sys.exit(1)

    # Create session with retry logic
    session = create_session_with_retries()

    # SHA resolution cache
    sha_cache: dict[str, str] = {}

    # Find workflow files
    if args.workflow:
        workflow_files = [workflows_dir / args.workflow]
        if not workflow_files[0].exists():
            logger.error(f"Workflow file not found: {workflow_files[0]}")
            sys.exit(1)
    elif args.recursive:
        workflow_files = list(workflows_dir.glob("**/*.yml"))
    else:
        workflow_files = list(workflows_dir.glob("*.yml"))

    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}Scanning {len(workflow_files)} workflow file(s)...")
    print(f"Configured with {len(CANONICAL_VERSIONS)} canonical action versions")

    total_updates = 0
    files_updated = 0
    errors = 0

    for workflow in sorted(workflow_files):
        try:
            updates = update_workflow_file(workflow, sha_cache, session, args.dry_run, args.verbose)
            if updates > 0:
                print(f"  {workflow.relative_to(workflows_dir.parent.parent)}: {updates} action(s) updated")
                total_updates += updates
                files_updated += 1
        except Exception as e:
            logger.error(f"Error processing {workflow}: {e}")
            errors += 1

    print(f"\nSummary: {total_updates} action(s) updated in {files_updated} file(s)")
    if errors > 0:
        print(f"Errors: {errors} file(s) could not be processed")

    if args.dry_run and total_updates > 0:
        print("\nRun without --dry-run to apply changes")

    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
