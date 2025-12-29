---
mode: 'agent'
description: 'Suggest relevant GitHub Copilot prompt files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing prompts in this repository.'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---
# Suggest Awesome GitHub Copilot Prompts

Analyze current repository context and suggest relevant prompt files from the [GitHub awesome-copilot repository](https://github.com/github/awesome-copilot/blob/main/docs/README.prompts.md) that are not already available in this repository.

## Process

1. **Fetch Available Prompts**: Extract prompt list and descriptions from [awesome-copilot README.prompts.md](https://github.com/github/awesome-copilot/blob/main/docs/README.prompts.md). Must use `#fetch` tool.
2. **Scan Local Prompts**: Discover existing prompt files in `.github/prompts/` folder
3. **Extract Descriptions**: Read front matter from local prompt files to get descriptions
4. **Analyze Context**: Review chat history, repository files, and current project needs
5. **Compare Existing**: Check against prompts already available in this repository
6. **Match Relevance**: Compare available prompts against identified patterns and requirements
7. **Present Options**: Display relevant prompts with descriptions, rationale, and availability status
8. **Validate**: Ensure suggested prompts would add value not already covered by existing prompts
9. **Output**: Provide structured table with suggestions, descriptions, and links to both awesome-copilot prompts and similar local prompts
   **AWAIT** user request to proceed with installation of specific instructions. DO NOT INSTALL UNLESS DIRECTED TO DO SO.
10. **Download Assets**: For requested instructions, automatically download and install individual instructions to `.github/prompts/` folder. Do NOT adjust content of the files. Use `#todos` tool to track progress. Prioritize use of `#fetch` tool to download assets, but may use `curl` using `#runInTerminal` tool to ensure all content is retrieved.

## Context Analysis Criteria

🔍 **Repository Patterns**:
- Programming languages used (.cs, .js, .py, etc.)
- Framework indicators (ASP.NET, React, Azure, etc.)
- Project types (web apps, APIs, libraries, tools)
- Documentation needs (README, specs, ADRs)

🗨️ **Chat History Context**:
- Recent discussions and pain points
- Feature requests or implementation needs
- Code review patterns
- Development workflow requirements

## Output Format

### 🎯 Executive Summary

Provide a quick overview of the analysis:
- **Total Prompts Analyzed**: X prompts from awesome-copilot
- **Already Installed**: X prompts (X%)
- **Recommended**: X high-value additions
- **Optional**: X nice-to-have prompts
- **Not Recommended**: X (overlap or low relevance)

### 📊 Recommendations by Priority

Display suggestions grouped by priority with enhanced visual hierarchy:

#### 🔥 High Priority (Immediate Value)

| Priority | Prompt Name | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-------------|-------------|-------------------|--------|-------------------|-------------------|
| 🔥🔥🔥 | [code-review](https://github.com/github/awesome-copilot/blob/main/prompts/code-review.md) | Automated code review prompts | ⭐ 450 stars · 📈 Trending · 💬 85 discussions | ❌ Missing | None | Critical gap: Would standardize code review process across all repos |
| 🔥🔥 | [debugging-assistant](https://github.com/github/awesome-copilot/blob/main/prompts/debugging.md) | Advanced debugging workflows | ⭐ 320 stars · 🔥 Popular · ✅ Well-maintained | ❌ Missing | None | High impact: Reduce debugging time by ~40% |

#### ⚡ Medium Priority (Quality Improvements)

| Priority | Prompt Name | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-------------|-------------|-------------------|--------|-------------------|-------------------|
| ⚡⚡ | [test-generation](https://github.com/github/awesome-copilot/blob/main/prompts/test-gen.md) | Auto-generate test cases | ⭐ 280 stars · 📚 Well-documented | ⚠️ Similar | breakdown-test.prompt.md | Enhancement: More comprehensive than existing test prompt |

#### 💡 Optional (Nice to Have)

| Priority | Prompt Name | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-------------|-------------|-------------------|--------|-------------------|-------------------|
| 💡 | [documentation](https://github.com/github/awesome-copilot/blob/main/prompts/documentation.md) | Generate project docs | ⭐ 195 stars · 📖 Stable | ✅ Covered | create-readme.prompt.md, documentation-writer.prompt.md | Already well-covered by 2 existing prompts |

### 📈 Quality Indicators Legend

- ⭐ **Stars**: GitHub stars (popularity metric)
- 📈 **Trending**: Recently gaining traction (>25% growth in 30 days)
- 🔥 **Popular**: High usage/adoption (top 25%)
- 💬 **Discussions**: Active community engagement (>50 discussions)
- ✅ **Well-maintained**: Updated within last 60 days
- 📚 **Well-documented**: Comprehensive documentation
- 🎓 **Course Featured**: Mentioned in popular courses
- 👥 **Team Recommended**: Endorsed by GitHub teams

## Local Prompts Discovery Process

1. List all `*.prompt.md` files directory `.github/prompts/`.
2. For each discovered file, read front matter to extract `description`
3. Build comprehensive inventory of existing prompts
4. Use this inventory to avoid suggesting duplicates

## Quality Metrics Analysis

When analyzing prompts from awesome-copilot, gather and display these quality indicators:

1. **Popularity Metrics**:
   - GitHub stars on the awesome-copilot repository
   - Number of forks and watchers
   - Community discussion activity

2. **Quality Signals**:
   - Last updated date (freshness)
   - Maintenance frequency
   - Documentation completeness
   - Number of contributors
   - Issue resolution rate

3. **Adoption Indicators**:
   - Mentioned in GitHub courses/documentation
   - Featured in GitHub blog posts
   - Trending status (recent star growth)
   - External references and citations

4. **Relevance Scoring**:
   - Match with repository technology stack (0-100%)
   - Gap analysis score (how much value it adds)
   - Team need alignment (based on chat history)

## Requirements

- Use `githubRepo` tool to get content and metadata from awesome-copilot repository
- Gather popularity and quality metrics from GitHub API (with fallback to cached/estimated values if API unavailable)
- Scan local file system for existing prompts in `.github/prompts/` directory
- Read YAML front matter from local prompt files to extract descriptions
- Compare against existing prompts in this repository to avoid duplicates
- **PRIORITIZE** prompts with highest quality indicators and relevance scores
- Focus on gaps in current prompt library coverage
- Validate that suggested prompts align with repository's purpose and standards
- Provide clear, data-driven rationale for each suggestion with metrics
- Include links to both awesome-copilot prompts and similar local prompts
- Group recommendations by priority (High/Medium/Optional)
- Use visual hierarchy with emojis, badges, and formatting for scannability
- Provide executive summary with key statistics
- Don't provide any additional information or context beyond the structured output

## Icons & Status Reference

### Status Indicators
- ✅ **Covered**: Already installed or well-covered by existing prompts
- ❌ **Missing**: Not available in repository, recommended for installation
- ⚠️ **Similar**: Partial coverage, enhancement opportunity
- 🔄 **Update**: Newer version available

### Priority Levels
- 🔥🔥🔥 **Critical**: Must-have, immediate installation recommended
- 🔥🔥 **High**: Strong recommendation, high value-add
- ⚡⚡ **Medium**: Quality improvement opportunity
- 💡 **Optional**: Nice-to-have, consider based on specific needs
- ⛔ **Not Recommended**: Significant overlap or not relevant
