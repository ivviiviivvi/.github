# Git Workflow & Branch Strategy

Comprehensive guide for Git workflows, branching strategies, and best practices.

## Table of Contents

- [Branch Strategy](#branch-strategy)
- [Commit Conventions](#commit-conventions)
- [Pull Request Workflow](#pull-request-workflow)
- [Release Process](#release-process)
- [Hotfix Process](#hotfix-process)
- [Best Practices](#best-practices)

---

## Branch Strategy

### Git Flow Model

We use a modified Git Flow strategy optimized for continuous deployment.

```
main (production)
  ├── develop (integration)
  │   ├── feature/user-authentication
  │   ├── feature/payment-integration
  │   └── feature/dashboard-redesign
  ├── release/v1.2.0
  └── hotfix/critical-security-fix
```

### Branch Types

#### 1. Main Branch (`main` or `master`)
- **Purpose**: Production-ready code
- **Protection**: Highest level
- **Deployment**: Automatically deploys to production
- **Restrictions**:
  - No direct commits
  - Requires PR approval
  - All checks must pass
  - Signed commits required

#### 2. Develop Branch (`develop`)
- **Purpose**: Integration branch for features
- **Protection**: High level
- **Deployment**: Automatically deploys to staging
- **Merging**: From feature branches

#### 3. Feature Branches (`feature/*`)
- **Naming**: `feature/short-description` or `feature/TICKET-123-description`
- **Purpose**: New features or enhancements
- **Base**: Created from `develop`
- **Merge to**: `develop`
- **Lifetime**: Delete after merging

Examples:
```bash
feature/user-authentication
feature/JIRA-456-payment-gateway
feature/add-dark-mode
```

#### 4. Release Branches (`release/*`)
- **Naming**: `release/v1.2.0`
- **Purpose**: Prepare for production release
- **Base**: Created from `develop`
- **Merge to**: Both `main` and `develop`
- **Activities**:
  - Version bumping
  - Final testing
  - Bug fixes only
  - Documentation updates

#### 5. Hotfix Branches (`hotfix/*`)
- **Naming**: `hotfix/critical-fix-description`
- **Purpose**: Urgent production fixes
- **Base**: Created from `main`
- **Merge to**: Both `main` and `develop`
- **Priority**: Highest

#### 6. Bugfix Branches (`bugfix/*`)
- **Naming**: `bugfix/fix-login-error`
- **Purpose**: Non-critical bug fixes
- **Base**: Created from `develop`
- **Merge to**: `develop`

---

## Commit Conventions

### Conventional Commits

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system changes
- **ci**: CI/CD changes
- **chore**: Other changes (dependency updates, etc.)
- **revert**: Revert a previous commit

### Examples

```bash
# Simple feature
feat: add user authentication

# Feature with scope
feat(auth): implement OAuth2 login

# Bug fix with issue reference
fix(api): resolve race condition in user creation

Closes #123

# Breaking change
feat(api)!: change response format for /users endpoint

BREAKING CHANGE: The /users endpoint now returns an array
instead of an object. Update all clients accordingly.

# Multiple paragraphs
refactor(database): optimize query performance

This commit refactors the database queries to use
batch operations instead of individual queries.

Performance improvement: 10x faster for large datasets
```

### Commit Message Guidelines

1. **Subject line**:
   - Max 50 characters
   - Imperative mood ("add" not "added")
   - No period at the end
   - Capitalize first letter

2. **Body** (optional):
   - Wrap at 72 characters
   - Explain what and why, not how
   - Separate from subject with blank line

3. **Footer** (optional):
   - Reference issues: `Closes #123`, `Fixes #456`
   - Breaking changes: `BREAKING CHANGE: description`

---

## Pull Request Workflow

### 1. Create Feature Branch

```bash
# Update develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/my-feature

# Work on your feature
git add .
git commit -m "feat: add new feature"

# Push to remote
git push -u origin feature/my-feature
```

### 2. Keep Branch Updated

```bash
# Regularly sync with develop
git checkout develop
git pull origin develop

git checkout feature/my-feature
git rebase develop

# Or merge if you prefer
git merge develop
```

### 3. Create Pull Request

**PR Title**: Should follow conventional commit format
```
feat: add user authentication
fix(api): resolve timeout issue
docs: update installation guide
```

**PR Description** should include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Added authentication middleware
- Implemented JWT token generation
- Added login/logout endpoints

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex code
- [x] Documentation updated
- [x] No new warnings generated
- [x] Tests pass locally

## Related Issues
Closes #123
Relates to #456
```

### 4. Code Review Process

1. **Automated Checks**: Must pass before review
   - Linting
   - Tests
   - Security scans
   - Coverage thresholds

2. **Peer Review**: At least one approval required
   - Review code quality
   - Check for bugs
   - Verify tests
   - Validate documentation

3. **Address Feedback**:
```bash
# Make requested changes
git add .
git commit -m "fix: address review feedback"
git push
```

4. **Merge**: Once approved and checks pass

---

## Release Process

### 1. Create Release Branch

```bash
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0
```

### 2. Prepare Release

```bash
# Update version in package.json, setup.py, etc.
npm version 1.2.0

# Update CHANGELOG
# Add release notes
# Final testing
```

### 3. Merge to Main

```bash
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags
```

### 4. Merge Back to Develop

```bash
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop
```

### 5. Delete Release Branch

```bash
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

---

## Hotfix Process

### 1. Create Hotfix Branch

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix
```

### 2. Fix the Issue

```bash
# Make necessary changes
git add .
git commit -m "fix: resolve critical security vulnerability"
```

### 3. Merge to Main

```bash
git checkout main
git merge --no-ff hotfix/critical-security-fix
git tag -a v1.2.1 -m "Hotfix: critical security fix"
git push origin main --tags
```

### 4. Merge to Develop

```bash
git checkout develop
git merge --no-ff hotfix/critical-security-fix
git push origin develop
```

### 5. Cleanup

```bash
git branch -d hotfix/critical-security-fix
git push origin --delete hotfix/critical-security-fix
```

---

## Best Practices

### Branching

✅ **Do**:
- Keep branches short-lived
- Sync with base branch regularly
- Use descriptive branch names
- Delete merged branches
- One feature per branch

❌ **Don't**:
- Commit directly to main/develop
- Let branches become stale
- Mix multiple features in one branch
- Create nested feature branches
- Use generic names like `fix` or `update`

### Commits

✅ **Do**:
- Write clear commit messages
- Make atomic commits
- Commit frequently
- Use conventional commit format
- Reference issues

❌ **Don't**:
- Commit generated files
- Make huge commits
- Use vague messages like "fix stuff"
- Commit commented-out code
- Commit secrets or credentials

### Pull Requests

✅ **Do**:
- Keep PRs small and focused
- Write detailed descriptions
- Link related issues
- Respond to reviews promptly
- Test before requesting review
- Update documentation

❌ **Don't**:
- Create massive PRs
- Ignore review feedback
- Force push after review starts
- Merge without approvals
- Leave unresolved comments

### Git Commands

```bash
# Amend last commit (if not pushed)
git commit --amend

# Interactive rebase (clean up history)
git rebase -i HEAD~3

# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Stash changes temporarily
git stash
git stash pop

# View commit history
git log --oneline --graph --all

# Find who changed a line
git blame <file>

# Show changes in a commit
git show <commit-hash>
```

---

## Branch Protection Rules

### Main Branch

- ✅ Require pull request before merging
- ✅ Require approvals (1+)
- ✅ Dismiss stale approvals
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require signed commits
- ✅ Include administrators
- ✅ Restrict who can push
- ✅ Allow force pushes: NO
- ✅ Allow deletions: NO

### Develop Branch

- ✅ Require pull request before merging
- ✅ Require approvals (1+)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Allow force pushes: NO

---

## Versioning Strategy

We use [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

Example: 1.2.3
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Pre-release Versions

```
1.2.3-alpha.1
1.2.3-beta.2
1.2.3-rc.1
```

---

## Quick Reference

### Common Workflows

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Update feature with develop changes
git checkout develop
git pull origin develop
git checkout feature/my-feature
git rebase develop

# Prepare for PR
git push -u origin feature/my-feature
# Then create PR on GitHub

# After PR merged
git checkout develop
git pull origin develop
git branch -d feature/my-feature
```

---

**Last Updated**: 2024-11-08
