# PR Automation Quick Reference

Quick commands and tips for using the PR automation system for ALL PRs
(Dependabot, Jules, GitHub Actions, Copilot, etc.).

## 🚀 Quick Commands

### Batch Merge Automated PRs

```bash
# View batches ready for merge
gh workflow run auto-batch-prs.yml

# Merge a specific batch (Jules, Dependabot, etc.)
gh workflow run pr-batch-merge.yml -f batch_label="batch:jules"
gh workflow run pr-batch-merge.yml -f batch_label="batch:dependabot-npm"
gh workflow run pr-batch-merge.yml -f batch_label="batch:copilot"

# Or comment on any PR in the batch:
/merge-batch jules
/merge-batch dependabot-npm
```

### Emergency Bulk Operations

```bash
# Approve all automated PRs (Jules, Dependabot, etc.) - dry run first!
gh workflow run bulk-pr-operations.yml \
  -f operation=approve-all-automated \
  -f dry_run=true

# Approve only Dependabot PRs
gh workflow run bulk-pr-operations.yml \
  -f operation=approve-all-dependabot \
  -f dry_run=false

# Merge all ready PRs (up to 50)
gh workflow run bulk-pr-operations.yml \
  -f operation=merge-all-ready \
  -f dry_run=false \
  -f max_prs=50

# Close stale PRs
gh workflow run bulk-pr-operations.yml \
  -f operation=close-all-stale \
  -f dry_run=false

# Convert all drafts to ready
gh workflow run bulk-pr-operations.yml \
  -f operation=convert-all-drafts \
  -f dry_run=false
```

### Manual Nightly Cleanup

```bash
# Run full cleanup
gh workflow run nightly-cleanup.yml

# Run with dry-run
gh workflow run nightly-cleanup.yml -f dry_run=true

# Skip specific tasks
gh workflow run nightly-cleanup.yml \
  -f skip_pr_cleanup=true \
  -f skip_branch_cleanup=false
```

## 🏷️ Important Labels

### Apply These to Control Automation

**Enable auto-merge:**

```bash
gh pr edit <PR_NUMBER> --add-label "auto-merge"
```

**Prevent auto-merge:**

```bash
gh pr edit <PR_NUMBER> --add-label "skip-auto-merge"
# or
gh pr edit <PR_NUMBER> --add-label "needs-review"
```

**Keep PR as draft:**

```bash
gh pr edit <PR_NUMBER> --add-label "keep-draft"
```

**Prevent stale closure:**

```bash
gh pr edit <PR_NUMBER> --add-label "keep-open"
```

## 📋 Common Scenarios

### Scenario 1: 100+ PRs from Multiple Sources (Jules, Dependabot, etc.)

1. **Check current state:**

   ```bash
   gh pr list --label automated --limit 100
   # Or check specific sources
   gh pr list --author Jules --limit 50
   gh pr list --author dependabot --limit 50
   ```

1. **Approve all automated PRs (dry run):**

   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=approve-all-automated \
     -f dry_run=true
   ```

1. **Review dry run output**, then run for real:

   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=approve-all-automated \
     -f dry_run=false
   ```

1. **Wait for CI, then merge ready PRs:**

   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=merge-all-ready \
     -f dry_run=false \
     -f max_prs=100
   ```

### Scenario 2: Batch Similar PRs

1. **Label PRs with a batch tag:**

   ```bash
   gh pr edit 123 --add-label "batch:api-updates"
   gh pr edit 124 --add-label "batch:api-updates"
   gh pr edit 125 --add-label "batch:api-updates"
   ```

1. **Merge the batch:**

   ```bash
   gh workflow run pr-batch-merge.yml -f batch_label="batch:api-updates"
   ```

### Scenario 3: Clean Up Old PRs

1. **See what would be closed (dry run):**

   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=close-all-stale \
     -f dry_run=true
   ```

1. **Close stale PRs:**

   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=close-all-stale \
     -f dry_run=false
   ```

### Scenario 4: Convert Multiple Draft PRs

```bash
gh workflow run bulk-pr-operations.yml \
  -f operation=convert-all-drafts \
  -f dry_run=false
```

## 🔍 Monitoring

### Check Workflow Status

```bash
# List recent workflow runs
gh run list --workflow=nightly-cleanup.yml --limit 5

# View specific run
gh run view <RUN_ID>

