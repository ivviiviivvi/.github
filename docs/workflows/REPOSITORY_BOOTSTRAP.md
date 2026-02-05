# Repository Bootstrap Workflow

Automate the setup of repository features including issues, projects,
discussions, wiki, labels, and workflow templates.

## Overview

The Repository Bootstrap workflow provides automated setup of standard
organization features for any repository. It ensures consistency across all
repositories and saves time by automating repetitive configuration tasks.

## Features

### Repository Features

- ✅ **Issues** - Enable issue tracking
- ✅ **Projects** - Enable project boards
- ✅ **Discussions** - Enable community discussions
- ✅ **Wiki** - Enable wiki documentation

### Automation

- 🏷️ **Standard Labels** - Creates 30+ standardized labels from `docs/LABELS.md`
- 📋 **Project Board** - Creates initial project board for task tracking
- 📄 **Workflow Templates** - Copies CI/CD workflow templates from `.github` repo
- 🔒 **Branch Protection** - Configures branch protection rules for main branch

## Usage

### As a Reusable Workflow

Call this workflow from another repository:

```yaml
name: Bootstrap Repository
on:
  workflow_dispatch:

jobs:
  bootstrap:
    uses: ivviiviivvi/.github/.github/workflows/repository-bootstrap.yml@main
    with:
      target_repository: ${{ github.repository }}
      enable_issues: true
      enable_projects: true
      enable_discussions: true
      enable_wiki: false
      create_labels: true
      create_project_board: true
      copy_workflow_templates: true
      configure_branch_protection: true
    secrets:
      GH_PAT: ${{ secrets.GITHUB_TOKEN }}
```

### From Workflow Templates

1. Navigate to **Actions** → **New workflow**
1. Find **Repository Bootstrap Workflow** in "By your organization"
1. Click **Set up this workflow**
1. Customize inputs as needed
1. Commit the workflow file

### Manual Trigger

1. Go to **Actions** tab in the `.github` repository
1. Select **Repository Bootstrap** workflow
1. Click **Run workflow**
1. Configure options:
   - Enter target repository (e.g., `org/repo` or `current`)
   - Select features to enable
   - Choose automation options
1. Click **Run workflow**

## Inputs

| Input                         | Type    | Default   | Description                               |
| ----------------------------- | ------- | --------- | ----------------------------------------- |
| `target_repository`           | string  | `current` | Target repository (org/repo or 'current') |
| `enable_issues`               | boolean | `true`    | Enable Issues feature                     |
| `enable_projects`             | boolean | `true`    | Enable Projects feature                   |
| `enable_discussions`          | boolean | `false`   | Enable Discussions feature                |
| `enable_wiki`                 | boolean | `false`   | Enable Wiki feature                       |
| `create_labels`               | boolean | `true`    | Create standard organization labels       |
| `create_project_board`        | boolean | `false`   | Create initial project board              |
| `copy_workflow_templates`     | boolean | `false`   | Copy workflow templates from .github repo |
| `configure_branch_protection` | boolean | `false`   | Configure branch protection rules         |

## What Gets Created

### Standard Labels (30+)

When `create_labels` is enabled, the workflow creates labels in these
categories:

**Type Labels:**

- bug, enhancement, documentation, question, refactoring, performance, security,
  testing

**Priority Labels:**

- critical, high priority, medium priority, low priority

**Status Labels:**

- in progress, blocked, on hold, needs review, needs testing, ready to merge

**Community Labels:**

- good first issue, help wanted

**Additional Labels:**

- discussion, duplicate, invalid, wontfix, automated, dependencies, stale,
  github-actions, frontend, backend, infrastructure, accessibility

### Workflow Templates

When `copy_workflow_templates` is enabled, the following templates are copied:

1. **ci.yml** - Basic CI pipeline for building, testing, and linting
1. **security-scan.yml** - CodeQL security scanning
1. **dependency-updates.yml** - Automated dependency updates with Dependabot
1. **stale-management.yml** - Automatic stale issue and PR management

Templates are copied to `.github/workflows/` and a PR is automatically created
for review.

### Branch Protection Rules

When `configure_branch_protection` is enabled:

- ✅ Require pull request reviews (1 approving review)
- ✅ Dismiss stale reviews when new commits are pushed
- ✅ Require conversation resolution before merging
- ✅ Prevent force pushes
- ✅ Prevent branch deletion
- ⚠️ Admins not exempt (can be overridden)

### Project Board

When `create_project_board` is enabled:

- Creates "Development Board" project (GitHub Projects V2)
- Linked to the organization
- Ready for customization with views and workflows

## Requirements

### Permissions

**For enabling repository features:**

- Repository `administration` write permission
- Organization member with appropriate role

**For creating labels:**

- Repository `issues` write permission

**For copying workflow templates:**

- Repository `contents` write permission
- Repository `pull-requests` write permission

**For branch protection:**

- Repository `administration` write permission
- Personal Access Token (PAT) with `repo` scope

### Secrets

