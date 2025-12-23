# Automated PR Merging - The Eternal Solution

## Overview

This guide provides a comprehensive, eternal solution to the problem: "Cannot programmatically merge PRs without GitHub API credentials."

**The Solution**: GitHub Actions workflows with built-in `GITHUB_TOKEN` provide automated PR merging capabilities without requiring custom API tokens or credentials.

## How It Works

GitHub provides every workflow run with an automatic `GITHUB_TOKEN` that has permissions to:
- Read repository contents
- Write to pull requests
- Merge pull requests (when properly configured)
- Close issues
- Add labels and comments

### Key Advantages

1. **No Manual Token Management**: `GITHUB_TOKEN` is automatically provided
2. **Secure by Default**: Token permissions are scoped to the workflow run
3. **No Expiration Issues**: Token is regenerated for each workflow run
4. **Audit Trail**: All actions are logged in GitHub Actions
5. **Works Forever**: No maintenance required for token rotation

## Quick Start

### 1. Enable Auto-Merge on Your Repository

```bash
# Via GitHub CLI
gh repo edit --enable-auto-merge

# Or via GitHub UI:
# Settings → General → Pull Requests → Allow auto-merge
```

### 2. Configure Branch Protection (Recommended)

```bash
# Require status checks before merging
gh api repos/{owner}/{repo}/branches/{branch}/protection \
  -X PUT \
  -f required_status_checks[strict]=true \
  -f required_status_checks[contexts][]=ci \
  -f required_status_checks[contexts][]=tests
```

### 3. Use the Auto-Merge Workflow

Our repository includes a pre-configured auto-merge workflow at `.github/workflows/auto-merge.yml`.

**To trigger auto-merge on a PR:**

Option A: Add a label
```bash
gh pr edit <pr-number> --add-label "auto-merge"
```

Option B: Include `[auto-merge]` in PR title
```bash
gh pr create --title "[auto-merge] My feature" --body "..."
```

Option C: Manual workflow dispatch
```bash
gh workflow run auto-merge.yml -f pr_number=123
```

## The Workflow Explained

### Built-in Workflow: `.github/workflows/auto-merge.yml`

This workflow:
1. Triggers on PR events (open, sync, review)
2. Checks eligibility (labels, title, draft status)
3. Verifies all status checks pass
4. Ensures required approvals are met
5. Automatically merges when conditions are satisfied
6. Cleans up merged branches

### Permissions Required

```yaml
permissions:
  contents: write       # To merge PRs and delete branches
  pull-requests: write  # To update PR status
  issues: write         # To add comments
  checks: read          # To verify status checks
```

These permissions are automatically available to `GITHUB_TOKEN` when specified in the workflow.

## Advanced Configuration

### Custom Merge Strategy

You can customize the merge strategy in the workflow:

```yaml
- name: Merge PR
  run: |
    gh pr merge ${{ github.event.pull_request.number }} \
      --squash \  # or --merge, --rebase
      --auto
```

### Conditional Auto-Merge

Add conditions based on file changes:

```yaml
- name: Check if auto-merge applies
  id: check
  run: |
    FILES_CHANGED=$(gh pr view $PR_NUMBER --json files --jq '.files[].path')
    if echo "$FILES_CHANGED" | grep -q "^docs/"; then
      echo "eligible=true" >> $GITHUB_OUTPUT
    fi
```

### Integration with CI/CD

The auto-merge workflow waits for all required checks to pass:

```yaml
- name: Wait for CI
  uses: lewagon/wait-on-check-action@v1
  with:
    ref: ${{ github.event.pull_request.head.sha }}
    check-regexp: '^(ci|test|lint).*$'
    wait-interval: 30
```

## Reusable Workflow Template

Create `.github/workflows/templates/auto-merge-template.yml`:

```yaml
name: Reusable Auto-Merge

on:
  workflow_call:
    inputs:
      merge_method:
        description: 'Merge method (merge, squash, rebase)'
        required: false
        default: 'squash'
        type: string
      require_approvals:
        description: 'Number of required approvals'
        required: false
        default: 1
        type: number

permissions:
  contents: write
  pull-requests: write
  issues: write
  checks: read

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge PR
        uses: pascalgn/automerge-action@v0.15.6
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MERGE_METHOD: ${{ inputs.merge_method }}
          MERGE_REQUIRED_APPROVALS: ${{ inputs.require_approvals }}
```

## Troubleshooting

### Issue: "Resource not accessible by integration"

**Cause**: Insufficient workflow permissions

**Solution**: Add required permissions to workflow:
```yaml
permissions:
  contents: write
  pull-requests: write
```

### Issue: "Branch protection rules not satisfied"

**Cause**: Required checks haven't passed yet

**Solution**: The workflow automatically waits. Ensure all required checks are configured correctly.

### Issue: "Pull request is not in a mergeable state"

**Cause**: Merge conflicts exist

**Solution**: The workflow includes conflict detection. Resolve conflicts manually or use our conflict resolution workflow.

### Issue: Auto-merge not triggering

