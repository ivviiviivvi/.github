# Jules Task Cascade Prevention & Daily PR Consolidation

## Overview

This system prevents cascading/redundant Jules tasks and consolidates all
automated PRs into a single daily PR for streamlined review and approval.

## Problem Solved

**Before:**

- Multiple daily workflows running independently creating 10-100+ redundant
  tasks
- Jules tasks cascading without deduplication
- Dozens of automated PRs from bots/Jules cluttering the repository
- Difficult to manage and review all the separate PRs
- Massive cleanup required daily

**After:**

- ✅ Single daily orchestrator coordinates all tasks
- ✅ Task deduplication prevents redundant work
- ✅ All bot/Jules PRs consolidated into ONE daily PR
- ✅ Simple checklist for approval/rejection
- ✅ Automated cleanup of old records

## Architecture

### 1. Daily Master Orchestrator

**File:** `.github/workflows/daily-master-orchestrator.yml`

**Schedule:** Daily at 1 AM UTC

**Workflow:**

1. Checks if already ran today (prevents multiple runs)
1. Orchestrates daily tasks with deduplication
1. Processes task queue
1. Waits for tasks to complete (30 minutes)
1. Triggers PR consolidation
1. Cleans up old task records

### 2. Task Deduplication System

**File:** `.github/scripts/task_deduplicator.py`

**Features:**

- Generates unique hash for each task based on type and data
- Tracks processed tasks in `.github/task_state.json`
- Prevents duplicate task execution within 24-hour window
- Registers PRs created by tasks
- Automatic cleanup of old records (7-day retention)

**Usage:**

```bash
# Check if task should be processed
python3 .github/scripts/task_deduplicator.py check "task_type" '{"key":"value"}'

# Register a PR for a task
python3 .github/scripts/task_deduplicator.py register_pr <pr_number> "task_type" '{"key":"value"}'

# Get active PRs for consolidation
python3 .github/scripts/task_deduplicator.py get_active_prs [max_age_hours]

# Cleanup old records
python3 .github/scripts/task_deduplicator.py cleanup [retention_days]
```

### 3. Daily PR Consolidator

**File:** `.github/workflows/daily-pr-consolidator.yml`

**Trigger:** Called by master orchestrator or manually

**Process:**

1. Identifies all open PRs from bots/Jules/github-actions
1. Creates single consolidation branch
1. Merges all PRs into consolidation branch
1. Auto-resolves conflicts using "theirs" strategy
1. Creates ONE consolidated PR with checklist
1. Closes all original PRs with explanation
1. Consolidated PR proceeds through CI/CD

**Result:** Just ONE PR to review instead of dozens!

### 4. Updated Workflows

#### Jules Workflow

**Changes:**

- Added deduplication check before processing
- Notifies users when duplicate requests are skipped
- Prevents cascade of redundant tasks

#### Orchestrator Workflow

**Changes:**

- Added deduplication for scheduled tasks
- Checks task hash before dispatching
- Skips recently processed tasks

## Daily Workflow

### Morning (1:00 AM UTC)

1. **Master Orchestrator runs:**
   - Checks if already ran today ✅
   - Orchestrates scheduled daily tasks with deduplication ✅
   - Processes queued tasks ✅

### Morning (1:30 AM UTC)

2. **PR Consolidation runs:**
   - Finds all bot/Jules PRs ✅
   - Creates single consolidated PR ✅
   - Closes original PRs ✅

### Morning (Check your repos)

3. **You review ONE PR:**
   - Review consolidated PR with checklist ✅
   - Check/uncheck items as you approve/reject ✅
   - Merge when ready ✅
   - Done! ✅

## State Management

### Task State File

**Location:** `.github/task_state.json`

**Structure:**

```json
{
  "processed_tasks": {
    "task_hash": "2024-01-09T01:00:00",
    ...
  },
  "active_prs": [
    {
      "pr_number": 123,
      "task_type": "jules_issue",
      "task_hash": "abc123",
      "created_at": "2024-01-09T01:00:00"
    }
  ],
  "last_orchestration": "2024-01-09",
  "last_cleanup": "2024-01-09T01:00:00"
}
```

**Managed by:** Task deduplicator script **Retention:** 7 days (configurable)
**Cleanup:** Automatic daily

## Configuration

### Deduplication Window

Default: 24 hours

To change, update calls to `should_process_task()`:

```python
deduplicator.should_process_task(task_type, task_data, dedupe_window_hours=48)
```

### Retention Period

Default: 7 days

To change cleanup retention:

