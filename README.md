# ivi374forivi Organization

> **Default Community Health Files and Configurations**

Welcome to the **ivi374forivi** organization! We believe in open collaboration,
transparent development, and building innovative solutions through high-quality
software and inclusive community practices.

## About This Repository

This is the special `.github` repository for our organization. It serves as the
central hub for:

- **Default community health files** that apply to all repositories
- **Standardized templates** for issues and pull requests
- **Reusable workflow templates** for CI/CD and automation
- **Organization-wide configuration** and documentation standards
- **Living Document System** - AI-driven governance and management protocols
- **Mouthpiece Filter System** - Transform natural human expression into AI-optimized prompts

When a repository in our organization doesn't have its own community health files, GitHub automatically uses the defaults from this repository.

> **Is this the right repository for these functions?** See our [Repository Purpose Analysis](docs/architecture/REPOSITORY_PURPOSE_ANALYSIS.md) for a detailed explanation of why this `.github` repository is the appropriate location for organization-wide governance, templates, and the Living Document System.

## Our Mission

At **ivi374forivi**, we are committed to:

- **Openness**: Developing in the open with transparency
- **Collaboration**: Welcoming diverse perspectives and contributors
- **Quality**: Delivering well-tested, documented, and maintainable software
- **Respect**: Maintaining an inclusive environment for all
- **Innovation**: Encouraging experimentation and creative problem-solving
- **Sustainability**: Building projects supported by healthy communities

Read our complete vision in the [Manifesto](docs/MANIFESTO.md).

### Commit Message Format

We follow conventional commit format:

```text
<type>: <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

**Examples**:

- `feat: add user authentication`
- `fix: resolve memory leak in data processor`
- `docs: update API documentation`

### Viewing Commit Reports

Commit tracking runs automatically on:

- Every push to `main` or `develop` branches
- Every pull request update

Weekly reports are generated every Monday and stored in the `reports/` directory
.

## What's Inside

### 🚀 Workflow Optimization Analysis (NEW!)

**Comprehensive 9-Dimensional Analysis of 76 GitHub Actions Workflows**

This repository has undergone an exhaustive workflow optimization analysis covering Critique, Logic, Logos, Pathos, Ethos, Blindspots, Shatter-points, Bloom, and Evolve dimensions. The analysis provides actionable insights to transform our CI/CD from "Very Good" (B+) to "Industry-Leading" (A+).

**📊 Quick Stats:**
- **Total Workflows**: 76 analyzed
- **Security Grade**: B+ → A+ (99% actions pinned, path to 100%)
- **Performance**: 40-60% faster builds achievable
- **Cost Savings**: 50-60% reduction potential
- **ROI**: 134% in first year

**📚 Documentation:**
- 🚀 [**Ready to Start? Next Steps Guide**](NEXT_STEPS_IMPLEMENTATION.md) - Day-by-day implementation plan
- 🎯 [**Executive Summary**](EXECUTIVE_SUMMARY.md) - 10-minute overview for decision-makers
- 🔬 [**Deep Dive: Comprehensive Analysis**](COMPREHENSIVE_WORKFLOW_OPTIMIZATION_ANALYSIS.md) - Complete 9-dimensional review
- 🗺️ [**Action Plan: Implementation Roadmap**](WORKFLOW_OPTIMIZATION_ROADMAP.md) - Step-by-step guide with timelines
- 🔒 [**Security: Audit Report**](WORKFLOW_SECURITY_AUDIT.md) - Security review and recommendations
- ⚡ [**Daily Use: Quick Reference**](WORKFLOW_QUICK_REFERENCE.md) - Copy-paste ready solutions
- 📑 [**Navigation: Complete Index**](WORKFLOW_OPTIMIZATION_INDEX.md) - Guide to all documentation

**🎯 Ready to Implement? Week 1 Tasks (3 days):**
1. 🔴 **Day 1 AM**: Pin 3 unpinned actions (30 min, HIGH security impact)
2. ⚡ **Day 1 PM**: Add caching to top 5 workflows (2 hrs, 30-40% faster immediately)
3. 📚 **Day 2**: Create contributor guide (3 hrs, better DX)
4. ✅ **Day 3**: Test and validate changes (2 hrs)

👉 **[See detailed day-by-day plan →](NEXT_STEPS_IMPLEMENTATION.md)**

**Expected Outcomes:**
- **3 Months**: 40% faster, more secure, better documented
- **6 Months**: 60% faster, 95%+ reliable, comprehensive observability
- **12 Months**: Industry-leading platform, autonomous optimization

### GitHub Copilot Customizations

This repository includes comprehensive GitHub Copilot customizations from the [github/awesome-copilot](https://github.com/github/awesome-copilot) repository for organization-wide implementation.

#### Custom Agents

- **Location**: `agents/` directory
- **Purpose**: Specialized GitHub Copilot agents that integrate with MCP servers for enhanced capabilities
- **Count**: 19 production-ready agents across 5 categories (Security, Infrastructure, Development, Languages, Documentation)
- **Registry**: See [Agent Registry](docs/AGENT_REGISTRY.md) for complete catalog with usage examples
- **Examples**: CSharpExpert, Terraform, ADR Generator, Security Audit, Completionism Specialist, and partner integrations

#### Instructions

- **Location**: `instructions/` directory
- **Purpose**: Comprehensive coding standards and best practices that apply to specific file patterns
- **Coverage**: Multiple frameworks and languages (Angular, React, Python, .NET, Azure, etc.)
- **Usage**: Instructions automatically apply based on file patterns

#### Prompts

- **Location**: `prompts/` directory
- **Purpose**: Task-specific prompts for code generation, documentation, and problem-solving
- **Usage**: Access via `/` commands in GitHub Copilot Chat (e.g., `/awesome-copilot create-readme`)

#### Chat Modes

- **Location**: `chatmodes/` directory
- **Purpose**: Specialized AI personas for different roles (architect, DBA, security expert, etc.)
- **Usage**: Activate modes for specialized assistance tailored to specific contexts

#### Collections

- **Location**: `collections/` directory
- **Purpose**: Curated collections of prompts, instructions, and chat modes organized by theme
- **Examples**: Azure Cloud Development, Frontend Web Dev, Security Best Practices

For detailed documentation on each component, see the `docs/` directory:

- [**Agent Registry**](docs/AGENT_REGISTRY.md) - Complete catalog of 18 production agents + future roadmap
- [Agents Documentation](docs/README.agents.md)
- [Instructions Documentation](docs/README.instructions.md)
- [Prompts Documentation](docs/README.prompts.md)
- [Chat Modes Documentation](docs/README.chatmodes.md)
- [Collections Documentation](docs/README.collections.md)

### Mouthpiece Filter System

**Transform your natural human expression into AI-optimized prompts.**

The Mouthpiece Filter System allows you to write and speak in your authentic voice—with all its imperfections, metaphors, and humanity—and automatically transforms that input into structured, clear prompts that AI systems can understand and act upon.

> _"Write like a human. Let the filter handle the rest."_

#### What It Does

- **Preserves Your Voice**: Keeps your unique style, metaphors, and emotional context
- **Extracts Intent**: Understands what you mean, not just what you say
- **Structures Information**: Organizes thoughts into clear, actionable formats
- **Optimizes for AI**: Creates prompts that AI systems can process effectively

#### Components

- **Filter Script** (`scripts/mouthpiece_filter.py`) - CLI transformation engine
- **Chat Mode** (`chatmodes/mouthpiece.chatmode.md`) - Interactive AI persona
- **Prompt Template** (`prompts/mouthpiece-transform.prompt.md`) - Quick transformations
- **Documentation** ([MOUTHPIECE_README.md](MOUTHPIECE_README.md)) - Complete guide

#### Quick Start

```bash
# Transform natural writing into structured prompts
python scripts/mouthpiece_filter.py "your natural thoughts here"

