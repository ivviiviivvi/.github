# GitHub Projects Configuration Guide

> **Step-by-step guide to visualizing the workflow system using GitHub
> Projects**

**Purpose:** Create kanban boards and roadmaps to track workflow
stages\
**Audience:** Project administrators and maintainers\
**Time:** 30
minutes setup

______________________________________________________________________

## 📋 Overview

GitHub Projects provides visual tracking for issues and PRs through the workflow
system. We'll configure:

1. **Workflow Board** - Kanban view of issue/PR lifecycle
1. **Roadmap View** - Timeline view for planning
1. **Automated Workflows** - Sync with workflow system labels

______________________________________________________________________

## 🎯 Project Structure

### Option 1: Single Project (Recommended for Small Teams)

**Name:** "Development Workflow"

**Views:**

- Board: Kanban view by status
- Roadmap: Timeline view
- Table: Detailed list view
- Priority: Grouped by priority

### Option 2: Multiple Projects (For Large Teams)

**Project 1:** "Issues & Backlog"

- Focus: Issue tracking and triage
- Views: Board, Priority, Area

**Project 2:** "Active Development"

- Focus: In-progress work and PRs
- Views: Board, Assignee, Timeline

**Project 3:** "Releases"

- Focus: Release planning and tracking
- Views: Roadmap, Milestones

______________________________________________________________________

## 🛠️ Setup Instructions

### Step 1: Create Project

1. **Navigate to Projects**

   - Organization: `https://github.com/orgs/YOUR_ORG/projects`
   - Repository: Go to repository → Projects tab

1. **Click "New project"**

1. **Choose template: "Board"**

1. **Name:** "Development Workflow"

1. **Description:**

   ```
   Tracking for discussions, issues, and pull requests through our workflow system.
   Automatically synced with workflow labels and status.
   ```

1. **Visibility:** Public or Private (match repository visibility)

1. **Click "Create"**

______________________________________________________________________

### Step 2: Configure Board View

**Default columns created:**

- Todo
- In Progress
- Done

**Customize columns to match workflow:**

1. **Click "..." on Todo column** → Rename to "📋 Backlog"

   - Automation: Add items with label `status: backlog`

1. **Add column: "🔍 Needs Triage"**

   - Automation: Add items with label `needs-triage`
   - Sort: Oldest first

1. **Rename "In Progress" to "🚀 In Progress"**

   - Automation: Add items with label `status: in-progress`
   - Sort: By priority

1. **Add column: "👀 In Review"**

   - Automation: Add items with label `awaiting-review` or `in-review`
   - Filter: Only PRs

1. **Add column: "✅ Approved"**

   - Automation: Add items with label `approved`
   - Filter: Only PRs

1. **Add column: "🚫 Blocked"**

   - Automation: Add items with label `status: blocked`
   - Sort: By priority (critical first)

1. **Rename "Done" to "✅ Completed"**

   - Automation: Add closed items
   - Archive after 7 days

**Final column order:**

```
🔍 Needs Triage → 📋 Backlog → 🚀 In Progress → 👀 In Review → ✅ Approved → 🚫 Blocked → ✅ Completed
```

______________________________________________________________________

### Step 3: Configure Automations

**For each column, set up automation:**

#### Column: 🔍 Needs Triage

**Automation rules:**

```
When: Item is added to project
If: Has label "needs-triage"
Then: Move to "🔍 Needs Triage"

When: Label "needs-triage" is added
Then: Move to "🔍 Needs Triage"

When: Label "needs-triage" is removed
Then: Move to "📋 Backlog" (if no other status)
```

#### Column: 📋 Backlog

**Automation rules:**

```
When: Label "status: backlog" is added
Then: Move to "📋 Backlog"

When: Item is triaged (type/priority labels added)
Then: Move to "📋 Backlog"
```

#### Column: 🚀 In Progress

**Automation rules:**

```
When: Label "status: in-progress" is added
Then: Move to "🚀 In Progress"

When: Item is assigned
Then: Move to "🚀 In Progress" (if not already placed)

When: PR is created and linked
Then: Keep issue in "🚀 In Progress"
```

#### Column: 👀 In Review

**Automation rules:**

```
When: Label "awaiting-review" is added (PRs only)
Then: Move to "👀 In Review"

When: PR is opened
Then: Move to "👀 In Review"

When: PR marked ready for review
Then: Move to "👀 In Review"
```

#### Column: ✅ Approved

**Automation rules:**

```
When: Label "approved" is added (PRs only)
Then: Move to "✅ Approved"

When: PR receives approval
Then: Move to "✅ Approved"
```

