# Organization Labels Standard

This document defines the standard set of labels to be used across all repositories in the organization. These labels are defined in `.github/labels.yml` and can be synchronized across repositories using the label-sync workflow.

## Priority Labels

These labels indicate the urgency or importance:

- **priority: critical** 🚨
  - Color: `#d73a4a`
  - Description: Critical priority - immediate attention required

- **priority: high** ⬆️
  - Color: `#ff6b6b`
  - Description: High priority - should be addressed soon

- **priority: medium** ➡️
  - Color: `#ffa500`
  - Description: Medium priority - normal queue

- **priority: low** ⬇️
  - Color: `#0e8a16`
  - Description: Low priority - can be scheduled later

## Type Labels

These labels categorize the type of issue or PR:

- **bug** 🐛
  - Color: `#d73a4a`
  - Description: Something isn't working

- **enhancement** ✨
  - Color: `#a2eeef`
  - Description: New feature or request

- **documentation** 📚
  - Color: `#0075ca`
  - Description: Improvements or additions to documentation

- **security** 🔒
  - Color: `#d93f0b`
  - Description: Security vulnerability or security-related issue

- **task** 📋
  - Color: `#7057ff`
  - Description: General task or work item

- **question** ❓
  - Color: `#d876e3`
  - Description: Further information is requested

- **breaking-change** 💥
  - Color: `#d93f0b`
  - Description: Breaking change that requires migration

- **performance** ⚡
  - Color: `#f9d0c4`
  - Description: Performance improvements

- **refactoring** 🔨
  - Color: `#fbca04`
  - Description: Code refactoring without functional changes

- **testing** ✅
  - Color: `#c5def5`
  - Description: Related to testing

- **accessibility** ♿
  - Color: `#f9c513`
  - Description: Accessibility improvements

## Status Labels

These labels track the current state:

- **triage** 🏷️
  - Color: `#fbca04`
  - Description: Needs triage and initial assessment

- **in-progress** 🔄
  - Color: `#0052cc`
  - Description: Work is currently in progress

- **blocked** 🚧
  - Color: `#b60205`
  - Description: Blocked by another issue or external dependency

- **needs-review** 👀
  - Color: `#6f42c1`
  - Description: Waiting for code review

- **approved** ✔️
  - Color: `#0e8a16`
  - Description: Approved and ready to merge

- **duplicate** ➕
  - Color: `#cfd3d7`
  - Description: This issue or pull request already exists

- **wontfix** 🚫
  - Color: `#ffffff`
  - Description: This will not be worked on

- **invalid** ❌
  - Color: `#e4e669`
  - Description: This doesn't seem right

- **stale** 💤
  - Color: `#eeeeee`
  - Description: Stale issue or PR - no recent activity

## Category Labels

These labels help categorize the area of work:

- **github-actions** ⚙️
  - Color: `#000000`
  - Description: Related to GitHub Actions workflows

- **configuration** 🔧
  - Color: `#bfdadc`
  - Description: Configuration changes

- **dependencies** 📦
  - Color: `#0366d6`
  - Description: Pull requests that update a dependency file

- **automated** 🤖
  - Color: `#ededed`
  - Description: Automated changes (e.g., Dependabot, bots)

## Community Labels

These labels help community engagement:

- **good-first-issue** 👶
  - Color: `#7057ff`
  - Description: Good for newcomers

- **help-wanted** 🙋
  - Color: `#008672`
  - Description: Extra attention is needed - looking for contributors

## Area Labels

These labels indicate specific functional areas:

- **area: ci-cd** 🔁
  - Color: `#1d76db`
  - Description: Continuous Integration / Continuous Deployment

- **area: api** 🔌
  - Color: `#5319e7`
  - Description: API-related changes

- **area: ui** 🎨
  - Color: `#c2e0c6`
  - Description: User interface changes

- **area: infrastructure** 🏗️
  - Color: `#0e8a16`
  - Description: Infrastructure and deployment

## Sync Labels to All Repositories

To sync these labels across all repositories, use the GitHub API or a label sync tool:

### Using GitHub CLI

```bash
# Export labels from this repository
gh label list --json name,color,description > labels.json

# Import to another repository
gh label create --repo OWNER/REPO --force \
  $(cat labels.json | jq -r '.[] | "--name \(.name) --color \(.color) --description \"\(.description)\""')
```

### Using Label Sync Action

Add a workflow that automatically syncs labels:

```yaml
name: Sync Labels
on:
  push:
    paths:
      - '.github/labels.yml'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: micnncim/action-label-syncer@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          manifest: .github/labels.yml
```

## Maintenance

- Review and update labels quarterly
- Remove unused labels
- Add new labels as needed for evolving project needs
- Ensure all team members understand label meanings
- Document any custom labels specific to certain projects

## References

- [GitHub Labels Documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
