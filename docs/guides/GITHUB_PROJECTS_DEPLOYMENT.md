# GitHub Projects Deployment Checklist

**Date Created:** January 18, 2026\
**Status:** Ready for
Deployment\
**Estimated Time:** 2-3 hours

______________________________________________________________________

## ✅ Pre-Deployment Checklist

### Prerequisites

- [ ] **GitHub Account Access**

  - [ ] Organization admin permissions for `{{ORG_NAME}}`
  - [ ] Verified two-factor authentication enabled
  - [ ] Access to organization settings

- [ ] **Personal Access Token**

  - [ ] Token created with required scopes:
    - [ ] `project` (all scopes)
    - [ ] `repo` (all scopes)
    - [ ] `admin:org` (read scope)
  - [ ] Token saved securely (1Password, GitHub Secrets, etc.)
  - [ ] Token tested: `gh auth status`
  - [ ] **1Password CLI** (if using 1Password): `op --version`

- [ ] **Environment Setup**

  - [ ] Python 3.8+ installed: `python3 --version`
  - [ ] `requests` library installed: `pip install requests`
  - [ ] GitHub CLI installed: `gh --version`
  - [ ] GitHub CLI authenticated: `gh auth login`

- [ ] **Documentation Review**

  - [ ] Read
    [GITHUB_PROJECTS_IMPLEMENTATION.md](GITHUB_PROJECTS_IMPLEMENTATION.md)
  - [ ] Reviewed [Quick Reference](GITHUB_PROJECTS_QUICKREF.md)
  - [ ] Understood [Visual Overview](GITHUB_PROJECTS_VISUAL.md)
  - [ ] Read
    [Scripts README](../../src/automation/scripts/utils/README_PROJECTS.md)

______________________________________________________________________

## 🚀 Deployment Steps

### Phase 1: Dry Run (15 minutes)

**Goal:** Test the setup without making changes

- [ ] **Set environment variable**

  **Option A: Using 1Password CLI (Recommended)**

  ```bash
  # Retrieve token from 1Password
  export GH_TOKEN=$(op read "op://Private/GitHub PAT/credential")
  echo "Token loaded from 1Password: ${GH_TOKEN:0:4}..." # Show first 4 chars
  ```

  **Option B: Manual entry**

  ```bash
  export GH_TOKEN="your_personal_access_token"
  echo $GH_TOKEN  # Verify it's set
  ```

- [ ] **Run dry-run mode**

  ```bash
  cd /workspace/scripts
  python3 configure-github-projects.py \
    --org {{ORG_NAME}} \
    --dry-run
  ```

- [ ] **Review output**

  - [ ] Check: Shows all 7 projects to be created
  - [ ] Check: Lists all fields for each project
  - [ ] Check: No errors displayed
  - [ ] Check: Estimated time shown

- [ ] **Verify token permissions**

  ```bash
  gh api user --jq '.login'  # Should show your username
  gh api orgs/{{ORG_NAME}} --jq '.login'  # Should show org name
  ```

**If dry run succeeds:** ✅ Proceed to Phase 2\
**If dry run fails:** ❌ Review
errors, fix issues, retry

______________________________________________________________________

### Phase 2: Project Creation (30-45 minutes)

**Goal:** Create all 7 projects with configured fields

**Method A: Using 1Password deployment script (easiest)**

- [ ] **Run automated deployment**

  ```bash
  cd /workspace/scripts
  ./deploy-with-1password.sh
  ```

  The script handles everything:

  - Retrieves token from 1Password
  - Runs configuration script
  - Logs output to timestamped file

**Method B: Manual Python script**

- [ ] **Run full setup**

  **With 1Password CLI:**

  ```bash
  export GH_TOKEN=$(op read "op://Private/GitHub PAT/credential")
  python3 configure-github-projects.py \
    --org {{ORG_NAME}} \
    2>&1 | tee projects-setup.log
  ```

  **Or manually:**

  ```bash
  python3 configure-github-projects.py \
    --org {{ORG_NAME}} \
    2>&1 | tee projects-setup.log
  ```

