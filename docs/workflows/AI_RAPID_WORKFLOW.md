# AI-Accelerated Rapid Development Workflow

> **Optimized for Solo Developer + Multiple AI Assistants**
>
> Problem: Traditional PR workflows create bottlenecks when one developer works with multiple AI agents, generating working software in <24 hours but drowning in branch/PR management.
>
> Solution: Streamlined trunk-based development with intelligent automation.

---

## The Problem

**Traditional workflow:**
```
AI 1 creates feature A → Branch A → PR A → Review → Merge
AI 2 creates feature B → Branch B → PR B → Review → Merge
AI 3 creates feature C → Branch C → PR C → Review → Merge
...
Result: 10+ open PRs, lost tasks, merge bottleneck
```

**You are both author AND reviewer** - pure overhead when CI ensures quality.

---

## The Solution: Speed-Optimized Workflow

### Core Principles

1. **CI is the Gatekeeper** - If tests pass, ship it
2. **Short-lived Branches** - Max 48 hours from creation to merge
3. **Auto-merge by Default** - Manual review only for critical changes
4. **Task-first, PR-second** - Track work in issues/tasks, not PR backlogs
5. **Batch Related Work** - Merge dependent PRs together
6. **Ruthless Cleanup** - Auto-close stale branches

---

## Feature Scope: 1 Feature = 1 PR

**Golden Rule:**
- ✅ **1 feature per branch** → **1 PR per feature**
- Clean git history
- Easy to review
- Easy to rollback if issues
- Clear changelog

**Bad:**
```bash
# DON'T: Multiple features in one PR
git checkout -b feature/dashboard-and-api-and-auth
# Mixes 3 features - hard to review, hard to rollback
```

**Good:**
```bash
# DO: Separate PRs for each feature
git checkout -b feature/user-dashboard    # PR #1
git checkout -b feature/api-v2-endpoint  # PR #2
git checkout -b feature/oauth-login      # PR #3
# Each can be reviewed, merged, or rolled back independently
```

**Exception - Use batch merge for tightly coupled features:**
```bash
# If features MUST go together:
gh pr create --label "batch:api-v2" --title "feat: API v2 endpoint"
gh pr create --label "batch:api-v2" --title "feat: API v2 client"
gh pr create --label "batch:api-v2" --title "test: API v2 integration tests"
# Merges all 3 together
```

---

## Workflow Types

### 🚀 Burst Mode (Default for Rapid Development)

**When:** You're in active development with AI assistants creating features in rapid succession (hours, not days)

**Philosophy:** Ship fast, fix forward. If CI passes, it's good enough.

**Timeline:**
- **0-2h:** Feature development
- **Immediate:** Auto-merge when CI passes
- **12h:** Stale warning (if no merge/activity)
- **24h:** Auto-close + task extraction

#### Type 1: Most Features (90% of PRs in burst mode)

**Use for:** Bug fixes, docs, config, small-to-medium features, refactoring

```bash
# AI creates feature branch (1 feature = 1 branch)
git checkout -b feature/user-dashboard

# AI implements feature (2 hours)
# ... makes changes ...

# AI commits and creates PR
git commit -m "feat: add user dashboard"
git push -u origin feature/user-dashboard

gh pr create --title "feat: add user dashboard" \
  --body "User dashboard with analytics\n\nCloses #123" \
  --label "automerge:when-ci-passes"  # ← Ship it!

# ✅ Auto-merges in ~5-15 min when CI passes
```

**Lifecycle:**
- Created → CI runs (5-10 min) → ✅ Pass → Auto-merge → Branch deleted
- **Total time: 15 minutes - 2 hours**
- You review AFTER merge (async) for learning, not blocking

#### Type 2: Complex Features (10% of PRs in burst mode)

**Use for:** Breaking changes, security, architecture changes, multi-service updates

```bash
# AI creates feature branch
git checkout -b feature/major-refactor

# AI implements (may take 4-6 hours)
# ... makes changes ...

# Create PR for manual review
gh pr create --title "feat: major refactor" \
  --body "Detailed explanation of changes\n\nCloses #456" \
  --label "needs-review"  # ← Explicit approval required

# You review within 2-4 hours (same day)
gh pr review --approve
gh pr merge --squash
```

**Lifecycle:**
- Created → CI runs → Manual review (2-4h) → Approve → Merge
- **Total time: 4-8 hours same day**
- Still fast, but with your explicit approval

---

### 🐢 Normal Mode (Optional - Lower Velocity)

**When:** Not actively developing, maintenance mode, or want extra caution

**Timeline:**
- **24h:** Review window before auto-merge
- **48h:** Stale warning
- **72h:** Final warning
- **96h:** Auto-close + task extraction

