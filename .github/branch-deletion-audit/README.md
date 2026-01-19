# Branch Deletion Audit Log

This directory contains audit logs of all branch deletions, preserving critical metadata for recovery purposes.

## Purpose

When branches are deleted (automatically or manually), we preserve:
- Branch name
- Tip commit SHA (the most recent commit on the branch)
- PR number (if associated with a PR)
- Deletion timestamp
- Deletion reason
- Commit metadata (author, date, message, parents)

This prevents the data loss issue described in `BRANCH_RECOVERY_REPORT.md` where "the deletion list contains branch names only, not the tip commit SHAs."

## File Format

Audit logs are stored as JSON Lines (`.jsonl`) files, one per month:
```
YYYY-MM-deletions.jsonl
```

Each line is a complete JSON object with branch deletion metadata.

### Schema

```json
{
  "timestamp": "2026-01-19T23:45:00Z",
  "branch": "feature/my-branch",
  "tip_sha": "abc123def456...",
  "pr_number": "123",
  "pr_title": "Add new feature",
  "pr_url": "https://github.com/org/repo/pull/123",
  "pr_state": "CLOSED",
  "reason": "stale-pr-no-tasks",
  "commit_author": "John Doe <john@example.com>",
  "commit_date": "2026-01-18T10:30:00Z",
  "commit_message": "feat: implement feature X",
  "commit_parents": "parent1sha parent2sha",
  "deleted_by": "github-actions",
  "repository": "org/repo"
}
```

## Usage

### Logging a Deletion (Automatic)

The branch-lifecycle workflow automatically logs deletions:
```bash
./.github/scripts/log-branch-deletion.sh "$BRANCH" "$PR_NUMBER" "reason"
```

### Recovering a Branch

Use the recovery script:
```bash
./.github/scripts/recover-branch.sh "feature/my-branch"
```

This will:
1. Search audit logs for the branch
2. Display deletion metadata
3. Provide recovery commands with the exact SHA

### Manual Recovery Steps

If you know the SHA:
```bash
# Create branch from SHA
git fetch origin <SHA>
git branch <branch-name> <SHA>
git push origin <branch-name>

# Or cherry-pick the commit
git cherry-pick <SHA>

# Or create a patch
git format-patch -1 <SHA> -o /tmp/
```

## Retention Policy

- Audit logs are kept indefinitely in git history
- Monthly files help with organization and querying
- No automatic cleanup - all deletion records are preserved

## Why This Matters

From the BRANCH_RECOVERY_REPORT.md incident:

> The part that becomes illogical (or at least not fully possible)
> Here's the hard limit:
>
> The deletion list contains branch names only, not the tip commit SHAs.
> Once branches are deleted, we cannot reconstruct each branch's exact diff unless we also preserved:
> - tip SHAs (e.g., from git ls-remote --heads origin …),
> - PR refs (if they existed),
> - or patches/artifacts.

This audit system solves all three requirements:
- ✅ Preserves tip SHAs
- ✅ Preserves PR refs
- ✅ Enables patch recreation via SHA

## Integration Points

The audit logging is integrated into:
- `.github/workflows/branch-lifecycle.yml` - Stale PR management
- `.github/workflows/branch-lifecycle.yml` - Merged branch cleanup
- Any future branch deletion workflows

## Querying Logs

Since logs are JSONL, they're easy to query with standard tools:

```bash
# Find a specific branch
grep '"branch":"feature/my-branch"' .github/branch-deletion-audit/*.jsonl

# All deletions in a month
cat .github/branch-deletion-audit/2026-01.jsonl

# Pretty print a record
grep '"branch":"feature/my-branch"' .github/branch-deletion-audit/*.jsonl | jq '.'

# List all deleted branches
grep -h '"branch":' .github/branch-deletion-audit/*.jsonl | jq -r '.branch' | sort

# Find deletions by PR
grep '"pr_number":"123"' .github/branch-deletion-audit/*.jsonl

# Find deletions by reason
grep '"reason":"stale-pr' .github/branch-deletion-audit/*.jsonl
```

## Security Considerations

- Audit logs contain commit SHAs and metadata but no sensitive data
- All information is already available in git history
- Logs are committed to git and subject to repository permissions
- No secrets or credentials are stored in audit logs

## Future Enhancements

Potential improvements:
- Automatic SHA verification (check if SHA still exists in repo)
- Web dashboard for browsing deleted branches
- Automated recovery suggestions based on branch patterns
- Integration with PR lifecycle to tag "important" branches
- Periodic SHA existence verification report
