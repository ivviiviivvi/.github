# Token Migration Phase 3: Production Monitoring & Validation

**Status**: 🟡 In Progress\
**Start Date**: 2026-01-18\
**Duration**: 7 days
(monitoring period)\
**Completion Target**: 2026-01-25

______________________________________________________________________

## Overview

Phase 3 focuses on validating that the 4 purpose-specific tokens work correctly
in production and monitoring for any authentication issues.

**Prerequisites:**

- ✅ Phase 1 Complete: All 4 tokens created and stored
- ✅ Phase 2 Complete: All 5 scripts updated
- ✅ Documentation: TOKEN_REGISTRY.md and guides updated
- ✅ Deployment: Changes pushed to main branch

______________________________________________________________________

## Quick Start

### Daily Validation

```bash
# Authenticate with 1Password
eval $(op signin)

# Run token health check
python3 scripts/validate-tokens.py

# Check token expiration dates
python3 scripts/validate-tokens.py --verbose
```

### Script Testing

```bash
# Test each script in dry-run mode
python3 automation/scripts/sync_labels.py --org ivviiviivvi --dry-run
python3 automation/scripts/web_crawler.py --dry-run
bash scripts/complete-project-setup.sh # (check if supports --dry-run)
```

______________________________________________________________________

## Monitoring Checklist

### Day 1 (2026-01-18) - Initial Validation

- [ ] **Authenticate 1Password CLI**: `eval $(op signin)`
- [ ] **Validate all 4 tokens exist**: Run token health check
- [ ] **Test org-label-sync-token**: Run sync_labels.py in dry-run
- [ ] **Test org-repo-analysis-token**: Run web_crawler.py in dry-run
- [ ] **Test org-project-admin-token**: Run complete-project-setup.sh
- [ ] **Check GitHub API rate limits**: Verify no exhaustion
- [ ] **Review logs**: Check for authentication errors
- [ ] **Verify gh CLI fallback**: Confirm utils.py uses gh token when available

**Expected Results:**

- All tokens authenticate successfully
- Scripts retrieve correct tokens from 1Password
- No "401 Unauthorized" or "Bad credentials" errors
- Rate limits show reasonable remaining quota

**Action if issues:**

- Check token scopes match requirements
- Verify 1Password item names are exact
- Re-run token creation if needed
- Check TOKEN_REGISTRY.md for correct expiration dates

______________________________________________________________________

### Day 2-3 (2026-01-19 to 2026-01-20) - Production Usage

- [ ] **Run scripts in production** (not dry-run)
- [ ] **Monitor GitHub Actions**: Check token-health-check.yml workflow
- [ ] **Review audit logs**: Check GitHub activity for token usage
- [ ] **Verify token segmentation**: Confirm each script uses correct token
- [ ] **Check rate limits again**: Ensure adequate headroom
- [ ] **Test utils.py fallback**: Temporarily disable gh CLI to test 1Password
  fallback

**Commands:**

```bash
# Production run (label sync)
python3 automation/scripts/sync_labels.py --org ivviiviivvi --repo .github

# Production run (repo analysis)
python3 automation/scripts/web_crawler.py --output reports/health-$(date +%Y%m%d).json

# Check GitHub Actions workflow
gh workflow view token-health-check.yml
gh run list --workflow=token-health-check.yml --limit 5
```

**Expected Results:**

- Scripts complete successfully in production
- GitHub Actions daily health check passes
- Each token used for its designated purpose
- No fallback to gh CLI when 1Password token should be used

______________________________________________________________________

### Day 4-5 (2026-01-21 to 2026-01-22) - Edge Cases

- [ ] **Test token rotation simulation**: Change one token value
- [ ] **Test 1Password CLI failure**: What happens if op command fails?
- [ ] **Test expired token simulation**: Set system date forward (if safe)
- [ ] **Test missing token**: Temporarily rename a 1Password item
- [ ] **Test utils.py error handling**: Verify clear error messages
- [ ] **Check secret_manager.py validation**: Confirm explicit token names
  required

**Commands:**

```bash
# Test with invalid token name (should error gracefully)
python3 -c "from automation.scripts.secret_manager import get_github_token; print(get_github_token('nonexistent-token'))"

# Test secret_manager requires token name
python3 -c "from automation.scripts.secret_manager import get_github_token; print(get_github_token())"

# Expected: ValueError with helpful message listing available tokens
```

**Expected Results:**

