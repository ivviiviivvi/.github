# GitHub Projects Guide

> **Comprehensive guide for using GitHub Projects (v2) in the Ivviiviivvi
> organization**

This guide provides an exhaustive framework for leveraging GitHub Projects to
manage work, track progress, and coordinate activities across the organization.

## Table of Contents

- [Overview](#overview)
- [Project Templates](#project-templates)
- [Project Views](#project-views)
- [Custom Fields](#custom-fields)
- [Automation](#automation)
- [Integration Patterns](#integration-patterns)
- [Best Practices](#best-practices)
- [Project Examples](#project-examples)

## Overview

GitHub Projects (v2) provides flexible, powerful project management with:

- **Multiple views** (table, board, roadmap, calendar)
- **Custom fields** for tracking any data
- **Automated workflows** via built-in automation
- **Cross-repository** issue and PR tracking
- **Real-time collaboration** and updates

### Projects vs Issues vs Discussions

| Feature       | Issues                      | Projects                          | Discussions             |
| ------------- | --------------------------- | --------------------------------- | ----------------------- |
| **Purpose**   | Track individual work items | Organize and track multiple items | Community conversation  |
| **Scope**     | Single task or bug          | Initiative or milestone           | Open-ended topics       |
| **Structure** | Linear, actionable          | Flexible, multi-view              | Threaded, collaborative |
| **Best For**  | Specific deliverables       | Project management                | Ideation and support    |

## Project Templates

### 1. 🚀 Product Roadmap

**Purpose**: Track features and releases across quarters\
**Views**: Roadmap, By
Quarter, By Status\
**Duration**: 6-12 months

**Custom Fields:**

- **Quarter** (Single select): Q1 2025, Q2 2025, Q3 2025, Q4 2025
- **Theme** (Single select): Performance, Security, UX, Infrastructure
- **Status** (Status): Planned, In Progress, In Review, Shipped
- **Priority** (Single select): P0, P1, P2, P3
- **Size** (Single select): XS, S, M, L, XL
- **Target Release** (Text)
- **Owner** (Person)

**Workflows:**

- Auto-set Quarter based on target date
- Move to "In Progress" when issue assigned
- Move to "Shipped" when PR merged
- Notify on quarter completion

**Board Layout:**

```
Backlog → Planned → In Progress → In Review → Shipped
```

### 2. 🐛 Bug Triage & Resolution

**Purpose**: Track and prioritize bug fixes\
**Views**: By Priority, By
Component, By Age\
**Duration**: Ongoing

**Custom Fields:**

- **Priority** (Single select): P0-Critical, P1-High, P2-Medium, P3-Low
- **Severity** (Single select): Blocker, Major, Minor, Trivial
- **Component** (Multiple select): Frontend, Backend, API, Database,
  Infrastructure
- **Affected Version** (Text)
- **Reproducibility** (Single select): Always, Sometimes, Once, Unable
- **Root Cause** (Single select): Code Bug, Configuration, Data, Environment,
  Unknown
- **Time to Fix** (Number) - in hours
- **Reporter Type** (Single select): User, Internal, Automated

**Workflows:**

- Auto-label by priority
- Auto-assign to component owners
- Escalate P0/P1 after 24h without update
- Close stale P3/P4 after 60 days
- Track time to resolution

**Board Layout:**

```
New → Triaged → Investigating → Fixing → Testing → Resolved
```

### 3. 📋 Sprint Planning

**Purpose**: Manage 2-week development sprints\
**Views**: Current Sprint, By
Assignee, Velocity Chart\
**Duration**: 2 weeks

**Custom Fields:**

- **Sprint** (Iteration): Sprint 1, Sprint 2, etc.
- **Story Points** (Number)
- **Type** (Single select): Feature, Bug, Chore, Spike
- **Epic** (Text): Links to epic issue
- **Status** (Status): Backlog, Todo, In Progress, Review, Done
- **Blocked** (Checkbox)
- **Blocker Reason** (Text)
- **Actual Points** (Number): Actuals vs estimates

**Workflows:**

- Auto-calculate sprint velocity
- Alert on sprint capacity exceeded
- Move to next sprint if incomplete
- Generate sprint report on completion

**Board Layout:**

```
Backlog → Sprint Planning → Current Sprint → Completed
```

### 4. 🏗️ Infrastructure & DevOps

**Purpose**: Track infrastructure work and incidents\
**Views**: By Environment,
By Service, Incident Board\
**Duration**: Ongoing

**Custom Fields:**

- **Environment** (Multiple select): Dev, Staging, Production
- **Service** (Single select): API, Database, Frontend, CDN, Auth, etc.
- **Type** (Single select): Incident, Maintenance, Improvement, Investigation
- **Severity** (Single select): SEV1, SEV2, SEV3, SEV4
- **Status** (Status): Detected, Investigating, Mitigating, Resolved,
  Post-Mortem
- **Impact** (Text): Number of users affected
- **MTTR** (Number): Mean time to resolution
- **RCA Complete** (Checkbox)

**Workflows:**

- Auto-create on monitoring alerts
- Escalate SEV1/2 to on-call
- Require post-mortem for SEV1/2
- Track SLA compliance

**Board Layout:**

```
Detected → Investigating → Mitigating → Resolved → Post-Mortem
```

### 5. 🎓 Onboarding & Training

**Purpose**: Track new contributor onboarding\
**Views**: By Phase, By Mentee,
By Skill\
**Duration**: Per cohort

**Custom Fields:**

- **Phase** (Single select): Week 1, Week 2, Week 3, Week 4, Ongoing
- **Mentee** (Person)
- **Mentor** (Person)
- **Skill Area** (Single select): Frontend, Backend, DevOps, Design,
  Documentation
- **Task Type** (Single select): Reading, Hands-on, Shadowing, Independent
- **Completion** (Number): Percentage complete
- **Status** (Status): Not Started, In Progress, Blocked, Complete
- **Feedback Given** (Checkbox)

**Workflows:**

- Assign mentor on start
- Progress through phases automatically
- Send reminders for stalled tasks
- Request feedback on completion

**Board Layout:**

```
Pre-Arrival → Week 1 → Week 2 → Week 3 → Week 4 → Alumni
```

### 6. 📚 Documentation Improvement

**Purpose**: Track documentation gaps and improvements\
**Views**: By Doc Type,
By Priority, By Audience\
**Duration**: Ongoing

**Custom Fields:**

- **Doc Type** (Single select): API, User Guide, Tutorial, Reference,
  Architecture
- **Audience** (Single select): End User, Contributor, Maintainer, Admin
- **Doc Status** (Status): Missing, Outdated, Needs Review, Up to Date
- **Priority** (Single select): Critical, High, Medium, Low
- **Difficulty** (Single select): Easy, Medium, Hard
- **Good First Issue** (Checkbox)
- **Last Updated** (Date)
- **Review Cycle** (Single select): Monthly, Quarterly, Yearly

**Workflows:**

- Flag outdated docs
- Request SME review
- Auto-link to related code
- Track doc coverage metrics

**Board Layout:**

```
Identified → Writing → Review → Published → Maintenance
```

### 7. 🔒 Security & Compliance

**Purpose**: Track security work and compliance requirements\
**Views**: By
Severity, By Compliance Area, Remediation Timeline\
**Duration**: Ongoing

**Custom Fields:**

- **Type** (Single select): Vulnerability, Compliance, Security Enhancement,
  Audit
- **Severity** (Single select): Critical, High, Medium, Low, Info
- **CVE** (Text): CVE identifier if applicable
- **Compliance** (Multiple select): GDPR, SOC2, HIPAA, PCI-DSS
- **Status** (Status): Identified, Assessing, Remediating, Verifying, Closed
- **SLA** (Date): Remediation deadline
- **Fix Version** (Text)
- **Verification Method** (Text)
- **False Positive** (Checkbox)

**Workflows:**

- Auto-create from security scans
- Escalate based on SLA
- Require verification before close
- Generate compliance reports

**Board Layout:**

```
New → Assessed → Scheduled → In Progress → Verification → Closed
```

### 8. 🌟 Community Engagement

**Purpose**: Track community initiatives and contributions\
**Views**: By
Initiative, By Contributor, By Status\
**Duration**: Ongoing

**Custom Fields:**

- **Initiative Type** (Single select): Event, Content, Outreach, Support,
  Recognition
- **Status** (Status): Idea, Planning, In Progress, Completed
- **Contributor** (Person)
- **Target Audience** (Multiple select): New Contributors, Active, Maintainers,
  Users
- **Reach** (Number): Estimated people impacted
- **Success Metric** (Text)
- **Budget Required** (Checkbox)
- **Partner Organizations** (Text)

**Workflows:**

- Track initiative completion rate
- Send thank-you notes
- Highlight contributions
- Generate community reports

**Board Layout:**

```
Ideas → Planning → Execution → Follow-up → Retrospective
```

### 9. ⚡ Performance Optimization

**Purpose**: Track performance improvements and benchmarks\
**Views**: By
Impact, By Component, Timeline\
**Duration**: Quarterly

**Custom Fields:**

- **Metric** (Single select): Load Time, Response Time, Throughput, Memory, CPU
- **Component** (Single select): Frontend, Backend, Database, Network, Storage
- **Current Value** (Number)
- **Target Value** (Number)
- **Improvement** (Number): Percentage
- **Impact** (Single select): High, Medium, Low
- **Status** (Status): Baseline, Investigating, Implementing, Testing, Shipped
- **Benchmark Results** (Text): Link to results

**Workflows:**

- Track before/after metrics
- Validate improvements
- Rollback if regression
- Publish results

**Board Layout:**

```
Baseline → Analysis → Implementation → Validation → Deployed
```

### 10. 🎨 Design System

**Purpose**: Track design system components and tokens\
**Views**: By Component
Type, By Status, Adoption View\
**Duration**: Ongoing

**Custom Fields:**

- **Component Type** (Single select): Layout, Navigation, Form, Data Display,
  Feedback
- **Status** (Status): Proposed, Designing, Developing, Documenting, Published
- **Design Status** (Single select): Not Started, In Progress, Review, Approved
- **Dev Status** (Single select): Not Started, In Progress, Review, Complete
- **Doc Status** (Single select): Not Started, In Progress, Review, Published
- **Adoption** (Number): Percentage of projects using it
- **Figma Link** (Text)
- **Storybook Link** (Text)
- **A11y Tested** (Checkbox)

**Workflows:**

- Coordinate design and dev
- Track component adoption
- Request accessibility review
- Update documentation

**Board Layout:**

```
Proposal → Design → Development → Documentation → Published
```

## Project Views

### Table View

**Best for**: Detailed data entry and bulk editing

**Configuration:**

```yaml
Columns:
  - Title (always visible)
  - Status
  - Priority
  - Assignees
  - Labels
  - Custom fields (as needed)

Grouping: By Status
Sorting: Priority (High to Low)
Filtering: Active items only
```

### Board View

**Best for**: Kanban-style workflow visualization

**Configuration:**

```yaml
Columns: Based on Status field
Card Display:
  - Title
  - Assignees
  - Labels
  - Priority badge

Column Limits:
  - In Progress: 5 (per person)
  - Review: 10 (team-wide)
```

### Roadmap View

**Best for**: Timeline and date-based planning

**Configuration:**

```yaml
Timeline: By Quarter or Month
Items: Sized by Story Points or Duration
Markers:
  - Release dates
  - Milestones
  - Deadlines

Grouping: By Theme or Epic
Colors: By Priority
```

### Calendar View (Custom)

**Best for**: Event and deadline tracking

**Configuration:**

```yaml
Date Field: Due Date or Target Date
Views:
  - Month view
  - Week view
  - Agenda view

Filters:
  - Upcoming deadlines
  - This week's tasks
  - Overdue items
```

## Custom Fields

### Field Types

1. **Text**: Free-form text (URLs, descriptions, IDs)
1. **Number**: Numeric values (story points, hours, percentages)
1. **Date**: Deadlines, start dates, target dates
1. **Single select**: One option from a list
1. **Multiple select**: Multiple options from a list
1. **Iteration**: Sprint/iteration planning
1. **Person**: Team member assignment
1. **Checkbox**: Boolean flags
1. **Status**: Workflow states

### Field Best Practices

**Naming Conventions:**

- Use clear, descriptive names
- Be consistent across projects
- Avoid abbreviations
- Use sentence case

**Single vs Multiple Select:**

- Use Single select for: Priority, Status, Owner
- Use Multiple select for: Labels, Tags, Components

**Required vs Optional:**

- Required: Status, Priority, Assignee
- Optional: Most custom fields

### Standard Field Set

Recommended fields for all projects:

- **Status**: Workflow state
- **Priority**: Importance level
- **Assignee**: Who's responsible
- **Size/Points**: Effort estimate
- **Labels**: Categorization
- **Due Date**: Deadline (if applicable)

## Automation

### Built-in Workflows

#### Auto-add Items

```yaml
Trigger: Issues/PRs matching criteria
Action: Add to project
Criteria:
  - Label matches
  - Repository matches
  - Milestone matches
```

#### Auto-set Values

```yaml
Trigger: Item added to project
Action: Set field values
Example:
  - Set Status to "Backlog"
  - Set Priority based on labels
  - Set Owner based on assignee
```

#### Auto-update Status

```yaml
Trigger: PR state changes
Action: Update status field
Examples:
  - PR opened → "In Review"
  - PR merged → "Done"
  - PR closed (unmerged) → "Cancelled"
```

#### Auto-archive Items

```yaml
Trigger: Status changed to "Done"
Action: Archive after X days
Configuration:
  - Days to wait: 7
  - Only if: All linked items closed
```

### GitHub Actions Integration

Create custom automations:

```yaml
name: Update Project on Issue Label
on:
  issues:
    types: [labeled]

jobs:
  update-project:
    runs-on: ubuntu-latest
    steps:
      - name: Update project field
        uses: titoportas/update-project-fields@v0.1.0
        with:
          project-url: ${{ secrets.PROJECT_URL }}
          github-token: ${{ secrets.PROJECT_TOKEN }}
          item-id: ${{ github.event.issue.node_id }}
          field-keys: Priority,Status
          field-values: High,In Progress
```

### Advanced Automation Examples

**Velocity Tracking:**

```yaml
# Calculate and update sprint velocity
on:
  schedule:
    - cron: "0 0 * * 1" # Every Monday

jobs:
  calculate-velocity:
    - Get completed story points
    - Calculate average
    - Update project field
    - Post to Slack
```

**SLA Monitoring:**

```yaml
# Alert on SLA violations
on:
  schedule:
    - cron: "0 */6 * * *" # Every 6 hours

jobs:
  check-sla:
    - Check issue ages
    - Identify SLA violations
    - Update priority
    - Notify stakeholders
```

**Dependency Tracking:**

```yaml
# Block items with incomplete dependencies
on:
  issues:
    types: [opened, edited]

jobs:
  check-dependencies:
    - Parse dependency links
    - Check if dependencies complete
    - Update blocked status
    - Add blocking comment
```

## Integration Patterns

### Cross-Repository Projects

**Organization-Level Projects:**

```yaml
Scope: All organization repositories
Use Cases:
  - Organization-wide initiatives
  - Cross-team dependencies
  - Leadership visibility

Setup:
  - Create at organization level
  - Auto-add from multiple repos
  - Use repository labels to filter
```

**Multi-Repo Product Project:**

```yaml
Scope: Product feature across repos
Repositories:
  - frontend-repo
  - backend-repo
  - docs-repo

Views:
  - By Repository
  - By Component
  - Integration Status
```

### Issue/PR Linking

**Reference Projects:**

```markdown
<!-- In issue body -->

This relates to project X
See project board for context
Part of Q1 2025 roadmap
```

**Multiple Projects:**

- Same issue can be in multiple projects
- Shows different aspects/contexts
- Useful for cross-functional tracking

### External Tool Integration

**Slack Integration:**

```yaml
Webhooks:
  - Project updates → Slack channel
  - High priority items → Direct message
  - Sprint completion → Team notification
```

**Analytics Integration:**

```yaml
Export Data:
  - GraphQL API queries
  - Regular exports to data warehouse
  - Custom dashboards in BI tools
```

## Best Practices

### Project Structure

1. **One Project per Initiative**: Don't try to track everything in one project
1. **Clear Ownership**: Each project should have a clear owner
1. **Regular Grooming**: Weekly review and updates
1. **Archive Completed**: Keep projects focused on active work
1. **Template Reuse**: Use templates for consistency

### Field Management

1. **Start Simple**: Add fields as needed
1. **Consistent Options**: Use same option lists across projects
1. **Document Meanings**: Explain what fields mean
1. **Regular Cleanup**: Remove unused fields
1. **Validate Data**: Ensure fields are filled correctly

### View Organization

1. **Default View**: Most commonly used view as default
1. **Save Filters**: Create saved views for common filters
1. **Appropriate View Types**: Board for workflow, table for data
1. **Mobile-Friendly**: Consider mobile access when designing
1. **Share Links**: Use direct view links in docs

### Collaboration

1. **Transparency**: Make projects visible to all
1. **Comment Culture**: Use comments for context
1. **@mention Sparingly**: Tag only when needed
1. **Status Updates**: Regular project status updates
1. **Celebrate Wins**: Acknowledge completed work

### Performance

1. **Archive Regularly**: Archive completed items
1. **Limit Scope**: Don't track more than 6 months in one project
1. **Optimize Queries**: Use filters to reduce load
1. **Batch Updates**: Bulk edit when possible
1. **Async Loading**: Let views load in background

## Project Examples

### Example 1: Q1 2025 Product Roadmap

```yaml
Name: Q1 2025 Product Roadmap
Type: Organization-wide
Duration: Jan 1 - Mar 31, 2025

Features:
  - 🔐 OAuth2 Implementation (8 weeks)
  - 📊 Analytics Dashboard (6 weeks)
  - 🎨 Design System v2 (12 weeks)
  - ⚡ API Performance (4 weeks)

Views:
  - Roadmap: Timeline view by month
  - By Status: Board view
  - By Team: Table view grouped by owner

Metrics:
  - 15 features planned
  - 120 story points total
  - 3 teams involved
  - 85% completion target
```

### Example 2: Bug Bash Week

```yaml
Name: Bug Bash - December 2025
Type: Time-boxed initiative
Duration: Dec 15-19, 2025

Goals:
  - Close 50+ bugs
  - Test all features
  - Improve stability

Setup:
  - Pre-populate with known bugs
  - Daily standup for updates
  - Leaderboard for motivation
  - Prizes for top contributors

Views:
  - By Priority: Focus on high-impact
  - By Finder: Track contributions
  - Progress Chart: Daily burn-down

Results:
  - 67 bugs fixed (134% of goal)
  - 12 contributors
  - 15 new bugs found and fixed
```

### Example 3: Documentation Sprint

```yaml
Name: Docs Sprint - API Documentation
Type: Sprint-based project
Duration: 2 weeks

Scope:
  - All REST API endpoints
  - Authentication flows
  - Code examples
  - Error handling

Tasks:
  - Audit existing docs (Day 1)
  - Write missing docs (Days 2-7)
  - Review and edit (Days 8-9)
  - Publish (Day 10)

Views:
  - By Endpoint: Table view
  - By Status: Kanban board
  - By Writer: Table grouped by assignee

Outcome:
  - 100% API coverage
  - 45 new examples
  - Interactive docs published
```

## Project Templates Repository

See `/.github/project-templates/` for:

- YAML configuration files
- Automation scripts
- View configurations
- Field definitions
- Example data

## GraphQL API

Query projects programmatically:

```graphql
query OrgProjects {
  organization(login: "ivviiviivvi") {
    projectsV2(first: 10) {
      nodes {
        title
        shortDescription
        url
        items(first: 100) {
          nodes {
            content {
              ... on Issue {
                title
                state
              }
            }
            fieldValues(first: 10) {
              nodes {
                ... on ProjectV2ItemFieldTextValue {
                  text
                  field {
                    ... on ProjectV2Field {
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)<!-- link:docs.github_projects -->
- [Projects GraphQL API](https://docs.github.com/en/graphql/reference/objects#projectv2)
- [Project Automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [Project Templates](./project-templates/)

---

**Last Updated**: 2025-12-28\
**Maintained By**: @ivviiviivvi project management
team
