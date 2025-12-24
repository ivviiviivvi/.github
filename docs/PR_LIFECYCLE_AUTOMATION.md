# Automated PR Lifecycle Management

> **Automated workflows for managing PR lifecycle: Draft → Ready → Merge with batch operations**

## Overview

This system automates the complete PR lifecycle, designed specifically for teams working with AI agents (like Jules) and high volumes of PRs. It handles:

1. **Draft to Ready Conversion** - Automatically converts draft PRs when criteria are met
2. **Suggestion Extraction** - Extracts actionable items from PR comments into TODO lists
3. **Batch Operations** - Processes multiple PRs simultaneously
4. **Auto-Merge** - Merges PRs when all checks pass

## Workflows

### 1. Draft to Ready Automation

**File:** `.github/workflows/draft-to-ready-automation.yml`

Automatically converts draft PRs to "ready for review" when:
- PR is from a trusted AI agent (Jules, github-actions[bot], dependabot)
- PR has `auto-ready` or `ready-when-green` label
- PR title contains `[auto-ready]`

**Usage:**

```bash
# Manual trigger for specific PR
gh workflow run draft-to-ready-automation.yml -f pr_number=123

# Force conversion even if checks aren't passing
gh workflow run draft-to-ready-automation.yml -f pr_number=123 -f force=true

# Scan all draft PRs and convert eligible ones
gh workflow run draft-to-ready-automation.yml
```

**Automatic Triggers:**
- When PR is opened or synchronized
- When check suites complete
- When PR is converted to draft (re-evaluates conversion)

**Prevention:**
Add one of these labels to keep PR as draft:
- `keep-draft`
- `skip-auto-ready`

---

### 2. PR Suggestion Implementation

**File:** `.github/workflows/pr-suggestion-implementation.yml`

Extracts suggestions and actionable items from PR comments and creates a TODO file for implementation.

**Usage:**

Comment on any PR with:
```
/implement-suggestions
```

Or:
```
/implement-all
```

Or manually trigger:
```bash
gh workflow run pr-suggestion-implementation.yml -f pr_number=123
```

**What it does:**
1. Scans all comments and review comments on the PR
2. Extracts suggestions, TODOs, blockers, and action items
3. Creates a `TODO_PR_<number>.md` file in the PR branch
4. Categorizes suggestions as auto-implementable or needs-review
5. Commits the TODO file to the PR branch
6. Comments on the PR with summary

**Extracted Keywords:**
- Suggestions: "suggest", "should", "could", "consider", "recommend"
- Blockers: "blocker", "must fix", "required", "critical", "FIXME", "TODO"
- Action items: Identified from review threads and comments

**Labels Added:**
- `has-todo` - PR has a TODO file
- `suggestions-extracted` - Suggestions have been extracted

---

### 3. Batch PR Lifecycle Management

**File:** `.github/workflows/batch-pr-lifecycle.yml`

Unified workflow to process multiple PRs through the entire lifecycle simultaneously.

**Usage:**

```bash
# Full pipeline: draft → ready → merge
gh workflow run batch-pr-lifecycle.yml -f action=full-pipeline

# Convert all draft PRs to ready
gh workflow run batch-pr-lifecycle.yml -f action=draft-to-ready-all

# Merge all ready PRs
gh workflow run batch-pr-lifecycle.yml -f action=merge-ready-prs

# With filters (only Jules PRs)
gh workflow run batch-pr-lifecycle.yml \
  -f action=full-pipeline \
  -f author_filter=Jules

# With label filter
gh workflow run batch-pr-lifecycle.yml \
  -f action=full-pipeline \
  -f label_filter=batch:api-update

# Dry run (see what would happen)
gh workflow run batch-pr-lifecycle.yml \
  -f action=full-pipeline \
  -f dry_run=true
```

