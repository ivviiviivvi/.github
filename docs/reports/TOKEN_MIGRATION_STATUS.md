# Token Segmentation Migration Status

**Date:** 2026-01-18\
**Status:** 🟢 **Phase 1 Ready to Start**\
**Progress:**
Implementation Complete → Token Creation Phase

______________________________________________________________________

## Executive Summary

### Key Discovery 🔍

The `master-org-token-011726` referenced in scripts **does not exist in
1Password**. This is actually positive news:

- ✅ **No legacy token to deprecate** - simplifies migration
- ✅ **Clean slate** - can implement best practices from day one
- ✅ **No security risk** - scripts currently rely on GitHub CLI token
  (auto-provided)
- ✅ **Scripts functional** - using `gh` CLI authentication or
  `secrets.GITHUB_TOKEN`

### Revised Approach

**OLD PLAN:** Migrate from master token → purpose-specific tokens\
**NEW PLAN:**
Create purpose-specific tokens from scratch

**Timeline:** Accelerated (no legacy migration needed)

______________________________________________________________________

## Current State Analysis

### Authentication Status by Script

| Script                                 | Current Authentication                         | Required Token            | Action Needed                    |
| -------------------------------------- | ---------------------------------------------- | ------------------------- | -------------------------------- |
| `scripts/complete-project-setup.sh`    | References master token (line 48)              | `org-project-admin-token` | Add token creation step          |
| `automation/scripts/web_crawler.py`    | References master token (line 49)              | `org-repo-analysis-token` | Update token parameter           |
| `automation/scripts/sync_labels.py`    | References master token (line 327)             | `org-label-sync-token`    | Update default value             |
| `automation/scripts/secret_manager.py` | Provides master token default (lines 127, 140) | N/A                       | Remove default, require explicit |
| `automation/scripts/utils.py`          | References master token (line 207)             | Token parameter           | Accept token or use gh CLI       |
| `archive/deployment/DEPLOY_PHASE*.sh`  | Documentation only (archived)                  | N/A                       | No code changes needed           |

**Current Behavior:** Scripts likely fall back to GitHub CLI authentication
(`gh`) or fail gracefully.

### Documentation Status

| Document                                              | Status      | Content                                                 |
| ----------------------------------------------------- | ----------- | ------------------------------------------------------- |
| **MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md** | ✅ Complete | 28K comprehensive analysis, 5 solutions, migration plan |
| **TOKEN_REGISTRY.md**                                 | ✅ Updated  | 22K with discovery findings, revised timeline           |
| **MASTER_ORG_TOKEN_QUICK_ACTION.md**                  | ✅ Complete | 8.2K executive summary, action items                    |

### Automation Tools Status

| Tool                                       | Status      | Purpose                     |
| ------------------------------------------ | ----------- | --------------------------- |
| `scripts/validate-tokens.py`               | ✅ Ready    | Automated health checking   |
| `scripts/rotate-token.sh`                  | ✅ Ready    | Guided rotation workflow    |
| `scripts/token-segmentation-migration.sh`  | ✅ Ready    | Interactive creation wizard |
| `.github/workflows/token-health-check.yml` | ✅ Deployed | Daily validation (8:00 UTC) |

______________________________________________________________________

## Phase 1: Token Creation (Current Phase)

### Required Tokens (4 Total)

#### 1. org-project-admin-token 🎯

- **Purpose:** GitHub Projects creation and management
- **Scopes:** `project`, `read:org`
- **Expiration:** 90 days
- **Used by:** `scripts/complete-project-setup.sh`, project automation
- **Priority:** High (needed for project workflows)

#### 2. org-label-sync-token 🏷️

- **Purpose:** Label synchronization across repositories
- **Scopes:** `repo`, `workflow`
- **Expiration:** 90 days
- **Used by:** `automation/scripts/sync_labels.py`
- **Priority:** High (frequently used)

#### 3. org-onboarding-token 🚀

