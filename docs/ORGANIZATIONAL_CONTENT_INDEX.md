# Organizational Content Master Index

> **Complete guide to issues, discussions, projects, and wikis in the
> Ivviiviivvi organization**

This document serves as the central index for all organizational content
creation resources, guidelines, and templates.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Templates & Tools](#templates--tools)
- [Automation](#automation)
- [Best Practices](#best-practices)
- [Support](#support)

## Overview

This organization provides comprehensive frameworks for creating and managing:

1. **📝 Issues** - Tracking work, bugs, and improvements
1. **💬 Discussions** - Community engagement and knowledge sharing
1. **📊 Projects** - Visual project management and tracking
1. **📚 Wikis** - Collaborative documentation and knowledge bases

### Why This Matters

Effective organizational content:

- ✅ **Improves transparency** - Everyone knows what's happening
- ✅ **Enhances collaboration** - Easy communication and coordination
- ✅ **Preserves knowledge** - Documented decisions and solutions
- ✅ **Accelerates onboarding** - New members find answers quickly
- ✅ **Builds community** - Engaged, informed contributors

### What's Included

```
📦 Organizational Content Framework
├── 📖 Comprehensive Documentation
│   ├── Issue Taxonomy & Guidelines
│   ├── Discussion Management Guide
│   ├── Project Planning Framework
│   └── Wiki Structure & Templates
├── 🎨 Ready-to-Use Templates
│   ├── Issue templates (20+ types)
│   ├── Discussion starters (12 categories)
│   ├── Project configurations (10 templates)
│   └── Wiki page templates (8 types)
├── 🤖 Automation Workflows
│   ├── Batch issue creation
│   ├── Discussion management
│   ├── Project synchronization
│   └── Wiki maintenance
└── 📊 Best Practices & Examples
    ├── Real-world examples
    ├── Success patterns
    ├── Anti-patterns to avoid
    └── Metrics & KPIs
```

## Quick Start

### For Repository Administrators

**1. Enable Features** (5 minutes)

```bash
# Enable all features on a repository
gh repo edit owner/repo \
  --enable-issues \
  --enable-discussions \
  --enable-projects \
  --enable-wiki
```

**2. Review Documentation** (30 minutes)

Read the guide relevant to what you're setting up:

- [Issue Taxonomy](ISSUE_TAXONOMY.md) - Issue classification
- [Discussion Guide](DISCUSSION_GUIDE.md) - Discussion framework
- [Projects Guide](PROJECTS_GUIDE.md) - Project management
- [Wiki Guide](WIKI_GUIDE.md) - Wiki structure

**3. Deploy Templates** (15 minutes)

```bash
# Run the creation workflow
gh workflow run create-organizational-content.yml \
  -f content_type=all \
  -f dry_run=false
```

**4. Customize for Your Needs** (1-2 hours)

- Adjust labels and categories
- Modify templates
- Set up automation
- Train your team

### For Content Creators

**1. Choose Your Content Type**

What are you creating today?

- 📝 [Creating Issues](#creating-issues) - Track work items
- 💬 [Starting Discussions](#starting-discussions) - Engage community
- 📊 [Managing Projects](#managing-projects) - Organize work
- 📚 [Writing Wiki Pages](#writing-wiki-pages) - Document knowledge

**2. Use the Right Template**

Each content type has ready-to-use templates in this repository.

**3. Follow Best Practices**

See the relevant guide for standards and conventions.

### For Community Members

**1. Find What You Need**

- 🔍 **Search Issues** - Find existing work or report bugs
- 💬 **Browse Discussions** - Ask questions or share ideas
- 📊 **View Projects** - See what's in progress
- 📚 **Read Wiki** - Learn from documentation

**2. Contribute**

- 📝 Create issues for bugs or features
- 💬 Participate in discussions
- 📖 Improve wiki documentation
- 🤝 Help others in the community

## Documentation

### Core Guides

| Document                                                            | Purpose                            | Audience                  | Length       |
| ------------------------------------------------------------------- | ---------------------------------- | ------------------------- | ------------ |
| [🚀 Quick Start](ORGANIZATIONAL_CONTENT_QUICK_START.md)             | Get started in 15 minutes          | Everyone                  | ~5 min read  |
| [🛠️ Implementation Guide](ORGANIZATIONAL_CONTENT_IMPLEMENTATION.md) | Step-by-step deployment            | Administrators            | ~45 min read |
| [📝 Issue Taxonomy](ISSUE_TAXONOMY.md)                              | Comprehensive issue classification | Maintainers, Contributors | ~25 min read |
| [💬 Discussion Guide](DISCUSSION_GUIDE.md)                          | Discussion framework and templates | Community Managers        | ~40 min read |
| [📊 Projects Guide](PROJECTS_GUIDE.md)                              | Project management best practices  | Project Managers          | ~50 min read |
| [📚 Wiki Guide](WIKI_GUIDE.md)                                      | Wiki structure and maintenance     | Documentation Team        | ~60 min read |

### Quick References

| Document                                            | Purpose               | Time   |
| --------------------------------------------------- | --------------------- | ------ |
| [Issue Quick Ref](#issue-quick-reference)           | Common issue patterns | 5 min  |
| [Discussion Quick Ref](#discussion-quick-reference) | Discussion templates  | 5 min  |
| [Project Quick Ref](#project-quick-reference)       | Project setup         | 10 min |
| [Wiki Quick Ref](#wiki-quick-reference)             | Wiki page creation    | 10 min |

### Supporting Documentation

- [Labels Guide](LABELS.md) - Standard label taxonomy
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards
- [Governance](GOVERNANCE.md) - Decision-making process

## Templates & Tools

### Issue Templates

**Location**: `ISSUE_TEMPLATE/`

| Template               | Use Case               | When to Use               |
| ---------------------- | ---------------------- | ------------------------- |
| Bug Report             | Report defects         | Something is broken       |
| Feature Request        | Suggest features       | New functionality needed  |
| Documentation          | Doc improvements       | Docs missing or unclear   |
| Question               | Ask questions          | Need clarification        |
| Security Vulnerability | Report security issues | Found a security flaw     |
| Performance            | Performance issues     | Something is slow         |
| Best Practices Review  | Request review         | Want feedback on approach |

**Usage**:

```bash
# Create issue from template
gh issue create --template bug_report.yml
```

### Discussion Templates

**Location**: `.github/discussion-starters/`

| Template         | Category       | Purpose                  |
| ---------------- | -------------- | ------------------------ |
| Welcome          | General        | Onboard new members      |
| Monthly Showcase | Show and Tell  | Highlight community work |
| Best Practices   | Best Practices | Share knowledge          |
| Q&A Template     | Q&A            | Structured questions     |
| Feature Proposal | Ideas          | Propose features         |

**Usage**:

```bash
# Start discussion from template
cat .github/discussion-starters/welcome.md | \
  gh discussion create --category "General" \
  --title "Welcome!" --body-file -
```

### Project Templates

**Location**: `.github/project-templates/`

| Template        | Focus               | Best For             |
| --------------- | ------------------- | -------------------- |
| Product Roadmap | Features & releases | Product planning     |
| Bug Triage      | Bug management      | Quality assurance    |
| Sprint Planning | Agile sprints       | Development teams    |
| Infrastructure  | DevOps work         | Infrastructure teams |
| Documentation   | Doc tracking        | Doc writers          |
| Security        | Security work       | Security teams       |

**Usage**: Import via GitHub web UI or API (CLI doesn't support Projects v2
creation yet)

### Wiki Templates

**Location**: `.github/wiki-templates/`

| Template        | Purpose            | Sections             |
| --------------- | ------------------ | -------------------- |
| Home            | Wiki entry point   | Overview, navigation |
| Installation    | Setup guide        | Requirements, steps  |
| Quick Start     | Getting started    | First steps          |
| Tutorial        | Step-by-step guide | Learning path        |
| How-To          | Task guide         | Specific tasks       |
| Reference       | API/CLI docs       | Complete reference   |
| FAQ             | Common questions   | Q&A format           |
| Troubleshooting | Problem solving    | Issues & solutions   |
| Architecture    | System design      | Technical overview   |

**Usage**:

```bash
# Initialize wiki from templates
git clone https://github.com/org/repo.wiki.git
cp .github/wiki-templates/*.md repo.wiki/
cd repo.wiki && git add . && git commit -m "Initialize" && git push
```

## Automation

### Workflow: Create Organizational Content

**File**: `.github/workflows/create-organizational-content.yml`

**Purpose**: Automate creation of issues, discussions, projects, and wikis

**Features**:

- ✅ Batch issue creation (20+ pre-defined issues)
- ✅ Discussion starter generation
- ✅ Project template export
- ✅ Wiki structure setup
- ✅ Dry-run mode for preview
- ✅ Target specific repositories

**Usage**:

```bash
# Preview what would be created (dry run)
gh workflow run create-organizational-content.yml \
  -f content_type=all \
  -f dry_run=true

# Create all content
gh workflow run create-organizational-content.yml \
  -f content_type=all \
  -f dry_run=false

# Create only issues
gh workflow run create-organizational-content.yml \
  -f content_type=issues \
  -f dry_run=false

# Target specific repository
gh workflow run create-organizational-content.yml \
  -f content_type=all \
  -f target_repo=owner/specific-repo \
  -f dry_run=false
```

**Inputs**:

| Input          | Description       | Options                                            | Default      |
| -------------- | ----------------- | -------------------------------------------------- | ------------ |
| `content_type` | What to create    | `all`, `issues`, `discussions`, `projects`, `wiki` | Required     |
| `target_repo`  | Target repository | Repository slug or empty for current               | Current repo |
| `dry_run`      | Preview only      | `true`, `false`                                    | `true`       |

### Other Automation

- **Stale Management**: Auto-close inactive issues/PRs
- **Label Sync**: Synchronize labels across repos
- **Project Sync**: Auto-add issues to projects
- **Wiki Backup**: Automated wiki backups

See [Automation Guide](automation/) for details.

## Best Practices

### Issue Management

**Do**:

- ✅ Use descriptive, searchable titles
- ✅ Fill out templates completely
- ✅ Apply appropriate labels
- ✅ Link related issues
- ✅ Keep issues focused (one topic)
- ✅ Update status regularly

**Don't**:

- ❌ Create duplicate issues (search first)
- ❌ Use issues for questions (use Discussions)
- ❌ Leave issues stale without updates
- ❌ Use vague titles like "Bug" or "Help"

**Example Good Issue**:

```markdown
Title: "API: /users endpoint returns 500 on invalid email format"

Body:

## Description

The /users endpoint crashes when receiving an invalid email format.

## Steps to Reproduce

1. POST to /users with email: "invalid.email"
2. Observe 500 response

## Expected

- 400 Bad Request with validation error

## Actual

- 500 Internal Server Error

## Environment

- Version: 1.2.3
- OS: Ubuntu 22.04
```

### Discussion Management

**Do**:

- ✅ Choose the right category
- ✅ Use welcoming, inclusive language
- ✅ Mark helpful answers
- ✅ Update the original post with resolutions
- ✅ Link to related issues/docs

**Don't**:

- ❌ Use Discussions for bug reports
- ❌ Hijack others' discussions
- ❌ Leave questions unanswered
- ❌ Post duplicate discussions

### Project Management

**Do**:

- ✅ Keep projects focused and scoped
- ✅ Update status regularly
- ✅ Use custom fields consistently
- ✅ Archive completed work
- ✅ Review and groom weekly

**Don't**:

- ❌ Try to track everything in one project
- ❌ Let projects get stale
- ❌ Ignore automation opportunities
- ❌ Overcomplicate with too many fields

### Wiki Maintenance

**Do**:

- ✅ Keep content current
- ✅ Use consistent formatting
- ✅ Link between related pages
- ✅ Include "Last Updated" dates
- ✅ Back up regularly

**Don't**:

- ❌ Let documentation go stale
- ❌ Use wiki for official release docs
- ❌ Forget to update after code changes
- ❌ Create orphaned pages

## Quick Reference Cards

### Issue Quick Reference

```bash
# Create bug report
gh issue create --label bug --title "Bug: [description]"

# Create feature request
gh issue create --label enhancement --title "Feature: [description]"

# Create from template
gh issue create --template feature_request.yml

# List open issues
gh issue list --state open

# View issue
gh issue view 123

# Close issue
gh issue close 123 --comment "Fixed in #456"
```

### Discussion Quick Reference

```bash
# Create discussion
gh discussion create \
  --category "Q&A" \
  --title "How do I...?" \
  --body "Question details"

# List discussions
gh discussion list

# View discussion
gh discussion view 123

# Close discussion
gh discussion close 123

# Mark as answered
gh discussion mark-answer 123 --answer 456
```

### Project Quick Reference

```bash
# View projects (requires web UI or API)
# CLI doesn't fully support Projects v2 yet

# Add issue to project (via API)
gh api graphql -f query='
  mutation {
    addProjectV2ItemById(input: {
      projectId: "PROJECT_ID"
      contentId: "ISSUE_ID"
    }) {
      item {
        id
      }
    }
  }
'
```

### Wiki Quick Reference

```bash
# Clone wiki
git clone https://github.com/org/repo.wiki.git

# Add page
cd repo.wiki
cat > New-Page.md << EOF
# New Page
Content here
EOF

# Commit and push
git add New-Page.md
git commit -m "Add new page"
git push

# View wiki online
open https://github.com/org/repo/wiki
```

## Success Metrics

### Issue Metrics

- **Time to Triage**: \< 24 hours
- **Time to First Response**: \< 48 hours
- **Resolution Time**: Varies by priority
  - P0: 4 hours
  - P1: 24 hours
  - P2: 1 week
  - P3: As capacity allows
- **Backlog Size**: \< 100 open issues
- **Stale Rate**: \< 10% > 60 days old

### Discussion Metrics

- **Response Rate**: > 80% get response
- **Response Time**: \< 24 hours median
- **Answer Rate**: > 60% Q&A marked answered
- **Participation**: > 20% of community active monthly
- **Satisfaction**: > 4.5/5 helpfulness rating

### Project Metrics

- **Completion Rate**: > 80% items completed
- **Velocity**: Consistent sprint-to-sprint
- **Cycle Time**: \< 1 week median
- **Blocked Rate**: \< 10% items blocked
- **Accuracy**: 90%+ estimates accurate

### Wiki Metrics

- **Coverage**: > 80% features documented
- **Freshness**: > 90% updated within 6 months
- **Usage**: > 1000 page views/month
- **Search Success**: > 70% find answers
- **Contribution**: > 10 contributors/quarter

## Support

### Getting Help

**For Users**:

- 💬
  [Ask in Discussions](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->
- 📖 Read the documentation guides
- 🔍 Search existing issues and discussions

**For Maintainers**:

- 📧 Contact organization administrators
- 📞 Schedule office hours
- 📚 Review detailed guides

**For Contributors**:

- 🤝 [Contributing Guide](CONTRIBUTING.md)
- 💬
  [Community Discussions](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->
- 🐛
  [Report Issues](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

### Feedback & Improvements

This framework is continuously evolving. We welcome:

- 💡 Suggestions for improvements
- 🐛 Bug reports in templates or docs
- 📖 Documentation enhancements
- 🎨 New templates and examples

### Resources

**Internal**:

- [Organization README](../README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)

**External**:

- [GitHub Issues Docs](https://docs.github.com/en/issues)<!-- link:docs.github_issues -->
- [GitHub Discussions Docs](https://docs.github.com/en/discussions)<!-- link:docs.github_discussions -->
- [GitHub Projects Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects)<!-- link:docs.github_projects -->
- [GitHub Wiki Docs](https://docs.github.com/en/communities/documenting-your-project-with-wikis)<!-- link:docs.github_wikis -->

## Version History

| Version | Date       | Changes                                 |
| ------- | ---------- | --------------------------------------- |
| 1.0.0   | 2025-12-28 | Initial comprehensive framework release |

## Maintenance

**Document Owner**: @ivviiviivvi/documentation-team\
**Review Frequency**:
Quarterly\
**Last Reviewed**: 2025-12-28\
**Next Review**: 2026-03-28

---

**📝 Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)\
**💬 Discuss**:
[GitHub Discussions](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->\
**🐛
Report Issues**:
[GitHub Issues](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

**Built with ❤️ by the Ivviiviivvi community**
