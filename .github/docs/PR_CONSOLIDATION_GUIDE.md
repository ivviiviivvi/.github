# PR Consolidation Workflow Guide

## Overview

The PR Consolidation Workflow (`pr-consolidation.yml`) is designed to
consolidate multiple open pull requests into a single unified PR. This helps
manage situations where many PRs have accumulated and need to be reviewed and
merged together efficiently.

## Purpose

This workflow:

- **Consolidates** all open PRs into a single branch
- **Resolves** merge conflicts automatically where possible
- **Extracts** tasks and suggestions from PR descriptions and comments
- **Preserves** all functionality from the original PRs
- **Documents** any issues requiring manual review
- **Closes** original PRs after consolidation
- **Results** in a single consolidated PR ready for final review and merge

## When to Use

Use this workflow when:

- Multiple PRs have accumulated and need to be merged together
- You want to streamline the review process for related changes
- PRs have dependencies or overlapping changes
- You need a comprehensive view of all pending changes
- You want to ensure all functionality is preserved across multiple PRs

## How It Works

### Workflow Steps

1. **Analyze PRs**: Lists all open PRs and their metadata
1. **Create Consolidation Branch**: Creates a new branch from `main`
1. **Merge PRs**: Iteratively merges each PR branch into the consolidation
   branch
1. **Handle Conflicts**: Automatically resolves conflicts where possible,
   documents others
1. **Extract Tasks**: Pulls out action items, TODOs, and suggestions from PR
   descriptions and comments
1. **Create Consolidated PR**: Opens a new PR with comprehensive documentation
1. **Close Original PRs**: Closes all original PRs with explanatory comments
1. **Generate Report**: Creates detailed summary of the consolidation process

### Merge Conflict Resolution

The workflow attempts to resolve merge conflicts automatically using the
"theirs" strategy (accepting incoming changes). If automatic resolution fails:

- The conflict is documented in detail
- Conflicted files are listed
- Manual review is flagged in the consolidated PR

## Usage

### Triggering the Workflow

The workflow is triggered manually via GitHub Actions:

1. Go to **Actions** → **PR Consolidation - Merge All Open PRs**
1. Click **Run workflow**
1. Configure options:
   - **Consolidation Branch**: Custom branch name (optional)
   - **Exclude PRs**: Comma-separated PR numbers to skip (e.g., `101,102`)
   - **Dry Run**: Test without making changes (recommended for first run)

### Input Parameters

| Parameter              | Description                             | Required | Default                            |
| ---------------------- | --------------------------------------- | -------- | ---------------------------------- |
| `consolidation_branch` | Name for the consolidation branch       | No       | `pr-consolidation-YYYYMMDD-HHMMSS` |
| `exclude_prs`          | PR numbers to exclude (comma-separated) | No       | None                               |
| `dry_run`              | Run without making actual changes       | No       | `false`                            |

### Example 1: Basic Consolidation

```yaml
# Run with defaults
consolidation_branch: (leave empty)
exclude_prs: (leave empty)
dry_run: false
```

This will:

- Create a branch named `pr-consolidation-20231225-143022`
- Process all open PRs
- Create the consolidated PR

### Example 2: Dry Run First

```yaml
consolidation_branch: test-consolidation
exclude_prs: (leave empty)
dry_run: true
```

This will:

- Show what would happen without making changes
- Help you verify the process before actual consolidation
- No branches created, no PRs modified

### Example 3: Exclude Specific PRs

```yaml
consolidation_branch: feature-consolidation
exclude_prs: 101,102,104
dry_run: false
```

This will:

- Skip PRs #101, #102, and #104
- Process all other open PRs
- Useful when some PRs need separate handling

## Output and Reports

### Consolidated PR

The workflow creates a comprehensive PR that includes:

1. **Summary Section**
   - Total PRs consolidated
   - Successfully merged count
   - Conflicts encountered

1. **Consolidated PRs List**
   - Checklist of all included PRs
   - Links to original PRs
   - Author information

1. **Merge Report**
   - Details for each PR merge
   - Conflict information
   - Resolution status

1. **Extracted Tasks**
   - All PR descriptions
   - Comments and discussions
   - TODO/FIXME/NOTE items

1. **Issues Requiring Decision**
   - Merge conflicts (if any)
   - Functionality preservation checklist
   - Next steps

### Artifacts

The workflow generates downloadable artifacts:

- `pr-data`: JSON file with all PR metadata
- `merge-report`: Detailed merge report
- `tasks-summary`: Extracted tasks and suggestions

## Best Practices

### Before Running

1. **Review Open PRs**: Understand what will be consolidated
1. **Check CI Status**: Ensure PRs have passing tests
1. **Communicate**: Notify team members about the consolidation
1. **Run Dry Run**: Test the process first with `dry_run: true`

