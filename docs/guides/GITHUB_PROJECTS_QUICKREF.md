# GitHub Projects Quick Reference

> **One-page guide for using GitHub Projects in the {{ORG_NAME}} organization**

## 🎯 Available Projects

| Icon | Project                       | For...                                       |
| ---- | ----------------------------- | -------------------------------------------- |
| 🤖   | **AI Framework Development**  | Agents, MCP servers, custom instructions     |
| 📚   | **Documentation & Knowledge** | Docs, guides, tutorials                      |
| ⚙️   | **Workflow & Automation**     | CI/CD, GitHub Actions, automation            |
| 🔒   | **Security & Compliance**     | Security audits, vulnerabilities, compliance |
| 🏗️   | **Infrastructure & DevOps**   | Cloud resources, IaC, deployments            |
| 👥   | **Community & Engagement**    | Support, contributors, community             |
| 🚀   | **Product Roadmap**           | Features, releases, strategy                 |

**Access:** https://github.com/orgs/{{ORG_NAME}}/projects

______________________________________________________________________

## 📋 Common Tasks

### Adding an Issue to a Project

**Method 1: From Issue Page**

1. Open the issue
1. Look for "Projects" in the right sidebar
1. Click "+ Add to project"
1. Select the project
1. Item appears in "New" or "Backlog" column

**Method 2: From Project Board**

1. Open the project
1. Click "+ Add item" at bottom of any column
1. Search for issue by number or title
1. Click to add

**Method 3: Automatic (if configured)**

- Issues with specific labels auto-add to projects
- Example: `agent` label → AI Framework project

### Updating Item Status

**Method 1: Drag and Drop**

1. Open board view
1. Drag item to new column
1. Status updates automatically

**Method 2: Edit Field**

1. Click on item
1. Find "Status" field
1. Select new value from dropdown

**Method 3: Via PR (automatic)**

- Opening PR → Status: Testing
- Merging PR → Status: Completed

### Filtering Items

**By Field:**

```
Status is "In Progress"
Priority is "High" or "Critical"
Type is "Agent"
```

**By Label:**

```
label:bug
label:documentation
label:agent
```

**By Assignee:**

```
assignee:@me
no:assignee
```

**By Date:**

```
created:>2026-01-01
updated:<2026-01-10
```

______________________________________________________________________

## 🎨 Project-Specific Quick Tips

### 🤖 AI Framework Development

**Labels to use:**

- `agent` - Agent development
- `mcp-server` - MCP server work
- `custom-instructions` - Instructions authoring

**Key fields:**

- Type: Agent/MCP Server/Instructions
- Language: Python/TypeScript/etc.
- Testing Status: Track test progress

**Views:**

- 📋 Board - Development pipeline
- 🗂️ Agent Catalog - All agents
- 🔌 MCP Server Development - SDK work

### 📚 Documentation & Knowledge

**Labels to use:**

- `documentation` - Doc updates
- `stale-docs` - Needs refresh

**Key fields:**

- Document Type: Guide/Tutorial/Reference
- Completeness: Draft/Complete
- Next Review Date: Schedule updates

**Views:**

- 📋 Board - Writing pipeline
- 🔍 Needs Attention - Updates needed
- 📚 Catalog - All docs organized

### ⚙️ Workflow & Automation

**Labels to use:**

- `workflow` - GitHub Actions
- `automation` - Scripts/tools
- `workflow-failing` - Needs fix

**Key fields:**

- Workflow Type: CI/CD/Testing/Security
- Success Rate: Track reliability
- Impact: Organization/Repo/Team

**Views:**

- 🏭 Active Workflows - Current state
- ⚠️ Needs Attention - Problems
- 📊 Analytics - Metrics

### 🔒 Security & Compliance

**Labels to use:**

- `security` - Security issues
- `vulnerability` - CVEs
- `sla-breach` - Urgent attention

**Key fields:**

- Severity: Critical/High/Medium/Low
- SLA Status: Within/At Risk/Breached
- Resolution Target: Due date

**Views:**

- 🚨 Critical Dashboard - High priority
- 📊 Remediation Pipeline - Fix progress
- ⏰ SLA Dashboard - Deadlines

**⚠️ Note:** This project is private

### 🏗️ Infrastructure & DevOps

**Labels to use:**

- `infrastructure` - IaC work
- `cloud` - Cloud resources
- `production-deploy` - Prod changes

**Key fields:**

- Infrastructure Type: Cloud/Database/Network
- Cloud Provider: Azure/AWS/GCP
- Environment: Prod/Staging/Dev

**Views:**

- ☁️ Cloud Resources - By provider
- 💰 Cost Management - Budget tracking
- 🚨 Production - Critical systems

### 👥 Community & Engagement

**Labels to use:**

- `good first issue` - Beginner-friendly
- `first-time-contributor` - New contributors
- `needs-response` - Awaiting reply

**Key fields:**

- Contributor Type: First-time/Returning
- Needs Mentor: Yes/No/Assigned
- Satisfaction: Track happiness

