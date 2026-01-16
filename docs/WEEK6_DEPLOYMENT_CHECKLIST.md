# Week 6 Repository Expansion - Deployment Checklist

**Pilot Repository:** `[owner/repo-name]`\
**Start Date:** February 22,
2026\
**Target Completion:** February 28, 2026\
**Deployment Lead:**
`@workflow-team`

---

## Pre-Deployment Checklist

### Day 1: Repository Selection (Feb 22)

- [ ] **Run evaluation script**

  ```bash
  python3 automation/scripts/evaluate_repository.py <owner/repo>
  # or evaluate all org repos:
  python3 automation/scripts/evaluate_repository.py --all <org>
  ```

- [ ] **Review evaluation results**
  - [ ] Total score ≥ 60 (minimum "GOOD" recommendation)
  - [ ] Activity score ≥ 50 (reasonable development activity)
  - [ ] Has CODEOWNERS file
  - [ ] Has CONTRIBUTING.md or willing to create one
  - [ ] Open issues: 5-50 (manageable volume)
  - [ ] Open PRs: 2-20 (active but not overwhelming)

- [ ] **Stakeholder approval**
  - [ ] Repository maintainer agrees to pilot
  - [ ] Team lead approves
  - [ ] Engineering manager notified

- [ ] **Create pilot configuration**

  ```bash
  cp automation/config/pilot-repo-config-template.yml \
     automation/config/pilot-<repo-name>-config.yml
  ```

- [ ] **Customize configuration file**
  - [ ] Update repository information
  - [ ] Map labels to repository conventions
  - [ ] Configure CODEOWNERS settings
  - [ ] Adjust stale detection parameters
  - [ ] Set workflow priorities
  - [ ] Define monitoring thresholds
  - [ ] Add stakeholder information

### Day 2: Workflow Generation (Feb 23)

- [ ] **Generate customized workflows**

  ```bash
  python3 automation/scripts/generate_pilot_workflows.py \
    automation/config/pilot-<repo-name>-config.yml
  ```

- [ ] **Review generated workflows**
  - [ ] `issue-triage.yml` - Label rules correct
  - [ ] `auto-assign-reviewers.yml` - Path mappings correct
  - [ ] `stale-management.yml` - Grace periods correct
  - [ ] All workflows have Slack notifications
  - [ ] Priorities match configuration (P1/P2/P3)

- [ ] **Create pilot branch in target repository**

  ```bash
  gh repo clone <owner/repo>
  cd <repo>
  git checkout -b workflow-automation-pilot
  mkdir -p .github/workflows
  ```

- [ ] **Copy workflows to pilot repository**

  ```bash
  cp generated_workflows/*.yml <repo>/.github/workflows/
  ```

- [ ] **Add dry-run flags for Phase 1**
  - [ ] Add `if: false` to all action steps (passive observation)
  - [ ] Keep only logging and notification steps active
  - [ ] Document dry-run configuration

- [ ] **Commit and push pilot branch**

  ```bash
  cd <repo>
  git add .github/workflows/
  git commit -m "feat: add workflow automation (Phase 1 - passive mode)"
  git push origin workflow-automation-pilot
  ```

- [ ] **Create pilot PR**

  ```bash
  gh pr create \
    --title "Workflow Automation Pilot - Phase 1 (Passive Mode)" \
    --body-file .github/pilot-pr-template.md \
    --label "workflow-automation,pilot" \
    --draft
  ```

### Day 3: Communication (Feb 24)

- [ ] **Announce pilot to repository team**
  - [ ] Post in repository's Slack/Teams channel
  - [ ] Email to stakeholders (use template below)
  - [ ] Update repository README with pilot notice

- [ ] **Schedule training session (optional)**
  - [ ] Date/time: \_\_\_\_\_\_\_\_\_\_\_\_\_
  - [ ] Duration: 15 minutes
  - [ ] Attendees: Repository maintainers + team
  - [ ] Use: `docs/SLACK_INTEGRATION_TRAINING.md`

- [ ] **Prepare monitoring dashboard**
  - [ ] Add pilot repository to metrics dashboard
  - [ ] Configure alerts for pilot-specific failures
  - [ ] Create dedicated Slack channel: `#pilot-<repo-name>`

---

## Phase 1: Passive Mode Deployment

