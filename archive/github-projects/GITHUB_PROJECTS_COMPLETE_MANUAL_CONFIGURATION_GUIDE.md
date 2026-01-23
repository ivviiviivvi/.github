# GitHub Projects - Complete Manual Configuration Guide

**Status:** Ready to Execute\
**Time Required:** 9-13 hours
total\
**Prerequisites:** Projects #8-14 deployed with custom fields\
**Date:**
January 18, 2026

---

## Table of Contents

1. [Overview](#overview)
1. [Prerequisites Check](#prerequisites-check)
1. [Part 1: Configure Project Views (6-9 hours)](#part-1-configure-project-views)
1. [Part 2: Configure Automation Rules (3-4 hours)](#part-2-configure-automation-rules)
1. [Part 3: Verification & Testing](#part-3-verification--testing)
1. [Troubleshooting](#troubleshooting)
1. [Quick Reference](#quick-reference)

---

## Overview

### What You're Configuring

This guide covers the **15% of manual work** that cannot be automated due to
GitHub API limitations:

- **42 Project Views** (6 per project × 7 projects)
- **35+ Automation Rules** (5 per project, minimum)

### Why This Guide Exists

GitHub's GraphQL API has **no mutations** for:

- `createProjectV2View` - Views must be created via UI
- `createProjectV2Workflow` - Automation must be configured via UI

This is a **platform limitation**, not a tooling limitation. All GitHub users
face this constraint.

### What's Already Done (85%)

✅ All 7 projects created and live\
✅ ~45 custom fields configured\
✅ 11 items
migrated with smart categorization\
✅ Token security framework implemented\
✅
Comprehensive automation scripts created

---

## Prerequisites Check

### Step 1: Verify Projects Are Accessible

**Action:** Open browser and visit each project URL

```
1. Open: https://github.com/orgs/ivviiviivvi/projects/8
2. Verify: Project title shows "🤖 AI Framework Development"
3. Verify: You see custom fields in the table
4. Verify: At least one item is present

5. Open: https://github.com/orgs/ivviiviivvi/projects/9
6. Verify: Project title shows "📚 Documentation & Knowledge"

7. Open: https://github.com/orgs/ivviiviivvi/projects/10
8. Verify: Project title shows "⚙️ Workflow Automation"

9. Open: https://github.com/orgs/ivviiviivvi/projects/11
10. Verify: Project title shows "🔒 Security & Compliance"

11. Open: https://github.com/orgs/ivviiviivvi/projects/12
12. Verify: Project title shows "🏗️ Infrastructure & DevOps"

13. Open: https://github.com/orgs/ivviiviivvi/projects/13
14. Verify: Project title shows "👥 Community & Support"

15. Open: https://github.com/orgs/ivviiviivvi/projects/14
16. Verify: Project title shows "🗺️ Product Roadmap"
```

**Expected Result:** All 7 projects load without errors

**If Projects Don't Load:**

- Check organization permissions
- Verify you're logged into correct GitHub account
- Try incognito/private browsing mode

### Step 2: Verify Custom Fields Exist

**Action:** For any project, check the table view columns

```
1. Open any project (e.g., Project #8)
2. Look at the column headers in the table
3. Verify these fields are present:
   - Status
   - Priority
   - Type
   - Complexity
   - Testing Status
   - Dependencies
```

**Expected Result:** All custom fields visible as columns

**If Fields Missing:**

- Run: `python3 scripts/configure-github-projects.py --project ai-framework`
- Check script output for errors

### Step 3: Prepare Your Workspace

**Action:** Set up for efficient configuration

```bash
1. Open this guide in a second monitor/window
2. Open GitHub in your main browser window
3. Keep a text editor open for tracking progress
4. Have a timer/clock visible
5. Clear 9-13 hours in your schedule (can be split across days)
```

**Recommendation:** Complete one full project before taking a break. This
maintains context and reduces errors.

---

## Part 1: Configure Project Views

**Total Time:** 6-9 hours\
**Per Project:** 45-75 minutes\
**Views to Create:**
42 (6 per project)

### Understanding Views

Each project needs 6 different views for different workflows:

1. **Board View** - Kanban-style for status tracking
1. **Table View** - Spreadsheet-style for data entry
1. **Roadmap View** - Timeline/Gantt for planning
1. **Priority View** - Grouped by priority field
1. **Team View** - Grouped by assignee
1. **Status View** - Filtered status summary

---

### PROJECT #8: AI Framework Development

**URL:** <https://github.com/orgs/ivviiviivvi/projects/8>\
**Estimated Time:**
45-75 minutes

#### View 1/6: Board View (Status Kanban)

**Purpose:** Visual kanban board for tracking work status

**Step-by-Step:**

```
1. Open Project #8: https://github.com/orgs/ivviiviivvi/projects/8

2. Click "+ New view" button (top right, next to existing view tabs)

3. Select "Board" as the layout type

4. Configure view settings:
   Name: "📋 Status Board"

5. Click "Create"

6. Configure board columns (click ⚙️ Settings icon):
   Group by: Status

7. Set column order (drag columns to arrange):
   - 🎯 Planned
   - 🔬 Research
   - 🏗️ In Development
   - 🧪 Testing
   - 👀 Code Review
   - ✅ Ready to Deploy
   - 🚀 Deployed
   - 📝 Documentation
   - ⏸️ On Hold
   - ✔️ Completed

8. Configure card display:
   Click "..." menu → View options
   Show: Title, Status, Priority, Type

9. Set default sorting:
   Sort by: Priority (High to Low)
   Then by: Last Updated (Newest first)

10. Save view (GitHub auto-saves)

11. Test view:
    - Drag an item between columns
    - Verify status updates
    - Use undo (Ctrl+Z / Cmd+Z) to revert
```

**Verification:**

- [ ] Board view visible in tab bar
- [ ] All status columns present and ordered correctly
- [ ] Cards show title, status, priority, type
- [ ] Dragging cards updates status field

---

#### View 2/6: Table View (Data Grid)

**Purpose:** Comprehensive data entry and bulk editing

**Step-by-Step:**

```
1. Still in Project #8

2. Click "+ New view" button

3. Select "Table" as the layout type

4. Configure view settings:
   Name: "📊 Data Grid"

5. Click "Create"

6. Configure visible columns (click "+" to add):
   - Title (always visible)
   - Status
   - Priority
   - Type
   - Complexity
   - Testing Status
   - Dependencies
   - Language
   - Last Updated
   - Assignees

7. Reorder columns (drag column headers):
   Order: Priority → Status → Type → Complexity → Language →
          Testing Status → Dependencies → Last Updated → Assignees

8. Set column widths:
   - Title: 300px (wide)
   - Status: 150px
   - Priority: 120px
   - Type: 180px
   - Others: 130px

9. Configure default sorting:
   Click column header "Priority" → Sort descending
   Then click "Status" → Add secondary sort

10. Set filters (click filter icon 🔍):
    No default filters (show all items)

11. Test table:
    - Click into a cell and edit
    - Verify changes save automatically
    - Use Tab key to navigate cells
    - Try bulk selection (Shift+Click)
```

**Verification:**

- [ ] Table view visible in tab bar
- [ ] All columns present and ordered logically
- [ ] In-place editing works
- [ ] Sorting works correctly

---

#### View 3/6: Roadmap View (Timeline)

**Purpose:** Timeline visualization for planning sprints

**Step-by-Step:**

```
1. Still in Project #8

2. Click "+ New view" button

3. Select "Roadmap" as the layout type

4. Configure view settings:
   Name: "🗓️ Timeline"

5. Click "Create"

6. Configure timeline settings (click ⚙️):
   Start date field: Created At (if no custom date field)
   End date field: Target Date (if configured)
   Zoom: Month view

7. Set grouping:
   Group by: Status

8. Configure item display:
   Show: Title, Priority (as color), Type (as label)

9. Set date range:
   Show: Next 6 months
   Starting: Current month

10. Configure markers:
    Add markers for:
    - Sprint boundaries (if applicable)
    - Release dates
    - Milestones

11. Set default view:
    Zoom level: Monthly
    Current date: Highlighted

12. Test roadmap:
    - Drag an item along timeline
    - Verify date updates
    - Try different zoom levels (Week/Month/Quarter)
    - Check item tooltips show details
```

**Verification:**

- [ ] Roadmap view visible in tab bar
- [ ] Items displayed on timeline
- [ ] Grouping by status works
- [ ] Date adjustments update fields

---

#### View 4/6: Priority View (Grouped)

**Purpose:** Focus on high-priority work

**Step-by-Step:**

```
1. Still in Project #8

2. Click "+ New view" button

3. Select "Table" as the layout type (we'll group it)

4. Configure view settings:
   Name: "⚡ Priority Focus"

5. Click "Create"

6. Configure grouping (click "Group" dropdown):
   Group by: Priority

7. Set group order (drag groups to arrange):
   - 🔥 Critical
   - ⚡ High
   - 📊 Medium
   - 🔽 Low

8. Configure visible columns:
   - Title
   - Status
   - Type
   - Complexity
   - Testing Status
   - Assignees

9. Set group display:
   Show: Item count per group
   Collapsed by default: Low priority group

10. Set filters:
    Filter: Status != "✔️ Completed"
    (Hide completed items to focus on active work)

11. Configure sorting within groups:
    Sort by: Last Updated (newest first)

12. Set compact display:
    View options → Compact mode: ON
    (Shows more items per screen)

13. Test priority view:
    - Verify critical items at top
    - Check filtering hides completed
    - Try collapsing/expanding groups
    - Move item to different priority
```

**Verification:**

- [ ] Priority view visible in tab bar
- [ ] Groups ordered Critical → High → Medium → Low
- [ ] Completed items hidden
- [ ] Item counts displayed per group

---

#### View 5/6: Team View (By Assignee)

**Purpose:** Track work distribution across team

**Step-by-Step:**

```
1. Still in Project #8

2. Click "+ New view" button

3. Select "Board" as the layout type

4. Configure view settings:
   Name: "👥 Team Workload"

5. Click "Create"

6. Configure board grouping:
   Group by: Assignees

7. Set column behavior:
   Unassigned: Show as first column

8. Configure card display:
   Show: Title, Status, Priority, Type
   Color: By priority level

9. Set column limits (optional):
   Max items per person: 10
   Visual warning when: >8 items

10. Configure sorting:
    Within each column:
    Sort by: Priority (High to Low)
    Then by: Status (In Progress first)

11. Set filters:
    Filter: Status != "✔️ Completed"
    Show: Last 30 days activity

12. Add team metrics (if available):
    Show: Items per person count
    Show: Avg completion time

13. Test team view:
    - Verify each person has a column
    - Check unassigned items column exists
    - Try dragging item between people
    - Verify reassignment works
```

**Verification:**

- [ ] Team view visible in tab bar
- [ ] Columns for each assignee
- [ ] Unassigned column present
- [ ] Item counts visible
- [ ] Reassignment via drag-drop works

---

#### View 6/6: Status View (Summary)

**Purpose:** Quick status overview and reporting

**Step-by-Step:**

```
1. Still in Project #8

2. Click "+ New view" button

3. Select "Table" as the layout type

4. Configure view settings:
   Name: "📈 Status Summary"

5. Click "Create"

6. Configure grouping:
   Group by: Status

7. Set visible columns (minimal for overview):
   - Title
   - Priority
   - Type
   - Assignees
   - Last Updated

8. Set group display:
   Show: Count and percentage per status
   Collapsed: Completed and On Hold

9. Configure filters:
   No filters (show everything for reporting)

10. Set sorting:
    Groups: By workflow order (Planned → Completed)
    Within groups: By Priority (High to Low)

11. Add summary statistics:
    Show: Total items, In Progress count, Completion rate

12. Configure highlights:
    Highlight: Items not updated in 7+ days (stale)
    Highlight: Critical priority items

13. Export configuration:
    Settings → Allow CSV export: ON
    Include: All visible columns

14. Test status view:
    - Verify all statuses represented
    - Check counts are accurate
    - Try expanding/collapsing groups
    - Test CSV export functionality
```

**Verification:**

- [ ] Status view visible in tab bar
- [ ] All status groups present
- [ ] Counts accurate
- [ ] CSV export works

---

#### Project #8 Completion Check

**After configuring all 6 views, verify:**

```
✓ View Tab Bar shows 6 views:
  1. 📋 Status Board
  2. 📊 Data Grid
  3. 🗓️ Timeline
  4. ⚡ Priority Focus
  5. 👥 Team Workload
  6. 📈 Status Summary

✓ Each view displays items correctly
✓ Switching between views is fast
✓ No error messages displayed
✓ Settings saved (try refresh to confirm)
```

**Time Check:** Mark completion time: \_\_\_\_\_\_\_\_\_\_\_\_\_

**Recommendation:** Take a 10-15 minute break before next project.

---

### PROJECT #9: Documentation & Knowledge

**URL:** <https://github.com/orgs/ivviiviivvi/projects/9>\
**Estimated Time:**
45-75 minutes

**Note:** Use same 6-view pattern as Project #8, but adjust for
documentation-specific fields.

#### View 1/6: Board View

```
1. Open Project #9: https://github.com/orgs/ivviiviivvi/projects/9
2. Click "+ New view" → Board
3. Name: "📋 Status Board"
4. Group by: Status
5. Columns (in order):
   - 📋 Backlog
   - ✍️ Writing
   - 👀 Review
   - 🔄 Revision
   - ✅ Approved
   - 📤 Published
   - 🔄 Needs Update
6. Show: Title, Status, Priority, Document Type
7. Sort: Priority (High to Low)
```

#### View 2/6: Table View

```
1. Click "+ New view" → Table
2. Name: "📊 Data Grid"
3. Columns:
   - Title
   - Status
   - Priority
   - Document Type
   - Completeness
   - Word Count
   - Last Updated
   - Next Review Date
   - Assignees
4. Sort: Priority desc, Last Updated desc
```

#### View 3/6: Roadmap View

```
1. Click "+ New view" → Roadmap
2. Name: "🗓️ Publication Timeline"
3. Start date: Last Updated
4. End date: Next Review Date
5. Group by: Document Type
6. Show: Next 12 months
7. Markers: Review cycles, Release dates
```

#### View 4/6: Priority View

```
1. Click "+ New view" → Table
2. Name: "⚡ Priority Docs"
3. Group by: Priority
4. Filter: Status != "📤 Published"
5. Columns: Title, Status, Document Type, Completeness, Assignees
6. Collapse: Low priority by default
```

#### View 5/6: Team View

```
1. Click "+ New view" → Board
2. Name: "👥 Writer Workload"
3. Group by: Assignees
4. Show: Title, Status, Document Type, Word Count
5. Filter: Status != "📤 Published"
6. Sort within columns: Priority desc
```

#### View 6/6: Status View

```
1. Click "+ New view" → Table
2. Name: "📈 Publication Status"
3. Group by: Status
4. Show: Title, Priority, Document Type, Completeness, Last Updated
5. Collapse: Published and Needs Update
6. Highlight: Docs not updated in 90+ days
```

**Project #9 Verification:**

- [ ] All 6 views created
- [ ] Documentation-specific fields visible
- [ ] Publication timeline makes sense
- [ ] Review workflow clear

---

### PROJECT #10: Workflow Automation

**URL:** <https://github.com/orgs/ivviiviivvi/projects/10>\
**Estimated Time:**
45-75 minutes

#### View 1/6: Board View

```
1. Open Project #10: https://github.com/orgs/ivviiviivvi/projects/10
2. Click "+ New view" → Board
3. Name: "📋 Workflow Status"
4. Group by: Status
5. Columns (workflow-specific):
   - 💡 Idea
   - 📝 Design
   - 🔨 Building
   - 🧪 Testing
   - 🚀 Deployed
   - 🔧 Maintenance
   - ⏸️ Paused
   - ✅ Stable
6. Show: Title, Priority, Workflow Type, Impact
```

#### View 2/6: Table View

```
1. Click "+ New view" → Table
2. Name: "📊 Automation Registry"
3. Columns:
   - Title
   - Status
   - Workflow Type
   - Priority
   - Impact
   - Complexity
   - Trigger Type
   - Dependencies
   - Last Run
   - Assignees
4. Sort: Impact desc, Priority desc
```

#### View 3/6: Roadmap View

```
1. Click "+ New view" → Roadmap
2. Name: "🗓️ Deployment Timeline"
3. Group by: Workflow Type
4. Show: Title, Priority, Impact
5. Timeline: Quarterly view
6. Markers: Release cycles, Maintenance windows
```

#### View 4/6: Impact View

```
1. Click "+ New view" → Table
2. Name: "💥 High Impact Workflows"
3. Group by: Impact
4. Filter: Status != "⏸️ Paused"
5. Columns: Title, Status, Workflow Type, Priority, Last Run
6. Sort: Priority desc within groups
```

#### View 5/6: Team View

```
1. Click "+ New view" → Board
2. Name: "👥 Workflow Ownership"
3. Group by: Assignees
4. Show: Title, Status, Workflow Type, Impact
5. Filter: Status != "✅ Stable"
6. Highlight: Workflows not run in 7+ days
```

#### View 6/6: Maintenance View

```
1. Click "+ New view" → Table
2. Name: "🔧 Maintenance Dashboard"
3. Group by: Status
4. Filter: Workflow Type = "Scheduled Maintenance"
5. Show: Title, Last Run, Next Run, Dependencies
6. Sort: Next Run (soonest first)
```

**Project #10 Verification:**

- [ ] All 6 views created
- [ ] Workflow-specific fields visible
- [ ] Impact prioritization clear
- [ ] Maintenance tracking functional

---

### PROJECT #11: Security & Compliance

**URL:** <https://github.com/orgs/ivviiviivvi/projects/11>\
**Estimated Time:**
45-75 minutes

#### View 1/6: Board View

```
1. Open Project #11: https://github.com/orgs/ivviiviivvi/projects/11
2. Click "+ New view" → Board
3. Name: "🔒 Security Pipeline"
4. Group by: Status
5. Columns (security workflow):
   - 🔍 Identified
   - 📊 Assessment
   - 🛡️ Mitigation Plan
   - 🔨 In Progress
   - ✅ Resolved
   - 📋 Documented
   - 🔄 Monitoring
6. Color code: By Severity (Critical = Red)
```

#### View 2/6: Table View

```
1. Click "+ New view" → Table
2. Name: "📊 Security Registry"
3. Columns:
   - Title
   - Status
   - Severity
   - Category
   - Compliance Framework
   - Risk Score
   - Mitigation Status
   - Assignees
   - Due Date
4. Sort: Severity desc, Risk Score desc
```

#### View 3/6: Roadmap View

```
1. Click "+ New view" → Roadmap
2. Name: "🗓️ Compliance Timeline"
3. Group by: Compliance Framework
4. Show: Title, Severity, Category
5. Markers: Audit dates, Certification renewals
6. Highlight: Overdue items in red
```

#### View 4/6: Severity View

```
1. Click "+ New view" → Table
2. Name: "🚨 Risk Prioritization"
3. Group by: Severity
4. Filter: Status != "✅ Resolved"
5. Groups: Critical → High → Medium → Low
6. Collapse: Low and Medium by default
7. Show: Title, Status, Risk Score, Mitigation Status
```

#### View 5/6: Compliance View

```
1. Click "+ New view" → Table
2. Name: "📋 Compliance Dashboard"
3. Group by: Compliance Framework
4. Show: Title, Status, Category, Due Date
5. Filter: Status != "📋 Documented"
6. Sort: Due Date (soonest first)
```

#### View 6/6: Audit View

```
1. Click "+ New view" → Table
2. Name: "🔍 Audit Trail"
3. Group by: Status
4. Show all columns for complete audit record
5. No filters (show everything)
6. Sort: Last Updated desc
7. Enable CSV export for audit reports
```

**Project #11 Verification:**

- [ ] All 6 views created
- [ ] Security severity levels clear
- [ ] Compliance tracking functional
- [ ] Audit trail comprehensive

---

### PROJECT #12: Infrastructure & DevOps

**URL:** <https://github.com/orgs/ivviiviivvi/projects/12>\
**Estimated Time:**
45-75 minutes

#### View 1/6: Board View

```
1. Open Project #12: https://github.com/orgs/ivviiviivvi/projects/12
2. Click "+ New view" → Board
3. Name: "🏗️ Infrastructure Pipeline"
4. Group by: Status
5. Columns (DevOps workflow):
   - 📋 Planned
   - 🔧 Configuring
   - 🧪 Testing
   - 🚀 Deploying
   - ✅ Running
   - 🔍 Monitoring
   - ⚠️ Issues
   - 🔧 Maintenance
6. Show: Title, Priority, Infrastructure Type
```

#### View 2/6: Table View

```
1. Click "+ New view" → Table
2. Name: "📊 Infrastructure Registry"
3. Columns:
   - Title
   - Status
   - Infrastructure Type
   - Environment
   - Priority
   - Health Status
   - Cost Category
   - Dependencies
   - Assignees
4. Sort: Environment, Priority desc
```

#### View 3/6: Roadmap View

```
1. Click "+ New view" → Roadmap
2. Name: "🗓️ Deployment Schedule"
3. Group by: Environment
4. Show: Title, Infrastructure Type, Priority
5. Markers: Maintenance windows, Upgrade dates
6. Highlight: Production deployments
```

#### View 4/6: Environment View

```
1. Click "+ New view" → Table
2. Name: "🌍 By Environment"
3. Group by: Environment
4. Groups: Production → Staging → Development
5. Show: Title, Status, Infrastructure Type, Health Status
6. Filter: Status != "⚠️ Issues"
```

#### View 5/6: Health View

```
1. Click "+ New view" → Table
2. Name: "💚 System Health"
3. Group by: Health Status
4. Groups: Healthy → Warning → Critical → Unknown
5. Show: Title, Environment, Infrastructure Type, Last Check
6. Highlight: Critical items
7. Auto-refresh: Enable (if available)
```

#### View 6/6: Cost View

```
1. Click "+ New view" → Table
2. Name: "💰 Cost Management"
3. Group by: Cost Category
4. Show: Title, Environment, Infrastructure Type, Monthly Cost
5. Sort: Cost desc within groups
6. Show totals: Per category
```

**Project #12 Verification:**

- [ ] All 6 views created
- [ ] Environment separation clear
- [ ] Health monitoring functional
- [ ] Cost tracking visible

---

### PROJECT #13: Community & Support

**URL:** <https://github.com/orgs/ivviiviivvi/projects/13>\
**Estimated Time:**
45-75 minutes

#### View 1/6: Board View

```
1. Open Project #13: https://github.com/orgs/ivviiviivvi/projects/13
2. Click "+ New view" → Board
3. Name: "👥 Support Pipeline"
4. Group by: Status
5. Columns (support workflow):
   - 📬 New
   - 👀 Triaged
   - 🔄 In Progress
   - ⏳ Waiting Response
   - ✅ Resolved
   - 📝 Documented
   - 🔒 Closed
6. Show: Title, Priority, Support Type
```

#### View 2/6: Table View

```
1. Click "+ New view" → Table
2. Name: "📊 Support Registry"
3. Columns:
   - Title
   - Status
   - Support Type
   - Priority
   - Urgency
   - Channel
   - Assignees
   - Response Time
   - Resolution Time
4. Sort: Urgency desc, Priority desc
```

#### View 3/6: Roadmap View

```
1. Click "+ New view" → Roadmap
2. Name: "🗓️ Community Events"
3. Group by: Support Type
4. Filter: Support Type = "Event" OR "Release"
5. Show: Upcoming 6 months
6. Markers: Major releases, Community calls
```

#### View 4/6: Priority View

```
1. Click "+ New view" → Table
2. Name: "🚨 Urgent Support"
3. Group by: Urgency
4. Filter: Status != "🔒 Closed"
5. Show: Title, Status, Support Type, Response Time
6. Collapse: Low urgency
7. Highlight: Items waiting >24 hours
```

#### View 5/6: Team View

```
1. Click "+ New view" → Board
2. Name: "👥 Support Load"
3. Group by: Assignees
4. Show: Title, Status, Support Type, Urgency
5. Filter: Status != "🔒 Closed"
6. Show: Item count per person
7. Visual warning: >15 items per person
```

#### View 6/6: Metrics View

```
1. Click "+ New view" → Table
2. Name: "📈 Support Metrics"
3. Group by: Status
4. Show: Title, Support Type, Response Time, Resolution Time
5. Calculate: Avg response time, Avg resolution time
6. Export: Enable CSV for reporting
```

**Project #13 Verification:**

- [ ] All 6 views created
- [ ] Support workflow clear
- [ ] Urgency prioritization working
- [ ] Metrics tracking enabled

---

### PROJECT #14: Product Roadmap

**URL:** <https://github.com/orgs/ivviiviivvi/projects/14>\
**Estimated Time:**
45-75 minutes

#### View 1/6: Board View

```
1. Open Project #14: https://github.com/orgs/ivviiviivvi/projects/14
2. Click "+ New view" → Board
3. Name: "🗺️ Roadmap Status"
4. Group by: Status
5. Columns (roadmap stages):
   - 💡 Ideation
   - 🔬 Research
   - 📋 Planned
   - 🏗️ In Development
   - 🎉 Released
   - 📊 Measuring
   - ✅ Successful
6. Show: Title, Quarter, Strategic Goal
```

#### View 2/6: Table View

```
1. Click "+ New view" → Table
2. Name: "📊 Roadmap Registry"
3. Columns:
   - Title
   - Status
   - Quarter
   - Strategic Goal
   - Priority
   - Impact
   - Effort
   - Dependencies
   - Assignees
4. Sort: Quarter, Priority desc
```

#### View 3/6: Roadmap View

```
1. Click "+ New view" → Roadmap
2. Name: "🗓️ Release Timeline"
3. Group by: Quarter
4. Show: Title, Strategic Goal, Impact
5. Timeline: Yearly view (4 quarters)
6. Markers: Major releases, Milestones
7. Color: By strategic goal
```

#### View 4/6: Strategic View

```
1. Click "+ New view" → Table
2. Name: "🎯 Strategic Goals"
3. Group by: Strategic Goal
4. Show: Title, Status, Quarter, Impact, Effort
5. Filter: Status != "✅ Successful"
6. Sort: Impact desc within groups
```

#### View 5/6: Quarter View

```
1. Click "+ New view" → Table
2. Name: "📅 Quarterly View"
3. Group by: Quarter
4. Show: Title, Status, Strategic Goal, Impact
5. Collapse: Past quarters
6. Focus: Current and next quarter
```

#### View 6/6: Impact View

```
1. Click "+ New view" → Table
2. Name: "💥 Impact Analysis"
3. Group by: Impact
4. Groups: High → Medium → Low
5. Show: Title, Status, Quarter, Effort, Strategic Goal
6. Calculate: Impact/Effort ratio
7. Sort: Ratio desc (high impact, low effort first)
```

**Project #14 Verification:**

- [ ] All 6 views created
- [ ] Quarterly planning visible
- [ ] Strategic alignment clear
- [ ] Impact analysis functional

---

## Part 1 Completion Check

**After configuring all 42 views (6 per project × 7 projects):**

```
Project #8:  ✓ 6 views ━━━━━━ Status Board, Data Grid, Timeline,
                              Priority Focus, Team Workload, Status Summary

Project #9:  ✓ 6 views ━━━━━━ Status Board, Data Grid, Publication Timeline,
                              Priority Docs, Writer Workload, Publication Status

Project #10: ✓ 6 views ━━━━━━ Workflow Status, Automation Registry,
                              Deployment Timeline, High Impact, Ownership, Maintenance

Project #11: ✓ 6 views ━━━━━━ Security Pipeline, Security Registry,
                              Compliance Timeline, Risk Prioritization,
                              Compliance Dashboard, Audit Trail

Project #12: ✓ 6 views ━━━━━━ Infrastructure Pipeline, Infrastructure Registry,
                              Deployment Schedule, By Environment,
                              System Health, Cost Management

Project #13: ✓ 6 views ━━━━━━ Support Pipeline, Support Registry,
                              Community Events, Urgent Support,
                              Support Load, Support Metrics

Project #14: ✓ 6 views ━━━━━━ Roadmap Status, Roadmap Registry,
                              Release Timeline, Strategic Goals,
                              Quarterly View, Impact Analysis

TOTAL: 42 views configured ✅
```

**Time Check:** Total views configuration time: \_\_\_\_\_\_\_\_\_\_\_\_\_ hours

**Recommendation:** Take a 30-60 minute break before starting automation rules.

---

## Part 2: Configure Automation Rules

**Total Time:** 3-4 hours\
**Per Project:** 25-35 minutes\
**Rules to Create:**
35+ (5 minimum per project)

### Understanding Automation Rules

Automation rules automatically:

- Update field values when conditions are met
- Trigger actions based on changes
- Maintain data consistency
- Reduce manual work

**Rule Types:**

1. **Status Triggers** - When status changes, do X
1. **Label Automation** - When label added, update fields
1. **Time-based** - After X days, do Y
1. **Assignment** - When assigned, update status
1. **Integration** - When PR merged, update project

---

### PROJECT #8: AI Framework Development

**URL:** <https://github.com/orgs/ivviiviivvi/projects/8>\
**Estimated Time:**
25-35 minutes

#### Rule 1/5: PR Merged → Status: Deployed

**Purpose:** Automatically mark items as deployed when PR merges

**Step-by-Step:**

```
1. Open Project #8: https://github.com/orgs/ivviiviivvi/projects/8

2. Click project menu (···) → Settings

3. Scroll to "Workflows" section

4. Click "+ Add workflow"

5. Choose trigger: "Pull request merged"

6. Configure trigger conditions:
   Repository: ivviiviivvi/.github (or specific repo)
   Branch: main (or production branch)

7. Choose action: "Set field value"

8. Configure action:
   Field: Status
   Value: 🚀 Deployed

9. Set conditions (optional):
   Only if: PR labels contain "ready-to-deploy"

10. Name the workflow:
    Name: "Auto-Deploy on PR Merge"
    Description: "Updates status to Deployed when PR merges to main"

11. Test the workflow:
    Active: ON

12. Save workflow

13. Verify:
    - Workflow appears in list
    - Toggle is ON (active)
    - Edit to confirm settings saved
```

---

#### Rule 2/5: Label Added → Auto-Populate Type Field

**Purpose:** Automatically set Type field based on labels

**Step-by-Step:**

```
1. Still in Project #8 Settings → Workflows

2. Click "+ Add workflow"

3. Choose trigger: "Issue labeled"

4. Configure trigger:
   Label matches: "agent", "mcp-server", "custom-instructions", etc.

5. Choose action: "Set field value"

6. Configure action:
   Field: Type
   Value: (depends on label)

7. Create multiple rules (one per label):

   Rule 2a: Label "agent" → Type: "🤖 Agent"
   Rule 2b: Label "mcp-server" → Type: "🔌 MCP Server"
   Rule 2c: Label "custom-instructions" → Type: "📋 Custom Instructions"
   Rule 2d: Label "chat-mode" → Type: "💬 Chat Mode"
   Rule 2e: Label "bug" → Type: "🐛 Bug Fix"

8. For each sub-rule:
   - Name: "Auto-Type: [Label Name]"
   - Active: ON
   - Test with sample issue

9. Save all workflow variants
```

---

#### Rule 3/5: New Item → Status: Planned

**Purpose:** Set default status for new items

**Step-by-Step:**

```
1. Project #8 Settings → Workflows

2. Click "+ Add workflow"

3. Choose trigger: "Item added to project"

4. Configure trigger:
   Any item: YES

5. Choose action: "Set field value"

6. Configure action:
   Field: Status
   Value: 🎯 Planned

7. Add secondary action: "Set field value"
   Field: Priority
   Value: 📊 Medium (default)

8. Name workflow:
   Name: "Initialize New Items"
   Description: "Sets default status and priority for new items"

9. Active: ON

10. Save workflow
```

---

#### Rule 4/5: Status: Testing → Require Testing Status

**Purpose:** Ensure testing status is tracked

**Step-by-Step:**

```
1. Project #8 Settings → Workflows

2. Click "+ Add workflow"

3. Choose trigger: "Field value changed"

4. Configure trigger:
   Field: Status
   New value: 🧪 Testing

5. Choose action: "Set field value" (if blank)

6. Configure action:
   Field: Testing Status
   Value: 🧪 Unit Tests (if not already set)
   Condition: Only if Testing Status is blank

7. Name workflow:
   Name: "Initialize Testing Tracking"

8. Active: ON

9. Save workflow
```

---

#### Rule 5/5: Stale Item Warning

**Purpose:** Flag items not updated in 30 days

**Step-by-Step:**

```
1. Project #8 Settings → Workflows

2. Click "+ Add workflow"

3. Choose trigger: "Schedule" (if available)
   OR use "Field value changed" as workaround

4. Configure trigger:
   Schedule: Daily at 9 AM UTC
   OR
   Trigger: Any field change

5. Choose action: "Add label"

6. Configure action:
   Label: "stale"
   Condition: Last updated > 30 days ago

7. Add comment (if available):
   Comment: "⚠️ This item hasn't been updated in 30+ days.
            Please review and update status."

8. Name workflow:
   Name: "Stale Item Detection"

9. Active: ON

10. Save workflow

Note: If scheduled workflows not available, this can be done via
      GitHub Actions instead (see scripts/stale-item-checker.yml)
```

---

#### Project #8 Automation Verification

**Test each rule:**

```
Rule 1: Create test PR, merge it → Item status updates to Deployed ✓
Rule 2: Add "agent" label to issue → Type updates to "🤖 Agent" ✓
Rule 3: Add new item to project → Status auto-set to Planned ✓
Rule 4: Change status to Testing → Testing Status initialized ✓
Rule 5: Check items >30 days old → Stale label added ✓
```

---

### PROJECT #9-14: Automation Rules Pattern

**For remaining 6 projects, apply same 5-rule pattern with project-specific
variations:**

#### PROJECT #9: Documentation & Knowledge

```
Rule 1: PR merged → Status: 📤 Published
Rule 2: Label "guide" → Type: 📖 Guide
Rule 3: New item → Status: 📋 Backlog
Rule 4: Status: Review → Add reviewer assignment
Rule 5: Not updated 90 days → Label: needs-review
```

#### PROJECT #10: Workflow Automation

```
Rule 1: PR merged → Status: 🚀 Deployed
Rule 2: Label "scheduled" → Workflow Type: Scheduled
Rule 3: New item → Status: 💡 Idea
Rule 4: Status: Testing → Set Last Run field
Rule 5: Not run 7 days → Label: needs-attention
```

#### PROJECT #11: Security & Compliance

```
Rule 1: PR merged → Status: ✅ Resolved
Rule 2: Label "critical" → Severity: 🔴 Critical
Rule 3: New item → Status: 🔍 Identified
Rule 4: Severity: Critical → Notify security team
Rule 5: Overdue mitigation → Label: overdue-critical
```

#### PROJECT #12: Infrastructure & DevOps

```
Rule 1: PR merged → Status: ✅ Running
Rule 2: Label "production" → Environment: Production
Rule 3: New item → Status: 📋 Planned
Rule 4: Health: Critical → Notify on-call
Rule 5: Not checked 24h → Label: health-unknown
```

#### PROJECT #13: Community & Support

```
Rule 1: Issue closed → Status: 🔒 Closed
Rule 2: Label "bug" → Support Type: Bug Report
Rule 3: New item → Status: 📬 New
Rule 4: Urgency: High → Assign to on-call
Rule 5: Waiting >48h → Label: needs-follow-up
```

#### PROJECT #14: Product Roadmap

```
Rule 1: PR merged → Status: 🎉 Released
Rule 2: Label "Q1-2026" → Quarter: Q1 2026
Rule 3: New item → Status: 💡 Ideation
Rule 4: Impact: High + Effort: Low → Priority: High
Rule 5: Quarter ended → Archive or move to next
```

---

### Automation Rules Template (Copy for Each Project)

**Use this checklist for each project:**

```
Project: ___________ (#_____)

✓ Rule 1: PR/Status Automation
  - Trigger: ______________
  - Action: _______________
  - Tested: _______________

✓ Rule 2: Label-to-Field Automation
  - Labels mapped: ________
  - Fields updated: ________
  - Tested: _______________

✓ Rule 3: New Item Initialization
  - Default status: ________
  - Default priority: ______
  - Tested: _______________

✓ Rule 4: Conditional Field Updates
  - Condition: ____________
  - Field updated: ________
  - Tested: _______________

✓ Rule 5: Stale/Time-based
  - Trigger: ______________
  - Action: _______________
  - Tested: _______________
```

---

## Part 2 Completion Check

**After configuring automation rules for all 7 projects:**

```
Project #8:  ✓ 5+ rules ━━━━━━ PR merge, Label mapping, New item init,
                                Testing required, Stale detection

Project #9:  ✓ 5+ rules ━━━━━━ Publishing, Doc type, Backlog init,
                                Review assignment, Review cycle

Project #10: ✓ 5+ rules ━━━━━━ Deployment, Workflow type, Idea init,
                                Last run tracking, Attention needed

Project #11: ✓ 5+ rules ━━━━━━ Resolution, Severity mapping, Identified init,
                                Critical notify, Overdue alert

Project #12: ✓ 5+ rules ━━━━━━ Running status, Environment, Planned init,
                                Health alert, Check timeout

Project #13: ✓ 5+ rules ━━━━━━ Close tracking, Support type, New init,
                                Urgent assignment, Follow-up needed

Project #14: ✓ 5+ rules ━━━━━━ Release tracking, Quarter mapping, Ideation init,
                                Impact/Effort calc, Archive old

TOTAL: 35+ automation rules configured ✅
```

---

## Part 3: Verification & Testing

### Step 1: View Verification

**Test each project's views:**

```
For each of the 7 projects:

1. Open project URL
2. Click through each of the 6 views
3. Verify:
   - View loads without errors
   - Items display correctly
   - Grouping/sorting works
   - Filters apply correctly
   - Visual layout makes sense

4. Test interactions:
   - Drag item between columns (Board view)
   - Edit cell in-place (Table view)
   - Adjust timeline (Roadmap view)
   - Expand/collapse groups
   - Apply additional filters

5. Performance check:
   - Views load in <2 seconds
   - Switching views is smooth
   - No browser console errors
```

**Expected Results:**

- All 42 views functional
- No error messages
- Interactions smooth and responsive

---

### Step 2: Automation Testing

**Test each project's automation rules:**

```
For each of the 7 projects:

1. Test Rule 1 (PR Merge):
   - Create test PR in related repo
   - Merge PR
   - Check item status updates
   - Verify timing (should be <1 minute)

2. Test Rule 2 (Label Mapping):
   - Add relevant label to test issue
   - Check Type field updates
   - Verify correct mapping

3. Test Rule 3 (New Item):
   - Add new issue to project
   - Verify default status set
   - Check default priority

4. Test Rule 4 (Conditional):
   - Trigger condition
   - Verify field updates
   - Check notifications sent (if applicable)

5. Test Rule 5 (Time-based):
   - Check existing items
   - Verify stale detection
   - Confirm labels/flags applied
```

**Expected Results:**

- All automation rules trigger correctly
- Field updates happen automatically
- No delays or failures
- Actions complete as configured

---

### Step 3: End-to-End Workflow Test

**Simulate complete item lifecycle:**

```
1. Create new issue in .github repo

2. Add to Project #8 (AI Framework)
   Expected: Status → "🎯 Planned", Priority → "📊 Medium"

3. Add label "agent"
   Expected: Type → "🤖 Agent"

4. Move to "🏗️ In Development" status
   Expected: Status updates across all views

5. Create PR referencing issue

6. Move to "🧪 Testing" status
   Expected: Testing Status field initialized

7. Merge PR
   Expected: Status → "🚀 Deployed"

8. Verify in all views:
   - Status Board: Item in Deployed column
   - Data Grid: All fields populated
   - Timeline: Item on correct date
   - Priority Focus: Item in correct group
   - Team Workload: Item under assignee
   - Status Summary: Counts updated
```

**Expected Results:**

- Complete workflow executes smoothly
- All automation triggers correctly
- Views update in real-time
- Data consistency maintained

---

### Step 4: Performance Verification

**Check system performance:**

```
1. Load time test:
   - Open each project
   - Measure load time (should be <3 seconds)
   - Switch between views (should be <1 second)

2. Large data test:
   - Projects with 50+ items should still load fast
   - Filtering should be instant
   - Sorting should be smooth

3. Automation responsiveness:
   - Trigger automation
   - Measure delay (should be <60 seconds)
   - Check for queuing/delays

4. Multi-user test (if possible):
   - Multiple users in same project
   - Concurrent edits
   - Real-time sync
```

**Performance Targets:**

- Project load: \<3 seconds
- View switch: \<1 second
- Automation trigger: \<60 seconds
- Filter/sort: Instant

---

### Step 5: Documentation Check

**Ensure configuration is documented:**

```
1. Take screenshots:
   - One screenshot per view (42 total)
   - Save to: docs/screenshots/projects/
   - Name: project-{number}-view-{name}.png

2. Document automation rules:
   - List all rules per project
   - Include trigger conditions
   - Document any special configurations

3. Create quick reference:
   - View purposes
   - Automation behaviors
   - Troubleshooting tips

4. Update README:
   - Link to projects
   - Explain view structure
   - Document automation rules
```

---

## Troubleshooting

### Common Issues

#### Issue: View doesn't save settings

**Symptoms:** Settings revert after refresh

**Solutions:**

```
1. Check browser:
   - Clear cache
   - Disable extensions
   - Try different browser

2. Check GitHub status:
   - Visit: https://www.githubstatus.com
   - Check for API issues

3. Recreate view:
   - Delete view
   - Recreate from scratch
   - Save incrementally
```

---

#### Issue: Automation rule doesn't trigger

**Symptoms:** Manual changes work, automation doesn't

**Solutions:**

```
1. Check rule status:
   - Verify toggle is ON
   - Check rule hasn't been disabled
   - Review trigger conditions

2. Check trigger event:
   - Verify event actually occurred
   - Check repository settings
   - Review webhook logs

3. Test with simple rule:
   - Create basic rule
   - Test trigger manually
   - Gradually add complexity

4. Check permissions:
   - Verify bot/app has access
   - Check repository permissions
   - Review organization settings
```

---

#### Issue: Views show wrong data

**Symptoms:** Items missing or incorrect

**Solutions:**

```
1. Check filters:
   - Review active filters
   - Check filter logic
   - Try removing all filters

2. Refresh data:
   - Hard refresh (Ctrl+Shift+R)
   - Clear browser cache
   - Reload project

3. Check item status:
   - Verify item actually in project
   - Check item hasn't been archived
   - Review field values
```

---

#### Issue: Performance is slow

**Symptoms:** Views load slowly, laggy interactions

**Solutions:**

```
1. Reduce visible items:
   - Apply filters to show fewer items
   - Archive old/completed items
   - Split into multiple projects

2. Simplify views:
   - Show fewer columns
   - Reduce grouping complexity
   - Use compact mode

3. Check browser:
   - Close other tabs
   - Restart browser
   - Update to latest version

4. Check internet:
   - Test connection speed
   - Try different network
   - Use wired connection if possible
```

---

## Quick Reference

### View Naming Convention

```
Standard view names across all projects:

1. 📋 [Subject] Board    - Kanban by status
2. 📊 Data Grid          - Full data table
3. 🗓️ [Subject] Timeline - Roadmap view
4. ⚡ [Priority Type]    - Priority-focused
5. 👥 [Team Aspect]      - Team workload
6. 📈 [Status/Summary]   - Summary/reporting
```

### Automation Rule Patterns

```
Standard automation rules:

1. PR Merge Rule
   Trigger: Pull request merged
   Action: Update status to deployed/published/released

2. Label Mapping Rule
   Trigger: Label added
   Action: Update Type/Category field

3. New Item Rule
   Trigger: Item added to project
   Action: Set default status and priority

4. Conditional Update Rule
   Trigger: Status/field change
   Action: Update related fields

5. Time-based Rule
   Trigger: Time elapsed or scheduled
   Action: Add label, send notification
```

### Keyboard Shortcuts

```
While in project view:

/ or Ctrl+K       - Quick search/command palette
E                 - Edit item (when selected)
N                 - New item
D                 - Duplicate item
Delete/Backspace  - Remove from project (not delete)
Ctrl+Z / Cmd+Z    - Undo
Ctrl+Shift+Z      - Redo
Tab               - Next cell (Table view)
Shift+Tab         - Previous cell
Enter             - Save and next row (Table view)
Esc               - Cancel edit
```

### Time Tracking

**Estimated times per section:**

```
Prerequisites Check:        15-30 minutes
Project #8 (First):        60-90 minutes
Projects #9-14 (Each):     45-60 minutes
Automation Rules (All):    180-240 minutes
Verification & Testing:    60-90 minutes
──────────────────────────────────────────
TOTAL TIME:                9-13 hours
```

**Recommended schedule:**

```
Day 1 (4-5 hours):
- Prerequisites check
- Project #8 complete (all views + automation)
- Project #9 complete
- Break

Day 2 (4-5 hours):
- Projects #10, #11, #12 complete
- Break

Day 3 (2-3 hours):
- Projects #13, #14 complete
- Verification & testing
- Documentation
```

---

## Completion Checklist

**Final verification before marking complete:**

```
✓ Prerequisites
  [ ] All 7 projects accessible
  [ ] All custom fields visible
  [ ] Workspace prepared

✓ Views (42 total)
  [ ] Project #8:  6 views configured and tested
  [ ] Project #9:  6 views configured and tested
  [ ] Project #10: 6 views configured and tested
  [ ] Project #11: 6 views configured and tested
  [ ] Project #12: 6 views configured and tested
  [ ] Project #13: 6 views configured and tested
  [ ] Project #14: 6 views configured and tested

✓ Automation (35+ rules)
  [ ] Project #8:  5+ rules configured and tested
  [ ] Project #9:  5+ rules configured and tested
  [ ] Project #10: 5+ rules configured and tested
  [ ] Project #11: 5+ rules configured and tested
  [ ] Project #12: 5+ rules configured and tested
  [ ] Project #13: 5+ rules configured and tested
  [ ] Project #14: 5+ rules configured and tested

✓ Verification
  [ ] All views load correctly
  [ ] All automation rules trigger
  [ ] End-to-end workflow tested
  [ ] Performance acceptable
  [ ] Documentation updated

✓ Documentation
  [ ] Screenshots captured
  [ ] Configuration documented
  [ ] README updated
  [ ] Quick reference created
```

**When all checkboxes are checked:** ✅ **Manual configuration 100% complete!**

---

## Success Criteria

**Configuration is complete when:**

1. ✅ All 42 views created and functional
1. ✅ All 35+ automation rules active and working
1. ✅ All views load in \<3 seconds
1. ✅ Automation triggers in \<60 seconds
1. ✅ End-to-end workflow successful
1. ✅ Team members can use projects effectively
1. ✅ Documentation complete and accurate

**Total Project Completion:** **100%** 🎉

- 85% Programmatic infrastructure (already done)
- 15% Manual configuration (this guide)

---

## Next Steps After Completion

**Once manual configuration is complete:**

1. **Team Training**
   - Schedule training session
   - Walk through each view
   - Demonstrate automation
   - Answer questions

1. **Gradual Rollout**
   - Start with one project
   - Gather feedback
   - Adjust as needed
   - Roll out remaining projects

1. **Monitoring**
   - Check automation logs daily (first week)
   - Monitor performance
   - Track usage patterns
   - Address issues promptly

1. **Optimization**
   - Review view usage after 2 weeks
   - Remove unused views
   - Add requested views
   - Refine automation rules

1. **Maintenance**
   - Review quarterly
   - Update as GitHub adds features
   - Archive old items
   - Optimize performance

---

## Support

**Need help during configuration?**

- 📚 Reference: `GITHUB_PROJECTS_DEPLOYMENT_COMPLETE.md`
- 📚 Reference: `MANUAL_CONFIG_QUICKSTART.md`
- 💬 Discussions: <https://github.com/orgs/ivviiviivvi/discussions>
- 🐛 Issues: <https://github.com/ivviiviivvi/.github/issues>

**GitHub Resources:**

- <https://docs.github.com/en/issues/planning-and-tracking-with-projects>
- <https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project>

---

**Document Version:** 1.0.0\
**Last Updated:** January 18, 2026\
**Maintained
By:** ivviiviivvi organization\
**Estimated Completion:** 9-13 hours total work

**Good luck with your manual configuration! You've got this! 🚀**
