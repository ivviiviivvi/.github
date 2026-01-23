#!/usr/bin/env python3
"""
Add existing issues and PRs to GitHub Projects.
Automatically categorizes and adds items based on labels and content.
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List

import requests

# Project mapping based on labels and keywords
PROJECT_MAPPINGS = {
    8: {  # AI Framework Development
        "labels": ["ai", "agent", "mcp", "copilot", "ai-framework"],
        "keywords": [
            "agent",
            "mcp server",
            "copilot",
            "ai framework",
            "prompt",
        ],
        "paths": ["ai_framework/", "agents/", "prompts/", "chatmodes/"],
    },
    9: {  # Documentation & Knowledge
        "labels": ["documentation", "docs"],
        "keywords": ["documentation", "guide", "tutorial", "readme"],
        "paths": ["docs/", "README"],
    },
    10: {  # Workflow Automation
        "labels": ["workflow", "automation", "ci/cd", "github-actions"],
        "keywords": ["workflow", "github actions", "automation", "ci/cd"],
        "paths": [".github/workflows/", "automation/"],
    },
    11: {  # Security & Compliance
        "labels": ["security", "vulnerability", "compliance"],
        "keywords": ["security", "vulnerability", "cve", "compliance"],
        "paths": [],
    },
    12: {  # Infrastructure & DevOps
        "labels": ["infrastructure", "devops", "deployment"],
        "keywords": [
            "infrastructure",
            "devops",
            "deployment",
            "terraform",
            "docker",
        ],
        "paths": [".devcontainer/", "infrastructure/"],
    },
    13: {  # Community & Support
        "labels": ["community", "support", "good first issue", "help wanted"],
        "keywords": ["community", "support", "help"],
        "paths": [],
    },
    14: {  # Product Roadmap
        "labels": ["roadmap", "feature", "enhancement"],
        "keywords": ["roadmap", "feature request", "enhancement"],
        "paths": [],
    },
}


class GitHubProjectManager:
    def __init__(self, token: str, org: str):
        self.token = token
        self.org = org
        self.api_url = "https://api.github.com/graphql"
        self.headers = {
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
        }

    def execute_query(self, query: str, variables: Dict = None) -> Dict:
        """Execute a GraphQL query."""
        response = requests.post(
            self.api_url,
            json={"query": query, "variables": variables or {}},
            headers=self.headers,
        )

        if response.status_code != 200:
            raise Exception(f"Query failed: {response.status_code} {response.text}")

        result = response.json()

        if "errors" in result:
            raise Exception(f"GraphQL errors: {json.dumps(result['errors'], indent=2)}")

        return result

    def get_project_id(self, project_number: int) -> str:
        """Get project ID by number."""
        query = """
        query($org: String!, $number: Int!) {
            organization(login: $org) {
                projectV2(number: $number) {
                    id
                    title
                }
            }
        }
        """

        result = self.execute_query(query, {"org": self.org, "number": project_number})
        return result["data"]["organization"]["projectV2"]["id"]

    def get_repository_issues(self, repo: str, state: str = "open") -> List[Dict]:
        """Get issues from a repository."""
        query = """
        query($org: String!, $repo: String!, $states: [IssueState!]) {
            repository(owner: $org, name: $repo) {
                issues(first: 100, states: $states) {
                    nodes {
                        id
                        number
                        title
                        labels(first: 10) {
                            nodes {
                                name
                            }
                        }
                        body
                    }
                }
            }
        }
        """

        states = [state.upper()]
        result = self.execute_query(
            query, {"org": self.org, "repo": repo, "states": states}
        )

        return result["data"]["repository"]["issues"]["nodes"]

    def get_repository_prs(self, repo: str, state: str = "open") -> List[Dict]:
        """Get pull requests from a repository."""
        query = """
        query($org: String!, $repo: String!, $states: [PullRequestState!]) {
            repository(owner: $org, name: $repo) {
                pullRequests(first: 100, states: $states) {
                    nodes {
                        id
                        number
                        title
                        labels(first: 10) {
                            nodes {
                                name
                            }
                        }
                        body
                        files(first: 10) {
                            nodes {
                                path
                            }
                        }
                    }
                }
            }
        }
        """

        states = [state.upper()]
        result = self.execute_query(
            query, {"org": self.org, "repo": repo, "states": states}
        )

        return result["data"]["repository"]["pullRequests"]["nodes"]

    def add_item_to_project(self, project_id: str, content_id: str) -> bool:
        """Add an item to a project."""
        mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
            addProjectV2ItemById(input: {
                projectId: $projectId
                contentId: $contentId
            }) {
                item {
                    id
                }
            }
        }
        """

        try:
            self.execute_query(
                mutation, {"projectId": project_id, "contentId": content_id}
            )
            return True
        except Exception as e:
            if "already exists" in str(e).lower():
                return False  # Already added
            print(f"  ✗ Error adding item: {e}")
            return False

    def categorize_item(self, item: Dict) -> List[int]:
        """Determine which projects an item should be added to."""
        projects = []

        # Get labels
        labels = [
            label["name"].lower() for label in item.get("labels", {}).get("nodes", [])
        ]

        # Get content for keyword matching
        title = item.get("title", "").lower()
        body = item.get("body", "").lower() if item.get("body") else ""
        content = f"{title} {body}"

        # Get file paths if available (for PRs)
        paths = []
        if "files" in item:
            paths = [f["path"] for f in item.get("files", {}).get("nodes", [])]

        # Check each project mapping
        for project_num, mapping in PROJECT_MAPPINGS.items():
            # Check labels
            if any(label in labels for label in mapping["labels"]):
                projects.append(project_num)
                continue

            # Check keywords
            if any(keyword in content for keyword in mapping["keywords"]):
                projects.append(project_num)
                continue

            # Check file paths
            if paths and any(
                any(path.startswith(prefix) for prefix in mapping["paths"])
                for path in paths
            ):
                projects.append(project_num)

        # Default to Product Roadmap if no match
        if not projects:
            projects.append(14)

        return projects


