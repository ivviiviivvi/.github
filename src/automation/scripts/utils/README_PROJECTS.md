# GitHub Projects Setup

> **Complete guide to setting up and using the 7 comprehensive GitHub Projects**

This directory contains scripts and documentation for creating, configuring, and
managing GitHub Projects across the organization.

## 📋 Overview

We've designed **7 comprehensive GitHub Projects** to organize work across all
organizational domains:

| Project                          | Purpose                                        | Items Tracked                                     |
| -------------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| **🤖 AI Framework Development**  | Agent development, MCP servers, AI tooling     | 26+ agents, 11 language SDKs, custom instructions |
| **📚 Documentation & Knowledge** | Documentation maintenance and knowledge base   | 133+ documentation files                          |
| **⚙️ Workflow & Automation**     | CI/CD, GitHub Actions, process automation      | 98+ workflows, automation scripts                 |
| **🔒 Security & Compliance**     | Security audits, incident response, compliance | Vulnerabilities, incidents, audits                |
| **🏗️ Infrastructure & DevOps**   | Cloud resources, deployments, platform ops     | IaC, cloud resources, deployments                 |
| **👥 Community & Engagement**    | Open source community, contributor support     | Support requests, contributions                   |
| **🚀 Product Roadmap**           | Strategic planning, feature roadmap, releases  | Features, initiatives, releases                   |

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Set your GitHub token
export GH_TOKEN="your_github_personal_access_token"

# Run the Python configuration script
python3 scripts/configure-github-projects.py --org {{ORG_NAME}}

# This will:
# - Create all 7 projects
# - Configure custom fields
# - Set up field options
```

### Option 2: Manual Setup via GitHub UI

1. Navigate to https://github.com/orgs/{{ORG_NAME}}/projects
1. Click "New project"
1. Follow the configuration guide in
   [GITHUB_PROJECTS_IMPLEMENTATION.md](../../../../docs/guides/GITHUB_PROJECTS_IMPLEMENTATION.md)

### Option 3: Bash Script (Basic Setup)

```bash
# Run the bash script (creates projects only, no field configuration)
./scripts/create-github-projects.sh
```

## 📚 Documentation

- **[GITHUB_PROJECTS_IMPLEMENTATION.md](../../../../docs/guides/GITHUB_PROJECTS_IMPLEMENTATION.md)**
  \- Complete implementation guide with:

  - Detailed project configurations
  - Field definitions
  - View layouts
  - Automation rules
  - Implementation checklist

- **[GITHUB_PROJECTS_CONFIGURATION.md](../../../../docs/guides/GITHUB_PROJECTS_CONFIGURATION.md)**
  \- Step-by-step configuration guide

## 🔧 Scripts

### `configure-github-projects.py`

**Purpose:** Complete project setup with field configuration

**Features:**

- Creates projects via GraphQL API
- Configures custom fields
- Sets up single-select options
- Handles all field types (text, number, date, select)

**Usage:**

```bash
# Create all projects
export GH_TOKEN="your_token"
python3 configure-github-projects.py --org {{ORG_NAME}}

# Create specific projects only
python3 configure-github-projects.py --org {{ORG_NAME}} \
    --projects ai-framework documentation

# Dry run (show what would be done)
python3 configure-github-projects.py --org {{ORG_NAME}} --dry-run
```

**Requirements:**

- Python 3.8+
- `requests` library: `pip install requests`
- GitHub personal access token with `project:write` scope

### `create-github-projects.sh`

**Purpose:** Basic project creation via GitHub CLI

**Features:**

- Creates project shells
- Sets titles and descriptions
- Saves project IDs for later configuration

**Usage:**

```bash
./scripts/create-github-projects.sh
```

**Requirements:**

- GitHub CLI (`gh`) installed and authenticated
- Organization admin permissions

## 🔑 Authentication

### Creating a Personal Access Token

1. Go to https://github.com/settings/tokens
1. Click "Generate new token (classic)"
1. Set note: "GitHub Projects Configuration"
1. Select scopes:
   - ✅ `project` (all)
   - ✅ `repo` (all)
   - ✅ `admin:org` (read)
1. Click "Generate token"
1. Copy the token (you won't see it again!)

### Setting the Token

```bash
# Option 1: Using 1Password CLI (Recommended - Secure)
# Install: brew install --cask 1password-cli (macOS)
# Docs: https://developer.1password.com/docs/cli/get-started/
eval $(op signin)  # One-time authentication
export GH_TOKEN=$(op read "op://Private/GitHub PAT/credential")
echo "Token loaded: ${GH_TOKEN:0:4}..."  # Verify (shows first 4 chars)