**Use labels:**
```bash
gh pr create --label "automerge:after-review-period"  # Wait 24h
gh pr create --label "needs-review"                    # Manual approval
```

**Most solo dev + AI scenarios should use Burst Mode.**

---

## Auto-Merge Configuration

### Labels that Trigger Auto-Merge

**For Burst Mode (Recommended):**

| Label | Behavior | Use When | % of PRs |
|-------|----------|----------|----------|
| `automerge:when-ci-passes` | ⚡ Merges immediately when CI ✅ | 90% of PRs - all features unless complex | **90%** |
| `needs-review` | 🛑 Blocks auto-merge, requires approval | Complex/breaking/security changes | **10%** |
| `batch:<name>` | 🔗 Groups related PRs, merges together | Tightly coupled features | As needed |

**For Normal Mode (Lower velocity):**

| Label | Behavior | Use When |
|-------|----------|----------|
| `automerge:after-review-period` | ⏰ Waits 24h before merging | Want extra review time |
| `needs-review` | 🛑 Requires manual approval | Critical changes |

### How to Apply

**When creating PR:**
```bash
gh pr create --label "automerge:when-ci-passes"
```

**To existing PR:**
```bash
gh pr edit 123 --add-label "automerge:when-ci-passes"
```

**In PR description:**
```markdown
/automerge when-ci-passes
```

---

## Branch Lifecycle Management

### Automatic Cleanup

**🚀 Burst Mode Timeline (Default - for rapid development):**

| Age | Status | Action |
|-----|--------|--------|
| 0-12h | Active | No action - rapid development in progress |
| 12-24h | Warning | Bot comments: "⚠️ PR is 12h old, merge or update soon" |
| 24h+ | Stale | Auto-closes PR, deletes branch, extracts tasks to issue |

**Why so aggressive?**
- Burst development = features ship in hours
- If PR isn't merged in 12h during active development, something's wrong
- Forces fast feedback loop: ship it or close it
- No lingering PRs during active sprints

**🐢 Normal Mode Timeline (for lower-velocity periods):**

| Age | Status | Action |
|-----|--------|--------|
| 0-48h | Active | No action |
| 48-72h | Warning | Bot comments: "Branch is 2 days old, merge or close soon" |
| 72h+ | Final Warning | Bot comments: "Will auto-close in 24h unless updated" |
| 96h+ | Closed | Auto-closes PR, deletes branch, extracts tasks to issue |

**Configure mode:**
```bash
# Enable burst mode (default)
# PRs auto-close after 24h
# Set in .github/workflows/branch-lifecycle.yml: BURST_MODE: true

# Enable normal mode
# PRs auto-close after 96h
# Set in .github/workflows/branch-lifecycle.yml: BURST_MODE: false
```

**Override stale automation:**
```bash
# For work that genuinely needs >24h (rare in burst mode)
gh pr edit 123 --add-label "keep-alive"
```

---

## Task Tracking Integration

### Problem: Lost Tasks in Closed PRs

When PRs are abandoned, the work/tasks inside are lost.

### Solution: Automated Task Extraction

**Before closing a stale PR, automation:**

1. Scans PR description and comments for task lists
2. Extracts incomplete tasks
3. Creates a new issue: "Extracted tasks from PR #123"
4. Links back to original PR
5. Closes PR, deletes branch

**Example:**

PR #123 is stale with:
```markdown
- [x] Implement feature A
- [ ] Add tests for feature A
- [ ] Update docs
```

Automation creates Issue #124:
```markdown
# Extracted Tasks from PR #123

Original PR was closed due to inactivity. These tasks remain:

- [ ] Add tests for feature A (from PR #123)
- [ ] Update docs (from PR #123)

See original work: #123
```

---

## PR Task Catcher

### Problem: Tasks/Suggestions in Comments Get Lost

**Common scenario:**
- Reviewer leaves comment: "Must fix the SQL injection vulnerability here"
- Or: "TODO: Add error handling"
- Or: "- [ ] Add unit tests for this function"
- PR gets merged without addressing the comment
- Security issue or tech debt gets lost forever

### Solution: Automated Comment Scanning

The **PR Task Catcher** workflow continuously scans all PR comments for:

1. **Unchecked task items**: `- [ ] task`
2. **Blocker keywords**: "FIXME", "TODO", "Must fix", "Required", "Blocker", "Action item"
3. **Suggestions**: "suggest", "should", "could", "consider", "recommend"
4. **Unresolved review threads**