# Example
python scripts/mouthpiece_filter.py "need something that watches APIs and alerts when they fail"
```

**Learn More:**

- [Mouthpiece System Overview](docs/MOUTHPIECE_README.md)
- [Complete Documentation](docs/MOUTHPIECE_SYSTEM.md)
- [Examples & Patterns](docs/mouthpiece-examples.md)

### 🎥 Video Walkthrough Generation System

**Autonomous video documentation for all organization repositories.**

The Video Walkthrough Generation system automatically creates professional 1-minute video walkthroughs with AI voiceover for all repositories in the Ivviiviivvi organization. This provides an engaging way to showcase your projects, onboard new team members, and create compelling documentation.

> _"Turn your code into compelling visual stories—automatically."_

#### Key Features

✅ **Automatic Application Detection** - Supports React, Vue, Angular, Next.js, Python (Flask/FastAPI/Django), Java (Spring Boot), and static sites
✅ **AI-Powered Voiceover** - Professional, casual, or technical narration styles
✅ **Zero Manual Intervention** - Fully automated workflow execution
✅ **Intelligent PR Creation** - Automatic pull requests with video artifacts
✅ **Organization-Wide Deployment** - Single-command rollout to all repositories
✅ **Customizable Settings** - Duration, style, focus areas, and more

#### Components

- **Main Workflow** (`.github/workflows/generate-walkthrough.yml`) - Automatic video generation with app detection
- **Reusable Workflow** (`.github/workflows/org-walkthrough-generator.yml`) - Organization-wide reusable workflow
- **Configuration** (`.github/walkthrough-config.yml`) - Comprehensive settings and detection rules
- **Bootstrap Script** (`scripts/bootstrap-walkthrough-org.sh`) - Deploy to all organization repositories
- **Documentation** ([.github/WALKTHROUGH_GUIDE.md](.github/WALKTHROUGH_GUIDE.md)) - Complete usage guide

#### Quick Start

```bash
# Deploy to all organization repositories
./scripts/bootstrap-walkthrough-org.sh --dry-run  # Preview first
./scripts/bootstrap-walkthrough-org.sh            # Deploy

