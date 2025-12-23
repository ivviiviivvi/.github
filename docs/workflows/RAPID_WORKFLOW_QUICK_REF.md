# AI Rapid Development - Quick Reference

> **For solo developers working with multiple AI assistants**
> Fast-track your PR workflow with intelligent automation

---

## 🚀 Quick Start

### Golden Rule: 1 Feature = 1 PR

```bash
# ✅ DO: One feature per branch/PR
git checkout -b feature/user-dashboard  # Single feature
gh pr create --label "automerge:when-ci-passes"

# ❌ DON'T: Multiple features in one PR
git checkout -b feature/dashboard-and-api-and-auth  # Bad!
```

### For AI Assistants Creating PRs (Burst Mode)

```bash
# 90% of PRs: Auto-merge immediately when CI passes
gh pr create \
  --title "feat: user dashboard" \
  --body "Description\n\nCloses #123" \
  --label "automerge:when-ci-passes"  # ← Default!

# 10% of PRs: Complex/breaking changes
gh pr create \
  --title "refactor: major architecture change" \
  --body "Detailed explanation" \
  --label "needs-review"  # ← Requires approval

# Related features that MUST go together
gh pr create --label "batch:api-v2" --title "feat: API endpoint"
gh pr create --label "batch:api-v2" --title "feat: API client"
gh pr create --label "batch:api-v2" --title "test: API tests"
# Trigger: /merge-batch api-v2
```

---

## 🏷️ Labels Quick Reference

**Burst Mode (Default):**

| Label | Effect | Use When | % of PRs |
|-------|--------|----------|----------|
| `automerge:when-ci-passes` | ⚡ Merges immediately when CI ✅ | **90% of PRs** - all features | **Default** |
| `needs-review` | 🛑 Blocks auto-merge, needs approval | Complex/breaking/security | 10% |
| `batch:<name>` | 🔗 Groups related PRs for batch merge | Tightly coupled features | As needed |
| `keep-alive` | ♾️ Prevents stale closure | Rare - work needs >24h | Rare |
| `hold` | ⏸️ Temporarily blocks merge | Need to pause | As needed |
| `do-not-extract-tasks` | 🚫 Skip task extraction on close | Obsolete/test PRs | As needed |

**Normal Mode (Lower velocity):**

| Label | Effect |
|-------|--------|
| `automerge:after-review-period` | ⏰ Waits 24h before merge |

---

## ⏱️ PR Lifecycle Timeline

### 🚀 Burst Mode (Default - for rapid development)

```
0h    PR Created → CI runs
      ↓
      ✅ CI passes + "automerge:when-ci-passes" → MERGED
      (Total time: 15 min - 2 hours)
      ↓
      OR if not merged...
      ↓
12h   ⚠️  Stale warning (ship it or close it!)
      ↓
24h   🔒 Auto-closed + task extraction
```

### 🐢 Normal Mode (for lower-velocity periods)

```
0h    PR Created
      ↓
24h   "automerge:after-review-period" → MERGED
      OR wait for manual merge...
      ↓
48h   ⚠️  Stale warning
      ↓
72h   🚨 Final warning
      ↓
96h   🔒 Auto-closed + task extraction
```

**Switch modes:** Edit `BURST_MODE` in `.github/workflows/branch-lifecycle.yml`

---

## 💬 Comment Commands

| Command | Action | Where |
|---------|--------|-------|
| `/merge-batch api-update` | Trigger batch merge | Any PR in batch |
| `/automerge` | Enable auto-merge | Any open PR |

---

## 🎯 PR Task Catcher (NEW)

**Automatically scans PR comments for tasks/suggestions that need action**

### What It Catches

- ✅ Unchecked tasks: `- [ ] task`
- 🚨 Blockers: "FIXME", "TODO", "Must fix", "Blocker"
- 💡 Suggestions: "suggest", "should", "consider"
- 💬 Unresolved review threads

### Automatic Actions

- Posts **Task Summary** comment (auto-updates)
- Adds labels: `has-blockers`, `has-pending-tasks`
- **Blocks merge** if blocker keywords found
- Creates issues for tasks (if `create-issues-for-tasks` label present)

### Usage

```bash
# AI creates PR with known follow-up tasks
gh pr create \
  --body "## Tasks
- [x] Implement feature
- [ ] Add tests (later)
- [ ] Update docs (later)" \
  --label "automerge:when-ci-passes,create-issues-for-tasks"

# Result: PR merges, 2 issues created for incomplete tasks
```

**Reviewer leaves blocker:**
```markdown
🚨 BLOCKER: Must fix SQL injection on line 42
```

**Result:**
- `has-blockers` label added
- Merge blocked until addressed
- Task summary updated

### Task Catcher Labels

| Label | Auto? | Purpose |
|-------|-------|---------|
| `has-blockers` | ✅ | Unresolved blocker items |
| `has-pending-tasks` | ✅ | Unchecked tasks exist |
| `create-issues-for-tasks` | ❌ | Create issues on merge |
| `ignore-task-checks` | ❌ | Bypass blocking (emergency) |

---

## 📊 Daily Dashboard (15 min/day)

### Morning
```bash
# What auto-merged overnight?
gh pr list --state merged --search "merged:>=yesterday"

# What needs your review?
gh pr list --label "needs-review"

# Any stale warnings?
gh pr list --label "stale:warning"

# Open PR count (keep <10)
gh pr list | wc -l
```

### Evening
```bash
# Today's velocity
gh pr list --state merged --search "merged:>=today"

# Clean up stale PRs
gh pr list --label "stale:final-warning"
```

---

## 🎯 Target Metrics

