# Branch Deletion Audit System

This directory contains audit logs for branch deletions, enabling recovery of
accidentally deleted branches.

## Purpose

When branches are deleted (via stale PR cleanup or merged branch cleanup), this
system captures:

- **Tip SHA**: The exact commit the branch pointed to before deletion
- **PR Reference**: Associated pull request number (if any)
- **Commit Details**: Last commit message and author
- **Deletion Context**: Why and when the branch was deleted

## Log Format

Logs are stored as JSONL (JSON Lines) files, one record per line:

```
.github/branch-deletion-audit/
├── 2026-01-deletions.jsonl
├── 2026-02-deletions.jsonl
└── ...
```

### Record Schema

```json
{
  "timestamp": "2026-01-23T12:00:00Z",
  "branch": "feature/my-branch",
  "tip_sha": "abc123def456...",
  "pr_number": "123",
  "commit_message": "feat: implement feature X",
  "commit_author": "user@example.com",
  "reason": "stale-pr-no-tasks|stale-pr-with-tasks|merged-branch",
  "deleted_by": "branch-lifecycle-workflow"
}
```

## Recovery Process

### Quick Recovery

```bash
# Find the branch in audit logs
.github/scripts/recover-branch.sh "feature/my-branch"

# Output shows tip SHA and recovery commands:
# git fetch origin abc123def456
# git branch feature/my-branch abc123def456
# git push origin feature/my-branch
```

### Manual Search

```bash
# Search all audit logs for a branch
grep "feature/my-branch" .github/branch-deletion-audit/*.jsonl

# Search by date range
grep "2026-01-2" .github/branch-deletion-audit/2026-01-deletions.jsonl
```

## Integration

The audit system is integrated into `.github/workflows/branch-lifecycle.yml`:

1. **Before stale PR closure** (with task extraction)
1. **Before stale PR closure** (without tasks)
1. **Before merged branch deletion**

Each deletion point calls `log-branch-deletion.sh` BEFORE the actual deletion.

## Retention

- Logs are retained indefinitely by default
- Consider archiving logs older than 1 year to `archive/branch-audit/`
- Never delete logs for branches that might need recovery

## Related Files

- [log-branch-deletion.sh](../scripts/log-branch-deletion.sh) - Logging script
- [recover-branch.sh](../scripts/recover-branch.sh) - Recovery script
- [branch-lifecycle.yml](../workflows/branch-lifecycle.yml) - Workflow
  integration
