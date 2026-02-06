# GitHub Token Registry

> **Central registry for all GitHub Personal Access Tokens and authentication
> mechanisms used in the {{ORG_NAME}} organization**

**Last Updated:** 2026-01-18\
**Owner:** Organization Security Team\
**Review
Schedule:** Quarterly (next: 2026-04-18)

______________________________________________________________________

## Table of Contents

- [Active Tokens](#active-tokens)
- [Usage Guidelines](#usage-guidelines)
- [Token Selection Guide](#token-selection-guide)
- [Rotation Process](#rotation-process)
- [Emergency Procedures](#emergency-procedures)
- [Compliance](#compliance)
- [Audit Log](#audit-log)

______________________________________________________________________

## Active Tokens

### ✅ Active Tokens

| Token Name                | Purpose                                             | Scopes                          | Location                                    | Owner | Created    | Expiration | Rotation Schedule | Status        |
| ------------------------- | --------------------------------------------------- | ------------------------------- | ------------------------------------------- | ----- | ---------- | ---------- | ----------------- | ------------- |
| `org-label-sync-token`    | Synchronize labels across organization repositories | `repo`, `workflow`              | 1Password: Personal/org-label-sync-token    | Admin | 2026-01-18 | 2026-04-18 | 90 days           | ✅ **Active** |
| `org-project-admin-token` | Create and manage GitHub Projects                   | `project`, `read:org`           | 1Password: Personal/org-project-admin-token | Admin | 2026-01-18 | 2026-04-18 | 90 days           | ✅ **Active** |
| `org-onboarding-token`    | Automated repository onboarding and setup           | `repo`, `workflow`, `admin:org` | 1Password: Personal/org-onboarding-token    | Admin | 2026-01-18 | 2026-03-19 | 60 days           | ✅ **Active** |
| `org-repo-analysis-token` | Read-only repository health checks and metrics      | `repo:status`, `read:org`       | 1Password: Personal/org-repo-analysis-token | Admin | 2026-01-18 | 2026-07-17 | 180 days          | ✅ **Active** |

**✅ MIGRATION COMPLETE:** All 4 purpose-specific tokens are now active and in
use.

**📋 Implementation Summary:**

- **Phase 1 (2026-01-18):** ✅ Created 4 tokens in GitHub with minimal scopes
- **Phase 1 (2026-01-18):** ✅ Stored all tokens in 1Password Personal vault
- **Phase 1 (2026-01-18):** ✅ Validated all tokens via GitHub API
- **Phase 2 (2026-01-18):** ✅ Updated 5 scripts to use purpose-specific tokens
- **Phase 2 (2026-01-18):** ✅ Deployed changes to production (commit f7f69dd)

**Scripts Updated:**

- ✅ `scripts/complete-project-setup.sh` - Uses `org-project-admin-token`
- ✅ `automation/scripts/web_crawler.py` - Uses `org-repo-analysis-token`
- ✅ `automation/scripts/sync_labels.py` - Uses `org-label-sync-token`
- ✅ `automation/scripts/secret_manager.py` - Requires explicit token names
- ✅ `automation/scripts/utils.py` - Prefers gh CLI, fallback to
  `org-label-sync-token`

**Migration Notes:** The legacy "master-org-token-011726" never existed in
1Password, allowing for a clean implementation of security best practices from
day one.

______________________________________________________________________

### ⚠️ Legacy Token (Deprecated)

| Token Name                   | Purpose                    | Status                                                       |
| ---------------------------- | -------------------------- | ------------------------------------------------------------ |
| ⚠️ `master-org-token-011726` | **Legacy universal token** | 🔴 **Never existed - Scripts referenced non-existent token** |

**Historical Note:** Investigation revealed this token was referenced in scripts
but never created or stored in 1Password. This discovery led to implementing
purpose-specific tokens following the principle of least privilege.

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

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

1. **Investigate root cause**

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

______________________________________________________________________

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

  - View at:
    <https://github.com/organizations/%7B%7BORG_NAME%7D%7D/settings/audit-log>
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

______________________________________________________________________

## Audit Log

### Token Lifecycle Events

| Date       | Event                | Token                     | Actor         | Details                                 |
| ---------- | -------------------- | ------------------------- | ------------- | --------------------------------------- |
| 2026-01-18 | 📝 Registry Created  | -                         | System        | Initial token registry created          |
| 2026-01-18 | 🔍 Analysis Complete | `master-org-token-011726` | Security Team | Contextual awareness analysis completed |
| 2026-01-18 | 📋 Migration Plan    | `master-org-token-011726` | Security Team | Segmentation migration plan approved    |
| 2026-01-18 | ✅ Phase 1 Complete  | All 4 tokens              | Admin         | Created, stored, and validated          |
| 2026-01-18 | ✅ Phase 2 Complete  | All 5 scripts             | Admin         | Scripts updated to use new tokens       |
| 2026-01-18 | 🚀 Deployed          | -                         | Admin         | Changes pushed to main (commit f7f69dd) |

### Rotation History

| Date       | Token                     | Action  | Previous Expiry | New Expiry | Rotated By | Notes                          |
| ---------- | ------------------------- | ------- | --------------- | ---------- | ---------- | ------------------------------ |
| 2026-01-18 | `org-label-sync-token`    | Created | -               | 2026-04-18 | Admin      | Initial creation (90d expiry)  |
| 2026-01-18 | `org-project-admin-token` | Created | -               | 2026-04-18 | Admin      | Initial creation (90d expiry)  |
| 2026-01-18 | `org-onboarding-token`    | Created | -               | 2026-03-19 | Admin      | Initial creation (60d expiry)  |
| 2026-01-18 | `org-repo-analysis-token` | Created | -               | 2026-07-17 | Admin      | Initial creation (180d expiry) |

### Security Incidents

| Date | Incident | Token | Severity | Resolution | Root Cause |
| ---- | -------- | ----- | -------- | ---------- | ---------- |
| -    | -        | -     | -        | -          | -          |

______________________________________________________________________

## Related Documentation

- [MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md](../analysis/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md)
  \- Detailed analysis and migration plan
- [SECRET_MANAGEMENT_GUIDE.md](../guides/SECRET_MANAGEMENT_GUIDE.md) - Universal
  secret management practices
- [SECRETS_SETUP.md](../guides/SECRETS_SETUP.md) - GitHub Actions secrets
  configuration
- `scripts/rotate-token.sh` - Automated token rotation script
- `scripts/validate-tokens.py` - Token health validation script

______________________________________________________________________

## Contact & Support

**Questions about tokens?**

- 💬 Slack: #security-engineering
- 📧 Email: \<security@{{ORG_NAME}}.org>
- 📝 Issues:
  [GitHub Issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->

**Token issues?**

- 🚨 Emergency: Follow procedures above, then notify #security-alerts
- 📋 Non-urgent: Create ticket with Security Team
- 📖 Documentation: Update this registry and submit PR

______________________________________________________________________

**Registry maintained by:** Organization Security Team\
**Next review:**
2026-04-18\
**Version:** 1.0.0

### Day 1 Token Validation (2026-01-18)

| Date       | Event                     | Token                   | Status       | Details                                   |
| ---------- | ------------------------- | ----------------------- | ------------ | ----------------------------------------- |
| 2026-01-18 | ✅ Phase 3 Day 1 Complete | All 4 tokens            | ✅ Validated | All tokens working, rate limits healthy   |
| 2026-01-18 | 🔧 Auth Solution          | Environment Variables   | ✅ Deployed  | Permanent storage in ~/.github-tokens     |
| 2026-01-18 | 📝 Auto-load Configured   | ~/.bashrc               | ✅ Active    | Tokens load automatically in all sessions |
| 2026-01-18 | 🔍 Rate Limit Check       | org-label-sync-token    | ✅ Healthy   | 4800+/5000 remaining                      |
| 2026-01-18 | 🔍 Rate Limit Check       | org-project-admin-token | ✅ Healthy   | 4800+/5000 remaining                      |
| 2026-01-18 | 🔍 Rate Limit Check       | org-onboarding-token    | ✅ Healthy   | 4800+/5000 remaining                      |
| 2026-01-18 | 🔍 Rate Limit Check       | org-repo-analysis-token | ✅ Healthy   | 4800+/5000 remaining                      |
