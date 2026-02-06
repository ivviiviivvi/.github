# Manual Configuration Quick Start Guide

**Ready to complete your GitHub Projects setup?** This guide helps you configure
the remaining views and automation rules through GitHub's web interface.

______________________________________________________________________

## 🎯 What You're Configuring

### Views (42 total - 6 per project)

- **Board View** - Kanban-style workflow
- **Table View** - Detailed data grid
- **Roadmap View** - Timeline/Gantt chart
- **Priority View** - Grouped by priority
- **Team View** - Grouped by assignee
- **Status View** - Grouped status summary

### Automation Rules (35+ total)

- **Status transitions** - Auto-update status on PR events
- **Field mapping** - Auto-populate fields from labels/paths
- **Workflow triggers** - Actions on item events

______________________________________________________________________

## 🚀 Getting Started

### Option A: Interactive Guided Mode (Recommended)

```bash
# Configure views (6-9 hours)
cd /workspace
./scripts/configure-project-views-guide.sh

# Configure automation rules (3-4 hours)
./scripts/configure-automation-rules-guide.sh
```

**Features:**

- ✅ Step-by-step instructions for each configuration
- ✅ Progress tracking with auto-save
- ✅ Resume anytime - your progress is saved
- ✅ Clear instructions replacing project numbers
- ✅ Detailed configuration parameters

### Option B: Manual Reference Mode

Use the comprehensive guides:

- Views: [setup-automation-rules.md](setup-automation-rules.md) (Section: Views
  Configuration)
- Automation: [setup-automation-rules.md](setup-automation-rules.md) (Section:
  Automation Rules)

______________________________________________________________________

## 📋 Recommended Workflow

### Phase 1: Start with Project #8 (AI Framework Development)

**Why start here?** Establishes patterns you'll replicate to other projects.

**Time:** ~1.5 hours

1. **Configure all 6 views** (~45 min)

   ```bash
   ./scripts/configure-project-views-guide.sh
   # Select option: 8
   ```

1. **Configure all 5 automation rules** (~30 min)

   ```bash
   ./scripts/configure-automation-rules-guide.sh
   # Select option: 8
   ```

1. **Test with sample items** (~15 min)

   - Create a test issue
   - Add it to Project #8
   - Verify views display correctly
   - Test automation rules trigger
   - Adjust as needed

### Phase 2: Replicate to Remaining Projects

**Time:** ~7-10 hours total

Once Project #8 is working, replicate the pattern:

```bash
# Continue with interactive guides
./scripts/configure-project-views-guide.sh    # Select: A (auto-mode)
./scripts/configure-automation-rules-guide.sh # Select: A (auto-mode)
```

Or configure one project at a time during breaks.

______________________________________________________________________

## 🎨 View Configuration Examples

### Example: Board View for Project #8

1. Go to: <https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/8>
1. Click "+ New view" → Select "Board"
1. Configure:
   - **Name:** Board
   - **Group by:** Status
   - **Cards show:** Title, Labels, Assignees, Repository
   - **Sort within columns:** Priority (High → Low)
1. Save

**Result:** Kanban board with status columns (Planned → In Development → Testing
→ Deployed)

### Example: Table View

1. Same project page
1. Click "+ New view" → Select "Table"
1. Configure columns (in order):
   - Title, Status, Priority, Type, Assignees, Repository, Labels, Date added
1. Sort by: Status, then Priority
1. Save

**Result:** Spreadsheet-like view with all fields visible

______________________________________________________________________

## ⚙️ Automation Rule Configuration Examples

### Example: "New items → Planned status" (Project #8)

1. Go to: <https://github.com/orgs/%7B%7BORG_NAME%7D%7D/projects/8/settings>
1. Click "Workflows" in sidebar
1. Click "+ New workflow"
1. Configure:
   - **Trigger:** Item added to project
   - **Action:** Set Status = 🎯 Planned
1. Test with a new issue
1. Save

### Example: "PR merged → Deployed" (Project #8)

1. Same settings page
1. Create workflow:
   - **Trigger:** Pull request: Merged
   - **Action:** Set Status = 🚀 Deployed
1. Save

______________________________________________________________________

## 📊 Progress Tracking

### Check Your Progress

```bash
# Views progress
cat .github-projects-views-progress.txt

# Automation rules progress
cat .github-projects-automation-progress.txt

# Or view in the interactive guides (option: P)
```

