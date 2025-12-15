# Logical Branch Policy: "Main Only" Model

Comprehensive policy and implementation guide for maintaining a single-main-branch repository model with strict branch hygiene and lifecycle management.

## Table of Contents

- [Executive Summary](#executive-summary)
- [Scope and Rationale](#scope-and-rationale)
- [Policy Rules](#policy-rules)
  - [Branch Creation Rules](#branch-creation-rules)
  - [Branch Merge Rules](#branch-merge-rules)
  - [Branch Review Rules](#branch-review-rules)
  - [Branch Lifecycle Rules](#branch-lifecycle-rules)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Branch Inventory and Classification](#branch-inventory-and-classification)
- [Execution Plan: Branch Cleanup](#execution-plan-branch-cleanup)
- [Deliverables and Artifacts](#deliverables-and-artifacts)
- [GitHub CLI Reference](#github-cli-reference)
- [GitHub UI Guidance](#github-ui-guidance)
- [Enforcement and Automation](#enforcement-and-automation)
- [Best Practices and Reminders](#best-practices-and-reminders)
- [Security Considerations](#security-considerations)
- [Related Documentation](#related-documentation)

---

## Executive Summary

**Purpose**: This policy establishes a "main only" branch model where all development work flows through short-lived feature branches that merge directly into the main branch. This approach maximizes simplicity, reduces merge conflicts, and ensures production-ready code is always deployable.

**Key Principles**:
1. **One permanent branch**: `main` (or `master`) is the only long-lived branch
2. **Short-lived feature branches**: Created from `main`, merged back to `main`, then deleted
3. **No develop branch**: Direct integration into `main` with proper CI/CD gates
4. **Continuous deployment**: Every merge to `main` represents a potential production release
5. **Strict hygiene**: All branches are classified, audited, and either merged or deleted

---

## Scope and Rationale

### Scope

This policy applies to:
- ✅ All repositories adopting the "main only" model
- ✅ All contributors, maintainers, and automated systems
- ✅ All branches: existing, new, and archived
- ✅ All merge operations into the main branch
- ✅ All CI/CD workflows and deployment pipelines

### Rationale

#### Why "Main Only"?

**Traditional Git Flow Problems**:
```
main ─── develop ─── feature/A
                 └── feature/B
                 └── feature/C
```

- ❌ Double merge overhead (feature→develop, develop→main)
- ❌ `develop` branch becomes integration bottleneck
- ❌ Confusion about what's in production vs. staging
- ❌ Merge conflicts accumulate in `develop`
- ❌ Release branch ceremony adds complexity

**Main Only Flow Benefits**:
```
main ─── feature/A (PR → merge → delete)
     └── feature/B (PR → merge → delete)
     └── feature/C (PR → merge → delete)
```

- ✅ Single source of truth: `main` is always production-ready
- ✅ Reduced merge overhead: one merge per feature
- ✅ Simplified CI/CD: deploy directly from `main`
- ✅ Faster feedback: features reach production quickly
- ✅ Easier rollback: tag-based or commit-based rollback
- ✅ Clear branch lifecycle: create, work, merge, delete

#### When to Use This Model

**Ideal For**:
- 🎯 Microservices and small-to-medium services
- 🎯 Continuous deployment environments
- 🎯 Trunk-based development teams
- 🎯 Projects with strong CI/CD and feature flags
- 🎯 Teams practicing test-driven development
- 🎯 Infrastructure-as-code repositories
- 🎯 Documentation and configuration repos

**Not Ideal For**:
- ⚠️ Projects requiring long-term support for multiple versions (use maintenance branches)
- ⚠️ Large monoliths with complex release cycles (consider release branches)
- ⚠️ Open-source projects with irregular release schedules

---

## Policy Rules

### Branch Creation Rules

#### Rule 1.1: One Permanent Branch
- **Only `main` (or `master`) is permanent**
- The main branch represents production-ready code at all times
- No other long-lived branches are permitted (e.g., no `develop`, `staging`, `qa`)
- **Exception**: Temporary maintenance branches for critical patches (must be documented and time-limited)

#### Rule 1.2: Feature Branches Must Originate from Main
```bash
# ✅ CORRECT
git checkout main
git pull origin main
git checkout -b feature/user-authentication

# ❌ INCORRECT
git checkout some-other-branch
git checkout -b feature/user-authentication
```

#### Rule 1.3: Short-Lived Branches Only
- Maximum lifetime: **7 days** (preferred: 1-3 days)
- Branches older than 7 days require justification and approval
- Stale branches (14+ days) are automatically flagged for cleanup

#### Rule 1.4: One Purpose Per Branch
- One feature, one bug fix, one refactor per branch
- No mixing multiple unrelated changes
- Use separate branches for independent changes

---

### Branch Merge Rules

#### Rule 2.1: All Merges Require Pull Requests
```yaml
# ❌ NEVER
git checkout main
git merge feature/my-feature  # Direct merge forbidden

# ✅ ALWAYS
# Create PR via GitHub UI or CLI
gh pr create --base main --head feature/my-feature
```

#### Rule 2.2: Merge Requirements Checklist
Before merging to `main`, **ALL** of the following must pass:

- [ ] **CI Checks**: All automated tests pass (unit, integration, E2E)
- [ ] **Code Review**: At least one approval from a maintainer or CODEOWNER
- [ ] **Security Scan**: No critical or high vulnerabilities introduced
- [ ] **Branch Status**: Branch is up-to-date with `main` (rebased or merged)
- [ ] **Conventional Commits**: Commit messages follow project standards
- [ ] **Breaking Changes**: Documented if applicable (CHANGELOG, migration notes)
- [ ] **Feature Flags**: Risky changes protected by feature flags or rollback plan
- [ ] **Documentation**: Updated if behavior changes (README, API docs)

#### Rule 2.3: Merge Strategy
**Default Strategy**: Squash and Merge
```bash
# Rationale: Clean linear history on main
# All commits from feature branch are squashed into a single commit
```

**Alternative Strategies**:
- **Merge Commit (`--no-ff`)**: For complex features requiring preserved history (requires approval)
- **Rebase and Merge**: For single-commit branches only

**Selection Criteria**:
| Scenario | Strategy | Reason |
|----------|----------|--------|
| Single feature branch with multiple WIP commits | Squash | Clean history |
| Hotfix with single commit | Rebase | Linear history |
| Complex multi-component feature | Merge Commit | Preserve context |
| Documentation updates | Squash | Simplicity |

#### Rule 2.4: Post-Merge Actions
Immediately after merging:
1. **Tag if Release**: If this merge represents a release, tag it: `git tag -a v1.2.3 -m "Release 1.2.3"`
2. **Delete Branch**: Remove the merged feature branch (automated via GitHub settings or manual)
3. **Notify Team**: CI/CD system notifies relevant channels (Slack, Teams, email)
4. **Verify Deploy**: Monitor production metrics for regressions

---

### Branch Review Rules

#### Rule 3.1: Mandatory Code Review
- **Minimum Reviewers**: 1 for standard features, 2+ for critical changes
- **Reviewer Qualifications**: Must be familiar with the affected codebase
- **Review Scope**: Code quality, security, tests, documentation, performance

#### Rule 3.2: Review Response Time
- **Standard PRs**: Review within 24 hours (business days)
- **Hotfixes**: Review within 2 hours
- **Documentation**: Review within 48 hours

#### Rule 3.3: Review Checklist
Reviewers must verify:
- [ ] Code follows project style guidelines (linting passes)
- [ ] Tests are comprehensive and cover edge cases
- [ ] No security vulnerabilities (secrets, XSS, SQL injection)
- [ ] Performance impact is acceptable (no N+1 queries, memory leaks)
- [ ] Breaking changes are clearly documented
- [ ] Error handling is robust
- [ ] Logging is appropriate (no sensitive data logged)
- [ ] Dependencies are justified and secure (see `SECURITY.md`)

#### Rule 3.4: Resolving Review Feedback
- **All comments must be addressed** before merge
- **"Resolved" is not enough**: Author must reply explaining the fix or rationale
- **Disagreements**: Escalate to team lead or architect; document decision

---

### Branch Lifecycle Rules

#### Rule 4.1: Branch Lifecycle States
Every branch exists in one of these states:

```
┌──────────┐
│  CREATED │ → Active development
└────┬─────┘
     │
     ↓
┌──────────┐
│  ACTIVE  │ → Work in progress, frequent commits
└────┬─────┘
     │
     ↓
┌──────────┐
│ PR OPEN  │ → Under review
└────┬─────┘
     │
     ├─→ MERGED → Integrated into main → DELETED
     │
     └─→ STALE → No activity 14+ days → FLAGGED → ARCHIVED or DELETED
```

#### Rule 4.2: Deletion Policy
**Automatic Deletion**:
- Merged branches are automatically deleted via GitHub settings (`Automatically delete head branches`)
- Enable this setting: `Settings → General → Pull Requests → Automatically delete head branches`

**Manual Deletion**:
```bash
# After merging PR #123
git branch -d feature/my-feature           # Delete local branch
git push origin --delete feature/my-feature # Delete remote branch

# Or use GitHub CLI
gh pr close 123 --delete-branch
```

**When NOT to Delete**:
- ⚠️ Branches under active development (still in ACTIVE state)
- ⚠️ Branches with open PRs (still in PR OPEN state)
- ⚠️ Archive branches (prefixed with `archive/`, see Rule 4.3)

#### Rule 4.3: Archival Policy
**When to Archive Instead of Delete**:
- Historical reference needed (e.g., experimental POCs)
- Legal or compliance requirements
- Complex work that may be revisited

**Archive Process**:
```bash
# Rename to archive prefix
git branch -m old-feature archive/2024-12-old-feature-experiment
git push origin archive/2024-12-old-feature-experiment
git push origin --delete old-feature

# Add archive documentation
git checkout archive/2024-12-old-feature-experiment
cat > ARCHIVE_README.md << 'EOF'
# Archive Notice

**Branch**: archive/2024-12-old-feature-experiment
**Date Archived**: 2024-12-15
**Original Author**: @username
**Reason**: Experimental feature was not adopted; superseded by feature/new-approach

## Context
This branch explored a machine learning approach to user recommendation.
After evaluation, the team decided the rule-based approach was more maintainable.

## Replacement
See: feature/rule-based-recommendations (merged to main, v2.3.0)

**Note**: This branch is for historical reference only. Do not merge or modify.
EOF

git add ARCHIVE_README.md
git commit -m "docs: add archive documentation"
git push
```

#### Rule 4.4: Stale Branch Handling
**Stale Branch Definition**: No commits or activity for 14+ days

**Detection**:
```bash
# List stale branches (14+ days old)
git for-each-ref --sort=-committerdate refs/remotes/origin/ \
  --format='%(committerdate:short) %(refname:short)' | \
  awk -v date="$(date -d '14 days ago' +%Y-%m-%d)" '$1 < date'
```

**Action Plan**:
1. **Week 1 (Day 14)**: Automated notification to branch owner
   - Message: "Your branch `feature/X` has been inactive for 14 days. Please update or close."
2. **Week 2 (Day 21)**: Escalation to team lead
   - Review branch with team lead: Merge, Archive, or Delete?
3. **Week 3 (Day 28)**: Final action
   - If no response: Archive (if valuable) or Delete (if not)

---

## Branch Naming Conventions

### Standard Format
```
<type>/<short-description>
```

### Valid Types
| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New feature or enhancement | `feature/oauth-login` |
| `fix/` | Bug fix | `fix/login-timeout` |
| `hotfix/` | Critical production fix | `hotfix/security-patch` |
| `refactor/` | Code restructuring | `refactor/api-client` |
| `docs/` | Documentation only | `docs/api-guide` |
| `test/` | Test additions or fixes | `test/integration-suite` |
| `chore/` | Build, config, dependencies | `chore/update-deps` |
| `perf/` | Performance improvement | `perf/cache-layer` |
| `archive/` | Archived branches | `archive/2024-12-old-feature` |

### Naming Guidelines
- **Use lowercase and hyphens**: `feature/user-auth` ✅ not `Feature/User_Auth` ❌
- **Be descriptive**: `feature/oauth-google-login` ✅ not `feature/update` ❌
- **Include ticket/issue number if applicable**: `fix/GH-456-login-error` ✅
- **Keep it short**: Max 50 characters
- **No special characters**: Avoid `/` (except type separator), `@`, `#`, `$`

### Examples
```bash
# ✅ GOOD
feature/user-authentication
fix/gh-789-null-pointer-exception
hotfix/cve-2024-1234-security-patch
refactor/database-connection-pool
docs/installation-guide
chore/upgrade-node-20
archive/2024-12-experimental-blockchain

# ❌ BAD
feature/Update
Fix
user_authentication
feature/add-new-feature-for-users-to-login-with-oauth
main-backup  # Don't create alternate main branches!
```

### Reserved Names (Do NOT Use)
- `main`, `master` (permanent branch only)
- `develop`, `dev` (not part of "main only" model)
- `staging`, `production`, `qa` (use environments, not branches)
- `backup`, `temp`, `test` (ambiguous)

---

## Branch Inventory and Classification

### Objective
Identify all existing branches, classify them, and determine their fate (merge, archive, delete).

### Step 1: Generate Branch Inventory

**Using GitHub CLI**:
```bash
# List all remote branches with last commit date and author
gh api repos/:owner/:repo/branches --paginate | \
  jq -r '.[] | "\(.name)\t\(.commit.commit.author.date)\t\(.commit.commit.author.name)"'
```

**Using Git**:
```bash
# List all branches sorted by last commit date
git for-each-ref --sort=-committerdate refs/remotes/origin/ \
  --format='%(committerdate:iso8601)|%(refname:short)|%(authorname)|%(subject)' | \
  column -t -s '|'
```

**Output to CSV**:
```bash
echo "Branch,Last Commit Date,Author,Last Commit Message" > branch-inventory.csv
git for-each-ref --sort=-committerdate refs/remotes/origin/ \
  --format='%(refname:short),%(committerdate:short),%(authorname),"%(subject)"' \
  >> branch-inventory.csv
```

### Step 2: Classify Branches

Open `branch-inventory.csv` and add a "Status" column. Classify each branch:

| Classification | Criteria | Action |
|----------------|----------|--------|
| **MAIN** | Branch name is `main` or `master` | ✅ **Keep** (permanent) |
| **ACTIVE** | Last commit < 7 days ago | ✅ **Keep** (under development) |
| **REVIEW** | Open PR exists | ✅ **Keep** (under review) |
| **MERGEABLE** | Complete work, no PR, < 30 days old | 🔀 **Merge to main** |
| **STALE** | No activity 14-90 days | ⚠️ **Contact owner → Merge, Archive, or Delete** |
| **DEAD** | No activity > 90 days | ❌ **Archive (if valuable) or Delete** |
| **LEGACY** | Old release/maintenance branches | 📦 **Archive with documentation** |
| **DUPLICATE** | Superseded by another branch | ❌ **Delete after verification** |

### Step 3: Contact Owners
For STALE and DEAD branches:

**Email/Slack Template**:
```
Subject: Branch Cleanup: Action Required for branch "feature/X"

Hi @author,

As part of our branch hygiene initiative, we've identified your branch as stale:

**Branch**: feature/X
**Last Activity**: 2024-10-01 (75 days ago)
**Status**: STALE

Please take one of the following actions by 2024-12-22:

1. **Merge**: If work is complete, create a PR to merge into main
2. **Update**: If work is ongoing, push a commit to keep the branch active
3. **Archive**: If work is abandoned but valuable, we'll archive it as archive/2024-12-feature-X
4. **Delete**: If no longer needed, we'll delete the branch

If we don't hear from you by the deadline, we'll default to option 3 (Archive) for historical reference.

Questions? Reply to this message or see: .github/logical-branch-policy.md

Thanks!
Repository Maintainers
```

---

## Execution Plan: Branch Cleanup

### Phase 1: Preparation (Week 1)

**Day 1-2: Inventory**
- [ ] Generate branch inventory CSV (see Step 1 above)
- [ ] Classify all branches (see Step 2 above)
- [ ] Identify branch owners (git log or GitHub API)
- [ ] Create tracking spreadsheet with columns: Branch, Owner, Classification, Action, Deadline, Status

**Day 3-4: Communication**
- [ ] Draft notification email/Slack message
- [ ] Send initial notifications to all branch owners (STALE and DEAD categories)
- [ ] Post announcement in team channels about upcoming cleanup
- [ ] Document policy in `.github/logical-branch-policy.md` (this file)
- [ ] Update `CONTRIBUTING.md` to reference this policy

**Day 5-7: Policy Review**
- [ ] Team review of branch classifications
- [ ] Resolve disputes or edge cases
- [ ] Finalize action plan for each branch
- [ ] Schedule cleanup execution date (Phase 2 start)

### Phase 2: Execution (Week 2-3)

**Week 2: Merge and Archive**
- [ ] **Day 1**: Merge MERGEABLE branches (work with owners to create PRs)
  ```bash
  # For each MERGEABLE branch:
  git checkout main
  git pull origin main
  git checkout feature/X
  git rebase main
  # Resolve conflicts
  gh pr create --base main --head feature/X --title "chore: merge branch feature/X" --body "Cleanup: merging stale branch"
  # Review and merge PR
  ```

- [ ] **Day 2-3**: Archive LEGACY and DEAD branches (with documentation)
  ```bash
  # For each branch to archive:
  git checkout <branch-name>
  git checkout -b archive/2024-12-<branch-name>
  # Add ARCHIVE_README.md (see Rule 4.3)
  git push origin archive/2024-12-<branch-name>
  gh pr create --base archive/2024-12-<branch-name> --head <branch-name> --title "docs: archive branch <branch-name>" --body "Adding archive documentation"
  # After merging ARCHIVE_README.md:
  git push origin --delete <branch-name>
  ```

- [ ] **Day 4-5**: Follow up with non-responsive owners
  - Send reminder emails
  - Escalate to team leads

**Week 3: Final Cleanup**
- [ ] **Day 1-2**: Delete DEAD branches (after final confirmation)
  ```bash
  # For each branch to delete:
  # Verify no open PRs
  gh pr list --head <branch-name>
  # Delete if none exist
  git push origin --delete <branch-name>
  ```

- [ ] **Day 3**: Update documentation
  - [ ] Update branch count in README (if mentioned)
  - [ ] Document archived branches in `BRANCH_ARCHIVE_LOG.md`
  - [ ] Update team wiki/docs with new policy

- [ ] **Day 4-5**: Post-cleanup verification
  ```bash
  # Verify only expected branches remain
  git fetch --prune origin
  git branch -r
  # Should see: origin/main, origin/feature/active-1, origin/feature/active-2, origin/archive/...
  ```

### Phase 3: Ongoing Maintenance (Continuous)

**Weekly**:
- [ ] Run stale branch detection script
  ```bash
  # Add to cron or GitHub Actions
  ./.github/scripts/detect-stale-branches.sh
  ```

**Monthly**:
- [ ] Review open PRs older than 7 days
- [ ] Generate branch health report
- [ ] Send reminders for stale branches

**Quarterly**:
- [ ] Audit branch naming compliance
- [ ] Review archive branch size (consider pruning old archives)
- [ ] Update policy based on team feedback

---

## Deliverables and Artifacts

### Required Documentation

#### 1. Branch Inventory Report
**File**: `reports/branch-inventory-YYYY-MM-DD.csv`
**Columns**: Branch, Last Commit Date, Author, Status, Classification, Action, Deadline, Notes

**Example**:
```csv
Branch,Last Commit Date,Author,Status,Classification,Action,Deadline,Notes
main,2024-12-15,alice,PROTECTED,MAIN,Keep,N/A,Production branch
feature/oauth-login,2024-12-14,bob,OPEN_PR,ACTIVE,Keep,N/A,PR #456 under review
feature/old-api,2024-08-01,charlie,STALE,DEAD,Archive,2024-12-22,Owner notified
hotfix/security-123,2024-12-10,diane,MERGED,MERGED,Delete,N/A,Merged in PR #789
```

#### 2. Branch Cleanup Summary
**File**: `reports/branch-cleanup-summary-YYYY-MM-DD.md`
**Sections**: Executive Summary, Statistics, Actions Taken, Remaining Branches

**Template**:
```markdown
# Branch Cleanup Summary - 2024-12-15

## Executive Summary
Cleaned up 47 branches as part of "main only" policy enforcement.

## Statistics
- **Total Branches Before**: 52
- **Total Branches After**: 5
- **Merged**: 12
- **Archived**: 8
- **Deleted**: 27
- **Remaining Active**: 4 (+ main)

## Actions Taken
### Merged (12)
- feature/oauth-login (PR #456) - Merged by bob on 2024-12-15
- fix/login-timeout (PR #457) - Merged by alice on 2024-12-15
...

### Archived (8)
- archive/2024-12-experimental-blockchain (formerly experimental/blockchain)
- archive/2024-12-old-api (formerly feature/old-api)
...

### Deleted (27)
- feature/test-branch (Dead > 90 days, no valuable content)
- feature/duplicate-work (Superseded by feature/new-approach)
...

## Remaining Branches
1. main (production)
2. feature/user-dashboard (Active, PR #460 open)
3. hotfix/critical-fix (Active, under review)
4. feature/new-api (Active, < 3 days old)
5. feature/refactor-auth (Active, < 5 days old)

## Next Steps
- Continue monitoring for stale branches (weekly check)
- All teams notified of new policy
- Automation enabled for future cleanup
```

#### 3. Branch Archive Log
**File**: `BRANCH_ARCHIVE_LOG.md` (root of repository)
**Purpose**: Historical record of all archived branches

**Template**:
```markdown
# Branch Archive Log

This document records all branches that have been archived for historical reference.

## 2024-12 Cleanup

### archive/2024-12-experimental-blockchain
- **Original Branch**: experimental/blockchain
- **Date Archived**: 2024-12-15
- **Author**: alice
- **Reason**: Experimental POC not adopted; superseded by traditional approach
- **Last Commit**: 2024-09-01
- **Replacement**: feature/database-storage (merged v2.1.0)
- **Reference**: See ARCHIVE_README.md in branch

### archive/2024-12-old-api
- **Original Branch**: feature/old-api
- **Date Archived**: 2024-12-15
- **Author**: charlie
- **Reason**: API redesigned in v3.0.0; kept for reference during migration
- **Last Commit**: 2024-08-01
- **Replacement**: feature/new-api (merged v3.0.0)
- **Reference**: See ARCHIVE_README.md in branch

...
```

### Automation Scripts

#### 1. Stale Branch Detector
**File**: `.github/scripts/detect-stale-branches.sh`

```bash
#!/bin/bash
# Detect stale branches (14+ days without activity)

set -e

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
STALE_DAYS="${2:-14}"
STALE_DATE=$(date -d "$STALE_DAYS days ago" +%Y-%m-%d)

echo "Detecting stale branches in $REPO (older than $STALE_DAYS days)..."

gh api "repos/$REPO/branches" --paginate | jq -r --arg stale_date "$STALE_DATE" '
  .[] |
  select(.commit.commit.author.date < $stale_date) |
  select(.name != "main" and .name != "master") |
  "\(.name)\t\(.commit.commit.author.date)\t\(.commit.commit.author.name)"
' | column -t -s $'\t'

echo ""
echo "Run with: .github/scripts/detect-stale-branches.sh [owner/repo] [days]"
```

#### 2. Branch Cleanup Workflow
**File**: `.github/workflows/branch-cleanup-notify.yml`

```yaml
name: Branch Cleanup Notification

on:
  schedule:
    # Run weekly on Monday at 9 AM UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:

jobs:
  detect-stale-branches:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Detect Stale Branches
        id: stale
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Detect branches older than 14 days
          STALE_BRANCHES=$(./.github/scripts/detect-stale-branches.sh "" 14)
          if [ -n "$STALE_BRANCHES" ]; then
            echo "found=true" >> $GITHUB_OUTPUT
            echo "$STALE_BRANCHES" > stale-branches.txt
          else
            echo "found=false" >> $GITHUB_OUTPUT
          fi

      - name: Create Issue for Stale Branches
        if: steps.stale.outputs.found == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BRANCHES=$(cat stale-branches.txt)
          gh issue create \
            --title "🧹 Stale Branch Cleanup: $(date +%Y-%m-%d)" \
            --label "chore,branch-cleanup" \
            --body "## Stale Branches Detected

The following branches have not been updated in 14+ days:

\`\`\`
$BRANCHES
\`\`\`

**Action Required**: Branch owners, please:
1. **Merge** if work is complete (create a PR)
2. **Update** if work is ongoing (push a commit)
3. **Archive** if work is abandoned but valuable (reply to this issue)
4. **Delete** if no longer needed (reply to this issue)

See: [Logical Branch Policy](.github/logical-branch-policy.md)

Branches not addressed within 7 days will be automatically archived or deleted.
"
```

---

## GitHub CLI Reference

### Installation
```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

### Common Commands

#### Branch Operations
```bash
# List all branches
gh api repos/:owner/:repo/branches --paginate | jq -r '.[].name'

# Get branch details
gh api repos/:owner/:repo/branches/<branch-name>

# Delete branch
gh api -X DELETE repos/:owner/:repo/git/refs/heads/<branch-name>

# Create branch from main
gh api repos/:owner/:repo/git/refs -f ref='refs/heads/feature/new-branch' -f sha='<main-sha>'
```

#### Pull Request Operations
```bash
# Create PR
gh pr create --base main --head feature/my-feature --title "feat: add new feature" --body "Description"

# List open PRs
gh pr list --state open

# Review PR
gh pr review <PR-number> --approve
gh pr review <PR-number> --request-changes --body "Feedback"

# Merge PR
gh pr merge <PR-number> --squash --delete-branch

# Close PR without merging
gh pr close <PR-number> --delete-branch
```

#### Repository Operations
```bash
# List branches with metadata
gh api repos/:owner/:repo/branches --paginate | jq -r '.[] | "\(.name)\t\(.commit.commit.author.date)"'

# Enable auto-delete merged branches
gh api -X PATCH repos/:owner/:repo -f delete_branch_on_merge=true

# Update branch protection rules
gh api repos/:owner/:repo/branches/main/protection -X PUT --input branch-protection.json
```

#### Stale Branch Detection
```bash
# Find branches older than 14 days
gh api repos/:owner/:repo/branches --paginate | jq -r --arg date "$(date -d '14 days ago' +%Y-%m-%d)" '.[] | select(.commit.commit.author.date < $date) | .name'

# Get branch owner
gh api repos/:owner/:repo/branches/<branch-name> | jq -r '.commit.commit.author.name'
```

---

## GitHub UI Guidance

### Enable Auto-Delete Merged Branches

**Path**: `Settings → General → Pull Requests`

1. Navigate to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll to **Pull Requests** section
4. Check ☑️ **Automatically delete head branches**
5. Click **Save changes**

**Effect**: After a PR is merged, the source branch is automatically deleted.

### Configure Branch Protection Rules

**Path**: `Settings → Branches → Branch protection rules`

#### For `main` Branch
1. Click **Add branch protection rule**
2. **Branch name pattern**: `main`
3. Configure settings:
   - ☑️ **Require a pull request before merging**
     - ☑️ Required approvals: **1** (or **2** for critical repos)
     - ☑️ Dismiss stale pull request approvals when new commits are pushed
   - ☑️ **Require status checks to pass before merging**
     - ☑️ Require branches to be up to date before merging
     - Select required checks: `CI`, `tests`, `lint`, `security-scan`
   - ☑️ **Require conversation resolution before merging**
   - ☑️ **Require signed commits** (optional, recommended)
   - ☑️ **Include administrators**
   - ☑️ **Restrict who can push to matching branches** (optional, for high-security repos)
   - ☑️ **Do not allow bypassing the above settings**
4. Click **Create** / **Save changes**

### Create a Pull Request (UI)

1. Navigate to repository
2. Click **Pull requests** tab
3. Click **New pull request**
4. **Base**: `main`
5. **Compare**: `feature/your-branch`
6. Click **Create pull request**
7. **Title**: Follow conventional commit format (e.g., `feat: add user authentication`)
8. **Description**: Fill out PR template (if available)
9. **Reviewers**: Assign reviewers
10. **Labels**: Add appropriate labels (`feature`, `bug`, `hotfix`)
11. Click **Create pull request**

### Merge a Pull Request (UI)

1. Open the PR
2. Verify all checks pass ✅
3. Verify at least one approval ✅
4. Click **Merge pull request** dropdown
5. Select merge strategy:
   - **Squash and merge** (default for "main only" model)
   - **Rebase and merge** (for single-commit branches)
   - **Create a merge commit** (for complex features)
6. Edit commit message if needed
7. Click **Confirm squash and merge**
8. (Optional) Click **Delete branch** if not auto-enabled

### Find Stale Branches (UI)

1. Navigate to repository
2. Click **Branches** (below repository name or via `/branches`)
3. Click **All branches**
4. Sort by **Last updated** (click column header)
5. Review branches not updated recently
6. Click **Delete** icon for stale branches (or **...** → **Delete branch**)

### Archive a Branch (UI)

GitHub doesn't have native "archive" feature, so use naming convention:

1. Locally rename branch: `git branch -m old-branch archive/2024-12-old-branch`
2. Push renamed branch: `git push origin archive/2024-12-old-branch`
3. Delete old branch: `git push origin --delete old-branch`
4. Create ARCHIVE_README.md in the archived branch (see Rule 4.3)

---

## Enforcement and Automation

### Automated Enforcement

#### 1. Branch Protection Rules (GitHub Settings)
- **Purpose**: Prevent direct commits to `main`
- **Configuration**: See [Configure Branch Protection Rules](#configure-branch-protection-rules)
- **Enforcement**: GitHub natively blocks non-compliant merges

#### 2. CI/CD Checks
**Required Checks** (must pass before merge):
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: npm test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security Scan
        run: npm audit

  branch-name-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check Branch Name
        run: |
          BRANCH_NAME="${{ github.head_ref }}"
          if ! [[ "$BRANCH_NAME" =~ ^(feature|fix|hotfix|refactor|docs|test|chore|perf)/ ]]; then
            echo "❌ Invalid branch name: $BRANCH_NAME"
            echo "Branch must start with: feature/, fix/, hotfix/, refactor/, docs/, test/, chore/, or perf/"
            exit 1
          fi
          echo "✅ Branch name is valid: $BRANCH_NAME"
```

#### 3. Stale Branch Automation
**Weekly Notification** (see [Branch Cleanup Workflow](#2-branch-cleanup-workflow))
- Detects branches older than 14 days
- Creates GitHub issue with list of stale branches
- Notifies branch owners

**Monthly Cleanup** (optional, requires approval):
```yaml
# .github/workflows/branch-auto-cleanup.yml
name: Auto-Cleanup Stale Branches

on:
  schedule:
    - cron: '0 2 1 * *'  # 1st of each month at 2 AM UTC
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Delete Stale Branches
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Delete branches older than 90 days (except main and archive/*)
          STALE_DATE=$(date -d '90 days ago' +%Y-%m-%d)
          gh api repos/:owner/:repo/branches --paginate | \
            jq -r --arg stale_date "$STALE_DATE" '
              .[] |
              select(.commit.commit.author.date < $stale_date) |
              select(.name != "main" and .name != "master") |
              select(.name | startswith("archive/") | not) |
              .name
            ' | while read branch; do
              echo "Deleting stale branch: $branch"
              gh api -X DELETE repos/:owner/:repo/git/refs/heads/$branch || echo "Failed to delete $branch"
            done
```

**⚠️ Warning**: Auto-deletion is aggressive. Use with caution. Consider requiring manual approval:
```yaml
      - name: Request Approval
        uses: trstringer/manual-approval@v1
        with:
          approvers: team-leads
          minimum-approvals: 1
```

#### 4. Branch Naming Enforcement (GitHub Actions)
See `branch-name-check` job in [CI/CD Checks](#2-cicd-checks) above.

### Manual Enforcement

#### Quarterly Branch Audit
**Responsibility**: Repository maintainers
**Process**:
1. Run branch inventory script (see [Branch Inventory and Classification](#branch-inventory-and-classification))
2. Review all branches manually
3. Contact owners of non-compliant branches
4. Archive or delete branches after confirmation
5. Update `BRANCH_ARCHIVE_LOG.md`

#### PR Review Checklist
**Responsibility**: Code reviewers
**Checklist** (add to PR template):
```markdown
## Reviewer Checklist
- [ ] Branch name follows convention (feature/, fix/, etc.)
- [ ] Branch is based on latest main
- [ ] CI checks pass
- [ ] Code quality acceptable
- [ ] Security scan clean
- [ ] Tests cover new code
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Conventional commit messages
```

---

## Best Practices and Reminders

### For Contributors

#### ✅ Do's
1. **Always branch from latest `main`**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-feature
   ```

2. **Keep branches short-lived**
   - Target: 1-3 days
   - Maximum: 7 days
   - If longer needed, break into smaller PRs

3. **Sync with main regularly**
   ```bash
   # Daily or before creating PR
   git checkout main
   git pull origin main
   git checkout feature/my-feature
   git rebase main
   # Or: git merge main
   ```

4. **Use conventional commit messages**
   ```bash
   git commit -m "feat: add user authentication"
   git commit -m "fix: resolve login timeout issue"
   ```

5. **Delete branches after merge**
   ```bash
   # Locally
   git branch -d feature/my-feature
   # Remotely (if not auto-deleted)
   git push origin --delete feature/my-feature
   ```

6. **Use feature flags for risky changes**
   ```javascript
   if (featureFlags.isEnabled('new-feature')) {
     // New code path
   } else {
     // Old code path (fallback)
   }
   ```

7. **Write comprehensive PR descriptions**
   - What changed?
   - Why?
   - How to test?
   - Any breaking changes?

#### ❌ Don'ts
1. **Don't commit directly to main**
   - Always use PRs, even for hotfixes

2. **Don't let branches go stale**
   - Push commits regularly to show activity
   - If blocked, communicate in PR comments

3. **Don't mix unrelated changes**
   - One feature/fix per branch
   - Create separate branches for independent work

4. **Don't skip tests**
   - Write tests for new code
   - Ensure existing tests pass

5. **Don't ignore review feedback**
   - Address all comments
   - Explain disagreements respectfully

6. **Don't force push after review starts**
   - Use `git commit --fixup` and `git rebase --autosquash` instead
   - Or add new commits and squash during merge

7. **Don't create `develop`, `staging`, or similar branches**
   - Use `main` only model
   - Use environments and feature flags instead

### For Maintainers

#### ✅ Do's
1. **Enable auto-delete merged branches**
   - Settings → General → Pull Requests → ☑️ Automatically delete head branches

2. **Configure branch protection for `main`**
   - Require PR reviews
   - Require status checks
   - Require conversation resolution

3. **Run weekly stale branch checks**
   - Use automation (see [Branch Cleanup Workflow](#2-branch-cleanup-workflow))
   - Notify owners proactively

4. **Document branch archival**
   - Update `BRANCH_ARCHIVE_LOG.md`
   - Add ARCHIVE_README.md to archived branches

5. **Communicate policy changes**
   - Announce in team channels
   - Update `CONTRIBUTING.md`
   - Provide training if needed

6. **Monitor branch health metrics**
   - Number of active branches
   - Average branch lifetime
   - Merge time (PR open → merged)

#### ❌ Don'ts
1. **Don't delete branches without confirmation**
   - Always notify owner first (except very old dead branches)
   - Archive if uncertain about value

2. **Don't bypass branch protection**
   - Even admins should follow the process
   - Use emergency override only for critical incidents

3. **Don't let policy drift**
   - Enforce consistently
   - Update policy based on team feedback

4. **Don't over-automate deletion**
   - Require manual approval for auto-cleanup
   - False positives can lose valuable work

### Common Pitfalls

#### Pitfall 1: Long-Lived Feature Branches
**Problem**: Branch open for 30+ days, massive merge conflicts

**Solution**:
- Break work into smaller PRs
- Use feature flags to merge incomplete features
- Merge main into feature branch daily

#### Pitfall 2: Merge Conflicts
**Problem**: Feature branch diverged too far from main

**Solution**:
```bash
# Keep branch up-to-date
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main
# Resolve conflicts incrementally
```

#### Pitfall 3: Stale Branches Accumulating
**Problem**: Dozens of old branches clutter repository

**Solution**:
- Enable stale branch automation
- Set clear expectations (7-day lifetime)
- Regular cleanup sprints (quarterly)

#### Pitfall 4: Lost Work from Premature Deletion
**Problem**: Accidentally deleted branch with unreleased work

**Solution**:
- Archive instead of delete when uncertain
- Use `git reflog` to recover deleted branches:
  ```bash
  git reflog show origin/<branch-name>
  git checkout -b recovered-branch <commit-sha>
  ```

---

## Security Considerations

### Threat Model

#### Threat 1: Unprotected Main Branch
**Risk**: Direct commits to main bypass CI/CD and code review

**Mitigation**:
- ✅ Enable branch protection (see [Configure Branch Protection Rules](#configure-branch-protection-rules))
- ✅ Require PR reviews (minimum 1, preferably 2)
- ✅ Require status checks (CI, tests, security scans)

#### Threat 2: Secrets in Branch History
**Risk**: API keys, passwords, tokens committed and pushed

**Mitigation**:
- ✅ Use pre-commit hooks to scan for secrets (e.g., `truffleHog`, `detect-secrets`)
- ✅ Run secret scanning in CI/CD (GitHub Advanced Security, GitGuardian)
- ✅ Rotate secrets immediately if exposed
- ✅ Educate team on `.gitignore` and environment variables

**If secrets are detected**:
```bash
# 1. Rotate the secret immediately (API key, password, token)
# 2. Remove from history using BFG Repo-Cleaner or git-filter-repo
git filter-repo --path-glob '**/config/secrets.json' --invert-paths

# 3. Force push (requires admin override)
git push --force origin main

# 4. Notify team to re-clone repository
```

#### Threat 3: Malicious Code via Stale Branches
**Risk**: Old branches with vulnerabilities merged without security review

**Mitigation**:
- ✅ Require security scans on all PRs (see [CI/CD Checks](#2-cicd-checks))
- ✅ Re-run security scans on stale branches before merge
- ✅ Require re-approval if branch is rebased/updated

#### Threat 4: Dependency Vulnerabilities
**Risk**: Outdated dependencies in feature branches

**Mitigation**:
- ✅ Run `npm audit`, `pip check`, or equivalent in CI/CD
- ✅ Use Dependabot or Renovate to auto-update dependencies
- ✅ Require security approval for dependency changes

### Secure Branch Management

#### Signed Commits
**Purpose**: Verify commit author identity

**Setup**:
```bash
# Generate GPG key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format=long

# Export public key
gpg --armor --export <KEY_ID>

# Add to GitHub: Settings → SSH and GPG keys → New GPG key

# Configure Git
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
```

**Enforce in Branch Protection**:
- Settings → Branches → Branch protection rules → ☑️ Require signed commits

#### Sensitive Branch Names
**Avoid** embedding sensitive info in branch names:
```bash
# ❌ BAD
feature/client-acme-secret-key-abc123
fix/prod-password-reset-admin@example.com

# ✅ GOOD
feature/client-integration
fix/password-reset-flow
```

### Compliance and Audit

#### SOC 2 / ISO 27001 Compliance
**Requirements**:
- All changes to production code (main) must be reviewed and approved
- Audit trail of all merges (Git history + PR comments)
- Access controls enforced (branch protection, required reviews)

**Evidence**:
- GitHub PR history
- Branch protection settings screenshots
- CI/CD logs showing automated checks

#### GDPR / Data Protection
**Requirements**:
- No personal data in code or commit messages
- Right to be forgotten (ability to remove contributor data)

**Compliance**:
- Train team to avoid PII in commits
- Use sanitization scripts if needed
- Document data removal process in `PRIVACY.md`

---

## Related Documentation

### Internal Docs (This Repository)
- [BRANCH_STRATEGY.md](../BRANCH_STRATEGY.md) - Comprehensive branching strategy (alternative to "main only")
- [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) - Git workflow and branch strategy details
- [VERSION_CONTROL_STANDARDS.md](../VERSION_CONTROL_STANDARDS.md) - Version control standards
- [CONTRIBUTING.md](../docs/CONTRIBUTING.md) - Contribution guidelines and commit conventions
- [SECURITY.md](../docs/SECURITY.md) - Security policy and vulnerability reporting
- [CODE_OF_CONDUCT.md](../docs/CODE_OF_CONDUCT.md) - Community standards (if available)

### GitHub Documentation
- [About Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About Merge Methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Actions for Branch Management](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

### Best Practices and Standards
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

---

## Changelog

### Version 1.0.0 - 2024-12-15
- Initial policy document
- Defined "main only" branch model
- Established branch creation, merge, review, and lifecycle rules
- Created branch naming conventions
- Documented branch inventory and classification process
- Provided step-by-step cleanup execution plan
- Added GitHub CLI and UI guidance
- Defined deliverables and automation scripts
- Added security considerations and cross-references

---

**Policy Owner**: Repository Maintainers  
**Last Updated**: 2024-12-15  
**Next Review**: 2025-03-15 (quarterly)

**Questions or Feedback?** Open an issue or contact the maintainers via [CONTRIBUTING.md](../docs/CONTRIBUTING.md).