**Duration:** 24 hours (Feb 24, 2:00 PM UTC → Feb 25, 2:00 PM UTC)\
**Mode:**
Observation only (dry-run, no actual changes)

### Feb 24, 2:00 PM UTC - Deployment

- [ ] **Merge pilot PR to main**

  ```bash
  gh pr merge <pr-number> --squash --delete-branch
  ```

- [ ] **Post deployment announcement**

  ```
  📢 Workflow Automation Pilot - Phase 1 ACTIVE

  Repository: <owner/repo>
  Mode: PASSIVE (observation only, no changes)
  Duration: 24 hours

  Workflows are running in dry-run mode. They will:
  ✅ Log what they would do
  ✅ Send test notifications
  ❌ NOT make any actual changes

  Questions? #pilot-<repo-name>
  ```

- [ ] **Monitor initial runs**
  - [ ] Check Actions tab: `https://github.com/<owner/repo>/actions`
  - [ ] Verify workflows trigger correctly
  - [ ] Confirm logs show intended behavior
  - [ ] Check Slack notifications arrive

### Phase 1 Monitoring (Every 6 hours)

- [ ] **Check 1: Feb 24, 8:00 PM UTC**
  - [ ] Workflow executions: \_\_\_\_\_ (count)
  - [ ] Errors: \_\_\_\_\_ (count)
  - [ ] Logs review: ☐ Clean ☐ Issues found
  - [ ] Action: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- [ ] **Check 2: Feb 25, 2:00 AM UTC**
  - [ ] Workflow executions: \_\_\_\_\_ (count)
  - [ ] Errors: \_\_\_\_\_ (count)
  - [ ] Logs review: ☐ Clean ☐ Issues found
  - [ ] Action: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- [ ] **Check 3: Feb 25, 8:00 AM UTC**
  - [ ] Workflow executions: \_\_\_\_\_ (count)
  - [ ] Errors: \_\_\_\_\_ (count)
  - [ ] Logs review: ☐ Clean ☐ Issues found
  - [ ] Action: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- [ ] **Final Check: Feb 25, 2:00 PM UTC**
  - [ ] Workflow executions: \_\_\_\_\_ (count)
  - [ ] Errors: \_\_\_\_\_ (count)
  - [ ] Logs review: ☐ Clean ☐ Issues found
  - [ ] Action: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### Phase 1 Go/No-Go Decision (Feb 25, 2:00 PM UTC)

**Criteria for Phase 2:**

- [ ] All workflows executed without errors
- [ ] Logs show correct behavior (would have made appropriate changes)
- [ ] Slack notifications delivered successfully
- [ ] No stakeholder concerns raised
- [ ] Team confidence: ☐ High ☐ Medium ☐ Low

**Decision:** ☐ GO TO PHASE 2 ☐ EXTEND PHASE 1 ☐ ROLLBACK

**If NO-GO, document reason:**

---

---

## Phase 2: Active Mode Deployment

**Duration:** 4 days (Feb 25 → Feb 28)\
**Mode:** Gradual activation with
intensive monitoring

### Day 1: Feb 25 - Issue Triage Only

- [ ] **2:30 PM UTC - Activate Issue Triage**

  ```bash
  # Remove dry-run flags from issue-triage.yml
  git checkout -b activate-issue-triage
  # Edit .github/workflows/issue-triage.yml
  # Remove: if: false
  git commit -m "feat: activate issue triage workflow"
  git push
  gh pr create --title "Activate Issue Triage" --body "Phase 2 Day 1"
  gh pr merge <pr-number> --squash --delete-branch
  ```

- [ ] **Monitor intensively (every 2 hours until 10:00 PM UTC)**
  - [ ] 4:30 PM: Check issue triage runs
  - [ ] 6:30 PM: Check issue triage runs
  - [ ] 8:30 PM: Check issue triage runs
  - [ ] 10:30 PM: Final check

- [ ] **Metrics for Day 1**
  - [ ] Issues triaged: \_\_\_\_\_ (count)
  - [ ] Labels applied correctly: \_\_\_\_\_ %
  - [ ] False positives: \_\_\_\_\_ (count)
  - [ ] Team feedback: ☐ Positive ☐ Neutral ☐ Negative

### Day 2: Feb 26 - Add Auto-Assign Reviewers