- [ ] **Monitor progress**

  - [ ] Watch for project creation confirmations
  - [ ] Verify field creation messages
  - [ ] Check for any errors or warnings
  - [ ] Note project numbers assigned

- [ ] **Verify project creation**

  - [ ] Open: https://github.com/orgs/{{ORG_NAME}}/projects
  - [ ] Count: Should see 7 new projects
  - [ ] Check: Each project has correct title and icon

**Projects to verify:**

- [ ] 🤖 AI Framework Development

- [ ] 📚 Documentation & Knowledge

- [ ] ⚙️ Workflow & Automation

- [ ] 🔒 Security & Compliance

- [ ] 🏗️ Infrastructure & DevOps

- [ ] 👥 Community & Engagement

- [ ] 🚀 Product Roadmap

- [ ] **Verify field configuration**

  For each project:

  - [ ] Open project settings
  - [ ] Check: Custom fields exist
  - [ ] Check: Field options are correct
  - [ ] Check: Colors are applied

**If creation succeeds:** ✅ Proceed to Phase 3\
**If creation fails:** ❌ Check
logs, fix issues, retry failed projects

______________________________________________________________________

### Phase 3: View Configuration (45-60 minutes)

**Goal:** Create all views for each project

**For each project, create these views:**

#### 🤖 AI Framework Development

- [ ] **Board: Development Pipeline**

  - [ ] Layout: Board
  - [ ] Columns: Status field
  - [ ] Group by: Status
  - [ ] Sort: Priority, Creation date

- [ ] **Table: Agent Catalog**

  - [ ] Layout: Table
  - [ ] Filter: Type = Agent
  - [ ] Visible columns: Title, Type, Agent Category, Language, Status, Priority
  - [ ] Group by: Agent Category

- [ ] **Table: MCP Server Development**

  - [ ] Layout: Table
  - [ ] Filter: Type = MCP Server
  - [ ] Visible columns: Title, Language, Status, Testing Status
  - [ ] Sort: Language

- [ ] **Board: Active Sprint**

  - [ ] Layout: Board
  - [ ] Columns: Status
  - [ ] Filter: Sprint = Current
  - [ ] Group by: Owner

- [ ] **Roadmap: Timeline**

  - [ ] Layout: Roadmap
  - [ ] Date field: Target completion
  - [ ] Group by: Type

- [ ] **Table: Bug Tracking**

  - [ ] Layout: Table
  - [ ] Filter: Type = Bug Fix
  - [ ] Sort: Priority, Created date

#### 📚 Documentation & Knowledge

- [ ] **Board: Documentation Pipeline**

  - [ ] Columns: Status (Backlog → Writing → Review → Published)
  - [ ] Filter: Exclude Deprecated
  - [ ] Sort: Priority

- [ ] **Table: Documentation Catalog**

  - [ ] Visible columns: Title, Document Type, Category, Completeness, Status
  - [ ] Sort: Category, Document Type

- [ ] **Table: Needs Attention**

  - [ ] Filter: Status = Needs Update OR Next Review Date \< Today
  - [ ] Sort: Priority, Next Review Date

- [ ] **Board: Quick Wins**

  - [ ] Filter: Completeness IN (Draft, Outline Only)
  - [ ] Filter: Word Count \< 500

- [ ] **Table: By Category**

  - [ ] Group by: Category
  - [ ] Sort: Priority within groups

- [ ] **Board: By Author**

  - [ ] Group by: Assigned Writer
  - [ ] Columns: Status

#### ⚙️ Workflow & Automation

- [ ] **Board: Workflow Pipeline**

  - [ ] Columns: Status (Proposed → Development → Testing → Deployed)
  - [ ] Sort: Priority, Impact