**Actions:**
- `draft-to-ready-all` - Convert all eligible draft PRs to ready
- `merge-ready-prs` - Merge all PRs that are ready and passing checks
- `full-pipeline` - Complete pipeline: convert drafts, then merge ready PRs
- `cleanup-merged` - Clean up branches for merged PRs

**Automatic Schedule:**
Runs daily at 2 AM UTC to process accumulated PRs.

**Outputs:**
- Analysis report showing all PRs and their status
- Summary issue with results
- Individual PR comments documenting actions taken

---

### 4. Existing Enhanced Workflows

These existing workflows are enhanced by the new system:

#### Auto-Merge (`auto-merge.yml`)
- Works with PRs that have been converted to ready
- Handles merge conflicts automatically
- Checks for required approvals
- Merges when all conditions are met

#### PR Task Catcher (`pr-task-catcher.yml`)
- Now works in conjunction with suggestion implementation
- Extracts and tracks tasks from comments
- Adds `has-blockers` label when blockers are found

#### Batch Merge (`pr-batch-merge.yml`)
- Handles PRs grouped by labels (e.g., `batch:feature-xyz`)
- Preserves data and functionality during merge

## Complete Workflow Examples

### Example 1: Jules creates 20 draft PRs

**What happens automatically:**

1. Jules creates 20 draft PRs
2. `draft-to-ready-automation.yml` detects Jules as trusted agent
3. When checks pass, PRs are converted to ready
4. `auto-merge.yml` merges each PR when:
   - All checks pass
   - No merge conflicts
   - Required approvals obtained (auto-approved for bot PRs)
5. Branches are automatically cleaned up

**Manual override:**
If you want to review before merge, add `keep-draft` label.

---

### Example 2: PR accumulates 30 comments with suggestions

**Workflow:**

1. PR has 30+ comments with various suggestions
2. Comment on PR: `/implement-suggestions`
3. Workflow extracts all actionable items
4. Creates `TODO_PR_123.md` with categorized suggestions
5. File is committed to PR branch
6. Review TODO and implement suggestions
7. Check off items as completed

---

### Example 3: Batch cleanup of 50 PRs

**Scenario:** 50 PRs from Jules are sitting in draft state, all ready to merge.

**Workflow:**

```bash
# Dry run first to see what would happen
gh workflow run batch-pr-lifecycle.yml \
  -f action=full-pipeline \
  -f author_filter=Jules \
  -f dry_run=true

# Review the analysis report

# Execute the full pipeline
gh workflow run batch-pr-lifecycle.yml \
  -f action=full-pipeline \
  -f author_filter=Jules
```

**Result:**
- All 50 draft PRs converted to ready (if checks pass)
- All ready PRs merged automatically
- All branches cleaned up
- Summary issue created with full report

---

## Configuration

### Trusted AI Agents

Edit workflows to add/remove trusted agents:

```yaml
trustedAgents = ['Jules', 'dependabot[bot]', 'github-actions[bot]', 'your-bot-name']
```

### Labels

Create these labels in your repository:

```bash
# Auto-ready labels
gh label create "auto-ready" --description "Auto-convert from draft to ready" --color "0E8A16"
gh label create "ready-when-green" --description "Convert to ready when checks pass" --color "0E8A16"
gh label create "keep-draft" --description "Keep this PR as draft" --color "D93F0B"
gh label create "skip-auto-ready" --description "Skip auto-conversion to ready" --color "D93F0B"

# Auto-merge labels (may already exist)
gh label create "auto-merge" --description "Auto-merge when ready" --color "0E8A16"
gh label create "auto-converted" --description "Auto-converted from draft" --color "BFDADC"

# Task tracking labels
gh label create "has-todo" --description "Has TODO file for implementation" --color "FEF2C0"
gh label create "suggestions-extracted" --description "Suggestions extracted from comments" --color "BFDADC"
gh label create "has-blockers" --description "Has blocking items" --color "D93F0B"
gh label create "has-pending-tasks" --description "Has pending tasks" --color "FBCA04"

# Batch labels
gh label create "batch-processed" --description "Processed in batch operation" --color "BFDADC"
```

