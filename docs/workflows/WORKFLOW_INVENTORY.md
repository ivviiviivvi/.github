# GitHub Actions Workflow Inventory

**Generated:** 2026-01-14\
**Total Workflows:** 99\
**Status:** 🔴 19 YAML syntax
errors, 80 working workflows

______________________________________________________________________

## Executive Summary

### Critical Findings

- **🔴 19 workflows with YAML syntax errors** - Preventing execution
- **💡 79 workflows without manual dispatch** - Hard to test
- **📊 7 high-complexity workflows** (>15KB) - Maintenance burden
- **🔄 78 workflows with undefined triggers** - Needs investigation
- **⏰ 1 workflow with cron schedule** - weekly-commit-report.yml

### Recommendations

1. **Immediate**: Fix 19 YAML syntax errors (Phase 4.2)
1. **High Priority**: Add `workflow_dispatch` to all workflows for testing
1. **Medium Priority**: Split high-complexity workflows into smaller, reusable
   components
1. **Low Priority**: Optimize triggers and consolidate duplicates

______________________________________________________________________

## Workflow Statistics

| Metric                  | Count |
| ----------------------- | ----- |
| Total Workflows         | 99    |
| With YAML Errors        | 19    |
| Scheduled (cron)        | 1     |
| Manual Dispatch Enabled | 1     |
| Push Triggers           | 1     |
| Pull Request Triggers   | 1     |
| Undefined Triggers      | 78    |

______________________________________________________________________

## YAML Syntax Errors (19 Workflows)

These workflows have critical YAML syntax errors preventing execution:

### 1. `branch-lifecycle-management.yml`

- **Error**: `expected alphabetic or numeric character, but found '*'` (line 73,
  column 2)
- **Cause**: Invalid YAML alias or anchor syntax
- **Priority**: 🔴 HIGH

### 2. `branch-lifecycle.yml`

- **Error**: `could not find expected ':'` (line 131, column 1)
- **Cause**: Missing colon in key-value pair
- **Priority**: 🔴 HIGH

### 3. `collect-deployment-metadata.yml`

- **Error**: `could not find expected ':'` (line 110, column 1)
- **Cause**: Malformed YAML structure
- **Priority**: 🔴 MEDIUM

### 4. `deploy-to-pages-live.yml`

- **Error**: `could not find expected ':'` (line 229, column 3)
- **Cause**: Indentation or structure issue
- **Priority**: 🔴 HIGH

### 5-9. `*_workflow.yml` (5 files)

Files affected:

- `gemini_workflow.yml`

- `grok_workflow.yml`

- `openai_workflow.yml`

- `perplexity_workflow.yml`

- `process_queue.yml`

- **Error**: `mapping values are not allowed here` (line 64/81, column 48)

- **Cause**: Likely inline comment or string formatting issue

- **Priority**: 🔴 MEDIUM

### 10. `manual_reset.yml`

- **Error**: `mapping values are not allowed here` (line 37, column 48)
- **Cause**: Same as above
- **Priority**: 🔴 LOW

### 11. `pr-batch-merge.yml`

- **Error**: `could not find expected ':'` (line 136, column 1)
- **Cause**: Missing colon in mapping
- **Priority**: 🔴 HIGH

### 12. `pr-consolidation.yml`

- **Error**: `could not find expected ':'` (line 503, column 1)
- **Cause**: Large file (500+ lines), likely indentation issue
- **Priority**: 🔴 HIGH

### 13. `pr-task-catcher.yml`

- **Error**: `could not find expected ':'` (line 254, column 1)
- **Cause**: Missing colon
- **Priority**: 🔴 MEDIUM

### 14. `repository-bootstrap.yml`

- **Error**: `expected <block end>, but found '-'` (line 379, column 1)
- **Cause**: Unexpected list item or indentation error
- **Priority**: 🔴 MEDIUM

### 15. `reset_quotas.yml`

- **Error**: `mapping values are not allowed here` (line 33, column 48)
- **Cause**: Inline formatting issue
- **Priority**: 🔴 LOW

### 16-18. `safeguard-*-*.yml` (3 files)

Files affected:

- `safeguard-7-staggered-scheduling.yml`

- `safeguard-8-usage-monitoring.yml`

- `task-extraction.yml`

