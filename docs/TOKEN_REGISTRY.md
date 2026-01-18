# GitHub Token Registry

> **Central registry for all GitHub Personal Access Tokens and authentication
> mechanisms used in the ivviiviivvi organization**

**Last Updated:** 2026-01-18\
**Owner:** Organization Security Team\
**Review
Schedule:** Quarterly (next: 2026-04-18)

---

## Table of Contents

- [Active Tokens](#active-tokens)
- [Usage Guidelines](#usage-guidelines)
- [Token Selection Guide](#token-selection-guide)
- [Rotation Process](#rotation-process)
- [Emergency Procedures](#emergency-procedures)
- [Compliance](#compliance)
- [Audit Log](#audit-log)

---

## Active Tokens

### ⚠️ Legacy Token (Being Deprecated)

| Token Name                   | Purpose                    | Scopes                         | Location                                    | Owner | Created | Expiration | Status                             |
| ---------------------------- | -------------------------- | ------------------------------ | ------------------------------------------- | ----- | ------- | ---------- | ---------------------------------- |
| ⚠️ `master-org-token-011726` | **Legacy universal token** | Unknown (not yet in 1Password) | 1Password: Personal/master-org-token-011726 | Admin | Unknown | Unknown    | 🔴 **NOT FOUND - Skip to Phase 1** |

**⚠️ DISCOVERY:** The master-org-token-011726 does not currently exist in
1Password. Analysis shows it was referenced in scripts but never stored. This
validates the need for token segmentation.

**📋 REVISED APPROACH:** Skip legacy token migration, proceed directly to Phase 1
(create purpose-specific tokens)

**⏰ Implementation Timeline:**

- **Phase 1 (This Week):** Create and test purpose-specific tokens ← **READY TO
  START**
- **Phase 2 (This Week):** Update all script references to use new tokens
- **Phase 3 (Next Week):** Monitor for issues, verify all migrations
- **Phase 4 (Not Needed):** ~~Revoke master token~~ (doesn't exist)

**Scripts to Update (Currently No Authentication):**

- ✏️ `scripts/complete-project-setup.sh` - Add `org-project-admin-token`
- ✏️ `automation/scripts/web_crawler.py` - Add `org-repo-analysis-token`
- ✏️ `automation/scripts/sync_labels.py` - Add `org-label-sync-token`
- ✏️ `automation/scripts/secret_manager.py` - Remove default, require explicit
  token name
- ✏️ `automation/scripts/utils.py` - Add token parameter (use provided or
  default to gh CLI)
- ℹ️ `DEPLOY_PHASE*.sh` - Documentation only (no code changes needed)

**Migration Status:** 🟢 **Ready to Start - No Legacy Token to Migrate**

- Run: `/workspace/scripts/token-segmentation-migration.sh` (Option 1: Create
  all tokens)
- See:
  [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)

---

## Purpose-Specific Tokens (Migration Target)

### Segmented Tokens (Ready to Create)

| Token Name                | Purpose                                             | Scopes Required                 | Location             | Expiration | Rotation Schedule | Status                 |
| ------------------------- | --------------------------------------------------- | ------------------------------- | -------------------- | ---------- | ----------------- | ---------------------- |
| `org-label-sync-token`    | Synchronize labels across organization repositories | `repo`, `workflow`              | 1Password: Personal/ | 90 days    | 90 days           | 🔴 **Not yet created** |
| `org-project-admin-token` | Create and manage GitHub Projects                   | `project`, `read:org`           | 1Password: Personal/ | 90 days    | 90 days           | 🔴 **Not yet created** |
| `org-repo-analysis-token` | Read-only repository health checks and metrics      | `repo:status`, `read:org`       | 1Password: Personal/ | 180 days   | 180 days          | 🔴 **Not yet created** |
| `org-onboarding-token`    | Automated repository onboarding and setup           | `repo`, `workflow`, `admin:org` | 1Password: Personal/ | 60 days    | 60 days           | 🔴 **Not yet created** |

**Creation Steps:**

1. Go to https://github.com/settings/tokens/new
1. Create each token with specified scopes and expiration
1. Store in 1Password:
   `op item create --category="Password" --title="<token-name>" password="<token-value>"`
1. Run validation: `/workspace/automation/scripts/validate_tokens.py`
1. Update scripts: `/workspace/scripts/token-segmentation-migration.sh`

**Or use automated wizard:**
`/workspace/scripts/token-segmentation-migration.sh`

---

## Usage Guidelines

### When to Create a New Token

Create a **new token** when:

- 🎯 **Distinct purpose** - Your script has a unique purpose not covered by
  existing tokens
- 🔒 **Minimal scopes** - You need fewer scopes than any existing token provides
- 👥 **Team separation** - Different teams need different access levels
- ⏰ **Different rotation** - You need a different rotation schedule for
  compliance
- 🔍 **Audit separation** - You need a separate audit trail for specific
  operations

### When to Use an Existing Token

Use an **existing token** when:

- ✅ **Purpose match** - Your use case aligns with an existing token's purpose
- ✅ **Scope subset** - Required scopes are a subset of an existing token's
  scopes
- ✅ **Same team** - Same team/owner as the existing token
- ✅ **Same compliance** - Same compliance requirements (rotation, auditing)
- ✅ **No audit separation needed** - Operations can share audit trail

### When to Use secrets.GITHUB_TOKEN

Use the **automatically-provided GitHub Actions token** when:

- ✅ Operating **within a GitHub Actions workflow**
- ✅ Only need **standard workflow permissions** (read repo, write comments,
  etc.)
- ✅ Don't need **organization-level permissions**
- ✅ Don't need **elevated repository permissions**

**Note:** `secrets.GITHUB_TOKEN` is automatically provided and rotated by
GitHub. Never store it in 1Password or pass it between systems.

---

## Token Selection Guide

### Quick Reference Table

```
Need to...                              → Use token...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sync labels across repositories         → org-label-sync-token
Create/modify labels in a repo           → org-label-sync-token
Deploy workflow templates                → org-onboarding-token
Create GitHub Projects                   → org-project-admin-token
Manage project fields/views              → org-project-admin-token
Analyze repository health (read-only)    → org-repo-analysis-token
Collect organization metrics             → org-repo-analysis-token
Onboard new repositories                 → org-onboarding-token
Configure repository settings            → org-onboarding-token
Run in GitHub Actions workflow           → secrets.GITHUB_TOKEN (default)
CI/CD pipeline operations                → secrets.GITHUB_TOKEN (default)
Emergency admin operations               → Generate temporary token (1 day)
Development/testing                      → Your personal development token
```

### Decision Tree

```
┌─────────────────────────────────────┐
│  Need GitHub authentication?        │
└───────────────┬─────────────────────┘
                │
                ▼
        ┌───────────────────┐
        │ Running in GitHub │
        │ Actions workflow? │
        └────┬──────────┬───┘
             │          │
            Yes        No
             │          │
             ▼          ▼
   ┌──────────────┐  ┌──────────────────────┐
   │ Use:         │  │ What operation?      │
   │ secrets.     │  └──┬──────────────┬───┘
   │ GITHUB_TOKEN │     │              │
   └──────────────┘     │              │
                   ┌────▼─────┐  ┌─────▼──────┐
                   │ Read-only│  │Read/Write  │
                   │ analysis?│  │operations? │
                   └────┬─────┘  └─────┬──────┘
                        │              │
                       Yes            Yes
                        │              │
                        ▼              ▼
            ┌────────────────────┐  ┌──────────────────┐
            │ org-repo-analysis  │  │ Check purpose:   │
            │ -token             │  │ Labels? Projects?│
            └────────────────────┘  │ Onboarding?      │
                                    └────────┬─────────┘
                                             │
                         ┌───────────────────┼──────────────┐
                         ▼                   ▼              ▼
                 ┌───────────────┐  ┌────────────┐  ┌─────────────┐
                 │ org-label-    │  │ org-project│  │ org-        │
                 │ sync-token    │  │ -admin-token│  │ onboarding- │
                 │               │  │            │  │ token       │
                 └───────────────┘  └────────────┘  └─────────────┘
```

---

## Rotation Process

### Standard Rotation Procedure

**Frequency:** Based on token's rotation schedule (60/90/180 days)

**Steps:**

1. **Generate new token**

   ```bash
   # Go to GitHub Settings → Developer Settings → Personal Access Tokens
   # Click "Generate new token (classic)"
   # Name: <token-name>-YYYYMMDD
   # Expiration: Match rotation schedule
   # Scopes: Match requirements in registry
   # Click "Generate token" and copy immediately
   ```

1. **Store in 1Password**

   ```bash
   # Update existing item (recommended - preserves item ID)
   op item edit "<token-name>" password="<new-token-value>"

   # Or create new item (creates new item ID)
   op item create \
     --category "Password" \
     --title "<token-name>" \
     --vault "Personal" \
     password="<new-token-value>"
   ```

1. **Test new token**

   ```bash
   # Retrieve and verify
   TOKEN=$(op read "op://Personal/<token-name>/password" --reveal)
   echo "Token retrieved: ${TOKEN:0:4}..."

   # Test authentication
   curl -H "Authorization: token $TOKEN" \
        https://api.github.com/user | jq '.login'

   # Expected: Your GitHub username
   ```

1. **Test with affected scripts (dry-run)**

   ```bash
   # Example: Label sync
   python3 automation/scripts/sync_labels.py \
     --dry-run \
     --token-name <token-name>

   # Example: Project setup
   export GH_TOKEN=$(op read "op://Personal/<token-name>/password" --reveal)
   python3 scripts/configure-github-projects.py --dry-run
   ```

1. **Monitor for errors**

   ```bash
   # Check logs for 24 hours after rotation
   # Look for authentication failures
   # Verify all scripts using the token still work
   ```

1. **Revoke old token**

   ```bash
   # After 24-48 hours of successful operations:
   # Go to GitHub Settings → Developer Settings → Personal Access Tokens
   # Find old token (by creation date or name)
   # Click "Delete" and confirm
   ```

1. **Update registry**

   ```bash
   # Edit this file (TOKEN_REGISTRY.md)
   # Update "Last Rotated" date
   # Update "Expiration" date
   # Add entry to Audit Log section
   # Commit changes
   ```

### Automated Rotation (Recommended)

Use the provided rotation script:

```bash
# Usage
./scripts/rotate-token.sh <token-name>

# Example
./scripts/rotate-token.sh org-label-sync-token
```

The script will:

- Guide you through token generation
- Update 1Password automatically
- Run validation tests
- Prompt for old token revocation
- Update this registry file

---

## Emergency Procedures

### Scenario 1: Token Compromised 🚨

**Immediate actions (within 15 minutes):**

1. **Revoke token immediately**

   ```bash
   # Go to: https://github.com/settings/tokens
   # Find the compromised token
   # Click "Delete" button
   # Confirm deletion
   ```

1. **Notify team**

   ```bash
   # Post to #security-alerts Slack channel
   # Include: Token name, suspected compromise time
   # Do NOT include token value
   ```

1. **Generate emergency replacement**

   ```bash
   # Generate with DIFFERENT name: <token-name>-emergency-YYYYMMDD
   # Use SAME scopes as original
   # Set expiration to 7 days (temporary)
   ```

1. **Deploy emergency token**

   ```bash
   # Update 1Password with NEW item name
   op item create \
     --category "Password" \
     --title "<token-name>-emergency-20260118" \
     --vault "Personal" \
     password="<emergency-token>"

   # Update scripts to use emergency token name
   # Or: Update original item to point to emergency token
   ```

1. **Audit for unauthorized activity**

   ```bash
   # Check GitHub audit log
   # Look for: Unexpected API calls, permission changes, data access
   # Time range: Last access of compromised token to now
   # Export audit log for investigation
   ```

**Follow-up actions (within 24 hours):**

6. **Investigate root cause**
   - How was token exposed?
   - Where was it stored/transmitted insecurely?
   - Who had access?

1. **Generate permanent replacement**
   - Use original token name
   - Standard rotation schedule
   - Replace emergency token

1. **Implement preventions**
   - Fix root cause
   - Update security procedures
   - Additional monitoring if needed

1. **Document incident**
   - Update audit log (below)
   - Lessons learned
   - Prevention measures

### Scenario 2: Token Expired

**Symptoms:**

- Scripts fail with "401 Unauthorized" or "Bad credentials"
- GitHub API returns authentication errors

**Resolution:**

1. **Verify expiration**

   ```bash
   # Test token
   TOKEN=$(op read "op://Personal/<token-name>/password" --reveal)
   curl -H "Authorization: token $TOKEN" \
        https://api.github.com/user

   # If response: "Bad credentials" → Token expired or invalid
   ```

1. **Generate replacement token**

   ```bash
   # Follow standard rotation procedure (above)
   # Use SAME token name in 1Password
   # This updates the value without changing scripts
   ```

1. **Update 1Password**

   ```bash
   # Overwrites old value
   op item edit "<token-name>" password="<new-token>"
   ```

1. **Test immediately**

   ```bash
   # Verify new token works
   TOKEN=$(op read "op://Personal/<token-name>/password" --reveal)
   curl -H "Authorization: token $TOKEN" \
        https://api.github.com/user | jq '.login'
   ```

1. **Resume operations**

   ```bash
   # Re-run failed scripts
   # Monitor for additional failures
   ```

### Scenario 3: 1Password CLI Failure

**Symptoms:**

- `op` command not found
- Authentication errors with 1Password
- Cannot retrieve secrets

**Resolution:**

1. **Check 1Password CLI status**

   ```bash
   # Verify CLI installed
   which op
   op --version

   # Check authentication
   op account list
   ```

1. **Re-authenticate if needed**

   ```bash
   eval $(op signin)
   # Follow prompts to authenticate
   ```

1. **Emergency token retrieval**

   ```bash
   # Manual retrieval from 1Password app
   # Open 1Password desktop/web app
   # Navigate to item
   # Copy token value manually
   # Export as environment variable
   export GH_TOKEN="<token-value>"
   ```

1. **Fix 1Password CLI**

   ```bash
   # Reinstall if necessary
   # macOS
   brew reinstall --cask 1password-cli

   # Linux
   curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
     sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
   ```

1. **Resume automated retrieval**

   ```bash
   # Test automated retrieval
   op read "op://Personal/org-label-sync-token/password" --reveal
   ```

### Scenario 4: Rate Limit Exceeded

**Symptoms:**

- HTTP 403 responses
- Error: "API rate limit exceeded"
- Headers show `X-RateLimit-Remaining: 0`

**Resolution:**

1. **Check rate limit status**

   ```bash
   TOKEN=$(op read "op://Personal/<token-name>/password" --reveal)
   curl -H "Authorization: token $TOKEN" \
        https://api.github.com/rate_limit | jq
   ```

1. **Wait for reset**

   ```bash
   # Check reset time
   # X-RateLimit-Reset header contains Unix timestamp
   # Wait until that time

   # Or calculate wait time
   RESET_TIME=$(curl -H "Authorization: token $TOKEN" \
                -I https://api.github.com/rate_limit | \
                grep -i 'x-ratelimit-reset' | cut -d' ' -f2)
   CURRENT_TIME=$(date +%s)
   WAIT_SECONDS=$((RESET_TIME - CURRENT_TIME))
   echo "Wait ${WAIT_SECONDS} seconds ($(($WAIT_SECONDS / 60)) minutes)"
   ```

1. **Optimize script to reduce calls**

   ```bash
   # Use GraphQL instead of REST (fewer calls)
   # Implement caching
   # Batch operations
   # Add delays between requests
   ```

1. **Consider GitHub App for higher limits**

   ```bash
   # PAT: 5,000 requests/hour
   # GitHub App: 5,000 requests/hour PER INSTALLATION
   # See MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md
   ```

---

## Compliance

### Rotation Schedule

| Security Tier   | Rotation Frequency | Token Types                                       |
| --------------- | ------------------ | ------------------------------------------------- |
| 🔴 **Critical** | 60 days            | `org-onboarding-token` (admin:org scope)          |
| 🟡 **High**     | 90 days            | `org-label-sync-token`, `org-project-admin-token` |
| 🟢 **Medium**   | 180 days           | `org-repo-analysis-token` (read-only)             |

### Access Reviews

| Review Type             | Frequency | Scope                                                     |
| ----------------------- | --------- | --------------------------------------------------------- |
| **Token Inventory**     | Monthly   | Verify all tokens in registry are still active and needed |
| **Scope Audit**         | Quarterly | Verify each token has minimal required scopes             |
| **Usage Review**        | Quarterly | Review audit logs for unexpected usage patterns           |
| **Security Assessment** | Annually  | Full security review of token management practices        |

### Audit Logging

All token operations are logged:

- **GitHub Audit Log**: All API calls made with each token
  - View at: https://github.com/organizations/ivviiviivvi/settings/audit-log
  - Retention: 90 days (GitHub Team), 180 days (GitHub Enterprise)

- **1Password Activity Log**: All secret retrievals
  - View in 1Password app → Settings → Activity
  - Shows: Who accessed which item, when

- **Script Logs**: Application-level logging
  - Location: `logs/` directory in each script's output
  - Retention: 30 days

### Compliance Standards

| Standard              | Requirement                  | Status          |
| --------------------- | ---------------------------- | --------------- |
| **PCI DSS 8.2.4**     | Rotate tokens every 90 days  | 🔄 In progress  |
| **SOC 2 CC6.1**       | Access reviews quarterly     | ✅ Scheduled    |
| **ISO 27001 A.9.2.3** | Privileged access management | 🔄 Implementing |
| **NIST 800-53 IA-5**  | Authenticator management     | ✅ Compliant    |

---

## Audit Log

### Token Lifecycle Events

| Date       | Event                | Token                     | Actor         | Details                                 |
| ---------- | -------------------- | ------------------------- | ------------- | --------------------------------------- |
| 2026-01-18 | 📝 Registry Created  | -                         | System        | Initial token registry created          |
| 2026-01-18 | 🔍 Analysis Complete | `master-org-token-011726` | Security Team | Contextual awareness analysis completed |
| 2026-01-18 | 📋 Migration Plan    | `master-org-token-011726` | Security Team | Segmentation migration plan approved    |

### Rotation History

| Date       | Token                     | Action  | Previous Expiry | New Expiry | Rotated By | Notes                  |
| ---------- | ------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------- |
| 2026-01-17 | `master-org-token-011726` | Created | -               | Unknown    | Admin      | Initial token creation |

### Security Incidents

| Date | Incident | Token | Severity | Resolution | Root Cause |
| ---- | -------- | ----- | -------- | ---------- | ---------- |
| -    | -        | -     | -        | -          | -          |

---

## Related Documentation

- [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
  \- Detailed analysis and migration plan
- [SECRET_MANAGEMENT_GUIDE.md](SECRET_MANAGEMENT_GUIDE.md) - Universal secret
  management practices
- [SECRETS_SETUP.md](SECRETS_SETUP.md) - GitHub Actions secrets configuration
- `scripts/rotate-token.sh` - Automated token rotation script
- `scripts/validate-tokens.py` - Token health validation script

---

## Contact & Support

**Questions about tokens?**

- 💬 Slack: #security-engineering
- 📧 Email: security@ivviiviivvi.org
- 📝 Issues:
  [GitHub Issues](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

**Token issues?**

- 🚨 Emergency: Follow procedures above, then notify #security-alerts
- 📋 Non-urgent: Create ticket with Security Team
- 📖 Documentation: Update this registry and submit PR

---

**Registry maintained by:** Organization Security Team\
**Next review:**
2026-04-18\
**Version:** 1.0.0
