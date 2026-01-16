# Workflow System Training Session

## 60-Minute Interactive Training

**Date:** January 16, 2026\
**Duration:** 60 minutes\
**Audience:** Maintainers
and Core Contributors\
**Format:** Interactive with live demos

---

## Agenda (60 minutes)

### Part 1: Introduction (10 minutes)

- Welcome and objectives
- Workflow system overview
- Benefits and goals
- Q&A checkpoint

### Part 2: System Architecture (15 minutes)

- Five workflow components
- How they work together
- Label taxonomy
- Trigger events
- Demo: Workflow visualization

### Part 3: Maintainer Operations (20 minutes)

- Daily operations walkthrough
- Manual intervention scenarios
- Monitoring workflows
- Handling edge cases
- Demo: Live workflow execution

### Part 4: Contributor Experience (10 minutes)

- What contributors see
- Automated assistance
- When to expect action
- How to get help

### Part 5: Q&A and Practice (5 minutes)

- Open questions
- Common scenarios
- Resources and support

---

## Part 1: Introduction (10 min)

### Welcome

Hello and welcome to the Workflow System Training! Today we'll learn about the
new automation that will help us manage issues and pull requests more
efficiently.

### Objectives

By the end of this session, you will:

- ✅ Understand how each workflow operates
- ✅ Know when to intervene manually
- ✅ Be able to monitor workflow health
- ✅ Handle common edge cases confidently

### System Overview

Our workflow system consists of 5 automated workflows:

1. **Issue Triage** - Auto-labels and enforces 48hr SLA
1. **Auto-Assign Reviewers** - Assigns based on CODEOWNERS
1. **Status Sync** - Keeps issues and PRs in sync
1. **Stale Management** - Manages inactive items
1. **Workflow Metrics** - Tracks performance

### Benefits

- 🚀 Faster issue triage (90% within 48 hours)
- 👥 Automatic reviewer assignment (95% accuracy)
- 🔄 Synchronized status (real-time updates)
- 🧹 Clean backlog (automatic stale management)
- 📊 Data-driven insights (daily metrics)

**Q&A Checkpoint:** Any questions so far?

---

## Part 2: System Architecture (15 min)

### The Five Workflows

#### 1. Issue Triage (issue-triage.yml)

**Trigger:** When issues are opened, reopened, or labeled

**What it does:**

- Adds `needs-triage` label to new issues
- Adds `status: new` label
- Posts welcome comment with next steps
- Removes `needs-triage` when type/priority added
- Adds `status: backlog` when triaged
- Enforces 48-hour SLA with warnings

**Key Features:**

- Smart detection: Scans title/body for bug/feature keywords
- Auto-escalation: Adds priority labels based on keywords
- SLA tracking: Warns at 48 hours, escalates at 72 hours

#### 2. Auto-Assign Reviewers (auto-assign-reviewers.yml)

**Trigger:** When PRs are opened or marked ready for review

**What it does:**

- Reads CODEOWNERS file
- Matches changed files to owners
- Assigns up to 5 individual reviewers
- Assigns up to 3 team reviewers
- Excludes PR author
- Adds `awaiting-review` label

**Key Features:**

- Pattern matching: Handles complex glob patterns
- Team support: Assigns GitHub teams as reviewers
- Smart exclusion: Never assigns PR author

#### 3. Status Sync (status-sync.yml)

**Trigger:** When PR or issue status changes

**What it does:**

- Syncs PR status to linked issues
- Updates issue labels when PR changes
- Adds contextual comments
- Handles draft/ready/approved/merged states
- Maintains bidirectional sync

**Key Features:**

- Draft detection: Updates when PR marked draft
- Merge detection: Closes issues when PR merges
- Review status: Tracks approval state

#### 4. Stale Management (stale-management.yml)

**Trigger:** Daily at midnight UTC + manual trigger

**What it does:**

- Marks issues stale after 90 days inactive
- Marks PRs stale after 30 days inactive
- Warns assignees at 14 days
- Auto-unassigns at 21 days
- Closes after 7-day grace period

**Key Features:**

- Exempt labels: Skip items with `pinned` or `security`
- Activity detection: Comments reset timer
- Grace period: 7 days warning before close

#### 5. Workflow Metrics (workflow-metrics.yml)

**Trigger:** Daily at 9 AM UTC + manual trigger

**What it does:**

- Counts issues/PRs created/closed/merged
- Tracks triage rate
- Measures review time
- Calculates merge rate
- Generates daily report

**Key Features:**

