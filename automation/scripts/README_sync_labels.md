# Label Sync Script

Synchronizes standardized labels across all repositories in a GitHub
organization.

## Features

- **Priority Labels**: critical, high, medium, low
- **Type Labels**: bug, enhancement, documentation, security, task, question
- **Status Labels**: triage, in-progress, blocked, needs-review, approved
- **Category Labels**: github-actions, configuration, dependencies, automated
- Dry-run mode to preview changes
- Color-coded labels with descriptions
- Handles archived repositories
- Detailed sync statistics

## Installation

```bash
pip install PyGithub
```

## Usage

### Basic Usage

```bash
# Dry run (preview changes)
python scripts/sync_labels.py --org ivviiviivvi --dry-run

# Actually sync labels
export GITHUB_TOKEN=ghp_xxxxx
python scripts/sync_labels.py --org ivviiviivvi
```

### Advanced Usage

```bash
# Exclude specific repositories
python scripts/sync_labels.py --org ivviiviivvi --exclude repo1 repo2

# Use token from command line
python scripts/sync_labels.py --org ivviiviivvi --token ghp_xxxxx

# List all label definitions
python scripts/sync_labels.py --list-labels
```

## Label Definitions

### Priority Labels

| Label                | Color                                                                     | Description       |
| -------------------- | ------------------------------------------------------------------------- | ----------------- |
| `priority: critical` | ![#d73a4a](https://via.placeholder.com/15/d73a4a/000000?text=+) `#d73a4a` | Critical priority |
| `priority: high`     | ![#ff6b6b](https://via.placeholder.com/15/ff6b6b/000000?text=+) `#ff6b6b` | High priority     |
| `priority: medium`   | ![#ffa500](https://via.placeholder.com/15/ffa500/000000?text=+) `#ffa500` | Medium priority   |
| `priority: low`      | ![#0e8a16](https://via.placeholder.com/15/0e8a16/000000?text=+) `#0e8a16` | Low priority      |

### Type Labels

| Label           | Color                                                                     | Description                                |
| --------------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| `bug`           | ![#d73a4a](https://via.placeholder.com/15/d73a4a/000000?text=+) `#d73a4a` | Something isn't working                    |
| `enhancement`   | ![#a2eeef](https://via.placeholder.com/15/a2eeef/000000?text=+) `#a2eeef` | New feature or request                     |
| `documentation` | ![#0075ca](https://via.placeholder.com/15/0075ca/000000?text=+) `#0075ca` | Improvements or additions to documentation |
| `security`      | ![#d93f0b](https://via.placeholder.com/15/d93f0b/000000?text=+) `#d93f0b` | Security related                           |
| `task`          | ![#d4c5f9](https://via.placeholder.com/15/d4c5f9/000000?text=+) `#d4c5f9` | General task or work item                  |
| `question`      | ![#d876e3](https://via.placeholder.com/15/d876e3/000000?text=+) `#d876e3` | Further information is requested           |

### Status Labels

| Label          | Color                                                                     | Description                 |
| -------------- | ------------------------------------------------------------------------- | --------------------------- |
| `triage`       | ![#fbca04](https://via.placeholder.com/15/fbca04/000000?text=+) `#fbca04` | Needs triage                |
| `in-progress`  | ![#0052cc](https://via.placeholder.com/15/0052cc/000000?text=+) `#0052cc` | Work in progress            |
| `blocked`      | ![#b60205](https://via.placeholder.com/15/b60205/000000?text=+) `#b60205` | Blocked by dependency       |
| `needs-review` | ![#6f42c1](https://via.placeholder.com/15/6f42c1/000000?text=+) `#6f42c1` | Ready for review            |
| `approved`     | ![#0e8a16](https://via.placeholder.com/15/0e8a16/000000?text=+) `#0e8a16` | Approved and ready to merge |

### Category Labels

| Label                      | Color                                                                     | Description                         |
| -------------------------- | ------------------------------------------------------------------------- | ----------------------------------- |
| `category: github-actions` | ![#2088ff](https://via.placeholder.com/15/2088ff/000000?text=+) `#2088ff` | Related to GitHub Actions workflows |
| `category: configuration`  | ![#e99695](https://via.placeholder.com/15/e99695/000000?text=+) `#e99695` | Configuration files or settings     |
| `category: dependencies`   | ![#0366d6](https://via.placeholder.com/15/0366d6/000000?text=+) `#0366d6` | Dependency updates or issues        |
| `category: automated`      | ![#bfd4f2](https://via.placeholder.com/15/bfd4f2/000000?text=+) `#bfd4f2` | Automated processes or bots         |

## Configuration

Edit `LABEL_DEFINITIONS` in `sync_labels.py` to customize labels:

```python
LABEL_DEFINITIONS = {
    "your-label": {
        "color": "ffffff",  # Hex color (without #)
        "description": "Your label description"
    }
}
```

## GitHub Token Permissions

The GitHub token needs the following scopes:

- `repo` - Full control of private repositories
- `admin:org` - Full control of organizations (for organization-wide operations)

Create a token at: https://github.com/settings/tokens

## Dry Run Output Example

```
🔍 DRY RUN MODE - No changes will be made

Found 15 repositories in organization 'ivviiviivvi'

📦 Processing repo1...
  Would create: priority: critical
  Would create: priority: high
  Would update: status: triage

📦 Processing repo2...
  ✓ All labels up to date

============================================================
SUMMARY
============================================================
Repositories processed: 15
Repositories skipped:   2
Labels created:         45
Labels updated:         12
Labels unchanged:       203
Errors:                 0
============================================================

💡 Run without --dry-run to apply these changes
```

## Automation

Add to GitHub Actions for automated label sync:

```yaml
name: Sync Labels

on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * 0" # Weekly on Sunday

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install PyGithub

      - name: Sync labels
        env:
          GITHUB_TOKEN: ${{ secrets.ORG_ADMIN_TOKEN }}
        run: |
          python scripts/sync_labels.py --org ivviiviivvi
```

## Troubleshooting

### Permission Errors

If you get 404 or permission errors:

- Verify your token has the required scopes
- Check that you're an organization owner/admin
- Ensure the organization name is correct

### Rate Limiting

GitHub API has rate limits. The script will work for most organizations, but for
very large orgs (100+ repos):

- Run during off-peak hours
- Use a token to get higher rate limits (5000 requests/hour)
- Add delays between repositories if needed

## Contributing

To add new labels, edit the `LABEL_DEFINITIONS` dictionary in the script and
submit a PR.
