# Branch Deletion Recovery Guide

## Overview

This guide explains how to recover accidentally deleted branches using the branch deletion audit system implemented to solve the issue described in `BRANCH_RECOVERY_REPORT.md`.

## The Problem We Solved

**Original Issue:**
> "The deletion list contains branch names only, not the tip commit SHAs.
> Once branches are deleted, we cannot reconstruct each branch's exact diff unless we also preserved:
> tip SHAs (e.g., from git ls-remote --heads origin …),
> PR refs (if they existed),
> or patches/artifacts."

**Our Solution:**
We now automatically capture and preserve all critical metadata before any branch deletion.

## How It Works

### Automatic Audit Logging

Every time a branch is deleted (automatically or manually), the system:

1. **Captures the tip commit SHA** using `git ls-remote`
2. **Records PR metadata** (number, title, URL, state)
3. **Stores commit details** (author, date, message, parents)
4. **Logs deletion context** (timestamp, reason, who deleted it)
5. **Saves everything** to `.github/branch-deletion-audit/YYYY-MM-deletions.jsonl`

### Integration Points

The audit logging is integrated into:
- **Branch Lifecycle Workflow** (`.github/workflows/branch-lifecycle.yml`)
  - Stale PR management (24h/96h thresholds)
  - Merged branch cleanup
- **Manual Deletions** (via helper script)

## Quick Start: Recovering a Branch

### Step 1: Search for the Branch

```bash
./.github/scripts/recover-branch.sh "branch-name"
```

This will:
- Search all audit logs
- Display the deletion record
- Show the tip commit SHA
- Provide recovery commands

### Step 2: Choose Recovery Method

#### Option A: Recreate the Branch

```bash
git fetch origin <SHA>
git branch <branch-name> <SHA>
git push origin <branch-name>
```

#### Option B: Cherry-pick the Commit

```bash
git cherry-pick <SHA>
```

#### Option C: Create a Patch File

```bash
git format-patch -1 <SHA> -o /tmp/
git am /tmp/0001-*.patch
```

#### Option D: Just View the Changes

```bash
git show <SHA>
git diff <SHA>^..<SHA>
```

## Manual Branch Deletion

If you need to manually delete a branch, ALWAYS log it first:

```bash
# Log the deletion (preserves SHA)
./.github/scripts/log-branch-deletion.sh "branch-name" "PR-number" "reason"

# Then delete the branch
git push origin --delete "branch-name"
```

**Never skip the logging step!** Without it, recovery becomes much harder.

## Querying Audit Logs

Audit logs use JSON Lines format, making them easy to query:

### Find a Specific Branch

```bash
grep '"branch":"feature/my-branch"' .github/branch-deletion-audit/*.jsonl | jq '.'
```

### List All Deleted Branches

```bash
grep -h '"branch":' .github/branch-deletion-audit/*.jsonl | jq -r '.branch' | sort -u
```

### Find Deletions This Month

```bash
cat .github/branch-deletion-audit/$(date +%Y-%m)-deletions.jsonl | jq '.'
```

### Find by PR Number

```bash
grep '"pr_number":"123"' .github/branch-deletion-audit/*.jsonl
```

### Find by Deletion Reason

```bash
grep '"reason":"stale-pr' .github/branch-deletion-audit/*.jsonl
```

### Find Recent Deletions

```bash
# Last 10 deletions across all files
tail -n 10 .github/branch-deletion-audit/*.jsonl | jq '.'
```

## Audit Log Schema

Each deletion record contains:

```json
{
  "timestamp": "2026-01-19T23:45:00Z",        // When deleted
  "branch": "feature/my-branch",              // Branch name
  "tip_sha": "abc123...",                     // Commit SHA (for recovery!)
  "pr_number": "123",                         // Associated PR
  "pr_title": "Add new feature",              // PR title
  "pr_url": "https://github.com/.../pull/123", // PR link
  "pr_state": "CLOSED",                       // PR state
  "reason": "stale-pr-no-tasks",              // Why deleted
  "commit_author": "John Doe <john@...>",     // Who wrote the code
  "commit_date": "2026-01-18T10:30:00Z",      // When committed
  "commit_message": "feat: implement X",      // Commit message
  "commit_parents": "parent1 parent2",        // Parent commits
  "deleted_by": "github-actions",             // Who triggered deletion
  "repository": "org/repo"                    // Which repo
}
```

## Common Scenarios

### Scenario 1: Accidentally Deleted Active Work

**Problem:** You deleted a branch but realize it had important uncommitted work.