- [ ] **9:00 AM UTC - Activate Auto-Assign Reviewers**

  ```bash
  git checkout -b activate-auto-assign
  # Edit .github/workflows/auto-assign-reviewers.yml
  # Remove: if: false
  git commit -m "feat: activate auto-assign reviewers workflow"
  git push
  gh pr create --title "Activate Auto-Assign Reviewers" --body "Phase 2 Day 2"
  gh pr merge <pr-number> --squash --delete-branch
  ```

- [ ] **Monitor intensively (every 2 hours)**
  - [ ] 11:00 AM: Check reviewer assignments
  - [ ] 1:00 PM: Check reviewer assignments
  - [ ] 3:00 PM: Check reviewer assignments
  - [ ] 5:00 PM: Final check

- [ ] **Metrics for Day 2**
  - [ ] PRs auto-assigned: \_\_\_\_\_ (count)
  - [ ] Correct reviewers: \_\_\_\_\_ %
  - [ ] Team feedback: ☐ Positive ☐ Neutral ☐ Negative

### Day 3: Feb 27 - Add Status Sync

- [ ] **9:00 AM UTC - Activate Status Sync**

  ```bash
  git checkout -b activate-status-sync
  # Edit .github/workflows/status-sync.yml
  # Remove: if: false
  git commit -m "feat: activate status sync workflow"
  git push
  gh pr create --title "Activate Status Sync" --body "Phase 2 Day 3"
  gh pr merge <pr-number> --squash --delete-branch
  ```

- [ ] **Monitor normally (2x daily)**
  - [ ] 9:00 AM: Check status sync
  - [ ] 5:00 PM: Check status sync

- [ ] **Metrics for Day 3**
  - [ ] Status syncs: \_\_\_\_\_ (count)
  - [ ] Success rate: \_\_\_\_\_ %

### Day 4: Feb 28 - Add Stale Management

- [ ] **9:00 AM UTC - Activate Stale Management**

  ```bash
  git checkout -b activate-stale-management
  # Edit .github/workflows/stale-management.yml
  # Remove: if: false
  git commit -m "feat: activate stale management workflow"
  git push
  gh pr create --title "Activate Stale Management" --body "Phase 2 Day 4"
  gh pr merge <pr-number> --squash --delete-branch
  ```

- [ ] **Monitor normally (2x daily)**
  - [ ] 9:00 AM: Check stale marking
  - [ ] 5:00 PM: Check stale marking

- [ ] **Metrics for Day 4**
  - [ ] Items marked stale: \_\_\_\_\_ (count)
  - [ ] False positives: \_\_\_\_\_ (count)

---

## End of Week Review (Feb 28, 5:00 PM UTC)

### Success Criteria Check

- [ ] **Technical Metrics**
  - [ ] Workflow success rate: \_\_\_\_\_ % (target: >95%)
  - [ ] Notification delivery: \_\_\_\_\_ % (target: >99%)
  - [ ] P1 response time: \_\_\_\_\_ min (target: \<30 min)
  - [ ] False positives: \_\_\_\_\_ % (target: \<5%)

- [ ] **Operational Metrics**
  - [ ] Zero critical failures: ☐ Yes ☐ No
  - [ ] All workflows operational: ☐ Yes ☐ No
  - [ ] Monitoring dashboard accurate: ☐ Yes ☐ No

- [ ] **Team Feedback**
  - [ ] Survey sent to repository team
  - [ ] Responses collected: \_\_\_\_\_ (count)
  - [ ] Average satisfaction: \_\_\_\_\_ /10 (target: >8.0)
  - [ ] Would recommend to other repos: \_\_\_\_\_ %

### Retrospective

**What went well:**

- ***
- ***
- ***

**What could be improved:**

- ***
- ***
- ***

**Action items:**

- ***
- ***
- ***

### Monthly Review Meeting Prep (Feb 28, 6:00 PM UTC)

- [ ] **Create presentation slides**
  - [ ] Month 1 results summary (from Feb metrics)
  - [ ] Week 5 Slack integration demo
  - [ ] Week 6 pilot repository results
  - [ ] Week 7-8 plans preview

- [ ] **Prepare live demos**
  - [ ] Slack notification examples (P0/P1/P2/P3)
  - [ ] Daily summary in #workflow-metrics
  - [ ] Pilot repository workflow runs
  - [ ] Metrics dashboard