- Historical tracking: Maintains trend data
- Configurable period: Default 7 days
- Manual trigger: Run anytime via Actions

### Label Taxonomy

Our system uses hierarchical labels:

**Status Labels:**

- `status: new` - Just created, needs triage
- `status: backlog` - Triaged, queued for work
- `status: in-progress` - Actively being worked
- `status: in-review` - Under review
- `status: done` - Completed
- `status: draft` - PR in draft mode

**Priority Labels:**

- `priority: critical` - Security, production down
- `priority: high` - Important features, major bugs

**Type Labels:**

- `type: bug` - Something is broken
- `type: feature` - New functionality
- `type: enhancement` - Improvement
- `type: documentation` - Docs update

**Area Labels:**

- `area: frontend` - UI/UX changes
- `area: backend` - API/server changes
- `area: infrastructure` - DevOps/config
- `area: testing` - Test-related

### How They Work Together

```
New Issue Created
    ↓
[Issue Triage] adds labels & comment
    ↓
Maintainer adds type/priority
    ↓
[Issue Triage] removes needs-triage, adds backlog
    ↓
PR Created to fix issue
    ↓
[Auto-Assign] assigns reviewers from CODEOWNERS
    ↓
[Status Sync] updates issue with PR status
    ↓
PR Reviewed & Approved
    ↓
[Status Sync] updates issue status
    ↓
PR Merged
    ↓
[Status Sync] closes issue
    ↓
[Metrics] tracks success metrics
```

**Demo Time:** Let's watch a workflow in action!

---

## Part 3: Maintainer Operations (20 min)

### Daily Operations

#### Morning Routine (5 minutes)

1. Check workflow metrics report: `docs/WORKFLOW_METRICS_REPORT.md`
1. Review failed workflow runs: GitHub Actions tab
1. Check issues needing attention: Filter by `needs-attention`
1. Review stale candidates: Filter by `stale`

#### Triage New Issues

**Automated:** System adds `needs-triage` label **Your Action:** Add type and
priority labels **Result:** System removes `needs-triage`, adds
`status: backlog`

**Example:**

```
1. Open issue with needs-triage label
2. Read issue description
3. Add label: type: bug
4. Add label: priority: high
5. Bot automatically:
   - Removes needs-triage
   - Adds status: backlog
   - Posts confirmation comment
```

#### Review PRs

**Automated:** System assigns reviewers based on CODEOWNERS **Your Action:**
Review code, approve/request changes **Result:** System updates linked issue
status

**Example:**

```
1. PR opened → You're auto-assigned
2. Review code
3. Approve PR
4. Bot automatically:
   - Updates issue status to in-review
   - Adds approved label
   - Posts update to issue
```

### Manual Intervention Scenarios

#### Scenario 1: Incorrect Auto-Assignment

**Situation:** Wrong reviewers assigned **Action:**

1. Remove incorrect reviewers
1. Add correct reviewers manually
1. Comment why (helps improve CODEOWNERS)

#### Scenario 2: Urgent Issue Needs Fast-Track

**Situation:** Critical bug needs immediate attention **Action:**

1. Add `priority: critical` label
1. Add `fast-track` label (exempt from stale)
1. Manually assign to on-call engineer
1. Comment with urgency details

#### Scenario 3: False Stale Detection

**Situation:** Active issue marked stale incorrectly **Action:**

1. Remove `stale` label
1. Add comment explaining why still active
1. Consider adding `pinned` label if long-running

#### Scenario 4: SLA Warning Incorrect

**Situation:** Issue already triaged but still warned **Action:**

1. Verify type/priority labels present
1. Check labels were added correctly
1. If bug, report in workflow discussions

### Monitoring Workflows

#### Check Workflow Health

1. Navigate to **Actions** tab
1. Filter by workflow name
1. Look for:
   - ✅ Green checkmarks (success)
   - ❌ Red X (failure)
   - 🟡 Yellow dot (in progress)

#### Common Failures and Fixes

**Permission Denied:**

- Check workflow has `issues: write` or `pull-requests: write`
- Verify GitHub Actions enabled for repo

**Rate Limit Exceeded:**

- Workflows pause automatically
- Wait for rate limit reset (usually 1 hour)
- Check metrics workflow not running too frequently

**Label Not Found:**

- Create missing label in repository settings
- Ensure label name matches exactly (case-sensitive)

#### View Workflow Logs

1. Click on failed workflow run
1. Expand failed job
1. Read error messages
1. Check for patterns (rate limit, permissions, etc.)

