# Labeling Configuration Guide

This repository uses multiple labeling configurations for different purposes.

## Overview

| Config File | Purpose | Trigger |
|-------------|---------|---------|
| `labeler.yml` | Path-based PR labels | PR file changes |
| `auto-labeler.yml` | Author-based PR labels | PR creation |
| `issue-labeler.yml` | ML-based issue classification | Issue creation |
| `keyword-labeler.yml` | Keyword-based issue labels | Issue title/body |

## Configuration Details

### 1. labeler.yml (Path-Based PR Labeling)

**Used by**: [actions/labeler](https://github.com/actions/labeler)

Labels PRs based on which files are changed:

```yaml
documentation:
  - changed-files:
    - any-glob-to-any-file:
      - '**/*.md'
      - docs/**/*

github-actions:
  - changed-files:
    - any-glob-to-any-file:
      - .github/workflows/**
```

**Labels Applied**:
- `documentation` - Markdown and docs changes
- `github-actions` - Workflow changes
- `configuration` - Config file changes (yml, json, toml)
- `dependencies` - Package manager files
- `javascript`, `typescript`, `python`, etc. - Language-specific
- `docker`, `tests`, `security` - Category-specific
- `frontend`, `backend`, `database` - Architecture-specific

### 2. auto-labeler.yml (Author-Based PR Labeling)

**Used by**: Custom workflow or action

Labels PRs based on the author:

```yaml
addLabels:
  - "needs-review"

authorLabels:
  dependabot[bot]:
    - "dependencies"
  renovate[bot]:
    - "dependencies"
```

**Behavior**:
- All new PRs get `needs-review` label
- Bot-authored PRs get `dependencies` label automatically

### 3. issue-labeler.yml (ML-Based Issue Classification)

**Used by**: [issue-label-bot](https://github.com/machine-learning-apps/issue-label-bot)

Uses machine learning to classify issues:

```yaml
threshold: 0.7  # Minimum confidence for label application
```

**Behavior**:
- Analyzes issue content using ML model
- Applies labels when confidence exceeds threshold
- Works best with trained models on your repository data

### 4. keyword-labeler.yml (Keyword-Based Issue Labeling)

**Used by**: Custom workflow or keyword-labeler action

Labels issues based on title/body keywords:

```yaml
keywords:
  bug: ["bug", "error", "fail", "crash"]
  enhancement: ["feature", "request", "add", "improve"]
  documentation: ["docs", "readme", "guide"]
  security: ["security", "vulnerability", "cve", "leak"]
```

**Behavior**:
- Scans issue title and body for keywords
- Applies corresponding label when keyword found
- Multiple labels can match

## Workflow Integration

The labeling configurations are triggered by:

1. **`auto-labeler.yml` workflow** - Runs on PR open/edit
2. **`issue-labeler` workflow** - Runs on issue creation
3. **External bots** - Dependabot, Renovate add their own labels

## Maintenance

### Adding New Labels

1. Define the label in `labels.yml` (label definitions)
2. Add matching rules to the appropriate labeler config
3. Test with a sample PR or issue

### Updating Path Patterns

Edit `labeler.yml` to add new path patterns:

```yaml
new-category:
  - changed-files:
    - any-glob-to-any-file:
      - 'path/to/files/**'
```

### Adding Keywords

Edit `keyword-labeler.yml`:

```yaml
keywords:
  new-label: ["keyword1", "keyword2"]
```

---

_Last Updated: 2026-01-30_
