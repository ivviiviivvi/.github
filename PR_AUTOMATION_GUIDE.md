# PR & Dependency Management Automation

Comprehensive automation system for managing ALL pull requests - from Dependabot, Jules, GitHub Actions, Copilot, Renovate, and any other automated sources - with minimal manual intervention.

## 🎯 Overview

This system addresses common pain points in managing repositories with high PR volume from ALL sources:
- ✅ **Automated PR batching** - Group PRs from Dependabot, Jules, and all automated tools
- ✅ **Nightly cleanup** - Automated maintenance of PRs, branches, and more
- ✅ **Draft-to-ready automation** - AI agent PRs (Jules, Copilot, etc.) auto-convert when ready
- ✅ **Bulk operations** - Emergency batch actions for 100+ PRs from any source
- ✅ **Smart merging** - Auto-merge qualified PRs when checks pass

## 📋 Workflows

### 1. Auto-Batch Automated PRs
**File:** `.github/workflows/auto-batch-prs.yml`

Automatically groups ALL automated PRs for batch processing.

**Triggers:**
- Daily at 4 AM UTC (after automated tools run)
- When automated PRs are opened
- Manual dispatch

**What it does:**
1. Finds all open automated PRs (Dependabot, Jules, GitHub Actions, Renovate, Copilot, etc.)
2. Groups them by source and category
3. Applies batch labels (e.g., `batch:jules`, `batch:dependabot-npm`)
4. Comments on each PR with batch information
5. Triggers batch merge if all PRs in a batch pass checks

**Supported automated sources:**
- **Dependabot** - Grouped by ecosystem (npm, pip, GitHub Actions, Docker, Go, PHP)
- **Jules** - All Jules PRs batched together
- **GitHub Actions** - Bot-generated PRs
- **Renovate** - Alternative dependency update tool
- **Copilot** - AI-generated PRs
- **Manual PRs** - With `auto-batch` or `batch-me` label

**Example batch labels:**
- `batch:jules`
- `batch:dependabot-npm`
- `batch:github-actions`
- `batch:copilot`

### 2. Nightly Cleanup
**File:** `.github/workflows/nightly-cleanup.yml`

Comprehensive nightly maintenance and cleanup.

**Schedule:** Every night at 2 AM UTC

**Tasks:**
- ✅ Auto-merge ready PRs with `auto-merge` label (from ALL sources)
- ✅ Convert draft PRs from trusted agents (Jules, Dependabot, GitHub Actions, Copilot)
- ✅ Delete merged branches (excluding protected branches)
- ✅ Close stale PRs (90+ days inactive)

**Manual triggers:** Can run selectively with options to skip specific tasks

### 3. Bulk PR Operations
**File:** `.github/workflows/bulk-pr-operations.yml`

Emergency bulk actions for handling large numbers of PRs.

**Manual dispatch only** with the following operations:

#### Available Operations:
1. **approve-all-dependabot** - Approve and label all Dependabot PRs
2. **merge-all-ready** - Merge all PRs that pass checks
3. **close-all-stale** - Close PRs inactive for 90+ days
4. **convert-all-drafts** - Convert all draft PRs to ready
5. **label-all-dependencies** - Label dependency PRs for auto-merge

**Safety features:**
- Dry run mode (default: enabled)
- Max PR limit (default: 50)
- Optional label filtering
- Summary issue created after execution

### 4. Enhanced Auto-Assign
**File:** `.github/workflows/auto-assign.yml`

Ensures Copilot and other reviewers are assigned to PRs.

**Triggers:**
- PR opened
- PR ready for review

**What it does:**
- Assigns PR to author
- Requests review from @copilot (with 3 retry attempts)
- Falls back to assigning @copilot as assignee
- Works for both PRs and issues

### 5. Existing Workflows (Enhanced)

#### Draft-to-Ready Automation
Already exists, works with trusted agents including:
- Jules
- Dependabot
- GitHub Actions
- Copilot