- [ ] **Table: Active Workflows**

  - [ ] Filter: Status NOT IN (Complete, Paused)
  - [ ] Visible columns: Title, Type, Status, Success Rate, Owner
  - [ ] Sort: Success Rate (ascending)

- [ ] **Table: Needs Attention**

  - [ ] Filter: Success Rate \< 80
  - [ ] Sort: Priority

- [ ] **Board: Deployment Workflows**

  - [ ] Filter: Workflow Type IN (CD Pipeline, Release)
  - [ ] Columns: Status

- [ ] **Table: Analytics Dashboard**

  - [ ] Group by: Workflow Type
  - [ ] Visible columns: Title, Success Rate, Avg Duration, Cost Impact

- [ ] **Table: Security Workflows**

  - [ ] Filter: Workflow Type = Security Scan
  - [ ] Sort: Status, Priority

#### 🔒 Security & Compliance

- [ ] **Table: Critical Dashboard**

  - [ ] Filter: Severity IN (Critical, High)
  - [ ] Visible columns: Title, Severity, SLA Status, Resolution Target
  - [ ] Sort: CVSS Score (descending), Resolution Target

- [ ] **Board: Remediation Pipeline**

  - [ ] Columns: Status (Identified → Triaged → Remediation → Fixed)
  - [ ] Filter: Severity IN (Critical, High, Medium)
  - [ ] Sort: Severity, CVSS Score

- [ ] **Table: Compliance Tracking**

  - [ ] Filter: Issue Type = Compliance Requirement
  - [ ] Group by: Compliance Framework

- [ ] **Table: SLA Dashboard**

  - [ ] Filter: SLA Status != Within SLA OR Resolution Target \< +7 days
  - [ ] Visible columns: Title, Severity, Resolution Target, SLA Status, Days
    Remaining
  - [ ] Sort: Resolution Target

- [ ] **Table: Vulnerability Trends**

  - [ ] Group by: Detection Method
  - [ ] Visible columns: Title, Severity, CVE ID, CVSS Score, Status

- [ ] **Board: Team Workload**

  - [ ] Group by: Assigned To
  - [ ] Columns: Status
  - [ ] Filter: Status NOT IN (Verified, Accepted Risk)

#### 🏗️ Infrastructure & DevOps

- [ ] **Board: Infrastructure Pipeline**

  - [ ] Columns: Status (Planned → Design → Provisioning → Deployed)
  - [ ] Sort: Priority, Environment

- [ ] **Table: Cloud Resources**

  - [ ] Group by: Cloud Provider
  - [ ] Visible columns: Title, Infrastructure Type, Environment, Status, Cost
    Estimate
  - [ ] Sort: Environment (Production first)

- [ ] **Table: Cost Management**

  - [ ] Visible columns: Title, Infrastructure Type, Cloud Provider, Cost
    Estimate, Impact
  - [ ] Sort: Cost Estimate (descending)

- [ ] **Table: IaC Tracking**

  - [ ] Filter: IaC Tool != Manual
  - [ ] Group by: IaC Tool

- [ ] **Table: Production Resources**

  - [ ] Filter: Production IN Environment
  - [ ] Visible columns: Title, Infrastructure Type, Status, Uptime SLA, Owner
  - [ ] Sort: Priority

- [ ] **Table: Operational Dashboard**

  - [ ] Filter: Status = Operational
  - [ ] Group by: Infrastructure Type

#### 👥 Community & Engagement

- [ ] **Board: Community Pipeline**

  - [ ] Columns: Status (New → Triaged → Discussion → Resolved)
  - [ ] Sort: Priority, Created Date

- [ ] **Table: Active Support Requests**

  - [ ] Filter: Engagement Type = Support Request
  - [ ] Filter: Status NOT IN (Resolved, Completed)
  - [ ] Sort: Priority, Created Date

- [ ] **Table: First-Time Contributors**

  - [ ] Filter: Contributor Type = First-time
  - [ ] Sort: Created Date (newest first)