def main():
    parser = argparse.ArgumentParser(
        description="Add existing issues and PRs to GitHub Projects"
    )
    parser.add_argument("--org", required=True, help="GitHub organization")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument(
        "--state",
        default="open",
        choices=["open", "closed", "all"],
        help="State of issues/PRs to process",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--issues-only", action="store_true", help="Only process issues"
    )
    parser.add_argument(
        "--prs-only", action="store_true", help="Only process pull requests"
    )

    args = parser.parse_args()

    # Get token
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("✗ GH_TOKEN environment variable not set")
        sys.exit(1)

    manager = GitHubProjectManager(token, args.org)

    print(f"ℹ Adding items from {args.org}/{args.repo} to projects")
    if args.dry_run:
        print("⚠ DRY RUN MODE - No changes will be made")
    print()

    # Cache project IDs
    project_ids = {}
    print("ℹ Loading project IDs...")
    for project_num in PROJECT_MAPPINGS.keys():
        try:
            project_ids[project_num] = manager.get_project_id(project_num)
            print(f"  ✓ Project #{project_num}")
        except Exception as e:
            print(f"  ✗ Project #{project_num}: {e}")
    print()

    stats = {
        "issues_processed": 0,
        "prs_processed": 0,
        "items_added": 0,
        "items_skipped": 0,
    }

    # Process issues
    if not args.prs_only:
        print("ℹ Processing issues...")
        try:
            issues = manager.get_repository_issues(args.repo, args.state)
            print(f"  Found {len(issues)} issues")

            for issue in issues:
                stats["issues_processed"] += 1
                projects = manager.categorize_item(issue)

                print(f"\n  Issue #{issue['number']}: {issue['title'][:60]}")
                print(f"    → Projects: {', '.join(f'#{p}' for p in projects)}")

                if not args.dry_run:
                    for project_num in projects:
                        if project_num in project_ids:
                            added = manager.add_item_to_project(
                                project_ids[project_num], issue["id"]
                            )
                            if added:
                                stats["items_added"] += 1
                                print(f"    ✓ Added to project #{project_num}")
                            else:
                                stats["items_skipped"] += 1
                                print(f"    - Already in project #{project_num}")
                            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"  ✗ Error processing issues: {e}")

    # Process PRs
    if not args.issues_only:
        print("\nℹ Processing pull requests...")
        try:
            prs = manager.get_repository_prs(args.repo, args.state)
            print(f"  Found {len(prs)} pull requests")

            for pr in prs:
                stats["prs_processed"] += 1
                projects = manager.categorize_item(pr)

                print(f"\n  PR #{pr['number']}: {pr['title'][:60]}")
                print(f"    → Projects: {', '.join(f'#{p}' for p in projects)}")

                if not args.dry_run:
                    for project_num in projects:
                        if project_num in project_ids:
                            added = manager.add_item_to_project(
                                project_ids[project_num], pr["id"]
                            )
                            if added:
                                stats["items_added"] += 1
                                print(f"    ✓ Added to project #{project_num}")
                            else:
                                stats["items_skipped"] += 1
                                print(f"    - Already in project #{project_num}")
                            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"  ✗ Error processing PRs: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Issues processed:  {stats['issues_processed']}")
    print(f"  PRs processed:     {stats['prs_processed']}")
    print(f"  Items added:       {stats['items_added']}")
    print(f"  Items skipped:     {stats['items_skipped']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