**Automatic actions:**
- Posts/updates a **Task Catcher Summary** comment showing all found items
- Adds labels: `has-blockers`, `has-pending-tasks`
- **Blocks merge** if blocker items are found (unless `ignore-task-checks` label is added)
- Creates issues for unresolved tasks when PR is merged (if `create-issues-for-tasks` label is present)

### How It Works

**Triggers:**
- When PR is opened
- When comments are added/edited
- When reviews are submitted
- When PR is ready for review

**Example Task Summary:**

```markdown
# 🚨 Task Catcher Summary

🚨 BLOCKERS FOUND - Address before merging

## 📋 Task Overview

| Category | Count |
|----------|-------|
| PR Body Unchecked Tasks | 2 |
| PR Body Checked Tasks | 3 ✅ |
| Comment Tasks | 1 |
| Blocker Items | 2 🚨 |
| Suggestions | 3 💡 |
| Unresolved Review Threads | 1 |

## 💬 Comment Tasks & Blockers

### 🚨 @reviewer1 - BLOCKER at auth.ts:42
Must fix the SQL injection vulnerability here

### 💡 @reviewer2 - Suggestion
Consider adding retry logic for API calls

## 🎯 Next Steps

- 🚨 Address all blocker items before merging
- ✅ Check off completed tasks in PR description
- 💬 Resolve review discussion threads

**Options:**
- ✅ Check off tasks as you complete them
- 📋 Create issues for tasks to handle later: Add `create-issues-for-tasks` label
- 🚫 Ignore tasks for merge: Add `ignore-task-checks` label
```

### Usage Patterns

**For AI Assistants:**

```bash
# When creating PR with known follow-up tasks
gh pr create \
  --title "feat: user authentication" \
  --body "Implements JWT authentication

## Tasks
- [x] Implement JWT signing
- [x] Add login endpoint
- [ ] Add refresh token logic  # Will do in next PR
- [ ] Add rate limiting       # Will do in next PR

Closes #123" \
  --label "automerge:when-ci-passes,create-issues-for-tasks"

# Result: PR merges, but 2 issues are auto-created for incomplete tasks
```

**For Reviewers:**

```markdown
# In PR comment:

🚨 **BLOCKER:** Must fix the SQL injection on line 42 before merging.

💡 **Suggestion:** Consider adding error handling for API timeout.

- [ ] Add unit tests for the new function
- [ ] Update API documentation
```

**Result:**
- Task Catcher finds 1 blocker, 1 suggestion, 2 tasks
- Adds `has-blockers` label
- Posts summary comment
- **Blocks merge** until blocker is addressed

**Resolving blockers:**

1. Fix the SQL injection
2. Update the comment or check off the task
3. Task Catcher re-scans (on next comment/push)
4. `has-blockers` label removed automatically
5. Merge proceeds

### Labels

| Label | Purpose | Auto-Added? |
|-------|---------|-------------|
| `has-blockers` | PR has unresolved blocker items | ✅ Yes |
| `has-pending-tasks` | PR has unchecked tasks | ✅ Yes |
| `ignore-task-checks` | Skip task blocking (not recommended) | ❌ Manual |
| `create-issues-for-tasks` | Create issues for incomplete tasks on merge | ❌ Manual |
| `task-from-pr` | Issue was created from PR task | ✅ Yes (on issues) |

### Benefits

**For solo dev + AI:**
- No reviewer feedback gets lost
- AI can leave tasks for you to review
- You can leave tasks for AI to implement
- Automatic accountability tracking

**Common workflow:**

```bash
# AI creates PR with known limitations
gh pr create --body "
Implements user dashboard.

## Known Limitations (for human review)
- [ ] Add mobile responsiveness
- [ ] Optimize database queries
- [ ] Add accessibility labels

Closes #123
" --label "automerge:when-ci-passes,create-issues-for-tasks"

# Result:
# - PR auto-merges (CI passes)
# - 3 issues auto-created for limitations
# - You can triage/assign later
```

### Disabling Task Catcher

**To bypass blocking:**
```bash
# If you really need to merge with blockers (emergency)
gh pr edit 123 --add-label "ignore-task-checks"
```

**To disable for a PR:**
The task catcher only blocks merge if blocker keywords are found. Regular unchecked tasks are informational only.

### Best Practices

**✅ DO:**
- Use blocker keywords sparingly (only for actual blockers)
- Check off tasks as you complete them
- Use `create-issues-for-tasks` label for follow-up work
- Resolve review threads to clear them from summary

**❌ DON'T:**
- Mark everything as "BLOCKER" (dilutes meaning)
- Ignore task summaries (defeats the purpose)
- Use `ignore-task-checks` routinely (defeats the purpose)

---

## Batch Merge Workflow

