# Deployment Metadata Collection Workflow

## Overview

The deployment metadata collection system enables the `.github` repository to
serve as a centralized gallery for all live app deployments across the
organization. This document describes the architecture and workflow for
collecting and aggregating deployment metadata.

## Architecture

### Workflow Components

1. **`deploy-to-pages-live.yml`** (In each source repository)

   - Detects app type and deployment strategy
   - Deploys the application (Pages Direct, Docker, Codespaces, or
     Documentation)
   - Creates a deployment metadata artifact
   - Triggers the collect-deployment-metadata workflow

1. **`collect-deployment-metadata.yml`** (In `.github` repository)

   - **Reusable workflow** with `workflow_call` trigger
   - Downloads deployment metadata artifacts
   - Validates metadata structure and required fields
   - Triggers gallery index update via repository dispatch

1. **`generate-pages-index.yml`** (In `.github` repository)

   - Queries GitHub API for all organization repositories
   - Discovers deployment configurations in each repo
   - Aggregates deployment metadata into `docs/_data/app-deployments.yml`
   - Generates statistics and updates the gallery

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Source Repository (e.g., org/my-app)                       │
│                                                               │
│  1. deploy-to-pages-live.yml runs                           │
│     └─> Creates deployment-metadata.json artifact           │
│     └─> Triggers workflow_run event                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  .github Repository - collect-deployment-metadata.yml       │
│                                                               │
│  2. Triggered by workflow_run event                          │
│     └─> Downloads artifact from source repo                  │
│     └─> Validates metadata structure                         │
│     └─> Sends repository_dispatch to .github repo           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  .github Repository - generate-pages-index.yml              │
│                                                               │
│  3. Triggered by repository_dispatch or schedule            │
│     └─> Queries all org repos via GitHub API                │
│     └─> Checks for .github/app-deployment-config.yml        │
│     └─> Queries recent deployment workflow runs             │
│     └─> Aggregates into docs/_data/app-deployments.yml      │
│     └─> Commits and pushes changes                          │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Reusable Workflow

The `collect-deployment-metadata.yml` workflow exposes a `workflow_call`
trigger, allowing it to be invoked from any repository in the organization:

```yaml
on:
  workflow_run:
    workflows:
      - "Deploy Live App to GitHub Pages"
    types:
      - completed
  workflow_dispatch:
    inputs:
      run_id:
        description: "Workflow run ID to ingest"
        required: false
        type: string
  workflow_call: # Enables cross-repo invocation
    inputs:
      run_id:
        required: false
        type: string
      repository:
        required: false
        type: string
```

### 2. Centralized Aggregation