```bash
python3 .github/scripts/task_deduplicator.py cleanup 14  # 14 days
```

### Consolidation Schedule

Default: Daily at 1:00 AM UTC

To change, edit `.github/workflows/daily-master-orchestrator.yml`:

```yaml
schedule:
  - cron: "0 3 * * *" # 3 AM UTC
```

## Manual Operations

### Force Master Orchestrator Run

```bash
gh workflow run daily-master-orchestrator.yml -f force_run=true
```

### Manually Consolidate PRs

```bash
gh workflow run daily-pr-consolidator.yml
```

### Check Task Deduplication Status

```bash
python3 .github/scripts/task_deduplicator.py check "jules_issue" '{"issue":"123"}'
```

### Cleanup Task State

```bash
python3 .github/scripts/task_deduplicator.py cleanup 7
```

## Troubleshooting

### Multiple Orchestrations Running

**Symptom:** Master orchestrator runs multiple times per day

**Solution:** Check `task_state.json` for `last_orchestration` date. The
workflow has a guard to prevent this, but if state file is corrupted, reset it:

```bash
echo '{"processed_tasks":{},"active_prs":[],"last_orchestration":null}' > .github/task_state.json
```

### Tasks Not Being Deduplicated

**Symptom:** Same task runs multiple times

**Solution:**

1. Check task hash generation is consistent
1. Verify `task_state.json` is being committed
1. Check deduplication window (may need to increase)

### PRs Not Being Consolidated

**Symptom:** Multiple PRs remain open after consolidation

**Solution:**

1. Check PR author filters in consolidator workflow
1. Verify PRs don't have "consolidated" label
1. Run consolidator manually: `gh workflow run daily-pr-consolidator.yml`

### Consolidation Merge Conflicts

**Symptom:** Consolidated PR has conflicts

**Solution:**

1. Review the "merge-details" section in consolidated PR
1. Conflicts are auto-resolved using "theirs" strategy
1. Manual review recommended for conflict PRs
1. Original PRs listed in consolidated PR for reference

## Benefits

### For Repository Maintainers

- ✅ **One PR per day** instead of 10-100
- ✅ **No redundant tasks** - deduplication prevents waste
- ✅ **Simple checklist** for approvals
- ✅ **Clean PR history** - no sprawl
- ✅ **Automated cleanup** - no manual maintenance

### For CI/CD

- ✅ **Fewer CI runs** - one consolidated PR
- ✅ **Faster feedback** - all checks in one place
- ✅ **Resource efficient** - no redundant builds

### For Users

- ✅ **Clear status** - one place to check progress
- ✅ **Fast notifications** - duplicate requests immediately notified
- ✅ **Predictable workflow** - daily consolidation schedule

## Migration Guide

### From Old System

1. Deploy new workflows
1. Let master orchestrator run once
1. Verify task state file created
1. Monitor consolidation on first run
1. Review and merge consolidated PR
1. Confirm old PRs are closed

### Rollback Plan

If issues occur:

1. Disable `daily-master-orchestrator.yml`
1. Disable `daily-pr-consolidator.yml`
1. Remove deduplication checks from `jules.yml` and `orchestrator.yml`
1. Delete `task_state.json`
1. Individual workflows continue as before

## Monitoring

### Check Daily Status

```bash
# View master orchestrator runs
gh run list --workflow=daily-master-orchestrator.yml --limit 7

# View consolidation runs
gh run list --workflow=daily-pr-consolidator.yml --limit 7

# View consolidated PRs
gh pr list --label consolidated
```

### Task Deduplication Stats

```bash
# Count processed tasks
jq '.processed_tasks | length' .github/task_state.json

# Count active PRs
jq '.active_prs | length' .github/task_state.json

# Last orchestration date
jq -r '.last_orchestration' .github/task_state.json
```

## Best Practices

1. **Review consolidated PR daily** - don't let them pile up
1. **Check task state weekly** - ensure deduplication working
1. **Monitor for conflicts** - review auto-resolved merges
1. **Adjust schedules** - optimize for your timezone
1. **Keep state file** - don't delete `task_state.json`
1. **Test changes** - use manual triggers to test workflows

## Support

For issues or questions:

1. Check this documentation
1. Review workflow run logs
1. Check `task_state.json` for state issues
1. Create an issue with logs and context

## Future Enhancements

Potential improvements:

- [ ] Web dashboard for task state
- [ ] Slack/email notifications for consolidated PR
- [ ] Smart conflict resolution based on file types
- [ ] PR grouping by feature/category
- [ ] Customizable consolidation rules
- [ ] Integration with project boards
