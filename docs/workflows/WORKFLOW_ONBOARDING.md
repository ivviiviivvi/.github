# Workflow System Onboarding

> **Materials for training team members on the new workflow system**

**Last Updated:** January 15, 2026\
**Duration:** 30-60 minutes\
**Audience:**
Maintainers and Contributors

______________________________________________________________________

## 📋 Session Outline

### Part 1: Overview (10 minutes)

- What is the workflow system?
- Why we built it
- Key benefits

### Part 2: For Contributors (15 minutes)

- How to use the system
- What to expect
- Getting help

### Part 3: For Maintainers (20 minutes)

- Daily responsibilities
- Using automation tools
- Handling edge cases

### Part 4: Q&A (15 minutes)

- Open questions
- Clarifications
- Feedback

______________________________________________________________________

## 🎤 Presentation Script

### Opening (2 minutes)

> **Slide 1: Title**
>
> "Welcome! Today we're introducing our new workflow system that will streamline
> how we manage discussions, issues, and pull requests.
>
> This system follows GitHub best practices and automates repetitive tasks,
> letting us focus on what matters: building great software and fostering
> community."

> **Slide 2: Agenda**
>
> "We'll cover three main areas:
>
> 1. What the system does
> 1. How contributors use it
> 1. How maintainers manage it
>
> Please hold questions until the Q&A section, but feel free to take notes!"

______________________________________________________________________

### Part 1: System Overview (8 minutes)

> **Slide 3: The Problem**
>
> "Before this system, we faced challenges:
>
> - Issues sat untriaged for days
> - PRs waited too long for reviewers
> - Stale items cluttered our backlog
> - Manual labeling was time-consuming
> - Status wasn't synchronized between issues and PRs
>
> **Demo:** \[Show screenshot of old workflow with unlabeled issues\]"

> **Slide 4: The Solution**
>
> "Our new workflow system provides:
>
> - **Automatic triage**: Issues get labeled within minutes
> - **Smart reviewer assignment**: Right people notified automatically
> - **Status synchronization**: Issues and PRs stay in sync
> - **SLA enforcement**: We respond within 48 hours
> - **Stale management**: Old items are flagged and cleaned up
>
> Everything happens automatically through GitHub Actions."

> **Slide 5: Workflow Stages**
>
> "Think of it as a pipeline with quality gates:
>
> ```
> Discussion → Issue → Pull Request → Merge
>      ↓         ↓          ↓            ↓
>   Explore   Commit    Implement    Deploy
> ```
>
> Each stage has:
>
> - Clear entry criteria
> - Automated checks
> - Expected outcomes
> - Time expectations"

> **Slide 6: Key Features**
>
> "Five main automations power the system:
>
> 1. **Issue Triage** (48hr SLA)
>
>    - Auto-labels: type, priority, status
>    - Detects bugs, features, security issues
>    - Tracks triage completion
>
> 1. **Reviewer Assignment**
>
>    - Reads CODEOWNERS file
>    - Assigns based on changed files
>    - Excludes PR author
>
> 1. **Status Sync**
>
>    - Links issues to PRs
>    - Updates labels automatically
>    - Adds contextual comments
>
> 1. **Stale Management**
>
>    - 90 days for issues
>    - 30 days for PRs
>    - 7-day grace period
>
> 1. **Assignment Warnings**
>
>    - 14-day inactivity warning
>    - 21-day auto-unassign
>
> **Demo:** \[Show workflow run logs\]"

______________________________________________________________________

### Part 2: For Contributors (15 minutes)

> **Slide 7: Contributor Journey**
>
> "Let's walk through a typical contribution:
>
> **Phase 1: Idea (Optional)**
>
> - Start a discussion to explore ideas
> - Get feedback from community
> - Refine the approach
>
> **Phase 2: Issue Creation**
>
> - Use issue template
> - Automation adds 'needs-triage' label
> - Maintainer triages within 48 hours
>
> **Phase 3: Assignment**
>
> - Request assignment or it's assigned to you
> - Issue labeled 'status: in-progress'
> - You have 14 days before inactivity warning
>
> **Phase 4: Development**
>
> - Create feature branch
> - Make your changes
> - Write tests
>
> **Phase 5: Pull Request**
>
> - Open PR with 'Fixes #123'
> - Reviewers auto-assigned
> - CI checks run automatically
>
> **Phase 6: Review**
>
> - Address feedback
> - Push changes
> - PR merged when approved"