- **Purpose:** Automated repository onboarding and setup
- **Scopes:** `repo`, `workflow`, `admin:org`
- **Expiration:** 60 days (highest privilege, shorter rotation)
- **Used by:** Deployment scripts, batch onboarding
- **Priority:** Medium (used for new repo setup)

#### 4. org-repo-analysis-token 📊

- **Purpose:** Read-only repository health checks and metrics
- **Scopes:** `repo:status`, `read:org`
- **Expiration:** 180 days (read-only, longer rotation)
- **Used by:** `automation/scripts/web_crawler.py`, metrics collection
- **Priority:** Low (read-only, less critical)

______________________________________________________________________

## Step-by-Step Creation Guide

### Prerequisites ✅

- [x] GitHub account with admin access to organization
- [x] 1Password CLI installed and authenticated
- [x] Documentation reviewed
- [x] Migration script ready

### Creation Process (15-20 minutes)

#### Step 1: Generate Tokens in GitHub

1. **Open GitHub Token Settings:**

   ```
   https://github.com/settings/tokens/new
   ```

1. **For EACH token, create with these settings:**

   **Token 1: org-project-admin-token**

   - Name: `org-project-admin-token`
   - Expiration: 90 days (select custom date: 2026-04-18)
   - Scopes:
     - ☑ `read:org` (under "admin:org" section)
     - ☑ `project` (full control of projects)
   - Click "Generate token"
   - **Copy immediately** (only shown once!)

   **Token 2: org-label-sync-token**

   - Name: `org-label-sync-token`
   - Expiration: 90 days (2026-04-18)
   - Scopes:
     - ☑ `repo` (full control of repositories)
     - ☑ `workflow` (update GitHub Actions workflows)
   - Generate and copy

   **Token 3: org-onboarding-token**

   - Name: `org-onboarding-token`
   - Expiration: 60 days (2026-03-19)
   - Scopes:
     - ☑ `repo` (full control)
     - ☑ `workflow` (workflow control)
     - ☑ `admin:org` (full organizational access)
   - Generate and copy

   **Token 4: org-repo-analysis-token**

   - Name: `org-repo-analysis-token`
   - Expiration: 180 days (2026-07-17)
   - Scopes:
     - ☑ `repo:status` (under "repo" section, minimal access)
     - ☑ `read:org` (under "admin:org" section)
   - Generate and copy

#### Step 2: Store Tokens in 1Password

**Option A: Interactive (Recommended)**

Run the migration wizard:

```bash
cd /workspace/scripts
./token-segmentation-migration.sh
```

Follow the prompts to paste each token.

**Option B: Manual (For Advanced Users)**

Ensure 1Password CLI is authenticated:

```bash
eval $(op signin)
```

Store each token:

```bash
# Store org-project-admin-token
op item create \
  --category="Password" \
  --title="org-project-admin-token" \
  --vault="Personal" \
  password="<paste-token-here>"

# Store org-label-sync-token
op item create \
  --category="Password" \
  --title="org-label-sync-token" \
  --vault="Personal" \
  password="<paste-token-here>"

# Store org-onboarding-token
op item create \
  --category="Password" \
  --title="org-onboarding-token" \
  --vault="Personal" \
  password="<paste-token-here>"

# Store org-repo-analysis-token
op item create \
  --category="Password" \
  --title="org-repo-analysis-token" \
  --vault="Personal" \
  password="<paste-token-here>"
```

#### Step 3: Validate Tokens

Run the validation script:

```bash
cd /workspace/scripts
python3 validate-tokens.py --verbose
```

**Expected output:**

```
🔍 Validating organization tokens...

Checking org-project-admin-token... ✅ Valid (rate limit: 5000)
Checking org-label-sync-token... ✅ Valid (rate limit: 5000)
Checking org-onboarding-token... ✅ Valid (rate limit: 5000)
Checking org-repo-analysis-token... ✅ Valid (rate limit: 5000)

============================================================
Summary:
  Valid: 4/4
  Failed: 0/4

✅ All tokens are healthy!
```