# View logs
gh run view <RUN_ID> --log
```

### Find PRs by Label

```bash
# Auto-merge PRs
gh pr list --label auto-merge

# Dependabot PRs
gh pr list --label dependencies

# PRs in a batch
gh pr list --label batch:dependabot-npm
```

### Check Batch Status

```bash
# List all batch labels
gh label list | grep "batch:"

# Count PRs in each batch
for label in $(gh label list --json name -q '.[].name' | grep "batch:"); do
  count=$(gh pr list --label "$label" --json number -q 'length')
  echo "$label: $count PRs"
done
```

## ⚙️ Configuration Tips

### Adjust Dependabot Frequency

Edit `.github/dependabot.yml`:

```yaml
schedule:
  interval: "weekly" # or "daily", "monthly"
  day: "monday" # day of week
  time: "03:00" # UTC time
```

### Change Nightly Schedule

Edit `.github/workflows/nightly-cleanup.yml`:

```yaml
schedule:
  - cron: "0 2 * * *" # 2 AM UTC daily
```

### Modify Stale Threshold

Edit `.github/workflows/nightly-cleanup.yml`, find:

```javascript
const staleDays = 90; // Change this value
```

### Add Trusted Agents

Edit `.github/workflows/draft-to-ready-automation.yml`:

```javascript
const trustedAgents = [
  "Jules",
  "dependabot[bot]",
  "github-actions[bot]",
  "copilot",
  "your-agent-name", // Add here
];
```

## 🛡️ Safety Checklist

Before running bulk operations:

- [ ] Test with `dry_run=true` first
- [ ] Set reasonable `max_prs` limit (start with 10-20)
- [ ] Use label filtering for specific PR groups
- [ ] Check that CI is working properly
- [ ] Verify branch protection rules
- [ ] Have rollback plan ready
- [ ] Monitor first few operations closely

## 📊 Useful Queries

### PRs by State

```bash
# Ready to merge
gh pr list --label auto-merge --json number,title,checks

# Stale PRs
gh pr list --search "updated:<$(date -d '90 days ago' +%Y-%m-%d)"

# Draft PRs
gh pr list --state open --json number,title,draft -q '.[] | select(.draft==true)'
```

### Workflow Statistics

```bash
# Success rate for nightly cleanup
gh run list --workflow=nightly-cleanup.yml --json conclusion \
  -q 'map(select(.conclusion != null)) | group_by(.conclusion) | map({conclusion: .[0].conclusion, count: length})'
```

## 🆘 Emergency Commands

### Stop All Auto-Merge

```bash
# Remove auto-merge label from all PRs
gh pr list --label auto-merge --json number -q '.[].number' | \
  xargs -I {} gh pr edit {} --remove-label auto-merge
```

### Disable Workflows Temporarily

```bash
# Disable a workflow
gh workflow disable nightly-cleanup.yml

# Re-enable later
gh workflow enable nightly-cleanup.yml
```

### Revert Batch Merge

```bash
# If a batch merge goes wrong
git revert <merge-commit-sha>
git push origin main
```

## 📚 Learn More

- [Full Documentation](PR_AUTOMATION_GUIDE.md)
- [Workflow Files](.github/workflows/)
- [Dependabot Config](.github/dependabot.yml)
- [PR Automation Config](.github/pr-automation.yml)

## 💡 Tips & Tricks

1. **Use aliases** for common commands:

   ```bash
   alias batch-approve='gh workflow run bulk-pr-operations.yml -f operation=approve-all-dependabot -f dry_run=false'
   alias batch-merge='gh workflow run bulk-pr-operations.yml -f operation=merge-all-ready -f dry_run=false'
   ```

1. **Monitor with watch**:

   ```bash
   watch -n 30 'gh pr list --label auto-merge | head -20'
   ```

1. **Create custom batch labels** for different types of work:

   ```bash
   gh label create "batch:security-updates" --color "d73a4a" --description "Security update batch"
   ```

1. **Set up notifications** for batch completion:

   - Subscribe to workflow runs in GitHub
   - Use GitHub mobile app for instant alerts

1. **Review batch summaries** regularly:

   ```bash
   gh issue list --label bulk-operation --limit 10
   ```

---

**Last Updated:** 2025-12-31\
**Quick Help:** `gh workflow list` to see all
available workflows
