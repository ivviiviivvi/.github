# Jules Cascade Prevention - Quick Reference

## TL;DR

**Problem:** Jules tasks were cascading, creating 10-100+ redundant PRs daily
**Solution:** Daily orchestrator + task deduplication + single consolidated PR

## Daily Workflow (Automated)

### 1:00 AM UTC - Master Orchestrator Runs

- ✅ Coordinates all daily tasks
- ✅ Deduplicates redundant work
- ✅ Processes task queue
- ✅ Triggers PR consolidation

### 1:30 AM UTC - PR Consolidator Runs

- ✅ Finds all bot/Jules PRs
- ✅ Merges into single branch
- ✅ Creates ONE consolidated PR
- ✅ Closes original PRs

### Your Morning - Review ONE PR

- ✅ Check consolidated PR
- ✅ Review checklist items
- ✅ Approve/reject each section
- ✅ Merge when ready

## Key Commands

### Manual Triggers

```bash
# Force run master orchestrator
gh workflow run daily-orchestrator.yml -f force_run=true

# Manually consolidate PRs
gh workflow run daily-pr-consolidator.yml

# Check task deduplication
python3 .github/scripts/task_deduplicator.py check "task_type" '{"data":"value"}'
```

### Monitoring

```bash
# View recent orchestrator runs
gh run list --workflow=daily-orchestrator.yml --limit 7

# View consolidated PRs
gh pr list --label consolidated

# Check task state
cat .github/task_state.json | jq '.'
```

## What Changed

### New Files

- `.github/workflows/daily-orchestrator.yml` - Main coordinator
- `.github/workflows/daily-pr-consolidator.yml` - PR consolidation
- `.github/scripts/task_deduplicator.py` - Deduplication engine
- `docs/JULES_CASCADE_PREVENTION.md` - Full documentation

### Updated Files

- `.github/workflows/jules.yml` - Added deduplication
- `.github/workflows/orchestrator.yml` - Added deduplication
- `.gitignore` - Exclude task_state.json

## How It Works

### Task Deduplication

1. Each task generates unique hash from type + data
1. Hash checked against recent tasks (24h window)
1. Duplicate tasks skipped with notification
1. Prevents cascade of redundant work

### PR Consolidation

1. Finds all PRs from bots/Jules/github-actions
1. Creates single consolidation branch
1. Merges all PRs (auto-resolves conflicts)
1. ONE PR with checklist for all changes
1. Closes original PRs with explanation

## Benefits

✅ **ONE PR per day** instead of 10-100\
✅ **No redundant tasks** - deduplication
prevents waste\
✅ **Simple checklist** - approve/reject items easily\
✅ **Clean
history** - no PR sprawl\
✅ **Auto cleanup** - old records removed daily

## Troubleshooting

### "Task already processed" message

**Normal** - deduplication working correctly. Wait 24h or contact maintainer if
urgent.

### Multiple orchestrations per day

Check `.github/task_state.json` for stale timestamps in `tasks` or an old
`last_orchestration`. Reset if corrupted:

```bash
echo '{"tasks":{},"active_prs":[],"last_orchestration":null,"last_cleanup":null}' > .github/task_state.json
```

### PRs not consolidating

1. Check PR authors (must be bot/Jules/github-actions)
1. Verify no "consolidated" label on PRs
1. Run manually: `gh workflow run daily-pr-consolidator.yml`

## Need Help?

📖 **Full docs:** `docs/JULES_CASCADE_PREVENTION.md`\
🔧 **Workflow logs:** GitHub
Actions tab\
💬 **Questions:** Create an issue

______________________________________________________________________

**Remember:** The system runs daily at 1 AM UTC. Check your repos each morning
for ONE consolidated PR to review!
