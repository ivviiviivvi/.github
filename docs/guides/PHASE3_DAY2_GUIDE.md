# Phase 3 Day 2 Guide - Production Script Testing

**Date:** 2026-01-19\
**Status:** Ready to Execute\
**Duration:** ~2-3 hours

______________________________________________________________________

## Overview

Day 2 focuses on **production script testing** with the newly validated tokens.
We'll test each script with its designated token to ensure real-world operations
work correctly.

______________________________________________________________________

## Pre-Flight Checklist

Before starting, verify the environment:

```bash
# 1. Verify tokens are loaded
env | grep "ORG_.*_TOKEN" | wc -l
# Expected: 4 (all tokens present)

# 2. Test basic connectivity
curl -H "Authorization: token $ORG_LABEL_SYNC_TOKEN" \
     https://api.github.com/user | jq '.login'
# Expected: Your GitHub username

# 3. Check rate limits
for token in ORG_LABEL_SYNC_TOKEN ORG_PROJECT_ADMIN_TOKEN \
             ORG_ONBOARDING_TOKEN ORG_REPO_ANALYSIS_TOKEN; do
  echo -n "$token: "
  curl -s -H "Authorization: token ${!token}" \
       https://api.github.com/rate_limit | jq -r '.rate.remaining'
done
# Expected: All >4500
```

______________________________________________________________________

## Test 1: Label Synchronization

**Token:** `org-label-sync-token`\
**Script:**
`automation/scripts/sync_labels.py`\
**Purpose:** Verify label operations work
with segregated token

### Dry-Run Test

```bash
cd /workspace

# Test with single repository (dry-run)
python3 automation/scripts/sync_labels.py \
  --token-name org-label-sync-token \
  --repo .github \
  --dry-run

# Expected output:
# - ✅ Token retrieved from environment
# - ✅ Connected to GitHub API
# - ✅ Label operations planned (no actual changes)
# - ✅ No authentication errors
```

### Production Test (Optional)

If dry-run succeeds and you want to test real sync:

```bash
# Sync labels to a test repository
python3 automation/scripts/sync_labels.py \
  --token-name org-label-sync-token \
  --repo .github \
  --force

# ⚠️ This makes real changes - use with caution
```

### Success Criteria

- ✅ Script runs without authentication errors
- ✅ GitHub API rate limit check passes
- ✅ Label operations are executed correctly
- ✅ Token scope is sufficient for operations

______________________________________________________________________

## Test 2: Repository Analysis

**Token:** `org-repo-analysis-token`\
**Script:**
`automation/scripts/web_crawler.py`\
**Purpose:** Verify read-only analysis
operations

### Test Command

```bash
cd /workspace

# Analyze organization repositories
python3 automation/scripts/web_crawler.py \
  --token-name org-repo-analysis-token \
  --org {{ORG_NAME}} \
  --output /tmp/repo-analysis.json

# Expected output:
# - ✅ Token retrieved from environment
# - ✅ Repository data fetched
# - ✅ Analysis completed
# - ✅ JSON output created
```

### Verify Output

```bash
# Check analysis results
cat /tmp/repo-analysis.json | jq '.repositories | length'
# Expected: Number of repositories in org

# View sample data
cat /tmp/repo-analysis.json | jq '.repositories[0] | keys'
# Expected: Repository metadata fields
```

### Success Criteria

- ✅ Script runs without errors
- ✅ All repositories analyzed
- ✅ Output file contains valid JSON
- ✅ Read-only token has sufficient permissions

______________________________________________________________________

## Test 3: Project Management

**Token:** `org-project-admin-token`\
**Script:**
`scripts/complete-project-setup.sh`\
**Purpose:** Verify GitHub Projects
operations

### Test Command

```bash
cd /workspace

# Set token for project operations
export GH_TOKEN=$(echo $ORG_PROJECT_ADMIN_TOKEN)

# Test project access (list existing projects)
gh project list --owner {{ORG_NAME}} --limit 5

# Expected output:
# - ✅ List of organization projects
# - ✅ No authentication errors
```

### Optional: Create Test Project

```bash
# Create a test project (if you want to verify write access)
python3 scripts/configure-github-projects.py --dry-run

# Expected:
# - ✅ Project configuration validated
# - ✅ No authentication errors
# - ✅ Dry-run shows planned operations
```

### Success Criteria

- ✅ Project listing works
- ✅ Token has project scope access
- ✅ No permission errors
- ✅ gh CLI authenticates correctly

______________________________________________________________________

## Test 4: GitHub Actions Workflow

**Workflow:** `.github/workflows/token-health-check.yml`\
**Time:** First run at
8:00 AM UTC\
**Token Used:** Organization secret (not env vars)

### Monitor First Run