# Adjust the 1Password reference to match your setup:
# - "Private" = your vault name
# - "GitHub PAT" = your item name
# - "credential" = field name
# Use: op item list --vault Private

# Option 2: Environment variable (temporary)
export GH_TOKEN="ghp_your_token_here"

# Option 3: Save to shell profile (persistent - less secure)
echo 'export GH_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc

# Option 4: Use GitHub CLI
gh auth login
# Then use: $(gh auth token)
```

## 📋 Implementation Phases

### Phase 1: Project Creation (Week 1)

✅ **Create Projects**

**Method 1: Automated 1Password deployment (Recommended)**

```bash
cd /workspace/scripts

# Dry run first to test
./deploy-with-1password.sh --dry-run

# Deploy for real
./deploy-with-1password.sh
```

This script automatically:

- Checks for 1Password CLI
- Signs in if needed
- Retrieves your GitHub PAT from 1Password
- Runs the Python configuration script
- Logs output to timestamped file

**Method 2: Manual Python script**

- Run automated setup script
- Verify all 7 projects exist
- Check project URLs and IDs

✅ **Configure Fields**

- Add custom fields
- Set field options
- Configure field types

✅ **Create Views**

- Board views (kanban)
- Table views (detailed)
- Roadmap views (timeline)
- Custom filtered views

**Status:** Ready for automation

### Phase 2: Automation Setup (Week 2)

🔄 **Built-in Automation**

- Status field triggers
- Label-based automation
- Assignment rules

🔄 **GitHub Actions Integration**

- Auto-add issues to projects
- Sync PR status
- Update project fields

🔄 **Workflow Rules**

- SLA tracking
- Stale item cleanup
- Notification triggers

**Status:** In progress

### Phase 3: Migration (Week 3)

⏳ **Existing Items**

- Add current issues
- Add active PRs
- Set initial status

⏳ **Team Training**

- Training materials
- Walkthrough sessions
- Documentation sharing

⏳ **Launch**

- Announce availability
- Monitor adoption
- Gather feedback

**Status:** Planned

### Phase 4: Optimization (Ongoing)

📊 **Metrics & Analytics**

- Track project usage
- Monitor automation effectiveness
- Measure cycle times

🔄 **Continuous Improvement**

- Adjust fields based on feedback
- Optimize views
- Refine automation rules

## 🎯 Project-Specific Details

### 🤖 AI Framework Development

**Focus:** Agent development, MCP servers, custom instructions

**Key Views:**

- Agent Catalog - All agents by category
- MCP Development - Language-specific servers
- Active Sprint - Current work
- Bug Tracking - Issues and fixes

**Automation:**

- Auto-label agent issues
- Move to testing when PR created
- Flag items without owners
- Notify on deployment ready

### 📚 Documentation & Knowledge

**Focus:** 133+ documentation files

**Key Views:**

- Documentation Catalog - All docs by type
- Needs Attention - Updates required
- By Category - Organized view
- Quick Wins - Easy improvements

**Automation:**

- Schedule reviews for new docs (90 days)
- Flag stale documentation (180 days)
- Notify on approval

### ⚙️ Workflow & Automation

**Focus:** 98+ GitHub Actions workflows

**Key Views:**

- Active Workflows - Current state
- Needs Attention - Low success rate
- Deployment Workflows - CD pipelines
- Analytics Dashboard - Metrics

**Automation:**

- Flag low success rate (\<80%)
- Move to monitoring after deploy

### 🔒 Security & Compliance

**Focus:** Security audits, vulnerability tracking

**Key Views:**

- Critical Dashboard - High severity items
- Remediation Pipeline - Fix progress
- SLA Dashboard - Time tracking
- Team Workload - Assignment view

**Automation:**

- Set SLA based on severity
- Flag SLA breaches
- Update status on fix

**Note:** This project is **private** by default.

### 🏗️ Infrastructure & DevOps

**Focus:** Infrastructure as code, cloud resources

**Key Views:**

- Cloud Resources - By provider
- Cost Management - Budget tracking
- Production Resources - Critical systems
- IaC Tracking - Terraform/Ansible

**Automation:**

- Flag production deployments
- Schedule maintenance reviews

### 👥 Community & Engagement

**Focus:** Open source community, contributor support

**Key Views:**

- Active Support Requests
- First-Time Contributors
- Good First Issues
- Community Health metrics

**Automation:**

- Welcome first-time contributors
- Flag slow response (>24h)

### 🚀 Product Roadmap

**Focus:** Strategic planning, feature roadmap

**Key Views:**

- Roadmap Timeline - Visual planning
- Current Quarter - Active initiatives
- Strategic Initiatives - High-level
- Critical Path - Dependencies

**Automation:**

- Flag delayed initiatives
- Request success metrics on launch

## 🛠️ Customization

### Adding New Fields

**Via Python Script:**

Edit `scripts/configure-github-projects.py`:

```python
"fields": {
    "My Custom Field": {
        "type": "single_select",
        "options": [
            {"name": "Option 1", "color": "GREEN"},
            {"name": "Option 2", "color": "BLUE"}
        ]
    }
}
```

**Via GraphQL API:**

```bash
gh api graphql -f query='
  mutation {
    createProjectV2Field(input: {
      projectId: "PROJECT_ID"
      dataType: SINGLE_SELECT
      name: "My Field"
      singleSelectOptions: [
        {name: "Value 1", color: GREEN}
      ]
    }) {
      projectV2Field {
        ... on ProjectV2SingleSelectField {
          id
          name
        }
      }
    }
  }