# Manual trigger in any repository
# Go to Actions → Generate Video Walkthrough → Run workflow
```

#### Usage in Individual Repositories

Add to your repository's `.github/workflows/walkthrough.yml`:

```yaml
name: Generate Walkthrough
on:
  workflow_dispatch:
  push:
    branches: [main, develop]

jobs:
  generate:
    uses: Ivviiviivvi/.github/.github/workflows/org-walkthrough-generator.yml@main
    with:
      duration: "60"
      voiceover_style: "professional"
      focus_areas: "authentication, dashboard, reporting"
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Learn More:**

- [Video Walkthrough Guide](.github/WALKTHROUGH_GUIDE.md) - Complete documentation
- [Configuration Reference](.github/walkthrough-config.yml) - All available settings
- [Bootstrap Script](scripts/bootstrap-walkthrough-org.sh) - Organization deployment

### Automated PR Merging - The Eternal Solution ✨

**Problem**: Cannot programmatically merge PRs without GitHub API credentials  
**Solution**: Built-in `GITHUB_TOKEN` with zero configuration needed

#### Quick Start

```bash
# Enable auto-merge for any PR
gh pr edit <PR#> --add-label "auto-merge"

# Or include [auto-merge] in the PR title
gh pr create --title "[auto-merge] Your feature"
```

**Features:**
- ✅ **Zero Setup** - Works immediately with built-in workflows
- ✅ **No Tokens** - Uses GitHub's native `GITHUB_TOKEN`
- ✅ **Fully Automated** - Monitors and merges 24/7
- ✅ **Safe** - Respects all branch protection rules
- ✅ **Eternal** - No maintenance required

**Documentation:**
- 📖 [Complete Guide](docs/workflows/AUTO_MERGE_GUIDE.md) - Full documentation with examples
- 🚀 [Quick Reference](docs/workflows/AUTO_MERGE_QUICK_REF.md) - 3-step setup guide
- 🔧 [Reusable Template](workflow-templates/auto-merge-reusable.yml) - Use in any repo

**Workflows Included:**
- `.github/workflows/auto-merge.yml` - Main auto-merge orchestrator
- `.github/workflows/auto-enable-merge.yml` - Auto-enables merge for qualifying PRs

### 🤖 Automated PR Lifecycle Management (NEW!)

**Complete automation from Draft → Ready → Merge with batch operations for AI agents.**

The PR Lifecycle Management system provides comprehensive automation for managing high volumes of PRs, especially from AI agents like Jules. It handles the complete PR lifecycle automatically while preserving all data and functionality.

#### Key Features

✅ **Draft to Ready Conversion** - Auto-converts draft PRs from trusted AI agents when checks pass  
✅ **Suggestion Extraction** - Extracts actionable items from PR comments into TODO lists  
✅ **Batch Operations** - Process multiple PRs simultaneously with filters  
✅ **Full Pipeline** - Complete draft → ready → merge automation  
✅ **Data Preservation** - Maintains all PR data, comments, and context  

#### Quick Start

```bash
# Convert all Jules's draft PRs and merge ready ones
gh workflow run batch-pr-lifecycle.yml \
  -f action=full-pipeline \
  -f author_filter=Jules

# Extract suggestions from a PR into a TODO file
# (comment on any PR with)
/implement-suggestions

# Auto-convert a specific draft PR to ready
gh workflow run draft-to-ready-automation.yml -f pr_number=123
```

**Common Use Cases:**

1. **AI Agent PR Cleanup** - Jules creates 50 draft PRs → automatically convert to ready → merge when passing
2. **Suggestion Implementation** - PR has 30 comments with suggestions → extract to TODO file → track implementation
3. **Batch Operations** - Process all PRs with specific label simultaneously
4. **Scheduled Cleanup** - Daily automatic processing of accumulated PRs