```bash
# Check workflow status
gh workflow view token-health-check.yml

# View recent runs
gh run list --workflow=token-health-check.yml --limit 5

# Watch live run (if in progress)
gh run watch
```

### Success Criteria

- ✅ Workflow triggers on schedule
- ✅ No authentication failures
- ✅ All token validation passes
- ✅ No rate limit issues

______________________________________________________________________

## Rate Limit Monitoring

Throughout the day, monitor rate limits:

```bash
# Quick rate limit check script
cat > /tmp/check-rates.sh << 'EOF'
#!/bin/bash
echo "Rate Limits at $(date)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for token_var in ORG_LABEL_SYNC_TOKEN ORG_PROJECT_ADMIN_TOKEN \
                 ORG_ONBOARDING_TOKEN ORG_REPO_ANALYSIS_TOKEN; do
  token_value="${!token_var}"
  remaining=$(curl -s -H "Authorization: token $token_value" \
              https://api.github.com/rate_limit | jq -r '.rate.remaining')
  echo "$token_var: $remaining/5000"
done
EOF

chmod +x /tmp/check-rates.sh

# Run it
/tmp/check-rates.sh
```

### Rate Limit Thresholds

- 🟢 **>4000**: Excellent (80%+ available)
- 🟡 **2000-4000**: Good (40-80% available)
- 🟠 **500-2000**: Monitor closely (10-40% available)
- 🔴 **\<500**: Critical (\< 10% available)

______________________________________________________________________

## Troubleshooting

### Issue: "Token not found in environment"

**Solution:**

```bash
# Verify tokens are loaded
source ~/.github-tokens
env | grep "ORG_.*_TOKEN"

# If missing, reload bashrc
source ~/.bashrc
```

### Issue: "401 Unauthorized"

**Solution:**

```bash
# Test token manually
curl -H "Authorization: token $ORG_LABEL_SYNC_TOKEN" \
     https://api.github.com/user

# If fails, token may be expired - check in GitHub settings
```

### Issue: "403 Rate Limit Exceeded"

**Solution:**

```bash
# Check rate limit reset time
curl -s -H "Authorization: token $ORG_LABEL_SYNC_TOKEN" \
     https://api.github.com/rate_limit | jq '.rate.reset'

# Wait until reset time, then retry
```

### Issue: "Insufficient scopes"

**Solution:**

```bash
# Check token scopes
curl -I -H "Authorization: token $ORG_LABEL_SYNC_TOKEN" \
     https://api.github.com/user | grep -i 'x-oauth-scopes'

# Compare with required scopes in TOKEN_REGISTRY.md
# If missing, may need to regenerate token with correct scopes
```

______________________________________________________________________

## Documentation Updates

At end of day, update:

1. **docs/PHASE3_MONITORING_STATUS.md**

   - Mark Day 2 as complete
   - Add test results to metrics table
   - Note any issues encountered

1. **docs/TOKEN_REGISTRY.md**

   - Add Day 2 audit log entries
   - Record token usage patterns
   - Update rate limit observations

1. **PHASE3_DAY2_CHECKLIST.md** (create if needed)

   - Checklist of all tests performed
   - Pass/fail status for each test
   - Issues to address

______________________________________________________________________

## Success Metrics

**Day 2 Success Criteria:**

- ✅ All 4 scripts tested successfully
- ✅ No authentication errors
- ✅ Rate limits remain healthy (>80%)
- ✅ GitHub Actions workflow runs successfully
- ✅ Documentation updated
- ✅ No regressions from Day 1

**If all criteria met:** Proceed to Day 3 (extended monitoring)

**If issues found:** Document, troubleshoot, and resolve before proceeding

______________________________________________________________________

## Next Steps (Day 3+)

After Day 2 testing:

- **Days 3-4:** Extended monitoring, edge case testing
- **Days 5-6:** Team training (if applicable), stress testing
- **Day 7:** Final validation, Phase 3 sign-off document
- **Phase 4:** Migrate to 1Password service account

______________________________________________________________________

## Quick Reference

```bash
# Source tokens
source ~/.github-tokens

# Check tokens loaded
env | grep ORG_

# Test label sync
python3 automation/scripts/sync_labels.py --dry-run --repo .github

# Test repo analysis
python3 automation/scripts/web_crawler.py --org {{ORG_NAME}}

# Check rate limits
/tmp/check-rates.sh

# Monitor workflow
gh run list --workflow=token-health-check.yml

# Update docs
vi docs/PHASE3_MONITORING_STATUS.md
```

______________________________________________________________________

**Prepared by:** GitHub Copilot\
**Date:** 2026-01-18\
**Phase:** 3 (Day 2
Preparation)\
**Related:** master-org-token-011726 contextual awareness solution
