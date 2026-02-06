# Customization Guide

How to customize the {{ORG_NAME}} GitHub template for your organization.

______________________________________________________________________

## Branding Changes

### Organization Identity

Update these files with your organization's branding:

| File            | Purpose              | Changes Required           |
| --------------- | -------------------- | -------------------------- |
| `README.md`     | Repository overview  | Logo, description, links   |
| `CLAUDE.md`     | AI assistant context | Organization name, purpose |
| `docs/INDEX.md` | Documentation portal | Organization references    |
| `FUNDING.yml`   | Sponsorship links    | Your sponsorship URLs      |

### Template Variable Replacement

```bash
# Replace all template variables
sed -i '' 's/{{ORG_NAME}}/your-org-name/g' README.md
sed -i '' 's/{{ORG_NAME}}/Your Organization/g' README.md
```

### Community Health Files

Customize these inherited files in the root:

| File                 | Purpose                   |
| -------------------- | ------------------------- |
| `CODE_OF_CONDUCT.md` | Community guidelines      |
| `CONTRIBUTING.md`    | Contribution guidelines   |
| `SECURITY.md`        | Security policy           |
| `SUPPORT.md`         | Support channels          |
| `FUNDING.yml`        | Sponsorship configuration |

______________________________________________________________________

## Workflow Modifications

### Enabling/Disabling Workflows

To disable a workflow without deleting it:

```yaml
# Add at the top of the workflow file
name: Workflow Name (Disabled)

on:
  workflow_dispatch:  # Only manual trigger
  # push: (commented out)
  # pull_request: (commented out)
```

Or move to a disabled directory:

```bash
mkdir -p .github/workflows/disabled
mv .github/workflows/unused-workflow.yml .github/workflows/disabled/
```

### Modifying Triggers

Common trigger patterns:

```yaml
# Push to specific branches
on:
  push:
    branches: [main, develop, 'release/**']
    paths:
      - 'src/**'
      - '!src/**/*.md'

# Pull request with path filters
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

# Scheduled runs
on:
  schedule:
    - cron: '0 9 * * 1-5'  # Weekdays at 9 AM UTC
```

### Adjusting Workflow Behavior

Modify default values:

```yaml
# In workflow file
env:
  COVERAGE_THRESHOLD: ${{ vars.COVERAGE_THRESHOLD || '80' }}  # Changed from 58
  MAX_STALE_DAYS: 30  # Organization preference
```

______________________________________________________________________

## Adding New Workflows

### Workflow Template

```yaml
name: New Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: false
        default: 'development'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  main:
    name: Main Job
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4

      - name: Setup
        run: |
          echo "Setting up..."

      - name: Execute
        run: |
          echo "Executing main logic..."
```

### Using Reusable Workflows

Reference existing reusable workflows:

```yaml
jobs:
  python-test:
    uses: ./.github/workflows/reusable/python-setup-test.yml
    with:
      python-version: '3.12'
      run-tests: true

  security:
    uses: ./.github/workflows/reusable/security-scanning.yml
    secrets: inherit
```

### Workflow Naming Convention

```
<category>-<action>.yml

Examples:
  ci.yml              - Main CI workflow
  deploy-staging.yml  - Staging deployment
  release.yml         - Release automation
  pr-labeler.yml      - PR labeling
```

______________________________________________________________________

## AI Framework Customization

### Adding Custom Agents

Create new agent files in `src/ai_framework/agents/`:

```markdown
---
name: Custom Agent Name
description: One-sentence description of the agent's purpose.
tools:
  - read
  - edit
  - search
tags:
  - custom
  - domain-specific
updated: 2026-01-30
---

# Custom Agent Name

## Purpose

Describe what this agent does and when to use it.

## Capabilities

- Capability 1
- Capability 2

## Usage

Instructions for invoking this agent.

## Example Prompts

- "Help me with X"
- "Analyze Y and suggest Z"
```

### Customizing Instructions

Add custom coding instructions in `src/ai_framework/instructions/`:

```markdown
---
name: Custom Instruction
description: Specific coding instruction for your domain.
language: python
tags:
  - custom
---

# Custom Instruction

When writing code for this organization:

1. Follow these patterns...
2. Use these libraries...
3. Avoid these anti-patterns...
```

