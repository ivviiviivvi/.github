---
mode: 'agent'
description: 'Suggest relevant GitHub Copilot collections from the awesome-copilot repository based on current repository context and chat history, providing automatic download and installation of collection assets.'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'think', 'changes', 'testFailure', 'openSimpleBrowser', 'fetch', 'githubRepo', 'todos', 'search']
---
# Suggest Awesome GitHub Copilot Collections

Analyze current repository context and suggest relevant collections from the [GitHub awesome-copilot repository](https://github.com/github/awesome-copilot/blob/main/docs/README.collections.md) that would enhance the development workflow for this repository.

## Process

1. **Fetch Available Collections**: Extract collection list and descriptions from [awesome-copilot README.collections.md](https://github.com/github/awesome-copilot/blob/main/docs/README.collections.md). Must use `#fetch` tool.
2. **Scan Local Assets**: Discover existing prompt files in `prompts/`, instruction files in `instructions/`, and chat modes in `chatmodes/` folders
3. **Extract Local Descriptions**: Read front matter from local asset files to understand existing capabilities
4. **Analyze Repository Context**: Review chat history, repository files, programming languages, frameworks, and current project needs
5. **Match Collection Relevance**: Compare available collections against identified patterns and requirements
6. **Check Asset Overlap**: For relevant collections, analyze individual items to avoid duplicates with existing repository assets
7. **Present Collection Options**: Display relevant collections with descriptions, item counts, and rationale for suggestion
8. **Provide Usage Guidance**: Explain how the installed collection enhances the development workflow
   **AWAIT** user request to proceed with installation of specific collections. DO NOT INSTALL UNLESS DIRECTED TO DO SO.
9. **Download Assets**: For requested collections, automatically download and install each individual asset (prompts, instructions, chat modes) to appropriate directories. Do NOT adjust content of the files. Prioritize use of `#fetch` tool to download assets, but may use `curl` using `#runInTerminal` tool to ensure all content is retrieved.

## Context Analysis Criteria

🔍 **Repository Patterns**:
- Programming languages used (.cs, .js, .py, .ts, .bicep, .tf, etc.)
- Framework indicators (ASP.NET, React, Azure, Next.js, Angular, etc.)
- Project types (web apps, APIs, libraries, tools, infrastructure)
- Documentation needs (README, specs, ADRs, architectural decisions)
- Development workflow indicators (CI/CD, testing, deployment)

🗨️ **Chat History Context**:
- Recent discussions and pain points
- Feature requests or implementation needs
- Code review patterns and quality concerns
- Development workflow requirements and challenges
- Technology stack and architecture decisions

## Output Format

### 🎯 Executive Summary

Provide a quick overview of the analysis:
- **Total Collections Analyzed**: X collections from awesome-copilot
- **Recommended**: X high-value collections
- **Total Assets in Recommendations**: X items (prompts, instructions, chat modes, agents)
- **Already Covered**: X assets (X%)
- **New Assets**: X unique additions
- **Estimated Setup Time**: X hours

### 📊 Collection Recommendations by Priority

Display collections grouped by priority with detailed breakdowns:

#### 🔥 High Priority Collections (Critical Value-Add)

| Priority | Collection | Theme | Total Assets | New Assets | Quality Indicators | Value Proposition |
|----------|------------|-------|--------------|------------|-------------------|-------------------|
| 🔥🔥🔥 | [Security & Compliance Suite](https://github.com/github/awesome-copilot/blob/main/collections/security.md) | 🔒 Security | 18 items | 14 new (78%) | ⭐ 520 stars · 📈 Trending · 🎓 Featured | Critical gap: Comprehensive security coverage from threat modeling to compliance |
| 🔥🔥 | [Testing Excellence Pack](https://github.com/github/awesome-copilot/blob/main/collections/testing.md) | 🧪 Testing | 15 items | 11 new (73%) | ⭐ 410 stars · 🔥 Popular · ✅ Maintained | High impact: TDD workflows, test automation, coverage analysis |

#### ⚡ Medium Priority Collections (Enhancements)

| Priority | Collection | Theme | Total Assets | New Assets | Quality Indicators | Value Proposition |
|----------|------------|-------|--------------|------------|-------------------|-------------------|
| ⚡⚡ | [Azure Cloud Development](https://github.com/github/awesome-copilot/blob/main/collections/azure-cloud.md) | ☁️ Azure | 15 items | 9 new (60%) | ⭐ 385 stars · 📚 Well-documented | Enhancement: Advanced Azure patterns, cost optimization, AVM modules |
| ⚡ | [Performance Optimization](https://github.com/github/awesome-copilot/blob/main/collections/performance.md) | ⚡ Performance | 12 items | 7 new (58%) | ⭐ 295 stars · 📖 Stable | Quality boost: Database tuning, code profiling, caching strategies |

#### 💡 Optional Collections (Nice to Have)

| Priority | Collection | Theme | Total Assets | New Assets | Quality Indicators | Value Proposition |
|----------|------------|-------|--------------|------------|-------------------|-------------------|
| 💡 | [C# .NET Development](https://github.com/github/awesome-copilot/blob/main/collections/csharp-dotnet.md) | 🎯 C#/.NET | 12 items | 3 new (25%) | ⭐ 245 stars · 📖 Stable | Incremental: Some advanced patterns not in existing 15+ C# assets |

### 📦 Detailed Asset Breakdown

For each recommended collection, show what's inside:

#### 🔥🔥🔥 Security & Compliance Suite (18 items, 14 new)

**Assets by Type:**
- 🎯 **Prompts** (6): Threat modeling, security review, vulnerability scanning, OWASP compliance, penetration test planning, security documentation
- 📋 **Instructions** (8): Secure coding (Python, Java, C#, JavaScript), SQL injection prevention, XSS mitigation, authentication best practices, secrets management
- 🎭 **Chat Modes** (3): Security expert, compliance auditor, penetration tester
- 🤖 **Agents** (1): Automated security scanner integration

**Quality Metrics:**
- ⭐ 520 stars · 📈 +35% in 30 days · 💬 125 discussions
- ✅ Updated 2 weeks ago · 🎓 Featured in GitHub Security course
- 👥 Endorsed by GitHub Security team

**Coverage Analysis:**
- ✅ **Already Have** (4 assets, 22%): General security instructions, StackHawk agent, JFrog security agent, security audit agent
- ❌ **Missing** (14 assets, 78%): Threat modeling, OWASP compliance, secure coding per language, penetration testing, compliance auditor mode
- 🎯 **High Value**: Fills critical gap in proactive security practices

**Installation Impact:**
- 📁 Will add to `prompts/`: 6 security-focused prompts
- 📁 Will add to `instructions/`: 8 language-specific secure coding guides
- 📁 Will add to `chatmodes/`: 3 specialized security personas
- 📁 Will add to `agents/`: 1 automated scanner integration
- ⏱️ **Setup Time**: ~2 hours (includes configuration and testing)
- 💰 **ROI**: High - reduces security vulnerabilities by ~60% based on case studies

### 🗂️ Collection Category Analysis

Group collections by theme to show coverage:

#### 🔒 Security & Quality
- 🔥🔥🔥 **Security & Compliance**: 14 new assets (recommended)
- ✅ **Code Review**: Well-covered by existing assets
- ❌ **Accessibility**: Missing (3 collections available)

#### 🧪 Development Practices
- 🔥🔥 **Testing Excellence**: 11 new assets (recommended)
- ⚡ **Performance Optimization**: 7 new assets (nice to have)
- ✅ **Refactoring**: Covered

#### ☁️ Cloud & Infrastructure
- ⚡⚡ **Azure Cloud Development**: 9 new assets (recommended)
- ❌ **AWS Development**: Missing (18 assets available)
- ⚠️ **Kubernetes & Containers**: Partial (12 assets available, 8 new)

#### 🎨 Frontend Development
- ⚠️ **React Ecosystem**: Partial (8 assets available, 4 new)
- ❌ **Vue.js Complete**: Missing (10 assets available)
- ✅ **Angular**: Well-covered

#### 🗄️ Backend & Data
- ⚠️ **API Development**: Partial (14 assets available, 6 new)
- ❌ **Microservices**: Missing (16 assets available)
- ⚠️ **Database Optimization**: Partial (9 assets available, 5 new)

### 📈 Quality Indicators Legend

- ⭐ **Stars**: GitHub stars (popularity metric)
- 📈 **Trending**: Recent growth >25% in 30 days
- 🔥 **Popular**: Top 20% of collections
- 💬 **Discussions**: Active community (>100 discussions)
- ✅ **Maintained**: Updated within 45 days
- 📚 **Well-documented**: Setup guides, examples, integration docs
- 🎓 **Featured**: Official GitHub courses/docs
- 👥 **Endorsed**: GitHub teams or verified partners
- 🏢 **Enterprise**: Production-tested at scale

### 🎯 Priority Decision Matrix

**Install Now (🔥🔥🔥):**
- >70% new assets
- Fills critical capability gap
- High quality indicators (>300 stars for collections, trending)
- Immediate value proposition

**Install Soon (🔥🔥 / ⚡⚡):**
- 50-70% new assets
- Enhances existing capabilities
- Good quality indicators (>250 stars for collections)
- Clear improvement potential

**Consider Later (⚡ / 💡):**
- 25-50% new assets
- Incremental improvements
- Moderate quality indicators
- Nice-to-have enhancements

**Skip (⛔):**
- <25% new assets
- Significant overlap with existing
- Low relevance to tech stack
- Outdated or poorly maintained

## Local Asset Discovery Process

1. **Scan Asset Directories**:
   - List all `*.prompt.md` files in `prompts/` directory
   - List all `*.instructions.md` files in `instructions/` directory
   - List all `*.chatmode.md` files in `chatmodes/` directory

2. **Extract Asset Metadata**: For each discovered file, read YAML front matter to extract:
   - `description` - Primary purpose and functionality
   - `tools` - Required tools and capabilities
   - `mode` - Operating mode (for prompts)
   - `model` - Specific model requirements (for chat modes)

3. **Build Asset Inventory**: Create comprehensive map of existing capabilities organized by:
   - **Technology Focus**: Programming languages, frameworks, platforms
   - **Workflow Type**: Development, testing, deployment, documentation, planning
   - **Specialization Level**: General purpose vs. specialized expert modes

4. **Identify Coverage Gaps**: Compare existing assets against:
   - Repository technology stack requirements
   - Development workflow needs indicated by chat history
   - Industry best practices for identified project types
   - Missing expertise areas (security, performance, architecture, etc.)

## Collection Asset Download Process

When user confirms a collection installation:

1. **Fetch Collection Manifest**: Get collection YAML from awesome-copilot repository
2. **Download Individual Assets**: For each item in collection:
   - Download raw file content from GitHub
   - Validate file format and front matter structure
   - Check naming convention compliance
3. **Install to Appropriate Directories**:
   - `*.prompt.md` files → `prompts/` directory
   - `*.instructions.md` files → `instructions/` directory
   - `*.chatmode.md` files → `chatmodes/` directory
4. **Avoid Duplicates**: Skip files that are substantially similar to existing assets
5. **Report Installation**: Provide summary of installed assets and usage instructions

## Quality Metrics Analysis

When analyzing collections from awesome-copilot, gather and display these quality indicators:

1. **Collection-Level Metrics**:
   - Total assets in collection
   - Asset type distribution (prompts/instructions/chatmodes/agents)
   - Thematic coherence score
   - Completeness rating (beginner to advanced coverage)
   - Last updated date for collection

2. **Aggregate Quality Signals**:
   - Average stars across collection assets
   - Maintenance frequency across all assets
   - Overall documentation quality
   - Number of contributors to collection
   - Issue resolution rate for collection assets

3. **Adoption Indicators**:
   - Featured in GitHub courses/documentation
   - Blog mentions and external references
   - Trending status (collection growth rate)
   - Community endorsements and case studies
   - Enterprise adoption signals

4. **Value Analysis**:
   - New assets percentage (vs. existing repository assets)
   - Gap filling score (0-100%)
   - Technology stack alignment
   - Workflow integration potential
   - ROI indicators (time savings, quality improvements)

5. **Asset Overlap Detection**:
   - Duplicate detection (exact matches)
   - Similarity analysis (partial overlaps)
   - Enhancement opportunities (better versions available)
   - Complementary assets (works well with existing)

6. **Category Coverage**:
   - Group collections by theme/category
   - Show coverage gaps by category
   - Identify synergies between collections
   - Highlight missing critical areas

## Requirements

- Use `fetch` tool to get collections data and metadata from awesome-copilot repository
- Gather popularity and quality metrics from GitHub API (with fallback to cached/estimated values if API unavailable)
- Use `githubRepo` tool to get individual asset content for analysis and download
- Scan local file system for existing assets in `prompts/`, `instructions/`, `chatmodes/`, and `agents/` directories
- Read YAML front matter from local asset files to extract descriptions and capabilities
- **ANALYZE** each collection's individual assets to determine new vs. existing
- **CALCULATE** overlap percentage and new asset count for each collection
- **PRIORITIZE** collections with >50% new assets and high quality indicators
- **CATEGORIZE** collections by theme for better organization
- Compare collections against repository context to identify relevant matches
- Focus on collections that fill capability gaps rather than duplicate existing assets
- Validate that suggested collections align with repository's technology stack and development needs
- Provide clear, data-driven rationale for each collection with specific benefits and ROI
- Group recommendations by priority (High/Medium/Optional) AND theme category
- Use visual hierarchy with emojis, badges, and formatting for scannability
- Provide executive summary with key statistics
- Include detailed asset breakdown for each recommended collection
- Show installation impact (where files go, setup time, expected benefits)
- Include category analysis showing coverage gaps
- Enable automatic download and installation of collection assets to appropriate directories
- Ensure downloaded assets follow repository naming conventions and formatting standards
- Provide usage guidance explaining how collections enhance the development workflow
- Include links to both awesome-copilot collections and individual assets within collections
- Don't provide any additional information or context beyond the structured output

## Icons & Status Reference

### Status Indicators
- ✅ **Covered**: Well-covered by existing assets
- ❌ **Missing**: Not available, recommended
- ⚠️ **Partial**: Some coverage, enhancement opportunity
- 🔄 **Update**: Newer versions available

### Priority Levels
- 🔥🔥🔥 **Critical**: >70% new assets, fills critical gap, install now
- 🔥🔥 **High**: 50-70% new assets, strong value-add, install soon
- ⚡⚡ **Medium**: 35-50% new assets, quality improvement
- ⚡ **Low-Medium**: 25-35% new assets, nice to have
- 💡 **Optional**: <25% new assets, consider based on needs
- ⛔ **Skip**: Significant overlap or low relevance

### Theme Category Icons
- 🔒 **Security & Quality**
- 🧪 **Development Practices**
- ☁️ **Cloud & Infrastructure**
- 🎨 **Frontend Development**
- 🗄️ **Backend & Data**
- 🔧 **DevOps & Automation**
- 📚 **Documentation & Learning**
- 🎯 **Language-Specific**
- 🌐 **Full-Stack**
- 🚀 **Productivity & Workflow**

## Collection Installation Workflow

1. **User Confirms Collection**: User selects specific collection(s) for installation
2. **Fetch Collection Manifest**: Download YAML manifest from awesome-copilot repository
3. **Asset Download Loop**: For each asset in collection:
   - Download raw content from GitHub repository
   - Validate file format and structure
   - Check for substantial overlap with existing local assets
   - Install to appropriate directory (`prompts/`, `instructions/`, or `chatmodes/`)
4. **Installation Summary**: Report installed assets with usage instructions
5. **Workflow Enhancement Guide**: Explain how the collection improves development capabilities

## Post-Installation Guidance

After installing a collection, provide:
- **Asset Overview**: List of installed prompts, instructions, and chat modes
- **Usage Examples**: How to activate and use each type of asset
- **Workflow Integration**: Best practices for incorporating assets into development process
- **Customization Tips**: How to modify assets for specific project needs
- **Related Collections**: Suggestions for complementary collections that work well together


## Icons Reference

- ✅ Collection recommended for installation
- ⚠️ Collection has some asset overlap but still valuable
- ❌ Collection not recommended (significant overlap or not relevant)
- 🎯 High-value collection that fills major capability gaps
- 📁 Collection partially installed (some assets skipped due to duplicates)
- 🔄 Collection needs customization for repository-specific needs
