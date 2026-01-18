# Phase 3 Day 1: Initial Validation Checklist

**Date**: 2026-01-18  
**Status**: 🟡 In Progress  
**Monitoring Period**: Day 1 of 7

---

## Day 1 Tasks

### Task 1: 1Password Authentication ⏳

**Status**: ⚠️ REQUIRED - Needs user action

**Method**: Service Account (Recommended - No More Signin!)

**Command**:

```bash
./scripts/setup-service-account.sh
```

**This will**:

1. Guide you to create a 1Password service account
2. Save the token to your shell profile
3. Test access to all 4 tokens
4. **Eliminate all future signin prompts!**

**Alternative** (Old Way - Not Recommended):

```bash
eval $(op signin)  # You'll have to do this repeatedly
```

**Expected Result**: Service account configured, tokens accessible  
**Actual Result**: Pending - requires user to run setup script

**Notes**:

- Service account = one-time setup, no more signin prompts
- Token stored in shell profile (auto-loaded every session)
- Get service account: <https://my.1password.com/developer-tools/service-accounts>
- Service accounts are designed for automation (better than signin)

---

### Task 2: Validate All 4 Tokens ⏳

**Status**: ⏳ Pending (awaits Task 1)

**Command**:

```bash
PYTHONPATH=/workspace/automation/scripts python3 scripts/validate-tokens.py
```

**Expected Results**:

- ✅ org-label-sync-token: Valid
- ✅ org-project-admin-token: Valid
- ✅ org-onboarding-token: Valid
- ✅ org-repo-analysis-token: Valid

**Actual Results**: Not yet run

**Notes**:

- Script validates token authentication via GitHub API
- Checks rate limits for each token
- Verifies token scopes match requirements

---

### Task 3: Test org-label-sync-token ⏳

**Status**: ⏳ Pending (awaits Task 2)

**Command**:

```bash
python3 automation/scripts/sync_labels.py --org ivviiviivvi --repo .github --dry-run
```

**Expected Result**: Script runs successfully with org-label-sync-token  
**Actual Result**: Not yet run

**Notes**:

- Dry-run mode tests authentication without making changes
- Verifies token retrieval from 1Password
- Confirms script uses correct token (not master-org-token)

---

### Task 4: Test org-repo-analysis-token ⏳

**Status**: ⏳ Pending (awaits Task 2)

**Command**:

```bash
python3 automation/scripts/web_crawler.py --dry-run
```

**Expected Result**: Script runs successfully with org-repo-analysis-token  
**Actual Result**: Not yet run

**Notes**:

- Read-only operation (safe to test)
- Verifies token has repo:status and read:org scopes
- Tests token retrieval from 1Password

---

### Task 5: Test org-project-admin-token ⏳

**Status**: ⏳ Pending (awaits Task 2)

**Command**:

```bash
bash scripts/complete-project-setup.sh --help
# Then run with --dry-run if supported
```

**Expected Result**: Script can retrieve token and authenticate  
**Actual Result**: Not yet run

**Notes**:

- Check if script supports dry-run flag
- Verifies token has project and read:org scopes
- Tests 1Password retrieval in bash script

---

### Task 6: Check GitHub API Rate Limits ⏳

**Status**: ⏳ Pending (awaits Task 1)

**Command**:

```bash
# For each token, check rate limit
for token_name in org-label-sync-token org-project-admin-token org-onboarding-token org-repo-analysis-token; do
  echo "=== $token_name ==="
  TOKEN=$(op read "op://Personal/$token_name/password" --reveal)
  curl -s -H "Authorization: token $TOKEN" https://api.github.com/rate_limit | jq '.rate'
  echo ""
done
```

**Expected Results**:

- All tokens have >4000/5000 requests remaining
- Reset times are reasonable
- No tokens showing exhaustion

**Actual Results**: Not yet run

**Notes**:

- Fresh tokens should have full 5000/hour quota
- Monitor for any unexpected usage
- Document baseline for future comparison

---

### Task 7: Review GitHub Actions Workflow ⏳

**Status**: ⏳ Pending

**Command**:

```bash
gh workflow view token-health-check.yml
gh run list --workflow=token-health-check.yml --limit 5
```

**Expected Result**: Workflow exists and is scheduled for daily runs  
**Actual Result**: Not yet run

**Notes**:

- Workflow should run daily at 8:00 UTC
- First run expected: 2026-01-19 08:00 UTC
- Check for any configuration issues

---

### Task 8: Verify gh CLI Fallback ⏳

**Status**: ⏳ Pending (awaits Task 1)

**Test**: Verify utils.py uses gh CLI token when available

**Command**:

```bash
# Check gh CLI authentication
gh auth status

# Test a script that uses utils.py
python3 automation/scripts/sync_labels.py --org ivviiviivvi --help
```

**Expected Result**:

- gh CLI is authenticated
- utils.py prefers gh CLI token over 1Password

**Actual Result**: Not yet run

**Notes**:

- utils.py should try gh CLI first, then fall back to 1Password
- Verify this behavior works as designed
- Document which token is actually used

---

## Day 1 Summary

**Completion Status**: 0/8 tasks complete

### Completed ✅

- None yet - awaiting 1Password authentication

### In Progress 🟡

- Task 1: 1Password authentication (user action required)

### Blocked ⏳

- Tasks 2-8: All waiting for Task 1 completion

### Issues Found 🐛

- None yet

### Notes 📝

- Phase 3 commenced at 2026-01-18 17:37 UTC
- Validation script executed but requires 1Password auth
- All tasks ready to execute once authentication is complete

---

## Next Steps

**Immediate** (Today - 2026-01-18):

1. ⚠️ **User action required**: Authenticate 1Password CLI
   - Run: `eval $(op signin)`
   - Provide credentials when prompted
   - Verify: `op account list`

2. Complete remaining Day 1 tasks in sequence
3. Document any issues encountered
4. Update this checklist with actual results

**Tomorrow** (2026-01-19):

- Review Day 1 results
- Begin Day 2-3 production testing
- Monitor GitHub Actions first scheduled run

---

## Day 1 Sign-Off

**Completed By**: _______________  
**Date**: _______________  
**All Tasks Successful?**: ☐ Yes ☐ No  
**Issues Found**: _______________  
**Ready for Day 2?**: ☐ Yes ☐ No

**Notes**: _______________

---

**Reference**: See [TOKEN_MIGRATION_PHASE3_MONITORING.md](docs/TOKEN_MIGRATION_PHASE3_MONITORING.md) for complete guide