**Solution:**
```bash
# Find the branch
./.github/scripts/recover-branch.sh "my-feature-branch"

# Recreate it
git fetch origin <SHA-from-output>
git branch my-feature-branch <SHA>
git checkout my-feature-branch

# Continue working
```

### Scenario 2: Need Code from Old Branch

**Problem:** You need to reference code that was in a deleted branch.

**Solution:**
```bash
# Find the branch
./.github/scripts/recover-branch.sh "old-branch"

# View the code
git show <SHA>

# Or extract specific files
git show <SHA>:path/to/file.js > /tmp/recovered-file.js
```

### Scenario 3: PR Was Auto-Closed But Needed

**Problem:** Stale PR was auto-closed and branch deleted, but work is still needed.

**Solution:**
```bash
# Find by PR number in audit logs
grep '"pr_number":"456"' .github/branch-deletion-audit/*.jsonl | jq '.'

# Get the SHA
SHA=$(grep '"pr_number":"456"' .github/branch-deletion-audit/*.jsonl | jq -r '.tip_sha')

# Create new branch
git fetch origin $SHA
git branch recovered-feature $SHA
git push origin recovered-feature

# Create new PR
gh pr create --base main --head recovered-feature
```

### Scenario 4: Bulk Recovery After Cleanup

**Problem:** Cleanup script deleted multiple branches, need to review them.

**Solution:**
```bash
# List all deletions from cleanup
grep '"reason":"merged-into-develop"' .github/branch-deletion-audit/*.jsonl | jq -r '.branch'

# For each branch of interest
./.github/scripts/recover-branch.sh "branch-name"
```

## Prevention Tips

### Use Keep-Alive Labels

For PRs that need more time:
```bash
gh pr edit <number> --add-label "keep-alive"
```

### Regular Audits

Review the audit logs periodically:
```bash
# Check recent deletions
tail -20 .github/branch-deletion-audit/*.jsonl | jq '.branch,.reason'
```

### Custom Deletion Scripts

Always use the logging script in custom automation:
```bash
# In your script
for branch in $BRANCHES_TO_DELETE; do
  ./.github/scripts/log-branch-deletion.sh "$branch" "unknown" "custom-cleanup"
  git push origin --delete "$branch"
done
```

## Limitations and Edge Cases

### When SHA Lookup Fails

If the branch was already deleted when the audit ran:
- SHA will be "already-deleted"
- Recovery not possible via this system
- Fall back to git reflog or GitHub PR archives

### SHA Garbage Collection

Git may garbage collect unreferenced commits after ~90 days:
- Recovery possible if SHA still exists
- Check with: `git cat-file -e <SHA>`
- May need to fetch from PR refs: `git fetch origin pull/123/head`

### Force-Pushed Branches

If a branch was force-pushed before deletion:
- Audit captures the final SHA only
- Previous SHAs not recorded
- May need reflog for intermediate states

## Troubleshooting

### "Branch not found in audit logs"

Possible causes:
1. Branch was deleted before audit system was implemented
2. Manual deletion without logging script
3. Deletion in different repository

**Solution:** Check git reflog or GitHub PR archives.

### "SHA not found in repository"

Possible causes:
1. Commit was garbage collected
2. Never fetched to local repository
3. From a fork that's deleted

**Solution:**
```bash
# Try fetching from PR ref
git fetch origin pull/<PR-number>/head

# Or if SHA is known
git fetch origin <SHA>
```

### Recovery Script Not Executable

```bash
chmod +x .github/scripts/log-branch-deletion.sh
chmod +x .github/scripts/recover-branch.sh
```

## Related Documentation

- [Branch Deletion Audit README](.github/branch-deletion-audit/README.md)
- [Branch Recovery Report](BRANCH_RECOVERY_REPORT.md)
- [Branch Lifecycle Workflow](.github/workflows/branch-lifecycle.yml)
- [AI Rapid Workflow](docs/workflows/AI_RAPID_WORKFLOW.md)

## Support

If you encounter issues with branch recovery:

1. Check the audit logs in `.github/branch-deletion-audit/`
2. Try the recovery script with verbose mode
3. Open an issue with:
   - Branch name
   - Approximate deletion date
   - PR number (if known)
   - Error messages from recovery attempts

## Contributing

To improve the branch recovery system:

1. Submit issues for edge cases not handled
2. Contribute enhanced recovery strategies
3. Add query examples to this documentation
4. Report false positives in SHA detection

---

**Remember:** The best recovery is prevention. Use `keep-alive` labels for important work, commit frequently, and review branches before deletion!