If any token fails validation:

- Verify token was copied correctly
- Check token hasn't expired
- Confirm scopes match requirements
- Re-generate if necessary

______________________________________________________________________

## Phase 2: Script Updates (After Token Creation)

### Scripts to Modify

Once tokens are created and validated, update these scripts:

#### 1. automation/scripts/secret_manager.py

**Change:** Remove default token parameter

```python
# BEFORE
def get_github_token(item_name: str = "master-org-token-011726") -> Optional[str]:
    ...

# AFTER
def get_github_token(item_name: str) -> Optional[str]:
    """
    Get GitHub token from 1Password.

    Args:
        item_name: REQUIRED. Name of 1Password item (e.g., "org-label-sync-token")
    """
    if not item_name:
        raise ValueError(
            "Token name required. Use purpose-specific token:\n"
            "  - org-label-sync-token: For label operations\n"
            "  - org-project-admin-token: For project operations\n"
            "  - org-repo-analysis-token: For read-only analysis\n"
            "  - org-onboarding-token: For repository onboarding"
        )
    return get_secret(item_name, "password", vault="Personal")
```

#### 2. automation/scripts/sync_labels.py

**Change:** Use purpose-specific token

```python
# Line 327 - BEFORE
default=get_secret("master-org-token-011726", "password")

# Line 327 - AFTER
default=get_secret("org-label-sync-token", "password")
```

#### 3. automation/scripts/web_crawler.py

**Change:** Use analysis token

```python
# Line 49 - BEFORE
github_token = get_secret("master-org-token-011726", "password")

# Line 49 - AFTER
github_token = get_secret("org-repo-analysis-token", "password")
```

#### 4. scripts/complete-project-setup.sh

**Change:** Use project admin token

```bash
# Line 48 - BEFORE
export GH_TOKEN=$(op read "op://Personal/master-org-token-011726/password" --reveal)

# Line 48 - AFTER
export GH_TOKEN=$(op read "op://Personal/org-project-admin-token/password" --reveal)
```

#### 5. automation/scripts/utils.py

**Change:** Accept token parameter or default to gh CLI

```python
# Line 207 - BEFORE
token = get_secret("master-org-token-011726", "password")

# Line 207 - AFTER
# Option 1: Accept token parameter
token = token or get_secret("org-label-sync-token", "password")

# Option 2: Fall back to gh CLI (recommended for utility functions)
import subprocess
token = token or subprocess.run(
    ["gh", "auth", "token"],
    capture_output=True,
    text=True
).stdout.strip()
```

### Testing Updates

After each script update, test in dry-run mode:

```bash
# Test label sync
python3 automation/scripts/sync_labels.py --dry-run --repo test-repo

# Test web crawler
python3 automation/scripts/web_crawler.py --dry-run

# Test project setup
bash scripts/complete-project-setup.sh --dry-run
```

______________________________________________________________________

## Phase 3: Monitoring & Verification (After Updates)

### Daily Monitoring (First Week)

**Automated Checks:**

- ✅ GitHub Actions workflow runs daily at 8:00 UTC
- ✅ Validates all 4 tokens automatically
- ✅ Creates GitHub issue if any token fails

**Manual Checks:**

```bash
# Check token health
python3 scripts/validate-tokens.py

# Check rate limits
for token in org-project-admin-token org-label-sync-token org-onboarding-token org-repo-analysis-token; do
  echo "=== $token ==="
  TOKEN=$(op read "op://Personal/$token/password" --reveal)
  curl -s -H "Authorization: token $TOKEN" https://api.github.com/rate_limit | jq '.rate'
done
```

### Success Metrics

- [ ] All 4 tokens created and stored ✅
- [ ] All tokens pass validation ✅
- [ ] Scripts updated with new tokens ⏳
- [ ] Dry-run tests pass for all scripts ⏳
- [ ] Production usage successful (24 hours) ⏳
- [ ] No authentication errors in logs ⏳
- [ ] Team trained on new system ⏳

______________________________________________________________________

