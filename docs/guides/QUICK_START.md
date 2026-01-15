# Quick Start Guide

Get up and running with this gold standard repository template in minutes.

## Table of Contents

- [For New Repositories](#for-new-repositories)
- [For Existing Repositories](#for-existing-repositories)
- [Essential Configuration](#essential-configuration)
- [Optional Enhancements](#optional-enhancements)
- [Verification](#verification)

---

## For New Repositories

### 1. Use This Template

If this is a `.github` organization repository:

```bash
# The files automatically apply to all repos in your organization
# Nothing to do! 🎉
```

If you want to copy to a specific repository:

```bash
# Clone this repository
git clone https://github.com/ivi374forivi/.github.git

# Copy files to your new repository
cp -r .github /path/to/your/repo/
cp CODEOWNERS /path/to/your/repo/
cp .gitattributes /path/to/your/repo/
cp renovate.json /path/to/your/repo/
cp .pre-commit-config.yaml /path/to/your/repo/
```

### 2. Customize Files

Update these files with your project-specific information:

```bash
# 1. CODEOWNERS - Replace with your GitHub username/team
sed -i 's/@ivi374forivi/@your-username/g' CODEOWNERS

# 2. renovate.json - Update assignees and reviewers
# Edit renovate.json manually

# 3. README.md - Create your own or use the template
```

### 3. Enable GitHub Features

Navigate to **Settings** → **Security & analysis**:

- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Secret scanning
- ✅ Push protection
- ✅ Code scanning (CodeQL)

### 4. Set Up Branch Protection

Go to **Settings** → **Branches** → **Add rule**:

**For `main` branch**:

```
✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Dismiss stale reviews
  ✅ Require review from CODEOWNERS
✅ Require status checks to pass
  ✅ Require branches to be up to date
  Add: ci/tests, security/scan, etc.
✅ Require signed commits
✅ Require linear history
✅ Include administrators
✅ Restrict pushes
```

See `BRANCH_PROTECTION.md` for detailed setup.

### 5. Add Secrets

Go to **Settings** → **Secrets and variables** → **Actions**:

```bash
# Required for Claude AI
CLAUDE_CODE_OAUTH_TOKEN

# Optional but recommended
CODECOV_TOKEN         # For code coverage
SNYK_TOKEN           # For security scanning
SLACK_WEBHOOK        # For notifications
```

### 6. Initialize Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Test it works
pre-commit run --all-files
```

---

## For Existing Repositories

### Step 1: Backup Your Current Setup

```bash
# Create backup branch
git checkout -b backup-before-gold-standard
git push origin backup-before-gold-standard
```

### Step 2: Copy Files Selectively

```bash
# Create feature branch
git checkout -b feat/add-gold-standard-practices

# Copy workflow files
mkdir -p .github/workflows
cp /path/to/template/.github/workflows/*.yml .github/workflows/

# Copy configuration files
cp /path/to/template/CODEOWNERS .
cp /path/to/template/.gitattributes .
cp /path/to/template/renovate.json .
cp /path/to/template/.pre-commit-config.yaml .

# Copy documentation
cp /path/to/template/BEST_PRACTICES.md .
cp /path/to/template/GIT_WORKFLOW.md .
cp /path/to/template/DOCKER_BEST_PRACTICES.md .
```

### Step 3: Merge Existing Configurations

If you already have these files, merge carefully:

**package.json**: Add scripts

```json
{
  "scripts": {
    "lint": "eslint .",
    "test": "jest",
    "benchmark": "node benchmarks/run.js",
    "type-check": "tsc --noEmit"
  }
}
```

**Existing workflows**: Keep your working workflows, add new ones

### Step 4: Test Incrementally

```bash
# Add and commit files in small batches
git add .github/workflows/codeql-analysis.yml
git commit -m "feat: add CodeQL security scanning"

git add .github/workflows/dependency-review.yml
git commit -m "feat: add dependency review workflow"

# Test each workflow before adding more
git push origin feat/add-gold-standard-practices
# Create PR and verify workflows run successfully
```

### Step 5: Update Documentation

```bash
# Update your README
cat >> README.md << EOF

## Development

See our comprehensive guides:
- [Best Practices](docs/guides/BEST_PRACTICES.md)
- [Git Workflow](docs/workflows/GIT_WORKFLOW.md)
- [Security](docs/reference/SECURITY_ADVANCED.md)
- [Docker](docs/guides/DOCKER_BEST_PRACTICES.md)
EOF
```

---

## Essential Configuration

### 1. Update CODEOWNERS

```bash
# .github/CODEOWNERS
* @your-org/core-team

# Language-specific
*.py @your-org/python-team
*.js @your-org/frontend-team
*.go @your-org/backend-team

# Security-sensitive
/SECURITY.md @your-org/security-team
/.github/workflows/security*.yml @your-org/security-team
```

### 2. Configure CodeQL

Edit `.github/workflows/codeql-analysis.yml`:

```yaml
matrix:
  language: ["javascript", "python"] # Add your languages
```

### 3. Customize Dependabot

Edit `dependabot.yml` to match your stack:

```yaml
version: 2
updates:
  # Keep only the package ecosystems you use
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 4. Set Up Labels

Run this script to create standard labels:

```bash
#!/bin/bash
# create-labels.sh

gh label create "bug" --color "d73a4a" --description "Something isn't working"
gh label create "enhancement" --color "a2eeef" --description "New feature or request"
gh label create "documentation" --color "0075ca" --description "Documentation improvements"
gh label create "security" --color "ee0701" --description "Security-related"
gh label create "dependencies" --color "0366d6" --description "Dependency updates"
gh label create "automated" --color "ededed" --description "Automated changes"

# Size labels
gh label create "size/xs" --color "00ff00"
gh label create "size/s" --color "00ee00"
gh label create "size/m" --color "ffaa00"
gh label create "size/l" --color "ff5500"
gh label create "size/xl" --color "ff0000"

# Run with: bash create-labels.sh
```

---

## Optional Enhancements

### Enable Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Add Code Coverage

**For JavaScript:**

```json
// package.json
{
  "scripts": {
    "test": "jest --coverage"
  },
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 70,
        "functions": 70,
        "lines": 70,
        "statements": 70
      }
    }
  }
}
```

**For Python:**

```ini
# .coveragerc
[run]
source = src
omit = */tests/*

[report]
fail_under = 70
```

### Set Up Notifications

**Slack Integration:**

1. Create Slack webhook
1. Add to repository secrets: `SLACK_WEBHOOK`
1. Workflows will automatically notify on failures

**Email Notifications:**

Go to **Settings** → **Notifications** → Configure email preferences

### Install Recommended Apps

See `GITHUB_APPS_INTEGRATIONS.md` for full list:

1. [Codecov](https://github.com/marketplace/codecov) - Code coverage
1. [Snyk](https://github.com/marketplace/snyk) - Security scanning
1. [All Contributors](https://github.com/marketplace/all-contributors) -
   Contributor recognition

---

## Verification

### Verify Setup Checklist

Run through this checklist to ensure everything is configured:

```bash
# 1. Check workflows are present
ls .github/workflows/

# 2. Verify CODEOWNERS syntax
gh api repos/:owner/:repo/codeowners/errors

# 3. Test pre-commit hooks
pre-commit run --all-files

# 4. Verify branch protection
gh api repos/:owner/:repo/branches/main/protection

# 5. Check secrets are set
gh secret list

# 6. Validate workflows
gh workflow list

# 7. Run a test workflow
gh workflow run ci-advanced.yml
```

### Expected Results

After setup, you should have:

✅ **Security**

- CodeQL scanning running on schedule
- Dependabot opening PRs for updates
- Secret scanning enabled
- SBOM generated on releases

✅ **Automation**

- PRs auto-labeled based on content
- New contributors welcomed
- Stale issues managed
- Release notes auto-generated

✅ **Quality**

- Code coverage tracked
- PR checks enforced
- Commit messages validated
- Links checked in docs

✅ **Documentation**

- Comprehensive guides available
- Templates for issues/PRs
- Changelog maintained
- Contributors recognized

---

## Common Issues

### Issue: Workflows Not Running

**Solution**:

```bash
# Check workflow permissions
# Settings → Actions → General → Workflow permissions
# Set to: "Read and write permissions"
```

### Issue: CodeQL Failing

**Solution**:

```yaml
# Reduce languages being scanned
matrix:
  language: ["javascript"] # Start with one language
```

### Issue: Too Many Dependabot PRs

**Solution**:

```yaml
# In dependabot.yml, reduce frequency and limit PRs
open-pull-requests-limit: 3
schedule:
  interval: "monthly" # Instead of weekly
```

### Issue: Pre-commit Too Slow

**Solution**:

```bash
# Skip slow hooks during development
SKIP=mypy,eslint git commit -m "message"

# Or disable for quick commits
git commit --no-verify -m "WIP: quick fix"
```

---

## Next Steps

After initial setup:

1. **Week 1**: Monitor workflows, fix any failures
1. **Week 2**: Customize workflows for your needs
1. **Week 3**: Enable optional features
1. **Week 4**: Train team on new processes
1. **Monthly**: Review metrics and optimize

### Learn More

- [BEST_PRACTICES.md](BEST_PRACTICES.md) - Comprehensive guide
- [GIT_WORKFLOW.md](../workflows/GIT_WORKFLOW.md) - Branching and commits
- [SECURITY_ADVANCED.md](../reference/SECURITY_ADVANCED.md) - Security details
- [DOCKER_BEST_PRACTICES.md](DOCKER_BEST_PRACTICES.md) - Container guide

---

## Getting Help

- 📖 Check documentation files in this repository
- 🐛 Open an issue for bugs or questions
- 💬 Discussions for general questions
- 📧 Contact: See SUPPORT.md

---

## Quick Command Reference

```bash
# Git workflow
git checkout -b feature/my-feature
git commit -m "feat: add feature"
git push -u origin feature/my-feature

# Pre-commit
pre-commit run --all-files
pre-commit autoupdate

# GitHub CLI
gh pr create --fill
gh workflow run ci-advanced.yml
gh issue create --label bug

# Testing
npm test -- --coverage
pytest --cov=. --cov-report=html

# Security
npm audit fix
pip-audit
trivy image myimage:latest
```

---

**Welcome to gold standard development! 🏆**

**Last Updated**: 2024-11-08