### Completion Checklist

- [ ] Project #8: AI Framework Development (6 views + 5 rules)
- [ ] Project #9: Documentation & Knowledge (6 views + 5 rules)
- [ ] Project #10: Workflow Automation (6 views + 6 rules)
- [ ] Project #11: Security & Compliance (6 views + 5 rules)
- [ ] Project #12: Infrastructure & DevOps (6 views + 6 rules)
- [ ] Project #13: Community & Support (6 views + 4 rules)
- [ ] Project #14: Product Roadmap (6 views + 4 rules)

**Total:** 42 views + 35 automation rules

______________________________________________________________________

## 🔍 Testing Your Configuration

After configuring each project:

### Test Views

1. Add a test issue to the project
1. Check each view:
   - Board: Item appears in correct column
   - Table: All fields visible
   - Roadmap: Timeline displays correctly
   - Priority: Grouped by priority
   - Team: Shows under assignee
   - Status: Grouped by status

### Test Automation Rules

1. Create a test pull request
1. Verify:
   - New PR triggers status change
   - PR approval triggers next status
   - PR merge triggers final status
   - Labels populate correct fields
   - Closed items update status

### Clean Up

```bash
# Remove test items after verification
# (Do this manually in GitHub UI)
```

______________________________________________________________________

## ⏱️ Time Management

### Efficient Schedule

**Day 1: Foundation (1.5 hours)**

- Morning: Configure Project #8 views (45 min)
- Afternoon: Configure Project #8 automation (30 min)
- Evening: Test and refine (15 min)

**Days 2-3: Bulk Configuration (6-8 hours total)**

- Use interactive guides in auto-mode
- Take breaks between projects
- 1 hour per project (views + automation)

**Day 4: Testing & Refinement (1-2 hours)**

- Test all projects
- Adjust configurations
- Document any custom patterns

**Total Time:** 9-11.5 hours over 4 days

### Alternative: Spread Over 2 Weeks

- 1 project per day (45-60 min each)
- More manageable chunks
- Less fatigue, better quality

______________________________________________________________________

## 🎯 Tips for Success

### Do's ✅

- **Start with Project #8** - Establish patterns first
- **Use the interactive guides** - Progress tracking helps
- **Test each project** before moving to the next
- **Take screenshots** of working configurations
- **Document custom rules** you create
- **Save progress frequently** - The guides auto-save

### Don'ts ❌

- **Don't skip testing** - Catch issues early
- **Don't rush** - Quality over speed
- **Don't configure all at once** - Fatigue leads to errors
- **Don't forget to save** - Click save after each configuration
- **Don't skip Project #8** - You need the reference pattern

______________________________________________________________________

## 🆘 Troubleshooting

### Views not displaying correctly

- Check grouping/sorting settings
- Verify field visibility configuration
- Refresh browser cache (Ctrl+Shift+R)

### Automation rules not triggering

- Verify trigger conditions match events
- Check filter criteria aren't too restrictive
- Test with simple rules first
- Look for conflicts with other rules

### Progress tracking issues

```bash
# Reset progress if needed
rm .github-projects-views-progress.txt
rm .github-projects-automation-progress.txt

# Restart interactive guide to reinitialize
./scripts/configure-project-views-guide.sh
```

______________________________________________________________________

## 📚 Additional Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)<!-- link:docs.github_projects -->
- [Automation Rules Guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [Views Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project)

______________________________________________________________________

## 🎉 When You're Done

After completing all configuration:

1. **Verify everything works:**

   ```bash
   # Add items to test all projects
   python3 scripts/add-items-to-projects.py --org {{ORG_NAME}} --repo .github
   ```

1. **Document your setup:**

   - Take screenshots of each project
   - Note any custom rules you created
   - Update team documentation

1. **Train your team:**

   - Share view purposes
   - Explain automation behaviors
   - Create quick reference cards

1. **Celebrate! 🎉**

   - You now have 7 fully-configured GitHub Projects
   - Complete automation for project management
   - Professional workflow tracking

______________________________________________________________________

## 🚀 Ready to Start?

```bash
# Launch the interactive guide
cd /workspace
./scripts/configure-project-views-guide.sh
```

**Remember:** Your progress is saved automatically. You can stop and resume
anytime!

**Estimated completion:** 9-11.5 hours total, but spread it over several days
for best results.

Good luck! 🎯
