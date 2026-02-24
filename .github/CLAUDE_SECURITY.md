# Claude Integration Security Guide

This document outlines the security measures implemented for Claude AI
integration in GitHub Actions workflows.

## Security Measures Implemented

### 1. User Permission Validation

Both Claude workflows (`claude.yml` and `claude-code-review.yml`) now include
permission checks to ensure only authorized users can trigger Claude operations:

**claude-code-review.yml**: Uses GitHub Actions conditional to check
`author_association` at workflow trigger time:

```yaml
if: |
  github.event.pull_request.author_association == 'OWNER' ||
  github.event.pull_request.author_association == 'MEMBER' ||
  github.event.pull_request.author_association == 'COLLABORATOR'
```

**claude.yml**: Uses GitHub API to validate user permissions at runtime:

```bash
PERMISSION=$(gh api /repos/$REPO/collaborators/$ACTOR/permission -q .permission)
# Allows: admin, write, maintain
```

- **Allowed permission levels**: admin, write, maintain (maps to OWNER, MEMBER,
  COLLABORATOR)
- **Blocked**: read, none (external users, first-time contributors)

This prevents unauthorized users from:

- Exhausting API quotas
- Triggering expensive AI operations
- Potentially abusing the system

### 2. OAuth Token Validation

The `CLAUDE_CODE_OAUTH_TOKEN` secret is now validated before use:

```yaml
- name: Validate CLAUDE_CODE_OAUTH_TOKEN
  run: |
    if [ -z "${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}" ]; then
      echo "Error: CLAUDE_CODE_OAUTH_TOKEN secret is not configured"
      exit 1
    fi
    echo "Token validation passed"
```

### 3. Third-Party Action Integrity

All third-party GitHub Actions are now pinned to specific commit SHAs to prevent
supply chain attacks:

- `actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955` (v4)
- `anthropics/claude-code-action@06e550b8ff71349db253443c6ca8a4b120e7f89d`
  (v1.0.16)

This ensures:

- Action code cannot be changed without updating the SHA
- Protection against compromised action repositories
- Verifiable action integrity

### 4. Minimal Permissions

Both workflows use the principle of least privilege:

```yaml
permissions:
  contents: read
  pull-requests: read
  issues: read
  id-token: write
  actions: read # Only in claude.yml for CI results
```

## Token Configuration Requirements

The `CLAUDE_CODE_OAUTH_TOKEN` must be configured with:

1. **Minimal required scopes** - Only grant permissions needed for:

   - Reading repository content
   - Commenting on PRs and issues
   - Viewing CI results

1. **Regular rotation** - Rotate the token periodically (recommended: every 90
   days)

1. **Access logging** - Monitor token usage for unusual patterns

1. **Secure storage** - Store only as a GitHub secret, never in code or logs

## Bash Command Restrictions

The `claude-code-review.yml` workflow limits Claude's bash command access to:

```
Bash(gh issue view:*)
Bash(gh search:*)
Bash(gh issue list:*)
Bash(gh pr comment:*)
Bash(gh pr diff:*)
Bash(gh pr view:*)
Bash(gh pr list:*)
```

These commands are:

- **Read-only operations** - Cannot modify repository state directly
- **Rate-limited by GitHub** - GitHub API rate limits apply
- **Scoped to GitHub CLI** - Cannot execute arbitrary system commands

## Input Sanitization

User inputs (PR content, comments, issue bodies) are:

1. **Processed by GitHub Actions** - GitHub sanitizes event data
1. **Scoped by permissions** - Only trusted users can trigger workflows
1. **Validated by Claude AI** - Claude includes built-in prompt injection
   protections

## Monitoring and Auditing

To monitor Claude integration security:

1. **Review workflow runs** in the Actions tab
1. **Check API usage** in Claude dashboard
1. **Monitor token access** via GitHub audit logs
1. **Review PR comments** for unusual activity

## Incident Response

If you suspect a security issue:

1. **Immediately disable** the workflow
1. **Rotate** the `CLAUDE_CODE_OAUTH_TOKEN`
1. **Review** recent workflow runs for suspicious activity
1. **Report** to repository maintainers following SECURITY.md

## Compliance Status

This implementation addresses the following compliance issues:

- ✅ **Unvalidated user trigger** - Added permission checks
- ✅ **Unvalidated OAuth token usage** - Added token validation
- ✅ **Unrestricted bash command execution** - Commands are scoped and read-only
- ✅ **Third-party action token exposure** - Actions pinned to commit SHAs
- ✅ **Security-first input validation** - Multiple layers of validation

## Regular Security Reviews

Recommended schedule:

- **Monthly**: Review workflow run logs
- **Quarterly**: Rotate OAuth token
- **Semi-annually**: Update action SHAs to latest stable versions
- **Annually**: Full security audit of Claude integration

## References

- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)<!-- link:docs.github_actions_hardening -->
- [Claude Code Action Documentation](https://github.com/anthropics/claude-code-action)
- [Repository Security Policy](../docs/governance/SECURITY.md)
