# Pull Request Automation System

Comprehensive guide for the automated PR creation, push, and merge system.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Auto PR Creation](#auto-pr-creation)
- [Auto Merge](#auto-merge)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

______________________________________________________________________

## Overview

The PR Automation System streamlines your development workflow by:

1. **Automatically creating pull requests** when you push feature branches
1. **Auto-merging PRs** when all requirements are met
1. **Resolving merge conflicts** automatically when possible
1. **Cleaning up merged branches** to keep the repository tidy

This system integrates seamlessly with your existing Git workflow and follows
the organization's branching strategy.

______________________________________________________________________

## Features

### 🚀 Auto PR Creation

- **Automatic PR creation** for feature, bugfix, hotfix, and release branches
- **Smart base branch detection** based on branch type
- **Conventional commit titles** following project standards
- **Auto-generated descriptions** with commit history
- **Automatic labeling** based on branch type
- **Author assignment** for accountability

### 🔄 Auto Merge

- **Intelligent merging** when all conditions are met
- **Conflict resolution** with automatic branch updates
- **Status check validation** before merging
- **Approval verification** based on branch type
- **Configurable merge methods** (merge, squash, rebase)
- **Automatic branch cleanup** after successful merge

### ⚙️ Merge Conflict Handling

- **Automatic conflict detection** on every PR update
- **Auto-update branch** to resolve simple conflicts
- **Notification system** for complex conflicts requiring manual resolution
- **Detailed guidance** for conflict resolution

______________________________________________________________________

## Quick Start

### 1. Enable Auto PR Creation

Simply push your feature branch:

```bash
# Create and push a feature branch
git checkout -b feature/user-authentication
git add .
git commit -m "feat: add user authentication"
git push -u origin feature/user-authentication
```

A pull request will be **automatically created** with:

- Title: `feat: user authentication`
- Base branch: `develop` (for feature branches)
- Labels: `enhancement`, `auto-created`
- Assigned to you

### 2. Enable Auto Merge

To enable auto-merge for a PR, use **any** of these methods:

**Method 1: Add label**

```bash
# Add the 'auto-merge' label via GitHub UI or CLI
gh pr edit <PR_NUMBER> --add-label "auto-merge"
```

**Method 2: Include in title**

```
feat: user authentication [auto-merge]
```

**Method 3: Auto-created PRs** Auto-created PRs are automatically eligible for
auto-merge.

### 3. Skip Automation

To skip automation for specific commits or PRs:

**Skip Auto PR Creation:**

```bash
git commit -m "feat: work in progress [skip-auto-pr]"
```

**Skip Auto Merge:** Include `[skip-auto-merge]` in PR title or description.

______________________________________________________________________

## Auto PR Creation

### Trigger Conditions

Auto PR creation triggers when you push to branches matching these patterns:

- `feature/**` - New features
- `bugfix/**` - Bug fixes
- `hotfix/**` - Critical production fixes
- `release/**` - Release preparation

### Base Branch Selection

The system automatically selects the appropriate base branch:

| Branch Type | Base Branch | Example                              |
| ----------- | ----------- | ------------------------------------ |
| `feature/*` | `develop`   | `feature/login` → PR to `develop`    |
| `bugfix/*`  | `develop`   | `bugfix/fix-typo` → PR to `develop`  |
| `hotfix/*`  | `main`      | `hotfix/critical-fix` → PR to `main` |
| `release/*` | `main`      | `release/v1.2.0` → PR to `main`      |

### Generated PR Details

Each auto-created PR includes:

1. **Conventional commit title** - e.g., `feat: user authentication`
1. **Detailed description** with:
   - Type of change checklist
   - List of commits included
   - Testing checklist
   - Code quality checklist
1. **Automatic labels** based on branch type
1. **Author assignment** for accountability
1. **Initial comment** with next steps

### Example Auto-Created PR

```markdown
## Description

Auto-generated PR for `feature/user-authentication`

## Type of Change

- [x] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Changes Made

- Add authentication middleware (a1b2c3d)
- Implement JWT token generation (e4f5g6h)
- Add login/logout endpoints (i7j8k9l)

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

______________________________________________________________________

## Auto Merge

### Eligibility Requirements

A PR is eligible for auto-merge when **ALL** of these conditions are met:

#### 1. **Auto-Merge Indicator**

One of:

- Has `auto-merge` or `automerge` label
- Was auto-created (has `auto-created` label)
- Title contains `[auto-merge]`

#### 2. **Not in Draft Mode**

PR must not be marked as draft

#### 3. **No Merge Conflicts**

Either:

- No conflicts exist, OR
- Conflicts were auto-resolved by updating the branch

#### 4. **All Status Checks Pass**

All required CI/CD checks must pass:

- Linting
- Tests
- Security scans
- Code coverage
- Any custom checks

#### 5. **Required Approvals**

Minimum approvals based on branch type:

| Branch Type | Required Approvals  |
| ----------- | ------------------- |
| `feature/*` | 1                   |
| `bugfix/*`  | 1                   |
| `hotfix/*`  | 0 (emergency fixes) |
| `release/*` | 2                   |

#### 6. **No Blocking Labels**

PR must NOT have these labels:

- `do-not-merge`
- `wip`
- `on-hold`

### Merge Process

When all conditions are met:

1. **Final verification** of all requirements
1. **Merge using configured method** (default: squash)
1. **Post-merge comment** with details
1. **Branch cleanup** (delete source branch)
1. **Notification** to PR participants

### Conflict Resolution

When merge conflicts are detected:

#### Automatic Resolution

The system attempts to auto-resolve by:

1. **Updating the branch** - Merges base branch into PR branch
1. **Re-running checks** - Validates the updated code
1. **Notifying participants** - Comments on successful update
1. **Proceeding to merge** - If checks pass

#### Manual Resolution Required

If auto-resolution fails:

1. **Notification comment** posted with instructions
1. **`conflicts` label** added to PR
1. **Detailed steps** provided for manual resolution

```markdown
⚠️ **Auto-Merge: Conflicts Detected**

This PR has merge conflicts that cannot be automatically resolved.

**To resolve:**

1. Update your local branch: `git checkout feature/my-feature`
2. Merge the base branch: `git merge develop`
3. Resolve conflicts in your editor
4. Commit the resolved changes
5. Push to update this PR

Once conflicts are resolved and all checks pass, auto-merge will proceed.
```

______________________________________________________________________

## Configuration

The PR automation behavior is controlled by `.github/pr-automation.yml`.

### Key Configuration Options

#### Auto PR Creation

```yaml
auto_pr:
  enabled: true
  branch_patterns:
    - "feature/**"
    - "bugfix/**"
    - "hotfix/**"
  base_branches:
    feature: develop
    bugfix: develop
    hotfix: main
  auto_assign: true
```

#### Auto Merge

```yaml
auto_merge:
  enabled: true
  merge_method: squash # Options: merge, squash, rebase

  approvals:
    minimum: 1
    by_branch_type:
      hotfix: 0
      release: 2

  conflict_resolution:
    auto_update_branch: true
    notify_on_conflict: true

  delete_branch_after_merge: true
```

#### Notifications

```yaml
notifications:
  on_pr_created: true
  on_merge_success: true
  on_conflict_detected: true
```

### Customizing Configuration

1. Edit `.github/pr-automation.yml`
1. Commit and push changes
1. New settings take effect immediately

______________________________________________________________________

## Usage Examples

### Example 1: Standard Feature Development

```bash
# 1. Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/add-dark-mode

# 2. Make changes
git add .
git commit -m "feat: add dark mode toggle"
git push -u origin feature/add-dark-mode

# ✅ PR automatically created!

# 3. Make more changes
git add .
git commit -m "feat: add dark mode styles"
git push

# ✅ PR automatically updated!

# 4. Once reviewed and checks pass
# ✅ PR automatically merged!
# ✅ Branch automatically deleted!
```

### Example 2: Hotfix with Immediate Merge

```bash
# 1. Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# 2. Apply critical fix
git add .
git commit -m "fix: patch security vulnerability"
git push -u origin hotfix/security-patch

# ✅ PR automatically created!
# ✅ Since it's a hotfix, 0 approvals required
# ✅ Automatically merged when checks pass!
```

### Example 3: Work in Progress (Skip Automation)

```bash
# Create feature branch
git checkout -b feature/experimental

# Commit with skip flag
git add .
git commit -m "feat: experimental feature [skip-auto-pr]"
git push -u origin feature/experimental

# ❌ No PR created (as intended)

# Later, when ready for PR, create manually
gh pr create --title "feat: experimental feature"
```

### Example 4: Manual Merge Control

```bash
# Create feature branch
git checkout -b feature/needs-review
git add .
git commit -m "feat: complex changes"
git push -u origin feature/needs-review

# ✅ PR automatically created

# Add do-not-merge label to prevent auto-merge
gh pr edit <PR_NUMBER> --add-label "do-not-merge"

# ❌ Auto-merge disabled until label removed
```

______________________________________________________________________

## Troubleshooting

### PR Not Auto-Created

**Check:**

- ✅ Branch name matches patterns (`feature/*`, `bugfix/*`, etc.)
- ✅ Commit message doesn't contain `[skip-auto-pr]`
- ✅ No existing open PR for this branch
- ✅ Workflow has proper permissions

**Solution:**

```bash
# Manually trigger workflow
git commit --allow-empty -m "trigger: auto-pr creation"
git push
```

### PR Not Auto-Merging

**Check:**

- ✅ PR has `auto-merge` label or was auto-created
- ✅ All status checks passed
- ✅ Required approvals obtained
- ✅ No merge conflicts
- ✅ Not in draft mode
- ✅ No `do-not-merge` label

**Debug:**

```bash
# Check PR status
gh pr view <PR_NUMBER> --json statusCheckRollup,reviews,mergeable

# View workflow logs
gh run list --workflow=auto-merge.yml
gh run view <RUN_ID> --log
```

### Merge Conflicts Not Auto-Resolved

**Reason:** Conflicts are too complex for automatic resolution

**Solution:**

```bash
# 1. Checkout your branch
git checkout feature/my-feature

# 2. Update from base branch
git fetch origin
git merge origin/develop

# 3. Resolve conflicts
# Edit files to resolve conflicts

# 4. Complete merge
git add .
git commit -m "fix: resolve merge conflicts"
git push

# ✅ Auto-merge will proceed once checks pass
```

### Branch Not Deleted After Merge

**Check:**

- ✅ Branch is not protected (not main/develop/master)
- ✅ `delete_branch_after_merge: true` in config
- ✅ Workflow has proper permissions

**Manual cleanup:**

```bash
# Delete local branch
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature
```

______________________________________________________________________

## Best Practices

### ✅ Do's

1. **Use descriptive branch names**

   ```bash
   ✅ feature/user-authentication
   ✅ bugfix/fix-login-timeout
   ✅ hotfix/critical-security-patch
   ```

1. **Follow conventional commits**

   ```bash
   ✅ feat: add user authentication
   ✅ fix: resolve login timeout issue
   ✅ docs: update API documentation
   ```

1. **Keep PRs focused and small**

   - One feature/fix per PR
   - Easier to review and merge
   - Reduces conflict likelihood

1. **Update PR descriptions**

   - Auto-generated descriptions are starting points
   - Add context and testing details
   - Link related issues

1. **Monitor auto-merge status**

   - Check workflow summaries
   - Address failed checks promptly
   - Respond to review feedback

### ❌ Don'ts

1. **Don't bypass required checks**

   ```bash
   ❌ Pushing without running tests locally
   ❌ Forcing merge with failing checks
   ```

1. **Don't create massive PRs**

   ```bash
   ❌ feature/everything - 50 files changed
   ✅ feature/user-auth - 5 files changed
   ✅ feature/user-profile - 4 files changed
   ```

1. **Don't ignore merge conflicts**

   - Address conflicts promptly
   - Test after resolving
   - Don't just accept all changes

1. **Don't disable safety features**

   - Keep required approvals
   - Maintain status checks
   - Use branch protection

1. **Don't use auto-merge for breaking changes**

   - Breaking changes need careful review
   - Add `do-not-merge` label
   - Coordinate with team

______________________________________________________________________

## Workflow Integration

### Integration with Existing Workflows

The PR automation system works alongside:

- **PR Quality Checks** - Validates titles, descriptions
- **CI/CD Pipelines** - Tests, linting, security scans
- **Code Review** - Approval requirements
- **Branch Protection** - Enforces merge policies

### Workflow Execution Order

1. **Push to branch** → Auto PR Creation
1. **PR created** → PR Quality Checks run
1. **CI/CD triggered** → Tests, linting, scans
1. **Reviews submitted** → Approval tracking
1. **All conditions met** → Auto Merge
1. **Merge successful** → Branch cleanup

______________________________________________________________________

## Advanced Usage

### Custom Merge Methods

Configure per repository:

```yaml
# .github/pr-automation.yml
auto_merge:
  merge_method: squash # or 'merge' or 'rebase'
```

**Squash (default):** Combines all commits into one **Merge:** Preserves all
commits with merge commit **Rebase:** Replays commits on base branch

### Branch-Specific Rules

```yaml
auto_merge:
  approvals:
    by_branch_type:
      feature: 1 # Features need 1 approval
      bugfix: 1 # Bugfixes need 1 approval
      hotfix: 0 # Hotfixes can merge without approval
      release: 2 # Releases need 2 approvals
```

### Manual Trigger

Manually trigger auto-merge for a specific PR:

```bash
# Via GitHub CLI
gh workflow run auto-merge.yml -f pr_number=123

# Via GitHub UI
# Actions → Auto Merge Pull Request → Run workflow → Enter PR number
```

______________________________________________________________________

## Security Considerations

### Protected Information

- Auto-merge requires proper authentication
- Branch protection rules still apply
- CODEOWNERS rules are respected
- Required reviews cannot be bypassed

### Audit Trail

All automation actions are:

- Logged in workflow runs
- Commented on PRs
- Visible in git history
- Traceable to specific events

### Permission Requirements

The workflows require these permissions:

```yaml
permissions:
  contents: write # Push and merge
  pull-requests: write # Create and modify PRs
  issues: write # Add labels and comments
  checks: read # Read status checks
```

______________________________________________________________________

## Support

### Getting Help

1. **Check this documentation** - Most questions answered here
1. **Review workflow logs** - Detailed execution information
1. **Check PR comments** - Automated feedback and guidance
1. **Open an issue** - For bugs or feature requests

### Reporting Issues

When reporting issues, include:

- PR number and link
- Expected vs actual behavior
- Workflow run logs
- Configuration settings
- Steps to reproduce

______________________________________________________________________

## Changelog

### Version 1.0.0 (2024-11-18)

Initial release:

- Auto PR creation for feature branches
- Auto merge with approval and check validation
- Automatic conflict resolution
- Branch cleanup after merge
- Comprehensive configuration options
- Full documentation

______________________________________________________________________

## Related Documentation

- [Git Workflow Guide](../workflows/GIT_WORKFLOW.md) - Branching strategy and
  commit conventions
- [Automation Master Guide](AUTOMATION_MASTER_GUIDE.md) - Overall automation
  architecture
- [Contributing Guidelines](../governance/CONTRIBUTING.md) - How to contribute
  to the organization
- [Branch Protection](../governance/BRANCH_PROTECTION.md) - Branch protection
  configuration

______________________________________________________________________

**Last Updated:** 2024-11-18 **Maintainer:** ivi374forivi organization
**License:** MIT
