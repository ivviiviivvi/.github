# Automated PR Merging - Quick Reference

## The Problem

**"Cannot programmatically merge PRs without GitHub API credentials"**

## The Eternal Solution

✅ **GitHub Actions with built-in `GITHUB_TOKEN`**

No external tokens needed. No maintenance required. Works forever.

## Quick Start (3 Steps)

### 1. Enable Auto-Merge in Your Repository

```bash
gh repo edit --enable-auto-merge
```

### 2. Add to Any PR

```bash
# Option A: Add label
gh pr edit <PR#> --add-label "auto-merge"

# Option B: Include in title
gh pr create --title "[auto-merge] Your feature"
```

### 3. Done! 

The PR will automatically merge when:
- ✅ All checks pass
- ✅ Required approvals obtained
- ✅ No conflicts exist

## How It Works

Our repository includes pre-configured workflows:

1. **`auto-merge.yml`** - Monitors PRs and merges when ready
2. **`auto-enable-merge.yml`** - Automatically enables auto-merge for qualifying PRs

Both use only the built-in `GITHUB_TOKEN` - no setup required!

## Features

- ✅ **Zero Configuration** - Works out of the box
- ✅ **No Tokens Required** - Uses built-in `GITHUB_TOKEN`
- ✅ **Fully Automated** - Set and forget
- ✅ **Safe** - Respects all branch protections
- ✅ **Flexible** - Multiple trigger methods
- ✅ **Auditable** - Complete GitHub Actions logs

## Trigger Methods

### Method 1: Label
```bash
gh pr edit 123 --add-label "auto-merge"
```

### Method 2: Title Marker
```bash
gh pr create --title "[auto-merge] Fix bug in auth"
```

### Method 3: Manual Dispatch
```bash
gh workflow run auto-merge.yml -f pr_number=123
```

### Method 4: Automatic (for bots)
Dependabot and other bot PRs are automatically enabled.

## Customization

### Change Merge Method

Edit `.github/workflows/auto-merge.yml`:

```yaml
# Line ~310
merge_method: 'squash'  # or 'merge', 'rebase'
```

### Adjust Approval Requirements

Edit `.github/workflows/auto-merge.yml`:

```yaml
# Line ~277
const requiredApprovals = isHotfix ? 0 : 1;  # Change the number
```

### Add Custom Rules

Create a new workflow that extends the auto-merge:

```yaml
name: Custom Auto-Merge Rules
on:
  pull_request:
    types: [labeled]

jobs:
  custom-rules:
    if: contains(github.event.pull_request.labels.*.name, 'auto-merge')
    runs-on: ubuntu-latest
    steps:
      - name: Your custom logic
        run: echo "Add your validation here"
```

## Troubleshooting

### Auto-merge not triggering?

**Checklist:**
- [ ] Repository has auto-merge enabled: `gh repo edit --enable-auto-merge`
- [ ] PR has `auto-merge` label or `[auto-merge]` in title
- [ ] PR is not in draft mode
- [ ] All required checks are passing
- [ ] Required approvals are obtained
- [ ] No merge conflicts

### Permission errors?

Check workflow permissions in `.github/workflows/auto-merge.yml`:

```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
  checks: read
```

### Still having issues?

1. Check workflow run logs: `gh run list --workflow=auto-merge.yml`
2. View specific run: `gh run view <run-id>`
3. See [Full Documentation](./AUTO_MERGE_GUIDE.md)

## Advanced Usage

### Use as Reusable Workflow

```yaml
name: My Custom Auto-Merge
on:
  pull_request:

jobs:
  auto-merge:
    uses: ./.github/workflow-templates/auto-merge-reusable.yml
```

### Integrate with Merge Queue

```yaml
# In repository settings
merge_group:
  required_checks:
    - ci
    - tests
```

### Monitor Activity

```bash
# View recent auto-merges
gh pr list --state merged --label auto-merged --limit 10

# Check pending auto-merges
gh pr list --state open --label auto-merge
```

## Examples

### Dependabot Auto-Merge
Automatically merges dependency update PRs:
```yaml
# Included in auto-enable-merge.yml
# Dependabot PRs (non-major) are auto-enabled
```

### Documentation Changes
Auto-merge docs-only changes:
```yaml
# Add 'documentation' label to your PR
# PRs with <10 file changes are auto-enabled
```

### Hotfix Fast-Track
Quick-merge critical fixes:
```yaml
# Add 'hotfix' label
# Bypasses approval requirements
```

## Benefits

| Feature | Manual Merge | Auto-Merge |
|---------|-------------|------------|
| Speed | Manual click | Automatic |
| Availability | Business hours | 24/7 |
| Consistency | Variable | Always same rules |
| Audit Trail | Basic | Complete logs |
| Cost | Time-consuming | Zero-cost |
| Maintenance | N/A | Zero maintenance |

## Security

✅ **Secure by Default**
- Uses GitHub's built-in authentication
- Respects all branch protection rules
- Full audit trail in Actions logs
- Token expires after each run
- No long-lived credentials

## Resources

- 📖 [Full Documentation](./AUTO_MERGE_GUIDE.md)
- 🔧 [Reusable Workflow Template](../workflow-templates/auto-merge-reusable.yml)
- 🤖 [Auto-Enable Workflow](../.github/workflows/auto-enable-merge.yml)
- 📝 [GitHub Docs: Auto-merge](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)

## Contributing

Found a bug or have a suggestion? Open an issue or PR!

---

**This solution is eternal.** It uses only GitHub's native features and requires no maintenance.