Unlike the previous approach where each source repo tried to write to
`app-deployments.yml` (which wouldn't work for cross-repo scenarios), the new
architecture:

- **Source repos**: Only create artifacts and trigger events
- **`.github` repo**: Serves as the single source of truth
- **Gallery**: Queries the central `app-deployments.yml` file

This ensures:

- No merge conflicts from multiple repos trying to write the same file
- Single source of truth for deployment data
- Proper separation of concerns

### 3. Comprehensive Error Handling

The workflow includes robust error handling:

```yaml
- name: "Download deployment metadata artifact"
  id: download-artifact
  continue-on-error: true # Don't fail the workflow on missing artifacts
  uses: actions/download-artifact@v4

- name: "Check artifact download"
  if: steps.download-artifact.outcome == 'failure'
  run: |
    echo "::warning::Failed to download artifact"
    echo "This may be because:"
    echo "  - The artifact has expired (7 day retention)"
    echo "  - The workflow run did not produce an artifact"
    exit 0  # Continue gracefully
```

### 4. Validation

Metadata is validated before being processed:

```python
# Required fields
required_fields = ["repository", "deployment_strategy", "app_type", "status"]
missing_fields = [field for field in required_fields if field not in metadata]

if missing_fields:
    print(f"::error::Missing required fields: {', '.join(missing_fields)}")
    sys.exit(1)
```

## Deployment Metadata Schema

Each deployment artifact contains a JSON file with the following structure:

```json
{
  "repository": "org/repo-name",
  "source_url": "https://github.com/org/repo-name",
  "app_type": "frontend|backend|fullstack|static|cli-library",
  "deployment_strategy": "pages-direct|docker|codespaces|documentation-only",
  "live_url": "https://org.github.io/repo-name",
  "status": "deployed|documentation",
  "last_updated": "2025-12-23T00:00:00Z",
  "docker_image": "org/repo-name:latest", // Optional, for Docker deployments
  "codespaces_url": "...", // Optional, for Codespaces
  "documentation_url": "..." // Optional, for documentation-only
}
```

## Triggering the Workflow

### Automatic Trigger (Recommended)

The workflow is automatically triggered when a deployment completes:

1. A repository runs `deploy-to-pages-live.yml`
1. The workflow creates a deployment metadata artifact
1. A `workflow_run` event triggers `collect-deployment-metadata.yml`
1. Metadata is validated and gallery is updated

### Manual Trigger

You can manually trigger the workflow via workflow dispatch:

```bash
gh workflow run collect-deployment-metadata.yml \
  -f run_id=<workflow-run-id>
```

### Cross-Repository Usage

To call this workflow from another repository:

```yaml
jobs:
  collect-metadata:
    uses: org/.github/.github/workflows/collect-deployment-metadata.yml@main
    with:
      run_id: ${{ github.run_id }}
      repository: ${{ github.repository }}
```

## Monitoring and Alerts

The `collect-deployment-metadata` workflow is monitored by
`alert-on-workflow-failure.yml`. Failed runs will:

- Be logged in workflow summaries
- Trigger failure alerts (if configured)
- Include detailed error messages about what went wrong

## Troubleshooting

### Artifact Not Found

**Symptom**: Warning message "Failed to download artifact from run X"

**Causes**:

1. The artifact has expired (7-day retention period)
1. The deployment workflow didn't produce an artifact
1. The artifact name doesn't match "app-deployment"

**Resolution**:

- Check the source workflow run to verify the artifact was created
- Manually trigger the workflow with a valid run_id
- Re-run the deployment workflow if needed

### Metadata Validation Failed

**Symptom**: Error message "Missing required fields: ..."

**Causes**:

1. Deployment workflow didn't generate complete metadata
1. JSON structure is malformed

**Resolution**:

- Review the deployment workflow's metadata generation step
- Ensure all required fields are present
- Check JSON syntax

### Gallery Not Updating

**Symptom**: Deployments don't appear in the gallery

**Causes**:

1. Repository dispatch failed
1. `generate-pages-index.yml` hasn't run yet
1. Repository doesn't have `app-deployment-config.yml`

**Resolution**:

- Check if the repository dispatch succeeded
- Manually trigger `generate-pages-index.yml`
- Add `.github/app-deployment-config.yml` to the source repository

## Best Practices

1. **Always create deployment artifacts**: Ensure your deployment workflow
   creates the `app-deployment` artifact with complete metadata

1. **Use standard metadata format**: Follow the schema documented above

1. **Enable deployment in config**: Add `.github/app-deployment-config.yml` to
   your repository:

   ```yaml
   deployment:
     enabled: true
     strategy: auto # or pages-direct, docker, codespaces
   ```

1. **Monitor workflow runs**: Check the workflow summary for warnings and errors

1. **Keep artifacts**: Don't delete deployment artifacts immediately; they're
   needed for metadata collection

## Future Improvements

Potential enhancements for this system:

1. **Direct artifact download in generate-pages-index**: Query artifacts
   directly from the API instead of relying on file-based triggers
1. **Deployment health metrics**: Track deployment success rates and uptime
1. **Historical deployment data**: Maintain a history of deployments for trend
   analysis
1. **Automated rollback**: Detect failed deployments and trigger rollbacks
1. **Multi-environment support**: Track staging, production, and preview
   deployments separately

## Related Documentation

- [Deployment Summary](../DEPLOYMENT_SUMMARY.md)
- [Complete Deployment README](../COMPLETE_DEPLOYMENT_README.md)
- [Architecture Guide](../architecture/AUTONOMOUS_ECOSYSTEM_ARCHITECTURE.md)