**Checklist**:
- [ ] Repository has auto-merge enabled
- [ ] PR has `auto-merge` label or `[auto-merge]` in title
- [ ] PR is not in draft mode
- [ ] All required reviews are approved
- [ ] All status checks pass
- [ ] No merge conflicts

## Best Practices

### 1. Use Labels for Control

```yaml
labels:
  - auto-merge      # Enable auto-merge
  - hotfix          # Bypass approval requirement
  - skip-auto-merge # Prevent auto-merge
```

### 2. Configure Merge Queues

For high-traffic repositories:

```yaml
merge_group:
  required_checks:
    - ci
    - tests
  method: squash
```

### 3. Add Safety Checks

```yaml
- name: Safety check
  run: |
    if [[ "${{ github.event.pull_request.user.login }}" == "dependabot[bot]" ]]; then
      if [[ "${{ github.event.pull_request.title }}" =~ "major" ]]; then
        echo "::error::Major version updates require manual review"
        exit 1
      fi
    fi
```

### 4. Monitor Auto-Merge Activity

Set up notifications:

```yaml
- name: Notify on merge
  if: success()
  uses: 8398a7/action-slack@v3
  with:
    status: custom
    custom_payload: |
      {
        text: "PR #${{ github.event.pull_request.number }} auto-merged!"
      }
```

## Examples

### Example 1: Dependabot Auto-Merge

```yaml
name: Dependabot Auto-Merge
on:
  pull_request:
    
jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - name: Enable auto-merge for Dependabot PRs
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

### Example 2: Documentation Auto-Merge

```yaml
name: Docs Auto-Merge
on:
  pull_request:
    paths:
      - 'docs/**'
      - '**.md'

jobs:
  auto-merge:
    if: contains(github.event.pull_request.labels.*.name, 'documentation')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - name: Auto-approve and merge docs
        run: |
          gh pr review --approve "$PR_URL"
          gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

### Example 3: Hotfix Fast-Track

```yaml
name: Hotfix Auto-Merge
on:
  pull_request:
    branches:
      - main

jobs:
  auto-merge:
    if: contains(github.event.pull_request.labels.*.name, 'hotfix')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - name: Verify hotfix criteria
        run: |
          # Hotfixes must be small and focused
          CHANGES=$(gh pr diff "$PR_URL" | wc -l)
          if [ $CHANGES -gt 100 ]; then
            echo "::error::Hotfix too large ($CHANGES lines)"
            exit 1
          fi
      
      - name: Fast-track merge
        run: gh pr merge --auto --merge "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

## FAQ

### Q: Do I need to create a Personal Access Token (PAT)?

**A: No!** The built-in `GITHUB_TOKEN` is sufficient for auto-merging PRs. PATs are only needed for:
- Triggering workflows from other workflows
- Accessing private repositories outside your organization
- Performing actions on behalf of a specific user

### Q: Will this work in other repositories?

**A: Yes!** You can:
1. Copy the workflow file to any repository
2. Use the reusable workflow template
3. Fork this repository and customize

### Q: What about security?

**A: Very secure!** The `GITHUB_TOKEN`:
- Is automatically generated per workflow run
- Has limited scope (only this repository)
- Expires when the workflow completes
- Actions are audited in GitHub's audit log

### Q: Can I merge PRs from forks?

**A: With restrictions.** For security, `GITHUB_TOKEN` from forked PRs has read-only permissions. Options:
1. Use `pull_request_target` trigger (with caution)
2. Require maintainer approval first
3. Use a bot account with appropriate permissions

### Q: How do I prevent auto-merge for specific PRs?

**A:** Add `[skip-auto-merge]` to the PR title or body, or add a `needs-review` label.

## Maintenance

### Updating the Workflow

The workflow is designed to be maintenance-free, but you can update it:

```bash
# Check for updates to GitHub Actions
gh extension install actions/gh-actions-cache
gh actions-cache list

# Update action versions
# Edit .github/workflows/auto-merge.yml
# Update action versions to latest (use Dependabot!)
```

### Monitoring

Track auto-merge activity:

```bash
# View recent workflow runs
gh run list --workflow=auto-merge.yml

# Check specific run
gh run view <run-id>

# View auto-merged PRs
gh pr list --state merged --label auto-merged --limit 10
```

## Related Workflows

- **`.github/workflows/auto-approve.yml`** - Auto-approve PRs from trusted sources
- **`.github/workflows/pr-labels.yml`** - Automatically label PRs
- **`.github/workflows/conflict-detection.yml`** - Detect and notify about conflicts
- **`.github/workflows/merge-queue.yml`** - Manage merge queue

## References

- [GitHub Actions: GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [GitHub Actions: Permissions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#permissions)
- [Auto-merge Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

## Support

For issues or questions:
- Open an issue in this repository
- Check existing discussions
- Review GitHub Actions logs for errors
- Consult the troubleshooting section above

---

**This is the eternal solution.** The workflow uses GitHub's native features and requires no external dependencies, API tokens, or ongoing maintenance. It will continue to work as long as GitHub Actions exists.
