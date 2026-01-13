# Organization-Wide Workflow Dispatch

## Overview

The **Organization-Wide Workflow Dispatch** workflow enables centralized
triggering of workflows across all repositories in your GitHub organization.
This is useful for:

- Running security scans across all repositories
- Triggering synchronized CI/CD operations
- Performing organization-wide health checks
- Batch updates and maintenance tasks
- Testing workflow changes across multiple repos

## Features

✅ **Flexible Repository Targeting**

- Target all repositories or specific ones
- Exclude specific repositories
- Filter by archived/private status
- Limit the number of repositories processed

✅ **Smart Discovery**

- Automatically discovers repositories in the organization
- Verifies workflow existence before dispatching
- Checks default branch for each repository

✅ **Safety Features**

- Dry-run mode to preview actions
- Rate limiting to avoid API throttling
- Comprehensive error handling
- Detailed logging and reporting

✅ **Customizable Workflow Inputs**

- Pass JSON inputs to target workflows
- Support for complex workflow parameters
- Branch selection per repository

## Workflow Configuration

### Required Inputs

| Input           | Description                                           | Required | Default |
| --------------- | ----------------------------------------------------- | -------- | ------- |
| `workflow_file` | Name of the workflow file to trigger (e.g., `ci.yml`) | Yes      | -       |

### Optional Inputs

| Input              | Description                                        | Required | Default |
| ------------------ | -------------------------------------------------- | -------- | ------- |
| `workflow_inputs`  | JSON object of inputs to pass to workflows         | No       | `{}`    |
| `target_repos`     | Comma-separated list of repos, or "all"            | No       | `all`   |
| `exclude_repos`    | Comma-separated list of repos to exclude           | No       | `''`    |
| `dry_run`          | Preview without triggering workflows               | No       | `false` |
| `include_archived` | Include archived repositories                      | No       | `false` |
| `include_private`  | Include private repositories                       | No       | `true`  |
| `max_repos`        | Maximum number of repos to process (0 = unlimited) | No       | `0`     |

## Usage Examples

### Example 1: Trigger CI Across All Active Repos

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="ci.yml" \
  -f dry_run=false
```

This will:

1. Discover all non-archived repositories
1. Check each for `.github/workflows/ci.yml`
1. Trigger the workflow on repositories that have it

### Example 2: Security Scan with Specific Inputs

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="security-scan.yml" \
  -f workflow_inputs='{"scan_type":"full","severity":"high"}' \
  -f dry_run=false
```

This passes custom inputs to the security scan workflow in each repository.

### Example 3: Target Specific Repositories

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="deploy.yml" \
  -f target_repos="repo1,repo2,repo3" \
  -f dry_run=false
```

This only triggers workflows in the specified repositories.

### Example 4: Exclude Specific Repositories

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="build.yml" \
  -f exclude_repos="legacy-repo,archived-project" \
  -f dry_run=false
```

This triggers workflows in all repos except the excluded ones.

### Example 5: Dry Run Preview

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="health-check.yml" \
  -f dry_run=true
```

This shows which repositories would be targeted without actually triggering
workflows.

### Example 6: Limited Batch Processing

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="update-dependencies.yml" \
  -f max_repos=10 \
  -f dry_run=false
```

This processes only the first 10 repositories that match the criteria.

## Target Workflow Requirements

For a workflow to be triggered by the organization-wide dispatcher, it must:

1. **Exist in the repository** at `.github/workflows/<workflow_file>`
1. **Have `workflow_dispatch` trigger** enabled:

```yaml
name: My Workflow

on:
  workflow_dispatch:
    inputs:
      # Optional: define inputs your workflow accepts
      example_input:
        description: "Example input parameter"
        required: false
        type: string
```

### Example Target Workflow Template

```yaml
name: Organization Health Check

on:
  workflow_dispatch:
    inputs:
      check_type:
        description: "Type of health check to run"
        required: false
        type: choice
        options:
          - "full"
          - "quick"
          - "security"
        default: "quick"
      notify:
        description: "Send notifications on completion"
        required: false
        type: boolean
        default: false

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run health check
        run: |
          echo "Running ${{ github.event.inputs.check_type }} health check"
          # Your health check logic here

      - name: Notify on completion
        if: github.event.inputs.notify == 'true'
        run: |
          echo "Health check completed"
          # Your notification logic here
```

