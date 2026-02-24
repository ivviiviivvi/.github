# Version Management

This document describes the centralized version management system for Python,
Node.js, and GitHub Action dependencies across workflows.

## Overview

The repository uses a three-tier version management approach:

1. **Repository Variables** - Centralized defaults via GitHub Settings
1. **Composite Actions** - Standardized setup with fallback logic
1. **Auto-Update Workflows** - Automated version detection and PR creation

## Repository Variables

Configure these in **Settings > Secrets and variables > Actions > Variables**:

| Variable                 | Description                          | Current Value              |
| ------------------------ | ------------------------------------ | -------------------------- |
| `PYTHON_VERSION_DEFAULT` | Default Python version for workflows | `3.12`                     |
| `PYTHON_VERSION_MATRIX`  | JSON array for matrix testing        | `["3.10", "3.11", "3.12"]` |
| `NODE_VERSION_DEFAULT`   | Default Node.js version              | `20`                       |
| `NODE_VERSION_MATRIX`    | JSON array for matrix testing        | `["18", "20", "22"]`       |

## Composite Actions

### Python Setup

Use `.github/actions/setup-python-standard` for consistent Python setup:

```yaml
- uses: ./.github/actions/setup-python-standard
  with:
    python-version: ''  # Uses vars.PYTHON_VERSION_DEFAULT, then falls back to 3.12
    cache: 'true'
```

**Version Resolution Order:**

1. Explicit `python-version` input
1. `vars.PYTHON_VERSION_DEFAULT` repository variable
1. Hardcoded default (`3.12`)

### Node.js Setup

Use `.github/actions/setup-node-standard` for consistent Node.js setup:

```yaml
- uses: ./.github/actions/setup-node-standard
  with:
    node-version: ''  # Uses vars.NODE_VERSION_DEFAULT, then falls back to 20
    cache: 'npm'
```

**Version Resolution Order:**

1. Explicit `node-version` input
1. `vars.NODE_VERSION_DEFAULT` repository variable
1. Hardcoded default (`20`)

## Reusable Workflows

The reusable workflows in `.github/workflows/reusable/` also support the
fallback pattern:

```yaml
# Calling a reusable workflow - version will auto-resolve
jobs:
  test:
    uses: ./.github/workflows/reusable/python-setup-test.yml
    with:
      python-version: ''  # Empty = use repository default
```

## Auto-Update Workflows

### Action Pins (`update-action-pins-scheduled.yml`)

- **Schedule:** Weekly (Tuesday 4 AM UTC)
- **Purpose:** Updates SHA-pinned GitHub Actions to latest versions
- **Output:** Creates PR with updated pins and preserved ratchet comments

Manual trigger:

```bash
gh workflow run update-action-pins-scheduled.yml --field dry_run=false
```

### Python Version (`update-python-version.yml`)

- **Schedule:** Monthly (15th at 5 AM UTC)
- **Purpose:** Detects latest stable Python and creates update PR
- **Validation:** Tests dependency installation before proposing update

Manual trigger:

```bash
gh workflow run update-python-version.yml --field dry_run=false
```

### Node.js Version (`update-nodejs-version.yml`)

- **Schedule:** Monthly (20th at 5 AM UTC)
- **Purpose:** Detects current LTS Node.js and creates update PR
- **Validation:** Tests npm install before proposing update

Manual trigger:

```bash
gh workflow run update-nodejs-version.yml --field dry_run=false
```

### Orchestrator (`version-update-orchestrator.yml`)

Provides a dashboard and management interface:

```bash
# View status of all version updates
gh workflow run version-update-orchestrator.yml --field action=status

# Trigger all updates at once
gh workflow run version-update-orchestrator.yml --field action=trigger-all

# Clean up stale PRs (older than 30 days)
gh workflow run version-update-orchestrator.yml --field action=cleanup-stale
```

## FUNCTIONcalled Workflow Metadata

### Overview

Workflows can have metadata sidecars following the FUNCTIONcalled naming
convention. This provides structured classification and enables registry
generation.

### Layers

| Layer         | Purpose                        | Examples                              |
| ------------- | ------------------------------ | ------------------------------------- |
| `core`        | Foundation, infrastructure, CI | `ci.yml`, `reusable-*.yml`            |
| `interface`   | User-facing, interaction       | `welcome.yml`, `auto-assign.yml`      |
| `logic`       | Validation, processing         | `pr-title-lint.yml`, `validate-*.yml` |
| `application` | Deployment, release            | `release.yml`, `deployment.yml`       |

### Creating Metadata Sidecars

Create a `.meta.json` file alongside your workflow:

**Minimal (light profile):**

```json
{
  "profile": "light",
  "name": "My Workflow",
  "identifier": "urn:uuid:<generate-a-uuid>",
  "version": "1.0.0"
}
```

**Complete (full profile):**

```json
{
  "profile": "full",
  "name": "My Workflow",
  "identifier": "urn:uuid:<generate-a-uuid>",
  "version": "1.0.0",
  "description": "What this workflow does",
  "functioncalled": {
    "canonical": "layer.role.domain.yml",
    "layer": "core|interface|logic|application",
    "role": "the-role",
    "domain": "the-domain"
  },
  "schema:type": "SoftwareSourceCode",
  "encodingFormat": "application/x-yaml",
  "triggers": ["push", "pull_request"],
  "dateCreated": "2025-01-01T00:00:00Z",
  "dateModified": "2025-01-24T00:00:00Z"
}
```

### Validation

Metadata is validated on PR via `validate-functioncalled.yml`:

```bash
# Validate manually
python .github/tools/functioncalled/validate_workflow_meta.py \
  --scan-dir .github/workflows/

# Build registry
python .github/tools/functioncalled/workflow-registry-builder.py \
  --root .github/workflows \
  --out registry/workflow-registry.json
```

### Registry

The workflow registry at `registry/workflow-registry.json` catalogs all
workflows with:

- File paths and SHA256 hashes
- FUNCTIONcalled classifications
- Version information
- Statistics by layer

## Migration Guide

### Updating Existing Workflows

To migrate a workflow to use centralized versions:

1. **Change hardcoded version to empty string:**

   ```yaml
   # Before
   python-version: '3.11'

   # After
   python-version: ''  # Uses vars.PYTHON_VERSION_DEFAULT
   ```

1. **Or use the composite action:**

   ```yaml
   # Replace direct setup-python call
   - uses: ./.github/actions/setup-python-standard
   ```

1. **Add version determination step (for complex cases):**

   ```yaml
   - name: Determine Python version
     id: version
     run: |
       VERSION="${{ inputs.python-version || vars.PYTHON_VERSION_DEFAULT || '3.12' }}"
       echo "version=$VERSION" >> $GITHUB_OUTPUT
   ```

### Adding Metadata to Existing Workflow

1. Create `<workflow-name>.yml.meta.json` alongside the workflow
1. Use the light profile for quick adoption
1. Optionally upgrade to full profile with FUNCTIONcalled classification

## Troubleshooting

### Version Not Resolving

Check the order of resolution:

1. Is the input explicitly set? (highest priority)
1. Is the repository variable defined in Settings?
1. Is the hardcoded default appropriate?

### Auto-Update PR Not Created

1. Check if an existing PR is already open on the auto branch
1. Verify the workflow has write permissions
1. Check workflow logs for validation failures

### Metadata Validation Failing

1. Validate JSON syntax: `python -m json.tool file.meta.json`
1. Check required fields for your profile level
1. Verify UUID format: `urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
