# Suggest-Awesome Prompts: Quality of Life Enhancements

## Overview

The `suggest-awesome-*` family of prompts has been enhanced with comprehensive
quality metrics, improved visual hierarchy, and intelligent categorization to
help teams discover the best GitHub Copilot assets from the
[awesome-copilot repository](https://github.com/github/awesome-copilot)<!-- link:github.awesome_copilot -->.

## What's New

### 🎯 Executive Summaries

Every suggestion now starts with a high-level overview:

```
🎯 Executive Summary
- Total Prompts Analyzed: 47 prompts from awesome-copilot
- Already Installed: 15 prompts (32%)
- Recommended: 12 high-value additions
- Optional: 8 nice-to-have prompts
- Not Recommended: 12 (overlap or low relevance)
```

This gives you instant visibility into:

- Total coverage
- What you already have
- How many recommendations to review
- What percentage is redundant

### 📊 Priority-Based Recommendations

Suggestions are now grouped by priority with clear visual indicators:

#### 🔥🔥🔥 Critical (Must-Have)

- > 70% new content
- Fills critical capability gaps
- Highest quality indicators
- Immediate value proposition

#### 🔥🔥 High Priority

- 50-70% new content
- Strong recommendations
- High value-add
- Should install soon

#### ⚡⚡ Medium Priority

- 35-50% new content
- Quality improvements
- Enhancement opportunities

#### 💡 Optional

- \<25% new content
- Nice-to-have features
- Consider based on specific needs

### 📈 Quality Indicators

Each suggestion includes comprehensive quality metrics:

| Indicator           | Meaning                   | Example                        |
| ------------------- | ------------------------- | ------------------------------ |
| ⭐ Stars            | GitHub stars (popularity) | ⭐ 450 stars                   |
| 📈 Trending         | Recent growth >20-30%     | 📈 +35% in 30 days             |
| 🔥 Popular          | Top 15-25% adoption       | 🔥 Top 20%                     |
| 💬 Discussions      | Active community          | 💬 125 discussions             |
| ✅ Maintained       | Recently updated          | ✅ Updated 2 weeks ago         |
| 📚 Well-documented  | Comprehensive guides      | 📚 Setup guides + examples     |
| 🎓 Course Featured  | In GitHub courses         | 🎓 Featured in Security course |
| 👥 Team Recommended | Official endorsement      | 👥 GitHub team endorsed        |

### 🗂️ Intelligent Categorization

#### For Instructions (Technology-Based)

```
🎯 Languages
- ✅ C#: 3 variants (English, Japanese, Korean)
- ❌ Rust: Missing (recommended)
- ⚠️ Python: Partial coverage

☁️ Cloud & Infrastructure
- ✅ Azure: Extensive (7 instructions)
- ❌ AWS: Missing
- ⚠️ Terraform: Basic coverage
```

#### For Chat Modes (Role-Based)

```
🏗️ Architecture & Design
- ✅ Azure Architect: Principal level
- ✅ API Architect: Specialized
- ❌ General Architect: Missing

👨‍💻 Development Specialists
- ✅ C#/.NET: Expert engineer
- ✅ React: Frontend specialist
- ⚠️ Python: Needs dedicated mode
```

#### For Agents (Integration-Based)

```
🚨 Incident Management & Monitoring
- ✅ PagerDuty: Incident response
- ✅ Dynatrace: Observability expert
- ❌ DataDog: Missing

🔒 Security & Compliance
- ✅ StackHawk: Security onboarding
- ✅ JFrog: Security remediation
- ❌ Snyk: Missing
```

#### For Collections (Theme-Based)

```
🔒 Security & Quality
- 🔥🔥🔥 Security & Compliance: 14 new assets (recommended)
- ✅ Code Review: Well-covered
- ❌ Accessibility: Missing

🧪 Development Practices
- 🔥🔥 Testing Excellence: 11 new assets (recommended)
- ⚡ Performance Optimization: 7 new assets
```

### 💰 Value Analysis

#### ROI Indicators

- Setup time estimates
- Expected benefits (% improvements)
- Coverage gap analysis
- Technology stack alignment scores

#### Example from Collections:

```
Installation Impact:
- 📁 Will add to prompts/: 6 security-focused prompts
- 📁 Will add to instructions/: 8 language-specific guides
- 📁 Will add to chatmodes/: 3 specialized personas
- ⏱️ Setup Time: ~2 hours
- 💰 ROI: High - reduces vulnerabilities by ~60%
```

## Prompt-Specific Features

### 1. suggest-awesome-github-copilot-prompts

**Focus**: Task-specific prompts for code generation and problem-solving

**Special Features**:

- Priority-based grouping (High/Medium/Optional)
- Workflow type categorization
- Quick-scan table format

**Best For**:

- Teams looking for specific workflow prompts
- Filling gaps in code generation capabilities
- Finding popular community solutions

### 2. suggest-awesome-github-copilot-instructions

**Focus**: Coding standards and best practices per language/framework

**Special Features**:

- Technology stack categorization
- Language coverage analysis
- Framework-specific recommendations
- Multi-language variants detection

**Best For**:

- Establishing coding standards
- Onboarding new languages/frameworks
- Ensuring consistent code quality

### 3. suggest-awesome-github-copilot-chatmodes

**Focus**: Specialized AI personas for different roles

**Special Features**:

- Role/persona categorization
- Expertise area mapping
- Coverage gap highlighting
- Critical role identification

**Best For**:

- Building specialized development teams
- Filling expertise gaps
- Role-based assistance

### 4. suggest-awesome-github-copilot-agents

**Focus**: MCP-enabled custom agents for tool integrations

**Special Features**:

- Integration type categorization
- Tool stack alignment
- Setup complexity indicators
- MCP compatibility checks
- Partner/enterprise status

**Best For**:

- Integrating external tools
- Automation opportunities
- Partner platform connections

### 5. suggest-awesome-github-copilot-collections

**Focus**: Curated bundles of related assets

**Special Features**:

- Detailed asset breakdown by type
- New vs. existing calculation
- Theme-based organization
- Multi-asset ROI analysis
- Category coverage gaps
- Priority decision matrix

**Best For**:

- Bulk capability additions
- Themed improvements (e.g., "Security", "Testing")
- Comprehensive coverage
- Strategic planning

## Usage Examples

### Example 1: Finding High-Priority Security Assets

Use `suggest-awesome-github-copilot-collections` and look for:

1. Executive summary showing security gaps
1. 🔥🔥🔥 Critical priority collections
1. 🔒 Security & Quality category
1. High new asset percentage (>70%)

### Example 2: Adding Language Support

Use `suggest-awesome-github-copilot-instructions` and review:

1. Technology category breakdown
1. 🎯 Languages section for gaps
1. Quality indicators (stars, maintenance)
1. Coverage comparison with existing

### Example 3: Building Specialized Team

Use `suggest-awesome-github-copilot-chatmodes` and focus on:

1. Role category breakdown
1. Missing critical roles (❌ indicators)
1. Priority recommendations for key personas
1. Expertise alignment with project needs

### Example 4: Integrating External Tools

Use `suggest-awesome-github-copilot-agents` and examine:

1. Integration category breakdown
1. Tool stack currently in use
1. Setup complexity and prerequisites
1. MCP compatibility and enterprise readiness

## Quality Metrics Explained

### Popularity Metrics

- **Stars**: Direct indicator of community adoption
- **Forks**: Shows active usage and customization
- **Watchers**: Indicates ongoing interest

### Quality Signals

- **Last Updated**: Freshness (30-60 days = excellent)
- **Maintenance Frequency**: Regular commits indicate health
- **Documentation**: Examples and guides = production-ready
- **Contributors**: Multiple contributors = community supported
- **Issue Resolution**: Fast resolution = responsive maintenance

### Adoption Indicators

- **Course Featured**: Official GitHub endorsement
- **Blog Posts**: Community recognition
- **Trending**: Recent momentum and growth
- **Team Recommended**: Verified quality

### Relevance Scoring

- **Stack Match**: Alignment with your technologies
- **Gap Analysis**: How much new value is added
- **Team Need**: Based on chat history and patterns
- **Workflow Fit**: Integration with existing processes

## Priority Decision Framework

### When to Install Immediately (🔥🔥🔥)

- Fills critical capability gap (no alternative exists)
- > 70% new assets in collections
- High quality indicators (>400 stars, trending)
- Immediate, measurable value proposition
- Team explicitly requested or discussed

### When to Install Soon (🔥🔥 / ⚡⚡)

- 50-70% new assets in collections
- Enhances existing capabilities significantly
- Good quality indicators (>300 stars)
- Clear improvement potential
- Moderate setup effort with good ROI

### When to Consider Later (⚡ / 💡)

- 25-50% new assets in collections
- Incremental improvements
- Moderate quality indicators
- Nice-to-have enhancements
- Lower priority on roadmap

### When to Skip (⛔)

- \<25% new assets in collections
- Significant overlap with existing
- Low relevance to tech stack
- Outdated or poorly maintained
- Better alternatives available

## Integration with Workflow

### Step 1: Discovery Phase

Run the appropriate suggest-awesome prompt based on your needs:

- General capabilities → `collections`
- Specific language → `instructions`
- Role/persona needed → `chatmodes`
- Tool integration → `agents`
- Specific workflow → `prompts`

### Step 2: Analysis Phase

Review the output focusing on:

1. **Executive Summary**: Get the big picture
1. **Priority Sections**: Start with 🔥🔥🔥 Critical
1. **Quality Indicators**: Verify community support
1. **Category Breakdown**: Identify systematic gaps
1. **Value Propositions**: Understand ROI

### Step 3: Selection Phase

Use the decision framework to filter:

- Must-haves (critical gaps + high quality)
- Should-haves (good value + moderate effort)
- Nice-to-haves (incremental + low priority)
- Skip (overlap + low relevance)

### Step 4: Installation Phase

Follow the prompt guidance to:

1. Confirm selections with team
1. Install assets to appropriate directories
1. Configure as needed
1. Test and validate
1. Document in team guidelines

## Tips for Best Results

### 1. Run Regularly

- Quarterly reviews for new additions
- After major tech stack changes
- When adopting new tools/frameworks
- Following team feedback or pain points

### 2. Use Category Breakdowns

- Identify systematic gaps
- Plan phased rollouts by category
- Balance coverage across types

### 3. Consider Quality Over Quantity

- Prioritize highly-rated assets
- Check maintenance status
- Look for team endorsements
- Verify documentation quality

### 4. Think Holistically

- Collections for comprehensive coverage
- Individual assets for targeted needs
- Complementary assets work better together

### 5. Track Adoption

- Monitor which assets get used
- Gather team feedback
- Iterate and refine
- Share success stories

## Troubleshooting

### "Too Many Recommendations"

- Focus on 🔥🔥🔥 Critical priority first
- Review executive summary percentages
- Use category breakdown to prioritize areas
- Consider collections for bulk additions

### "Not Enough New Assets"

- Your coverage may already be excellent!
- Look for ⚡ Medium priority enhancements
- Check for newer versions (🔄 indicators)
- Focus on specific gaps identified in categories

### "Unsure About Quality"

- Check ⭐ stars (>300 = well-adopted)
- Look for 📈 trending (growing interest)
- Verify ✅ maintained status
- Prefer 🎓 course-featured assets

### "Wrong Technology Stack"

- Prompts analyze your repository automatically
- If mismatched, check chat history context
- Consider providing explicit technology info
- Use technology-specific category breakdowns

## Future Enhancements

Planned improvements include:

- [ ] Automated A/B comparison of similar assets
- [ ] Historical trending data over 6-12 months
- [ ] Team usage statistics integration
- [ ] Custom quality threshold filtering
- [ ] Saved recommendation profiles
- [ ] Automated installation workflows
- [ ] Success metrics tracking
- [ ] Community rating integration

## Related Documentation

- [Agent Registry](AGENT_REGISTRY.md)
- [Agents Documentation](README.agents.md)
- [Instructions Documentation](README.instructions.md)
- [Prompts Documentation](README.prompts.md)
- [Chat Modes Documentation](README.chatmodes.md)
- [Collections Documentation](README.collections.md)
- [GitHub Awesome-Copilot Repository](https://github.com/github/awesome-copilot)<!-- link:github.awesome_copilot -->

## Feedback

Have suggestions for improving these suggest-awesome prompts?

- Open an issue with the `enhancement` label
- Contribute improvements via pull request
- Share your success stories in discussions
- Report quality metric accuracy issues

---

**Last Updated**: 2025-12-28\
**Version**: 2.0 (Quality Metrics & Visual
Hierarchy Enhancement)
