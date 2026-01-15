# GitHub Workflow Visualization

> **Visual representation of the discussion/issue/PR workflow**

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DISCUSSION PHASE (Optional)                       │
│                          Idea Exploration                            │
├─────────────────────────────────────────────────────────────────────┤
│  Community discusses → Gather feedback → Build consensus            │
│  Timeline: 3-7 days                                                 │
│  Exit: Convert to issue OR Mark as answered OR Close                │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         ISSUE PHASE                                  │
│                      Work Item Definition                            │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 1: Triage (0-48 hours)                                       │
│    • Auto-labeled: needs-triage, status: new                        │
│    • Maintainer reviews and classifies                              │
│    • Apply: type, priority, area labels                             │
│    • Exit: status: backlog                                          │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 2: Backlog                                                   │
│    • Ready for implementation                                       │
│    • Available for contributors                                     │
│    • Exit: Contributor claims → Assignment                          │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 3: In Progress                                               │
│    • Contributor assigned                                           │
│    • status: in-progress                                            │
│    • Active development                                             │
│    • Exit: PR opened → status: in-review                           │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PULL REQUEST PHASE                              │
│                    Implementation Review                             │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 1: Draft (Optional)                                          │
│    • Work in progress                                               │
│    • Basic checks run                                               │
│    • Exit: Mark ready for review                                    │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 2: Ready for Review                                          │
│    • Reviewers auto-assigned via CODEOWNERS                         │
│    • Full CI suite runs                                             │
│    • Security scans execute                                         │
│    • Quality gates enforced                                         │
│    • awaiting-review label                                          │
│    • Exit: All checks pass + Approval                               │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 3: Approved                                                  │
│    • Auto-merge enabled                                             │
│    • Final checks                                                   │
│    • Exit: Merged to main                                           │
├─────────────────────────────────────────────────────────────────────┤
│  Stage 4: Merged                                                    │
│    • Branch deleted                                                 │
│    • Linked issues closed                                           │
│    • status: done                                                   │
│    • Added to changelog                                             │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DEPLOYMENT PHASE                               │
│                          Release                                     │
├─────────────────────────────────────────────────────────────────────┤
│  • Release notes generated                                          │
│  • Version tagged                                                   │
│  • Stakeholders notified                                            │
│  • Deployed to production                                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Issue Flow

```
┌──────────────┐
│ Issue        │
│ Created      │
│              │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Add labels         │
       │ │ - needs-triage                 │
       │ │ - status: new                  │
       │ │ - Auto-detect type/priority    │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐       Yes     ┌──────────────┐
│   Invalid    │──────────────>│ Close with   │
│   or         │               │ explanation  │
│ Duplicate?   │               └──────────────┘
└──────┬───────┘
       │ No
       │
       ▼
┌──────────────┐
│ Maintainer   │
│ Triages      │
│ (< 48 hours) │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: SLA check          │
       │ │ - Warn if > 48 hours           │
       │ │ - Escalate priority            │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ Labels       │
│ Applied:     │
│ - type       │
│ - priority   │
│ - area       │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Remove triage      │
       │ │ - Remove: needs-triage         │
       │ │ - Add: status: backlog         │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│  Backlog     │
│ (Available)  │
└──────┬───────┘
       │
       │ Contributor claims
       │
       ▼
┌──────────────┐
│  Assigned    │
│              │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Update status      │
       │ │ - Add: status: in-progress     │
       │ │ - Notify assignee              │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐       Yes     ┌──────────────┐
│ Inactive     │──────────────>│ Warn at      │
│ > 14 days?   │               │ 14 days      │
└──────┬───────┘               └──────┬───────┘
       │ No                           │
       │                              │ No response
       │                              │ after 7 days
       │                              ▼
       │                      ┌──────────────┐
       │                      │ Unassign &   │
       │                      │ Return to    │
       │                      │ Backlog      │
       │                      └──────────────┘
       │
       ▼
┌──────────────┐
│  PR Opened   │
│  and Linked  │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Sync status        │
       │ │ - Add: status: in-review       │
       │ │ - Link PR to issue             │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│  PR Under    │
│  Review      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  PR Merged   │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Close issue        │
       │ │ - Add: status: done            │
       │ │ - Close automatically          │
       │ │ - Add to changelog             │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Complete   │
└──────────────┘
```

## Detailed PR Flow