### Branch Protection

Ensure branch protection rules allow bot merges:

1. Go to Settings → Branches → Branch protection rules
2. For `main` branch:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Allow auto-merge
   - ✅ Allow GitHub Actions to bypass restrictions (for bot merges)

---

## Best Practices

### For AI Agent PRs (Jules, etc.)

1. **Trust the automation** - Let the system handle draft → ready → merge
2. **Use labels for exceptions** - Add `keep-draft` if manual review needed
3. **Review TODO files** - Check `TODO_PR_*.md` files for extracted suggestions
4. **Monitor batch runs** - Review summary issues from batch operations

### For Manual PRs

1. **Add `auto-ready` label** - If you want draft converted automatically
2. **Add `auto-merge` label** - If you want automatic merging
3. **Use `/implement-suggestions`** - To extract and track feedback

### For Batch Operations

1. **Start with dry run** - Always test with `dry_run=true` first
2. **Use filters** - Filter by author or label to target specific PRs
3. **Review analysis** - Check the analysis report before executing
4. **Monitor progress** - Watch workflow logs during execution

---

## Troubleshooting

### PR not converting from draft

**Check:**
- Is PR from trusted agent? (Jules, dependabot, github-actions)
- Does PR have `auto-ready` or `ready-when-green` label?
- Does PR have `keep-draft` or `skip-auto-ready` label? (these block conversion)
- Are checks passing?

**Fix:**
- Add `auto-ready` label
- Remove skip labels
- Wait for checks to pass
- Manually trigger: `gh workflow run draft-to-ready-automation.yml -f pr_number=123 -f force=true`

### PR not auto-merging

**Check:**
- Is PR still draft? (must be ready)
- Does PR have `auto-merge` label?
- Are all checks passing?
- Does PR have merge conflicts?
- Does PR have `has-blockers` label?

**Fix:**
- Add `auto-merge` label
- Wait for checks to pass
- Resolve merge conflicts
- Address blockers

### Batch operation not processing all PRs

**Check:**
- Are filters too restrictive?
- Do PRs have skip labels?
- Are checks failing?

**Fix:**
- Adjust filters
- Remove skip labels
- Fix failing checks
- Run with `dry_run=true` to see what would be processed

---

## Monitoring

### View Batch Reports

Analysis reports are created for each batch run:
- Download from workflow artifacts
- Posted as issues (for non-scheduled runs)

### Check Workflow Runs

```bash
# List recent workflow runs
gh run list --workflow=batch-pr-lifecycle.yml

# View specific run
gh run view <run-id>

# View logs
gh run view <run-id> --log
```

### PR Status

Each processed PR gets:
- Labels indicating its status
- Comments documenting actions taken
- TODO files for suggestions (if applicable)

---

## Integration with Existing Workflows

These new workflows integrate seamlessly with existing automation:

1. **auto-merge.yml** - Works with converted PRs
2. **pr-task-catcher.yml** - Enhanced with suggestion extraction
3. **pr-batch-merge.yml** - Complementary batch operations
4. **auto-enable-merge.yml** - Enables auto-merge for converted PRs

No changes to existing workflows are required.

---

## Security Considerations

- All workflows use pinned action versions (SHA hashes)
- Branch protection rules are respected
- Protected branches (main, master, develop) are never deleted
- Dry run mode available for testing
- Manual approval can be required via labels

---

## Future Enhancements

Potential improvements:
- [ ] AI-powered suggestion implementation (actually apply the changes)
- [ ] Conflict resolution automation
- [ ] Priority-based processing
- [ ] Cross-repository batch operations
- [ ] Advanced dependency detection for merge order
- [ ] Rollback capabilities

---

## Support

For issues or questions:
1. Check this documentation
2. Review workflow logs
3. Check PR comments for automation status
4. Create an issue in the repository

---

_Last updated: 2024-12-24_
