# Organizational Content Quick Start

> **Get started in 15 minutes**

This quick start gets you up and running with issues, discussions, projects, and
wikis fast.

## 🎯 Choose Your Path

### Path A: "I Want Everything" (15 minutes)

**For**: New repositories or complete organizational setup

```bash
# 1. Enable all features (2 min)
REPO="your-org/your-repo"
gh repo edit $REPO --enable-issues --enable-discussions --enable-projects --enable-wiki

# 2. Deploy all content (1 min to start)
gh workflow run create-organizational-content.yml \
  -f content_type=all \
  -f target_repo=$REPO \
  -f dry_run=false

# 3. Wait for workflow (10 min)
gh run watch

# 4. Review and customize (2 min)
gh repo view $REPO --web
```

**What you get**:

- ✅ 20+ pre-created issues
- ✅ Discussion categories and starters
- ✅ Project templates ready to use
- ✅ Wiki structure initialized

### Path B: "Just Issues" (5 minutes)

**For**: Better issue management

```bash
# 1. Enable issues
gh repo edit your-org/your-repo --enable-issues

# 2. Deploy issue templates
gh workflow run create-organizational-content.yml \
  -f content_type=issues \
  -f target_repo=your-org/your-repo \
  -f dry_run=false

# 3. Review created issues
gh issue list --repo your-org/your-repo
```

**What you get**:

- ✅ Issue taxonomy applied
- ✅ 20+ tracking issues created
- ✅ Labels configured
- ✅ Templates ready to use

### Path C: "Community Engagement" (5 minutes)

**For**: Building community

```bash
# 1. Enable discussions
gh repo edit your-org/your-repo --enable-discussions

# 2. Set up categories (via web UI)
# Go to Settings → Discussions → Categories

# 3. Create starter discussions
gh discussion create \
  --repo your-org/your-repo \
  --category "General" \
  --title "👋 Welcome!" \
  --body "Welcome to our community! Introduce yourself..."
```

**What you get**:

- ✅ Discussion categories configured
- ✅ Welcome discussion started
- ✅ Engagement framework ready

### Path D: "Project Management" (10 minutes)

**For**: Visual project tracking

```bash
# 1. Enable projects
gh repo edit your-org/your-repo --enable-projects

# 2. Create project (via web UI)
# Go to Projects → New project → Choose template

# 3. Link repository
# Add repository to project
# Configure auto-add workflows
```

**What you get**:

- ✅ Project board created
- ✅ Custom fields configured
- ✅ Views set up
- ✅ Automation enabled

### Path E: "Documentation Hub" (10 minutes)

**For**: Knowledge management

```bash
# 1. Enable wiki
gh repo edit your-org/your-repo --enable-wiki

# 2. Clone and initialize
git clone https://github.com/your-org/your-repo.wiki.git
cd your-repo.wiki

# 3. Copy templates
cp /path/to/.github/wiki-templates/*.md .

# 4. Customize and push
# Edit files with your content
git add . && git commit -m "Initialize wiki" && git push
```

**What you get**:

- ✅ Wiki structure ready
- ✅ Home page created
- ✅ Navigation sidebar
- ✅ Page templates available

## 📚 Next Steps After Quick Start

### Immediate (Today)

1. **Review Created Content**:

   - Browse created issues
   - Check discussion categories
   - Explore project boards
   - Read wiki pages

1. **Customize Key Items**:

   - Update issue descriptions
   - Pin important discussions
   - Adjust project fields
   - Edit wiki home page

1. **Share with Team**:

   - Send announcement
   - Share links
   - Brief explanation

### This Week

1. **Read Documentation**:

   - [Master Index](../reference/ORGANIZATIONAL_CONTENT_INDEX.md) - 20 min
   - [Issue Taxonomy](../reference/ISSUE_TAXONOMY.md) - 25 min
   - Skim other guides as needed

1. **Engage Your Team**:

   - Create first real issues
   - Start discussions
   - Add items to projects
   - Contribute to wiki

1. **Set Up Processes**:

   - Issue triage schedule
   - Discussion moderation
   - Project grooming
   - Wiki maintenance

