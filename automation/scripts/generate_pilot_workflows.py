#!/usr/bin/env python3
"""
Generate Customized Workflow Files for Pilot Repository

Takes pilot-repo-config.yml and generates customized workflow files.

Usage:
    python3 generate_pilot_workflows.py pilot-repo-config.yml
"""

import sys
from pathlib import Path
from typing import Optional

import yaml


class WorkflowGenerator:
    """Generates customized workflow files for pilot repositories."""

    def __init__(self, config_path: str):
        """Initialize generator with configuration file."""
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.repo = self.config["repository"]
        self.workflows = self.config["workflows"]
        self.customization = self.config["customization"]

    def generate_issue_triage(self) -> Optional[str]:
        """Generate issue-triage.yml with customizations."""
        config = self.workflows["issueTriage"]
        if not config["enabled"]:
            return None

        # Build label rules
        label_rules = []
        for rule in config["labelRules"]:
            pattern = rule["pattern"]
            conditions = rule["conditions"]

            # Convert to workflow conditions
            title_conditions = " || ".join(
                [
                    f"contains(github.event.issue.title, '{term}')"
                    for term in conditions[0].get("titleContains", [])
                ]
            )

            body_conditions = " || ".join(
                [
                    f"contains(github.event.issue.body, '{term}')"
                    for term in conditions[1].get("bodyContains", [])
                    if len(conditions) > 1
                ]
            )

            if title_conditions and body_conditions:
                condition = f"({title_conditions}) || ({body_conditions})"
            elif title_conditions:
                condition = title_conditions
            else:
                condition = body_conditions

            label_rules.append({"label": pattern, "condition": condition})

        workflow = """name: Issue Triage

on:
  issues:
    types: [opened, reopened]

permissions:
  issues: write
  contents: read

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Auto-label issue
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const labels = [];

"""

        # Add label logic
        for rule in label_rules:
            workflow += """
            // Check for {rule['label']} label
            if ({rule['condition']}) {{
              labels.push('{rule['label']}');
            }}
"""

        workflow += """
            // Add needs-triage label
            labels.push('needs-triage');

            // Apply labels
            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                labels: labels
              });
            }
"""

        # Add auto-assign if enabled
        if config["autoAssign"]["enabled"]:
            config["autoAssign"]["teams"]
            workflow += """
      - name: Auto-assign to team
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.addAssignees({{
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.issue.number,
              assignees: [{', '.join([f"'{t}'" for t in teams])}]
            }});
"""

        # Add Slack notification
        workflow += """
      - name: Notify Slack on Failure
        if: failure()
        uses: ./.github/actions/slack-notify
        with:
          webhook-url: ${{{{ secrets.SLACK_WEBHOOK_ALERTS }}}}
          priority: {config['priority']}
          title: "Issue Triage Failed - {self.repo['name']}"
          message: >
            The issue triage workflow failed in pilot repository
            {self.repo['name']}.
          workflow: issue-triage
          status: failure
          details-url: >
            ${{{{ github.server_url }}}}/
            ${{{{ github.repository }}}}/actions/runs/${{{{ github.run_id }}}}
"""

        return workflow

    def generate_auto_assign_reviewers(self) -> Optional[str]:
        """Generate auto-assign-reviewers.yml with customizations."""
        config = self.workflows["autoAssignReviewers"]
        if not config["enabled"]:
            return None

        workflow = """name: Auto-Assign Reviewers

on:
  pull_request:
    types: [opened, ready_for_review]

permissions:
  pull-requests: write
  contents: read

jobs:
  assign-reviewers:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Assign reviewers based on paths
        uses: actions/github-script@v7
        with:
          script: |
            const {{ data: files }} = await github.rest.pulls.listFiles({{
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.payload.pull_request.number
            }});

            const changedPaths = files.map(f => f.filename);
            const reviewers = new Set();

"""

        # Add path-based rules
        for rule in config["rules"]:
            rule["paths"]
            rule["reviewers"]
            rule["count"]

            workflow += """
            // Check paths: {', '.join(paths)}
            if (changedPaths.some(p => {
                ' || '.join([f"p.startsWith('{path}')" for path in paths])
            })) {{
              {'; '.join([f"reviewers.add('{r}')"
                         for r in rule_reviewers[:count]])};
            }}
"""

        workflow += """
            // Request reviews
            if (reviewers.size > 0) {
              await github.rest.pulls.requestReviewers({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: context.payload.pull_request.number,
                reviewers: Array.from(reviewers)
              });
            }
"""

        # Add Slack notification
        workflow += """
      - name: Notify Slack on Failure
        if: failure()
        uses: ./.github/actions/slack-notify
        with:
          webhook-url: ${{{{ secrets.SLACK_WEBHOOK_ALERTS }}}}
          priority: {config['priority']}
          title: "Auto-Assign Reviewers Failed - {self.repo['name']}"
          message: >
            The reviewer assignment workflow failed in pilot repository
            {self.repo['name']}.
          workflow: auto-assign-reviewers
          status: failure
          details-url: >
            ${{{{ github.server_url }}}}/
            ${{{{ github.repository }}}}/actions/runs/${{{{ github.run_id }}}}
"""

        return workflow

    def generate_stale_management(self) -> Optional[str]:
        """Generate stale-management.yml with customizations."""
        config = self.workflows["staleManagement"]
        if not config["enabled"]:
            return None

        self.customization["stale"]

        workflow = """name: Stale Management

on:
  schedule:
    - cron: '{config['schedule']}'
  workflow_dispatch:

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - name: Mark stale issues and PRs
        uses: actions/stale@v9
        with:
          repo-token: ${{{{ secrets.GITHUB_TOKEN }}}}
          days-before-stale: {stale_config['daysUntilStale']}
          days-before-close: {stale_config['daysUntilClose']}
          stale-issue-label: '{stale_config['staleIssueLabel']}'
          stale-pr-label: '{stale_config['stalePRLabel']}'
          exempt-issue-labels: '{','.join(stale_config['exemptLabels'])}'
          exempt-pr-labels: '{','.join(stale_config['exemptLabels'])}'
          stale-issue-message: |
            {stale_config['staleIssueMessage']}
          stale-pr-message: |
            {stale_config['stalePRMessage']}

      - name: Notify Slack on Failure
        if: failure()
        uses: ./.github/actions/slack-notify
        with:
          webhook-url: ${{{{ secrets.SLACK_WEBHOOK_ALERTS }}}}
          priority: {config['priority']}
          title: "Stale Management Failed - {self.repo['name']}"
          message: >
            The stale management workflow failed in pilot repository
            {self.repo['name']}.
          workflow: stale-management
          status: failure
          details-url: >
            ${{{{ github.server_url }}}}/
            ${{{{ github.repository }}}}/actions/runs/${{{{ github.run_id }}}}
"""

        return workflow

    def generate_all(self, output_dir: str = "./generated_workflows"):
        """Generate all workflow files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        workflows = {
            "issue-triage.yml": self.generate_issue_triage(),
            "auto-assign-reviewers.yml": self.generate_auto_assign_reviewers(),
            "stale-management.yml": self.generate_stale_management(),
        }

        for filename, content in workflows.items():
            if content:
                file_path = output_path / filename
                with open(file_path, "w") as f:
                    f.write(content)
                print(f"✅ Generated: {file_path}")
            else:
                print(f"⏭️  Skipped: {filename} (disabled in config)")

        print(f"\n📁 Workflows generated in: {output_path.absolute()}")
        print("\n📝 Next steps:")
        print(f"1. Review generated workflows in {output_path}")
        print(
            f"2. Copy to {self.repo['owner']}/{self.repo['name']}/.github/workflows/"  # noqa: E501
        )
        print("3. Test in passive mode (dry-run)")
        print("4. Activate gradually per deployment plan")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 generate_pilot_workflows.py <config.yml>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not Path(config_path).exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    generator = WorkflowGenerator(config_path)
    generator.generate_all()


if __name__ == "__main__":
    main()
