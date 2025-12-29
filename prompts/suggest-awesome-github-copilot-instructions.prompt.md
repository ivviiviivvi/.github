---
mode: 'agent'
description: 'Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing instructions in this repository.'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---
# Suggest Awesome GitHub Copilot Instructions

Analyze current repository context and suggest relevant copilot-instruction files from the [GitHub awesome-copilot repository](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md) that are not already available in this repository.

## Process

1. **Fetch Available Instructions**: Extract instruction list and descriptions from [awesome-copilot README.instructions.md](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md). Must use `#fetch` tool.
2. **Scan Local Instructions**: Discover existing instruction files in `.github/instructions/` folder
3. **Extract Descriptions**: Read front matter from local instruction files to get descriptions and `applyTo` patterns
4. **Analyze Context**: Review chat history, repository files, and current project needs
5. **Compare Existing**: Check against instructions already available in this repository
6. **Match Relevance**: Compare available instructions against identified patterns and requirements
7. **Present Options**: Display relevant instructions with descriptions, rationale, and availability status
8. **Validate**: Ensure suggested instructions would add value not already covered by existing instructions
9. **Output**: Provide structured table with suggestions, descriptions, and links to both awesome-copilot instructions and similar local instructions
   **AWAIT** user request to proceed with installation of specific instructions. DO NOT INSTALL UNLESS DIRECTED TO DO SO.
10. **Download Assets**: For requested instructions, automatically download and install individual instructions to `.github/instructions/` folder. Do NOT adjust content of the files.  Use `#todos` tool to track progress. Prioritize use of `#fetch` tool to download assets, but may use `curl` using `#runInTerminal` tool to ensure all content is retrieved.

## Context Analysis Criteria

🔍 **Repository Patterns**:
- Programming languages used (.cs, .js, .py, .ts, etc.)
- Framework indicators (ASP.NET, React, Azure, Next.js, etc.)
- Project types (web apps, APIs, libraries, tools)
- Development workflow requirements (testing, CI/CD, deployment)

🗨️ **Chat History Context**:
- Recent discussions and pain points
- Technology-specific questions
- Coding standards discussions
- Development workflow requirements

## Output Format

### 🎯 Executive Summary

Provide a quick overview of the analysis:
- **Total Instructions Analyzed**: X instructions from awesome-copilot
- **Already Installed**: X instructions (X%)
- **Recommended**: X high-value additions
- **Optional**: X nice-to-have instructions
- **Not Recommended**: X (overlap or low relevance)

### 📊 Recommendations by Priority & Category

Display suggestions grouped by priority and technology category with enhanced visual hierarchy:

#### 🔥 High Priority (Critical Gaps)