**Enhanced in this update:**
- Now explicitly summons AI assistants (@copilot, @claude, @jules) when converting from draft to ready
- Manually triggers `pr-task-catcher.yml` workflow to scan for tasks
- Attempts to enable auto-merge via GitHub CLI
- Updates PR comments to indicate assistants have been notified
- **NEW: Supports both automated AND manual draft-to-ready conversions**

**Why this was needed:**
When the workflow programmatically converts a PR from draft to ready using `github.rest.pulls.update`, GitHub does not trigger the `ready_for_review` event. This meant workflows listening for that event (like `auto-assign.yml` and `auto-enable-merge.yml`) would not run automatically. 

Additionally, when users manually converted PRs from draft to ready via the GitHub UI, the workflow didn't run at all because it wasn't listening for the `ready_for_review` event. This caused AI assistants and integrated GitHub Apps to not be triggered.

**Solution:**
The workflow now:
1. Listens for the `ready_for_review` event (for manual conversions)
2. Explicitly performs notification actions for both automated and manual conversions
3. Ensures the full automation chain works correctly regardless of conversion method

#### PR Batch Merge
Manual and comment-triggered batch merging by label.

#### Auto-Enable Merge
Automatically enables auto-merge for qualifying PRs.

## ⚙️ Configuration

### Dependabot Configuration
**File:** `.github/dependabot.yml`

Optimized to reduce PR noise:
- **Grouped dependencies** by type (production, development, types)
- **Lower PR limits** (2-3 instead of 5)
- **Auto-merge labels** applied automatically
- **Weekly schedule** on Mondays at 3 AM UTC

### PR Automation Config
**File:** `.github/pr-automation.yml`

Controls auto-PR creation and merging behavior.

## 🚀 Usage

### For Regular Operation

**Everything runs automatically!** The system handles:
1. Dependabot PRs are batched daily
2. Ready PRs are merged nightly
3. Drafts from AI agents auto-convert
4. Stale PRs are cleaned up
5. Copilot is assigned to all PRs

### For Emergency Bulk Actions

When you have 100+ PRs to handle:

```bash
# 1. Approve all Dependabot PRs (dry run first)
gh workflow run bulk-pr-operations.yml \
  -f operation=approve-all-dependabot \
  -f dry_run=true

# 2. Review the dry run output, then run for real
gh workflow run bulk-pr-operations.yml \
  -f operation=approve-all-dependabot \
  -f dry_run=false

# 3. Merge all ready PRs
gh workflow run bulk-pr-operations.yml \
  -f operation=merge-all-ready \
  -f dry_run=false \
  -f max_prs=100
```

### For Manual Batch Merge

Comment on any PR in a batch:
```
/merge-batch dependabot-npm
```

Or trigger manually:
```bash
gh workflow run pr-batch-merge.yml \
  -f batch_label="batch:dependabot-npm"
```

### For Manual Nightly Run

```bash
# Full cleanup
gh workflow run nightly-cleanup.yml

# Skip specific tasks
gh workflow run nightly-cleanup.yml \
  -f skip_pr_cleanup=true \
  -f skip_branch_cleanup=false

# Dry run
gh workflow run nightly-cleanup.yml \
  -f dry_run=true
```

## 🏷️ Important Labels

### Auto-Applied Labels
- `auto-merge` - PR will be automatically merged when ready
- `auto-batch` - PR is part of an automated batch
- `auto-converted` - Draft PR was automatically converted
- `dependencies` - Dependency update PR

### Manual Control Labels
- `skip-auto-merge` - Prevent automatic merging
- `keep-draft` - Prevent draft-to-ready conversion
- `keep-open` - Prevent stale PR closure
- `needs-review` - Require manual review before merge

### Batch Labels
- `batch:dependabot-{ecosystem}` - Groups PRs for batch merge
- `batch:{custom}` - Custom batch grouping

## 📊 Monitoring

### Workflow Run Summaries
Each workflow provides a detailed summary in the Actions tab:
- Number of PRs processed
- Success/failure counts
- Errors encountered
- Next scheduled run

### Summary Issues
Bulk operations create summary issues with:
- Operation details
- Results breakdown
- Error list (if any)
- Timestamp and filter used