### Handling Edge Cases

#### Edge Case 1: PR Without Linked Issue

**Default:** Status sync doesn't run **Action:** Ask contributor to link issue
with "Fixes #123"

#### Edge Case 2: Multiple PRs for One Issue

**Behavior:** Status syncs to most recent PR **Action:** Close duplicate PRs or
split issue

#### Edge Case 3: External Contributor PR

**Behavior:** May not auto-assign if not in CODEOWNERS **Action:** Manually
assign appropriate reviewers

#### Edge Case 4: Draft PR Reopened

**Behavior:** Auto-assign runs again **Action:** Reviewers notified
automatically

**Demo Time:** Let's walk through monitoring a workflow run!

---

## Part 4: Contributor Experience (10 min)

### What Contributors See

#### When Opening an Issue

1. **Immediately:** Bot adds `needs-triage` label
1. **Within seconds:** Welcome comment appears
1. **Within 48 hours:** Maintainer adds type/priority
1. **Result:** Bot confirms triage complete

**Sample Comment:**

```
🤖 Thanks for opening this issue!

A maintainer will triage this issue within 48 hours.

**Next Steps:**
- A maintainer will review and add appropriate labels
- You'll receive an update once it's been triaged
- Please provide any additional context if needed

Labels applied: needs-triage, status: new
```

#### When Opening a PR

1. **Immediately:** Bot assigns reviewers from CODEOWNERS
1. **Immediately:** `awaiting-review` label added
1. **When reviewed:** Bot updates linked issue
1. **When merged:** Bot closes linked issue

#### When PR Goes Stale

1. **After 30 days:** Warning comment posted
1. **After 7 more days:** PR marked stale
1. **After 7 more days:** PR closed (if still inactive)

### Setting Expectations

**Timeline Communication:**

```markdown
## Response Times

- **Issue Triage:** Within 48 hours
- **PR Review:** Within 7 days
- **Stale Warning:** After 30 days (PRs) or 90 days (issues)
- **Auto-Close:** 7 days after stale warning
```

### When to Get Help

Contributors should ping maintainers if:

- Issue not triaged within 48 hours
- PR not reviewed within 7 days
- Incorrect labels applied
- Bot behavior seems wrong

---

## Part 5: Q&A and Practice (5 min)

### Common Questions

**Q: What if I disagree with bot's labels?** A: Simply change them! Bot respects
manual overrides.

**Q: Can I disable workflows for specific issues?** A: Yes, add
`workflow-exempt` label.

**Q: How do I trigger metrics manually?** A: Go to Actions → Workflow Metrics →
Run workflow

**Q: What if CODEOWNERS assigns wrong people?** A: Update CODEOWNERS file and
notify team.

**Q: Can I adjust SLA timers?** A: Yes, edit workflow files (requires repo
admin).

### Practice Scenarios

Let's practice together:

1. **Triage an issue:** Find issue with `needs-triage`, add labels
1. **Review a PR:** Check auto-assigned reviewers
1. **Check metrics:** Open latest report
1. **Monitor workflows:** Check Actions tab

### Resources and Support

**Documentation:**

- `docs/MAINTAINER_WORKFLOW.md` - Complete operations guide
- `docs/CONTRIBUTOR_WORKFLOW.md` - User-facing guide
- `docs/WORKFLOW_TESTING_GUIDE.md` - Test scenarios
- Issue #246 - Deployment tracking

**Getting Help:**

- GitHub Discussions (workflow-system category)
- Tag @workflow-maintainers in issues
- Check workflow run logs for errors

**Feedback:**

- Report bugs: Open issue with `type: bug, area: workflow`
- Suggest improvements: Open discussion
- Share experiences: Comment on Issue #246

---

## Training Complete! 🎉

### Key Takeaways

✅ Five workflows automate issue/PR management\
✅ Label taxonomy drives workflow
behavior\
✅ Manual intervention always possible\
✅ Monitoring via Actions tab
and metrics\
✅ Documentation available for reference

### Next Steps

1. ✅ Review `docs/MAINTAINER_WORKFLOW.md` for detailed operations
1. ✅ Bookmark metrics report location
1. ✅ Watch first workflow run live
1. ✅ Ask questions in discussions

### Thank You!

Questions? Let's discuss now or in GitHub Discussions.

---

**Training Session:** Workflow System Operations\
**Recorded:** January 16,
2026\
**Instructor:** Workflow Automation Team\
**Next Session:** TBD (based on
team feedback)