> **Slide 8: What You'll See**
>
> "As a contributor, automation will:
>
> ✅ Add labels to your issues automatically\
> ✅ Assign reviewers to your PRs\
> ✅
> Sync status between issue and PR\
> ✅ Add helpful comments with next steps\
> ✅
> Warn you if assigned issue is inactive for 14 days\
> ✅ Close stale items after
> 7-day grace period
>
> **Demo:** \[Create test issue, show auto-labeling\]"

> **Slide 9: Best Practices for Contributors**
>
> "To work effectively with the system:
>
> **DO:**
>
> - ✅ Use issue templates completely
> - ✅ Link PRs to issues with 'Fixes #123'
> - ✅ Update issue if you're blocked
> - ✅ Respond to automation comments
> - ✅ Ask for help when needed
>
> **DON'T:**
>
> - ❌ Remove automation labels
> - ❌ Go silent on assigned issues
> - ❌ Ignore reviewer feedback
> - ❌ Open PRs without linked issues (for features)
> - ❌ Remove 'Fixes #' from PR descriptions"

> **Slide 10: Getting Help**
>
> "If you have questions:
>
> 1. **Read the guide**: [CONTRIBUTOR_WORKFLOW.md](CONTRIBUTOR_WORKFLOW.md)
> 1. **Ask in discussions**: General Q&A category
> 1. **Tag a maintainer**: Use @mention in your issue/PR
> 1. **Check FAQs**: Common questions answered
>
> The workflow is designed to guide you, not block you!"

______________________________________________________________________

### Part 3: For Maintainers (20 minutes)

> **Slide 11: Maintainer Responsibilities**
>
> "As a maintainer, you're responsible for:
>
> **Daily (15-30 min):**
>
> - Check notifications and triage new items
> - Review PRs awaiting approval
> - Respond to mentions
> - Monitor automation health
>
> **Weekly (30 min):**
>
> - Review metrics dashboard
> - Check in on in-progress items
> - Handle stale item warnings
>
> **Monthly (1 hour):**
>
> - Analyze trends
> - Adjust automation if needed
> - Update documentation"

> **Slide 12: Triage Process**
>
> "Triage is REQUIRED within 48 hours:
>
> **Step 1: Validate**
>
> - Is the issue clear and complete?
> - Can you reproduce it (if bug)?
> - Is it in scope?
> - Any duplicates?
>
> **Step 2: Label**
>
> - Type: bug, feature, docs, etc.
> - Priority: critical, high, medium, low
> - Area: frontend, backend, etc. (optional)
>
> **Step 3: Context**
>
> - Add triage notes
> - Set acceptance criteria
> - Identify dependencies
>
> **Step 4: Remove 'needs-triage'**
>
> - Automation handles this when type/priority/status added
>
> **Demo:** \[Show triage process on test issue\]"

> **Slide 13: Review Priorities**
>
> "Review PRs in this order:
>
> 1. 🚨 Critical fixes
> 1. 🔒 Security patches
> 1. ⚠️ Breaking changes
> 1. ✅ Ready PRs from active contributors
> 1. 📝 Draft PRs (quick feedback only)
> 1. 🎓 First-time contributor PRs
>
> Target: First review within 24 hours for non-draft PRs"

