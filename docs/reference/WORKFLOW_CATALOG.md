# Workflow Catalog

Complete reference catalog of all GitHub Actions workflows in the {{ORG_NAME}}
template.

______________________________________________________________________

## Summary

- **Total Workflows**: 130+
- **Reusable Workflows**: 6
- **Categories**: 10

______________________________________________________________________

## Table of Contents

- [CI/CD Workflows](#cicd-workflows)
- [PR Automation](#pr-automation)
- [Issue Management](#issue-management)
- [Security & Compliance](#security--compliance)
- [AI & Code Intelligence](#ai--code-intelligence)
- [Metrics & Reporting](#metrics--reporting)
- [Release & Deployment](#release--deployment)
- [Maintenance & Cleanup](#maintenance--cleanup)
- [Reusable Workflows](#reusable-workflows)
- [Safeguard Workflows](#safeguard-workflows)

______________________________________________________________________

## CI/CD Workflows

### ci.yml

**Purpose**: Main continuous integration pipeline.

| Property     | Value                                       |
| ------------ | ------------------------------------------- |
| **Triggers** | Push (main, develop), PR, workflow_dispatch |
| **Jobs**     | lint, test, build-and-test-node, security   |
| **Inputs**   | None                                        |

**Key Features**:

- Python linting with pre-commit
- Test execution with coverage
- Node.js build (if package.json exists)
- Dependency review on PRs

______________________________________________________________________

### ci-advanced.yml

**Purpose**: Advanced CI with additional checks.

| Property     | Value                     |
| ------------ | ------------------------- |
| **Triggers** | Push, PR                  |
| **Jobs**     | lint, test, security-scan |
| **Inputs**   | None                      |

______________________________________________________________________

### code-coverage.yml

**Purpose**: Code coverage analysis and reporting.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | Push, PR                    |
| **Jobs**     | coverage                    |
| **Outputs**  | Coverage reports to Codecov |

______________________________________________________________________

### test-coverage.yml

**Purpose**: Detailed test coverage tracking.

| Property     | Value                   |
| ------------ | ----------------------- |
| **Triggers** | Push, PR                |
| **Jobs**     | test                    |
| **Outputs**  | JUnit XML, coverage.xml |

______________________________________________________________________

### run-integration-tests.yml

**Purpose**: Run integration test suite.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | workflow_dispatch, schedule |
| **Jobs**     | integration-tests           |
| **Inputs**   | test_suite, environment     |

______________________________________________________________________

## PR Automation

### auto-labeler.yml

**Purpose**: Automatically label PRs based on changed files.

| Property          | Value                  |
| ----------------- | ---------------------- |
| **Triggers**      | PR opened, synchronize |
| **Configuration** | `.github/labeler.yml`  |

______________________________________________________________________

### pr-title-lint.yml

**Purpose**: Validate PR titles follow conventional commit format.

| Property       | Value             |
| -------------- | ----------------- |
| **Triggers**   | PR opened, edited |
| **Validation** | \`^(feat          |

______________________________________________________________________

### pr-quality-checks.yml

**Purpose**: Enforce PR quality standards.

| Property     | Value                                                      |
| ------------ | ---------------------------------------------------------- |
| **Triggers** | PR                                                         |
| **Checks**   | Title format, description length, linked issues, checklist |

______________________________________________________________________

### pr-task-catcher.yml

**Purpose**: Ensure PR checklist tasks are completed.

| Property     | Value                    |
| ------------ | ------------------------ |
| **Triggers** | PR opened, edited        |
| **Action**   | Warns on unchecked tasks |

______________________________________________________________________

### auto-assign.yml

**Purpose**: Auto-assign PRs to authors.

| Property     | Value                      |
| ------------ | -------------------------- |
| **Triggers** | PR opened                  |
| **Action**   | Assigns author as assignee |

______________________________________________________________________

### auto-assign-reviewers.yml

**Purpose**: Auto-assign reviewers based on CODEOWNERS.

| Property     | Value                            |
| ------------ | -------------------------------- |
| **Triggers** | PR opened                        |
| **Action**   | Requests reviews from CODEOWNERS |

______________________________________________________________________

### auto-merge.yml

**Purpose**: Auto-merge approved PRs.

| Property       | Value                      |
| -------------- | -------------------------- |
| **Triggers**   | PR approved, checks passed |
| **Conditions** | All checks green, approved |

______________________________________________________________________

### auto-enable-merge.yml

**Purpose**: Enable auto-merge on qualifying PRs.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |
| **Inputs**   | pr_number         |

______________________________________________________________________

### combine-prs.yml

**Purpose**: Batch multiple Dependabot PRs into one.

| Property     | Value                                |
| ------------ | ------------------------------------ |
| **Triggers** | Schedule (weekly), workflow_dispatch |
| **Action**   | Creates combined PR                  |

______________________________________________________________________

### pr-batch-merge.yml

**Purpose**: Merge multiple PRs in batch.

| Property     | Value                    |
| ------------ | ------------------------ |
| **Triggers** | workflow_dispatch        |
| **Inputs**   | pr_numbers, merge_method |

______________________________________________________________________

### batch-pr-operations.yml

**Purpose**: Perform bulk operations on PRs.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |
| **Inputs**   | operation, filter |

______________________________________________________________________

### batch-pr-lifecycle.yml

**Purpose**: Manage PR lifecycle in batch.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | schedule, workflow_dispatch |

______________________________________________________________________

### draft-to-ready-automation.yml

**Purpose**: Auto-convert drafts to ready when checks pass.

| Property     | Value                 |
| ------------ | --------------------- |
| **Triggers** | check_suite completed |

______________________________________________________________________

### pr-suggestion-implementation.yml

**Purpose**: Implement PR review suggestions automatically.

| Property     | Value                    |
| ------------ | ------------------------ |
| **Triggers** | issue_comment            |
| **Command**  | `/implement-suggestions` |

______________________________________________________________________

## Issue Management

### issue-triage.yml

**Purpose**: Triage and label new issues.

| Property     | Value                   |
| ------------ | ----------------------- |
| **Triggers** | Issues opened           |
| **Actions**  | Add labels, assign team |

______________________________________________________________________

### welcome.yml

**Purpose**: Welcome first-time contributors.

| Property     | Value                          |
| ------------ | ------------------------------ |
| **Triggers** | Issues/PRs opened (first time) |
| **Action**   | Post welcome comment           |

______________________________________________________________________

### stale-management.yml

**Purpose**: Manage stale issues and PRs.

| Property        | Value            |
| --------------- | ---------------- |
| **Triggers**    | Schedule (daily) |
| **Stale After** | 60 days          |
| **Close After** | 7 days warning   |

______________________________________________________________________

### stale-management-ab.yml

**Purpose**: A/B test stale management strategies.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

### project-automation.yml

**Purpose**: Automate GitHub Projects board.

| Property     | Value                     |
| ------------ | ------------------------- |
| **Triggers** | Issues, PRs               |
| **Actions**  | Move cards, update status |

______________________________________________________________________

### task-extraction.yml

**Purpose**: Extract tasks from issues/comments.

| Property     | Value         |
| ------------ | ------------- |
| **Triggers** | issue_comment |

______________________________________________________________________

## Security & Compliance

### codeql-analysis.yml

**Purpose**: Static analysis with CodeQL.

| Property      | Value                                    |
| ------------- | ---------------------------------------- |
| **Triggers**  | Push, PR, schedule (weekly)              |
| **Languages** | Python, JavaScript, TypeScript, Go, Ruby |
| **Output**    | SARIF to Security tab                    |

______________________________________________________________________

### security-scan.yml

**Purpose**: Comprehensive security scanning.

| Property     | Value                   |
| ------------ | ----------------------- |
| **Triggers** | Push, PR, schedule      |
| **Tools**    | Trivy, dependency-check |

______________________________________________________________________

### semgrep.yml

**Purpose**: Semgrep static analysis.

| Property     | Value              |
| ------------ | ------------------ |
| **Triggers** | Push, PR           |
| **Rules**    | OWASP, CWE, custom |

______________________________________________________________________

### scan-for-secrets.yml

**Purpose**: Detect leaked secrets.

| Property     | Value      |
| ------------ | ---------- |
| **Triggers** | Push, PR   |
| **Tool**     | TruffleHog |

______________________________________________________________________

### dependency-review.yml

**Purpose**: Review dependency changes for vulnerabilities.

| Property     | Value                                  |
| ------------ | -------------------------------------- |
| **Triggers** | PR                                     |
| **Blocks**   | High/critical vulnerabilities, GPL-3.0 |

______________________________________________________________________

### sbom-generation.yml

**Purpose**: Generate Software Bill of Materials.

| Property     | Value                      |
| ------------ | -------------------------- |
| **Triggers** | Release, workflow_dispatch |
| **Formats**  | SPDX, CycloneDX            |

______________________________________________________________________

### validate-action-pins.yml

**Purpose**: Validate all actions are SHA-pinned.

| Property     | Value        |
| ------------ | ------------ |
| **Triggers** | PR, schedule |

______________________________________________________________________

### update-action-pins-scheduled.yml

**Purpose**: Automatically update action SHA pins.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | Schedule (weekly) |

______________________________________________________________________

## AI & Code Intelligence

### claude.yml

**Purpose**: Claude AI integration.

| Property     | Value                 |
| ------------ | --------------------- |
| **Triggers** | PR, workflow_dispatch |

______________________________________________________________________

### claude-code-review.yml

**Purpose**: AI-powered code review with Claude.

| Property     | Value                 |
| ------------ | --------------------- |
| **Triggers** | PR                    |
| **Action**   | Posts review comments |

______________________________________________________________________

### gemini-triage.yml

**Purpose**: Issue triage with Gemini.

| Property     | Value         |
| ------------ | ------------- |
| **Triggers** | Issues opened |

______________________________________________________________________

### gemini-review.yml

**Purpose**: Code review with Gemini.

| Property     | Value |
| ------------ | ----- |
| **Triggers** | PR    |

______________________________________________________________________

### gemini-scheduled-triage.yml

**Purpose**: Scheduled issue triage with Gemini.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

### gemini-dispatch.yml / gemini-invoke.yml

**Purpose**: Gemini dispatch and invocation.

| Property     | Value                                  |
| ------------ | -------------------------------------- |
| **Triggers** | workflow_dispatch, repository_dispatch |

______________________________________________________________________

### openai-workflow.yml

**Purpose**: OpenAI integration.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### grok-workflow.yml

**Purpose**: Grok AI integration.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### perplexity-workflow.yml

**Purpose**: Perplexity AI integration.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### jules.yml

**Purpose**: Jules AI agent automation.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### orchestrator.yml

**Purpose**: Multi-AI workflow orchestration.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### process-queue.yml

**Purpose**: Async task processing queue.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | schedule, workflow_dispatch |

______________________________________________________________________

## Metrics & Reporting

### metrics-collection.yml

**Purpose**: Collect repository metrics.

| Property     | Value            |
| ------------ | ---------------- |
| **Triggers** | Schedule (daily) |

______________________________________________________________________

### metrics-dashboard.yml

**Purpose**: Generate metrics dashboard.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | Schedule, workflow_dispatch |

______________________________________________________________________

### repo-metrics.yml

**Purpose**: Repository statistics.

| Property     | Value              |
| ------------ | ------------------ |
| **Triggers** | Schedule (monthly) |

______________________________________________________________________

### workflow-metrics.yml

**Purpose**: Workflow performance metrics.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

### commit-tracking.yml

**Purpose**: Track and validate commits.

| Property     | Value |
| ------------ | ----- |
| **Triggers** | Push  |

______________________________________________________________________

### weekly-commit-report.yml

**Purpose**: Weekly activity report.

| Property     | Value                        |
| ------------ | ---------------------------- |
| **Triggers** | Schedule (Monday)            |
| **Output**   | `reports/commit-report-*.md` |

______________________________________________________________________

### performance-benchmark.yml

**Purpose**: Performance regression detection.

| Property     | Value        |
| ------------ | ------------ |
| **Triggers** | PR, schedule |

______________________________________________________________________

### mutation-testing.yml

**Purpose**: Test effectiveness validation.

| Property     | Value                 |
| ------------ | --------------------- |
| **Triggers** | PR, workflow_dispatch |

______________________________________________________________________

### accessibility-testing.yml

**Purpose**: WCAG 2.1 compliance validation.

| Property     | Value        |
| ------------ | ------------ |
| **Triggers** | PR, schedule |

______________________________________________________________________

## Release & Deployment

### release.yml

**Purpose**: Release automation.

| Property     | Value                             |
| ------------ | --------------------------------- |
| **Triggers** | Tag push (v\*), workflow_dispatch |
| **Actions**  | Changelog, GitHub release         |

______________________________________________________________________

### semantic-release.yml

**Purpose**: Semantic versioning automation.

| Property     | Value                            |
| ------------ | -------------------------------- |
| **Triggers** | Push to main                     |
| **Actions**  | Version bump, changelog, release |

______________________________________________________________________

### version-bump.yml

**Purpose**: Manual version bumping.

| Property     | Value                         |
| ------------ | ----------------------------- |
| **Triggers** | workflow_dispatch             |
| **Inputs**   | bump_type (major/minor/patch) |

______________________________________________________________________

### deployment.yml

**Purpose**: Deployment orchestration.

| Property     | Value                           |
| ------------ | ------------------------------- |
| **Triggers** | Push to main, workflow_dispatch |

______________________________________________________________________

### demo-deployment.yml

**Purpose**: Deploy demo environment.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### docker-build-push.yml

**Purpose**: Build and push Docker images.

| Property     | Value         |
| ------------ | ------------- |
| **Triggers** | Push, release |

______________________________________________________________________

### deploy-to-pages-live.yml

**Purpose**: Deploy to GitHub Pages.

| Property     | Value        |
| ------------ | ------------ |
| **Triggers** | Push to main |

______________________________________________________________________

### pages.yml / build-pages-site.yml

**Purpose**: Build Jekyll site for GitHub Pages.

| Property     | Value                   |
| ------------ | ----------------------- |
| **Triggers** | Push, workflow_dispatch |

______________________________________________________________________

### generate-pages-index.yml

**Purpose**: Generate index for Pages.

| Property     | Value |
| ------------ | ----- |
| **Triggers** | Push  |

______________________________________________________________________

### sentry-release.yml

**Purpose**: Create Sentry releases.

| Property     | Value   |
| ------------ | ------- |
| **Triggers** | Release |

______________________________________________________________________

## Maintenance & Cleanup

### nightly-cleanup.yml

**Purpose**: Nightly maintenance tasks.

| Property     | Value              |
| ------------ | ------------------ |
| **Triggers** | Schedule (nightly) |

______________________________________________________________________

### branch-cleanup-notify.yml

**Purpose**: Notify about stale branches.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

### branch-lifecycle.yml / branch-lifecycle-management.yml

**Purpose**: Manage branch lifecycle.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | Schedule, workflow_dispatch |

______________________________________________________________________

### proactive-maintenance.yml

**Purpose**: Proactive maintenance tasks.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

### self-healing.yml

**Purpose**: Self-healing automation.

| Property     | Value                     |
| ------------ | ------------------------- |
| **Triggers** | workflow_run (on failure) |

______________________________________________________________________

### health-check.yml / health-check-live-apps.yml

**Purpose**: System health checks.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | Schedule, workflow_dispatch |

______________________________________________________________________

### link-checker.yml

**Purpose**: Validate markdown links.

| Property     | Value                 |
| ------------ | --------------------- |
| **Triggers** | PR, schedule (weekly) |

______________________________________________________________________

### label-sync.yml

**Purpose**: Sync labels across repos.

| Property     | Value                   |
| ------------ | ----------------------- |
| **Triggers** | Push, workflow_dispatch |

______________________________________________________________________

### manual-reset.yml

**Purpose**: Manual system reset.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |
| **Inputs**   | scope, confirm    |

______________________________________________________________________

### reset-quotas.yml

**Purpose**: Reset API quotas.

| Property     | Value                       |
| ------------ | --------------------------- |
| **Triggers** | Schedule, workflow_dispatch |

______________________________________________________________________

## Reusable Workflows

Located in `.github/workflows/reusable/`:

### python-setup-test.yml

**Purpose**: Reusable Python setup and testing.

| Input               | Type    | Default            | Description                         |
| ------------------- | ------- | ------------------ | ----------------------------------- |
| `python-version`    | string  | ''                 | Python version (falls back to vars) |
| `requirements-file` | string  | 'requirements.txt' | Requirements file path              |
| `run-tests`         | boolean | true               | Whether to run tests                |
| `test-command`      | string  | 'pytest --cov'     | Test command                        |
| `install-dev-deps`  | boolean | false              | Install dev dependencies            |

**Outputs**: `coverage-report-path`, `test-results-path`

______________________________________________________________________

### nodejs-setup-build.yml

**Purpose**: Reusable Node.js setup and build.

| Input          | Type    | Default | Description          |
| -------------- | ------- | ------- | -------------------- |
| `node-version` | string  | ''      | Node.js version      |
| `cache`        | string  | 'npm'   | Cache type           |
| `run-build`    | boolean | true    | Whether to run build |

______________________________________________________________________

### security-scanning.yml

**Purpose**: Reusable security scanning.

| Input              | Type   | Default | Description            |
| ------------------ | ------ | ------- | ---------------------- |
| `scan-type`        | string | 'full'  | Scan type (full/quick) |
| `fail-on-severity` | string | 'high'  | Fail threshold         |

______________________________________________________________________

### docker-build-push.yml

**Purpose**: Reusable Docker build and push.

| Input        | Type    | Default  | Description     |
| ------------ | ------- | -------- | --------------- |
| `image-name` | string  | required | Image name      |
| `push`       | boolean | false    | Whether to push |
| `tags`       | string  | 'latest' | Image tags      |

______________________________________________________________________

### artifact-management.yml

**Purpose**: Reusable artifact handling.

| Input            | Type   | Default  | Description      |
| ---------------- | ------ | -------- | ---------------- |
| `artifact-name`  | string | required | Artifact name    |
| `path`           | string | required | Artifact path    |
| `retention-days` | number | 30       | Retention period |

______________________________________________________________________

### github-cli-pr-ops.yml

**Purpose**: Reusable PR operations via CLI.

| Input       | Type   | Default  | Description    |
| ----------- | ------ | -------- | -------------- |
| `operation` | string | required | Operation type |
| `pr-number` | number | required | PR number      |

______________________________________________________________________

## Safeguard Workflows

### safeguard-5-secret-scanning.yml

**Purpose**: Secret scanning safeguard.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Push, PR |

______________________________________________________________________

### safeguard-6-admin-approval.yml

**Purpose**: Require admin approval for sensitive operations.

| Property     | Value             |
| ------------ | ----------------- |
| **Triggers** | workflow_dispatch |

______________________________________________________________________

### safeguard-7-staggered-scheduling.yml

**Purpose**: Staggered workflow scheduling.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

### safeguard-8-usage-monitoring.yml

**Purpose**: Monitor workflow usage.

| Property     | Value    |
| ------------ | -------- |
| **Triggers** | Schedule |

______________________________________________________________________

## Additional Workflows

### Organization Management

| Workflow                              | Purpose                           |
| ------------------------------------- | --------------------------------- |
| `org-health-crawler.yml`              | Crawl org repos for health status |
| `org-walkthrough-generator.yml`       | Generate org walkthrough          |
| `org-wide-workflow-dispatch.yml`      | Dispatch workflows org-wide       |
| `repository-bootstrap.yml`            | Bootstrap new repositories        |
| `repository-structure-validation.yml` | Validate repo structure           |

### Notifications

| Workflow                        | Purpose                      |
| ------------------------------- | ---------------------------- |
| `alert-on-workflow-failure.yml` | Alert on failures            |
| `email-digest.yml`              | Email activity digest        |
| `slack-daily-summary.yml`       | Slack daily summary          |
| `test-slack-notifications.yml`  | Test Slack integration       |
| `incident-response.yml`         | Incident response automation |

### Version Management

| Workflow                          | Purpose                     |
| --------------------------------- | --------------------------- |
| `update-python-version.yml`       | Update Python version       |
| `update-nodejs-version.yml`       | Update Node.js version      |
| `version-control-standards.yml`   | Enforce version standards   |
| `version-update-orchestrator.yml` | Orchestrate version updates |
| `commitizen-bump.yml`             | Commitizen version bump     |

### Validation

| Workflow                        | Purpose                       |
| ------------------------------- | ----------------------------- |
| `validate-quality.yml`          | Quality validation            |
| `validate-workspace-config.yml` | Workspace config validation   |
| `validate-functioncalled.yml`   | Function call validation      |
| `schema-org-validation.yml`     | Schema.org validation         |
| `chatmode-frontmatter.yml`      | Validate chatmode frontmatter |

______________________________________________________________________

## Workflow Statistics

| Category               | Count |
| ---------------------- | ----- |
| CI/CD                  | 5     |
| PR Automation          | 17    |
| Issue Management       | 6     |
| Security & Compliance  | 9     |
| AI & Code Intelligence | 13    |
| Metrics & Reporting    | 10    |
| Release & Deployment   | 12    |
| Maintenance & Cleanup  | 14    |
| Reusable               | 6     |
| Safeguards             | 4     |
| Other                  | 30+   |

______________________________________________________________________

## Next Steps

- **[Workflow Guide](../guides/WORKFLOWS.md)** - Patterns and troubleshooting
- **[Configuration Guide](../getting-started/CONFIGURATION.md)** - Configure
  workflows
- **[Architecture Overview](../architecture/OVERVIEW.md)** - System design
