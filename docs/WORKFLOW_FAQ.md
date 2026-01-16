# Workflow System FAQ

## Frequently Asked Questions

Last Updated: January 16, 2026

---

## For Contributors

### General Questions

**Q: What is the workflow system?**

A: The workflow system is a set of 5 GitHub Actions automations that help manage
issues and pull requests more efficiently. It automatically labels issues,
assigns reviewers, syncs status, manages stale items, and tracks metrics.

**Q: How does it affect me as a contributor?**

A: You'll experience:

- Faster issue triage (within 48 hours)
- Automatic reviewer assignment on PRs
- Clear status updates on your contributions
- Automated reminders for inactive items

**Q: Do I need to do anything different?**

A: No! The workflows work automatically. Just:

- Open issues and PRs as usual
- Respond to bot comments if needed
- Link PRs to issues with "Fixes #123" in description

### Issue Management

**Q: Why did a bot add labels to my issue?**

A: The Issue Triage workflow automatically adds `needs-triage` and `status: new`
labels to help maintainers track new issues. A maintainer will review within 48
hours and add appropriate type/priority labels.

**Q: My issue was marked "needs-triage" for over 48 hours. What should I do?**

A: This means it's taking longer than our target response time. Please add a
comment pinging `@workflow-maintainers` or the repository maintainer team.

**Q: Can I add labels to my own issue?**

A: Yes! If you have write access to the repository. If not, suggest labels in
your issue description and maintainers will add them.

**Q: My issue was marked stale. Is it being ignored?**

A: No! Issues are marked stale after 90 days of inactivity to keep the backlog
manageable. If it's still relevant, simply add a comment explaining why it
should stay open and the `stale` label will be removed.

**Q: How do I prevent my issue from going stale?**

A: Add periodic updates, even just "still relevant" comments. Or ask a
maintainer to add the `pinned` label for long-running issues.

### Pull Requests

**Q: Why were reviewers automatically assigned to my PR?**

A: The Auto-Assign Reviewers workflow reads the CODEOWNERS file and
automatically assigns appropriate reviewers based on the files you changed. This
ensures the right people review your code.

**Q: The wrong reviewers were assigned. What should I do?**

A: Don't worry! A maintainer will correct the assignments. You can also comment
tagging the right reviewers: `@username please review`.

**Q: My PR was marked draft but still got reviewers assigned. Is that a bug?**

A: Reviewers are assigned when a PR is opened or moved to "Ready for review". If
your PR is still draft, reviewers won't be notified until you mark it ready.

**Q: How do I link my PR to an issue?**

A: Add "Fixes #123" (replace 123 with issue number) in your PR description. The
Status Sync workflow will automatically update the issue status as your PR
progresses.

**Q: My PR was marked stale after 30 days. Will it be closed?**

A: Not immediately. You'll receive a warning, then 7 days grace period. If
there's still no activity after that, it will be closed. To prevent this, add a
comment with an update or ETA.

### Bot Behavior

**Q: Can I tell the bot to do something?**

A: Not directly. The workflows respond to events (issue opened, PR created,
labels changed, etc.) and GitHub's built-in triggers.

**Q: What if the bot makes a mistake?**

A: Simply correct it manually:

- Remove wrong labels
- Add missing labels
- Reassign reviewers
- Add comments explaining the situation

The bot respects manual overrides and won't revert your changes.

**Q: Can I disable the bot for my issue/PR?**

A: Yes, ask a maintainer to add the `workflow-exempt` label. This prevents all
automated workflows from affecting that item.

---

## For Maintainers

### Operations

**Q: How do I manually trigger a workflow?**

A: Go to Actions tab → Select workflow → Click "Run workflow" button. Some
workflows (like metrics) support manual triggers.

**Q: What happens if I change labels after the bot?**

A: Your changes take precedence. The bot won't revert manual label changes.

**Q: How do I triage an issue?**

A: Simply add type (bug/feature/etc.) and priority (high/critical) labels. The
bot automatically removes `needs-triage` and adds `status: backlog`.

**Q: Can I adjust the 48-hour SLA timer?**

A: Yes, edit `.github/workflows/issue-triage.yml` and change the `48h` value in
the SLA check job. Requires repository admin access.

### CODEOWNERS

**Q: How do I update reviewer assignments?**

A: Edit `.github/CODEOWNERS` file to change which users/teams are assigned for
specific file patterns.

**Q: What's the priority when multiple CODEOWNERS match?**

A: More specific patterns take precedence. The workflow assigns up to 5
individual reviewers and 3 team reviewers.

**Q: Can I exclude someone from auto-assignment?**

A: Yes, remove them from CODEOWNERS or they can be manually removed after
assignment. The PR author is always automatically excluded.

### Stale Management

**Q: How do I prevent an issue/PR from going stale?**

A: Add one of these labels:

- `pinned` - Long-running, should never close
- `security` - Security-related, needs attention
- `fast-track` - Urgent, expedited handling

**Q: Can I adjust stale thresholds?**

A: Yes, edit `.github/workflows/stale-management.yml`:

- Issues: 90 days (change `90d` in config)
- PRs: 30 days (change `30d` in config)
- Grace period: 7 days (change `7d` in close job)

**Q: What resets the inactivity timer?**

A: Any comment (from anyone), new commits, label changes, or issue/PR state
changes reset the timer.