- Clear error messages when tokens not found
- Helpful guidance on which token to use
- No silent failures or unclear exceptions
- Graceful degradation where appropriate

______________________________________________________________________

### Day 6-7 (2026-01-23 to 2026-01-25) - Final Validation

- [ ] **Review all logs**: No authentication errors in 7 days
- [ ] **Verify rate limits**: All tokens have adequate quota
- [ ] **Check GitHub audit log**: Confirm token activity is as expected
- [ ] **Update TOKEN_REGISTRY.md**: Document any findings
- [ ] **Schedule rotation reminders**: Add to calendar
- [ ] **Train team members**: Share documentation
- [ ] **Document lessons learned**: Add to TOKEN_REGISTRY.md

**Final Validation:**

```bash
# Comprehensive health check
python3 scripts/validate-tokens.py --verbose

# Review GitHub rate limits
for token in org-label-sync-token org-project-admin-token org-onboarding-token org-repo-analysis-token; do
  echo "=== $token ==="
  TOKEN=$(op read "op://Personal/$token/password" --reveal)
  curl -s -H "Authorization: token $TOKEN" https://api.github.com/rate_limit | jq '.rate'
  echo ""
done
```

**Expected Results:**

- All tokens validate successfully
- Rate limits show sufficient remaining quota
- No authentication errors in logs
- Team members understand new token system

______________________________________________________________________

## Success Criteria

### Must Have ✅

- [ ] All 4 tokens authenticate successfully for 7 consecutive days
- [ ] No "401 Unauthorized" errors in any script
- [ ] GitHub Actions workflow passes daily
- [ ] Each script uses correct token (no cross-contamination)
- [ ] TOKEN_REGISTRY.md updated with production findings

### Should Have 📋

- [ ] Clear error messages when tokens fail
- [ ] Graceful fallback in utils.py (gh CLI → 1Password)
- [ ] Rate limits show >50% remaining quota
- [ ] GitHub audit log shows expected activity
- [ ] Team trained on new token system

### Nice to Have 🎯

- [ ] Automated rotation reminders (calendar/Slack)
- [ ] Dashboard showing token health
- [ ] Rotation dry-run tested successfully
- [ ] Documentation reviewed and improved based on findings

______________________________________________________________________

## Common Issues & Troubleshooting

### Issue 1: Token Not Found in 1Password

**Symptoms:**

```
ERROR: Token 'org-label-sync-token' not found in 1Password
```

**Diagnosis:**

```bash
# Check if item exists
op item list --vault Personal | grep org-label-sync-token

# Verify exact name (case-sensitive)
op read "op://Personal/org-label-sync-token/password" --reveal
```

**Solution:**

- Verify token name spelling (exact match required)
- Check 1Password vault is "Personal" (not "Private")
- Re-authenticate: `eval $(op signin)`
- If missing, recreate token and store in 1Password

______________________________________________________________________

### Issue 2: Authentication Fails (401 Unauthorized)

**Symptoms:**

```
{"message":"Bad credentials","documentation_url":"..."}
```

**Diagnosis:**

```bash
# Test token directly with GitHub API
TOKEN=$(op read "op://Personal/org-label-sync-token/password" --reveal)
curl -H "Authorization: token $TOKEN" https://api.github.com/user
```

**Solution:**

- Token may be expired (check expiration in TOKEN_REGISTRY.md)
- Token may have been revoked in GitHub settings
- Token scopes may be insufficient
- Regenerate token and update in 1Password

______________________________________________________________________

### Issue 3: Wrong Token Used

**Symptoms:**

- Script works but uses wrong scopes
- Audit log shows unexpected token usage

**Diagnosis:**

```bash
# Check which token script is using
# Add debug print in script:
# print(f"Using token: {token_name}")
```

**Solution:**

- Review script code (should explicitly name token)
- Check secret_manager.py requires token name (no defaults)
- Update script to use correct token
- See TOKEN_REGISTRY.md Token Selection Guide

______________________________________________________________________

### Issue 4: Rate Limit Exceeded

**Symptoms:**

```
{"message":"API rate limit exceeded..."}
```

**Diagnosis:**

```bash
# Check rate limit for token
TOKEN=$(op read "op://Personal/org-label-sync-token/password" --reveal)
curl -H "Authorization: token $TOKEN" https://api.github.com/rate_limit | jq
```

**Solution:**