- [ ] **Board: Good First Issues**

  - [ ] Filter: Good First Issue = Yes
  - [ ] Filter: Status = Triaged
  - [ ] Columns: Area
  - [ ] Sort: Priority

- [ ] **Table: Feature Requests**

  - [ ] Filter: Engagement Type = Feature Request
  - [ ] Group by: Area

- [ ] **Table: Community Health**

  - [ ] Group by: Engagement Type
  - [ ] Visible columns: Engagement Type, Count, Avg Response Time, Satisfaction

#### 🚀 Product Roadmap

- [ ] **Roadmap: Timeline**

  - [ ] Layout: Roadmap
  - [ ] Date field: Target Date
  - [ ] Group by: Quarter
  - [ ] Zoom: Quarter
  - [ ] Filter: Status NOT IN (Cancelled, Completed)

- [ ] **Board: Current Quarter**

  - [ ] Filter: Quarter = Q1 2026
  - [ ] Columns: Status
  - [ ] Sort: Priority

- [ ] **Table: Strategic Initiatives**

  - [ ] Filter: Initiative Type = Strategic Initiative
  - [ ] Visible columns: Title, Status, Impact, Effort, Success Metrics
  - [ ] Sort: Priority

- [ ] **Timeline: Release Planning**

  - [ ] Filter: Initiative Type = Release
  - [ ] Sort: Target Date

- [ ] **Table: Critical Path**

  - [ ] Filter: Priority IN (P0 - Critical, P1 - High)
  - [ ] Sort: Target Date

- [ ] **Table: Impact Dashboard**

  - [ ] Group by: Impact
  - [ ] Visible columns: Title, Initiative Type, Status, Effort, Quarter

**If view creation succeeds:** ✅ Proceed to Phase 4\
**If view creation fails:**
❌ Create views manually, note issues

______________________________________________________________________

### Phase 4: Automation Setup (30 minutes)

**Goal:** Configure automation rules for each project

**Note:** Automation rules must be configured in the GitHub UI as they're not
available via API yet.

**For each project:**