### Monitoring

**Q: How do I check if workflows are running correctly?**

A:

1. Go to Actions tab
1. Filter by workflow name
1. Look for red X (failed) or yellow dot (in progress)
1. Click on runs to see detailed logs

**Q: Where do I find workflow metrics?**

A: Check `docs/WORKFLOW_METRICS_REPORT.md` - updated daily at 9 AM UTC.

**Q: What should I do if a workflow fails?**

A:

1. Check the error logs in Actions tab
1. Common causes: rate limits, permissions, missing labels
1. Fix the issue (create labels, adjust permissions, wait for rate limit)
1. Workflow will retry on next trigger

**Q: How do I see which workflows ran on a specific issue/PR?**

A: Check the issue/PR timeline - workflow actions appear as comments or events.

### Customization

**Q: Can I add custom workflows?**

A: Yes! Add new YAML files to `.github/workflows/`. Follow existing patterns for
permissions and triggers.

**Q: Can I modify existing workflows?**

A: Yes, but carefully:

1. Review workflow documentation first
1. Test changes in a sandbox environment
1. Update documentation if behavior changes
1. Notify team of changes

**Q: How do I add new labels?**

A:

1. Go to Issues tab → Labels
1. Click "New label"
1. Follow naming convention: `category: value` (e.g., `status: new`)
1. Update workflow files if needed

### Troubleshooting

**Q: Workflow is not triggering. Why?**

A: Check:

- GitHub Actions enabled for repository
- Workflow has correct trigger events
- No syntax errors in YAML file
- Workflow file in `.github/workflows/` directory

**Q: Bot posted duplicate comments. What happened?**

A: Likely the workflow ran multiple times due to multiple trigger events. Check
workflow logs to see what triggered it.

**Q: Reviewer assignment not working. Help!**

A: Verify:

- CODEOWNERS file exists at `.github/CODEOWNERS`
- File has correct syntax (see GitHub docs)
- Users/teams mentioned actually exist
- Workflow has `pull-requests: write` permission

**Q: How do I report workflow bugs?**

A: Open an issue with:

- Label: `type: bug, area: workflow`
- Description of unexpected behavior
- Link to affected issue/PR
- Workflow run logs if available

---

## Advanced Topics

### For Repository Admins

**Q: How do I deploy these workflows to a new repository?**

A: Follow the deployment guide in `docs/WORKFLOW_IMPLEMENTATION_SUMMARY.md` or
the checklist in Issue #246.

**Q: Can these workflows work with private repositories?**

A: Yes! GitHub Actions work in private repos. Just ensure your team has
appropriate access.

**Q: What are the rate limits?**

A: GitHub Actions has rate limits for API calls:

- 5000 requests/hour for authenticated requests
- Workflows automatically pause if limit reached
- Metrics workflow runs daily to avoid limits

**Q: How much does this cost in Actions minutes?**

A: Minimal:

- Each workflow run: ~30-60 seconds
- Daily metrics: ~2 minutes
- Total: ~5-10 minutes per day
- Free tier: 2000 minutes/month (enough for most repos)

**Q: Can I use this with GitHub Enterprise?**

A: Yes! All workflows use standard GitHub Actions features available in
Enterprise.

### Security

**Q: Are there security concerns with automated workflows?**

A: We follow security best practices:

- Least-privilege permissions (`issues: write` only when needed)
- No hardcoded secrets (use GitHub Secrets)
- Pinned action versions (@v4, not @main)
- Regular security audits

**Q: Can external contributors trigger workflows?**

A: Yes, but with restrictions:

- First-time contributors need approval to run workflows
- Pull requests from forks have limited permissions
- Secrets are not accessible to fork PRs

**Q: How do I audit workflow actions?**

A: Check:

- Actions tab for complete run history
- Issue/PR timeline for bot actions
- Workflow run logs for detailed execution
- Metrics report for aggregate statistics

### Integration

**Q: Can I integrate with other tools (Slack, PagerDuty, etc.)?**

A: Yes! Add steps to workflows to call external APIs:

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

**Q: Can I use this with GitHub Projects?**

A: Yes! See `docs/GITHUB_PROJECTS_CONFIGURATION.md` for setup guide. Workflows
can automatically update project boards.

**Q: Can I add more complex logic?**

A: Yes! Use:

- GitHub Actions expressions:
  `${{ contains(github.event.issue.labels.*.name, 'bug') }}`
- Custom scripts: Run Python/Node/shell scripts as workflow steps
- Third-party actions: Browse GitHub Marketplace

---

## Getting Help

**Still have questions?**

- 📖 **Read the docs:** Check `docs/` directory for detailed guides
- 💬 **Ask in discussions:** GitHub Discussions → workflow-system category
- 🐛 **Report bugs:** Open issue with `type: bug, area: workflow`
- 👥 **Contact maintainers:** Tag @workflow-maintainers in issues

**Documentation:**

- `docs/CONTRIBUTOR_WORKFLOW.md` - For contributors
- `docs/MAINTAINER_WORKFLOW.md` - For maintainers
- `docs/WORKFLOW_DESIGN.md` - Architecture and design
- `docs/WORKFLOW_TESTING_GUIDE.md` - Testing procedures
- Issue #246 - Deployment tracking

---

**This FAQ is a living document. Have a question not covered here?**\
Open an
issue or discussion and we'll add it!