- **Error**: `expected alphabetic or numeric character, but found '*'` (lines
  131-373)

- **Cause**: Invalid alias/anchor syntax

- **Priority**: 🔴 HIGH

### 19. `version-control-standards.yml`

- **Error**: `could not find expected ':'` (line 197, column 1)
- **Cause**: Missing colon
- **Priority**: 🔴 MEDIUM

______________________________________________________________________

## High Complexity Workflows (>15KB)

These workflows are large and complex, making them harder to maintain:

| Workflow                            | Size  | Jobs | Complexity Score |
| ----------------------------------- | ----- | ---- | ---------------- |
| `create-organizational-content.yml` | ~21KB | 5    | 21,616           |
| `safeguard-6-admin-approval.yml`    | ~20KB | 1    | 20,132           |
| `draft-to-ready-automation.yml`     | ~18KB | 2    | 18,510           |
| `batch-pr-lifecycle.yml`            | ~18KB | 5    | 18,098           |
| `reconcile-deployments.yml`         | ~17KB | 1    | 17,019           |
| `bio-description-completions.yml`   | ~15KB | 1    | 15,474           |
| `usage-monitoring.yml`              | ~15KB | 3    | 15,428           |

**Recommendation**: Consider splitting these into smaller, reusable workflows.

______________________________________________________________________

## Trigger Distribution Analysis

| Trigger Type      | Count | Notes                                                 |
| ----------------- | ----- | ----------------------------------------------------- |
| Unknown/Undefined | 78    | Needs investigation - may be workflow_call or invalid |
| Push              | 1     | commit-tracking.yml                                   |
| Pull Request      | 1     | commit-tracking.yml                                   |
| Schedule (cron)   | 1     | weekly-commit-report.yml                              |
| Manual Dispatch   | 1     | weekly-commit-report.yml                              |

**Issue**: 78 workflows show "unknown" triggers, which likely means:

- They use `workflow_call` (reusable workflows)
- They have complex conditional triggers
- They have syntax errors preventing trigger parsing

______________________________________________________________________

## Working Workflows by Category

### CI/CD & Testing (7 workflows)

- `ci.yml` - Basic CI pipeline
- `ci-advanced.yml` - Advanced CI with change detection
- `code-coverage.yml` - Coverage reporting
- `mutation-testing.yml` - Mutation testing
- `performance-benchmark.yml` - Performance metrics
- `pr-quality-checks.yml` - PR validation
- `commit-tracking.yml` - Commit analysis

### Security & Compliance (6 workflows)

- `codeql-analysis.yml` - CodeQL analysis
- `security-scan.yml` - General security scanning
- `semgrep.yml` - Semgrep analysis
- `scan-for-secrets.yml` - Secret detection
- `dependency-review.yml` - Dependency security
- `sbom-generation.yml` - Software bill of materials

### Automation (15 workflows)

- `auto-merge.yml` - Auto-merge PRs
- `auto-enable-merge.yml` - Enable merge automatically
- `auto-pr-create.yml` - Create PRs automatically
- `auto-assign.yml` - Auto-assign issues/PRs
- `auto-labeler.yml` - Auto-label issues/PRs
- `auto-batch-prs.yml` - Batch automated PRs
- `nightly-cleanup.yml` - Nightly maintenance
- `daily-pr-consolidator.yml` - Consolidate bot PRs
- `daily-orchestrator.yml` - Daily task orchestration
- `batch-pr-operations.yml` - Bulk PR operations
- `batch-pr-lifecycle.yml` - Batch PR management
- `pr-suggestion-implementation.yml` - Implement PR suggestions
- `staggered-scheduling.yml` - Quota-aware scheduling
- `orchestrator.yml` - AI task orchestrator
- `combine-prs.yml` - Combine multiple PRs

### AI Assistants (8 workflows)

- `gemini-review.yml` - Gemini code review
- `gemini-triage.yml` - Gemini issue triage
- `gemini-scheduled-triage.yml` - Scheduled triage
- `gemini-invoke.yml` - Manual Gemini invoke
- `gemini-dispatch.yml` - Gemini dispatcher
- `claude.yml` - Claude assistant
- `claude-code-review.yml` - Claude reviews
- `jules.yml` - Jules agent

### Documentation & Content (7 workflows)