### This Month

1. **Full Customization**:

   - Tailor all templates
   - Add domain-specific content
   - Set up automation
   - Define workflows

1. **Training**:

   - Team training sessions
   - Document best practices
   - Create examples

1. **Measure & Iterate**:

   - Track metrics
   - Collect feedback
   - Make improvements

## 🔗 Essential Links

### Documentation

- 🗂️ [Master Index](../reference/ORGANIZATIONAL_CONTENT_INDEX.md) - Start here
- 📝 [Issue Taxonomy](../reference/ISSUE_TAXONOMY.md) - Issue types and
  guidelines
- 💬 [Discussion Guide](DISCUSSION_GUIDE.md) - Discussion framework
- 📊 [Projects Guide](PROJECTS_GUIDE.md) - Project templates
- 📚 [Wiki Guide](WIKI_GUIDE.md) - Wiki structure
- 🚀 [Implementation Guide](../analysis/ORGANIZATIONAL_CONTENT_IMPLEMENTATION.md)
  \- Full deployment

### Templates

- `.github/ISSUE_TEMPLATE/` - Issue templates
- `.github/discussion-starters/` - Discussion starters
- `.github/project-templates/` - Project configurations
- `.github/wiki-templates/` - Wiki page templates

### Automation

- `.github/workflows/create-organizational-content.yml` - Content creation
  workflow

## 💡 Quick Tips

### Issues

```bash
# Create from template
gh issue create --template bug_report.yml

# Add to project
gh issue edit 123 --add-project "Product Roadmap"

# Bulk label
gh issue list --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "triage"
```

### Discussions

```bash
# Create discussion
gh discussion create --category "Q&A" --title "How do I...?"

# List by category
gh discussion list --category "Ideas"

# Mark as answered
gh discussion mark-answer 123 --answer 456
```

### Projects

```bash
# View projects (limited CLI support)
gh project list

# For more control, use web UI or GraphQL API
```

### Wiki

```bash
# Clone wiki
git clone https://github.com/org/repo.wiki.git

# Edit locally
cd repo.wiki
vim New-Page.md

# Push changes
git add . && git commit -m "Update" && git push
```

## 🆘 Getting Help

### Quick Answers

- 📖 Check [Master Index](../reference/ORGANIZATIONAL_CONTENT_INDEX.md)
- 🔍 Search documentation
- 💬 Browse discussions

### Ask for Help

- 💬 [Create Discussion](https://github.com/your-org/your-repo/discussions/new)
- 🐛 [Report Issue](https://github.com/your-org/your-repo/issues/new)
- 📧 Contact maintainers

### Common Questions

**Q: Do I need all features?**\
A: No! Start with what you need. Issues are most
common, discussions for community, projects for tracking, wikis for docs.

**Q: Can I customize everything?**\
A: Yes! All templates and configurations are
fully customizable.

**Q: What if my team doesn't adopt it?**\
A: Start small, show value, provide
training, lead by example.

**Q: How do I maintain this?**\
A: Set regular review schedules, assign owners,
automate where possible.

**Q: Can I roll this back?**\
A: Yes! You can disable features, delete content,
or archive as needed. Nothing is permanent.

## ✅ Success Checklist

### Day 1

- [ ] Features enabled
- [ ] Content deployed (if using automation)
- [ ] Quick review completed
- [ ] Team notified

### Week 1

- [ ] Templates customized
- [ ] First real content created
- [ ] Team starting to use
- [ ] Initial feedback collected

### Month 1

- [ ] Active usage established
- [ ] Processes documented
- [ ] Metrics being tracked
- [ ] Continuous improvement started

## 🎉 You're Ready!

You now have:

- ✅ Framework deployed
- ✅ Templates ready
- ✅ Documentation available
- ✅ Path forward clear

**Start creating amazing organizational content!** 🚀

______________________________________________________________________

**Questions?** See [Master Index](../reference/ORGANIZATIONAL_CONTENT_INDEX.md)
or ask in [Discussions](https://github.com/your-org/your-repo/discussions)