'
```

### Creating Custom Views

1. Open project in GitHub
1. Click "New view"
1. Choose layout: Board, Table, or Roadmap
1. Configure:
   - Filters
   - Grouping
   - Sorting
   - Visible fields
1. Save view

## 📊 Monitoring & Metrics

### Project Health Indicators

Track these metrics per project:

```python
# Items by status
active_items = items.filter(status__in=["In Progress", "Review"])
completion_rate = completed_items / total_items * 100

# Cycle time
avg_cycle_time = (closed_date - created_date).mean()

# Team engagement
comments_per_item = total_comments / total_items
```

### Automation Effectiveness

```python
# Automation rules triggered
rule_executions = automation_log.count()
successful_transitions = automation_log.filter(success=True).count()
success_rate = successful_transitions / rule_executions * 100
```

### Dashboard Queries

See
[GITHUB_PROJECTS_IMPLEMENTATION.md](../../../../docs/guides/GITHUB_PROJECTS_IMPLEMENTATION.md#success-metrics)
for GraphQL queries.

## 🐛 Troubleshooting

### Common Issues

**Issue:** Script fails with authentication error

**Solution:**

```bash
# Verify token is set
echo $GH_TOKEN

# Test token permissions
gh auth status

# If using GitHub CLI, refresh:
gh auth refresh -s project
```

______________________________________________________________________

**Issue:** Rate limit exceeded

**Solution:**

```bash
# Check rate limit
gh api rate_limit

# Add delay between operations
time.sleep(1)  # In Python script
```

______________________________________________________________________

**Issue:** Field creation fails

**Solution:**

- Verify field name is unique
- Check color codes are valid (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, PINK,
  GRAY)
- Ensure field type matches data

______________________________________________________________________

**Issue:** Projects not visible

**Solution:**

- Check organization/repository access
- Verify project visibility settings
- Confirm team permissions

## 🆘 Support

**Questions?**

- Open an issue:
  [GitHub Issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
- Start a discussion:
  [GitHub Discussions](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->

**Documentation:**

- [Complete Implementation Guide](../../../../docs/guides/GITHUB_PROJECTS_IMPLEMENTATION.md)
- [Configuration Guide](../../../../docs/guides/GITHUB_PROJECTS_CONFIGURATION.md)
- [Workflow Documentation](../../../../docs/workflows/WORKFLOW_DESIGN.md)

**GitHub Resources:**

- [Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)<!-- link:docs.github_projects -->
- [GraphQL API](https://docs.github.com/en/graphql)
- [Projects API Reference](https://docs.github.com/en/graphql/reference/objects#projectv2)

## 📝 Changelog

### 2026-01-18

- ✅ Created comprehensive project implementation plan
- ✅ Developed automated configuration scripts
- ✅ Documented all 7 project structures
- ✅ Added field definitions and view layouts
- ✅ Designed automation rules

### Next Steps

- [ ] Run automated setup
- [ ] Create project views
- [ ] Set up automation rules
- [ ] Migrate existing items
- [ ] Train team members

______________________________________________________________________

_Last Updated: January 18, 2026_