### Problem: Related PRs Create Merge Conflicts

```
PR #100: Update API endpoint
PR #101: Update API tests (depends on #100)
PR #102: Update API docs (depends on #100)

Merging #100 creates conflicts in #101 and #102
```

### Solution: Batch Merge Labels

**Mark PRs as related:**
```bash
gh pr edit 100 --add-label "batch:api-update"
gh pr edit 101 --add-label "batch:api-update"
gh pr edit 102 --add-label "batch:api-update"
```

**Automation:**
1. Waits for ALL PRs with `batch:api-update` to pass CI
2. Rebases them in dependency order
3. Merges all together
4. Deletes all branches

**Or manually trigger:**
```bash
# Comment on any PR in the batch
/merge-batch api-update
```

---

## Daily Workflow for Solo Dev + AI

### Morning (15 min)
```bash
# Check what AI agents accomplished overnight
gh pr list --label "automerge:when-ci-passes"

# Review auto-merged PRs (just awareness)
gh pr list --state merged --limit 10

# Check anything that needs your review
gh pr list --label "needs-review"

# Prioritize tasks for AI agents today
gh issue list --label "priority:high"
```

### During Day (Continuous)
```bash
# AI 1 works on task A → auto-merges when done
# AI 2 works on task B → auto-merges when done
# AI 3 works on task C → needs your review

# You work on core architecture
# You review complex PRs async (not blocking)
```

### Evening (15 min)
```bash
# Review what shipped today
gh pr list --state merged --search "merged:>=2024-01-15"

# Check for stale branches
gh pr list --label "stale"

# Plan tomorrow's AI tasks
gh issue create --title "Task for AI: implement X"
```

### Weekly (30 min)
```bash
# Batch close stale PRs
gh pr list --label "stale" --json number --jq '.[].number' | xargs -I {} gh pr close {}

# Review metrics
gh run list --workflow="repo-metrics.yml"

# Adjust automation based on patterns
```

---

## Feature Flags for Incomplete Work

### Problem: Feature not done but need to merge to reduce PR backlog

### Solution: Feature flags

```typescript
// Use feature flags for work-in-progress
const FEATURE_FLAGS = {
  NEW_DASHBOARD: process.env.ENABLE_NEW_DASHBOARD === 'true', // default: false
  API_V2: process.env.ENABLE_API_V2 === 'true',
};

// Merge incomplete features disabled by default
if (FEATURE_FLAGS.NEW_DASHBOARD) {
  return <NewDashboard />;
}
return <OldDashboard />;
```

**Benefits:**
- Merge early, merge often
- Reduce PR backlog
- Enable features when ready
- A/B test in production

---

## PR Size Guidelines

### Target Sizes for Fast Merge

| Size | Lines Changed | Merge Time | Auto-Merge? |
|------|---------------|------------|-------------|
| XS | <10 | <5 min | ✅ Yes |
| S | 10-99 | <15 min | ✅ Yes |
| M | 100-499 | <1 hour | ⚠️ Maybe |
| L | 500-999 | <4 hours | ❌ No |
| XL | 1000+ | Manual | ❌ No |

**If PR is L or XL:**
1. Break into smaller PRs
2. Use feature flags
3. Use draft PR for incremental work

---

## Handling CI Failures

### Auto-Merge Behavior on Failure

```
PR created with "automerge:when-ci-passes"
  ↓
CI starts running
  ↓
CI fails ❌
  ↓
Auto-merge: BLOCKED
  ↓
Bot comments: "Auto-merge blocked. Fix CI to proceed."
  ↓
AI or you fix the issue
  ↓
Push new commit
  ↓
CI re-runs
  ↓
CI passes ✅
  ↓
Auto-merge: EXECUTES
```

**No manual intervention needed if AI fixes CI failures**

---

## Migration from Current State

### Step 1: Triage Existing PRs (One-time, 1 hour)

```bash
# Get all open PRs
gh pr list --limit 100

# For each PR, decide:
# 1. Merge now → Add "automerge:when-ci-passes"
# 2. Needs work → Add "needs-review"
# 3. Obsolete → Close, extract tasks
# 4. Batch merge → Add "batch:<name>"

# Example:
gh pr edit 45 --add-label "automerge:when-ci-passes"
gh pr edit 46 --add-label "batch:api-refactor"
gh pr close 47 --comment "Obsolete, extracted tasks to #200"
```

### Step 2: Enable Auto-Merge Workflows (5 min)

```bash
# Workflows are already created in .github/workflows/
# Just enable branch protection to allow auto-merge

# Settings → Branches → Branch protection rules → develop
# ✅ Require status checks to pass
# ✅ Require branches to be up to date
# ✅ Allow auto-merge
```