| Secret   | Required | Description                                                                                                                                                    |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GH_PAT` | Optional | Personal Access Token with repo and admin:org scopes. Required for branch protection and some advanced features. Falls back to `GITHUB_TOKEN` if not provided. |

## Examples

### Complete Bootstrap for New Repository

```yaml
jobs:
  bootstrap:
    uses: ivviiviivvi/.github/.github/workflows/repository-bootstrap.yml@main
    with:
      target_repository: "ivviiviivvi/new-project"
      enable_issues: true
      enable_projects: true
      enable_discussions: true
      enable_wiki: false
      create_labels: true
      create_project_board: true
      copy_workflow_templates: true
      configure_branch_protection: true
    secrets:
      GH_PAT: ${{ secrets.ORG_ADMIN_TOKEN }}
```

### Minimal Bootstrap (Labels Only)

```yaml
jobs:
  bootstrap:
    uses: ivviiviivvi/.github/.github/workflows/repository-bootstrap.yml@main
    with:
      target_repository: "ivviiviivvi/existing-project"
      enable_issues: false
      enable_projects: false
      enable_discussions: false
      enable_wiki: false
      create_labels: true
      create_project_board: false
      copy_workflow_templates: false
      configure_branch_protection: false
```

### Add Workflows to Existing Repository

```yaml
jobs:
  bootstrap:
    uses: ivviiviivvi/.github/.github/workflows/repository-bootstrap.yml@main
    with:
      target_repository: ${{ github.repository }}
      enable_issues: false
      enable_projects: false
      enable_discussions: false
      enable_wiki: false
      create_labels: false
      create_project_board: false
      copy_workflow_templates: true
      configure_branch_protection: false
```

## Workflow Details

### Execution Time

- **Typical duration:** 2-5 minutes
- **Maximum timeout:** 15 minutes

### Concurrency

- Uses concurrency control to prevent multiple runs on the same repository
- Concurrent runs for different repositories are allowed

### Error Handling

The workflow includes graceful error handling:

- ⚠️ Non-critical failures (like feature enablement requiring admin) log
  warnings but don't fail the workflow
- ❌ Critical failures (like repository access) fail the workflow with clear
  error messages
- 📊 Summary report shows what succeeded and what was skipped

### Idempotency

The workflow is idempotent - running it multiple times on the same repository:

- Skips labels that already exist
- Skips workflow files that already exist
- Updates feature settings to match inputs
- Does not duplicate project boards

## Integration with Other Features

### Repository Setup Agent

This workflow complements the `repository-setup` agent (in
`agents/repository-setup.agent.md`). The agent provides AI-driven setup and
customization, while this workflow provides automated, repeatable configuration.

### Bio and Description Completions

After bootstrapping, run the `bio-description-completions.yml` workflow to audit
and complete repository metadata.

### Repository Health Check

Use `repository-health-check.yml` workflow template to monitor ongoing
repository health after bootstrap.

## Troubleshooting

### "Cannot access repository" Error

**Cause:** Invalid repository name or insufficient permissions

**Solution:**

- Verify repository name format: `org/repo`
- Ensure the PAT or GITHUB_TOKEN has `repo` scope
- Check that the repository exists

### "Could not update repository features" Warning

**Cause:** Requires admin permissions

**Solution:**

- Provide a PAT with admin:org scope via `GH_PAT` secret
- Manually enable features in repository settings
- Ask an organization admin to run the workflow

### "Could not enable Discussions" Warning

**Cause:** Discussions not available for this repository type

**Solution:**

- Verify repository is public or part of GitHub Enterprise
- Enable Discussions manually in repository settings
- Skip this feature for private repositories without Enterprise

### "Could not configure branch protection" Warning

**Cause:** Requires admin permissions and fine-grained PAT

**Solution:**

- Create a fine-grained PAT with `administration:write` permission
- Add PAT as `GH_PAT` repository secret
- Manually configure branch protection rules

### Workflow Templates PR Not Created

**Cause:** No new templates to copy or branch already exists

**Solution:**

- Check if templates already exist in target repository
- Delete the `bootstrap/workflow-templates-*` branch if it exists
- Review workflow logs for specific errors

## Best Practices

1. **Test on a demo repository first** - Verify settings before applying to
   production repositories

1. **Use organization-level PAT** - Store a PAT with appropriate permissions at
   the organization level for reuse

1. **Customize labels** - Edit `docs/LABELS.md` in the `.github` repository to
   define organization-wide labels

1. **Review template PRs** - Always review and test workflow template PRs before
   merging

1. **Run incrementally** - Start with labels and features, then add workflows
   and branch protection

1. **Document customizations** - Track any repository-specific deviations from
   organization standards

## Related Documentation

- [Repository Purpose Analysis](../architecture/REPOSITORY_PURPOSE_ANALYSIS.md)
  \- Understanding what belongs in repositories
- [Repository Setup Checklist](../REPOSITORY_SETUP_CHECKLIST.md) - Manual setup
  checklist
- [Labels Documentation](../LABELS.md) - Standard label definitions
- [Repository Setup Agent](../../ai_framework/agents/repository-setup.agent.md)
  \- AI-powered setup assistant

## Contributing

To enhance this workflow:

1. Test changes in a fork first
1. Update documentation with new features
1. Follow conventional commit messages
1. Add examples for new functionality

______________________________________________________________________

**Last Updated:** 2025-12-23\
**Workflow Version:** 1.0.0\
**Maintained by:**
Organization Automation Team
