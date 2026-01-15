# GitHub Workflow Design: Discussion/Issue/PR Lifecycle

> **Comprehensive workflow design implementing GitHub best practices for
> discussion, issue, and pull request management**

## Table of Contents

- [Overview](#overview)
- [Workflow Principles](#workflow-principles)
- [Lifecycle Stages](#lifecycle-stages)
- [Flow Diagrams](#flow-diagrams)
- [Automation Strategy](#automation-strategy)
- [Implementation Details](#implementation-details)
- [Metrics and Monitoring](#metrics-and-monitoring)

---

## Overview

This document defines the complete workflow for managing discussions, issues,
and pull requests in alignment with GitHub best practices and this
organization's standards.

### Design Goals

1. **Clear Pathways**: Unambiguous progression from idea to deployment
1. **Automated Quality Gates**: Enforce standards automatically
1. **Transparent Process**: Every stakeholder knows the current state
1. **Community Friendly**: Easy for contributors at all levels
1. **Maintainer Efficient**: Reduce manual overhead for maintainers
1. **Security First**: Integrate security checks at every stage

---

## Workflow Principles

### 1. Progressive Disclosure

Start with discussions for exploration, move to issues for commitment, and PRs
for implementation.

```
Discussion → Issue → Pull Request → Deployment
   (Idea)   (Work)    (Solution)    (Release)
```

### 2. Early Quality Gates

Catch problems early with automated checks at each transition:

- **Discussion → Issue**: Community consensus and maintainer approval
- **Issue → PR**: Clear acceptance criteria and assigned owner
- **PR → Merge**: All CI checks, reviews, and security scans pass
- **Merge → Deploy**: Staging validation before production

### 3. Clear Ownership

Every item has a clear owner and reviewers:

- **Discussions**: Community-owned, maintainer-moderated
- **Issues**: Assigned contributor, tracked by maintainer
- **PRs**: Author-driven, reviewer-approved, CODEOWNERS enforced

### 4. Automated Enforcement

Use GitHub Actions to automate:

- Label management
- Status transitions
- Quality checks
- Notifications
- Stale item management

---

## Lifecycle Stages

### Discussion Lifecycle

#### Stage 1: Idea Submission

**Purpose**: Explore ideas without commitment

**Actions**:

1. User creates discussion in appropriate category
1. Auto-labeled with `status: new`
1. Community provides feedback
1. Maintainers monitor for actionable items

**Automation**:

- Auto-label based on category
- Weekly digest to maintainers
- Link related issues/PRs

**Exit Criteria**:

- Convert to issue (actionable)
- Mark as answered (resolved)
- Archive (not actionable)

#### Stage 2: Community Feedback

**Purpose**: Gather diverse perspectives

**Actions**:

1. Community upvotes and comments
1. Similar discussions linked automatically
1. Maintainers provide guidance

**Automation**:

- Duplicate detection
- Related content linking
- Popularity tracking

#### Stage 3: Resolution

**Outcomes**:

- **Accepted**: Create issue, close discussion
- **Answered**: Mark answered, close with summary
- **Declined**: Comment with reasoning, close
- **Inactive**: Auto-close after 60 days

### Issue Lifecycle

#### Stage 1: Triage (0-2 days)

**Purpose**: Classify and prioritize

**Actions**:

1. Issue created (manual or from discussion)
1. Auto-labeled with `needs-triage`
1. Maintainer reviews within 48 hours
1. Assign priority, type, and area labels

**Automation**:

- Auto-label based on title/content
- SLA reminder at 48 hours
- Template validation

**Exit Criteria**:

- Labels applied: priority, type, area
- `needs-triage` removed
- Move to Backlog or close as invalid

#### Stage 2: Backlog

**Purpose**: Queued for work

**Actions**:

1. Issue ready for implementation
1. Labeled with `status: backlog`
1. Available for contributors to pick up

**Automation**:

- Stale detection (90 days)
- Good first issue identification
- Dependency tracking

**Exit Criteria**:

- Assigned to contributor
- Move to In Progress

#### Stage 3: In Progress

**Purpose**: Active development

**Actions**:

1. Contributor assigns themselves
1. Labeled with `status: in-progress`
1. Linked to draft PR (recommended)

**Automation**:

- Status sync with PR
- Inactivity warnings (14 days)
- Blocker detection

**Exit Criteria**:

- PR opened and linked
- Move to In Review

#### Stage 4: In Review

**Purpose**: Code review and validation

**Actions**:

1. PR opened and linked
1. Labeled with `status: in-review`
1. Reviewers assigned via CODEOWNERS

**Automation**:

- Auto-assign reviewers
- Review reminder (3 days)
- CI status sync

**Exit Criteria**:

- PR approved and merged
- Close issue with reference

#### Stage 5: Done

**Purpose**: Completed and released

**Actions**:

1. Issue closed with PR link
1. Labeled with `status: done`
1. Added to release notes

**Automation**:

- Auto-close on PR merge
- Release note generation
- Changelog update

### Pull Request Lifecycle

#### Stage 1: Draft

**Purpose**: Work in progress

**Actions**:

1. PR opened as draft
1. CI runs basic checks
1. Auto-merge disabled

**Automation**:

- Title validation
- Branch name validation
- Draft checks (linting, formatting)
- Related issue linking

**Exit Criteria**:

- Mark as ready for review
- All draft checks pass

#### Stage 2: Ready for Review

**Purpose**: Request maintainer review

**Actions**:

1. Author marks PR ready
1. Reviewers auto-assigned via CODEOWNERS
1. Full CI suite runs
1. Security scans execute

**Automation**:

- Assign reviewers
- Label based on changes
- Size calculation
- Review reminders

**Quality Gates**:

- ✅ All CI checks pass
- ✅ No merge conflicts
- ✅ Tests pass with coverage
- ✅ Security scans clear
- ✅ Pre-commit hooks pass

**Exit Criteria**:

- At least 1 approval from CODEOWNERS
- All checks pass
- No requested changes

#### Stage 3: Approved

**Purpose**: Ready to merge

**Actions**:

1. Reviewers approve
1. Auto-merge enabled (if configured)
1. Awaiting merge

**Automation**:

- Enable auto-merge
- Final pre-merge checks
- Branch update if needed

**Exit Criteria**:

- PR merged to target branch

#### Stage 4: Merged

**Purpose**: Code integrated

**Actions**:

1. PR merged
1. Branch deleted (if enabled)
1. Issues auto-closed
1. Release tracking

**Automation**:

- Close linked issues
- Delete branch
- Notify stakeholders
- Add to changelog

---

## Flow Diagrams

### High-Level Flow

```
┌─────────────┐
│ Discussion  │
│  (Explore)  │
└──────┬──────┘
       │ Convert
       ▼
┌─────────────┐
│   Issue     │
│  (Define)   │
└──────┬──────┘
       │ Implement
       ▼
┌─────────────┐
│     PR      │
│  (Deliver)  │
└──────┬──────┘
       │ Merge
       ▼
┌─────────────┐
│   Release   │
│  (Deploy)   │
└─────────────┘
```

### Detailed Issue Flow

```
┌─────────────────┐
│  Issue Created  │
│   needs-triage  │
└────────┬────────┘
         │
         ▼
   ┌─────────────┐      ┌─────────────┐
   │   Invalid?  │─YES─→│    Close    │
   └──────┬──────┘      └─────────────┘
          │ NO
          ▼
   ┌─────────────┐
   │   Triaged   │
   │   backlog   │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  Assigned   │
   │ in-progress │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  PR Opened  │
   │  in-review  │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  PR Merged  │
   │    done     │
   └─────────────┘
```

### Detailed PR Flow

```
┌──────────────┐
│ Draft PR     │
│ Created      │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌─────────────┐
│ Basic Checks │─FAIL→│  Block      │
│ Pass?        │      │  Review     │
└──────┬───────┘      └─────────────┘
       │ PASS
       ▼
┌──────────────┐
│ Ready for    │
│ Review       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ CODEOWNERS   │
│ Assigned     │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌─────────────┐
│ All Checks   │─FAIL→│  Request    │
│ Pass?        │      │  Changes    │
└──────┬───────┘      └─────────────┘
       │ PASS
       ▼
┌──────────────┐
│ Reviews      │
│ Approved?    │
└──────┬───────┘
       │ YES
       ▼
┌──────────────┐
│ Auto-merge   │
│ Enabled      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Merged     │
└──────────────┘
```

---

## Automation Strategy

### Critical Automations

#### 1. Label Management

**Trigger**: Issue/PR creation, status changes **Actions**:

- Apply initial labels based on templates
- Update labels on status transitions
- Remove conflicting labels
- Add labels based on file changes

**Implementation**: `.github/workflows/auto-labeler.yml`

#### 2. Triage Enforcement

**Trigger**: New issue creation **Actions**:

- Add `needs-triage` label
- Set SLA timer (48 hours)
- Notify maintainers if SLA expires
- Validate issue template usage

**Implementation**: `.github/workflows/issue-triage.yml`

#### 3. PR Quality Checks

**Trigger**: PR opened/synchronized **Actions**:

- Validate PR title format
- Check for linked issues
- Run linting and formatting
- Execute test suite
- Calculate code coverage
- Run security scans

**Implementation**: `.github/workflows/pr-quality-checks.yml`

#### 4. Review Assignment

**Trigger**: PR ready for review **Actions**:

- Parse CODEOWNERS
- Assign reviewers based on changed files
- Set review reminders
- Track review completion

**Implementation**: CODEOWNERS + `.github/workflows/auto-assign-reviewers.yml`

#### 5. Auto-merge

**Trigger**: All checks pass, approvals received **Actions**:

- Enable auto-merge
- Wait for final checks
- Merge when ready
- Delete branch
- Close linked issues

**Implementation**: `.github/workflows/auto-enable-merge.yml`

#### 6. Stale Item Management

**Trigger**: Scheduled (daily) **Actions**:

- Detect inactive issues (90 days)
- Detect inactive PRs (30 days)
- Warn before closing (7 days)
- Close if no response
- Optionally archive discussions

**Implementation**: `.github/workflows/stale-management.yml`

#### 7. Status Synchronization

**Trigger**: Issue/PR status changes **Actions**:

- Sync issue status with linked PR
- Update project boards
- Notify assignees
- Update labels

**Implementation**: `.github/workflows/status-sync.yml`

### Optional Automations

#### 8. Release Management

**Trigger**: PR merge to main **Actions**:

- Generate changelog
- Create release notes
- Tag version
- Notify stakeholders

#### 9. Community Health

**Trigger**: New contributor **Actions**:

- Welcome message
- Link to contributing guide
- Assign mentor (optional)
- Add `good-first-issue` label

#### 10. Performance Tracking

**Trigger**: Scheduled (weekly) **Actions**:

- Calculate average time to triage
- Calculate average time to merge
- Generate metrics report
- Identify bottlenecks

---

## Implementation Details

### Required Files

#### Templates

1. **Discussion Templates** (existing):
   - `.github/DISCUSSION_TEMPLATE/`
     - `announcements.yml`
     - `general.yml`
     - `ideas.yml`
     - `q-and-a.yml`
     - `show-and-tell.yml`

1. **Issue Templates** (existing):
   - `.github/ISSUE_TEMPLATE/`
     - `bug_report.yml`
     - `feature_request.yml`
     - `documentation.yml`
     - `question.md`
     - `config.yml`

1. **PR Template** (existing):
   - `.github/PULL_REQUEST_TEMPLATE.md`

#### Configuration Files

1. **CODEOWNERS** (existing):
   - `.github/CODEOWNERS`

1. **Labeler Configuration** (create):
   - `.github/labeler.yml`

1. **Auto-merge Configuration** (enhance):
   - `.github/pr-automation.yml`

#### Workflow Files

1. **Core Workflows** (create/enhance):
   - `.github/workflows/issue-triage.yml` - NEW
   - `.github/workflows/auto-assign-reviewers.yml` - NEW
   - `.github/workflows/status-sync.yml` - NEW
   - `.github/workflows/stale-management.yml` - ENHANCE
   - `.github/workflows/auto-labeler.yml` - EXISTING
   - `.github/workflows/pr-quality-checks.yml` - EXISTING
   - `.github/workflows/auto-enable-merge.yml` - EXISTING

1. **Documentation** (create):
   - `docs/WORKFLOW_GUIDE.md` - EXISTING (enhance)
   - `docs/CONTRIBUTOR_WORKFLOW.md` - NEW
   - `docs/MAINTAINER_WORKFLOW.md` - NEW

### Branch Protection Rules

```yaml
Required Status Checks:
  - CI / build
  - CI / test
  - CI / lint
  - Security / CodeQL
  - Security / Secret Scanning
  - Pre-commit / hooks

Required Reviews:
  - At least 1 approval
  - From CODEOWNERS
  - Dismiss stale reviews

Additional Rules:
  - Require branches to be up to date
  - Require signed commits (optional)
  - Include administrators
  - Restrict force pushes
  - Allow deletions (for feature branches)
```

### Label Structure

**Priority Labels**:

- `priority: critical` (red)
- `priority: high` (orange)
- `priority: medium` (yellow)
- `priority: low` (green)

**Type Labels**:

- `type: bug` (red)
- `type: feature` (blue)
- `type: enhancement` (light blue)
- `type: documentation` (dark blue)
- `type: question` (purple)
- `type: security` (dark red)

**Status Labels**:

- `status: needs-triage` (yellow)
- `status: backlog` (gray)
- `status: in-progress` (blue)
- `status: in-review` (purple)
- `status: blocked` (red)
- `status: done` (green)

**Area Labels**:

- `area: frontend` (light green)
- `area: backend` (light blue)
- `area: infrastructure` (light purple)
- `area: documentation` (light yellow)
- `area: testing` (light pink)

---

## Metrics and Monitoring

### Key Performance Indicators (KPIs)

#### Issue Metrics

- **Time to Triage**: Target \< 48 hours
- **Time to First Response**: Target \< 72 hours
- **Time to Resolution**: Track by priority
- **Stale Rate**: Target \< 10%
- **Reopen Rate**: Target \< 5%

#### PR Metrics

- **Time to First Review**: Target \< 48 hours
- **Time to Merge**: Track by size
- **Review Iterations**: Average \< 3
- **CI Success Rate**: Target > 95%
- **Merge Conflict Rate**: Target \< 5%

#### Community Metrics

- **New Contributors**: Track monthly
- **Contributor Retention**: Track quarterly
- **Discussion Conversion Rate**: % → issues
- **Community Satisfaction**: Survey quarterly

### Monitoring Dashboard

Create GitHub Actions workflow to generate weekly reports:

```yaml
Workflow Metrics Report
=======================

Issues:
- Created this week: X
- Closed this week: Y
- Average time to triage: Z hours
- Awaiting triage: N

Pull Requests:
- Opened this week: X
- Merged this week: Y
- Average time to merge: Z hours
- Awaiting review: N

Community:
- New contributors: X
- Active discussions: Y
- Community questions answered: Z
```

---

## Next Steps

1. **Review and Approve**: Team review of workflow design
1. **Implement Core Workflows**: Priority automations first
1. **Update Documentation**: Contributor and maintainer guides
1. **Configure Branch Protection**: Enforce quality gates
1. **Test in Sandbox**: Validate workflows in test repo
1. **Phased Rollout**: Enable gradually with monitoring
1. **Gather Feedback**: Iterate based on team experience
1. **Optimize**: Tune automation timing and thresholds

---

## References

- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [About Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
- [About Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/best-practices-for-github-actions)
- [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

_Last Updated: January 15, 2026_