## Architecture

### Workflow Jobs

The workflow consists of three main jobs:

```
┌─────────────────────────────────────────────────────────────┐
│  Job 1: discover-repositories                               │
│                                                               │
│  - Fetches all organization repositories                    │
│  - Applies filters (archived, private, excluded)            │
│  - Checks for workflow file existence                       │
│  - Outputs list of target repositories                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  Job 2: dispatch-workflows (if not dry-run)                 │
│                                                               │
│  - Iterates through target repositories                     │
│  - Dispatches workflow to each repository                   │
│  - Handles errors and rate limiting                         │
│  - Generates success/failure report                         │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  Job 3: dry-run-summary (if dry-run)                        │
│                                                               │
│  - Lists repositories that would be targeted                │
│  - Shows preview without taking action                      │
└─────────────────────────────────────────────────────────────┘
```

### API Interactions

The workflow interacts with GitHub API in the following ways:

1. **List Organization Repositories**

   ```
   GET /orgs/{org}/repos
   ```

1. **Check Workflow File Existence**

   ```
   GET /repos/{owner}/{repo}/contents/.github/workflows/{workflow_file}
   ```

1. **Dispatch Workflow**

   ```
   POST /repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches
   ```

## Permissions

The workflow requires the following permissions:

- `contents: read` - To read workflow file from the repository
- `actions: write` - To dispatch workflows in other repositories

**Note:** The `GITHUB_TOKEN` used must have permissions to dispatch workflows in
target repositories. For organization-wide operations, you may need to use a
GitHub App token or PAT with broader permissions.

## Rate Limiting and Performance

### GitHub API Rate Limits

- **Standard rate limit**: 5,000 requests per hour
- **Workflow dispatch**: Limited to prevent abuse

### Built-in Protections

1. **Delay between dispatches**: 0.5 seconds
1. **Request timeout**: 15 seconds per dispatch
1. **Maximum repositories**: Configurable via `max_repos` input
1. **Pagination**: Efficiently fetches all organization repos

### Performance Tips

- Use `max_repos` to process repositories in batches
- Use `dry_run` mode first to verify targeting
- Monitor API rate limits in organization settings
- Consider off-peak hours for large operations

## Monitoring and Troubleshooting

### Workflow Summary

Each run generates a detailed summary including:

- Total repositories discovered
- Successful dispatches
- Failed dispatches with error details
- Repository filtering criteria

### Artifacts

The workflow creates a JSON artifact with detailed results:

```json
{
  "total": 50,
  "successful": 48,
  "failed": 2,
  "failed_repos": [
    {
      "repo": "org/problematic-repo",
      "status": 404,
      "error": "Workflow file not found"
    }
  ]
}
```

### Common Issues

#### Issue: "Workflow file not found"

**Cause**: Target repository doesn't have the specified workflow file.

**Solution**:

- Verify the workflow file name
- Ensure the file exists at `.github/workflows/{workflow_file}`
- Use dry-run mode to preview which repos have the workflow

#### Issue: "Resource not accessible by integration"

**Cause**: `GITHUB_TOKEN` lacks permissions to dispatch workflows.

**Solution**:

- Ensure workflow has `actions: write` permission
- For cross-organization operations, use a PAT or GitHub App token
- Check repository access settings

#### Issue: "Rate limit exceeded"

**Cause**: Too many API requests in a short time.

**Solution**:

- Reduce `max_repos` to process smaller batches
- Increase delay between dispatches
- Wait for rate limit reset (shown in API response headers)

#### Issue: "Workflow not triggered despite success"

**Cause**: Target workflow may not have `workflow_dispatch` trigger.

**Solution**:

- Add `workflow_dispatch` trigger to target workflow
- Verify workflow syntax is correct
- Check workflow run history in target repository

## Security Considerations

### Token Permissions

