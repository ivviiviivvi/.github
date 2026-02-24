# Commitizen Setup Guide

This guide explains how to use Commitizen for standardized commit messages and
automated version management in the {{ORG_NAME}} organization.

## Overview

[Commitizen](https://commitizen-tools.github.io/commitizen/) is a tool that
helps create standardized commit messages following the
[Conventional Commits](https://www.conventionalcommits.org/)<!-- link:standards.conventional_commits -->
specification.

## Installation

### Local Development

```bash
# Install with pip
pip install commitizen

# Or with pipx (recommended for CLI tools)
pipx install commitizen
```

### Pre-commit Hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v4.0.0
    hooks:
      - id: commitizen
      - id: commitizen-branch
        stages: [push]
```

## Usage

### Creating Commits

Instead of `git commit`, use:

```bash
# Interactive commit with prompts
cz commit

# Or use the alias
git cz
```

This guides you through creating a properly formatted commit message.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

| Type       | Description                           |
| ---------- | ------------------------------------- |
| `feat`     | New feature                           |
| `fix`      | Bug fix                               |
| `docs`     | Documentation changes                 |
| `style`    | Code style changes (formatting, etc.) |
| `refactor` | Code refactoring (no feature/fix)     |
| `perf`     | Performance improvements              |
| `test`     | Test additions/changes                |
| `build`    | Build system changes                  |
| `ci`       | CI configuration changes              |
| `chore`    | Other changes (maintenance)           |
| `revert`   | Revert a previous commit              |

**Scopes** (optional, repository-specific):

- `workflows` - GitHub Actions changes
- `docs` - Documentation
- `automation` - Automation scripts
- `ci` - CI/CD configuration
- `deps` - Dependencies

### Examples

```bash
# Feature
feat(workflows): add auto-labeling for new PRs

# Bug fix
fix(ci): correct permissions for token access

# Breaking change
feat(api)!: change response format for user endpoints

BREAKING CHANGE: Response now returns array instead of object

# With issue reference
fix(auth): resolve token expiration issue

Closes #123
```

## Version Bumping

### Manual Bump

```bash
# Bump version based on commits
cz bump

# Dry run (see what would happen)
cz bump --dry-run

# Specific bump type
cz bump --increment PATCH
cz bump --increment MINOR
cz bump --increment MAJOR
```

### Automated via GitHub Actions

The repository includes a workflow that automatically:

1. Analyzes commits since last release
1. Determines version bump type
1. Updates version files
1. Creates release tag
1. Generates changelog

Trigger manually via: Actions > Commitizen Bump > Run workflow

## Changelog Generation

```bash
# Generate changelog
cz changelog

# Generate for specific version range
cz changelog --start-rev v1.0.0
```

## Configuration

The configuration is in `pyproject.toml`:

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "1.0.0"
tag_format = "v$version"
version_scheme = "semver"
version_files = [
    "pyproject.toml:version",
    "VERSION",
    "package.json:version",
]
update_changelog_on_bump = true
changelog_file = "CHANGELOG.md"
```

### Version Files

Commitizen updates version in these files:

- `pyproject.toml` - Python project version
- `VERSION` - Plain text version file
- `package.json` - Node.js package version

## GitHub Actions Integration

### Reusable Workflow

For other repositories, use the reusable workflow:

```yaml
name: Version Bump
on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: "Type of bump (auto, patch, minor, major)"
        required: false
        default: "auto"

jobs:
  bump:
    uses: {{ORG_NAME}}/.github/.github/workflows/reusable-commitizen-bump.yml@main
    with:
      bump_type: ${{ inputs.bump_type }}
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### CI Validation

Validate commit messages in CI:

```yaml
- name: Check commit messages
  run: |
    pip install commitizen
    cz check --rev-range origin/main..HEAD
```

## Troubleshooting

### "No commits found"

Ensure there are commits with conventional format since the last tag:

```bash
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

### "Invalid commit message"

Use `cz commit` instead of `git commit` for guided prompts.

### Version Not Updating

Check that `version_files` paths in `pyproject.toml` are correct.

## Related Resources

- [Conventional Commits Spec](https://www.conventionalcommits.org/)<!-- link:standards.conventional_commits -->
- [Commitizen Documentation](https://commitizen-tools.github.io/commitizen/)
- [PR Title Lint Workflow](../workflows/pr-title-lint.yml)
- [Semantic Versioning](https://semver.org/)<!-- link:standards.semver -->

______________________________________________________________________

_Based on configuration from log-commit-preserve repository._