| Metric | Target | Check With |
|--------|--------|------------|
| Open PRs | <10 | `gh pr list \| wc -l` |
| PR merge time | <2h | Auto-merged PRs |
| Stale PRs | <5 | `gh pr list --label stale` |
| Auto-merge rate | >70% | Weekly report |

---

## 🚦 Decision Tree

```
New PR needed?
  ↓
Is it quick (<2h) and low-risk?
  YES → automerge:when-ci-passes ⚡
  NO ↓
Is it related to open PRs?
  YES → batch:<name> 🔗
  NO ↓
Is it standard feature?
  YES → automerge:after-24h ⏰
  NO ↓
Is it complex/critical?
  YES → needs-review 🛑
```

---

## 🔥 Common Scenarios

### Scenario 1: 10+ Open PRs (Overwhelmed)

**Solution: Batch Close/Merge**

```bash
# Find old PRs
gh pr list --json number,createdAt | jq -r '.[] | select(.createdAt < "2024-01-10") | .number'

# Review each:
# - Obsolete? Close manually
# - Ready? Add automerge:when-ci-passes
# - Related? Add batch:<name>

# Example:
gh pr edit 45 --add-label "automerge:when-ci-passes"
gh pr edit 46 47 48 --add-label "batch:feature-x"
gh pr close 49 --comment "Obsolete work"
```

### Scenario 2: Related PRs Creating Conflicts

**Solution: Batch Merge**

```bash
# Label all related PRs
gh pr edit 100 101 102 --add-label "batch:api-update"

# Wait for all to pass CI, then:
# Comment on any PR: /merge-batch api-update

# Or manually trigger:
# Actions → Batch Merge → Run → Enter: batch:api-update
```

### Scenario 3: Important Change Merged Too Fast

**Solution: Post-Merge Review**

```bash
# Review what auto-merged
gh pr view 123

# If issue found, create fix PR or revert
gh pr comment 123 --body "Found issue: <explanation>"
git revert <commit>
```

### Scenario 4: Feature Not Done But Need to Reduce PR Backlog

**Solution: Feature Flags**

```typescript
// Merge with feature disabled
const FEATURE_FLAGS = {
  NEW_DASHBOARD: false,  // Not ready yet
};

if (FEATURE_FLAGS.NEW_DASHBOARD) {
  return <NewDashboard />;
}
```

```bash
# Label and merge
gh pr edit 150 --add-label "automerge:when-ci-passes"
```

---

## ⚙️ Configuration Changes

### Enable Auto-Merge in Repo Settings

1. Settings → General → Pull Requests
2. ✅ Allow auto-merge
3. ✅ Automatically delete head branches

### Update Branch Protection (Optional)

Settings → Branches → Add rule for `develop`:
- ✅ Require status checks: `CodeQL`, `Semgrep`, `Tests`
- ✅ Require branches up to date
- ⬜ Require pull request reviews (optional for solo dev)

### Create Labels

```bash
# Auto-merge labels
gh label create "automerge:when-ci-passes" --color "0E8A16" --description "Auto-merge when CI passes"
gh label create "automerge:after-24h" --color "1D76DB" --description "Auto-merge 24h after creation"
gh label create "automerge:batch" --color "5319E7" --description "Batch merge with related PRs"

# Stale labels
gh label create "stale:warning" --color "FEF2C0" --description "PR inactive 48+ hours"
gh label create "stale:final-warning" --color "FF9800" --description "PR will be closed soon"

# Control labels
gh label create "keep-alive" --color "006B75" --description "Prevent stale auto-closure"
gh label create "hold" --color "D93F0B" --description "Temporarily block merge"
gh label create "do-not-extract-tasks" --color "E99695" --description "Skip task extraction"

# Task labels
gh label create "extracted-tasks" --color "C5DEF5" --description "Tasks extracted from closed PR"
gh label create "needs-triage" --color "FBCA04" --description "Needs review and prioritization"
```

---

## 🆘 Troubleshooting

### Auto-merge not working?

```bash
# Check PR details
gh pr view 123

# Requirements:
# ✅ Not a draft
# ✅ CI all passed
# ✅ No merge conflicts
# ✅ Has automerge:* label
# ✅ No 'hold' or 'needs-review' label (unless approved)

# Manual trigger:
gh pr merge 123 --auto --squash
```

### Too many stale PRs?

```bash
# Find all stale
gh pr list --label "stale:warning,stale:final-warning"

# Batch decision:
for pr in $(gh pr list --label stale --json number -q '.[].number'); do
  echo "PR #$pr"
  gh pr view $pr
  read -p "Action? (m=merge, c=close, k=keep, s=skip): " action
  case $action in
    m) gh pr edit $pr --add-label "automerge:when-ci-passes" ;;
    c) gh pr close $pr ;;
    k) gh pr edit $pr --add-label "keep-alive" ;;
    *) echo "Skipped" ;;
  esac
done
```

### Lost track of tasks?

```bash
# Find extracted task issues
gh issue list --label "extracted-tasks"

# Manually extract from old PR
gh workflow run task-extraction.yml -f pr_number=123
```

---

## 📚 Related Docs

- **Full Guide**: `AI_RAPID_WORKFLOW.md`
- **Git Workflow**: `GIT_WORKFLOW.md`
- **Best Practices**: `BEST_PRACTICES.md`
- **CLAUDE.md**: Main AI assistant guide

---

## 🎓 Philosophy

> **For solo dev + AI:**
> - CI is your code reviewer
> - PRs are a means to ship, not a process to follow
> - Speed > bureaucracy (but quality via automation)
> - Track work in issues, not PR backlogs
> - Merge often, ship fast, fix forward

---

**Last Updated:** 2025-11-18
**Version:** 1.0.0