**Views:**

- 🙋 Support Requests - Active help
- 🆕 First-Time Contributors - Welcome!
- 🌟 Good First Issues - Easy starts

### 🚀 Product Roadmap

**Labels to use:**

- `enhancement` - New features
- `strategic` - Big initiatives
- `delayed` - Needs attention

**Key fields:**

- Initiative Type: Feature/Strategic/Release
- Quarter: Q1/Q2/Q3/Q4 2026
- Impact: Organization/Team
- Target Date: Deadline

**Views:**

- 🗓️ Timeline - Visual roadmap
- 📊 Current Quarter - Active work
- 🔥 Critical Path - High priority

______________________________________________________________________

## 🔔 Notifications

### Enabling Notifications

**For specific project:**

1. Go to project
1. Click "⋯" menu
1. Select "Manage notifications"
1. Choose notification level

**For items you're assigned:**

- Automatically notified of:
  - Status changes
  - Comments
  - Field updates
  - Due date approaches

### Notification Levels

- **All activity** - Every change
- **Participating** - Only items you're involved in
- **Ignoring** - No notifications

______________________________________________________________________

## 📊 Viewing Your Work

### Personal Dashboard

```
https://github.com/orgs/{{ORG_NAME}}/projects?query=is:open+assignee:@me
```

Shows all items assigned to you across all projects

### This Week's Tasks

In any project:

1. Open board view
1. Add filter: `assignee:@me`
1. Add filter: `updated:>1 week ago`
1. Bookmark this view

### Overdue Items

```
assignee:@me target-date:<today status:!"Completed"
```

______________________________________________________________________

## 🎯 Field Cheat Sheet

### Common Fields Across Projects

| Field              | Type   | Purpose                        |
| ------------------ | ------ | ------------------------------ |
| **Status**         | Select | Current stage in workflow      |
| **Priority**       | Select | Urgency level                  |
| **Owner/Assigned** | People | Who's responsible              |
| **Type**           | Select | Category of work               |
| **Target Date**    | Date   | Deadline or goal date          |
| **Dependencies**   | Text   | What this blocks/is blocked by |

### Color Codes

**Priority Colors:**

- 🔥 Red = Critical/Urgent
- ⚡ Orange = High
- 📊 Yellow = Medium
- 🔽 Gray = Low

**Status Colors:**

- 🟢 Green = Done/Completed/Approved
- 🟡 Yellow = In Progress/Active
- 🟠 Orange = Review/Testing
- 🔵 Blue = Planning/Research
- ⚪ Gray = Backlog/On Hold
- 🔴 Red = Blocked/Failed

______________________________________________________________________

## 💡 Pro Tips

### Keyboard Shortcuts

- `/` - Search/filter
- `e` - Edit item
- `c` - Close item
- `←→` - Navigate columns
- `?` - Show all shortcuts

### Quick Filters

Save these as bookmarks:

```
# My urgent work
assignee:@me priority:"🔥 Critical"

# Team's next sprint
status:"🎯 Planned" updated:>1 week

# Stale items
status:!"Completed" updated:<30 days

# Ready to deploy
status:"✅ Ready to Deploy"
```

### Bulk Operations

1. Select multiple items (Shift+Click)
1. Right-click
1. Choose action:
   - Change status
   - Update field
   - Add label
   - Close items

### Mobile Access

- GitHub Mobile app supports Projects
- View and update items on the go
- Get notifications on your phone

______________________________________________________________________

## 🆘 Need Help?

**Documentation:**

- [Full Implementation Guide](GITHUB_PROJECTS_IMPLEMENTATION.md)
- [Setup Instructions](../../src/automation/scripts/utils/README_PROJECTS.md)
- [GitHub's Projects Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects)<!-- link:docs.github_projects -->

**Support:**

- Ask in
  [Discussions](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->
- Open an
  [Issue](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
- Check [Workflow Documentation](../workflows/WORKFLOW_DESIGN.md)

**Training:**

- New user onboarding guide
- Video tutorials (coming soon)
- Weekly office hours (Fridays 2-3 PM)

______________________________________________________________________

## 📝 Quick Action Commands

### Via Issue/PR Comments

```
# Add to project
/project AI Framework

# Update status
/status In Progress

# Set priority
/priority High

# Assign to self
/assign @me
```

### Via GitHub CLI

```bash
# Add issue to project
gh project item-add PROJECT_NUMBER --url ISSUE_URL

# Update field
gh project field-update PROJECT_NUMBER ITEM_ID \
  --field-id FIELD_ID --value "In Progress"

# List my items
gh project item-list PROJECT_NUMBER --assignee @me
```

______________________________________________________________________

**🎉 You're ready to use GitHub Projects!**

Start by browsing projects at: https://github.com/orgs/{{ORG_NAME}}/projects

______________________________________________________________________

_Last Updated: January 18, 2026_\
_Print this page for quick reference at your
desk!_
