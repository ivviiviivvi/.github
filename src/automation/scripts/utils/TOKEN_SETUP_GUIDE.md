# GitHub Personal Access Token Setup Guide

## Issue

The GitHub CLI token (`GITHUB_TOKEN`) doesn't have sufficient permissions to
create organization projects. You need a Personal Access Token (PAT) with
specific scopes.

## Error Encountered

```
"type": "FORBIDDEN",
"message": "Resource not accessible by integration"
```

## Solution: Create a Personal Access Token

### Step 1: Generate New Token

1. Go to: https://github.com/settings/tokens?type=beta
1. Click **"Generate new token"** → **"Generate new token (classic)"**
1. Fill in the form:

**Token Name:** `GitHub Projects Management`

**Expiration:** Choose appropriate expiration (90 days recommended)

**Scopes Required:**

- ✅ `project` - Full control of projects
  - `read:project` - Read project data
  - `write:project` - Write project data
- ✅ `read:org` - Read organization data
- ✅ `repo` - Full control of repositories (needed for adding items)
  - `repo:status` - Access commit status
  - `repo_deployment` - Access deployment status
  - `public_repo` - Access public repositories

**Minimum Required Scopes:**

```
project (full)
read:org
```

4. Click **"Generate token"**
1. **IMPORTANT:** Copy the token immediately (starts with `ghp_`)

### Step 2: Store Token in 1Password

```bash
# Add to 1Password via CLI
op item create --category=Login \
  --title="GitHub PAT - Projects" \
  --vault="Your Vault" \
  'username=4444J99' \
  'credential[password]=ghp_your_token_here'

# Or add via 1Password app:
# 1. Open 1Password app
# 2. Create new "Password" item
# 3. Title: "GitHub PAT - Projects"
# 4. Save the token
```

### Step 3: Configure Deployment Script

Set your 1Password reference:

```bash
# Export the reference path
export OP_REFERENCE="op://YourVault/GitHub PAT - Projects/credential"

# Test retrieval
op read "$OP_REFERENCE"
```

### Step 4: Deploy

```bash
# Using 1Password
./deploy-with-1password.sh

# Or set environment variable directly
export GH_TOKEN="ghp_your_token_here"
./deploy.sh
```

## Alternative: Use Existing 1Password Token

If you already have a GitHub PAT in 1Password:

```bash
# Find your token reference
op item list --vault YourVault | grep -i github

# Get the reference path
op item get "Your GitHub Token Item" --format json | jq -r '.fields[] | select(.label=="password") | "op://YourVault/\(.id)/password"'

# Set and deploy
export OP_REFERENCE="op://YourVault/YourItem/password"
./deploy-with-1password.sh
```

## Verification

Check your token has correct scopes:

```bash
# Set token
export GH_TOKEN="ghp_your_token_here"

# Test GraphQL query
curl -H "Authorization: bearer $GH_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query":"query { viewer { login } }"}' \
     https://api.github.com/graphql
```

## Troubleshooting

### "Bad credentials" error

- Token is incorrect or expired
- Regenerate token from GitHub settings

### "Resource not accessible by integration"

- Token missing required scopes
- Regenerate with `project` and `read:org` scopes

### "Not Found" error

- Organization name might be wrong
- Verify: `gh api orgs/{{ORG_NAME}}`

### 1Password CLI not working

- Not signed in: `eval $(op signin)`
- Reference incorrect: Check with `op item list`
- Account not configured: Run `op account add`

## Security Best Practices

1. **Use 1Password:** Store tokens securely, never in code
1. **Limit Scopes:** Only grant necessary permissions
1. **Set Expiration:** Use 90-day expiration, rotate regularly
1. **Audit Access:** Review token usage in GitHub settings
1. **Revoke Old Tokens:** Delete unused tokens immediately

## Quick Reference

**Minimum token scopes needed:**

```
project (full control)
read:org (organization data)
```

**Deployment commands:**

```bash
# With 1Password
export OP_REFERENCE="op://Vault/Item/field"
./deploy-with-1password.sh

# With environment variable
export GH_TOKEN="ghp_your_token"
./deploy.sh

# Dry-run first
./deploy.sh --dry-run
```

## Next Steps After Token Setup

1. Generate new token with correct scopes
1. Store in 1Password
1. Run `./deploy-with-1password.sh` or set `GH_TOKEN`
1. Projects will be created successfully
1. Configure views and automation in GitHub UI

## Related Documentation

- [GitHub PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [1Password CLI Guide](./1PASSWORD_QUICK_START.md)
- [Deployment Guide](../../../../docs/guides/GITHUB_PROJECTS_DEPLOYMENT.md)
- [Ready to Deploy](./READY_TO_DEPLOY.md)