### Adding Chat Modes

Create chat modes in `src/ai_framework/chatmodes/`:

```markdown
---
name: Custom Chat Mode
description: Specialized conversation mode.
context: domain-specific
---

# Custom Chat Mode

You are a specialized assistant for [domain].

## Behavior

- Focus on [specific area]
- Use [specific terminology]
- Provide [type of responses]
```

______________________________________________________________________

## Label Customization

### Adding Labels

Update label configuration in `.github/labels.yml`:

```yaml
- name: "org/custom-label"
  description: "Organization-specific label"
  color: "0e8a16"

- name: "priority/p0"
  description: "Critical priority"
  color: "b60205"
```

### Syncing Labels

```bash
# Using GitHub CLI
gh label create "org/custom-label" --description "Custom label" --color "0e8a16"

# Or run the label sync workflow
gh workflow run label-sync.yml
```

______________________________________________________________________

## Issue and PR Templates

### Custom Issue Templates

Add templates in `.github/ISSUE_TEMPLATE/`:

```markdown
---
name: Custom Issue Type
about: Template for custom issue type
title: "[CUSTOM] "
labels: org/custom-label
assignees: ''
---

## Description

<!-- Describe the issue -->

## Context

<!-- Relevant context -->

## Expected Outcome

<!-- What should happen -->
```

### Custom PR Template

Modify `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description

<!-- Describe your changes -->

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Follows code style guidelines

## Related Issues

Closes #
```

______________________________________________________________________

## Automation Scripts

### Adding Custom Scripts

Create scripts in `src/automation/scripts/`:

```python
#!/usr/bin/env python3
"""
Custom automation script.

Usage:
    python custom_script.py --option value
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Custom script")
    parser.add_argument("--option", required=True, help="Option description")
    args = parser.parse_args()

    # Script logic here
    print(f"Running with option: {args.option}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Integrating with Workflows

```yaml
- name: Run custom script
  run: |
    python src/automation/scripts/custom_script.py --option value
```

______________________________________________________________________

## Removing Unused Components

### Safe Removal Checklist

Before removing any component:

1. **Check dependencies**: Search for references

   ```bash
   grep -r "component-name" .github/workflows/
   ```

1. **Check imports**: For Python scripts

   ```bash
   grep -r "from component import" src/
   ```

1. **Archive instead of delete**: Move to archive directory

   ```bash
   mkdir -p archive/removed
   mv component archive/removed/
   ```

### Components Safe to Remove

| Component        | Dependencies               | Safe to Remove         |
| ---------------- | -------------------------- | ---------------------- |
| Unused workflows | Check triggers             | Yes, if not referenced |
| Unused agents    | Check workflow invocations | Yes                    |
| Documentation    | None                       | Yes                    |
| Test files       | None                       | Yes                    |

______________________________________________________________________

## Testing Customizations

### Local Testing

```bash
# Run tests
python -m pytest tests/ -v

# Run pre-commit
pre-commit run --all-files

# Validate workflow syntax
python -c "
import yaml
from pathlib import Path
for f in Path('.github/workflows').glob('*.yml'):
    yaml.safe_load(f.read_text())
    print(f'{f.name}: OK')
"
```

### CI Testing

Create a test branch:

```bash
git checkout -b test/customization
# Make changes
git push -u origin test/customization
# Open PR to trigger CI
gh pr create --title "Test: Customization" --body "Testing customizations"
```

______________________________________________________________________

## Best Practices

### Do

- Keep customizations documented
- Use repository variables for configurable values
- Test changes in branches before merging
- Maintain backward compatibility
- Follow existing naming conventions

### Avoid

- Hardcoding organization-specific values in workflows
- Removing safety checks without understanding impact
- Modifying reusable workflows without testing consumers
- Creating duplicate workflows for minor variations

______________________________________________________________________

## Next Steps

- **[Workflow Guide](../guides/WORKFLOWS.md)** - Workflow patterns and
  troubleshooting
- **[Agents Guide](../guides/AGENTS.md)** - Working with AI agents
- **[Architecture Overview](../architecture/OVERVIEW.md)** - Understanding the
  system design