| Priority | Instruction | Technology | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-------------|------------|-------------|-------------------|--------|-------------------|-------------------|
| 🔥🔥🔥 | [rust](https://github.com/github/awesome-copilot/blob/main/instructions/rust.instructions.md) | 🦀 Rust | Rust best practices | ⭐ 520 stars · 📈 Trending · 🎓 Course featured | ❌ Missing | rust.instructions.md exists | Critical: Repository has Rust code but needs better guidelines |
| 🔥🔥 | [kubernetes](https://github.com/github/awesome-copilot/blob/main/instructions/kubernetes.md) | ☸️ K8s | K8s deployment patterns | ⭐ 380 stars · 🔥 Popular · ✅ Well-maintained | ⚠️ Partial | kubernetes-deployment-best-practices.instructions.md | Enhancement: More comprehensive than existing |

#### ⚡ Medium Priority (Enhancements)

| Priority | Instruction | Technology | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-------------|------------|-------------|-------------------|--------|-------------------|-------------------|
| ⚡⚡ | [reactjs-advanced](https://github.com/github/awesome-copilot/blob/main/instructions/react-advanced.md) | ⚛️ React | Advanced React patterns | ⭐ 295 stars · 📚 Well-documented | ⚠️ Similar | reactjs.instructions.md | Adds advanced hooks and performance optimization patterns |

#### 💡 Optional (Nice to Have)

| Priority | Instruction | Technology | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-------------|------------|-------------|-------------------|--------|-------------------|-------------------|
| 💡 | [csharp](https://github.com/github/awesome-copilot/blob/main/instructions/csharp.md) | 🎯 C# | C# best practices | ⭐ 210 stars · 📖 Stable | ✅ Covered | csharp.instructions.md, csharp-ja.instructions.md, csharp-ko.instructions.md | Already well-covered by 3 existing instructions |

### 📂 Technology Category Breakdown

Display available instructions grouped by technology:

#### 🎯 Languages
- ✅ **C#**: 3 variants (English, Japanese, Korean)
- ❌ **Rust**: Missing (recommended)
- ⚠️ **Python**: Partial coverage
- ✅ **Java**: Complete
- ❌ **Elixir**: Missing

#### ☁️ Cloud & Infrastructure
- ✅ **Azure**: Extensive (7 instructions)
- ❌ **AWS**: Missing (recommended if AWS usage detected)
- ⚠️ **Terraform**: Basic coverage
- ❌ **Kubernetes**: Missing (recommended)

#### 🎨 Frontend
- ✅ **React**: Basic
- ⚠️ **Angular**: Needs enhancement
- ✅ **Vue.js**: Complete
- ❌ **Svelte**: Missing

### 📈 Quality Indicators Legend

- ⭐ **Stars**: GitHub stars (popularity metric)
- 📈 **Trending**: Recently gaining traction (>20% growth in 30 days)
- 🔥 **Popular**: High usage/adoption (top 25%)
- 💬 **Discussions**: Active community (>50 discussions)
- ✅ **Well-maintained**: Updated within last 60 days
- 📚 **Well-documented**: Comprehensive examples and usage guides
- 🎓 **Course Featured**: Mentioned in official GitHub courses
- 👥 **Team Recommended**: Endorsed by GitHub teams or verified contributors

## Local Instructions Discovery Process

1. List all `*.instructions.md` files in the `instructions/` directory
2. For each discovered file, read front matter to extract `description` and `applyTo` patterns
3. Build comprehensive inventory of existing instructions with their applicable file patterns
4. Use this inventory to avoid suggesting duplicates

## File Structure Requirements

Based on GitHub documentation, copilot-instructions files should be:
- **Repository-wide instructions**: `.github/copilot-instructions.md` (applies to entire repository)
- **Path-specific instructions**: `.github/instructions/NAME.instructions.md` (applies to specific file patterns via `applyTo` frontmatter)
- **Community instructions**: `instructions/NAME.instructions.md` (for sharing and distribution)

## Front Matter Structure

Instructions files in awesome-copilot use this front matter format:
```markdown
---
description: 'Brief description of what this instruction provides'
applyTo: '**/*.js,**/*.ts' # Optional: glob patterns for file matching
---
```

## Quality Metrics Analysis

When analyzing instructions from awesome-copilot, gather and display these quality indicators:

1. **Popularity Metrics**:
   - GitHub stars on the awesome-copilot repository
   - Number of forks and watchers
   - Community discussion activity
   - Download/usage statistics

2. **Quality Signals**:
   - Last updated date (freshness indicator)
   - Maintenance frequency (commit history)
   - Documentation completeness (examples, usage guides)
   - Number of contributors
   - Issue resolution rate
   - Test coverage (if applicable)

3. **Adoption Indicators**:
   - Mentioned in GitHub courses/documentation
   - Featured in GitHub blog posts or newsletters
   - Trending status (recent star growth >20% in 30 days)
   - External references and citations
   - Community endorsements

4. **Relevance Scoring**:
   - Technology stack match (0-100%)
   - Code pattern detection in repository
   - Gap analysis score (how much value it adds)
   - Team need alignment (based on chat history and file patterns)

5. **Category Analysis**:
   - Group by technology (Languages, Cloud, Frontend, Backend, etc.)
   - Identify coverage gaps by category
   - Show distribution of existing vs. recommended instructions

## Requirements

- Use `githubRepo` tool to get content and metadata from awesome-copilot repository
- Gather popularity and quality metrics from GitHub API (with fallback to cached/estimated values if API unavailable)
- Scan local file system for existing instructions in `instructions/` directory
- Read YAML front matter from local instruction files to extract descriptions and `applyTo` patterns
- Compare against existing instructions in this repository to avoid duplicates
- **PRIORITIZE** instructions with highest quality indicators and relevance scores
- **CATEGORIZE** by technology area for better organization
- Focus on gaps in current instruction library coverage
- Validate that suggested instructions align with repository's purpose and standards
- Provide clear, data-driven rationale for each suggestion with metrics
- Include links to both awesome-copilot instructions and similar local instructions
- Group recommendations by priority (High/Medium/Optional) AND category
- Use visual hierarchy with emojis, badges, and formatting for scannability
- Provide executive summary with key statistics
- Include technology category breakdown showing coverage gaps
- Consider technology stack compatibility and project-specific needs
- Don't provide any additional information or context beyond the structured output

## Icons & Status Reference

### Status Indicators
- ✅ **Covered**: Already installed or well-covered by existing instructions
- ❌ **Missing**: Not available in repository, recommended for installation
- ⚠️ **Similar**: Partial coverage, enhancement opportunity
- 🔄 **Update**: Newer version available

### Priority Levels
- 🔥🔥🔥 **Critical**: Must-have, immediate installation recommended
- 🔥🔥 **High**: Strong recommendation, high value-add
- ⚡⚡ **Medium**: Quality improvement opportunity
- 💡 **Optional**: Nice-to-have, consider based on specific needs
- ⛔ **Not Recommended**: Significant overlap or not relevant

### Technology Icons
- 🎯 **C#/.NET**
- ⚛️ **React**
- 🅰️ **Angular**
- 🟢 **Vue.js**
- 🐍 **Python**
- ☕ **Java**
- 🦀 **Rust**
- 🔷 **Go**
- ☸️ **Kubernetes**
- ☁️ **Cloud (AWS/Azure/GCP)**
- 🐳 **Docker**
- 🔧 **DevOps**
