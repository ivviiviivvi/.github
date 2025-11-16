# Organization Labels Standard

This document defines the standard set of labels to be used across all repositories in the organization.

## Type Labels

These labels categorize the type of issue or PR:

- **bug** 🐛
  - Color: `#d73a4a`
  - Description: Something isn't working correctly

- **enhancement** ✨
  - Color: `#a2eeef`
  - Description: New feature or improvement request

- **documentation** 📚
  - Color: `#0075ca`
  - Description: Documentation improvements or additions

- **question** ❓
  - Color: `#d876e3`
  - Description: Further information is requested

- **refactoring** 🔨
  - Color: `#fbca04`
  - Description: Code refactoring without changing functionality

- **performance** ⚡
  - Color: `#f9d0c4`
  - Description: Performance improvements

- **security** 🔒
  - Color: `#d93f0b`
  - Description: Security-related issues or improvements

- **testing** ✅
  - Color: `#1d76db`
  - Description: Testing-related changes or improvements

## Priority Labels

These labels indicate the urgency or importance:

- **critical** 🚨
  - Color: `#b60205`
  - Description: Requires immediate attention

- **high priority** ⬆️
  - Color: `#d93f0b`
  - Description: Should be addressed soon

- **medium priority** ➡️
  - Color: `#fbca04`
  - Description: Normal priority

- **low priority** ⬇️
  - Color: `#0e8a16`
  - Description: Can be addressed later

## Status Labels

These labels track the current state:

- **in progress** 🔄
  - Color: `#ffff00`
  - Description: Currently being worked on

- **blocked** 🚧
  - Color: `#d93f0b`
  - Description: Blocked by another issue or dependency

- **on hold** ⏸️
  - Color: `#fef2c0`
  - Description: Temporarily paused

- **needs review** 👀
  - Color: `#bfdadc`
  - Description: Waiting for code review

- **needs testing** 🧪
  - Color: `#c5def5`
  - Description: Requires testing before completion

- **ready to merge** ✔️
  - Color: `#0e8a16`
  - Description: Approved and ready to be merged

## Community Labels

These labels help community engagement:

- **good first issue** 👶
  - Color: `#7057ff`
  - Description: Good for newcomers

- **help wanted** 🙋
  - Color: `#008672`
  - Description: Extra attention is needed

- **discussion** 💬
  - Color: `#cc317c`
  - Description: Requires discussion before implementation

- **duplicate** ➕
  - Color: `#cfd3d7`
  - Description: This issue or PR already exists

- **invalid** ❌
  - Color: `#e4e669`
  - Description: This doesn't seem right

- **wontfix** 🚫
  - Color: `#ffffff`
  - Description: This will not be worked on

## Automated Labels

These labels are typically applied by automation:

- **automated** 🤖
  - Color: `#fbca04`
  - Description: Created or updated by automation

- **dependencies** 📦
  - Color: `#0366d6`
  - Description: Pull requests that update a dependency file

- **stale** 💤
  - Color: `#eeeeee`
  - Description: No recent activity

- **github-actions** ⚙️
  - Color: `#000000`
  - Description: Related to GitHub Actions workflows

## Platform/Technology Labels

Use these to indicate specific platforms or technologies:

- **frontend** 🎨
  - Color: `#bfe5bf`
  - Description: Frontend-related changes

- **backend** 💾
  - Color: `#c2e0c6`
  - Description: Backend-related changes

- **infrastructure** 🏗️
  - Color: `#fad8c7`
  - Description: Infrastructure and DevOps changes

- **database** 🗄️
  - Color: `#d4c5f9`
  - Description: Database-related changes

- **api** 🔌
  - Color: `#f9c513`
  - Description: API-related changes

- **ui/ux** 🖼️
  - Color: `#eb6420`
  - Description: User interface or experience changes

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
