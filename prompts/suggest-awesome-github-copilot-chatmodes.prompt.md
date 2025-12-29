---
mode: 'agent'
description: 'Suggest relevant GitHub Copilot Custom Chat Modes files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing custom chat modes in this repository.'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---

# Suggest Awesome GitHub Copilot Custom Chat Modes

Analyze current repository context and suggest relevant Custom Chat Modes files from the [GitHub awesome-copilot repository](https://github.com/github/awesome-copilot/blob/main/docs/README.chatmodes.md) that are not already available in this repository. Custom Chat Mode files are located in the [chatmodes](https://github.com/github/awesome-copilot/tree/main/chatmodes) folder of the awesome-copilot repository.

## Process

1. **Fetch Available Custom Chat Modes**: Extract Custom Chat Modes list and descriptions from [awesome-copilot README.chatmodes.md](https://github.com/github/awesome-copilot/blob/main/docs/README.chatmodes.md). Must use `#fetch` tool.
2. **Scan Local Custom Chat Modes**: Discover existing custom chat mode files in `.github/chatmodes/` folder
3. **Extract Descriptions**: Read front matter from local custom chat mode files to get descriptions
4. **Analyze Context**: Review chat history, repository files, and current project needs
5. **Compare Existing**: Check against custom chat modes already available in this repository
6. **Match Relevance**: Compare available custom chat modes against identified patterns and requirements
7. **Present Options**: Display relevant custom chat modes with descriptions, rationale, and availability status
8. **Validate**: Ensure suggested chatmodes would add value not already covered by existing chatmodes
9. **Output**: Provide structured table with suggestions, descriptions, and links to both awesome-copilot custom chat modes and similar local custom chat modes
   **AWAIT** user request to proceed with installation of specific custom chat modes. DO NOT INSTALL UNLESS DIRECTED TO DO SO.
10. **Download Assets**: For requested chat modes, automatically download and install individual chat modes to `.github/chatmodes/` folder. Do NOT adjust content of the files. Use `#todos` tool to track progress. Prioritize use of `#fetch` tool to download assets, but may use `curl` using `#runInTerminal` tool to ensure all content is retrieved.

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
- **Total Chat Modes Analyzed**: X chat modes from awesome-copilot
- **Already Installed**: X chat modes (X%)
- **Recommended**: X high-value additions
- **Optional**: X nice-to-have chat modes
- **Not Recommended**: X (overlap or low relevance)

### 📊 Recommendations by Priority & Role Category

Display suggestions grouped by priority and persona/role with enhanced visual hierarchy:

#### 🔥 High Priority (Critical Roles)

| Priority | Chat Mode | Role | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-----------|------|-------------|-------------------|--------|-------------------|-------------------|
| 🔥🔥🔥 | [security-expert](https://github.com/github/awesome-copilot/blob/main/chatmodes/security-expert.chatmode.md) | 🔒 Security | Security vulnerability analysis | ⭐ 485 stars · 📈 Trending · 🎓 Course featured | ❌ Missing | None | Critical gap: No dedicated security persona for vulnerability analysis |
| 🔥🔥 | [code-reviewer](https://github.com/github/awesome-copilot/blob/main/chatmodes/code-reviewer.chatmode.md) | 👁️ Review | Comprehensive code review | ⭐ 410 stars · 🔥 Popular · ✅ Well-maintained | ❌ Missing | gilfoyle.chatmode.md (partial) | High value: Dedicated review mode vs. general-purpose |

#### ⚡ Medium Priority (Enhanced Capabilities)

| Priority | Chat Mode | Role | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-----------|------|-------------|-------------------|--------|-------------------|-------------------|
| ⚡⚡ | [performance-optimizer](https://github.com/github/awesome-copilot/blob/main/chatmodes/perf-opt.chatmode.md) | ⚡ Performance | Performance analysis & optimization | ⭐ 305 stars · 📚 Well-documented | ⚠️ Partial | Multiple specialized modes | Enhancement: Unified performance optimization approach |

#### 💡 Optional (Nice to Have)

| Priority | Chat Mode | Role | Description | Quality Indicators | Status | Local Alternative | Value Proposition |
|----------|-----------|------|-------------|-------------------|--------|-------------------|-------------------|
| 💡 | [architect](https://github.com/github/awesome-copilot/blob/main/chatmodes/architect.chatmode.md) | 🏗️ Architecture | Software architecture guidance | ⭐ 280 stars · 📖 Stable | ✅ Covered | azure-principal-architect.chatmode.md, api-architect.chatmode.md | Already well-covered by 2 existing architect modes |

### 🎭 Role Category Breakdown

Display available chat modes grouped by role/persona:

#### 🏗️ Architecture & Design
- ✅ **Azure Architect**: Principal level (azure-principal-architect.chatmode.md)
- ✅ **API Architect**: Specialized (api-architect.chatmode.md)
- ✅ **SaaS Architect**: Azure focus (azure-saas-architect.chatmode.md)
- ❌ **General Architect**: Missing (recommended for non-Azure projects)
- ❌ **Microservices Architect**: Missing

#### 👨‍💻 Development Specialists
- ✅ **C#/.NET**: Expert engineer (expert-dotnet-software-engineer.chatmode.md)
- ✅ **React**: Frontend specialist (expert-react-frontend-engineer.chatmode.md)
- ✅ **C++**: Expert engineer (expert-cpp-software-engineer.chatmode.md)
- ⚠️ **Python**: Needs dedicated mode
- ❌ **Java Spring**: Missing

#### 🔒 Security & Quality
- ❌ **Security Expert**: Missing (critical gap)
- ⚠️ **Code Reviewer**: Partial via gilfoyle.chatmode.md
- ✅ **Accessibility**: Complete (accessibility.chatmode.md)
- ❌ **Compliance Auditor**: Missing

#### 🗄️ Data & Infrastructure
- ✅ **MS SQL DBA**: Complete (ms-sql-dba.chatmode.md)
- ✅ **PostgreSQL DBA**: Complete (postgresql-dba.chatmode.md)
- ✅ **Power BI Expert**: Multiple modes (4 specialized)
- ❌ **MongoDB DBA**: Missing
- ❌ **Redis Expert**: Missing

#### 🎨 Frontend & Design
- ✅ **React Expert**: Complete
- ✅ **AEM Frontend**: Specialized (aem-frontend-specialist.chatmode.md)
- ❌ **Vue.js Expert**: Missing
- ❌ **UX Designer**: Missing

#### 📋 Planning & Management
- ✅ **Planner**: Multiple modes (planner.chatmode.md, task-planner.chatmode.md)
- ✅ **PRD Writer**: Complete (prd.chatmode.md)
- ✅ **Implementation Plan**: Complete (implementation-plan.chatmode.md)
- ❌ **Agile Coach**: Missing
- ⚠️ **Tech Lead**: Needs dedicated mode

### 📈 Quality Indicators Legend

- ⭐ **Stars**: GitHub stars (popularity metric)
- 📈 **Trending**: Recently gaining traction (>25% growth in 30 days)
- 🔥 **Popular**: High usage/adoption (top 20%)
- 💬 **Discussions**: Active community (>75 discussions)
- ✅ **Well-maintained**: Updated within last 45 days
- 📚 **Well-documented**: Comprehensive examples and usage guides
- 🎓 **Course Featured**: Mentioned in official GitHub courses
- 👥 **Team Recommended**: Endorsed by GitHub teams or verified contributors
- 🎯 **Specialized**: Highly focused expertise area

## Local Chatmodes Discovery Process

1. List all `*.chatmode.md` files in `.github/chatmodes/` directory
2. For each discovered file, read front matter to extract `description`
3. Build comprehensive inventory of existing chatmodes
4. Use this inventory to avoid suggesting duplicates

## Quality Metrics Analysis

When analyzing chat modes from awesome-copilot, gather and display these quality indicators:

1. **Popularity Metrics**:
   - GitHub stars on the awesome-copilot repository
   - Number of forks and watchers
   - Community discussion activity
   - Usage patterns and adoption rates

2. **Quality Signals**:
   - Last updated date (freshness indicator)
   - Maintenance frequency (commit history)
   - Documentation completeness (examples, usage guides, model recommendations)
   - Number of contributors
   - Issue resolution rate
   - User testimonials and feedback

3. **Adoption Indicators**:
   - Mentioned in GitHub courses/documentation
   - Featured in GitHub blog posts or newsletters
   - Trending status (recent star growth >25% in 30 days)
   - External references and citations
   - Community endorsements and success stories

4. **Relevance Scoring**:
   - Role/persona match (0-100%)
   - Specialized expertise alignment
   - Gap analysis score (how much value it adds)
   - Team need alignment (based on chat history and project type)
   - Workflow integration potential

5. **Role Category Analysis**:
   - Group by role/persona (Architecture, Development, Security, Data, etc.)
   - Identify coverage gaps by category
   - Show distribution of existing vs. recommended chat modes
   - Highlight missing critical roles

## Requirements

- Use `githubRepo` tool to get content and metadata from awesome-copilot repository chatmodes folder
- Gather popularity and quality metrics from GitHub API (with fallback to cached/estimated values if API unavailable)
- Scan local file system for existing chatmodes in `.github/chatmodes/` directory
- Read YAML front matter from local chatmode files to extract descriptions
- Compare against existing chatmodes in this repository to avoid duplicates
- **PRIORITIZE** chat modes with highest quality indicators and relevance scores
- **CATEGORIZE** by role/persona type for better organization
- Focus on gaps in current chatmode library coverage
- Validate that suggested chatmodes align with repository's purpose and standards
- Provide clear, data-driven rationale for each suggestion with metrics
- Include links to both awesome-copilot chatmodes and similar local chatmodes
- Group recommendations by priority (High/Medium/Optional) AND role category
- Use visual hierarchy with emojis, badges, and formatting for scannability
- Provide executive summary with key statistics
- Include role category breakdown showing coverage gaps
- Highlight critical missing roles (especially security, compliance, testing)
- Don't provide any additional information or context beyond the structured output

## Icons & Status Reference

### Status Indicators
- ✅ **Covered**: Already installed or well-covered by existing chat modes
- ❌ **Missing**: Not available in repository, recommended for installation
- ⚠️ **Similar**: Partial coverage, enhancement opportunity
- 🔄 **Update**: Newer version available

### Priority Levels
- 🔥🔥🔥 **Critical**: Must-have role, immediate installation recommended
- 🔥🔥 **High**: Strong recommendation, high value-add
- ⚡⚡ **Medium**: Quality improvement opportunity
- 💡 **Optional**: Nice-to-have, consider based on specific needs
- ⛔ **Not Recommended**: Significant overlap or not relevant

### Role Category Icons
- 🏗️ **Architecture & Design**
- 👨‍💻 **Development Specialists**
- 🔒 **Security & Quality**
- 🗄️ **Data & Infrastructure**
- 🎨 **Frontend & Design**
- 📋 **Planning & Management**
- 🧪 **Testing & QA**
- ⚡ **Performance & Optimization**
- 🔧 **DevOps & Operations**
- 📚 **Documentation & Training**