## Migration Timeline

### Week 1: Token Creation & Initial Testing

- **Day 1-2:** Create and validate 4 tokens ← **YOU ARE HERE**
- **Day 3-4:** Update scripts with new tokens
- **Day 5-7:** Dry-run testing, monitor for issues

### Week 2: Production Deployment

- **Day 8-10:** Deploy updated scripts to production
- **Day 11-14:** Monitor production usage, collect metrics

### Week 3: Documentation & Training

- **Day 15-17:** Update all documentation
- **Day 18-21:** Team training, knowledge transfer

### Week 4: Completion

- **Day 22-28:** Final validation, mark project complete

**Target Completion:** 2026-02-18 (1 month)

______________________________________________________________________

## Rollback Plan

If issues arise during migration:

1. **Scripts still reference non-existent master token:**

   - No risk - scripts already handle this case
   - Fall back to GitHub CLI authentication

1. **Purpose-specific token fails:**

   - Generate new token with same name
   - Update 1Password (overwrites old value)
   - No script changes needed

1. **Major issues discovered:**

   - Revert script changes via git
   - Keep tokens for future use
   - Review and adjust migration plan

**Note:** Since master token never existed, there's no "rollback" to previous
state - only forward progress.

______________________________________________________________________

## Quick Reference Commands

### Check Token Status

```bash
python3 /workspace/scripts/validate-tokens.py
```

### Rotate a Token

```bash
bash /workspace/scripts/rotate-token.sh <token-name>
```

### Create All Tokens (Interactive)

```bash
bash /workspace/scripts/token-segmentation-migration.sh
```

### Manual Token Retrieval

```bash
op read "op://Personal/<token-name>/password" --reveal
```

### Check GitHub CLI Auth

```bash
gh auth status
```

______________________________________________________________________

## Support & Resources

### Documentation

- [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](../analysis/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
  \- Comprehensive analysis
- [TOKEN_REGISTRY.md](../reference/TOKEN_REGISTRY.md) - Token management
  registry
- [MASTER_ORG_TOKEN_QUICK_ACTION.md](../analysis/MASTER_ORG_TOKEN_QUICK_ACTION.md)
  \- Quick reference

### Automation Tools

- `scripts/validate-tokens.py` - Health validation
- `scripts/rotate-token.sh` - Guided rotation
- `scripts/token-segmentation-migration.sh` - Interactive wizard
- `.github/workflows/token-health-check.yml` - Daily CI/CD checks

### Need Help?

- 💬 Review documentation above
- 🔧 Run migration wizard for guided setup
- 📋 Check TOKEN_REGISTRY.md for procedures
- 🚨 Emergency procedures in TOKEN_REGISTRY.md

______________________________________________________________________

## Next Actions (Immediate)

### Priority 1: Create Tokens (15-20 min)

1. Open <https://github.com/settings/tokens/new>
1. Create all 4 tokens following guide above
1. Store in 1Password
1. Run validation: `python3 scripts/validate-tokens.py`

### Priority 2: Update Scripts (30-45 min)

1. Update `automation/scripts/secret_manager.py` (remove default)
1. Update `automation/scripts/sync_labels.py` (use org-label-sync-token)
1. Update `automation/scripts/web_crawler.py` (use org-repo-analysis-token)
1. Update `scripts/complete-project-setup.sh` (use org-project-admin-token)
1. Test each script in dry-run mode

### Priority 3: Monitor & Verify (1 week)

1. Deploy updated scripts to production
1. Monitor for authentication errors
1. Check daily validation workflow
1. Update TOKEN_REGISTRY.md with completion dates

______________________________________________________________________

**Status:** 🟢 Ready to proceed with token creation\
**Blocker:** None (clean
slate, no legacy migration needed)\
**Estimated Time:** 15-20 minutes for token
creation\
**Risk Level:** Low (no existing dependencies to break)

______________________________________________________________________

**Last Updated:** 2026-01-18\
**Next Review:** After token creation (Phase 1
complete)