### Step 3: Update AI Agent Instructions (10 min)

Add to your AI prompts:

```markdown
When creating PRs:
- For bug fixes, docs, small features: Add label "automerge:when-ci-passes"
- For standard features: Add label "automerge:after-24h"
- For complex changes: Add label "needs-review"
- Always link to related issue: "Closes #123"
- Keep PRs small (<500 lines if possible)
```

### Step 4: Adopt New Daily Routine (Ongoing)

See "Daily Workflow" section above.

---

## Metrics to Track

### Measure Success

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **PR Merge Time** | <2 hours for small PRs | `gh pr list --state merged` |
| **Open PR Count** | <10 at any time | `gh pr list | wc -l` |
| **Stale PR Count** | <5 | `gh pr list --label stale | wc -l` |
| **Auto-merge Rate** | >70% of PRs | Weekly metrics workflow |
| **CI Pass Rate** | >90% | GitHub Actions insights |
| **Time to Ship** | <24h from idea to production | Track issue → merge time |

### Weekly Review

```bash
# Run weekly report
gh run view --workflow="weekly-commit-report.yml"

# Check auto-merge stats
gh pr list --state merged --search "merged:>=2024-01-08" --label "automerge:when-ci-passes" | wc -l
```

---

## Guardrails (Safety Checks)

### What Auto-Merge Will NOT Do

❌ Merge if ANY CI check fails
❌ Merge PRs labeled `needs-review` without approval
❌ Merge PRs targeting `main` (only `develop`)
❌ Merge PRs with unresolved review comments
❌ Merge PRs with merge conflicts
❌ Bypass security scans (CodeQL, Semgrep)

### Required CI Checks (Must Pass for Auto-Merge)

✅ All tests pass
✅ Code coverage >80% (if configured)
✅ CodeQL security scan passes
✅ Semgrep security scan passes
✅ Link checker passes (for docs)
✅ Conventional commit format
✅ PR description >50 characters

---

## Troubleshooting

### Issue: Too many auto-merges, not enough review

**Solution:**
```bash
# Change default to 24h delay
# In PR template, change default label to:
automerge:after-24h
```

### Issue: AI creating merge conflicts

**Solution:**
```bash
# Use batch merge for related work
# AI should coordinate:
gh pr edit 100 --add-label "batch:feature-x"
gh pr edit 101 --add-label "batch:feature-x"
```

### Issue: Important changes merged too fast

**Solution:**
```bash
# For critical files, require review
# Add to .github/CODEOWNERS:
/config/* @your-username
/security/* @your-username
```

### Issue: Want to disable auto-merge temporarily

**Solution:**
```bash
# Add label to PRs:
gh pr edit <number> --add-label "hold"

# Automation will skip these
```

---

## Best Practices

### ✅ DO

- Use auto-merge for >70% of your PRs (bug fixes, docs, small features)
- Keep PRs small (<500 lines changed)
- Link PRs to issues (track work in issues, not PR backlogs)
- Review auto-merged PRs async (for learning, not blocking)
- Use feature flags for incomplete work
- Close stale PRs ruthlessly (extract tasks first)
- Use batch merge for dependent PRs
- Trust your CI pipeline

### ❌ DON'T

- Create PRs without linking to issues/tasks
- Let PRs live >72 hours without activity
- Create XL PRs (>1000 lines) - break them up
- Disable CI checks to "move faster" (CI IS your safety net)
- Accumulate >15 open PRs (if you do, batch merge or close)
- Review every auto-merged PR before it merges (waste of time)

---

## Summary

**Old Way:**
- AI creates PR → you manually review → you manually merge → repeat
- Result: 20+ open PRs, lost tasks, slow shipping

**New Way:**
- AI creates PR with `automerge` label → CI passes → auto-merges
- You review complex PRs async, auto-merge handles 70%+ of work
- Result: <10 open PRs, no lost tasks, ship in hours not days

**Key Insight:**
> As a solo developer with AI assistants, the traditional PR review process is **pure overhead**. Your CI pipeline is your code reviewer. Trust it, automate it, ship faster.

---

**See Also:**
- `.github/workflows/auto-merge.yml` - Auto-merge implementation
- `.github/workflows/branch-lifecycle.yml` - Branch cleanup automation
- `.github/workflows/pr-batch-merge.yml` - Batch merge workflow
- `.github/workflows/task-tracker-integration.yml` - Task extraction
- `GIT_WORKFLOW.md` - Git branching strategy
- `BEST_PRACTICES.md` - General best practices

**Last Updated:** 2025-11-18