> **Slide 14: Using Automation**
>
> "Key automation dashboards:
>
> **For Triage:**
>
> - [Needs triage](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage)
> - [Critical items](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3A%22priority%3A+critical%22)
> - [Blocked items](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues?q=is%3Aopen+label%3A%22status%3A+blocked%22)
>
> **For Reviews:**
>
> - [Awaiting review](https://github.com/%7B%7BORG_NAME%7D%7D/.github/pulls?q=is%3Apr+is%3Aopen+label%3Aawaiting-review)
> - [Changes requested](https://github.com/%7B%7BORG_NAME%7D%7D/.github/pulls?q=is%3Apr+is%3Aopen+label%3Achanges-requested)
>
> **For Monitoring:**
>
> - [Actions tab](https://github.com/%7B%7BORG_NAME%7D%7D/.github/actions) -
>   workflow runs
> - Metrics report - daily stats
>
> **Demo:** \[Navigate through filters\]"

> **Slide 15: Handling Edge Cases**
>
> "Common situations:
>
> **Unresponsive contributor:**
>
> - Day 14: Automation warns
> - Day 21: Automation unassigns
> - You: Offer help, consider reassigning
>
> **Contentious PR:**
>
> - Facilitate discussion
> - Seek consensus
> - Make final decision if needed
> - Document reasoning
>
> **Automation error:**
>
> - Check workflow logs
> - Fix manually if needed
> - Report bug if recurring
>
> **False positive stale:**
>
> - Remove stale label
> - Add comment explaining
> - Consider adjusting timers"

> **Slide 16: Metrics & Health**
>
> "Monitor these KPIs weekly:
>
> | Metric              | Target | Action If Below  |
> | ------------------- | ------ | ---------------- |
> | Triage rate (48h)   | 90%    | Review backlog   |
> | Reviewer assignment | 95%    | Check CODEOWNERS |
> | Avg review time     | \<24h  | Add reviewers    |
> | Merge rate          | >80%   | Improve feedback |
>
> **Demo:** \[Show metrics dashboard\]"

> **Slide 17: Best Practices for Maintainers**
>
> "To maintain quality and community:
>
> **Communication:**
>
> - Be welcoming and encouraging
> - Provide constructive feedback
> - Explain the 'why' behind decisions
> - Thank contributors regularly
>
> **Decision Making:**
>
> - Seek team input
> - Document decisions
> - Be consistent
> - Update standards as needed
>
> **Quality:**
>
> - Maintain high standards
> - Apply consistently
> - Help contributors meet them"

______________________________________________________________________

### Part 4: Q&A (15 minutes)

> **Slide 18: Common Questions**
>
> "Let's address frequent questions:
>
> **Q: What if automation makes a mistake?** A: Fix manually, report if it's a
> pattern. Automation learns over time.
>
> **Q: Can I still label things manually?** A: Yes! Automation supplements,
> doesn't replace manual work.
>
> **Q: What if I disagree with a label?** A: Change it! Automation won't fight
> you.
>
> **Q: How do I disable a workflow?** A: Edit the .yml file or disable in
> Actions settings. Requires admin.
>
> **Q: What if I'm blocked on an issue?** A: Add 'status: blocked' label and
> comment explaining. Maintainers will help.
>
> **Q: Can we customize the timers?** A: Yes! Edit workflow files. Suggest
> changes if you think timers need adjustment."

> **Slide 19: Resources**
>
> "Documentation you need:
>
> **For Everyone:**
>
> - [Workflow Design](WORKFLOW_DESIGN.md) - Complete architecture
> - [Visualization](WORKFLOW_VISUALIZATION.md) - Flow diagrams
>
> **For Contributors:**
>
> - [Contributor Guide](CONTRIBUTOR_WORKFLOW.md) - Step-by-step
> - [Contributing](../../CONTRIBUTING.md) - General guidelines
>
> **For Maintainers:**
>
> - [Maintainer Guide](MAINTAINER_WORKFLOW.md) - Operations manual
> - [Implementation Summary](../reports/WORKFLOW_IMPLEMENTATION_SUMMARY.md) -
>   Deployment
>
> **Bookmarks:** Save these links!"

> **Slide 20: Next Steps**
>
> "What happens now:
>
> **This Week:**
>
> - System goes live with passive workflows (labels only)
> - No items will be auto-closed yet
> - Monitor for issues
>
> **Next Week:**
>
> - Enable stale management after team feedback
> - Review metrics dashboard
> - Adjust timers if needed
>
> **Ongoing:**
>
> - Weekly metrics review
> - Monthly retrospective
> - Continuous improvement
>
> **Your Action:** Try the system! Open a test issue, create a test PR, see how
> it works."

> **Slide 21: Open Q&A**
>
> "Now let's open the floor for questions!"
>
> \[Allow 10-15 minutes for questions\]

______________________________________________________________________

## 📊 Slides Template

Below are suggested slides for a presentation tool (PowerPoint, Google Slides,
etc.):

### Slide 1: Title

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
   WORKFLOW SYSTEM
   ONBOARDING

   Streamlining Our Development
   Process with Automation
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Slide 2: Agenda

```
📋 TODAY'S AGENDA

1. System Overview (10 min)
   - What and why

2. For Contributors (15 min)
   - How to use the system

3. For Maintainers (20 min)
   - Daily operations

4. Q&A (15 min)
```

### Slide 3: The Problem

```
😓 BEFORE: CHALLENGES

❌ Issues untriaged for days
❌ PRs waiting for reviewers
❌ Stale items everywhere
❌ Manual labeling tedious
❌ Status out of sync

[Screenshot of messy issue list]
```

### Slide 4: The Solution

```
✨ NOW: WORKFLOW SYSTEM

✅ Automatic triage (48hr SLA)
✅ Smart reviewer assignment
✅ Status synchronization
✅ SLA enforcement
✅ Stale management

Powered by GitHub Actions
```

### Slide 5: Workflow Stages

```
📍 THE PIPELINE

Discussion → Issue → PR → Merge
    ↓         ↓      ↓       ↓
 Explore   Commit  Build  Deploy

Each stage has:
• Entry criteria
• Automated checks
• Expected outcomes
• Time expectations
```

### Slide 6: Key Features

```
🤖 FIVE AUTOMATIONS

1. Issue Triage
   Auto-labels, 48hr SLA

2. Reviewer Assignment
   Based on CODEOWNERS

3. Status Sync
   Links issues ↔ PRs

4. Stale Management
   90d issues, 30d PRs

5. Assignment Warnings
   14d warning, 21d unassign
```

### Slide 7: Contributor Journey

```
🚀 YOUR CONTRIBUTION PATH

1. Idea → Discussion (optional)
2. Issue → Gets triaged (48h)
3. Assigned → Start work
4. Develop → Feature branch
5. PR → Auto-reviewers
6. Merge → Issue closes

System guides you!
```

### Slide 8: What You'll See

```
👀 AUTOMATION IN ACTION

✅ Auto-labels on issues
✅ Reviewers on PRs
✅ Status sync comments
✅ Next-step guidance
✅ Inactivity warnings
✅ Stale notifications

[Demo: Create issue, show labels]
```

### Slide 9: Contributor Best Practices

```
✅ DO:
• Use templates fully
• Link PRs with "Fixes #123"
• Update if blocked
• Respond to comments

❌ DON'T:
• Remove automation labels
• Go silent when assigned
• Ignore reviewers
• Skip issue links
```

### Slide 10: Getting Help

```
🆘 NEED HELP?

1. Read the guide
   docs/CONTRIBUTOR_WORKFLOW.md

2. Ask in discussions
   Q&A category

3. Tag maintainer
   @mention in issue/PR

4. Check FAQs
   Common questions

System designed to help!
```

______________________________________________________________________

## 🎬 Demo Checklist

Prepare these demonstrations:

- [ ] **Demo 1: Issue Auto-Labeling**

  - Create new issue with bug description
  - Show `needs-triage` label added
  - Show automation comment
  - Manually add type/priority labels
  - Show `needs-triage` removed

- [ ] **Demo 2: PR Reviewer Assignment**

  - Create PR touching specific files
  - Show CODEOWNERS file
  - Show reviewers auto-assigned
  - Show `awaiting-review` label

- [ ] **Demo 3: Status Sync**

  - Create PR with "Fixes #123"
  - Show issue updated with PR link
  - Mark PR ready for review
  - Show issue labels updated
  - Merge PR
  - Show issue closed

- [ ] **Demo 4: Metrics Dashboard**

  - Navigate to workflow metrics report
  - Explain each KPI
  - Show trend over time
  - Highlight action items

- [ ] **Demo 5: Workflow Logs**

  - Open GitHub Actions tab
  - Select a workflow run
  - Show execution steps
  - Point out where to find errors

______________________________________________________________________

## 📝 Post-Session Materials

After the training, provide:

1. **Slide deck** (PDF or PowerPoint)
1. **Recording** of the session
1. **Quick reference guide** (one-pager)
1. **FAQ document** (based on Q&A)
1. **Feedback survey**

### Quick Reference Template

```markdown
# Workflow Quick Reference

## For Contributors

**Create Issue:**

1. Use template
2. Wait for triage (48h)
3. Request assignment

**Create PR:**

1. Link with "Fixes #123"
2. Reviewers auto-assigned
3. Address feedback
4. Merge when approved

**If Stuck:**

- Add comment
- Tag maintainer
- Check discussions

## For Maintainers

**Daily:**

- Triage new issues (<48h)
- Review PRs (<24h)
- Check notifications

**Weekly:**

- Review metrics
- Check stale items
- Monitor automation

**Filters:**

- [Needs triage](link)
- [Awaiting review](link)
- [Critical](link)

**Docs:**

- Contributor: [link]
- Maintainer: [link]
```

______________________________________________________________________

## 🔄 Feedback & Iteration

After the session:

1. **Collect feedback** via survey
1. **Review questions** from Q&A
1. **Update FAQ** with new questions
1. **Improve slides** based on feedback
1. **Schedule follow-up** if needed

**Survey Questions:**

- How clear was the presentation? (1-5)
- Do you feel prepared to use the system? (1-5)
- What was most confusing?
- What additional training would help?
- Any suggestions for improvement?

______________________________________________________________________

**This onboarding material is a living document. Update as the system evolves!**

______________________________________________________________________

_Last Updated: January 15, 2026_