#### Column: 🚫 Blocked

**Automation rules:**

```
When: Label "status: blocked" is added
Then: Move to "🚫 Blocked"

When: Label "status: blocked" is removed
Then: Move back to previous status column
```

#### Column: ✅ Completed

**Automation rules:**

```
When: Issue is closed
Then: Move to "✅ Completed"

When: PR is merged
Then: Move to "✅ Completed"

Archive: After 7 days
```

______________________________________________________________________

### Step 4: Add Custom Fields

Add metadata fields to track additional information:

1. **Priority** (Single select)

   - Options: Critical, High, Medium, Low
   - Auto-populate from labels

1. **Type** (Single select)

   - Options: Bug, Feature, Documentation, Security, etc.
   - Auto-populate from labels

1. **Area** (Single select)

   - Options: Frontend, Backend, Infrastructure, etc.
   - Auto-populate from labels

1. **Size** (Single select)

   - Options: Small, Medium, Large, XL
   - Manual selection

1. **Sprint** (Iteration)

   - Configure sprint dates
   - 2-week iterations recommended

1. **Target Date** (Date)

   - Manual entry
   - For deadline tracking

1. **Effort** (Number)

   - Story points or hour estimates
   - Manual entry

**To add fields:**

1. Click "..." in top right → "Settings"
1. Scroll to "Custom fields"
1. Click "+ New field"
1. Configure as above

______________________________________________________________________

### Step 5: Create Additional Views

#### View 2: Roadmap

1. **Click "+" next to view tabs**
1. **Select "Roadmap"**
1. **Name:** "Roadmap"
1. **Settings:**
   - Group by: Sprint (or milestone)
   - Date field: Target Date
   - Show: Open items only
   - Zoom: Month view

#### View 3: Priority

1. **Create new view: "Table"**
1. **Name:** "Priority View"
1. **Group by:** Priority field
1. **Sort:** Critical first
1. **Filter:** Open items only
1. **Columns:**
   - Title
   - Status
   - Type
   - Assignee
   - Updated
   - Target Date

#### View 4: By Assignee

1. **Create new view: "Board"**
1. **Name:** "By Assignee"
1. **Group by:** Assignee
1. **Filter:** Status = In Progress
1. **Purpose:** See who's working on what

#### View 5: Stale Items

1. **Create new view: "Table"**
1. **Name:** "Stale Items"
1. **Filter:**
   - Has label "stale" OR
   - Updated \< 30 days ago AND Open
1. **Sort:** Oldest first
1. **Purpose:** Quick review of items needing attention

______________________________________________________________________

### Step 6: Add Items to Project

**Automatic addition (recommended):**

1. **Go to project settings**

1. **Scroll to "Workflows"**

1. **Enable: "Auto-add to project"**

1. **Configure:**

   ```
   When: Issue or PR is opened
   In: This repository
   Then: Add to project
   Initial status: 🔍 Needs Triage (for issues)
                  👀 In Review (for PRs)
   ```

**Manual addition:**

1. Open issue or PR
1. In sidebar, find "Projects"
1. Click "Add to project"
1. Select your project
1. Choose initial column

**Bulk addition:**

1. In project, click "+ Add item"
1. Search for issues/PRs
1. Select multiple with checkboxes
1. Click "Add selected items"

______________________________________________________________________

### Step 7: Configure Access & Permissions

**Project visibility:**

- Public: Anyone can view
- Private: Only collaborators can view

**Permission levels:**

- **Admin:** Full control, can delete project
- **Write:** Can edit items, fields, views
- **Read:** Can view only

**To add collaborators:**

1. Project settings → Manage access
1. Click "Invite collaborators"
1. Add users/teams with appropriate roles

**Recommended setup:**

- Maintainers: Write access
- Contributors: Read access
- Admins: Admin access

______________________________________________________________________

## 📊 Using the Project Board

### For Maintainers

**Daily workflow:**

1. **Morning: Check "🔍 Needs Triage"**

   - Triage new items
   - Move to appropriate columns

1. **Throughout day: Monitor "👀 In Review"**

   - Review PRs
   - Move to "✅ Approved" when ready

1. **End of day: Check "🚫 Blocked"**

   - Help unblock items
   - Update status

**Weekly:**

- Review "Stale Items" view
- Update roadmap with upcoming work
- Check priority distribution

### For Contributors

**Using the board:**

