# Week 11 Phase 1: Manual Deployment Guide

**Date**: January 16, 2026\
**Status**: Required due to token permission
limitations\
**Estimated Time**: 15-20 minutes

______________________________________________________________________

## Overview

Automated label deployment is blocked by GitHub token permissions (403
Forbidden). Both the `batch_onboard_repositories.py` script and `gh` CLI are
using GitHub Actions tokens that lack the `issues: write` permission required to
create or modify labels.

This guide provides instructions for manual label deployment to the 3 Phase 1
pilot repositories.

______________________________________________________________________

## Affected Repositories

1. **{{ORG_NAME}}/theoretical-specifications-first** (Score: 87)
1. **{{ORG_NAME}}/system-governance-framework** (Score: 69)
1. **{{ORG_NAME}}/trade-perpetual-future** (Score: 63)

______________________________________________________________________

## Labels to Deploy

The following 12 labels should be created in each repository:

### Status Labels

| Name                        | Color    | Description                  |
| --------------------------- | -------- | ---------------------------- |
| `status: in progress`       | `1d76db` | Work is actively in progress |
| `status: ready for review`  | `0e8a16` | Ready for team review        |
| `status: changes requested` | `d93f0b` | Changes have been requested  |

### Priority Labels

| Name               | Color    | Description                 |
| ------------------ | -------- | --------------------------- |
| `priority: high`   | `d93f0b` | High priority issue or PR   |
| `priority: medium` | `fbca04` | Medium priority issue or PR |
| `priority: low`    | `0e8a16` | Low priority issue or PR    |

### Type Labels

| Name                  | Color    | Description                     |
| --------------------- | -------- | ------------------------------- |
| `type: bug`           | `d73a4a` | Something isn't working         |
| `type: feature`       | `a2eeef` | New feature or request          |
| `type: enhancement`   | `84b6eb` | Improvement to existing feature |
| `type: documentation` | `0075ca` | Documentation improvements      |

### Deployment Tracking Labels

| Name                          | Color    | Description                               |
| ----------------------------- | -------- | ----------------------------------------- |
| `deployment: week-11-phase-1` | `5319e7` | Deployed in Week 11 Phase 1 (Pilot)       |
| `automation: batch-deployed`  | `006b75` | Repository onboarded via batch automation |

______________________________________________________________________

## Manual Deployment Methods

### Option 1: GitHub Web Interface (Recommended)

**Time**: ~5 minutes per repository (15 minutes total)

**Steps for each repository**:

1. Navigate to repository:
   `https://github.com/{{ORG_NAME}}/<repository-name>/labels`
1. Click **"New label"** button
1. For each label:
   - Enter **Name** (e.g., `status: in progress`)
   - Enter **Color** (without `#`, e.g., `1d76db`)
   - Enter **Description**
   - Click **"Create label"**
1. Repeat for all 12 labels

**Direct Links**:

- [theoretical-specifications-first labels](https://github.com/%7B%7BORG_NAME%7D%7D/theoretical-specifications-first/labels)
- [system-governance-framework labels](https://github.com/%7B%7BORG_NAME%7D%7D/system-governance-framework/labels)
- [trade-perpetual-future labels](https://github.com/%7B%7BORG_NAME%7D%7D/trade-perpetual-future/labels)

### Option 2: GitHub CLI with Personal Access Token

**Time**: ~10 minutes (one-time setup + deployment)

**Prerequisites**:

1. Generate a fine-grained Personal Access Token:

   - Go to: https://github.com/settings/tokens?type=beta
   - Click **"Generate new token"**
   - Token name: `Week 11 Label Deployment`
   - Expiration: 7 days
   - Repository access: Select the 3 repositories
   - Permissions:
     - Repository permissions → Issues: **Read and write**
   - Click **"Generate token"**
   - Copy the token (starts with `github_pat_`)

1. Authenticate with the new token:

   ```bash
   gh auth login --with-token <<< "YOUR_TOKEN_HERE"
   ```

**Deployment**:

```bash
# Use the deployment script with authenticated gh CLI
/tmp/deploy-phase1-labels.sh
```

### Option 3: Sync from .github Repository

**Time**: ~5 minutes

**If .github repository has label config file**:

1. Check if label config exists:

   ```bash
   cat .github/labels.yml
   ```

1. If exists, use GitHub's label sync action or manual import in each repository

______________________________________________________________________

## Verification

After deployment, verify labels were created successfully:

### Using gh CLI:

```bash
gh label list --repo {{ORG_NAME}}/theoretical-specifications-first
gh label list --repo {{ORG_NAME}}/system-governance-framework
gh label list --repo {{ORG_NAME}}/trade-perpetual-future
```

### Using Web Interface:

Visit each repository's labels page and confirm all 12 labels are present with
correct colors and descriptions.

______________________________________________________________________

## Expected Results

After successful deployment:

- ✅ 3 repositories updated
- ✅ 12 labels per repository
- ✅ 36 total labels created
- ✅ All labels have correct colors and descriptions
- ✅ Phase 1 pilot repositories ready for workflow testing

______________________________________________________________________

## Troubleshooting

### Issue: Cannot create labels in web interface

**Cause**: Insufficient repository permissions

**Solution**: Ensure you have **Write** or **Admin** access to the repositories.
Contact repository owner to grant access.

### Issue: gh CLI still returns 403 Forbidden

**Cause**: Still using GitHub Actions token instead of PAT

**Solution**:

```bash
# Check current auth
gh auth status

# Switch to PAT
gh auth login --with-token <<< "YOUR_PAT_HERE"

# Verify new token is used
gh auth status
```

### Issue: Label already exists

**Action**: Update the existing label instead of creating new one

**Web Interface**: Click on label name → Edit → Update
color/description\
**CLI**: Use `gh label edit` instead of `gh label create`

______________________________________________________________________

## Alternative: Defer to Phase 2

If manual deployment is not immediately feasible, consider:

1. **Document the requirement** in Phase 2 planning
1. **Obtain GitHub App** with proper permissions for Phase 2
1. **Deploy labels as part of Phase 2** expansion to all 8 repositories
1. **Focus Phase 1 on** workflow deployment only (once path resolution is fixed)

This approach consolidates label deployment into Phase 2 when proper automation
credentials are available.

______________________________________________________________________

## Post-Deployment Steps

Once labels are deployed:

1. **Update Phase 1 Status**:

   ```bash
   # Update WEEK_11_PHASE1_STATUS.md
   # Change: "❌ Deployment: BLOCKED"
   # To: "✅ Deployment: COMPLETE (manual)"
   ```

1. **Test Label Usage**:

   - Create a test issue in one repository
   - Apply the new labels
   - Verify they appear correctly

1. **Document Results**:

   - Record deployment method used
   - Note any issues encountered
   - Update success metrics

1. **Proceed to Workflow Deployment**:

   - Fix workflow path resolution issue
   - Deploy workflows to Phase 1 repositories
   - Complete Phase 1 validation

______________________________________________________________________

## Summary

**Manual deployment is the fastest path forward** given the current token
permission constraints. The web interface method requires ~15 minutes and no
additional setup. Once labels are deployed, Phase 1 can proceed to workflow
deployment and validation.

**Recommended**: Use **Option 1 (Web Interface)** for immediate deployment, then
obtain proper credentials for automated Phase 2 and Phase 3 deployments.

______________________________________________________________________

**Next Action**: Choose deployment method and execute, then update Phase 1
status documentation.
