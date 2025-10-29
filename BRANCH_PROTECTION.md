# Branch Protection Rules Configuration

This document outlines the recommended branch protection rules for repositories in the organization.

## Protection Rules for Production Branches (main/master)

### Required Settings

#### Pull Request Requirements
- ✅ **Require pull request reviews before merging**
  - Required number of approvers: 1 (minimum)
  - Dismiss stale pull request approvals when new commits are pushed: ✅
  - Require review from Code Owners: ✅
  - Restrict who can dismiss pull request reviews: ✅

#### Status Checks
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging: ✅
  - Status checks that must pass:
    - CI/CD pipeline
    - Unit tests
    - Integration tests
    - Code quality checks (linting)
    - Security scans (CodeQL, dependency scans)

#### Additional Restrictions
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (recommended for security-sensitive projects)
- ✅ **Include administrators** in these restrictions
- ✅ **Restrict pushes that create matching branches** (recommended)

#### Protection Against Force Pushes
- ✅ **Do not allow force pushes**
- ✅ **Do not allow deletions**

### Optional Settings

- **Require deployments to succeed before merging** (for production environments)
- **Lock branch** (for archived or frozen releases)
- **Restrict who can push to matching branches** (limit to specific teams/users)

## Protection Rules for Development Branches (develop/staging)

### Required Settings

#### Pull Request Requirements
- ✅ **Require pull request reviews before merging**
  - Required number of approvers: 1
  - Dismiss stale pull request approvals: ❌ (optional)

#### Status Checks
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date: ❌ (optional)
  - Status checks that must pass:
    - CI pipeline
    - Unit tests
    - Linting

#### Additional Restrictions
- ✅ **Require conversation resolution before merging**

## Implementation via GitHub API

To automate branch protection rules across repositories, use the GitHub API:

```bash
# Example: Set branch protection for 'main' branch
curl -X PUT \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["ci", "tests", "security-scan"]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews": true,
      "require_code_owner_reviews": true
    },
    "restrictions": null,
    "allow_force_pushes": false,
    "allow_deletions": false
  }'
```

## Monitoring and Compliance

- Regularly audit branch protection settings across all repositories
- Ensure critical repositories maintain strict protection rules
- Document any exceptions or special cases
- Review and update protection rules as the organization evolves

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub API Branch Protection](https://docs.github.com/en/rest/branches/branch-protection)