1. **Find work:** Check "📋 Backlog" for available items
1. **Start work:** Gets moved to "🚀 In Progress" when assigned
1. **Track progress:** See your work in "By Assignee" view
1. **Monitor PRs:** Watch "👀 In Review" for your PRs

### For Project Managers

**Planning:**

- Use "Roadmap" view for release planning
- Use "Priority View" for sprint planning
- Track capacity with "By Assignee" view

**Reporting:**

- Export table views to CSV
- Use insights for metrics (coming soon)
- Take screenshots for stakeholder updates

______________________________________________________________________

## 🔗 Integration with Workflow System

**The project automatically syncs with workflow labels:**

| Workflow Label        | Project Column  | Automation                    |
| --------------------- | --------------- | ----------------------------- |
| `needs-triage`        | 🔍 Needs Triage | Auto-added when label applied |
| `status: backlog`     | 📋 Backlog      | Moves when triaged            |
| `status: in-progress` | 🚀 In Progress  | Moves when assigned           |
| `awaiting-review`     | 👀 In Review    | Moves when PR opened          |
| `approved`            | ✅ Approved     | Moves when PR approved        |
| `status: blocked`     | 🚫 Blocked      | Moves when blocked            |
| Closed                | ✅ Completed    | Archives after 7 days         |

**This means:**

- Labels applied by workflow system automatically move cards
- No manual dragging needed for most cases
- Boards stay in sync with actual state

______________________________________________________________________

## 🎨 Customization Ideas

### By Team Size

**Small team (\<10 people):**

- Single project with all items
- Simple board: Backlog → In Progress → Review → Done
- No custom fields needed

**Medium team (10-50):**

- Separate projects for Issues and PRs
- Add Area and Sprint fields
- Multiple views for different roles

**Large team (50+):**

- Multiple projects by product area
- Detailed custom fields
- Automated reporting workflows

### By Workflow Complexity

**Simple workflow:**

```
To Do → In Progress → Done
```

**Standard workflow:**

```
Backlog → In Progress → Review → Approved → Done
```

**Complex workflow:**

```
Triage → Backlog → Assigned → In Progress →
Code Review → QA Review → Approved →
Staging → Production → Done
```

______________________________________________________________________

## 📈 Metrics & Insights

**Available metrics (GitHub Projects Beta):**

1. **Throughput:**

   - Items completed per week
   - Velocity trends

1. **Cycle time:**

   - Time in each column
   - Identify bottlenecks

1. **Work in progress:**

   - Current active items
   - Capacity planning

1. **Priority distribution:**

   - Balance of critical/high/medium/low
   - Risk assessment

**To view insights:**

- Currently in beta
- Click "Insights" tab when available
- Configure charts and dashboards

**Manual tracking:**

- Export table view to CSV weekly
- Track trends in spreadsheet
- Calculate your own KPIs

______________________________________________________________________

## 🔧 Troubleshooting

### Items not auto-adding

**Check:**

1. Auto-add workflow is enabled
1. Repository is linked to project
1. Items match the filter criteria

**Fix:**

- Manually add items
- Verify workflow configuration
- Check project permissions

### Cards not moving automatically

**Check:**

1. Automation rules are configured
1. Labels match exactly (case-sensitive)
1. Workflow permissions are correct

**Fix:**

- Manually move cards
- Verify automation rules
- Check label names

### Project not visible

**Check:**

1. Project visibility setting
1. Your access level
1. Repository/org connection

**Fix:**

- Request access from admin
- Change visibility to public
- Re-link project to repository

______________________________________________________________________

## ✅ Checklist

**Project Setup:**

- [ ] Project created
- [ ] Columns configured
- [ ] Automations set up
- [ ] Custom fields added
- [ ] Multiple views created
- [ ] Access configured
- [ ] Auto-add enabled

**Integration:**

- [ ] Labels synced with workflow system
- [ ] Tested automation rules
- [ ] Verified board updates with label changes
- [ ] Documented for team

**Training:**

- [ ] Team walkthrough completed
- [ ] Documentation shared
- [ ] Feedback collected
- [ ] Improvements planned

______________________________________________________________________

## 📚 Additional Resources

**GitHub Documentation:**

- [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [Automating Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [Custom Fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)

**Our Documentation:**

- [Workflow Design](../workflows/WORKFLOW_DESIGN.md)
- [Maintainer Guide](../workflows/MAINTAINER_WORKFLOW.md)
- [Contributor Guide](../workflows/CONTRIBUTOR_WORKFLOW.md)

______________________________________________________________________

**Ready to visualize your workflow? Start with Step 1!**

______________________________________________________________________

_Last Updated: January 15, 2026_
