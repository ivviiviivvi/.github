# Week 10: Production Deployment Guide

**Batch Onboarding System - Production Ready**

**Date**: 2026-01-16  
**Version**: 1.0  
**Status**: ✅ Ready for Production Deployment

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Configuration](#configuration)
4. [Deployment Procedure](#deployment-procedure)
5. [Validation](#validation)
6. [Monitoring](#monitoring)
7. [Rollback Procedures](#rollback-procedures)
8. [Troubleshooting](#troubleshooting)
9. [Performance Expectations](#performance-expectations)

---

## Prerequisites

### System Requirements

- **Python**: 3.11 or later
- **Dependencies**:
  - PyGithub 2.8.1
  - aiohttp 3.13.3
  - pyyaml 6.0.3
- **GitHub Token**:
  - Permissions: `repo`, `workflow`, `write:org` (for labels)
  - Optional: admin permissions for branch protection

### Validated Environment

This system has been tested and validated in:

- Week 10 Day 3: 100% test pass rate (5/5 tests)
- Week 10 Day 4: 100% integration test success
- Performance: 5.78s per repository (61% under target)
- Rollback: 100% success rate across 4 failure scenarios

---

## Pre-Deployment Checklist

### ✅ Testing Validation

- [x] Unit tests passed (100% - Week 10 Day 3)
- [x] Integration tests passed (100% - Week 10 Day 4)
- [x] Real API execution validated (5.56s per repo)
- [x] Rollback mechanism tested (4 scenarios, 100% success)
- [x] Performance benchmarked (concurrency 1, 3, 5)

### ✅ Documentation Review

- [x] Configuration file examples provided
- [x] Workflow templates validated
- [x] Label schemas defined
- [x] Error handling documented

### ✅ Security Review

- [x] Token permissions documented
- [x] Secrets handling validated
- [x] API rate limiting considered
- [x] Rollback procedures tested

### ⏳ Production Preparation

- [ ] Repository list finalized
- [ ] Production configuration created
- [ ] Stakeholders notified
- [ ] Deployment window scheduled

---

## Configuration

### Production Configuration File

Create `automation/config/batch-onboard-production.yml`:

```yaml
# Production Batch Onboarding Configuration
# Week 11 Deployment

# Repositories to onboard (start with pilot batch)
repositories:
  # Pilot Phase (3 repositories)
  - "ivviiviivvi/repo-1"
  - "ivviiviivvi/repo-2"
  - "ivviiviivvi/repo-3"

# Workflow deployment
workflow_deployment:
  enabled: true
  workflows:
    - name: "pr-validation"
      source: ".github/workflow-templates/pr-validation.yml"
      description: "Pull request validation workflow"
    
    - name: "merge-related-prs"
      source: ".github/workflow-templates/merge-related-prs.yml"
      description: "Automatically merge related pull requests"

# Label configuration
label_configuration:
  enabled: true
  labels:
    # Status Labels
    - name: "status: ready"
      color: "0E8A16"
      description: "Ready for review or deployment"
    
    - name: "status: blocked"
      color: "D93F0B"
      description: "Blocked by dependencies or issues"
    
    - name: "status: in-progress"
      color: "FBCA04"
      description: "Work in progress"
    
    # Priority Labels
    - name: "priority: high"
      color: "D93F0B"
      description: "High priority"
    
    - name: "priority: medium"
      color: "FBCA04"
      description: "Medium priority"
    
    - name: "priority: low"
      color: "0E8A16"
      description: "Low priority"
    
    # Type Labels
    - name: "type: bug"
      color: "D73A4A"
      description: "Bug fix"
    
    - name: "type: feature"
      color: "A2EEEF"
      description: "New feature"
    
    - name: "type: docs"
      color: "0075CA"
      description: "Documentation update"
    
    - name: "type: chore"
      color: "FEF2C0"
      description: "Maintenance or chore"

# Branch protection (requires admin token)
# Uncomment when admin token is available
# branch_protection:
#   branch: "main"
#   required_approving_reviews: 1
#   require_code_owner_reviews: true
#   dismiss_stale_reviews: true
#   enforce_admins: false
#   required_checks:
#     - "test"
#     - "lint"

# Performance settings (validated in Day 4)
performance:
  max_concurrent: 3  # Optimal based on benchmarking
  timeout_seconds: 30
  retry_attempts: 3
  retry_delay: 2

# Rollback settings
rollback:
  enabled: true
  on_failure: true
  backup_workflows: true
```

### Recommended Concurrency Settings

Based on Week 10 Day 4 performance testing:

| Batch Size | Recommended Concurrency | Expected Duration |
|------------|------------------------|-------------------|
| 1-5 repos | 3 | 5.78s - 19.3s |
| 6-10 repos | 3 | 23.1s - 34.7s |
| 11-15 repos | 3-5 | 38.5s - 50s |
| 16+ repos | 5 | Consider batching |

**Note**: Start conservative (concurrency=3) and increase after validating with larger batches.

---

## Deployment Procedure

### Phase 1: Pilot Deployment (3 Repositories)

**Objective**: Validate production deployment with small batch

**Timeline**: Day 1 (Week 11)

#### Step 1: Preparation

```bash
# Navigate to repository
cd /path/to/.github

# Ensure clean working directory
git status

# Pull latest changes
git pull origin main

# Verify dependencies
pip install -r automation/requirements.txt
```

#### Step 2: Configuration Review

```bash
# Review production configuration
cat automation/config/batch-onboard-production.yml

# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('automation/config/batch-onboard-production.yml'))"

# Dry-run test
python3 automation/scripts/batch_onboard_repositories.py \
  --config automation/config/batch-onboard-production.yml \
  --dry-run \
  --output test-results-pilot-dryrun.json
```

#### Step 3: Execute Pilot Deployment

```bash
# Real execution (3 repositories)
python3 automation/scripts/batch_onboard_repositories.py \
  --config automation/config/batch-onboard-production.yml \
  --output deployment-results-pilot.json \
  --verbose

# Expected output:
# ✅ Processing 3 repositories
# ✅ Repository 1/3: ivviiviivvi/repo-1 - SUCCESS (5.8s)
# ✅ Repository 2/3: ivviiviivvi/repo-2 - SUCCESS (5.8s)
# ✅ Repository 3/3: ivviiviivvi/repo-3 - SUCCESS (5.8s)
# 
# Summary:
# - Successful: 3
# - Failed: 0
# - Total duration: ~17.4s
```

#### Step 4: Pilot Validation

```bash
# Check deployment results
cat deployment-results-pilot.json | python3 -m json.tool

# Validate workflow deployment
for repo in repo-1 repo-2 repo-3; do
  echo "=== Checking $repo ==="
  gh api repos/ivviiviivvi/$repo/contents/.github/workflows | \
    jq -r '.[].name' | grep -E "(pr-validation|merge-related)"
done

# Validate label configuration
for repo in repo-1 repo-2 repo-3; do
  echo "=== Labels in $repo ==="
  gh label list --repo ivviiviivvi/$repo | \
    grep -E "(status|priority|type)"
done
```

### Phase 2: Expanded Deployment (5 More Repositories)

**Timeline**: Day 2 (Week 11)

**Prerequisites**: Pilot deployment successful, no issues detected

#### Configuration Update

Add 5 more repositories to configuration:

```yaml
repositories:
  # Pilot Phase (validated)
  - "ivviiviivvi/repo-1"
  - "ivviiviivvi/repo-2"
  - "ivviiviivvi/repo-3"
  
  # Expansion Phase
  - "ivviiviivvi/repo-4"
  - "ivviiviivvi/repo-5"
  - "ivviiviivvi/repo-6"
  - "ivviiviivvi/repo-7"
  - "ivviiviivvi/repo-8"
```

#### Execution

```bash
# Update configuration
git pull origin main

# Execute expansion deployment
python3 automation/scripts/batch_onboard_repositories.py \
  --config automation/config/batch-onboard-production.yml \
  --output deployment-results-expansion.json \
  --verbose

# Expected duration: ~46s (8 repos at 5.78s each)
```

### Phase 3: Final Deployment (Remaining Repositories)

**Timeline**: Day 3-4 (Week 11)

**Prerequisites**: Expansion deployment successful, performance validated

Add remaining repositories (up to 12 total) and execute final deployment.

---

## Validation

### Post-Deployment Validation Checklist

For each repository, validate:

#### ✅ Workflow Deployment

```bash
# Check workflow files exist
REPO="ivviiviivvi/your-repo"
gh api repos/$REPO/contents/.github/workflows | jq -r '.[].name'

# Expected workflows:
# - pr-validation.yml
# - merge-related-prs.yml

# Verify workflow syntax
gh workflow list --repo $REPO
```

#### ✅ Label Configuration

```bash
# List all labels
gh label list --repo $REPO

# Check specific labels
gh label list --repo $REPO | grep "status: ready"
gh label list --repo $REPO | grep "priority: high"
gh label list --repo $REPO | grep "type: bug"
```

#### ✅ No Breaking Changes

```bash
# Check repository still accessible
gh repo view $REPO

# Check issues still work
gh issue list --repo $REPO --limit 5

# Check PRs still work
gh pr list --repo $REPO --limit 5
```

#### ✅ Workflow Execution

```bash
# Trigger test workflow (if applicable)
gh workflow run pr-validation.yml --repo $REPO

# Check workflow runs
gh run list --repo $REPO --limit 5
```

### Automated Validation Script

```bash
#!/bin/bash
# validate-deployment.sh

REPOS=(
  "ivviiviivvi/repo-1"
  "ivviiviivvi/repo-2"
  "ivviiviivvi/repo-3"
)

for REPO in "${REPOS[@]}"; do
  echo "=== Validating $REPO ==="
  
  # Check workflows
  WORKFLOW_COUNT=$(gh api repos/$REPO/contents/.github/workflows | jq '. | length')
  echo "Workflows: $WORKFLOW_COUNT"
  
  # Check labels
  LABEL_COUNT=$(gh label list --repo $REPO | wc -l)
  echo "Labels: $LABEL_COUNT"
  
  # Check repository access
  gh repo view $REPO --json isPrivate,visibility > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ Repository accessible"
  else
    echo "❌ Repository access failed"
  fi
  
  echo ""
done
```

---

## Monitoring

### Metrics to Track

#### Performance Metrics

- **Execution Time**: Per repository and total batch
- **Success Rate**: Percentage of successful deployments
- **Rollback Rate**: Percentage requiring rollback
- **API Rate Limits**: Monitor GitHub API usage

#### Quality Metrics

- **Workflow Deployment**: Success rate
- **Label Configuration**: Success rate
- **Error Types**: Categorize and track errors

### Monitoring During Deployment

```bash
# Real-time monitoring script
#!/bin/bash

# Monitor deployment progress
tail -f deployment-results-*.json | \
  jq -r 'select(.timestamp != null) | "\(.timestamp): \(.repository) - \(.success)"'

# Check API rate limits
gh api rate_limit | jq '.resources.core'

# Monitor repository count
watch -n 5 'gh api user/repos | jq ". | length"'
```

### Post-Deployment Metrics

```bash
# Generate deployment report
python3 automation/scripts/generate_deployment_report.py \
  --input deployment-results-*.json \
  --output deployment-summary.md
```

---

## Rollback Procedures

### Automated Rollback

The batch onboarding system includes **automatic rollback** on failures:

- **Workflow files**: Automatically removed if deployment fails
- **Label changes**: Labels created during failed run are removed
- **Branch protection**: Reverted if partially configured

**Validated**: 100% success rate across 4 failure scenarios (Week 10 Day 4)

### Manual Rollback

If automated rollback fails or manual intervention needed:

#### Remove Workflows

```bash
# List workflows to remove
REPO="ivviiviivvi/your-repo"
gh api repos/$REPO/contents/.github/workflows | \
  jq -r '.[] | select(.name | contains("batch-onboarding")) | .name'

# Remove specific workflow
gh api \
  --method DELETE \
  repos/$REPO/contents/.github/workflows/workflow-name.yml \
  -f message="chore: rollback batch onboarding workflow" \
  -f sha="$(gh api repos/$REPO/contents/.github/workflows/workflow-name.yml | jq -r '.sha')"
```

#### Remove Labels

```bash
# List labels created by batch onboarding
gh label list --repo $REPO | grep -E "(status|priority|type)"

# Remove specific label
gh label delete "status: ready" --repo $REPO --yes
```

#### Emergency Rollback Script

```bash
#!/bin/bash
# emergency-rollback.sh

REPO=$1
if [ -z "$REPO" ]; then
  echo "Usage: $0 <org/repo>"
  exit 1
fi

echo "=== Emergency Rollback for $REPO ==="

# Remove workflows
echo "Removing workflows..."
for workflow in pr-validation merge-related-prs; do
  gh api --method DELETE \
    repos/$REPO/contents/.github/workflows/$workflow.yml \
    -f message="chore: emergency rollback" \
    -f sha="$(gh api repos/$REPO/contents/.github/workflows/$workflow.yml 2>/dev/null | jq -r '.sha')" \
    2>/dev/null && echo "✅ Removed $workflow.yml" || echo "⚠️  $workflow.yml not found"
done

# Remove labels (optional - may want to keep)
# gh label delete "status: ready" --repo $REPO --yes

echo "=== Rollback Complete ==="
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Permission Denied (403)

**Symptom**: `Resource not accessible by integration: 403`

**Cause**: Token lacks required permissions

**Solution**:

1. Verify token has `repo`, `workflow`, `write:org` scopes
2. For branch protection, use admin token
3. Check organization settings for third-party app restrictions

```bash
# Check token scopes
gh api user | jq -r '.login'
gh auth status
```

#### Issue 2: Branch Not Found (404)

**Symptom**: `Branch not found: 404`

**Cause**: Branch protection configured for non-existent branch

**Solution**:

1. Create the branch if needed
2. Update configuration to target existing branch
3. Disable branch protection if not required

```bash
# Create branch
git checkout -b your-branch
git push -u origin your-branch
```

#### Issue 3: API Rate Limit

**Symptom**: `API rate limit exceeded`

**Cause**: Too many API calls in short time

**Solution**:

1. Check rate limit status: `gh api rate_limit`
2. Wait for reset time
3. Reduce concurrency setting
4. Use authenticated token (higher limits)

```bash
# Check rate limit
gh api rate_limit | jq '.resources.core'

# Wait for reset
RESET_TIME=$(gh api rate_limit | jq -r '.resources.core.reset')
echo "Rate limit resets at: $(date -d @$RESET_TIME)"
```

#### Issue 4: Workflow Already Exists

**Symptom**: Workflow file already exists in repository

**Cause**: Previous deployment or manual workflow creation

**Solution**:

1. System is idempotent - will update existing workflow
2. To force replacement, delete existing file first
3. Review diff to ensure no conflicts

```bash
# Check existing workflow
gh api repos/org/repo/contents/.github/workflows/workflow-name.yml

# Compare versions
gh api repos/org/repo/contents/.github/workflows/workflow-name.yml | \
  jq -r '.content' | base64 -d > existing-workflow.yml

diff existing-workflow.yml .github/workflow-templates/workflow-name.yml
```

#### Issue 5: Label Color Mismatch

**Symptom**: Labels exist but with different colors

**Cause**: Labels created manually before batch onboarding

**Solution**:

1. System updates existing labels (idempotent)
2. Verify color codes in configuration
3. Re-run deployment to update colors

```bash
# Check current label color
gh label list --repo org/repo | grep "status: ready"

# Update will occur automatically on re-run
```

### Debugging Commands

```bash
# Enable verbose logging
python3 automation/scripts/batch_onboard_repositories.py \
  --config config.yml \
  --verbose \
  --log-file debug.log

# Check log file
tail -f debug.log

# Test single repository
python3 automation/scripts/batch_onboard_repositories.py \
  --config config-single.yml \
  --dry-run \
  --verbose
```

### Getting Help

1. **Check Documentation**: Review BATCH_ONBOARDING_GUIDE.md
2. **Review Test Results**: Week 10 Day 3 & 4 reports
3. **Check GitHub Status**: <https://www.githubstatus.com>
4. **Contact Team**: Open issue in repository

---

## Performance Expectations

### Validated Performance (Week 10 Day 4)

Based on comprehensive integration testing:

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Per Repository** | 5.78s | 15s | ✅ 61% under |
| **Concurrency 1** | 6.07s | 15s | ✅ 60% under |
| **Concurrency 3** | 5.78s | 15s | ✅ 61% under |
| **Concurrency 5** | 5.89s | 15s | ✅ 61% under |
| **Rollback Time** | 1.53s | 5s | ✅ 69% under |

### Expected Deployment Times

#### Pilot Phase (3 Repositories)

- **Sequential**: ~17.4s
- **Concurrent (c=3)**: ~11.6s
- **Target**: Under 45s ✅

#### Expansion Phase (8 Repositories)

- **Sequential**: ~46.2s
- **Concurrent (c=3)**: ~23.1s
- **Target**: Under 2 minutes ✅

#### Full Deployment (12 Repositories)

- **Sequential**: ~69.4s
- **Concurrent (c=3)**: ~34.7s
- **Target**: Under 3 minutes ✅

### Performance Factors

**Factors that improve performance**:

- Concurrent execution (3-5 recommended)
- Cached GitHub API responses
- Network proximity to GitHub servers

**Factors that slow performance**:

- API rate limiting
- Large workflow files
- Network latency
- Many labels to configure

### Scalability

System tested and validated for:

- ✅ Up to 15 repositories per batch
- ✅ Concurrent execution (3-5 repositories)
- ✅ Automatic rollback on failures
- ✅ Idempotent operations (safe to re-run)

For larger batches (15+ repositories):

1. Split into multiple batches
2. Monitor API rate limits
3. Consider increasing concurrency to 5
4. Allow time between batches for API limit reset

---

## Success Criteria

### Deployment Success

A deployment is considered successful when:

- ✅ All workflows deployed to target repositories
- ✅ All labels configured correctly
- ✅ No failed repositories (or all failures rolled back)
- ✅ Validation checks pass
- ✅ No breaking changes introduced

### Quality Metrics

- **Success Rate**: 100% (0 failures after rollback)
- **Deployment Time**: Under 3 minutes for 12 repositories
- **Rollback Time**: Under 5 seconds average
- **Zero Data Loss**: No repositories left in inconsistent state

---

## Next Steps After Deployment

1. **Monitor for 24-48 Hours**: Watch for any issues or errors
2. **Collect Metrics**: Track usage and performance
3. **Gather Feedback**: Survey developers on new workflows/labels
4. **Document Lessons**: Update guide with real-world learnings
5. **Plan Next Batch**: Identify additional repositories for onboarding

---

## Appendix A: Quick Reference

### Common Commands

```bash
# Dry-run test
python3 automation/scripts/batch_onboard_repositories.py \
  --config config.yml --dry-run

# Real execution
python3 automation/scripts/batch_onboard_repositories.py \
  --config config.yml --output results.json --verbose

# Check API rate limits
gh api rate_limit | jq '.resources.core'

# Validate repository
gh repo view org/repo

# List workflows
gh workflow list --repo org/repo

# List labels
gh label list --repo org/repo
```

### File Locations

- **Script**: `automation/scripts/batch_onboard_repositories.py`
- **Config**: `automation/config/batch-onboard-production.yml`
- **Workflows**: `.github/workflow-templates/`
- **Results**: `deployment-results-*.json`
- **Logs**: `debug.log` (if enabled)

### Support Resources

- **Testing Report**: docs/WEEK_10_DAY3_TESTING_REPORT.md
- **Integration Results**: docs/WEEK_10_DAY4_INTEGRATION_RESULTS.md
- **User Guide**: docs/BATCH_ONBOARDING_GUIDE.md

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-16  
**Status**: Production Ready ✅