- [ ] Open project settings
- [ ] Navigate to "Workflows" tab
- [ ] Enable built-in automations
- [ ] Configure custom automation rules (see
  [Implementation Guide](GITHUB_PROJECTS_IMPLEMENTATION.md#automation-rules))

**Key automations to set up:**

#### All Projects

- [ ] Auto-add items when labeled
- [ ] Archive completed items after 30 days
- [ ] Notify on status changes

#### Security & Compliance

- [ ] Set SLA deadlines based on severity
- [ ] Flag SLA breaches
- [ ] Update SLA status on fix

#### Workflow & Automation

- [ ] Flag workflows with low success rate
- [ ] Move to monitoring after deployment

#### Community & Engagement

- [ ] Welcome first-time contributors
- [ ] Flag slow response times

**If automation setup succeeds:** ✅ Proceed to Phase 5\
**If automation fails:**
❌ Set up manually, document issues

______________________________________________________________________

### Phase 5: Integration (30 minutes)

**Goal:** Connect projects with existing workflows

- [ ] **Create GitHub Actions workflow**

  Create `.github/workflows/project-sync.yml`:

  ```yaml
  name: Sync to Projects

  on:
    issues:
      types: [opened, labeled, closed]
    pull_request:
      types: [opened, labeled, closed, ready_for_review]

  jobs:
    sync:
      runs-on: ubuntu-latest
      steps:
        - name: Add to appropriate project
          uses: actions/add-to-project@v0.5.0
          with:
            project-url: ${{ secrets.PROJECT_URL }}
            github-token: ${{ secrets.PROJECT_TOKEN }}
  ```

- [ ] **Configure repository secrets**

  - [ ] Add PROJECT_TOKEN with project:write scope
  - [ ] Add project URLs for each domain

- [ ] **Test integration**

  - [ ] Create test issue with label
  - [ ] Verify it appears in correct project
  - [ ] Update issue status
  - [ ] Verify project updates

**If integration succeeds:** ✅ Proceed to Phase 6\
**If integration fails:** ❌
Debug workflow, check permissions

______________________________________________________________________

### Phase 6: Testing & Validation (30 minutes)

**Goal:** Verify everything works end-to-end

- [ ] **Create test items**

  - [ ] Create test issue in each project
  - [ ] Add to project manually
  - [ ] Update fields
  - [ ] Move between columns
  - [ ] Close item
  - [ ] Verify appears in correct views

- [ ] **Test filters**

  - [ ] Apply filters in each view
  - [ ] Verify results are correct
  - [ ] Test saved filters

- [ ] **Test automation**

  - [ ] Verify auto-labeling works
  - [ ] Check status transitions
  - [ ] Confirm notifications sent

- [ ] **Performance check**

  - [ ] Pages load quickly (\<2 seconds)
  - [ ] Filters apply instantly
  - [ ] No errors in browser console

**If testing succeeds:** ✅ Proceed to Phase 7\
**If testing fails:** ❌ Fix
issues, retest

______________________________________________________________________

### Phase 7: Team Rollout (1-2 hours)

**Goal:** Onboard team members to use projects

- [ ] **Prepare training materials**

  - [ ] Share [Quick Reference](GITHUB_PROJECTS_QUICKREF.md)
  - [ ] Prepare demo walkthrough
  - [ ] Create video tutorial (optional)

- [ ] **Schedule training session**

  - [ ] Book time with team
  - [ ] Prepare agenda
  - [ ] Set up demo environment

- [ ] **Conduct training**

  - [ ] Explain project structure
  - [ ] Demo common workflows
  - [ ] Show how to add/update items
  - [ ] Review views and filters
  - [ ] Answer questions

- [ ] **Gather initial feedback**

  - [ ] Survey team members
  - [ ] Note pain points
  - [ ] Collect improvement suggestions

**If rollout succeeds:** ✅ Proceed to Phase 8\
**If rollout has issues:** ❌
Address concerns, provide additional support

______________________________________________________________________

### Phase 8: Migration (1-2 days)

**Goal:** Move existing issues and PRs to projects

- [ ] **Identify items to migrate**

  ```bash
  # List open issues
  gh issue list --repo {{ORG_NAME}}/.github --limit 1000 --json number,title,labels

  # List open PRs
  gh pr list --repo {{ORG_NAME}}/.github --limit 1000 --json number,title,labels
  ```

- [ ] **Bulk add to projects**

  ```bash
  # Add issues with specific labels
  for issue in $(gh issue list --label agent --json number --jq '.[].number'); do
    gh project item-add PROJECT_NUMBER --owner {{ORG_NAME}} --url "https://github.com/{{ORG_NAME}}/.github/issues/$issue"
  done
  ```

- [ ] **Set initial status**

  - [ ] Review each item
  - [ ] Set appropriate status
  - [ ] Assign owners
  - [ ] Set priority

- [ ] **Verify migration**

  - [ ] Count items in each project
  - [ ] Check for missing items
  - [ ] Verify data accuracy

**If migration succeeds:** ✅ Proceed to Phase 9\
**If migration incomplete:** ❌
Continue migration, fix data issues

______________________________________________________________________

### Phase 9: Documentation Update (1 hour)

**Goal:** Update org documentation with project information

- [ ] **Update README.md**

  - [ ] Add projects section ✅ (Already done!)
  - [ ] Link to project documentation
  - [ ] Include quick start commands

- [ ] **Update documentation index**

  - [ ] Add project docs to index ✅ (Already done!)
  - [ ] Update navigation
  - [ ] Cross-reference related docs

- [ ] **Create project-specific docs**

  - [ ] Per-project usage guidelines
  - [ ] Team-specific workflows
  - [ ] Best practices

- [ ] **Update onboarding docs**

  - [ ] Add projects to new contributor guide
  - [ ] Include in team onboarding
  - [ ] Update screenshots and examples

**If documentation complete:** ✅ Proceed to Phase 10\
**If documentation
incomplete:** ❌ Finish documentation

______________________________________________________________________

### Phase 10: Monitoring & Optimization (Ongoing)

**Goal:** Track usage and improve over time

- [ ] **Set up monitoring**

  - [ ] Track project views
  - [ ] Monitor automation effectiveness
  - [ ] Measure team adoption

- [ ] **Weekly review**

  - [ ] Check project health metrics
  - [ ] Review stale items
  - [ ] Verify automation working

- [ ] **Monthly review**

  - [ ] Analyze usage patterns
  - [ ] Gather team feedback
  - [ ] Adjust configurations

- [ ] **Quarterly review**

  - [ ] Strategic assessment
  - [ ] Review field/view effectiveness
  - [ ] Plan improvements

**Monitoring checklist:**

- [ ] Projects being actively used
- [ ] Items being added regularly
- [ ] Status updates happening
- [ ] Automation rules executing
- [ ] Team satisfaction high

______________________________________________________________________

## 📊 Success Criteria

### Immediate Success (Week 1)

- [ ] All 7 projects created
- [ ] Fields configured correctly
- [ ] Views set up and working
- [ ] Team can access projects
- [ ] Basic automation working

### Short-term Success (Month 1)

- [ ] 80%+ of new issues added to projects
- [ ] Team using projects daily
- [ ] Average 5+ updates per item
- [ ] Automation handling 50%+ of transitions
- [ ] Positive team feedback

### Long-term Success (Quarter 1)

- [ ] 95%+ of work tracked in projects
- [ ] Average cycle time \< 7 days
- [ ] 80%+ items completed on time
- [ ] Full team adoption
- [ ] Projects central to workflow

______________________________________________________________________

## 🆘 Troubleshooting

### Common Issues

**Issue: Script fails with authentication error**

- Check: Token is set correctly (`echo $GH_TOKEN`)
- Check: Token has required scopes
- Fix: Generate new token with correct scopes

**Issue: Field creation fails**

- Check: Field name is unique
- Check: Color codes are valid
- Fix: Use different field name or color

**Issue: Views not displaying correctly**

- Check: Filters are correct
- Check: Fields exist in project
- Fix: Recreate view with correct settings

**Issue: Automation not triggering**

- Check: Automation rules are enabled
- Check: Conditions are met
- Fix: Review and update automation rules

**Issue: Items not appearing in project**

- Check: Item was added to project
- Check: Filters not excluding item
- Fix: Manually add item, check view filters

______________________________________________________________________

## 📞 Support

**Questions?**

- Review
  [Troubleshooting](../../src/automation/scripts/utils/README_PROJECTS.md#troubleshooting)
- Check [Quick Reference](GITHUB_PROJECTS_QUICKREF.md)
- Ask in
  [Discussions](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->

**Issues?**

- Open
  [Issue](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
- Tag with `project-management` label
- Provide error logs and screenshots

______________________________________________________________________

## ✅ Final Verification

Before marking deployment complete, verify:

- [ ] All 7 projects exist and are accessible
- [ ] All fields configured with correct options
- [ ] All views created and working
- [ ] Automation rules set up and testing
- [ ] Integration with workflows active
- [ ] Team trained and onboarded
- [ ] Existing items migrated
- [ ] Documentation updated
- [ ] Monitoring in place

**Deployment Status:** ⬜ Not Started | ⬜ In Progress | ⬜ Complete

**Deployed by:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Date:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
**Time spent:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

______________________________________________________________________

**🎉 Congratulations! GitHub Projects deployment complete!**

Next: [Monitor and optimize](GITHUB_PROJECTS_IMPLEMENTATION.md#maintenance-plan)

______________________________________________________________________

_Last Updated: January 18, 2026_
