# Reusable Workflows

This repository provides reusable workflows that can be called from other
repositories in the organization using the `workflow_call` trigger.

## Available Reusable Workflows

### 1. Pull Request Labeler

**File:** `.github/workflows/reusable-labeler.yml`

Automatically labels pull requests based on file paths using
[actions/labeler](https://github.com/actions/labeler).

**Usage:**

```yaml
name: Label PRs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    uses: {{ORG_NAME}}/.github/.github/workflows/reusable-labeler.yml@main
    with:
      config-path: ".github/labeler.yml"
      sync-labels: true
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Inputs:**

| Input         | Required | Default               | Description                        |
| ------------- | -------- | --------------------- | ---------------------------------- |
| `config-path` | No       | `.github/labeler.yml` | Path to labeler config             |
| `sync-labels` | No       | `true`                | Remove labels that no longer match |

______________________________________________________________________

### 2. PR Title Lint

**File:** `.github/workflows/reusable-pr-title.yml`

Validates PR titles against conventional commit format using
[action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request).

**Usage:**

```yaml
name: PR Title
on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  lint:
    uses: {{ORG_NAME}}/.github/.github/workflows/reusable-pr-title.yml@main
    with:
      requireScope: false
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Inputs:**

| Input          | Required | Default        | Description               |
| -------------- | -------- | -------------- | ------------------------- |
| `types`        | No       | Standard types | Allowed commit types      |
| `scopes`       | No       | `""`           | Allowed scopes            |
| `requireScope` | No       | `false`        | Whether scope is required |

**Default Types:**

- `build`, `chore`, `ci`, `docs`, `feat`, `fix`
- `perf`, `refactor`, `revert`, `style`, `test`

______________________________________________________________________

### 3. Release

**File:** `.github/workflows/reusable-release.yml`

Creates releases using
[release-drafter](https://github.com/release-drafter/release-drafter) with
automatic changelog generation.

**Usage:**

```yaml
name: Release
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  release:
    uses: {{ORG_NAME}}/.github/.github/workflows/reusable-release.yml@main
    with:
      publish: true
      release-config-name: "release-drafter.yml"
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Inputs:**

| Input                 | Required | Default               | Description                      |
| --------------------- | -------- | --------------------- | -------------------------------- |
| `publish`             | No       | `true`                | Publish release or keep as draft |
| `release-config-name` | No       | `release-drafter.yml` | Config file name                 |

**Outputs:**

| Output      | Description                |
| ----------- | -------------------------- |
| `full-tag`  | Full tag (e.g., `v1.2.3`)  |
| `short-tag` | Major version (e.g., `v1`) |
| `body`      | Release body content       |

**Trigger Conditions:**

- Manual `workflow_dispatch`, OR
- Merged PR with labels: `breaking`, `feature`, `vuln`, or `release`

______________________________________________________________________

### 4. Major Version Updater

**File:** `.github/workflows/reusable-major-version-updater.yml`

Updates major version tags to point to the latest release. Useful for GitHub
Actions that need `v1`, `v2` tags.

**Usage:**

```yaml
name: Update Major Version
on:
  release:
    types: [published]

jobs:
  update-tag:
    uses: {{ORG_NAME}}/.github/.github/workflows/reusable-major-version-updater.yml@main
    with:
      tag-name: ${{ github.event.release.tag_name }}
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Inputs:**

| Input      | Required | Default | Description                    |
| ---------- | -------- | ------- | ------------------------------ |
| `tag-name` | Yes      | -       | Full tag name (e.g., `v1.2.3`) |

**Example:** When releasing `v1.2.3`, this workflow updates the `v1` tag to
point to `v1.2.3`.

______________________________________________________________________

## Other Reusable Workflows

The repository also includes these reusable workflows:

| Workflow                     | Description                |
| ---------------------------- | -------------------------- |
| `reusable-notify.yml`        | Notification utilities     |
| `reusable-api-retry.yml`     | API call retry logic       |
| `reusable-app-detect.yml`    | Application type detection |
| `reusable-security-scan.yml` | Security scanning          |

______________________________________________________________________

## Creating a Labeler Config

To use the reusable labeler, create a `.github/labeler.yml` in your repository:

```yaml
# Label PRs based on file paths
documentation:
  - changed-files:
      - any-glob-to-any-file:
          - "**/*.md"
          - "docs/**"

workflows:
  - changed-files:
      - any-glob-to-any-file:
          - ".github/workflows/**"

dependencies:
  - changed-files:
      - any-glob-to-any-file:
          - "package.json"
          - "package-lock.json"
          - "requirements.txt"
          - "pyproject.toml"
```

______________________________________________________________________

## Creating a Release Drafter Config

To use the reusable release workflow, create a `.github/release-drafter.yml`:

```yaml
name-template: "v$RESOLVED_VERSION"
tag-template: "v$RESOLVED_VERSION"
categories:
  - title: "Features"
    labels:
      - "feature"
      - "enhancement"
  - title: "Bug Fixes"
    labels:
      - "bug"
      - "fix"
  - title: "Maintenance"
    labels:
      - "chore"
      - "dependencies"
change-template: "- $TITLE @$AUTHOR (#$NUMBER)"
version-resolver:
  major:
    labels:
      - "breaking"
  minor:
    labels:
      - "feature"
  patch:
    labels:
      - "bug"
      - "fix"
  default: patch
template: |
  ## Changes
  $CHANGES

  ## Contributors
  $CONTRIBUTORS
```

______________________________________________________________________

## Best Practices

1. **Pin to a specific ref**: Use `@main` or a specific commit SHA
1. **Pass required secrets**: Always pass `github-token`
1. **Check permissions**: Ensure the calling workflow has required permissions
1. **Version your configs**: Keep labeler and release-drafter configs in sync

## Source

These workflows are based on patterns from
[github/ospo-reusable-workflows](https://github.com/github/ospo-reusable-workflows).