```
┌──────────────┐
│   PR         │
│  Opened      │
└──────┬───────┘
       │
       ▼
┌──────────────┐       Yes     ┌──────────────┐
│   Draft?     │──────────────>│ Draft Mode   │
└──────┬───────┘               │ Basic checks │
       │ No                    └──────────────┘
       │
       ▼
┌──────────────┐
│  Ready for   │
│  Review      │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Assign reviewers   │
       │ │ - Parse CODEOWNERS             │
       │ │ - Match changed files          │
       │ │ - Assign reviewers & teams     │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│  Reviewers   │
│  Assigned    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  CI Checks   │
│  Running     │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Quality Gates:                 │
       │ │ ✓ Linting                      │
       │ │ ✓ Tests                        │
       │ │ ✓ Coverage                     │
       │ │ ✓ Security scans               │
       │ │ ✓ Pre-commit hooks             │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐       Fail    ┌──────────────┐
│ All Checks   │──────────────>│  Fix and     │
│   Pass?      │               │  Push Again  │
└──────┬───────┘               └──────────────┘
       │ Pass
       │
       ▼
┌──────────────┐
│  Code        │
│  Review      │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Review Areas:                  │
       │ │ - Correctness                  │
       │ │ - Code quality                 │
       │ │ - Testing                      │
       │ │ - Documentation                │
       │ │ - Security                     │
       │ │ - Performance                  │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐       Yes     ┌──────────────┐
│  Changes     │──────────────>│  Address     │
│ Requested?   │               │  Feedback    │
└──────┬───────┘               └──────┬───────┘
       │ No                           │
       │                              │
       │<─────────────────────────────┘
       │
       ▼
┌──────────────┐
│  Approved    │
│ (1+ from     │
│ CODEOWNERS)  │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Enable auto-merge  │
       │ │ - Check all requirements       │
       │ │ - Enable auto-merge            │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ Auto-merge   │
│  Pending     │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Final checks:                  │
       │ │ ✓ Branch up to date            │
       │ │ ✓ No conflicts                 │
       │ │ ✓ All checks still green       │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Merged!    │
└──────┬───────┘
       │
       │ ┌────────────────────────────────┐
       │ │ Automation: Post-merge         │
       │ │ - Delete branch                │
       │ │ - Close linked issues          │
       │ │ - Update changelog             │
       │ │ - Notify stakeholders          │
       │ └────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Complete   │
└──────────────┘
```

## Status Transitions

```
Issue Statuses:
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  needs-      │───>│   status:    │───>│   status:    │
│  triage      │    │   backlog    │    │ in-progress  │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                                               ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   status:    │<───│   status:    │<───│   status:    │
│    done      │    │   blocked    │    │  in-review   │
└──────────────┘    └──────────────┘    └──────────────┘
```

```
PR Statuses:
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   status:    │───>│  awaiting-   │───>│   approved   │
│    draft     │    │   review     │    │              │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │   merged     │
                                        └──────────────┘
```

## Automation Triggers

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTOMATION MATRIX                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Issue Created ──────> issue-triage.yml                         │
│    ├─> Add labels                                               │
│    ├─> Welcome message                                          │
│    └─> Start SLA timer                                          │
│                                                                  │
│  Daily Cron ─────────> issue-triage.yml                         │
│    └─> Check SLA violations                                     │
│                                                                  │
│  Issue Labeled ───────> issue-triage.yml                        │
│    └─> Remove triage label when complete                        │
│                                                                  │
│  PR Opened ───────────> auto-assign-reviewers.yml               │
│    ├─> Parse CODEOWNERS                                         │
│    ├─> Assign reviewers                                         │
│    └─> Add tracking labels                                      │
│                                                                  │
│  PR Ready ────────────> pr-quality-checks.yml                   │
│    ├─> Run CI checks                                            │
│    ├─> Run security scans                                       │
│    └─> Calculate coverage                                       │
│                                                                  │
│  PR/Issue Change ─────> status-sync.yml                         │
│    ├─> Sync issue to PR                                         │
│    ├─> Update labels                                            │
│    └─> Add comments                                             │
│                                                                  │
│  PR Approved ─────────> auto-enable-merge.yml                   │
│    ├─> Check all requirements                                   │
│    ├─> Enable auto-merge                                        │
│    └─> Wait for merge                                           │
│                                                                  │
│  Daily Cron ──────────> stale-management.yml                    │
│    ├─> Mark stale items                                         │
│    ├─> Close very stale                                         │
│    ├─> Warn inactive assigned                                   │
│    └─> Unassign long-inactive                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Timeline Example

```
Day 0
09:00  Issue created
       ├─> Automation: Add labels, welcome message
       └─> Status: needs-triage

Day 0-1
       Maintainer reviews

Day 1
14:00  Issue triaged
       ├─> Automation: Remove triage label
       ├─> Labels: type: feature, priority: medium
       └─> Status: backlog

Day 2
10:00  Contributor claims issue
       ├─> Maintainer assigns
       ├─> Automation: Update status
       └─> Status: in-progress

Day 2-5
       Development work

Day 5
16:00  PR opened
       ├─> Automation: Assign reviewers via CODEOWNERS
       ├─> Automation: Run CI checks
       ├─> Automation: Update issue status
       └─> Status: in-review (both PR and issue)

Day 6
10:00  Code review
       └─> Changes requested

Day 7
15:00  Changes pushed
       ├─> Automation: Re-run CI
       └─> Request re-review

Day 8
11:00  PR approved
       ├─> Automation: Enable auto-merge
       └─> All checks pass

Day 8
11:05  PR merged
       ├─> Automation: Delete branch
       ├─> Automation: Close issue
       ├─> Automation: Add to changelog
       └─> Status: done

Total Time: 8 days (within typical timelines)
```

---

_This visualization complements the detailed documentation in
[WORKFLOW_DESIGN.md](WORKFLOW_DESIGN.md)_