- [ ] **Document pilot results**
  - [ ] Create: `docs/WEEK6_PILOT_RESULTS.md`
  - [ ] Include: Metrics, feedback, lessons learned
  - [ ] Attach: Survey results, charts, screenshots

---

## Rollback Procedure

### Trigger Conditions

- [ ] Workflow success rate \< 90%
- [ ] Multiple critical failures
- [ ] Negative team feedback
- [ ] Stakeholder request

### Immediate Rollback (\< 5 minutes)

```bash
# Disable all workflows
gh workflow disable issue-triage.yml --repo <owner/repo>
gh workflow disable auto-assign-reviewers.yml --repo <owner/repo>
gh workflow disable status-sync.yml --repo <owner/repo>
gh workflow disable stale-management.yml --repo <owner/repo>
```

### Post-Rollback Actions

- [ ] **Notify stakeholders**

  ```
  🔴 Workflow Automation Pilot - ROLLED BACK

  Repository: <owner/repo>
  Reason: [specific reason]
  Status: All workflows disabled
  Next steps: Root cause analysis within 24 hours

  Contact: @workflow-team in #workflow-alerts
  ```

- [ ] **Create incident issue**

  ```bash
  gh issue create \
    --title "Pilot Rollback: <repo-name>" \
    --label "incident,workflow-automation" \
    --body "Rollback reason: [reason]..."
  ```

- [ ] **Document lessons learned**
  - [ ] Root cause identified
  - [ ] Preventive measures defined
  - [ ] Timeline for re-attempt established

---

## Communication Templates

### Pre-Deployment Email

```
Subject: Workflow Automation Pilot Starting in [Repository Name]

Team,

We're excited to announce that [repository-name] has been selected for our
workflow automation pilot, starting February 24, 2026.

What to Expect:
• Phase 1 (24 hours): Workflows run in passive mode - no changes, just observation
• Phase 2 (4 days): Gradual activation of automation features
• Training: Optional 15-minute session on [date/time]

Benefits:
✅ Automatic issue triaging and labeling
✅ Smart reviewer assignment based on changed files
✅ Stale issue/PR management
✅ Real-time Slack notifications for important events

Timeline:
• Feb 24, 2:00 PM: Phase 1 starts (passive mode)
• Feb 25, 2:00 PM: Phase 2 starts (active mode)
• Feb 28, 5:00 PM: Week 6 review

Questions? Join #pilot-[repo-name] or contact @workflow-team.

Thanks,
Workflow Team
```

### Post-Deployment Announcement

```
🎉 Workflow Automation Pilot Complete!

Repository: [owner/repo]
Duration: Feb 24-28, 2026 (4 days)

Results:
✅ Success Rate: [X]%
✅ Issues Triaged: [X]
✅ PRs Auto-Assigned: [X]
✅ Team Satisfaction: [X]/10

Thank you to everyone who participated! Your feedback was invaluable.

Next: Results presentation at Monthly Review Meeting (Feb 28, 6 PM UTC).
```

---

## Files and Resources

### Generated During Week 6

- [ ] `automation/config/pilot-<repo-name>-config.yml` - Configuration
- [ ] `generated_workflows/*.yml` - Generated workflows
- [ ] `docs/WEEK6_PILOT_RESULTS.md` - Results documentation
- [ ] `reports/week6-pilot-metrics.json` - Metrics data
- [ ] `reports/week6-survey-results.csv` - Survey responses

### Reference Documents

- [ ] `docs/WEEK6_REPOSITORY_EXPANSION_GUIDE.md` - Overall guide
- [ ] `docs/SLACK_INTEGRATION_TRAINING.md` - Training materials
- [ ] `docs/PRODUCTION_WORKFLOW_INTEGRATION.md` - Integration patterns
- [ ] `automation/scripts/evaluate_repository.py` - Evaluation tool
- [ ] `automation/scripts/generate_pilot_workflows.py` - Generator tool

---

## Sign-Off

**Deployment Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date:
\_\_\_\_\_\_\_\
**Repository Maintainer:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
Date: \_\_\_\_\_\_\_\
**Engineering Manager:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_

---

_Week 6 Deployment Checklist v1.0 - Created 2026-02-22_
