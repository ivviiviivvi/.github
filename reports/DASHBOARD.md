# 🎯 Organization Ecosystem Dashboard

![Health](https://img.shields.io/badge/health-31%25_poor-orange)

**Last Updated**: December 25, 2025 at 02:37 AM
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
| ⚡ GitHub Actions Workflows | 88 |
| 🤖 Copilot Agents | 25 |
| 📝 Copilot Instructions | 110 |
| 💬 Copilot Prompts | 119 |
| 🎭 Copilot Chat Modes | 88 |
| 🛠️ Technologies Supported | 110 |

[Back to Top](#organization-ecosystem-dashboard)

## 🔗 Link Health

| Status | Count | Percentage |
|--------|-------|------------|
| Valid | 125 | 5.1% |
| Broken | 1426 | 94.9% |
| **Total** | **2448** | **100%** |

<details>
<summary>View top 20 broken links (of 1426)</summary>

| URL | Status |
|---|---|
| `<invalid or redacted URL>` | 500 |
| `http://+:8080` | 404 |
| `http://localhost:3000/health` | 403 |
| `https://GUI-rs.org),` | 404 |
| `http://localhost:5000` | 403 |
| `http://localhost:PORT` | 403 |
| `http://localhost:3000/sitemap.xml` | 403 |
| `http://localhost:3000` | 403 |
| `http://localhost:PORT/mcp` | 403 |
| `http://localhost:8080/mcp/sse` | 403 |
| `http://localhost:8080/health` | 403 |
| `http://localhost:8080` | 403 |
| `http://localhost:8000/health` | 403 |
| `https://agentsphere.dev/` | 404 |
| `http://json-schema.org/draft-04/schema#` | 500 |
| `https://agentsphere.dev/example)` | 404 |
| `http://www.w3.org/2001/XMLSchema-instance` | 500 |
| `https://agentsphere.example.com/demo/your-repo)` | 404 |
| `https://agentsphere.dev/ivviiviivvi/my-app` | 404 |
| `http://maven.apache.org/POM/4.0.0` | 404 |

</details>

[Back to Top](#organization-ecosystem-dashboard)

## ⚠️  Alerts

✅ No alerts found! The ecosystem is healthy.

[Back to Top](#organization-ecosystem-dashboard)


## 🗺️  Ecosystem Map

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
        AGENTS_COUNT[25 agents]:::agent
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

[Back to Top](#organization-ecosystem-dashboard)

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

[Back to Top](#organization-ecosystem-dashboard)

## ⚙️  Active Workflows

<details>
<summary>View all 88 workflows</summary>

- [`accessibility-testing.yml`](../.github/workflows/accessibility-testing.yml)
- [`admin-approval-dashboard.yml`](../.github/workflows/admin-approval-dashboard.yml)
- [`agentsphere-deployment.yml`](../.github/workflows/agentsphere-deployment.yml)
- [`alert-on-workflow-failure.yml`](../.github/workflows/alert-on-workflow-failure.yml)
- [`auto-assign.yml`](../.github/workflows/auto-assign.yml)
- [`auto-enable-merge.yml`](../.github/workflows/auto-enable-merge.yml)
- [`auto-labeler.yml`](../.github/workflows/auto-labeler.yml)
- [`auto-merge.yml`](../.github/workflows/auto-merge.yml)
- [`auto-pr-create.yml`](../.github/workflows/auto-pr-create.yml)
- [`badge-management.yml`](../.github/workflows/badge-management.yml)
- [`batch-pr-lifecycle.yml`](../.github/workflows/batch-pr-lifecycle.yml)
- [`bio-description-completions.yml`](../.github/workflows/bio-description-completions.yml)
- [`branch-cleanup-notify.yml`](../.github/workflows/branch-cleanup-notify.yml)
- [`branch-lifecycle-management.yml`](../.github/workflows/branch-lifecycle-management.yml)
- [`branch-lifecycle.yml`](../.github/workflows/branch-lifecycle.yml)
- [`build-pages-site.yml`](../.github/workflows/build-pages-site.yml)
- [`ci-advanced.yml`](../.github/workflows/ci-advanced.yml)
- [`ci.yml`](../.github/workflows/ci.yml)
- [`claude-code-review.yml`](../.github/workflows/claude-code-review.yml)
- [`claude.yml`](../.github/workflows/claude.yml)
- [`code-coverage.yml`](../.github/workflows/code-coverage.yml)
- [`codeql-analysis.yml`](../.github/workflows/codeql-analysis.yml)
- [`collect-deployment-metadata.yml`](../.github/workflows/collect-deployment-metadata.yml)
- [`combine-prs.yml`](../.github/workflows/combine-prs.yml)
- [`commit-tracking.yml`](../.github/workflows/commit-tracking.yml)
- [`community-health.yml`](../.github/workflows/community-health.yml)
- [`dependency-review.yml`](../.github/workflows/dependency-review.yml)
- [`deploy-to-pages-live.yml`](../.github/workflows/deploy-to-pages-live.yml)
- [`deployment.yml`](../.github/workflows/deployment.yml)
- [`docker-build-push.yml`](../.github/workflows/docker-build-push.yml)
- [`draft-to-ready-automation.yml`](../.github/workflows/draft-to-ready-automation.yml)
- [`gemini-dispatch.yml`](../.github/workflows/gemini-dispatch.yml)
- [`gemini-invoke.yml`](../.github/workflows/gemini-invoke.yml)
- [`gemini-review.yml`](../.github/workflows/gemini-review.yml)
- [`gemini-scheduled-triage.yml`](../.github/workflows/gemini-scheduled-triage.yml)
- [`gemini-triage.yml`](../.github/workflows/gemini-triage.yml)
- [`gemini_workflow.yml`](../.github/workflows/gemini_workflow.yml)
- [`generate-pages-index.yml`](../.github/workflows/generate-pages-index.yml)
- [`generate-walkthrough.yml`](../.github/workflows/generate-walkthrough.yml)
- [`grok_workflow.yml`](../.github/workflows/grok_workflow.yml)
- [`health-check-live-apps.yml`](../.github/workflows/health-check-live-apps.yml)
- [`health-check.yml`](../.github/workflows/health-check.yml)
- [`jules.yml`](../.github/workflows/jules.yml)
- [`link-checker.yml`](../.github/workflows/link-checker.yml)
- [`manual_reset.yml`](../.github/workflows/manual_reset.yml)
- [`metrics-collection.yml`](../.github/workflows/metrics-collection.yml)
- [`metrics-dashboard.yml`](../.github/workflows/metrics-dashboard.yml)
- [`mutation-testing.yml`](../.github/workflows/mutation-testing.yml)
- [`openai_workflow.yml`](../.github/workflows/openai_workflow.yml)
- [`orchestrator.yml`](../.github/workflows/orchestrator.yml)
- [`org-health-crawler.yml`](../.github/workflows/org-health-crawler.yml)
- [`org-walkthrough-generator.yml`](../.github/workflows/org-walkthrough-generator.yml)
- [`org-wide-workflow-dispatch.yml`](../.github/workflows/org-wide-workflow-dispatch.yml)
- [`performance-benchmark.yml`](../.github/workflows/performance-benchmark.yml)
- [`perplexity_workflow.yml`](../.github/workflows/perplexity_workflow.yml)
- [`pr-batch-merge.yml`](../.github/workflows/pr-batch-merge.yml)
- [`pr-quality-checks.yml`](../.github/workflows/pr-quality-checks.yml)
- [`pr-suggestion-implementation.yml`](../.github/workflows/pr-suggestion-implementation.yml)
- [`pr-task-catcher.yml`](../.github/workflows/pr-task-catcher.yml)
- [`process_queue.yml`](../.github/workflows/process_queue.yml)
- [`project-automation.yml`](../.github/workflows/project-automation.yml)
- [`reconcile-deployments.yml`](../.github/workflows/reconcile-deployments.yml)
- [`release.yml`](../.github/workflows/release.yml)
- [`repo-metrics.yml`](../.github/workflows/repo-metrics.yml)
- [`repository-bootstrap.yml`](../.github/workflows/repository-bootstrap.yml)
- [`reset_quotas.yml`](../.github/workflows/reset_quotas.yml)
- [`reusable-api-retry.yml`](../.github/workflows/reusable-api-retry.yml)
- [`reusable-app-detect.yml`](../.github/workflows/reusable-app-detect.yml)
- [`reusable-notify.yml`](../.github/workflows/reusable-notify.yml)
- [`reusable-security-scan.yml`](../.github/workflows/reusable-security-scan.yml)
- [`safeguard-5-secret-scanning.yml`](../.github/workflows/safeguard-5-secret-scanning.yml)
- [`safeguard-6-admin-approval.yml`](../.github/workflows/safeguard-6-admin-approval.yml)
- [`safeguard-7-staggered-scheduling.yml`](../.github/workflows/safeguard-7-staggered-scheduling.yml)
- [`safeguard-8-usage-monitoring.yml`](../.github/workflows/safeguard-8-usage-monitoring.yml)
- [`sbom-generation.yml`](../.github/workflows/sbom-generation.yml)
- [`scan-for-secrets.yml`](../.github/workflows/scan-for-secrets.yml)
- [`scheduled-walkthrough-generator.yml`](../.github/workflows/scheduled-walkthrough-generator.yml)
- [`security-scan.yml`](../.github/workflows/security-scan.yml)
- [`semantic-release.yml`](../.github/workflows/semantic-release.yml)
- [`semgrep.yml`](../.github/workflows/semgrep.yml)
- [`staggered-scheduling.yml`](../.github/workflows/staggered-scheduling.yml)
- [`task-extraction.yml`](../.github/workflows/task-extraction.yml)
- [`usage-monitoring.yml`](../.github/workflows/usage-monitoring.yml)
- [`validate-quality.yml`](../.github/workflows/validate-quality.yml)
- [`version-bump.yml`](../.github/workflows/version-bump.yml)
- [`version-control-standards.yml`](../.github/workflows/version-control-standards.yml)
- [`weekly-commit-report.yml`](../.github/workflows/weekly-commit-report.yml)
- [`welcome.yml`](../.github/workflows/welcome.yml)

</details>

[Back to Top](#organization-ecosystem-dashboard)

---

*Dashboard generated by Ecosystem Visualizer*