**Documentation:**
- 📖 [Complete Guide](docs/PR_LIFECYCLE_AUTOMATION.md) - Full documentation with examples
- 🚀 [Quick Reference](docs/PR_LIFECYCLE_AUTOMATION.md#quick-start) - Common workflows
- 🔧 [Configuration Guide](docs/PR_LIFECYCLE_AUTOMATION.md#configuration) - Labels and settings

**Workflows Included:**
- `.github/workflows/draft-to-ready-automation.yml` - Auto-convert draft PRs
- `.github/workflows/pr-suggestion-implementation.yml` - Extract and track suggestions
- `.github/workflows/batch-pr-lifecycle.yml` - Unified batch PR processing

**Integration:**
Works seamlessly with existing workflows (`auto-merge.yml`, `pr-task-catcher.yml`, `pr-batch-merge.yml`)

### Organization-Wide Workflow Dispatch 🚀

**Centrally trigger workflows across all organization repositories.**

The Organization-Wide Workflow Dispatch workflow enables you to trigger workflows across all repositories in your organization from a single location. This is perfect for organization-wide operations like security scans, health checks, CI/CD updates, and batch maintenance tasks.

#### Key Features

✅ **Flexible Repository Targeting** - Target all repos, specific repos, or exclude specific repos
✅ **Smart Discovery** - Automatically discovers repos and verifies workflow existence
✅ **Safety Features** - Dry-run mode, rate limiting, and comprehensive error handling
✅ **Custom Inputs** - Pass JSON inputs to target workflows
✅ **Detailed Reporting** - Success/failure tracking with downloadable results

#### Quick Start

```bash
# Dry run to preview which repos will be targeted
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="ci.yml" \
  -f dry_run=true

# Trigger security scans across all active repos
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="security-scan.yml" \
  -f dry_run=false

# Target specific repositories with custom inputs
gh workflow run org-wide-workflow-dispatch.yml \
  -f workflow_file="deploy.yml" \
  -f target_repos="repo1,repo2,repo3" \
  -f workflow_inputs='{"environment":"production"}' \
  -f dry_run=false
```

**Use Cases:**
- 🔒 **Security Scans** - Run security audits across all repositories
- 🏥 **Health Checks** - Verify repository health and compliance
- 🔄 **CI/CD Updates** - Trigger synchronized build and deploy operations
- 🧹 **Maintenance Tasks** - Batch updates and cleanup operations
- 📊 **Data Collection** - Gather metrics from all repositories

**Documentation:**
- 📖 [Complete Guide](docs/workflows/ORG_WIDE_WORKFLOW_DISPATCH.md) - Full documentation with examples
- 🔧 [Workflow Template](workflow-templates/org-health-check.yml) - Example dispatchable workflow
- 🎯 [Main Workflow](.github/workflows/org-wide-workflow-dispatch.yml) - Organization dispatcher

**Workflow Included:**
- `.github/workflows/org-wide-workflow-dispatch.yml` - Main organization-wide dispatcher

### Repository Quality and Metadata Management 🎨

**Automated Badge Management** - Keep your repositories looking professional with automatically generated and maintained badges.

#### Badge Management Workflow

**Features:**
- ✅ **Auto-Detection** - Automatically detects languages, frameworks, and tools
- ✅ **Comprehensive Badges** - CI status, license, languages, stats, Docker, and more
- ✅ **Smart Placement** - Inserts badges in README with customizable position
- ✅ **Zero Config** - Works out of the box with sensible defaults
- ✅ **Customizable** - Fine-tune via `.github/badge-config.yml`

**Usage:**

```yaml
# Trigger manually for any repository
on:
  workflow_dispatch:

# Or include as part of your CI
jobs:
  badges:
    uses: ivviiviivvi/.github/.github/workflows/badge-management.yml@main
```

**Configuration:** [`.github/badge-config.yml`](.github/badge-config.yml)

#### Bio and Description Completions Workflow

**Features:**
- ✅ **Organization-Wide Auditing** - Scans all repositories for missing descriptions
- ✅ **Profile Completeness** - Checks organization profile and metadata
- ✅ **Smart Suggestions** - Generates description suggestions from repository content
- ✅ **Automated Issues** - Creates issues for incomplete metadata
- ✅ **Weekly Reports** - Scheduled audits with completion metrics
- ✅ **Agent Integration** - Works with completionism-specialist agent

**Audit Coverage:**
- Repository descriptions (minimum length, quality checks)
- Repository topics/tags (recommended 3-5)
- Website URLs and homepage links
- Organization profile completeness
- Community health files
- README.md presence and quality

**Usage:**

```bash
# Trigger a manual audit
gh workflow run bio-description-completions.yml

# Audit specific scope
gh workflow run bio-description-completions.yml -f scope=repositories
```

**Configuration:** [`.github/completions-config.yml`](.github/completions-config.yml)

**Learn More:**
- 🎨 [Badge Management Workflow](.github/workflows/badge-management.yml)
- 📋 [Bio Completions Workflow](.github/workflows/bio-description-completions.yml)
- ⚙️ [Badge Configuration](.github/badge-config.yml)
- 📝 [Completions Configuration](.github/completions-config.yml)

### Community Health Files

These files establish standards for community interaction and contribution acros
s all repositories:

| File                                          | Purpose                                        |
| --------------------------------------------- | ---------------------------------------------- |
| [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md) | Standards for respectful community interaction |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md)       | Guidelines for contributing to our projects    |
| [SECURITY.md](docs/SECURITY.md)               | Security policy and vulnerability reporting    |
| [SUPPORT.md](docs/SUPPORT.md)                 | How to get help and support                    |
| [LICENSE](LICENSE)                            | MIT License for our projects                   |
| [FUNDING.yml](FUNDING.yml)                    | Funding and sponsorship configuration          |
| [GOVERNANCE.md](docs/GOVERNANCE.md)           | Project governance and decision-making         |
| [MANIFESTO.md](docs/MANIFESTO.md)             | Our core principles and values                 |

### Documentation & Guides

All our documentation and guides are located in the `docs/` directory. Highlights include:

| Document                                                                           | Description                                                  |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [VERSION_CONTROL_STANDARDS.md](docs/reference/VERSION_CONTROL_STANDARDS.md)        | Organization-wide version control and branching standards    |
| [logical-branch-policy.md](.github/logical-branch-policy.md)                       | "Main only" branch model policy with cleanup automation      |
| [STYLE_GUIDE.md](docs/guides/STYLE_GUIDE.md)                                       | Comprehensive English language and documentation style guide |
| [ARCHIVAL_STRATEGY.md](docs/reference/ARCHIVAL_STRATEGY.md)                        | Version archival, maintenance branches, and preservation     |
| [COMMUNITY_AGENTS.md](docs/guides/COMMUNITY_AGENTS.md)                             | Community engagement, coordination, and monitoring agents    |
| [AGENT_ARCHITECTURE_GUIDE.md](docs/AGENT_ARCHITECTURE_GUIDE.md)                    | Comprehensive guide for building and deploying agents        |
| [AI_IMPLEMENTATION_GUIDE.md](docs/AI_IMPLEMENTATION_GUIDE.md)                      | AI-driven organization management guide                      |
| [GITHUB_COPILOT_ACTIONS_SETUP.md](docs/GITHUB_COPILOT_ACTIONS_SETUP.md)            | GitHub Copilot Actions setup and troubleshooting             |
| [WALKTHROUGH_ANNOUNCEMENT.md](docs/WALKTHROUGH_ANNOUNCEMENT.md)                    | Autonomous walkthrough generation system guide               |
| [SECRETS_SETUP.md](docs/SECRETS_SETUP.md)                                          | API keys and integrations setup for walkthrough system       |
| [BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md)                                  | Branch protection rules and configuration                    |
| [REPOSITORY_SETUP_CHECKLIST.md](docs/REPOSITORY_SETUP_CHECKLIST.md)                | New repository setup checklist                               |
| [LABELS.md](docs/LABELS.md)                                                        | Standard label set for consistent tagging                    |
| [TESTING.md](docs/TESTING.md)                                                      | Testing standards and best practices                         |
| [PR_AUTOMATION.md](docs/automation/PR_AUTOMATION.md)                               | Automated PR creation, push, and merge system                |
| [AI_IMPLEMENTATION_NOTES.txt](docs/guides/AI_IMPLEMENTATION_NOTES.txt)             | Complete AI GitHub management protocol                       |
| [REPOSITORY_PURPOSE_ANALYSIS.md](docs/architecture/REPOSITORY_PURPOSE_ANALYSIS.md) | Analysis of repository appropriateness for function set      |

### Issue Templates

Comprehensive templates to help contributors submit high-quality issues:

- **Bug Reports** - Both classic markdown and modern form-based templates
- **Feature Requests** - Structured templates for proposing new features
- **Documentation** - Template for documentation improvements
- **Questions** - Template for asking questions
- **Walkthrough Requests** - Request custom video walkthroughs for applications ([Guide](docs/WALKTHROUGH_ANNOUNCEMENT.md))

Configuration: [ISSUE_TEMPLATE/config.yml](ISSUE_TEMPLATE/config.yml)

### Pull Request Templates

Specialized templates for different types of contributions:

- **Default Template** - [PULL_REQUEST_TEMPLATE.md](docs/PULL_REQUEST_TEMPLATE.md)
- **Bug Fix** - [PULL_REQUEST_TEMPLATE/bug_fix.md](PULL_REQUEST_TEMPLATE/bug_fix.md)
- **Feature** - [PULL_REQUEST_TEMPLATE/feature.md](PULL_REQUEST_TEMPLATE/feature.md)
- **Documentation** - [PULL_REQUEST_TEMPLATE/documentation.md](PULL_REQUEST_TEMPLATE/documentation.md)
- **Refactoring** - [PULL_REQUEST_TEMPLATE/refactoring.md](PULL_REQUEST_TEMPLATE/refactoring.md)
- **Performance** - [PULL_REQUEST_TEMPLATE/performance.md](PULL_REQUEST_TEMPLATE/performance.md)

💡 **Tip**: Select a specific template by adding `?template=<name>.md` to the PR URL

### Workflow Templates

Reusable GitHub Actions workflows ready to use in any repository:

| Template                                                            | Purpose                               | Use Case                        |
| ------------------------------------------------------------------- | ------------------------------------- | ------------------------------- |
| [ci.yml](workflow-templates/ci.yml)                                 | Basic CI pipeline                     | Building and testing            |
| [security-scan.yml](workflow-templates/security-scan.yml)           | CodeQL analysis                       | Vulnerability scanning          |
| [stale-management.yml](workflow-templates/stale-management.yml)     | Stale issue and PR management         | Keeping repositories clean      |
| [dependency-updates.yml](workflow-templates/dependency-updates.yml) | Automated dependency update workflows | Managing dependencies           |
| [deployment.yml](workflow-templates/deployment.yml)                 | Deployment pipeline                   | Staging and production releases |
| [repository-bootstrap.yml](workflow-templates/repository-bootstrap.yml) | Repository feature setup              | Automating repository configuration |

💡 **New:** The **repository-bootstrap** workflow automates setup of repository features (Issues, Projects, Discussions, Wiki), creates standard labels, copies workflow templates, and configures branch protection. See [Repository Bootstrap Documentation](docs/workflows/REPOSITORY_BOOTSTRAP.md).

#### Organization Workflows

Advanced workflows for organization-wide automation:

| Workflow                                                                                        | Purpose                                   | Trigger                   |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------- |
| [repository-bootstrap.yml](.github/workflows/repository-bootstrap.yml)                         | Automate repository feature setup         | Manual, workflow_call     |
| [generate-walkthrough.yml](.github/workflows/generate-walkthrough.yml)                         | Generate video walkthroughs               | Manual, code changes      |
| [org-walkthrough-generator.yml](.github/workflows/org-walkthrough-generator.yml)               | Reusable video generation workflow        | Called by other workflows |
| [deploy-to-pages-live.yml](.github/workflows/deploy-to-pages-live.yml)                         | Deploy live apps to GitHub Pages          | Push to main, manual      |
| [collect-deployment-metadata.yml](.github/workflows/collect-deployment-metadata.yml)           | Collect deployment metadata (reusable)    | Workflow run, workflow_call |
| [generate-pages-index.yml](.github/workflows/generate-pages-index.yml)                         | Generate gallery index from all org repos | Schedule, repository dispatch |
| [badge-management.yml](.github/workflows/badge-management.yml)                                 | Generate and manage repository badges     | Push, PR, manual, workflow_call |
| [bio-description-completions.yml](.github/workflows/bio-description-completions.yml)           | Audit and complete repo/org descriptions  | Weekly schedule, manual   |

See [Repository Bootstrap Guide](docs/workflows/REPOSITORY_BOOTSTRAP.md), [Video Walkthrough Guide](.github/WALKTHROUGH_GUIDE.md) and [Deployment Metadata Collection Guide](docs/workflows/DEPLOYMENT_METADATA_COLLECTION.md) for detailed documentation.

#### 🚀 Workflow Optimization (NEW!)

**All workflows have been optimized for security, performance, and cost efficiency.**

- **[Workflow Standards](.github/WORKFLOW_STANDARDS.md)**: Comprehensive standards and best practices
- **[Optimization Report](.github/WORKFLOW_OPTIMIZATION_REPORT.md)**: Detailed metrics and analysis  
- **[Quick Start Guide](.github/WORKFLOW_OPTIMIZATION_QUICKSTART.md)**: Get started with optimized workflows

**Key Improvements:**
- ✅ **Security**: SHA-pinned actions, minimal permissions, deprecated syntax removed
- ✅ **Performance**: 30-60% faster builds with caching and path filters
- ✅ **Cost**: 25-32% reduction (estimated $225-325/month savings)
- ✅ **Reliability**: Timeouts, concurrency controls, better error handling

**Stats:** 8/73 workflows optimized | 83% reduction in health check costs | 0 deprecated syntax

### Automation Configuration

- **[dependabot.yml](dependabot.yml)** - Organization-wide Dependabot configurat
  ion for:
  - npm (JavaScript/Node.js)
  - pip (Python)
  - GitHub Actions
  - Docker
  - Go modules
  - Composer (PHP)

### Organization Profile

The [profile/README.md](profile/README.md) file is displayed on our organization
's public profile page.

## Getting Started

### For New Repositories

1. **Automatic Inheritance**: New repositories automatically inherit community h
   ealth files from this repository if they don't have their own versions.

2. **Using Workflow Templates**:

   - Navigate to **Actions → New workflow** in your repository
   - Look for templates in the "By your organization" section
   - Select, customize, and commit the workflow

3. **Setup Checklist**: Follow the [Repository Setup Checklist](docs/REPOSITORY_SETUP_CHECKLIST.md) for comprehensive guidance.

### For Existing Repositories

1. **Adopt Standards**: Review organization standards from this repository
2. **Enable Workflows**: Copy desired workflow templates to `.github/workflows/` in your repo
3. **Configure Dependabot**: Copy [dependabot.yml](dependabot.yml) to `.github/` in your repository
4. **Apply Labels**: Use [LABELS.md](docs/LABELS.md) to standardize issue labels
5. **Enable Branch Protection**: Follow [BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md) guidelines

### Customizing Templates

Individual repositories can override these defaults by creating their own versio
ns of any file. The repository-level file will take precedence over the organiza
tion default.

## Repository Structure

```text
.github/
├── .config/                                # Configuration files
│   ├── renovate.json                       # Renovate bot configuration
│   ├── .releaserc.json                     # Semantic release config
│   └── mouthpiece-config.example.json      # Mouthpiece filter config example
├── docs/                                   # Documentation hub
│   ├── architecture/                       # Architecture & design docs
│   │   ├── AI_CODE_INTELLIGENCE.md
│   │   ├── AGENTSPHERE_GITHUB_PAGES_IMPLEMENTATION.md
│   │   ├── CONTEXT_HANDOFF_IMPLEMENTATION.md
│   │   ├── LOGICAL_EXPANSIONS.md
│   │   └── REPOSITORY_PURPOSE_ANALYSIS.md
│   ├── automation/                         # Automation documentation
│   │   ├── AUTOMATION_MASTER_GUIDE.md
│   │   ├── BRANCH_AUTOMATION_LOGIC_REVIEW.md
│   │   └── PR_AUTOMATION.md
│   ├── guides/                             # How-to guides & best practices
│   │   ├── AI_IMPLEMENTATION_NOTES.txt
│   │   ├── BEST_PRACTICES.md
│   │   ├── CLAUDE.md
│   │   ├── COMMUNITY_AGENTS.md
│   │   ├── DOCKER_BEST_PRACTICES.md
│   │   ├── GITHUB_APPS_INTEGRATIONS.md
│   │   ├── MARKDOWN_STYLE_GUIDE.md
│   │   ├── QUICK_START.md
│   │   └── STYLE_GUIDE.md
│   ├── reference/                          # Reference documentation
│   │   ├── ARCHIVAL_STRATEGY.md
│   │   ├── SECURITY_ADVANCED.md
│   │   ├── SEMANTIC_VERSIONING.md
│   │   └── VERSION_CONTROL_STANDARDS.md
│   ├── workflows/                          # Workflow documentation
│   │   ├── AI_RAPID_WORKFLOW.md
│   │   ├── BRANCH_STRATEGY.md
│   │   ├── GIT_WORKFLOW.md
│   │   ├── RAPID_WORKFLOW_QUICK_REF.md
│   │   └── RELEASE_PROCESS.md
│   ├── AGENT_ARCHITECTURE_GUIDE.md         # Agent development guide
│   ├── AGENT_REGISTRY.md                   # Complete agent catalog
│   ├── AI_IMPLEMENTATION_GUIDE.md          # AI management implementation
│   ├── BRANCH_PROTECTION.md                # Branch protection setup
│   ├── CHANGELOG.md                        # Repository changelog
│   ├── CODE_OF_CONDUCT.md                  # Community standards
│   ├── CONTRIBUTING.md                     # Contribution guidelines
│   ├── CONTRIBUTORS.md                     # Contributor acknowledgments
│   ├── GITHUB_COPILOT_ACTIONS_SETUP.md     # Copilot Actions setup
│   ├── GITHUB_PAGES_SETUP.md               # GitHub Pages configuration
│   ├── GOVERNANCE.md                       # Governance model
│   ├── LABELS.md                           # Standard labels
│   ├── MANIFESTO.md                        # Organization manifesto
│   ├── MOUTHPIECE_README.md                # Mouthpiece system overview
│   ├── MOUTHPIECE_SYSTEM.md                # Complete Mouthpiece docs
│   ├── POSTING_WALKTHROUGH_ANNOUNCEMENT.md # Walkthrough announcements
│   ├── PULL_REQUEST_TEMPLATE.md            # Default PR template
│   ├── README.agents.md                    # Agents documentation
│   ├── README.chatmodes.md                 # Chat modes documentation
│   ├── README.collections.md               # Collections documentation
│   ├── README.instructions.md              # Instructions documentation
│   ├── README.prompts.md                   # Prompts documentation
│   ├── REPOSITORY_SETUP_CHECKLIST.md       # New repo setup
│   ├── SECRETS_SETUP.md                    # Secrets configuration
│   ├── SECURITY.md                         # Security policy
│   ├── SUPPORT.md                          # Support information
│   ├── TESTING.md                          # Testing standards
│   ├── The Living Document System.pdf      # Living document system
│   └── WALKTHROUGH_ANNOUNCEMENT.md         # Walkthrough system guide
├── .github/
│   ├── copilot-instructions.md             # Copilot code review rules
│   ├── dependabot.yml                      # Dependabot configuration
│   └── workflows/                          # GitHub Actions workflows
├── agents/                                 # GitHub Copilot custom agents
├── chatmodes/                              # GitHub Copilot chat modes
├── chaos-zone/                             # Temporary workspace
│   ├── chats/                              # Chat transcripts
│   ├── drafts/                             # Work-in-progress docs
│   ├── ideas/                              # Brainstorming notes
│   └── misc/                               # Miscellaneous content
├── collections/                            # Curated Copilot collections
├── context-handoff/                        # Context handoff system
├── instructions/                           # Copilot coding instructions
├── ISSUE_TEMPLATE/                         # Issue templates
├── observability/                          # Monitoring & observability
├── profile/                                # Organization profile
├── prompts/                                # GitHub Copilot prompts
├── PULL_REQUEST_TEMPLATE/                  # PR templates
├── reports/                                # Health reports & analytics
├── scripts/                                # Automation scripts
├── workflow-templates/                     # Reusable workflow templates
├── README.md                               # This file
└── PULL_REQUEST_TEMPLATE.md                # Default PR template
```

## AI-Driven Organization Management

This organization implements an advanced AI-driven GitHub management system with
8 core modules:

1. **Organization & Repository Administration** - Setup, access control, and bra
   nch protection
2. **Project Management & Workflow Automation** - Boards, issues, labels, and au
   tomation
3. **CI/CD & Development Lifecycle** - Build pipelines, testing, and deployment
4. **Security & Compliance Operations** - Vulnerability management and complianc
   e
5. **Documentation & Knowledge Base** - Maintaining comprehensive documentation
6. **Ecosystem Integration & Architecture** - Monitoring service dependencies
7. **Observability & System Health** - Analytics and system monitoring
8. **Strategic Analysis & Risk Mitigation** - Proactive risk identification

Read the full protocol: [AI Implementation Notes](docs/guides/AI_IMPLEMENTATION_NOTES.txt) | [Implementation Guide](docs/AI_IMPLEMENTATION_GUIDE.md)

### Active Health Monitoring

The organization now features **automated health monitoring** that brings the AI protocol to life:

- **🔍 Web Crawler** - Continuously analyzes organization health, validates documentation links, and maps the ecosystem
- **📊 Health Dashboard** - Real-time visualization of repository health, workflow coverage, and Copilot customizations
- **🔦 Blind Spot Detection** - Identifies unknown risks and unmaintained areas
- **💥 Shatter Point Analysis** - Detects single points of failure in workflows and infrastructure
- **⚡ Automated Reporting** - Weekly health reports with critical issue alerts

**Current Stats**: 32 workflows • 324 Copilot customizations • 109 technologies supported

📊 View the [Live Dashboard](reports/DASHBOARD.md) | 🛠️ [Scripts Documentation](scripts/README.md)

## Key Features

### PR Automation (NEW!)

- **Auto PR Creation**: Automatically creates PRs when feature branches are pushed
- **Auto Merge**: Intelligently merges PRs when all requirements are met
- **Conflict Resolution**: Automatically resolves merge conflicts when possible
- **Branch Cleanup**: Removes merged branches automatically
- **Comprehensive Documentation**: See [PR_AUTOMATION.md](docs/automation/PR_AUTOMATION.md) for details

### Automated Security

- **Dependabot**: Automatic dependency updates across multiple ecosystems
- **CodeQL Analysis**: Continuous security scanning for vulnerabilities
- **Branch Protection**: Enforced protection rules on production branches
- **Secret Scanning**: Detection of hardcoded secrets (where enabled)

### Quality Assurance

- **Standardized Templates**: Consistent issue and PR formats
- **Code Review Guidelines**: Built into PR templates
- **Testing Standards**: Documented in [TESTING.md](docs/TESTING.md)
- **Contribution Guidelines**: Clear expectations in [CONTRIBUTING.md](docs/CONTRIBUTING.md)

### Developer Experience

- **Workflow Templates**: Ready-to-use CI/CD pipelines
- **Stale Issue Management**: Automated cleanup of inactive items
- **Comprehensive Documentation**: Setup guides and best practices
- **Label Standards**: Consistent categorization across repositories

## 🤝 Contributing

We welcome contributions from everyone! Here's how to get started:

1. **Read the Guidelines**: Check [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed instructions
2. **Follow the Code of Conduct**: All interactions must follow our [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md)
3. **Use Templates**: Submit issues and PRs using our templates
4. **Ask Questions**: Don't hesitate to open a question issue or discussion

### Improving This Repository

To enhance our organization's GitHub management:

- Propose changes via pull requests
- Use appropriate PR templates
- Ensure changes align with our AI GitHub Management Protocol
- Update documentation when adding new features

## 📚 Resources

### GitHub Documentation

- [About default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [About organization profiles](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile)
- [Creating workflow templates](https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization)
- [Dependabot configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

### Organization Documentation

- [Manifesto](docs/MANIFESTO.md) - Our core principles and values
- [Governance](docs/GOVERNANCE.md) - How we make decisions
- [Support](docs/SUPPORT.md) - Getting help
- [Security](docs/SECURITY.md) - Reporting vulnerabilities

## 📄 License

This repository and all default community health files are provided under the [M
IT License](LICENSE).

## 💬 Support

Need help? Have questions?

- 📖 Check our [Support Documentation](docs/SUPPORT.md) for detailed guidance
- 🐛 Report issues using our [issue templates](ISSUE_TEMPLATE/)
- 📧 Contact repository maintainers through GitHub
- 💬 For general discussions, check if [GitHub Discussions](https://github.com/orgs/ivi374forivi/discussions) are enabled

---

Built with ❤️ by the ivi374forivi community.
