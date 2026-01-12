# 🎯 Organization Ecosystem Dashboard

![Health](https://img.shields.io/badge/health-42%25_fair-yellow)

**Last Updated**: December 30, 2025 at 02:37 AM
**Organization**:

---

## 📋 Table of Contents

- [Quick Stats](#-quick-stats)
- [Repository Health](#-repository-health)
- [Link Health](#-link-health)
- [Alerts](#-alerts)
- [Ecosystem Map](#-ecosystem-map)
- [Technology Coverage](#-technology-coverage)
- [Active Workflows](#-active-workflows)

---

## 📊 Quick Stats

| Category | Count |
|----------|-------|
| ⚡ GitHub Actions Workflows | 90 |
| 🤖 Copilot Agents | 26 |
| 📝 Copilot Instructions | 110 |
| 💬 Copilot Prompts | 119 |
| 🎭 Copilot Chat Modes | 88 |
| 🛠️  Technologies Supported | 110 |

[⬆️ Back to Top](#organization-ecosystem-dashboard)

## 🏥 Repository Health

⚠️ **Data Unavailable**: No GitHub token provided

[⬆️ Back to Top](#organization-ecosystem-dashboard)

## 🔗 Link Health

ℹ️ **No Data**: External link validation was skipped or found no links.

[⬆️ Back to Top](#organization-ecosystem-dashboard)

## ⚠️  Alerts

✅ No alerts found! The ecosystem is healthy.

[⬆️ Back to Top](#organization-ecosystem-dashboard)


## 🗺️  Ecosystem Map

ℹ️  *The diagram below displays the first 10 workflows for readability. All 90 workflows are listed in the [Active Workflows](#-active-workflows) section.*

```mermaid
graph TD
    %% Styles
    classDef org fill:#0969da,stroke:#0969da,color:#fff,stroke-width:2px;
    classDef workflow fill:#8250df,stroke:#54aeff,color:#fff,stroke-width:1px;
    classDef agent fill:#1a7f37,stroke:#d4a72c,color:#fff,stroke-width:1px;
    classDef tech fill:#57606a,stroke:#4ac26b,color:#fff,stroke-width:1px;

    subgraph "GitHub Organization"
        ORG[Organization Root]:::org
    end

    subgraph "Automation Layer"
        WF0[pr-suggestion-implementation.yml]:::workflow
        click WF0 "../.github/workflows/pr-suggestion-implementation.yml" "View Workflow"
        ORG --> WF0
        WF1[safeguard-7-staggered-scheduling.yml]:::workflow
        click WF1 "../.github/workflows/safeguard-7-staggered-scheduling.yml" "View Workflow"
        ORG --> WF1
        WF2[scan-for-secrets.yml]:::workflow
        click WF2 "../.github/workflows/scan-for-secrets.yml" "View Workflow"
        ORG --> WF2
        WF3[build-pages-site.yml]:::workflow
        click WF3 "../.github/workflows/build-pages-site.yml" "View Workflow"
        ORG --> WF3
        WF4[grok_workflow.yml]:::workflow
        click WF4 "../.github/workflows/grok_workflow.yml" "View Workflow"
        ORG --> WF4
        WF5[project-automation.yml]:::workflow
        click WF5 "../.github/workflows/project-automation.yml" "View Workflow"
        ORG --> WF5
        WF6[reusable-security-scan.yml]:::workflow
        click WF6 "../.github/workflows/reusable-security-scan.yml" "View Workflow"
        ORG --> WF6
        WF7[alert-on-workflow-failure.yml]:::workflow
        click WF7 "../.github/workflows/alert-on-workflow-failure.yml" "View Workflow"
        ORG --> WF7
        WF8[weekly-commit-report.yml]:::workflow
        click WF8 "../.github/workflows/weekly-commit-report.yml" "View Workflow"
        ORG --> WF8
        WF9[safeguard-8-usage-monitoring.yml]:::workflow
        click WF9 "../.github/workflows/safeguard-8-usage-monitoring.yml" "View Workflow"
        ORG --> WF9
    end

    subgraph "GitHub Copilot Customizations"
        AGENTS[Agents]:::agent
        AGENTS_COUNT[26 agents]:::agent
        AGENTS --> AGENTS_COUNT
        ORG --> AGENTS
        INSTR[Instructions]:::agent
        INSTR_COUNT[110 instructions]:::agent
        INSTR --> INSTR_COUNT
        ORG --> INSTR
        PROMPTS[Prompts]:::agent
        PROMPTS_COUNT[119 prompts]:::agent
        PROMPTS --> PROMPTS_COUNT
        ORG --> PROMPTS
        CHATMODES[Chat Modes]:::agent
        CHATMODES_COUNT[88 modes]:::agent
        CHATMODES --> CHATMODES_COUNT
        ORG --> CHATMODES
    end

    subgraph "Technologies"
        TECH0[a11y]:::tech
        TECH1[ai-prompt-engineering-safety-best-practices]:::tech
        TECH2[angular]:::tech
        TECH3[ansible]:::tech
        TECH4[aspnet-rest-apis]:::tech
        TECH5[astro]:::tech
        TECH6[azure-devops-pipelines]:::tech
        TECH7[azure-functions-typescript]:::tech
        TECH8[azure-logic-apps-power-automate]:::tech
        TECH9[azure-verified-modules-terraform]:::tech
        TECH10[bicep-code-best-practices]:::tech
        TECH11[blazor]:::tech
        TECH12[clojure]:::tech
        TECH13[cmake-vcpkg]:::tech
        TECH14[codexer]:::tech
    end
```

**Legend:** 🔵 Organization | 🟣 Workflow | 🟢 AI Agent | 🔘 Technology

[⬆️ Back to Top](#organization-ecosystem-dashboard)

## 🛠️  Technology Coverage

Supported languages and frameworks:

<details>
<summary>View all 110 technologies</summary>

| `a11y` | `ai-prompt-engineering-safety-best-practices` | `angular` | `ansible` |
| --- | --- | --- | --- |
| `aspnet-rest-apis` | `astro` | `azure-devops-pipelines` | `azure-functions-typescript` |
| `azure-logic-apps-power-automate` | `azure-verified-modules-terraform` | `bicep-code-best-practices` | `blazor` |
| `clojure` | `cmake-vcpkg` | `codexer` | `coldfusion-cfc` |
| `coldfusion-cfm` | `collections` | `containerization-docker-best-practices` | `convert-jpa-to-spring-data-cosmos` |
| `copilot-thought-logging` | `csharp` | `csharp-ja` | `csharp-ko` |
| `csharp-mcp-server` | `dart-n-flutter` | `declarative-agents-microsoft365` | `devbox-image-definition` |
| `devops-core-principles` | `dotnet-architecture-good-practices` | `dotnet-framework` | `dotnet-maui` |
| `dotnet-upgrade` | `dotnet-wpf` | `genaiscript` | `generate-modern-terraform-code-for-azure` |
| `gilfoyle-code-review` | `github-actions-ci-cd-best-practices` | `go` | `go-mcp-server` |
| `instructions` | `java` | `java-11-to-java-17-upgrade` | `java-17-to-java-21-upgrade` |
| `java-21-to-java-25-upgrade` | `java-mcp-server` | `joyride-user-project` | `joyride-workspace-automation` |
| `kotlin-mcp-server` | `kubernetes-deployment-best-practices` | `langchain-python` | `localization` |
| `markdown` | `memory-bank` | `mongo-dba` | `ms-sql-dba` |
| `nestjs` | `nextjs` | `nextjs-tailwind` | `nodejs-javascript-vitest` |
| `object-calisthenics` | `oqtane` | `performance-optimization` | `php-mcp-server` |
| `playwright-python` | `playwright-typescript` | `power-apps-canvas-yaml` | `power-apps-code-apps` |
| `power-bi-custom-visuals-development` | `power-bi-data-modeling-best-practices` | `power-bi-dax-best-practices` | `power-bi-devops-alm-best-practices` |
| `power-bi-report-design-best-practices` | `power-bi-security-rls-best-practices` | `power-platform-connector` | `power-platform-mcp-development` |
| `powershell` | `powershell-pester-5` | `prompt` | `python` |
| `python-mcp-server` | `quarkus` | `quarkus-mcp-server-sse` | `r` |
| `reactjs` | `ruby-mcp-server` | `ruby-on-rails` | `rust` |
| `rust-mcp-server` | `security-and-owasp` | `self-explanatory-code-commenting` | `shell` |
| `spec-driven-workflow-v1` | `springboot` | `sql-sp-generation` | `svelte` |
| `swift-mcp-server` | `taming-copilot` | `tanstack-start-shadcn-tailwind` | `task-implementation` |
| `tasksync` | `terraform` | `terraform-azure` | `terraform-sap-btp` |
| `typescript-5-es2022` | `typescript-mcp-server` | `update-code-from-shorthand` | `version-control-standards` |
| `vuejs3` | `wordpress` |  |  |

</details>

[⬆️ Back to Top](#organization-ecosystem-dashboard)

## ⚙️  Active Workflows

> **Legend:** 🛡️ Safeguard · 🔐 Security · ♻️ Reusable · 🤖 AI Agent · 🚀 CI/CD · 🔀 PR Mgmt · ⏱️ Scheduled · 💓 Health · ⚙️ General

**Legend:**
🛡️ Safeguards | 🔐 Security | ♻️ Reusable | 🤖 AI Agents | 🚀 CI/CD | 🔀 PR Management | ⏱️ Scheduled | 💓 Health/Metrics | ⚙️ General

<details>
<summary>View all 90 workflows</summary>

> **Legend:** 🛡️ Safeguards & Policies | 🔐 Security | ♻️ Reusable Workflows | 🤖 AI Agents & Automation | 🚀 CI/CD & Deployment | 🔀 PR Management | ⏱️ Scheduled Tasks | 💓 Health & Metrics | ⚙️ Utility & Other

| # | Type | Workflow | Action |
|---|---|---|---|
| 1 | 🚀 | `accessibility-testing.yml` | [View](../.github/workflows/accessibility-testing.yml) |
| 2 | 💓 | `admin-approval-dashboard.yml` | [View](../.github/workflows/admin-approval-dashboard.yml) |
| 3 | 🤖 | `agentsphere-deployment.yml` | [View](../.github/workflows/agentsphere-deployment.yml) |
| 4 | ⚙️ | `alert-on-workflow-failure.yml` | [View](../.github/workflows/alert-on-workflow-failure.yml) |
| 5 | ⚙️ | `auto-assign.yml` | [View](../.github/workflows/auto-assign.yml) |
| 6 | 🔀 | `auto-enable-merge.yml` | [View](../.github/workflows/auto-enable-merge.yml) |
| 7 | ⚙️ | `auto-labeler.yml` | [View](../.github/workflows/auto-labeler.yml) |
| 8 | 🔀 | `auto-merge.yml` | [View](../.github/workflows/auto-merge.yml) |
| 9 | 🔀 | `auto-pr-create.yml` | [View](../.github/workflows/auto-pr-create.yml) |
| 10 | ⚙️ | `badge-management.yml` | [View](../.github/workflows/badge-management.yml) |
| 11 | 🔀 | `batch-pr-lifecycle.yml` | [View](../.github/workflows/batch-pr-lifecycle.yml) |
| 12 | ⚙️ | `bio-description-completions.yml` | [View](../.github/workflows/bio-description-completions.yml) |
| 13 | ⚙️ | `branch-cleanup-notify.yml` | [View](../.github/workflows/branch-cleanup-notify.yml) |
| 14 | ⚙️ | `branch-lifecycle-management.yml` | [View](../.github/workflows/branch-lifecycle-management.yml) |
| 15 | ⚙️ | `branch-lifecycle.yml` | [View](../.github/workflows/branch-lifecycle.yml) |
| 16 | 🚀 | `build-pages-site.yml` | [View](../.github/workflows/build-pages-site.yml) |
| 17 | 🚀 | `ci-advanced.yml` | [View](../.github/workflows/ci-advanced.yml) |
| 18 | 🚀 | `ci.yml` | [View](../.github/workflows/ci.yml) |
| 19 | 🤖 | `claude-code-review.yml` | [View](../.github/workflows/claude-code-review.yml) |
| 20 | 🤖 | `claude.yml` | [View](../.github/workflows/claude.yml) |
| 21 | ⚙️ | `code-coverage.yml` | [View](../.github/workflows/code-coverage.yml) |
| 22 | 🔐 | `codeql-analysis.yml` | [View](../.github/workflows/codeql-analysis.yml) |
| 23 | 🚀 | `collect-deployment-metadata.yml` | [View](../.github/workflows/collect-deployment-metadata.yml) |
| 24 | ⚙️ | `combine-prs.yml` | [View](../.github/workflows/combine-prs.yml) |
| 25 | ⚙️ | `commit-tracking.yml` | [View](../.github/workflows/commit-tracking.yml) |
| 26 | 💓 | `community-health.yml` | [View](../.github/workflows/community-health.yml) |
| 27 | ⚙️ | `create-organizational-content.yml` | [View](../.github/workflows/create-organizational-content.yml) |
| 28 | ⚙️ | `dependency-review.yml` | [View](../.github/workflows/dependency-review.yml) |
| 29 | 🚀 | `deploy-to-pages-live.yml` | [View](../.github/workflows/deploy-to-pages-live.yml) |
| 30 | 🚀 | `deployment.yml` | [View](../.github/workflows/deployment.yml) |
| 31 | 🚀 | `docker-build-push.yml` | [View](../.github/workflows/docker-build-push.yml) |
| 32 | ⚙️ | `draft-to-ready-automation.yml` | [View](../.github/workflows/draft-to-ready-automation.yml) |
| 33 | 🤖 | `gemini-dispatch.yml` | [View](../.github/workflows/gemini-dispatch.yml) |
| 34 | 🤖 | `gemini-invoke.yml` | [View](../.github/workflows/gemini-invoke.yml) |
| 35 | 🤖 | `gemini-review.yml` | [View](../.github/workflows/gemini-review.yml) |
| 36 | 🤖 | `gemini-scheduled-triage.yml` | [View](../.github/workflows/gemini-scheduled-triage.yml) |
| 37 | 🤖 | `gemini-triage.yml` | [View](../.github/workflows/gemini-triage.yml) |
| 38 | 🤖 | `gemini_workflow.yml` | [View](../.github/workflows/gemini_workflow.yml) |
| 39 | ⚙️ | `generate-pages-index.yml` | [View](../.github/workflows/generate-pages-index.yml) |
| 40 | ⚙️ | `generate-walkthrough.yml` | [View](../.github/workflows/generate-walkthrough.yml) |
| 41 | 🤖 | `grok_workflow.yml` | [View](../.github/workflows/grok_workflow.yml) |
| 42 | 💓 | `health-check-live-apps.yml` | [View](../.github/workflows/health-check-live-apps.yml) |
| 43 | 💓 | `health-check.yml` | [View](../.github/workflows/health-check.yml) |
| 44 | 🤖 | `jules.yml` | [View](../.github/workflows/jules.yml) |
| 45 | 💓 | `link-checker.yml` | [View](../.github/workflows/link-checker.yml) |
| 46 | ⚙️ | `manual_reset.yml` | [View](../.github/workflows/manual_reset.yml) |
| 47 | 💓 | `metrics-collection.yml` | [View](../.github/workflows/metrics-collection.yml) |
| 48 | 💓 | `metrics-dashboard.yml` | [View](../.github/workflows/metrics-dashboard.yml) |
| 49 | 🚀 | `mutation-testing.yml` | [View](../.github/workflows/mutation-testing.yml) |
| 50 | 🤖 | `openai_workflow.yml` | [View](../.github/workflows/openai_workflow.yml) |
| 51 | ⚙️ | `orchestrator.yml` | [View](../.github/workflows/orchestrator.yml) |
| 52 | 💓 | `org-health-crawler.yml` | [View](../.github/workflows/org-health-crawler.yml) |
| 53 | ⚙️ | `org-walkthrough-generator.yml` | [View](../.github/workflows/org-walkthrough-generator.yml) |
| 54 | ⚙️ | `org-wide-workflow-dispatch.yml` | [View](../.github/workflows/org-wide-workflow-dispatch.yml) |
| 55 | ⚙️ | `performance-benchmark.yml` | [View](../.github/workflows/performance-benchmark.yml) |
| 56 | 🤖 | `perplexity_workflow.yml` | [View](../.github/workflows/perplexity_workflow.yml) |
| 57 | 🔀 | `pr-batch-merge.yml` | [View](../.github/workflows/pr-batch-merge.yml) |
| 58 | 🔀 | `pr-consolidation.yml` | [View](../.github/workflows/pr-consolidation.yml) |
| 59 | 🔀 | `pr-quality-checks.yml` | [View](../.github/workflows/pr-quality-checks.yml) |
| 60 | 🔀 | `pr-suggestion-implementation.yml` | [View](../.github/workflows/pr-suggestion-implementation.yml) |
| 61 | 🔀 | `pr-task-catcher.yml` | [View](../.github/workflows/pr-task-catcher.yml) |
| 62 | ⚙️ | `process_queue.yml` | [View](../.github/workflows/process_queue.yml) |
| 63 | ⚙️ | `project-automation.yml` | [View](../.github/workflows/project-automation.yml) |
| 64 | 🚀 | `reconcile-deployments.yml` | [View](../.github/workflows/reconcile-deployments.yml) |
| 65 | 🚀 | `release.yml` | [View](../.github/workflows/release.yml) |
| 66 | 💓 | `repo-metrics.yml` | [View](../.github/workflows/repo-metrics.yml) |
| 67 | ⚙️ | `repository-bootstrap.yml` | [View](../.github/workflows/repository-bootstrap.yml) |
| 68 | ⚙️ | `reset_quotas.yml` | [View](../.github/workflows/reset_quotas.yml) |
| 69 | ♻️ | `reusable-api-retry.yml` | [View](../.github/workflows/reusable-api-retry.yml) |
| 70 | ♻️ | `reusable-app-detect.yml` | [View](../.github/workflows/reusable-app-detect.yml) |
| 71 | ♻️ | `reusable-notify.yml` | [View](../.github/workflows/reusable-notify.yml) |
| 72 | 🔐 | `reusable-security-scan.yml` | [View](../.github/workflows/reusable-security-scan.yml) |
| 73 | 🛡️ | `safeguard-5-secret-scanning.yml` | [View](../.github/workflows/safeguard-5-secret-scanning.yml) |
| 74 | 🛡️ | `safeguard-6-admin-approval.yml` | [View](../.github/workflows/safeguard-6-admin-approval.yml) |
| 75 | 🛡️ | `safeguard-7-staggered-scheduling.yml` | [View](../.github/workflows/safeguard-7-staggered-scheduling.yml) |
| 76 | 🛡️ | `safeguard-8-usage-monitoring.yml` | [View](../.github/workflows/safeguard-8-usage-monitoring.yml) |
| 77 | ⚙️ | `sbom-generation.yml` | [View](../.github/workflows/sbom-generation.yml) |
| 78 | 🔐 | `scan-for-secrets.yml` | [View](../.github/workflows/scan-for-secrets.yml) |
| 79 | ⏱️ | `scheduled-walkthrough-generator.yml` | [View](../.github/workflows/scheduled-walkthrough-generator.yml) |
| 80 | 🔐 | `security-scan.yml` | [View](../.github/workflows/security-scan.yml) |
| 81 | 🚀 | `semantic-release.yml` | [View](../.github/workflows/semantic-release.yml) |
| 82 | 🔐 | `semgrep.yml` | [View](../.github/workflows/semgrep.yml) |
| 83 | ⚙️ | `staggered-scheduling.yml` | [View](../.github/workflows/staggered-scheduling.yml) |
| 84 | ⚙️ | `task-extraction.yml` | [View](../.github/workflows/task-extraction.yml) |
| 85 | 💓 | `usage-monitoring.yml` | [View](../.github/workflows/usage-monitoring.yml) |
| 86 | ⚙️ | `validate-quality.yml` | [View](../.github/workflows/validate-quality.yml) |
| 87 | ⚙️ | `version-bump.yml` | [View](../.github/workflows/version-bump.yml) |
| 88 | ⚙️ | `version-control-standards.yml` | [View](../.github/workflows/version-control-standards.yml) |
| 89 | ⏱️ | `weekly-commit-report.yml` | [View](../.github/workflows/weekly-commit-report.yml) |
| 90 | ⚙️ | `welcome.yml` | [View](../.github/workflows/welcome.yml) |

</details>
### 🛡️ Safeguards & Policies

| Workflow | Action |
|---|---|
| `safeguard-5-secret-scanning.yml` | [View](../.github/workflows/safeguard-5-secret-scanning.yml) |
| `safeguard-6-admin-approval.yml` | [View](../.github/workflows/safeguard-6-admin-approval.yml) |
| `safeguard-7-staggered-scheduling.yml` | [View](../.github/workflows/safeguard-7-staggered-scheduling.yml) |
| `safeguard-8-usage-monitoring.yml` | [View](../.github/workflows/safeguard-8-usage-monitoring.yml) |

### 🔐 Security

| Workflow | Action |
|---|---|
| `codeql-analysis.yml` | [View](../.github/workflows/codeql-analysis.yml) |
| `reusable-security-scan.yml` | [View](../.github/workflows/reusable-security-scan.yml) |
| `scan-for-secrets.yml` | [View](../.github/workflows/scan-for-secrets.yml) |
| `security-scan.yml` | [View](../.github/workflows/security-scan.yml) |
| `semgrep.yml` | [View](../.github/workflows/semgrep.yml) |

### ♻️ Reusable Workflows

| Workflow | Action |
|---|---|
| `reusable-api-retry.yml` | [View](../.github/workflows/reusable-api-retry.yml) |
| `reusable-app-detect.yml` | [View](../.github/workflows/reusable-app-detect.yml) |
| `reusable-notify.yml` | [View](../.github/workflows/reusable-notify.yml) |

### 🤖 AI Agents & Automation

| Workflow | Action |
|---|---|
| `agentsphere-deployment.yml` | [View](../.github/workflows/agentsphere-deployment.yml) |
| `claude-code-review.yml` | [View](../.github/workflows/claude-code-review.yml) |
| `claude.yml` | [View](../.github/workflows/claude.yml) |
| `gemini-dispatch.yml` | [View](../.github/workflows/gemini-dispatch.yml) |
| `gemini-invoke.yml` | [View](../.github/workflows/gemini-invoke.yml) |
| `gemini-review.yml` | [View](../.github/workflows/gemini-review.yml) |
| `gemini-scheduled-triage.yml` | [View](../.github/workflows/gemini-scheduled-triage.yml) |
| `gemini-triage.yml` | [View](../.github/workflows/gemini-triage.yml) |
| `gemini_workflow.yml` | [View](../.github/workflows/gemini_workflow.yml) |
| `grok_workflow.yml` | [View](../.github/workflows/grok_workflow.yml) |
| `jules.yml` | [View](../.github/workflows/jules.yml) |
| `openai_workflow.yml` | [View](../.github/workflows/openai_workflow.yml) |
| `perplexity_workflow.yml` | [View](../.github/workflows/perplexity_workflow.yml) |

### 🚀 CI/CD & Deployment

| Workflow | Action |
|---|---|
| `accessibility-testing.yml` | [View](../.github/workflows/accessibility-testing.yml) |
| `build-pages-site.yml` | [View](../.github/workflows/build-pages-site.yml) |
| `ci-advanced.yml` | [View](../.github/workflows/ci-advanced.yml) |
| `ci.yml` | [View](../.github/workflows/ci.yml) |
| `collect-deployment-metadata.yml` | [View](../.github/workflows/collect-deployment-metadata.yml) |
| `deploy-to-pages-live.yml` | [View](../.github/workflows/deploy-to-pages-live.yml) |
| `deployment.yml` | [View](../.github/workflows/deployment.yml) |
| `docker-build-push.yml` | [View](../.github/workflows/docker-build-push.yml) |
| `mutation-testing.yml` | [View](../.github/workflows/mutation-testing.yml) |
| `reconcile-deployments.yml` | [View](../.github/workflows/reconcile-deployments.yml) |
| `release.yml` | [View](../.github/workflows/release.yml) |
| `semantic-release.yml` | [View](../.github/workflows/semantic-release.yml) |

### 🔀 PR Management

| Workflow | Action |
|---|---|
| `auto-enable-merge.yml` | [View](../.github/workflows/auto-enable-merge.yml) |
| `auto-merge.yml` | [View](../.github/workflows/auto-merge.yml) |
| `auto-pr-create.yml` | [View](../.github/workflows/auto-pr-create.yml) |
| `batch-pr-lifecycle.yml` | [View](../.github/workflows/batch-pr-lifecycle.yml) |
| `pr-batch-merge.yml` | [View](../.github/workflows/pr-batch-merge.yml) |
| `pr-consolidation.yml` | [View](../.github/workflows/pr-consolidation.yml) |
| `pr-quality-checks.yml` | [View](../.github/workflows/pr-quality-checks.yml) |
| `pr-suggestion-implementation.yml` | [View](../.github/workflows/pr-suggestion-implementation.yml) |
| `pr-task-catcher.yml` | [View](../.github/workflows/pr-task-catcher.yml) |

### ⏱️ Scheduled Tasks

| Workflow | Action |
|---|---|
| `scheduled-walkthrough-generator.yml` | [View](../.github/workflows/scheduled-walkthrough-generator.yml) |
| `weekly-commit-report.yml` | [View](../.github/workflows/weekly-commit-report.yml) |

### 💓 Health & Metrics

| Workflow | Action |
|---|---|
| `admin-approval-dashboard.yml` | [View](../.github/workflows/admin-approval-dashboard.yml) |
| `community-health.yml` | [View](../.github/workflows/community-health.yml) |
| `health-check-live-apps.yml` | [View](../.github/workflows/health-check-live-apps.yml) |
| `health-check.yml` | [View](../.github/workflows/health-check.yml) |
| `link-checker.yml` | [View](../.github/workflows/link-checker.yml) |
| `metrics-collection.yml` | [View](../.github/workflows/metrics-collection.yml) |
| `metrics-dashboard.yml` | [View](../.github/workflows/metrics-dashboard.yml) |
| `org-health-crawler.yml` | [View](../.github/workflows/org-health-crawler.yml) |
| `repo-metrics.yml` | [View](../.github/workflows/repo-metrics.yml) |
| `usage-monitoring.yml` | [View](../.github/workflows/usage-monitoring.yml) |

### ⚙️ Utility & Other

| Workflow | Action |
|---|---|
| `alert-on-workflow-failure.yml` | [View](../.github/workflows/alert-on-workflow-failure.yml) |
| `auto-assign.yml` | [View](../.github/workflows/auto-assign.yml) |
| `auto-labeler.yml` | [View](../.github/workflows/auto-labeler.yml) |
| `badge-management.yml` | [View](../.github/workflows/badge-management.yml) |
| `bio-description-completions.yml` | [View](../.github/workflows/bio-description-completions.yml) |
| `branch-cleanup-notify.yml` | [View](../.github/workflows/branch-cleanup-notify.yml) |
| `branch-lifecycle-management.yml` | [View](../.github/workflows/branch-lifecycle-management.yml) |
| `branch-lifecycle.yml` | [View](../.github/workflows/branch-lifecycle.yml) |
| `code-coverage.yml` | [View](../.github/workflows/code-coverage.yml) |
| `combine-prs.yml` | [View](../.github/workflows/combine-prs.yml) |
| `commit-tracking.yml` | [View](../.github/workflows/commit-tracking.yml) |
| `create-organizational-content.yml` | [View](../.github/workflows/create-organizational-content.yml) |
| `dependency-review.yml` | [View](../.github/workflows/dependency-review.yml) |
| `draft-to-ready-automation.yml` | [View](../.github/workflows/draft-to-ready-automation.yml) |
| `generate-pages-index.yml` | [View](../.github/workflows/generate-pages-index.yml) |
| `generate-walkthrough.yml` | [View](../.github/workflows/generate-walkthrough.yml) |
| `manual_reset.yml` | [View](../.github/workflows/manual_reset.yml) |
| `orchestrator.yml` | [View](../.github/workflows/orchestrator.yml) |
| `org-walkthrough-generator.yml` | [View](../.github/workflows/org-walkthrough-generator.yml) |
| `org-wide-workflow-dispatch.yml` | [View](../.github/workflows/org-wide-workflow-dispatch.yml) |
| `performance-benchmark.yml` | [View](../.github/workflows/performance-benchmark.yml) |
| `process_queue.yml` | [View](../.github/workflows/process_queue.yml) |
| `project-automation.yml` | [View](../.github/workflows/project-automation.yml) |
| `repository-bootstrap.yml` | [View](../.github/workflows/repository-bootstrap.yml) |
| `reset_quotas.yml` | [View](../.github/workflows/reset_quotas.yml) |
| `sbom-generation.yml` | [View](../.github/workflows/sbom-generation.yml) |
| `staggered-scheduling.yml` | [View](../.github/workflows/staggered-scheduling.yml) |
| `task-extraction.yml` | [View](../.github/workflows/task-extraction.yml) |
| `validate-quality.yml` | [View](../.github/workflows/validate-quality.yml) |
| `version-bump.yml` | [View](../.github/workflows/version-bump.yml) |
| `version-control-standards.yml` | [View](../.github/workflows/version-control-standards.yml) |
| `welcome.yml` | [View](../.github/workflows/welcome.yml) |

</details>

[⬆️ Back to Top](#organization-ecosystem-dashboard)

---

*Dashboard generated by Ecosystem Visualizer*
