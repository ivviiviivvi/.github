---
agent: "agent"
description: "Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing custom agents in this repository."
tools: ["edit", "search", "runCommands", "runTasks", "changes", "testFailure", "openSimpleBrowser", "fetch", "githubRepo", "todos"]
---

# Suggest Awesome GitHub Copilot Custom Agents

Analyze current repository context and suggest relevant Custom Agents files from the [GitHub awesome-copilot repository](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md) that are not already available in this repository. Custom Agent files are located in the [agents](https://github.com/github/awesome-copilot/tree/main/agents) folder of the awesome-copilot repository.

## Process

1. **Fetch Available Custom Agents**: Extract Custom Agents list and descriptions from [awesome-copilot README.agents.md](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md). Must use `fetch` tool.
2. **Scan Local Custom Agents**: Discover existing custom agent files in `.github/agents/` folder
3. **Extract Descriptions**: Read front matter from local custom agent files to get descriptions
4. **Analyze Context**: Review chat history, repository files, and current project needs
5. **Compare Existing**: Check against custom agents already available in this repository
6. **Match Relevance**: Compare available custom agents against identified patterns and requirements
7. **Present Options**: Display relevant custom agents with descriptions, rationale, and availability status
8. **Validate**: Ensure suggested agents would add value not already covered by existing agents
9. **Output**: Provide structured table with suggestions, descriptions, and links to both awesome-copilot custom agents and similar local custom agents
   **AWAIT** user request to proceed with installation of specific custom agents. DO NOT INSTALL UNLESS DIRECTED TO DO SO.
10. **Download Assets**: For requested agents, automatically download and install individual agents to `.github/agents/` folder. Do NOT adjust content of the files. Use `#todos` tool to track progress. Prioritize use of `#fetch` tool to download assets, but may use `curl` using `#runInTerminal` tool to ensure all content is retrieved.

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

Display analysis results in structured table comparing awesome-copilot custom agents with existing repository custom agents:

| Awesome-Copilot Custom Agent                                                                                                                            | Description                                                                                                                                                                | Already Installed | Similar Local Custom Agent         | Suggestion Rationale                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------- | ------------------------------------------------------------- |
| [amplitude-experiment-implementation.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/amplitude-experiment-implementation.agent.md) | This custom agent uses Amplitude's MCP tools to deploy new experiments inside of Amplitude, enabling seamless variant testing capabilities and rollout of product features | ❌ No             | None                               | Would enhance experimentation capabilities within the product |
| [launchdarkly-flag-cleanup.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/launchdarkly-flag-cleanup.agent.md)                     | Feature flag cleanup agent for LaunchDarkly                                                                                                                                | ✅ Yes            | launchdarkly-flag-cleanup.agent.md | Already covered by existing LaunchDarkly custom agents        |

## Local Agent Discovery Process

1. List all `*.agent.md` files in `.github/agents/` directory
2. For each discovered file, read front matter to extract `description`
3. Build comprehensive inventory of existing agents
4. Use this inventory to avoid suggesting duplicates

## Quality Metrics Analysis

When analyzing custom agents from awesome-copilot, gather and display these quality indicators:

1. **Popularity Metrics**:
   - GitHub stars on the awesome-copilot repository
   - Number of forks and watchers
   - Community discussion activity
   - Integration adoption rates
   - Partner endorsements

2. **Quality Signals**:
   - Last updated date (freshness indicator)
   - Maintenance frequency (commit history)
   - Documentation completeness (setup guides, examples, troubleshooting)
   - Number of contributors
   - Issue resolution rate
   - MCP server compatibility
   - Enterprise readiness indicators

3. **Adoption Indicators**:
   - Mentioned in GitHub courses/documentation
   - Featured in GitHub blog posts or partner announcements
   - Trending status (recent star growth >30% in 30 days)
   - External references and case studies
   - Community endorsements and success stories
   - Official partner status

4. **Integration Value**:
   - Integration complexity (low/medium/high)
   - Prerequisites and dependencies
   - Setup time estimate
   - Maintenance effort
   - ROI potential

5. **Relevance Scoring**:
   - Tool stack match (0-100%)
   - Integration need alignment
   - Gap analysis score (how much value it adds)
   - Team workflow fit (based on chat history and project needs)
   - Complementary vs. duplicate capability

6. **Category Analysis**:
   - Group by integration type (Incident, Security, Infrastructure, etc.)
   - Identify coverage gaps by category
   - Show distribution of existing vs. recommended agents
   - Highlight missing critical integrations

## Requirements

- Use `githubRepo` tool to get content and metadata from awesome-copilot repository agents folder
- Gather popularity and quality metrics from GitHub API (with fallback to cached/estimated values if API unavailable)
- Scan local file system for existing agents in `.github/agents/` directory
- Read YAML front matter from local agent files to extract descriptions
- Compare against existing agents in this repository to avoid duplicates
- **PRIORITIZE** agents with highest quality indicators, MCP integration, and relevance scores
- **CATEGORIZE** by integration type for better organization
- Focus on gaps in current agent library coverage
- Validate that suggested agents align with repository's tool stack and needs
- Provide clear, data-driven rationale for each suggestion with metrics
- Include links to both awesome-copilot agents and similar local agents
- Group recommendations by priority (High/Medium/Optional) AND integration category
- Use visual hierarchy with emojis, badges, and formatting for scannability
- Provide executive summary with key statistics
- Include integration category breakdown showing coverage gaps
- Highlight missing critical integrations (especially monitoring, security, CI/CD)
- Show setup complexity and prerequisites for each agent
- Don't provide any additional information or context beyond the structured output

## Icons & Status Reference

### Status Indicators
- ✅ **Covered**: Already installed or well-covered by existing agents
- ❌ **Missing**: Not available in repository, recommended for installation
- ⚠️ **Similar**: Partial coverage, enhancement opportunity
- 🔄 **Update**: Newer version available
- 🔧 **Needs Config**: Installed but requires configuration

### Priority Levels
- 🔥🔥🔥 **Critical**: Must-have integration, immediate installation recommended
- 🔥🔥 **High**: Strong recommendation, high value-add
- ⚡⚡ **Medium**: Quality improvement opportunity
- 💡 **Optional**: Nice-to-have, consider based on specific tool usage
- ⛔ **Not Recommended**: Tool not in use or significant overlap

### Integration Category Icons
- 🚨 **Incident Management & Monitoring**
- 🔒 **Security & Compliance**
- 🏗️ **Infrastructure & Cloud**
- 🧪 **Feature Management & Experimentation**
- 🔧 **Development & Automation**
- 🗄️ **Data Management**
- 📋 **Productivity & Workflow**
- 🔌 **API & Integration**
- 📊 **Analytics & Observability**
- 🎯 **Quality & Testing**