- Wait for rate limit reset (check X-RateLimit-Reset header)
- Use different token if available
- Implement request caching
- Consider GitHub App for higher limits (5000/hour per installation)

______________________________________________________________________

### Issue 5: 1Password CLI Not Authenticated

**Symptoms:**

```
[ERROR] 2026/01/18 17:22:00 You are not currently signed in. Please run `op signin`
```

**Solution:**

```bash
# Re-authenticate
eval $(op signin)

# Verify authentication
op account list

# Test token retrieval
op read "op://Personal/org-label-sync-token/password" --reveal
```

______________________________________________________________________

## Monitoring Commands Reference

### Token Health Check

```bash
# Quick validation (all tokens)
python3 scripts/validate-tokens.py

# Verbose output with details
python3 scripts/validate-tokens.py --verbose

# Check specific token
TOKEN=$(op read "op://Personal/org-label-sync-token/password" --reveal)
curl -H "Authorization: token $TOKEN" https://api.github.com/user | jq
```

### Rate Limit Monitoring

```bash
# Check all tokens
for token_name in org-label-sync-token org-project-admin-token org-onboarding-token org-repo-analysis-token; do
  echo "=== $token_name ==="
  TOKEN=$(op read "op://Personal/$token_name/password" --reveal)
  curl -s -H "Authorization: token $TOKEN" https://api.github.com/rate_limit | \
    jq '{rate: .rate, resources: .resources.core}'
  echo ""
done
```

### GitHub Actions Workflow

```bash
# View workflow details
gh workflow view token-health-check.yml

# List recent runs
gh run list --workflow=token-health-check.yml --limit 10

# View specific run logs
gh run view <run-id> --log

# Manually trigger workflow
gh workflow run token-health-check.yml
```

### GitHub Audit Log

```bash
# View recent API activity (requires org admin)
gh api /orgs/ivviiviivvi/audit-log \
  --jq '.[] | select(.action | contains("oauth")) | {timestamp, action, actor, token_id}'

# Or visit web interface
# https://github.com/organizations/ivviiviivvi/settings/audit-log
```

### Script Dry-Run Testing

```bash
# Label sync (dry-run)
python3 automation/scripts/sync_labels.py \
  --org ivviiviivvi \
  --repo .github \
  --dry-run

# Repo analysis (dry-run)
python3 automation/scripts/web_crawler.py \
  --dry-run \
  --output /tmp/test-output.json

# Project setup (check script for dry-run flag)
bash scripts/complete-project-setup.sh --help
```

______________________________________________________________________

## Phase 3 Completion Checklist

### Before Declaring Phase 3 Complete

- [ ] All success criteria met (see above)
- [ ] No authentication errors for 7 consecutive days
- [ ] TOKEN_REGISTRY.md updated with findings
- [ ] Team trained on new system
- [ ] Rotation procedures tested (at least dry-run)
- [ ] Documentation reviewed and improved
- [ ] Lessons learned documented
- [ ] Next rotation dates in calendar

### Phase 3 Sign-Off

**Completed By**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Date**:
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Issues Found**:
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Issues Resolved**:
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Recommendations for Phase 4**:
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

______________________________________________________________________

## Next Steps (Phase 4 - Optional)

After Phase 3 completion, consider:

1. **GitHub App Migration** (Long-term enhancement)

   - Replace PATs with GitHub App authentication
   - Auto-rotating tokens (1-hour lifetime)
   - Programmatic token generation
   - See: MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md

1. **Enhanced Monitoring**

   - Slack notifications for token issues
   - Dashboard showing token health
   - Automated rotation reminders

1. **Security Hardening**

   - Review token scopes (further minimize if possible)
   - Implement token usage analytics
   - Set up anomaly detection

______________________________________________________________________

## Resources

- [TOKEN_REGISTRY.md](TOKEN_REGISTRY.md) - Token management procedures
- [TOKEN_MIGRATION_STATUS.md](../reports/TOKEN_MIGRATION_STATUS.md) - Migration
  guide
- [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](../analysis/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
  \- Full analysis
- scripts/validate-tokens.py - Validation script
- scripts/rotate-token.sh - Rotation automation
- [.github/workflows/token-health-check.yml](../../.github/workflows/token-health-check.yml)
  \- Daily CI/CD check

______________________________________________________________________

**Last Updated**: 2026-01-18\
**Maintained By**: Organization Security
Team\
**Next Review**: 2026-01-25 (Phase 3 completion)
