# Token Security Implementation - Action Plan

**Date:** January 18, 2026\
**Priority:** 🔥 Critical\
**Status:** Ready to
Execute

______________________________________________________________________

## Executive Summary

Implementing token segmentation to replace the single `master-org-token-011726`
with purpose-specific tokens for improved security, audit trail, and
maintainability.

**Current State:** Single universal token used by 9+ scripts\
**Target State:**
4 purpose-specific tokens with minimal required scopes\
**Timeline:** 4 weeks
(target completion: February 18, 2026)

______________________________________________________________________

## Implementation Steps

### ✅ Phase 1: Planning & Documentation (COMPLETE)

**Completed:**

- ✅ Security analysis document created
- ✅ Token registry updated with migration plan
- ✅ Migration scripts created and tested
- ✅ Validation tooling implemented

**Deliverables:**

- `/workspace/docs/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md`
- `/workspace/docs/TOKEN_REGISTRY.md`
- `/workspace/scripts/token-segmentation-migration.sh`
- `/workspace/automation/scripts/validate_tokens.py`

______________________________________________________________________

### 🔄 Phase 2: Token Creation (IN PROGRESS - Week 1)

**Action Required:** Create 4 new tokens in GitHub

**Steps:**

1. **Navigate to GitHub Token Settings**

   ```
   https://github.com/settings/tokens/new
   ```

1. **Create Token 1: org-label-sync-token**

   - Name: `org-label-sync-token`
   - Expiration: 90 days
   - Scopes: `repo`, `workflow`
   - Purpose: Label synchronization across repositories

1. **Create Token 2: org-project-admin-token**

   - Name: `org-project-admin-token`
   - Expiration: 90 days
   - Scopes: `project`, `read:org`
   - Purpose: GitHub Projects creation and management

1. **Create Token 3: org-repo-analysis-token**

   - Name: `org-repo-analysis-token`
   - Expiration: 180 days
   - Scopes: `repo:status`, `read:org`
   - Purpose: Read-only repository health checks

1. **Create Token 4: org-onboarding-token**

   - Name: `org-onboarding-token`
   - Expiration: 60 days
   - Scopes: `repo`, `workflow`, `admin:org`
   - Purpose: Automated repository onboarding

1. **Store Tokens in 1Password**

   ```bash
   # Run interactive wizard
   cd /workspace/scripts
   ./token-segmentation-migration.sh
   ```

1. **Validate Tokens**

   ```bash
   python3 /workspace/automation/scripts/validate_tokens.py
   ```

**Expected Output:**

```
✓ org-label-sync-token validated
✓ org-project-admin-token validated
✓ org-repo-analysis-token validated
✓ org-onboarding-token validated
```

______________________________________________________________________

### ⏳ Phase 3: Script Migration (Week 2)

**Scripts to Update:**

| Script                                 | Current Token           | New Token               | Priority    |
| -------------------------------------- | ----------------------- | ----------------------- | ----------- |
| `scripts/complete-project-setup.sh`    | master-org-token-011726 | org-project-admin-token | 🔥 High     |
| `scripts/projects-quick-ref.sh`        | master-org-token-011726 | org-project-admin-token | 📊 Medium   |
| `automation/scripts/sync_labels.py`    | master-org-token-011726 | org-label-sync-token    | 🔥 High     |
| `automation/scripts/web_crawler.py`    | master-org-token-011726 | org-repo-analysis-token | 📊 Medium   |
| `automation/scripts/secret_manager.py` | master-org-token-011726 | Remove default          | 🔥 High     |
| `automation/scripts/utils.py`          | master-org-token-011726 | Use parameter           | 📊 Medium   |
| `DEPLOY_PHASE1.sh`                     | master-org-token-011726 | org-onboarding-token    | ⚡ Critical |
| `DEPLOY_PHASE2.sh`                     | master-org-token-011726 | org-onboarding-token    | ⚡ Critical |
| `DEPLOY_PHASE3.sh`                     | master-org-token-011726 | org-onboarding-token    | ⚡ Critical |

**Automated Update:**

```bash
# Creates backups and updates all references
cd /workspace/scripts
./token-segmentation-migration.sh
# Choose "Auto-update scripts now" option
```

**Manual Verification:**

```bash
# Check for remaining references
grep -r "master-org-token-011726" /workspace --exclude-dir=.git \
  --include="*.py" --include="*.sh" | grep -v ".backup"
```

______________________________________________________________________

### ⏳ Phase 4: Testing & Validation (Week 3)

**Test Each Token:**

1. **Label Sync Token**

   ```bash
   export GH_TOKEN=$(op read "op://Personal/org-label-sync-token/password")
   python3 automation/scripts/sync_labels.py --dry-run
   ```

1. **Project Admin Token**

   ```bash
   export GH_TOKEN=$(op read "op://Personal/org-project-admin-token/password")
   cd scripts
   ./complete-project-setup.sh
   # Test project creation
   ```

1. **Repo Analysis Token**

   ```bash
   export GH_TOKEN=$(op read "op://Personal/org-repo-analysis-token/password")
   python3 automation/scripts/web_crawler.py --dry-run
   ```

