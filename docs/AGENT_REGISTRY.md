# Agent Registry

> **The complete catalog of organizational GitHub Copilot agents**

Welcome to the Agent Registry — your single source of truth for all GitHub Copilot agents available across the organization. This catalog provides comprehensive documentation for discovering, understanding, and using specialized agents that extend GitHub Copilot's capabilities.

**Current Status**: 22 production-ready agents across 6 categories

## Table of Contents

- [Quick Reference](#quick-reference)
- [Getting Started](#getting-started)
- [Agent Categories](#agent-categories)
  - [Data Management & Governance](#data-management--governance)
  - [Security & Compliance](#security--compliance)
  - [Infrastructure & DevOps](#infrastructure--devops)
  - [Development & Operations](#development--operations)
  - [Language & Framework Experts](#language--framework-experts)
  - [Documentation & Analysis](#documentation--analysis)
- [Agent Development Guidelines](#agent-development-guidelines)
- [Related Documentation](#related-documentation)
- [Future Agents](#future-agents)

## Quick Reference

| Agent | Category | Description | MCP Servers | File Path |
|-------|----------|-------------|-------------|-----------|
| [ADR Generator](#adr-generator) | Documentation & Analysis | Creates comprehensive Architectural Decision Records | None | [agents/adr-generator.agent.md](../agents/adr-generator.agent.md) |
| [Amplitude Experiment](#amplitude-experiment-implementation) | Development & Operations | Deploys feature experiments using Amplitude MCP | None | [agents/amplitude-experiment-implementation.agent.md](../agents/amplitude-experiment-implementation.agent.md) |
| [Arm Migration](#arm-migration-agent) | Infrastructure & DevOps | Migrates x86 workloads to Arm infrastructure | custom-mcp | [agents/arm-migration.agent.md](../agents/arm-migration.agent.md) |
| [C# Expert](#c-expert) | Language & Framework Experts | .NET project development specialist | None | [agents/CSharpExpert.agent.md](../agents/CSharpExpert.agent.md) |
| [Data Decommissioning](#data-decommissioning-agent) | Data Management & Governance | Securely removes data and systems following compliance requirements | github | [agents/data-decommissioning.agent.md](../agents/data-decommissioning.agent.md) |
| [Data Forensics](#data-forensics-agent) | Data Management & Governance | Investigates data issues, security breaches, and audit trails | github | [agents/data-forensics.agent.md](../agents/data-forensics.agent.md) |
| [Data Reclamation](#data-reclamation-agent) | Data Management & Governance | Recovers and restores lost or corrupted data | github | [agents/data-reclamation.agent.md](../agents/data-reclamation.agent.md) |
| [Data Sanitization](#data-sanitization-agent) | Data Management & Governance | Cleans and sanitizes data, removes PII, ensures compliance | github | [agents/data-sanitization.agent.md](../agents/data-sanitization.agent.md) |
| [Dynatrace Expert](#dynatrace-expert) | Development & Operations | Observability and security incident response | dynatrace | [agents/dynatrace-expert.agent.md](../agents/dynatrace-expert.agent.md) |
| [GitHub Org Manager](#github-organization-manager) | Infrastructure & DevOps | Organization governance and automation | github | [agents/github-org-manager.agent.md](../agents/github-org-manager.agent.md) |
| [JFrog Security](#jfrog-security-agent) | Security & Compliance | Application security remediation | None | [agents/jfrog-sec.agent.md](../agents/jfrog-sec.agent.md) |
| [LaunchDarkly Flag Cleanup](#launchdarkly-flag-cleanup) | Development & Operations | Automated feature flag cleanup | launchdarkly | [agents/launchdarkly-flag-cleanup.agent.md](../agents/launchdarkly-flag-cleanup.agent.md) |
| [Neon Migration Specialist](#neon-migration-specialist) | Infrastructure & DevOps | Zero-downtime Postgres migrations | None | [agents/neon-migration-specialist.agent.md](../agents/neon-migration-specialist.agent.md) |
| [Neon Performance Analyzer](#neon-performance-analyzer) | Infrastructure & DevOps | Postgres query optimization | None | [agents/neon-optimization-analyzer.agent.md](../agents/neon-optimization-analyzer.agent.md) |
| [Octopus Release Notes](#octopus-deploy-release-notes) | Development & Operations | Generates Octopus Deploy release notes | octopus | [agents/octopus-deploy-release-notes-mcp.agent.md](../agents/octopus-deploy-release-notes-mcp.agent.md) |
| [PagerDuty Responder](#pagerduty-incident-responder) | Security & Compliance | Incident response automation | pagerduty | [agents/pagerduty-incident-responder.agent.md](../agents/pagerduty-incident-responder.agent.md) |
| [Repository Setup](#repository-setup-agent) | Infrastructure & DevOps | New repository creation and configuration | github | [agents/repository-setup.agent.md](../agents/repository-setup.agent.md) |
| [Security Audit](#security-audit-agent) | Security & Compliance | Comprehensive security audits | github | [agents/security-audit.agent.md](../agents/security-audit.agent.md) |
| [StackHawk Onboarding](#stackhawk-security-onboarding) | Security & Compliance | API security testing setup | stackhawk-mcp | [agents/stackhawk-security-onboarding.agent.md](../agents/stackhawk-security-onboarding.agent.md) |
| [Terraform](#terraform-agent) | Infrastructure & DevOps | Infrastructure as Code specialist | terraform | [agents/terraform.agent.md](../agents/terraform.agent.md) |
| [WinForms Expert](#winforms-expert) | Language & Framework Experts | .NET WinForms development | None | [agents/WinFormsExpert.agent.md](../agents/WinFormsExpert.agent.md) |
| [Workflow Optimizer](#workflow-optimizer-agent) | Infrastructure & DevOps | GitHub Actions optimization | github | [agents/workflow-optimizer.agent.md](../agents/workflow-optimizer.agent.md) |

## Getting Started

### What are GitHub Copilot Agents?

GitHub Copilot agents are specialized AI assistants that extend Copilot's capabilities with domain-specific expertise. Each agent is configured with:
- Specific instructions and workflows
- Integration with MCP (Model Context Protocol) servers
- Access to specialized tools and APIs
- Domain knowledge and best practices

### How to Use Agents

#### In VS Code / VS Code Insiders

1. **Install an agent**:
   - Click the install button in the Quick Reference table above
   - Or download the `*.agent.md` file and add it to your repository

2. **Configure MCP servers** (if required):
   - Each agent specifies required MCP servers in its documentation
   - Follow the installation links in the Quick Reference table
   - Configure environment variables as needed

3. **Invoke the agent**:
   - Use the `@agent-name` syntax in GitHub Copilot Chat
   - Example: `@terraform create a VPC module`
   - Or assign the agent in the Copilot Coding Agent (CCA)

#### Common Usage Patterns

```
# Security analysis
@security-audit perform a comprehensive security audit of this repository

# Infrastructure tasks
@terraform generate AWS infrastructure for a web application
@neon-migration-specialist migrate the user schema to add email verification

# Development operations
@dynatrace-expert investigate the deployment failure from yesterday
@pagerduty-responder analyze incident INC-12345

# Documentation
@adr-generator create an ADR for our database selection decision
```

### Prerequisites

Most agents require:
- GitHub Copilot subscription (individual, business, or enterprise)
- Access to required MCP servers (see individual agent documentation)
- Appropriate API keys and credentials stored as environment variables
- Repository access and permissions

## Agent Categories

### Data Management & Governance

Agents specialized in data forensics, sanitization, recovery, and secure decommissioning to ensure data integrity, privacy, and compliance.

#### Data Forensics Agent

**Purpose**: Investigates data-related incidents, security breaches, compliance violations, and maintains comprehensive audit trails.

**Key Features**:
- Security breach investigation and incident analysis
- Data integrity verification and corruption detection
- Audit trail investigation across repositories and systems
- Compliance investigation (GDPR, CCPA, HIPAA, SOC 2, PCI DSS)
- Data lineage tracing and provenance mapping
- Repository forensics and commit history analysis
- Performance investigation and anomaly detection
- Evidence collection and incident timeline reconstruction

**Prerequisites**:
- GitHub MCP server access
- Repository access and audit log permissions
- Access to relevant logs and monitoring systems

**Invocation Examples**:
```
@data-forensics investigate unauthorized access to the production database
@data-forensics analyze the data breach that occurred last week
@data-forensics trace the source of data corruption in the users table
@data-forensics prepare a forensic report for the security incident
```

**Integration Points**:
- GitHub API and audit logs
- Database query logs
- Application logs
- CI/CD pipeline history
- Access control systems

**Related Workflows**:
- Security scanning workflows
- Audit logging systems
- Compliance reporting

**Documentation**: [agents/data-forensics.agent.md](../agents/data-forensics.agent.md)

---

#### Data Sanitization Agent

**Purpose**: Cleans and sanitizes data, removes PII, ensures compliance, and prepares data for safe sharing or disposal.

**Key Features**:
- PII (Personally Identifiable Information) identification and removal
- Sensitive data redaction and anonymization
- Code sanitization (secrets, credentials, tokens)
- Log sanitization and secure data masking
- Database anonymization and synthetic data generation
- Git history sanitization and secret removal
- Compliance-driven sanitization (GDPR, CCPA, HIPAA, PCI DSS)
- Pattern-based detection and automated cleanup

**Prerequisites**:
- GitHub MCP server access
- Repository write permissions
- Access to data sources requiring sanitization

**Invocation Examples**:
```
@data-sanitization remove all PII from application logs
@data-sanitization clean up the commit history to remove exposed API keys
@data-sanitization sanitize the database export file before sharing with QA team
@data-sanitization prepare anonymized dataset for research purposes
```

**Integration Points**:
- GitHub API for repository cleanup
- Secret scanning tools
- Data anonymization libraries
- Backup and archival systems

**Related Workflows**:
- Secret scanning workflows
- Data export processes
- Compliance reporting

**Documentation**: [agents/data-sanitization.agent.md](../agents/data-sanitization.agent.md)

---

#### Data Reclamation Agent

**Purpose**: Recovers and restores lost, corrupted, or accidentally deleted data from various sources with comprehensive recovery strategies.

**Key Features**:
- Git repository recovery (deleted branches, commits, files)
- Database recovery (backups, PITR, transaction logs)
- File recovery from various sources
- Configuration and secrets recovery
- Backup and archive restoration
- Cloud resource recovery
- GitHub artifact and release recovery
- Multi-source data reconstruction

**Prerequisites**:
- GitHub MCP server access
- Access to backup systems
- Repository and database permissions
- Cloud provider access (AWS, Azure, GCP)

**Invocation Examples**:
```
@data-reclamation recover the feature branch that was deleted yesterday
@data-reclamation restore database records deleted in the last hour
@data-reclamation recover files from last week's backup
@data-reclamation restore the repository to its state before the merge
```

**Integration Points**:
- GitHub API and reflog
- Database backup systems
- Cloud provider APIs
- Snapshot and versioning systems

**Related Workflows**:
- Backup automation
- Disaster recovery procedures
- Version control systems

**Documentation**: [agents/data-reclamation.agent.md](../agents/data-reclamation.agent.md)

---

#### Data Decommissioning Agent

**Purpose**: Securely removes data and systems following compliance requirements, ensuring complete and verifiable data destruction.

**Key Features**:
- Secure data destruction (crypto-shredding, multi-pass wiping)
- System and infrastructure decommissioning
- Repository archival and deletion
- Cloud infrastructure teardown
- Database retirement procedures
- Application and service shutdown
- Account and access removal
- Compliance-driven decommissioning (GDPR, NIST SP 800-88, DoD 5220.22-M)

**Prerequisites**:
- GitHub MCP server access
- Administrative permissions
- Cloud provider access
- Approval for data destruction

**Invocation Examples**:
```
@data-decommissioning decommission the staging environment AWS account
@data-decommissioning securely remove the deprecated user database
@data-decommissioning archive and delete the legacy-api repository
@data-decommissioning prepare destruction certificate for HIPAA audit
```

**Integration Points**:
- GitHub API for repository management
- Cloud provider APIs
- Certificate management systems
- Compliance documentation systems

**Related Workflows**:
- Infrastructure teardown automation
- Compliance certification processes
- Resource cleanup jobs

**Documentation**: [agents/data-decommissioning.agent.md](../agents/data-decommissioning.agent.md)

---

#### Choosing the Right Data Management Agent

| Use Case | Recommended Agent | Primary Outcome | Safety Checks |
| --- | --- | --- | --- |
| Investigate breaches, integrity issues, or timeline of changes | **Data Forensics** | Evidence-backed incident report with audit-ready artifacts | Preserve evidence snapshots first; record chain of custody; define incident scope before querying |
| Remove PII/secrets or prepare data for sharing | **Data Sanitization** | Cleaned dataset/repo with documented sanitization steps | Test on surrogates; verify for re-identification risk; rotate any exposed credentials |
| Recover deleted, corrupted, or overwritten assets | **Data Reclamation** | Restored data with RTO/RPO and integrity validation | Restore in isolation; document snapshot/commit IDs; keep rollback path open |
| Retire systems, repositories, or infrastructure | **Data Decommissioning** | Verified destruction with compliance-grade evidence | Require approvals; pair teardown with billing checks; issue destruction certificates |

**Category Guardrails**:

- Favor **smallest-possible blast radius** first: start with scoped restores, targeted sanitization, and sandboxed forensics before touching production systems.
- Keep **evidence and auditability** central: log tool versions, commit/SHA references, timestamps, and approvals so findings withstand external review.
- **Couple high-risk actions with compensating controls**: dual-control for destructive operations, credential rotation after sanitization, and post-action billing/monitoring verification after decommissions.
- Demand **rollback readiness**: keep restorable checkpoints for reclamation/decommissioning work and dry-run dangerous operations in sandboxes first.
- Define **exit criteria upfront**: success metrics such as RTO/RPO targets, absence of PII matches, or confirmed cost reductions prevent ambiguous closures.
- Maintain **communication loops**: notify data owners and dependent teams before and after changes to avoid surprises and secondary incidents.

---

### Security & Compliance

Agents focused on security analysis, vulnerability remediation, incident response, and compliance monitoring.

#### JFrog Security Agent

**Purpose**: Automated application security remediation with policy compliance verification.

**Key Features**:
- Package and version compliance verification
- Vulnerability fixes using JFrog security intelligence
- Curation policy checks before dependency upgrades
- CVE-specific remediation guidance

**Prerequisites**:
- JFrog MCP server access
- Organization curation policies configured

**Invocation Examples**:
```
@jfrog-sec remediate the security vulnerabilities in package.json
@jfrog-sec check if upgrading to lodash 4.17.21 is policy-compliant
@jfrog-sec analyze dependencies for security issues
```

**Integration Points**:
- JFrog Artifactory / Xray
- Package managers (npm, pip, Maven, etc.)
- Security scanning tools

**Related Workflows**: None

**Documentation**: [agents/jfrog-sec.agent.md](../agents/jfrog-sec.agent.md)

---

#### Security Audit Agent

**Purpose**: Comprehensive security audits of repositories, workflows, and organizational settings.

**Key Features**:
- Code security scanning (secrets, vulnerabilities, OWASP Top 10)
- Dependency security analysis
- GitHub Actions & workflow security review
- Repository configuration audit
- Access control & permissions review
- Secret management verification
- Supply chain security assessment
- Container security analysis

**Prerequisites**:
- GitHub MCP server access
- Repository admin permissions (for full audits)

**Invocation Examples**:
```
@security-audit perform a comprehensive security audit of this repository
@security-audit review GitHub Actions workflows for security issues
@security-audit audit access controls and permissions
@security-audit check for exposed secrets and credentials
```

**Integration Points**:
- GitHub API via MCP server
- Dependabot
- CodeQL
- Secret scanning

**Related Workflows**:
- Security scanning workflows
- Dependabot configuration
- Branch protection rules

**Documentation**: [agents/security-audit.agent.md](../agents/security-audit.agent.md)

---

#### StackHawk Security Onboarding

**Purpose**: Automatically set up StackHawk API security testing for repositories.

**Key Features**:
- Attack surface assessment
- Automated stackhawk.yml configuration
- GitHub Actions workflow generation
- Application vs. library detection
- Security testing prioritization

**Prerequisites**:
- StackHawk MCP server (`uvx stackhawk-mcp`)
- STACKHAWK_API_KEY environment variable
- Application with APIs or web endpoints

**Invocation Examples**:
```
@stackhawk-onboarding set up security testing for this API
@stackhawk-onboarding analyze if this repository needs security testing
@stackhawk-onboarding configure StackHawk for my Express application
```

**Integration Points**:
- StackHawk platform
- GitHub Actions
- API documentation (OpenAPI/Swagger)

**Related Workflows**:
- `.github/workflows/stackhawk.yml` (auto-generated)
- CI/CD pipelines

**Documentation**: [agents/stackhawk-security-onboarding.agent.md](../agents/stackhawk-security-onboarding.agent.md)

---

#### PagerDuty Incident Responder

**Purpose**: Automated incident response and remediation for PagerDuty incidents.

**Key Features**:
- Incident context analysis
- Recent code change identification
- Root cause hypothesis formulation
- Automated fix or rollback PR generation
- On-call team identification

**Prerequisites**:
- PagerDuty MCP server
- GitHub MCP server
- OAuth authentication for PagerDuty

**Invocation Examples**:
```
@pagerduty-responder analyze incident INC-12345
@pagerduty-responder investigate failures on the payment-service
@pagerduty-responder create a fix PR for the current incident
```

**Integration Points**:
- PagerDuty API
- GitHub commit history
- Deployment tracking

**Related Workflows**:
- Incident response workflows
- Deployment automation

**Documentation**: [agents/pagerduty-incident-responder.agent.md](../agents/pagerduty-incident-responder.agent.md)

---

### Infrastructure & DevOps

Agents for infrastructure management, cloud migrations, database operations, and DevOps automation.

#### Terraform Agent

**Purpose**: Infrastructure as Code specialist with HCP Terraform integration.

**Key Features**:
- Registry intelligence (public and private)
- Code generation with latest provider/module versions
- HCP Terraform workspace management
- Run orchestration and validation
- Security and compliance best practices
- Module testing with Terraform Test

**Prerequisites**:
- Terraform MCP server (Docker)
- TFE_TOKEN for private registry access (optional)
- TFE_ADDRESS for HCP Terraform
- ENABLE_TF_OPERATIONS for destructive operations (optional)

**Invocation Examples**:
```
@terraform create an AWS VPC module with public and private subnets
@terraform generate Kubernetes deployment configuration
@terraform search for the latest AWS provider version
@terraform create a workspace for this repository
```

**Integration Points**:
- Terraform Registry (public)
- HCP Terraform (private registry, workspaces, runs)
- Cloud providers (AWS, Azure, GCP, etc.)

**Related Workflows**:
- Infrastructure deployment pipelines
- Terraform plan/apply automation

**Documentation**: [agents/terraform.agent.md](../agents/terraform.agent.md)

---

#### Arm Migration Agent

**Purpose**: Accelerates migration from x86 to Arm infrastructure.

**Key Features**:
- Architecture assumption scanning
- Container base image compatibility checking
- Dependency compatibility verification
- Multi-arch container build support
- Performance optimization recommendations

**Prerequisites**:
- custom-mcp Docker server (`armswdev/arm-mcp:latest`)
- Repository with Dockerfiles or dependencies

**Invocation Examples**:
```
@arm-migration migrate this application to Arm architecture
@arm-migration check Docker images for Arm compatibility
@arm-migration analyze Python dependencies for Arm support
```

**Integration Points**:
- Docker/container registries
- Package managers (pip, npm, apt, etc.)
- migrate-ease scanning tools

**Related Workflows**:
- Multi-arch build workflows
- Performance benchmarking

**Documentation**: [agents/arm-migration.agent.md](../agents/arm-migration.agent.md)

---

#### Neon Migration Specialist

**Purpose**: Safe, zero-downtime Postgres schema migrations using Neon's branching.

**Key Features**:
- Test migrations on isolated database branches
- Support for Prisma, Drizzle, SQLAlchemy, and other ORMs
- Automatic rollback capability
- Migration validation and testing
- 4-hour TTL test branches

**Prerequisites**:
- Neon API key
- Neon project ID or connection string
- Existing migration system (preferred) or migra

**Invocation Examples**:
```
@neon-migration-specialist add email_verified column to users table
@neon-migration-specialist migrate the schema for user preferences
@neon-migration-specialist test the pending Prisma migrations
```

**Integration Points**:
- Neon Serverless Postgres API
- ORM migration systems (Prisma, Drizzle, etc.)
- CI/CD pipelines

**Related Workflows**:
- Database migration automation
- Schema validation

**Documentation**: [agents/neon-migration-specialist.agent.md](../agents/neon-migration-specialist.agent.md)

---

#### Neon Performance Analyzer

**Purpose**: Identify and optimize slow Postgres queries using Neon's branching.

**Key Features**:
- pg_stat_statements analysis
- EXPLAIN plan optimization
- Index recommendation
- Query rewriting
- Before/after performance metrics
- Safe testing on database branches

**Prerequisites**:
- Neon API key
- Neon project ID or connection string
- pg_stat_statements extension (auto-enabled if missing)

**Invocation Examples**:
```
@neon-optimization-analyzer find and fix slow queries
@neon-optimization-analyzer analyze query performance for the users table
@neon-optimization-analyzer optimize the top 5 slowest queries
```

**Integration Points**:
- Neon Serverless Postgres API
- pg_stat_statements
- Application codebase (for query context)

**Related Workflows**:
- Performance monitoring
- Query optimization tracking

**Documentation**: [agents/neon-optimization-analyzer.agent.md](../agents/neon-optimization-analyzer.agent.md)

---

#### GitHub Organization Manager

**Purpose**: Implements the 8-module AI GitHub Management Protocol for organization governance.

**Key Features**:
- Organization & repository administration
- Project management & workflow automation
- CI/CD & development lifecycle management
- Security & compliance operations
- Documentation & knowledge base management
- Ecosystem integration monitoring
- Observability & system health
- Strategic analysis & risk mitigation

**Prerequisites**:
- GitHub MCP server
- Organization admin permissions

**Invocation Examples**:
```
@github-org-manager audit branch protection rules across all repositories
@github-org-manager create a new repository setup checklist
@github-org-manager assess compliance with security module
@github-org-manager identify single points of failure in our architecture
```

**Integration Points**:
- GitHub API (organizations, repos, workflows)
- Security scanning tools
- Observability platforms

**Related Workflows**:
- Organization health monitoring
- Compliance reporting

**Documentation**: [agents/github-org-manager.agent.md](../agents/github-org-manager.agent.md)

---

#### Repository Setup Agent

**Purpose**: Automates creation and configuration of new repositories following organization standards.

**Key Features**:
- Repository initialization with templates
- Community health files setup
- Issue & PR templates configuration
- Branch protection rules
- Standardized label sets
- GitHub Actions workflows
- Security configuration

**Prerequisites**:
- GitHub MCP server
- Organization membership
- Repository creation permissions

**Invocation Examples**:
```
@repository-setup create a new Python project repository
@repository-setup configure branch protection for main branch
@repository-setup set up standard issue templates
@repository-setup apply organization defaults to this repository
```

**Integration Points**:
- GitHub API
- Organization defaults
- Template repositories

**Related Workflows**:
- Repository provisioning automation
- Onboarding workflows

**Documentation**: [agents/repository-setup.agent.md](../agents/repository-setup.agent.md)

---

#### Workflow Optimizer Agent

**Purpose**: Analyzes and optimizes GitHub Actions workflows for performance, cost, security, and reliability.

**Key Features**:
- Performance optimization (caching, parallelization)
- Cost reduction (runner selection, path filters)
- Security hardening (permissions, action pinning)
- Reliability improvements (retries, timeouts)
- Maintainability enhancements (reusable workflows)

**Prerequisites**:
- GitHub MCP server
- Repository with GitHub Actions workflows

**Invocation Examples**:
```
@workflow-optimizer analyze and optimize the CI workflow
@workflow-optimizer reduce costs in GitHub Actions
@workflow-optimizer improve security of deployment workflows
@workflow-optimizer add caching to the build workflow
```

**Integration Points**:
- GitHub Actions
- Workflow syntax and features
- Security best practices

**Related Workflows**:
- All `.github/workflows/*.yml` files

**Documentation**: [agents/workflow-optimizer.agent.md](../agents/workflow-optimizer.agent.md)

---

### Development & Operations

Agents for feature management, observability, deployment automation, and operational excellence.

#### Dynatrace Expert

**Purpose**: Master observability and security specialist for incident response and performance analysis.

**Key Features**:
- Incident response & root cause analysis
- Deployment impact analysis
- Production error triage
- Performance regression detection
- Release validation & health checks
- Security vulnerability response
- Complete DQL (Dynatrace Query Language) expertise

**Prerequisites**:
- Dynatrace MCP server
- COPILOT_MCP_DT_API_TOKEN
- Dynatrace environment access

**Invocation Examples**:
```
@dynatrace-expert investigate yesterday's deployment failure
@dynatrace-expert analyze performance regression in checkout service
@dynatrace-expert find root cause of 500 errors
@dynatrace-expert validate the latest release health
```

**Integration Points**:
- Dynatrace platform
- Traces, logs, metrics, events
- Davis AI problems
- Security findings

**Related Workflows**:
- Deployment validation
- Incident response
- Performance monitoring

**Documentation**: [agents/dynatrace-expert.agent.md](../agents/dynatrace-expert.agent.md)

---

#### LaunchDarkly Flag Cleanup

**Purpose**: Safely automate feature flag cleanup workflows using LaunchDarkly's source of truth.

**Key Features**:
- Flag removal readiness determination
- Forward value identification
- Production behavior preservation
- Safe code transformation
- Stale default updates

**Prerequisites**:
- LaunchDarkly MCP server (`@launchdarkly/mcp-server`)
- LD_ACCESS_TOKEN environment variable
- LaunchDarkly project access

**Invocation Examples**:
```
@launchdarkly-flag-cleanup remove the new-checkout-flow flag
@launchdarkly-flag-cleanup clean up flags marked as deprecated
@launchdarkly-flag-cleanup check if user-onboarding-v2 can be removed
```

**Integration Points**:
- LaunchDarkly platform
- Feature flag evaluation in code
- Environment configurations

**Related Workflows**:
- Flag lifecycle management
- Code cleanup automation

**Documentation**: [agents/launchdarkly-flag-cleanup.agent.md](../agents/launchdarkly-flag-cleanup.agent.md)

---

#### Amplitude Experiment Implementation

**Purpose**: Deploy feature experiments using Amplitude's MCP tools.

**Key Features**:
- Experiment creation in Amplitude
- Feature implementation with variants
- Instrumentation setup
- A/B testing configuration
- Feature rollout automation

**Prerequisites**:
- Amplitude MCP server access
- Amplitude project configuration
- GitHub issue with requirements

**Invocation Examples**:
```
@amplitude-experiment implement the experiment from issue #42
@amplitude-experiment create A/B test for new checkout flow
@amplitude-experiment set up feature flag for user onboarding
```

**Integration Points**:
- Amplitude Experiment platform
- Application instrumentation
- Analytics tracking

**Related Workflows**:
- Feature deployment
- A/B testing pipelines

**Documentation**: [agents/amplitude-experiment-implementation.agent.md](../agents/amplitude-experiment-implementation.agent.md)

---

#### Octopus Deploy Release Notes

**Purpose**: Generate comprehensive release notes from Octopus Deploy deployments.

**Key Features**:
- Release information extraction
- Git commit analysis
- Author and date tracking
- Markdown-formatted output
- Relevant commit filtering

**Prerequisites**:
- Octopus MCP server (`@octopusdeploy/mcp-server`)
- OCTOPUS_API_KEY secret
- OCTOPUS_SERVER_URL secret
- Octopus Deploy project access

**Invocation Examples**:
```
@octopus-release-notes generate release notes for project MyApp in Production
@octopus-release-notes create changelog for the latest deployment
@octopus-release-notes summarize commits in release 1.2.3
```

**Integration Points**:
- Octopus Deploy API
- GitHub commit history
- Release management

**Related Workflows**:
- Release automation
- Changelog generation

**Documentation**: [agents/octopus-deploy-release-notes-mcp.agent.md](../agents/octopus-deploy-release-notes-mcp.agent.md)

---

### Language & Framework Experts

Specialized agents for specific programming languages and frameworks.

#### C# Expert

**Purpose**: Expert .NET developer for clean, well-designed C# code.

**Key Features**:
- Modern C# language features
- .NET conventions and patterns
- SOLID principles application
- Async/await patterns
- Dependency injection
- Testing with xUnit/NUnit/MSTest
- Security best practices
- Performance optimization

**Prerequisites**: None (native Copilot capabilities)

**Invocation Examples**:
```
@csharp-expert create an ASP.NET Core Web API for user management
@csharp-expert implement authentication with JWT tokens
@csharp-expert optimize this LINQ query for performance
@csharp-expert write unit tests for the UserService class
```

**Integration Points**:
- .NET SDK and runtime
- NuGet packages
- Testing frameworks
- ORM tools (Entity Framework, Dapper)

**Related Workflows**:
- .NET build and test workflows
- NuGet package publishing

**Documentation**: [agents/CSharpExpert.agent.md](../agents/CSharpExpert.agent.md)

---

#### WinForms Expert

**Purpose**: Specialized support for .NET WinForms Designer-compatible applications.

**Key Features**:
- .NET 10+ support with DarkMode
- Windows API projections
- Designer-compatible code generation
- MVVM binding (requires .NET 8+)
- HighDPI support
- VB.NET App Framework support
- Two-context coding (Designer vs Regular)

**Prerequisites**: None (native Copilot capabilities)

**Invocation Examples**:
```
@winforms-expert create a new WinForms project with .NET 10
@winforms-expert add a DataGridView with user management
@winforms-expert implement DarkMode support
@winforms-expert fix Designer compatibility issues
```

**Integration Points**:
- Windows Forms Designer
- .NET SDK
- NuGet packages
- Windows API

**Related Workflows**:
- Windows application build workflows
- MSI/installer creation

**Documentation**: [agents/WinFormsExpert.agent.md](../agents/WinFormsExpert.agent.md)

---

### Documentation & Analysis

Agents for documentation creation, architectural decisions, and repository analysis.

#### ADR Generator

**Purpose**: Creates comprehensive, well-structured Architectural Decision Records (ADRs).

**Key Features**:
- Standardized ADR format with front matter
- Structured sections (Context, Decision, Consequences)
- Alternatives documentation with rejection rationale
- Implementation notes and references
- Machine-parsable coded bullet points
- Sequential numbering (adr-NNNN)

**Prerequisites**: None (native Copilot capabilities)

**Invocation Examples**:
```
@adr-generator create an ADR for database selection
@adr-generator document the decision to use microservices architecture
@adr-generator write an ADR for authentication strategy
```

**Integration Points**:
- `/docs/adr/` directory
- Related ADRs via references
- External documentation

**Related Workflows**:
- Documentation generation
- Architecture reviews

**Documentation**: [agents/adr-generator.agent.md](../agents/adr-generator.agent.md)

---

## Agent Development Guidelines

### Creating New Agents

When creating a new GitHub Copilot agent for the organization:

#### 1. File Structure

Create a file in the `agents/` directory following this naming convention:
```
agents/your-agent-name.agent.md
```

#### 2. Front Matter

All agent files must include YAML front matter:

```yaml
---
name: Your Agent Name
description: 'Brief description of what your agent does'
tools: ['read', 'edit', 'search', 'shell']  # Optional
mcp-servers:  # Optional
  server-name:
    type: 'local' | 'http'
    command: 'executable'
    args: ['arg1', 'arg2']
    env:
      VAR_NAME: $SECRET_NAME
    tools: ["*"]
dependencies:  # Optional
  - mcp: github
---
```

**Required Fields**:
- `name`: Display name for the agent
- `description`: Single-line description (use quotes for special characters)

**Optional Fields**:
- `tools`: Array of tool names the agent uses
- `mcp-servers`: MCP server configurations
- `dependencies`: Required MCP servers or other dependencies

#### 3. Content Structure

Organize your agent documentation with these sections:

1. **Overview**: Brief introduction and role definition
2. **Key Features**: Bulleted list of capabilities
3. **Prerequisites**: Required setup, API keys, permissions
4. **Core Workflow**: Step-by-step agent behavior
5. **Usage Examples**: Concrete invocation examples
6. **Integration Points**: External services and tools
7. **Best Practices**: Guidelines for effective use
8. **Troubleshooting** (optional): Common issues and solutions

#### 4. Writing Style

- Use clear, concise language
- Write in second person ("You are...")
- Include specific examples
- Document all prerequisites
- Link to external documentation
- Follow Markdown best practices

#### 5. MCP Server Configuration

If your agent requires MCP servers:

**Local MCP Server**:
```yaml
mcp-servers:
  my-server:
    type: 'local'
    command: 'npx'
    args: ['-y', 'my-mcp-server']
    env:
      API_KEY: $COPILOT_MCP_MY_API_KEY
```

**HTTP MCP Server**:
```yaml
mcp-servers:
  my-server:
    type: 'http'
    url: 'https://api.example.com/mcp'
    headers:
      Authorization: 'Bearer $COPILOT_MCP_MY_TOKEN'
```

**Docker MCP Server**:
```yaml
mcp-servers:
  my-server:
    type: 'local'
    command: 'docker'
    args: ['run', '-i', '--rm', 'my-org/my-mcp:latest']
```

#### 6. Testing Your Agent

Before submitting:
- [ ] Test all documented invocation examples
- [ ] Verify MCP server connectivity
- [ ] Check that prerequisites are accurate
- [ ] Validate front matter YAML syntax
- [ ] Ensure links work correctly
- [ ] Test with real-world scenarios

#### 7. Documentation Updates

After creating your agent:
1. Update this registry (AGENT_REGISTRY.md)
2. Add entry to Quick Reference table
3. Add detailed section in appropriate category
4. Update `docs/README.agents.md` with install buttons
5. Create any related workflow documentation

#### 8. Organization Standards

Follow these organization standards:
- **Language**: Python 3.11+ for scripts
- **Security**: Security-first principles, no hardcoded secrets
- **Testing**: Include example usage and test cases
- **Versioning**: Use semantic versioning for agent updates
- **Comments**: Explain complex logic, document edge cases

### Best Practices

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Composability**: Design agents to work well together
3. **Error Handling**: Provide clear error messages and recovery steps
4. **Idempotency**: Agent actions should be safe to repeat
5. **Documentation**: Keep agent docs in sync with implementation
6. **Security**: Never expose secrets, use environment variables
7. **Performance**: Optimize for common use cases
8. **Extensibility**: Design for future enhancements

### Security Guidelines

When developing agents:
- ✅ Use environment variables for all credentials
- ✅ Validate all input parameters
- ✅ Follow least privilege principle
- ✅ Log security-relevant actions
- ✅ Sanitize any user-provided data
- ✅ Use HTTPS for all external communications
- ❌ Never hardcode API keys or tokens
- ❌ Never commit secrets to the repository
- ❌ Never expose sensitive data in logs
- ❌ Never execute untrusted code

### Review Process

All new agents must go through:
1. **Code Review**: Peer review of agent logic and documentation
2. **Security Review**: Security team approval for agents with external access
3. **Testing**: Validation of all documented use cases
4. **Documentation Review**: Ensure clarity and completeness
5. **Integration Testing**: Test with related agents and workflows

## Related Documentation

### Core Documentation
- [README.agents.md](README.agents.md) - Agent installation and usage guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute to the organization
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards
- [SECURITY.md](SECURITY.md) - Security policies and reporting

### GitHub Copilot Resources
- [README.prompts.md](README.prompts.md) - Task-specific prompts
- [README.instructions.md](README.instructions.md) - Coding standards and best practices
- [README.chatmodes.md](README.chatmodes.md) - Chat mode configurations
- [README.collections.md](README.collections.md) - Copilot collections

### Organization Guides
- [QUICK_START.md](../QUICK_START.md) - Organization quick start guide
- [BEST_PRACTICES.md](../BEST_PRACTICES.md) - Development best practices
- [AUTOMATION_MASTER_GUIDE.md](../AUTOMATION_MASTER_GUIDE.md) - Automation patterns
- [AI_RAPID_WORKFLOW.md](../AI_RAPID_WORKFLOW.md) - AI-assisted development workflow

### Technical References
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)

---

## Future Agents

The following agents are planned for future development and are not yet available for use.

### Nervous Archaeologist

**Purpose**: Repository analysis and documentation specialist.

**Planned Features**:
- Repository structure analysis
- Code archaeology and history analysis
- Documentation gap identification
- Dependency mapping
- Historical context extraction
- Legacy code understanding

**Expected Use Cases**:
```
@nervous-archaeologist analyze the repository structure
@nervous-archaeologist find undocumented features
@nervous-archaeologist trace the history of the authentication module
```

**Status**: Planned for Q1 2026

**Note**: If you're interested in contributing this agent or have requirements to share, please open a discussion or feature request issue.

---

## Feedback and Support

### Questions or Issues?

- **General Questions**: Open a [discussion](../../discussions)
- **Bug Reports**: Create an [issue](../../issues/new?template=bug_report.md)
- **Feature Requests**: Create an [issue](../../issues/new?template=feature_request.md)
- **Security Issues**: See [SECURITY.md](SECURITY.md) for reporting procedures

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to contribute new agents
- Code review process
- Testing requirements
- Documentation standards

---

**Last Updated**: 2025-11-24

**Maintained by**: ivi374forivi Organization

**License**: MIT (see [LICENSE](../LICENSE))