### During Review

1. **Verify Functionality**: Test that all features still work
1. **Check Conflicts**: Review any auto-resolved conflicts
1. **Validate Tests**: Run full test suite
1. **Review Tasks**: Address extracted action items

### After Merging

1. **Verify Closure**: Confirm all original PRs are closed
1. **Update Documentation**: If needed based on changes
1. **Deploy Changes**: Follow your deployment process
1. **Communicate**: Notify team of successful consolidation

## Troubleshooting

### Workflow Fails to Fetch PR Branch

**Issue**: `Could not fetch branch <branch-name>`

**Solution**:

- Verify the branch still exists
- Check if the PR has been closed
- Exclude the problematic PR using `exclude_prs`

### Too Many Merge Conflicts

**Issue**: Many PRs have conflicts

**Solution**:

- Break consolidation into smaller groups
- Manually resolve conflicts in some PRs first
- Use `exclude_prs` to handle problematic PRs separately

### Original PRs Not Closing

**Issue**: PRs remain open after consolidation

**Solution**:

- Check workflow permissions
- Manually close PRs if needed
- Verify the `close-original-prs` job completed

### Consolidated PR Too Large

**Issue**: The consolidated PR is overwhelming to review

**Solution**:

- Break into multiple consolidation runs
- Group related PRs together
- Use `exclude_prs` to create smaller consolidations

## Permissions Required

The workflow requires these permissions:

- `contents: write` - To create branches and push changes
- `pull-requests: write` - To create and close PRs
- `issues: write` - To create summary issues

## Safety Features

1. **Dry Run Mode**: Test without making changes
1. **Exclude List**: Skip specific PRs if needed
1. **Conflict Documentation**: All conflicts are recorded
1. **Atomic Operations**: Each PR merge is independent
1. **Abort on Failure**: Conflicts don't block other PRs
1. **Detailed Logging**: Full audit trail of all actions

## Related Workflows

- `batch-pr-lifecycle.yml` - Automated PR lifecycle management
- `pr-batch-merge.yml` - Batch merge PRs with same label
- `combine-prs.yml` - Simple PR combination

## Support

For issues or questions:

1. Check the workflow run logs
1. Review the generated artifacts
1. Open an issue with the `workflow-support` label
1. Reference the workflow run URL

## Examples

### Scenario 1: Consolidate All Open PRs

You have 5 open PRs that all relate to the same feature and want to review them
together.

```
1. Go to Actions → PR Consolidation
2. Click "Run workflow"
3. Leave all fields empty (use defaults)
4. Click "Run workflow"
```

Result: All 5 PRs are merged into a new consolidation PR.

### Scenario 2: Test Consolidation First

You want to see what would happen before actually consolidating.

```
1. Go to Actions → PR Consolidation
2. Click "Run workflow"
3. Set dry_run: true
4. Click "Run workflow"
5. Review the logs
```

Result: No changes made, but you see what would happen.

### Scenario 3: Consolidate Except One PR

You have 4 PRs to consolidate, but PR #102 needs separate review.

```
1. Go to Actions → PR Consolidation
2. Click "Run workflow"
3. Set exclude_prs: 102
4. Click "Run workflow"
```

Result: PRs #101, #103, #104 are consolidated, #102 remains open.

## Advanced Usage

### Custom Branch Naming

Use meaningful branch names for different types of consolidations:

```
# Feature consolidation
consolidation_branch: feature-auth-consolidation

# Bug fix consolidation
consolidation_branch: bugfix-consolidation-dec2023

# Hotfix consolidation
consolidation_branch: hotfix-emergency-consolidation
```

### Staged Consolidation

For many PRs, consolidate in stages:

**Stage 1**: Backend PRs

```
exclude_prs: 103,104,105  # Frontend PRs
```

**Stage 2**: Frontend PRs

```
exclude_prs: 101,102  # Backend PRs (already consolidated)
```

### Integration with CI/CD

After consolidation:

1. Wait for CI checks to pass on consolidated PR
1. Run additional integration tests
1. Perform manual testing if needed
1. Merge when all checks pass

## Maintenance

### Workflow Updates

To update the workflow:

1. Edit `.github/workflows/pr-consolidation.yml`
1. Test changes with dry run
1. Deploy to production

### Monitoring

Monitor workflow success:

- Check workflow run history
- Review consolidation PR quality
- Track conflict resolution rate
- Measure time savings

## Changelog

### Version 1.0.0 (2025-12-25)

- Initial release
- Support for basic PR consolidation
- Automatic conflict resolution
- Task extraction
- Dry run mode
- Exclude list functionality