- `build-pages-site.yml` - GitHub Pages build
- `generate-pages-index.yml` - Pages index generation
- `link-checker.yml` - Link validation
- `accessibility-testing.yml` - A11y testing
- `bio-description-completions.yml` - Profile completions
- `generate-walkthrough.yml` - Video walkthroughs
- `org-walkthrough-generator.yml` - Org-wide walkthroughs

### Metrics & Monitoring (9 workflows)

- `health-check.yml` - Workflow health check
- `health-check-live-apps.yml` - App health monitoring
- `metrics-collection.yml` - Metrics gathering
- `metrics-dashboard.yml` - Dashboard generation
- `repo-metrics.yml` - Repository metrics
- `usage-monitoring.yml` - Usage tracking
- `org-health-crawler.yml` - Organization health
- `alert-on-workflow-failure.yml` - Failure notifications
- `weekly-commit-report.yml` - Weekly commit reports

### Deployment & Release (6 workflows)

- `deployment.yml` - Production deployment
- `docker-build-push.yml` - Docker images
- `release.yml` - Release management
- `semantic-release.yml` - Semantic versioning
- `version-bump.yml` - Version updates
- `agentsphere-deployment.yml` - AgentSphere deploys

### Organization Management (8 workflows)

- `create-organizational-content.yml` - Content creation
- `org-wide-workflow-dispatch.yml` - Org-wide dispatch
- `scheduled-walkthrough-generator.yml` - Scheduled walkthroughs
- `badge-management.yml` - Badge updates
- `label-sync.yml` - Label synchronization
- `project-automation.yml` - Project board automation
- `reconcile-deployments.yml` - Deployment reconciliation
- `validate-workspace-config.yml` - Workspace validation

### Community & Engagement (5 workflows)

- `welcome.yml` - Welcome new contributors
- `stale.yml` - Stale issue management
- `community-health.yml` - Community metrics
- `branch-cleanup-notify.yml` - Stale branch notifications

### Reusable Workflows (5 workflows)

- `reusable-notify.yml` - Notification template
- `reusable-api-retry.yml` - API retry logic
- `reusable-security-scan.yml` - Security scan template
- `reusable-app-detect.yml` - App detection template

### Admin & Safeguards (4+ workflows)

- `admin-approval-dashboard.yml` - Approval dashboard
- `safeguard-5-secret-scanning.yml` - Secret scanning
- `safeguard-6-admin-approval.yml` - Admin approval
- `validate-quality.yml` - Video quality validation

______________________________________________________________________

## Recommendations

### Phase 4.2: Fix YAML Errors (Priority: 🔴 CRITICAL)

1. **Check line-by-line** the 19 workflows with syntax errors
1. **Common issues**:
   - Missing colons after keys
   - Invalid YAML alias/anchor syntax (`*` without proper definition)
   - Inline comments breaking YAML parsing (`: # comment` → `': # comment'`)
   - Indentation errors
1. **Validate** after fixes: Use `yamllint` or Python's `yaml.safe_load()`

### Phase 4.3: Add Manual Dispatch (Priority: 🟡 HIGH)

Add `workflow_dispatch:` to all 79 workflows missing it:

```yaml
on:
  workflow_dispatch:
  # ... existing triggers
```

This enables manual testing without waiting for triggers.

### Phase 4.4: Consolidate Reusable Workflows (Priority: 🟢 MEDIUM)

Create reusable workflow templates for common patterns:

- Python CI/lint/test
- Node CI/lint/test
- Security scanning
- Deployment steps

Move to `.github/workflows/reusable/` directory.

### Phase 4.5: Optimize Triggers (Priority: 🟢 LOW)

1. Review `push` triggers - should they be `pull_request`?
1. Add path filters where appropriate
1. Implement concurrency groups to cancel redundant runs

______________________________________________________________________

## Next Steps

1. ✅ **Phase 4.1 Complete**: Workflow inventory generated
1. 🔄 **Phase 4.2 In Progress**: Fix 19 YAML syntax errors
1. ⏸️ **Phase 4.3 Pending**: Consolidate reusable workflows
1. ⏸️ **Phase 4.4 Pending**: Optimize workflow triggers

______________________________________________________________________

**Last Updated:** 2026-01-14\
**Related Issues:** #193, #207 (21 errors = 19
YAML + 2 other issues)
