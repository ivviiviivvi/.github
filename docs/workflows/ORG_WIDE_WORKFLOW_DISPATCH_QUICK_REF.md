# Organization-Wide Workflow Dispatch - Quick Reference

## Basic Usage

### Dry Run (Preview)

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="ci.yml" \
  -f dry_run=true
```

### Trigger All Active Repos

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="ci.yml" \
  -f dry_run=false
```

### Target Specific Repos

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="security-scan.yml" \
  -f target_repos="repo1,repo2,repo3" \
  -f dry_run=false
```

### Exclude Specific Repos

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="build.yml" \
  -f exclude_repos="legacy-repo,deprecated-app" \
  -f dry_run=false
```

### With Custom Inputs

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="deploy.yml" \
  -f workflow_inputs='{"environment":"staging","version":"v2.0.0"}' \
  -f dry_run=false
```

### Limit Number of Repos

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="update-deps.yml" \
  -f max_repos=10 \
  -f dry_run=false
```

## Common Scenarios

### Weekly Security Scan

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="security-scan.yml" \
  -f workflow_inputs='{"scan_type":"full","severity":"high"}' \
  -f exclude_repos="archived-projects" \
  -f dry_run=false
```

### Health Check All Repos

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="org-health-check.yml" \
  -f workflow_inputs='{"check_type":"full","notify_on_completion":"true"}' \
  -f dry_run=false
```

### Update Dependencies in Batches

```bash
# Batch 1
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="update-dependencies.yml" \
  -f max_repos=5 \
  -f dry_run=false

# Wait for completion, then batch 2
# Repeat as needed
```

### Production Deployment

```bash
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="deploy.yml" \
  -f target_repos="prod-api,prod-web,prod-worker" \
  -f workflow_inputs='{"environment":"production"}' \
  -f dry_run=false
```

## Required Workflow Setup

Target repositories must have a workflow with `workflow_dispatch` trigger:

```yaml
name: My Workflow

on:
  workflow_dispatch:
    inputs:
      # Define your inputs here
      example_input:
        description: "Example input"
        required: false
        type: string

jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - name: Use input
        run: echo "${{ github.event.inputs.example_input }}"
```

## Monitoring Results

### Check Workflow Summary

- Navigate to Actions → Organization-Wide Workflow Dispatch
- View the latest run
- Check the summary for success/failure counts

### Download Results Artifact

```bash
gh run download <run-id> -n dispatch-results-<run-number>
```

### View Results JSON

```bash
cat dispatch_results.json | jq '.'
```

## Troubleshooting

### "Workflow file not found" errors

- Verify the workflow file exists in target repos
- Check the file name matches exactly
- Use dry-run to preview which repos have the workflow

### "Resource not accessible" errors

- Ensure workflow has `actions: write` permission
- Check repository access settings
- May need PAT for cross-organization operations

### "Rate limit exceeded"

- Reduce `max_repos` to process smaller batches
- Wait for rate limit reset
- Use off-peak hours for large operations

## Best Practices

1. **Always test with dry-run first**
1. **Start with small batches** (`max_repos=5`)
1. **Exclude production repos during testing**
1. **Monitor results immediately after dispatch**
1. **Document custom workflow inputs**
1. **Use specific targeting for critical operations**

## Input Reference

| Input              | Type    | Default  | Description                        |
| ------------------ | ------- | -------- | ---------------------------------- |
| `workflow_file`    | string  | required | Workflow filename (e.g., `ci.yml`) |
| `workflow_inputs`  | string  | `{}`     | JSON object of inputs              |
| `target_repos`     | string  | `all`    | Comma-separated repo list or "all" |
| `exclude_repos`    | string  | `''`     | Comma-separated repos to exclude   |
| `dry_run`          | boolean | `false`  | Preview without triggering         |
| `include_archived` | boolean | `false`  | Include archived repos             |
| `include_private`  | boolean | `true`   | Include private repos              |
| `max_repos`        | number  | `0`      | Max repos to process (0=unlimited) |

## More Information

📖 [Complete Documentation](ORG_WIDE_WORKFLOW_DISPATCH.md) 🔧
[Workflow Template](../../.github/workflow-templates/org-health-check.yml) 🎯
[Main Workflow](../../.github/workflows/org-wide-workflow-dispatch.yml)