## 🛡️ Safety Features

1. **Dry Run Mode** - Test before applying changes
2. **PR Limits** - Prevent runaway operations (default: 50)
3. **Protected Branches** - Never auto-delete main/master/develop
4. **Skip Labels** - Manual override for any automation
5. **Concurrency Control** - Prevents simultaneous runs
6. **Retry Logic** - Handles transient failures

## 🔧 Customization

### Adjust Stale Threshold
Edit `nightly-cleanup.yml`, line with `staleDays`:
```yaml
const staleDays = 90; // Change to desired days
```

### Modify Batch Labels
Edit `auto-batch-dependabot.yml` to add custom ecosystems:
```yaml
const groups = {
  npm: [],
  pip: [],
  'github-actions': [],
  'your-custom-ecosystem': []  # Add here
};
```

### Change Schedule
Edit workflow `cron` expressions:
```yaml
schedule:
  - cron: '0 2 * * *'  # 2 AM UTC daily
```

[Cron syntax reference](https://crontab.guru/)

### Trusted Agents List
Edit `draft-to-ready-automation.yml` or `nightly-cleanup.yml`:
```javascript
const trustedAgents = [
  'Jules', 
  'dependabot[bot]', 
  'github-actions[bot]',
  'copilot',
  'your-custom-agent'  // Add here
];
```

## 🎓 Best Practices

1. **Start with dry runs** - Always test bulk operations first
2. **Use batch labels** - Group related PRs for efficient merging
3. **Monitor nightly runs** - Check summaries occasionally
4. **Set PR limits conservatively** - Increase only after testing
5. **Use skip labels** - For important PRs needing manual review
6. **Review dependabot batches** - Before they auto-merge
7. **Keep protected branches updated** - Add new long-lived branches

## 🆘 Troubleshooting

### Dependabot PRs Not Batching
- Check if PRs have `dependencies` label
- Verify workflow runs daily at 4 AM UTC
- Look for ecosystem detection in workflow logs

### PRs Not Auto-Merging
- Ensure `auto-merge` label is present
- Check that all CI checks pass
- Verify PR is not in draft mode
- Look for `skip-auto-merge` or `needs-review` labels

### Nightly Cleanup Not Running
- Check workflow schedule settings
- Verify workflow is enabled in Actions tab
- Review failed workflow runs for errors

### Bulk Operation Fails
- Check max_prs limit
- Review error messages in workflow summary
- Try with smaller batch and dry_run=true
- Verify permissions are correct

## 📚 Related Documentation

- [PR Automation Config](pr-automation.yml)
- [Dependabot Config](dependabot.yml)
- [Workflow Optimization Guide](../WORKFLOW_OPTIMIZATION_ROADMAP.md)
- [Branch Lifecycle](workflows/branch-lifecycle.yml)

## 🔄 Migration Guide

### From Manual PR Management

1. **Enable auto-merge labels** on existing PRs:
   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=label-all-dependencies \
     -f dry_run=false
   ```

2. **Convert draft PRs**:
   ```bash
   gh workflow run bulk-pr-operations.yml \
     -f operation=convert-all-drafts \
     -f dry_run=false
   ```

3. **Batch existing Dependabot PRs**:
   ```bash
   gh workflow run auto-batch-dependabot.yml
   ```

### From Other CI Systems

1. Update branch protection rules to allow auto-merge
2. Configure required status checks
3. Test with small PRs first
4. Gradually enable more automation

## 📈 Metrics & Insights

Track automation effectiveness:
- PRs merged automatically vs manually
- Time saved on PR management
- Dependabot PRs grouped per batch
- Stale PRs closed automatically

## 🤝 Contributing

To improve these workflows:
1. Test changes in a fork first
2. Use dry run mode extensively
3. Document any new features
4. Update this README
5. Add safety checks for new operations

## 📞 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Share ideas in GitHub Discussions
- **Logs**: Check workflow runs in Actions tab for debugging

---

**Last Updated:** 2025-12-31  
**Version:** 1.0.0  
**Maintained By:** Automation Team