- Use the principle of least privilege
- Limit token scope to necessary repositories
- Regularly audit token usage
- Consider using GitHub Apps for organization-wide operations

### Input Validation

- Workflow inputs are validated by target workflows
- JSON parsing errors are caught and logged
- Repository names are validated against organization membership

### Audit Trail

- All dispatches are logged in workflow runs
- Failed attempts are recorded with reasons
- Summary artifacts provide complete audit trail

## Best Practices

1. **Always test with dry-run first**

   ```bash
   gh workflow run org-wide-workflow-dispatch.yml \
     -f workflow_file="new-workflow.yml" \
     -f dry_run=true
   ```

1. **Start with small batches**

   ```bash
   gh workflow run org-wide-workflow-dispatch.yml \
     -f workflow_file="critical-update.yml" \
     -f max_repos=5 \
     -f dry_run=false
   ```

1. **Use specific targeting for critical operations**

   ```bash
   gh workflow run org-wide-workflow-dispatch.yml \
     -f workflow_file="prod-deploy.yml" \
     -f target_repos="prod-api,prod-frontend" \
     -f dry_run=false
   ```

1. **Exclude sensitive repositories**

   ```bash
   gh workflow run org-wide-workflow-dispatch.yml \
     -f workflow_file="experimental-feature.yml" \
     -f exclude_repos="production,critical-service" \
     -f dry_run=false
   ```

1. **Monitor results immediately**

   - Check workflow summary for failures
   - Download and review the results artifact
   - Investigate failed repositories promptly

## Integration with Other Workflows

### Scheduled Organization-Wide Scans

```yaml
name: Weekly Security Scan

on:
  schedule:
    - cron: "0 0 * * 0" # Every Sunday at midnight
  workflow_dispatch:

jobs:
  trigger-scans:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger security scans across organization
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.actions.createWorkflowDispatch({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'org-wide-workflow-dispatch.yml',
              ref: 'main',
              inputs: {
                workflow_file: 'security-scan.yml',
                dry_run: 'false'
              }
            });
```

### Conditional Batch Processing

```yaml
name: Conditional Batch Update

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Environment to update"
        required: true
        type: choice
        options:
          - "development"
          - "staging"
          - "production"

jobs:
  trigger-updates:
    runs-on: ubuntu-latest
    steps:
      - name: Set repository filters based on environment
        id: filters
        run: |
          case "${{ github.event.inputs.environment }}" in
            development)
              echo "repos=dev-app-1,dev-app-2" >> $GITHUB_OUTPUT
              ;;
            staging)
              echo "repos=staging-api,staging-web" >> $GITHUB_OUTPUT
              ;;
            production)
              echo "repos=prod-api,prod-web,prod-worker" >> $GITHUB_OUTPUT
              ;;
          esac

      - name: Trigger updates
        run: |
          gh workflow run org-wide-workflow-dispatch.yml \
            -f workflow_file="deploy.yml" \
            -f target_repos="${{ steps.filters.outputs.repos }}" \
            -f workflow_inputs='{"environment":"${{ github.event.inputs.environment }}"}' \
            -f dry_run=false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Future Enhancements

Potential improvements for this workflow:

1. **Parallel Dispatching**: Use matrix strategy to dispatch to multiple repos
   concurrently
1. **Status Monitoring**: Track and report on triggered workflow runs
1. **Retry Logic**: Automatically retry failed dispatches
1. **Conditional Targeting**: Support more complex filtering (e.g., by topic,
   language)
1. **Workflow Dependencies**: Support dispatching workflows in a specific order
1. **Result Aggregation**: Collect and summarize results from all triggered
   workflows

## Related Documentation

- [GitHub Actions Workflow Dispatch API](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
- [Organization Repository Management](../architecture/REPOSITORY_PURPOSE_ANALYSIS.md)
- [Workflow Security Best Practices](../../WORKFLOW_SECURITY_AUDIT.md)
- [Deployment Metadata Collection](DEPLOYMENT_METADATA_COLLECTION.md)

## Support

For issues or questions:

- Check the workflow summary for error details
- Review the dispatch results artifact
- Consult organization documentation
- Open an issue in the `.github` repository