1. **Onboarding Token**

   ```bash
   export GH_TOKEN=$(op read "op://Personal/org-onboarding-token/password")
   ./DEPLOY_PHASE1.sh --dry-run
   ```

**Validation Checklist:**

- [ ] All 4 tokens validate successfully
- [ ] Each script works with new token
- [ ] No permission errors
- [ ] Rate limits acceptable
- [ ] Audit logs show correct token usage

______________________________________________________________________

### ⏳ Phase 5: Deprecation (Week 4)

**Master Token Deprecation Steps:**

1. **Monitor for 7 Days**

   - Watch for any unexpected failures
   - Check logs for master token usage
   - Verify all scripts migrated

1. **Search for Stragglers**

   ```bash
   # Find any remaining references
   find /workspace -type f \( -name "*.py" -o -name "*.sh" -o -name "*.yml" \) \
     -exec grep -l "master-org-token-011726" {} \; | \
     grep -v ".backup" | grep -v "docs/"
   ```

1. **Revoke Master Token**

   - Go to: https://github.com/settings/tokens
   - Find `master-org-token-011726`
   - Click "Delete"
   - Confirm deletion

1. **Update Documentation**

   - Move master token to "Deprecated" section in TOKEN_REGISTRY.md
   - Update last rotated date in audit log
   - Document lessons learned

1. **Archive in 1Password**

   ```bash
   # Tag as deprecated
   op item edit master-org-token-011726 --vault Personal \
     --tags "deprecated,revoked-2026-02-18"
   ```

______________________________________________________________________

## Success Metrics

### Security Improvements

- ✅ Reduced blast radius (1 compromised token ≠ full org compromise)
- ✅ Clear audit trail (token name indicates purpose)
- ✅ Minimal required scopes per operation
- ✅ Independent rotation schedules

### Operational Improvements

- ✅ Easier token rotation (doesn't break all systems)
- ✅ Clear documentation (TOKEN_REGISTRY.md)
- ✅ Automated validation (validate_tokens.py)
- ✅ Self-service token management

______________________________________________________________________

## Risk Mitigation

### Risk 1: Scripts Break During Migration

**Mitigation:**

- Automated backups created before updates
- Dry-run testing before production use
- Keep master token active during testing
- Rollback plan: restore .backup files

### Risk 2: Missing Token Permissions

**Mitigation:**

- Validation script tests all required operations
- Document exact scopes needed per token
- Add scopes incrementally if needed

### Risk 3: Token Creation Errors

**Mitigation:**

- Detailed step-by-step instructions
- Interactive wizard with validation
- Fallback to manual creation

______________________________________________________________________

## Rollback Plan

If issues arise during migration:

1. **Restore Backup Files**

   ```bash
   for file in scripts/*.backup-*; do
     original="${file%.backup-*}"
     cp "$file" "$original"
   done
   ```

1. **Verify Master Token Still Works**

   ```bash
   export GH_TOKEN=$(op read "op://Personal/master-org-token-011726/password")
   curl -H "Authorization: token $GH_TOKEN" https://api.github.com/user
   ```

1. **Revert and Investigate**

   - Document what went wrong
   - Fix root cause
   - Retry migration

______________________________________________________________________

## Timeline

| Week | Phase       | Tasks                                | Status            |
| ---- | ----------- | ------------------------------------ | ----------------- |
| 1    | Planning    | Analysis, documentation, tooling     | ✅ Complete       |
| 1    | Creation    | Create 4 new tokens, validate        | ⏳ Ready to start |
| 2    | Migration   | Update all scripts, test changes     | ⏳ Pending        |
| 3    | Testing     | Comprehensive validation, monitoring | ⏳ Pending        |
| 4    | Deprecation | Revoke master token, final docs      | ⏳ Pending        |

**Target Completion:** February 18, 2026

______________________________________________________________________

## Quick Start

**To begin Phase 2 (Token Creation):**

```bash
cd /workspace/scripts
./token-segmentation-migration.sh
```

Follow the interactive prompts to:

1. Review token requirements
1. Create tokens in GitHub
1. Store tokens in 1Password
1. Validate tokens work
1. Update script references

______________________________________________________________________

## Documentation References

- **Analysis:**
  [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](../docs/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
- **Registry:** [TOKEN_REGISTRY.md](../docs/TOKEN_REGISTRY.md)
- **Migration Script:** `/workspace/scripts/token-segmentation-migration.sh`
- **Validation Script:** `/workspace/automation/scripts/validate_tokens.py`

______________________________________________________________________

## Support

**Questions or Issues?**

- Review documentation in `/workspace/docs/`
- Check TOKEN_REGISTRY.md for token details
- Run validation script for diagnostics
- Open issue if blocked

______________________________________________________________________

**Next Action:** Run `/workspace/scripts/token-segmentation-migration.sh` to
begin Phase 2.

______________________________________________________________________

_Created: January 18, 2026_\
_Owner: Security Team_\
_Priority: Critical_
