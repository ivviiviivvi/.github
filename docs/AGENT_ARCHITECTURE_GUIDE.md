# 🤖 Agent Architecture Guide

> **Comprehensive guide to building, testing, and deploying agents following
> organizational patterns**

## Table of Contents

- [Overview](#overview)
- [Agent Architecture Patterns](#agent-architecture-patterns)
  - [BaseAgent Pattern](#baseagent-pattern)
  - [Skills System Pattern](#skills-system-pattern)
  - [Agent Orchestration Pattern](#agent-orchestration-pattern)
  - [TypeScript Agents Pattern](#typescript-agents-pattern)
- [Agent File Structure](#agent-file-structure)
- [Agent Frontmatter Format](#agent-frontmatter-format)
- [Agent Lifecycle](#agent-lifecycle)
- [GitHub Copilot Integration](#github-copilot-integration)
- [MCP Server Integration](#mcp-server-integration)
- [Best Practices](#best-practices)
- [Agent Examples](#agent-examples)
- [Workflow Diagrams](#workflow-diagrams)
- [Troubleshooting](#troubleshooting)

---

## Overview

Agents are specialized AI assistants that integrate with GitHub Copilot to
provide domain-specific expertise and automation capabilities. This guide
documents the architectural patterns discovered across the organization and
provides a comprehensive framework for building production-ready agents.

**Key Principles:**

- **Single Responsibility**: Each agent focuses on a specific domain or task
- **MCP Integration**: Leverage Model Context Protocol servers for enhanced
  capabilities
- **Declarative Configuration**: Use YAML frontmatter for agent metadata and
  configuration
- **Testability**: Design agents with clear inputs/outputs for automated testing
- **Documentation First**: Comprehensive documentation enables discoverability
  and adoption

---

## Agent Architecture Patterns

### BaseAgent Pattern

The BaseAgent pattern provides a foundational structure for agents with common
functionality.

**Characteristics:**

- Centralized configuration management
- Standardized error handling
- Built-in logging and telemetry
- Reusable utility methods

**Example Structure:**

```python
from typing import Dict, Any, Optional
import logging

class BaseAgent:
    """
    Base class for all agents providing common functionality.

    Attributes:
        name: Agent identifier
        description: Human-readable agent purpose
        config: Agent configuration dictionary
        logger: Logging instance
    """

    def __init__(self, name: str, description: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.description = description
        self.config = config or {}
        self.logger = logging.getLogger(f"agent.{name}")
        self._initialize()

    def _initialize(self) -> None:
        """Initialize agent-specific resources."""
        self.logger.info(f"Initializing agent: {self.name}")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic with provided context.

        Args:
            context: Execution context dictionary

        Returns:
            Result dictionary with status and data
        """
        try:
            self.logger.info(f"Executing {self.name}")
            result = self._execute_impl(context)
            return {"status": "success", "data": result}
        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _execute_impl(self, context: Dict[str, Any]) -> Any:
        """Override this method in subclasses."""
        raise NotImplementedError("Subclass must implement _execute_impl")
```

**Usage Example:**

```python
class TerraformAgent(BaseAgent):
    """Terraform infrastructure specialist agent."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            name="terraform",
            description="Terraform infrastructure specialist",
            config=config
        )

    def _execute_impl(self, context: Dict[str, Any]) -> Any:
        action = context.get("action", "plan")
        workspace = self.config.get("workspace")

        if action == "plan":
            return self._run_plan(workspace)
        elif action == "apply":
            return self._run_apply(workspace)
        else:
            raise ValueError(f"Unknown action: {action}")
```

---

### Skills System Pattern

The Skills System pattern organizes agent capabilities into discrete, reusable
skills.

**Characteristics:**

- Modular skill registration
- Dynamic skill discovery
- Skill composition and chaining
- Metadata-driven execution

**SKILL.md Frontmatter Format:**

```yaml
---
name: "code-review"
description: "Automated code review with security and quality checks"
license: "MIT"
version: "1.0.0"
author: "Organization Team"
tools:
  - read
  - search
  - edit
  - github/list_pull_requests
  - github/get_pull_request
mcp-servers:
  - github
  - codeql
dependencies:
  - python: ">=3.11"
parameters:
  pr_number:
    type: "integer"
    required: true
    description: "Pull request number to review"
  focus_areas:
    type: "array"
    required: false
    default: ["security", "performance", "maintainability"]
---
```

**Skill Implementation:**

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class SkillMetadata:
    """Metadata for a skill."""
    name: str
    description: str
    version: str
    tools: List[str]
    parameters: Dict[str, Any]

class Skill:
    """Base class for agent skills."""

    def __init__(self, metadata: SkillMetadata):
        self.metadata = metadata
        self.name = metadata.name

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill with provided parameters."""
        raise NotImplementedError

class SkillRegistry:
    """Registry for managing available skills."""

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """Register a new skill."""
        self._skills[skill.name] = skill

    def get_skill(self, name: str) -> Optional[Skill]:
        """Retrieve a skill by name."""
        return self._skills.get(name)
```

---

### Agent Orchestration Pattern

The Agent Orchestration pattern enables coordination between multiple agents.

**Characteristics:**

- Council-based decision making
- Swarm coordination for parallel execution
- Task delegation and routing
- Result aggregation

**Council Pattern:**

```python
from typing import List, Dict, Any
from enum import Enum

class VoteDecision(Enum):
    """Possible vote decisions."""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"

class CouncilMember:
    """Represents an agent in the council."""

    def __init__(self, agent: 'BaseAgent', weight: float = 1.0):
        self.agent = agent
        self.weight = weight

    def vote(self, proposal: Dict[str, Any]) -> VoteDecision:
        """Cast a vote on a proposal."""
        result = self.agent.execute({"action": "review", "proposal": proposal})
        return VoteDecision(result.get("decision", "abstain"))

    def provide_feedback(self, proposal: Dict[str, Any]) -> str:
        """Provide detailed feedback on proposal."""
        result = self.agent.execute({"action": "feedback", "proposal": proposal})
        return result.get("feedback", "")

class AgentCouncil:
    """Orchestrates decision-making across multiple agents."""

    def __init__(self, members: List[CouncilMember], quorum: float = 0.5):
        self.members = members
        self.quorum = quorum

    def deliberate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct deliberation on a proposal."""
        votes = {}
        feedback = []

        # Collect votes from all members
        for member in self.members:
            vote = member.vote(proposal)
            votes[member.agent.name] = {
                "decision": vote,
                "weight": member.weight
            }

        # Calculate weighted results
        approval_weight = sum(
            v["weight"] for v in votes.values()
            if v["decision"] == VoteDecision.APPROVE
        )
        total_weight = sum(v["weight"] for v in votes.values())
        approval_ratio = approval_weight / total_weight if total_weight > 0 else 0

        return {
            "decision": "approved" if approval_ratio >= self.quorum else "rejected",
            "approval_ratio": approval_ratio,
            "votes": votes,
            "feedback": feedback
        }
```

---

### TypeScript Agents Pattern

TypeScript agents provide type-safe agent implementations for Node.js
ecosystems.

```typescript
interface AgentConfig {
  name: string;
  description: string;
  version: string;
  tools?: string[];
  mcpServers?: string[];
}

interface ExecutionContext {
  action: string;
  params?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

interface ExecutionResult {
  status: 'success' | 'error';
  data?: unknown;
  error?: string;
}

abstract class BaseAgent {
  protected config: AgentConfig;
  protected logger: Logger;

  constructor(config: AgentConfig) {
    this.config = config;
    this.logger = new Logger(\`agent.\${config.name}\`);
    this.initialize();
  }

  protected initialize(): void {
    this.logger.info(\`Initializing agent: \${this.config.name}\`);
  }

  async execute(context: ExecutionContext): Promise<ExecutionResult> {
    try {
      const result = await this.executeImpl(context);
      return { status: 'success', data: result };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return { status: 'error', error: errorMessage };
    }
  }

  protected abstract executeImpl(context: ExecutionContext): Promise<unknown>;
}
```

---

## Agent File Structure

Agents in this organization follow a standardized file structure:

```
agents/
├── agent-name.agent.md          # Agent definition with frontmatter
└── README.md                     # Optional: additional documentation

docs/
├── README.agents.md              # Agent catalog
└── AGENT_ARCHITECTURE_GUIDE.md   # This guide
```

**Agent File Naming Convention:**

- Format: `{agent-name}.agent.md`
- Use lowercase with hyphens
- Must end with `.agent.md` extension
- Examples: `terraform.agent.md`, `security-audit.agent.md`

---

## Agent Frontmatter Format

All agent files MUST include YAML frontmatter:

```yaml
---
name: 'Agent Name'
description: 'Detailed description of agent purpose and capabilities'
version: '1.0.0'
author: 'Team or Individual'
license: 'MIT'
tools:
  - read
  - edit
  - search
  - github/*
mcp-servers:
  server-name:
    type: 'local' | 'http'
    command: 'executable'
    args: ['arg1', 'arg2']
    url: 'https://...'
    headers:
      Authorization: 'Bearer $TOKEN'
    tools: ['*']
dependencies:
  - mcp: github
---
```

**Required Fields:**

- `name`: Human-readable agent name
- `description`: Clear description (single quotes required)

**Optional Fields:**

- `version`: Semantic version number
- `tools`: List of Copilot tools
- `mcp-servers`: MCP server configurations
- `dependencies`: Required dependencies

---

## Agent Lifecycle

### Creation

**Step 1: Define Agent Purpose**

- What problem does this agent solve?
- Who are the primary users?
- What are the success criteria?

**Step 2: Create Agent File**

```bash
touch agents/my-agent.agent.md
```

**Step 3: Write Instructions**

```markdown
# My Agent Instructions

You are a specialized agent for [domain].

## Responsibilities

1. Primary responsibility
2. Secondary responsibility

## Workflow

When user requests [action]:

1. Validate inputs
2. Execute core logic
3. Return results

## Usage Examples

- "Example request 1"
- "Example request 2"
```

### Testing

**Manual Testing:**

```bash
# Test through GitHub Copilot Chat
# @my-agent "test request"
```

**Automated Testing:**

```python
import pytest

class AgentTestHarness:
    def __init__(self, agent):
        self.agent = agent

    def test_execute_success(self, context):
        result = self.agent.execute(context)
        assert result["status"] == "success"
        assert "data" in result

    def test_execute_error(self, context):
        result = self.agent.execute(context)
        assert result["status"] == "error"
```

### Deployment

**Step 1: Validate Agent**

```bash
pre-commit run --files agents/my-agent.agent.md
```

**Step 2: Update Documentation** Update `docs/README.agents.md`

**Step 3: Commit and Push**

```bash
git add agents/my-agent.agent.md docs/README.agents.md
git commit -m "feat: add My Agent for domain-specific tasks"
git push origin main
```

### Maintenance

**Regular Updates:**

1. Version bumps
1. Dependency updates
1. Documentation updates
1. Expand test coverage

**Monitoring:**

```python
class AgentMetrics:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.execution_count = 0
        self.error_count = 0

    def record_execution(self, success: bool):
        self.execution_count += 1
        if not success:
            self.error_count += 1

    def get_success_rate(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return (self.execution_count - self.error_count) / self.execution_count
```

---

## GitHub Copilot Integration

Agents integrate with GitHub Copilot through:

### Installation

**Via VS Code:**

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square)](install-link)

**Via Direct Download:** Download `.agent.md` files to your repository's
`agents/` directory.

### Activation

1. **Chat Interface**: `@agent-name "request"`
1. **Inline Comments**: `// @agent-name: suggestion`
1. **Workspace Integration**: Automatic based on file patterns

### Tool Access

```yaml
tools:
  - read # Read file contents
  - edit # Edit files
  - search # Search codebase
  - shell # Execute shell commands
  - github/* # All GitHub operations
```

---

## MCP Server Integration

Model Context Protocol (MCP) servers extend agent capabilities.

### MCP Server Types

**Local Servers:**

```yaml
mcp-servers:
  terraform:
    type: "local"
    command: "docker"
    args: ["run", "-i", "--rm", "hashicorp/terraform-mcp-server:latest"]
    tools: ["*"]
```

**HTTP Servers:**

```yaml
mcp-servers:
  dynatrace:
    type: "http"
    url: "https://api.dynatrace.com/mcp"
    headers:
      Authorization: "Bearer $TOKEN"
    tools: ["*"]
```

### Configuration

MCP servers configured in agent frontmatter and user settings.

### Tool Discovery

```python
from typing import List, Dict, Any

class MCPClient:
    """Client for interacting with MCP servers."""

    def __init__(self, server_config: Dict[str, Any]):
        self.config = server_config
        self.tools = {}  # Populated by discover_tools() after initialization

    async def discover_tools(self) -> List[str]:
        """Discover available tools from MCP server."""
        if self.config["type"] == "http":
            return await self._discover_http_tools()
        return await self._discover_local_tools()

    async def call_tool(self, tool_name: str, params: Dict) -> Any:
        """Call a tool on the MCP server."""
        return await self._execute_tool_call(tool_name, params)
```

---

## Best Practices

### Security

**Secret Management:**

```python
import os

class SecureConfig:
    @staticmethod
    def get_secret(key: str, default: str = None) -> str:
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Required secret {key} not found")
        return value
```

**Input Validation:**

```python
import re

class InputValidator:
    @staticmethod
    def sanitize_path(path: str) -> str:
        # Remove path traversal attempts
        path = re.sub(r'\.\./', '', path)
        return path.strip()

    @staticmethod
    def sanitize_user_input(user_input: str) -> str:
        # Remove potentially dangerous characters
        return re.sub(r'[;&|`$]', '', user_input)
```

### Error Handling and Retries

**Retry Logic:**

```python
import time
import random
from typing import Callable, Any

class RetryStrategy:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute_with_retry(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    jitter = random.uniform(0, delay * 0.1)
                    time.sleep(delay + jitter)
                else:
                    raise e
```

### Testing Strategies

**Unit Testing:**

```python
import pytest
from unittest.mock import Mock

class TestAgentUnit:
    @pytest.fixture
    def mock_mcp_client(self):
        client = Mock()
        client.call_tool.return_value = {"result": "success"}
        return client

    def test_execute_success(self, mock_mcp_client):
        agent = TerraformAgent()
        agent.mcp_client = mock_mcp_client
        result = agent.execute({"action": "plan"})
        assert result["status"] == "success"
```

### Documentation Requirements

**Agent Documentation Template:**

```markdown
# Agent Name

> Brief one-line description

## Overview

Comprehensive overview of agent purpose

## Prerequisites

- Required MCP servers
- Required permissions
- Required environment variables

## Installation

Step-by-step instructions

## Usage

### Basic Usage

\`\`\`
@agent-name "basic request"
\`\`\`

### Advanced Usage

Complex scenarios

## Examples

Real-world usage examples

## Troubleshooting

Common issues and solutions

## Contributing

How to contribute

## License

License information
```

---

## Agent Examples

### Example 1: Repository Setup Agent

**Location**: `agents/repository-setup.agent.md`

**Purpose**: Automate repository creation and configuration

**Key Features**:

- Creates repositories with standard templates
- Configures branch protection
- Sets up CI/CD workflows

**Usage**:

```
@repository-setup "Create a new Python repository"
```

### Example 2: Terraform Agent

**Location**: `agents/terraform.agent.md`

**Purpose**: Terraform infrastructure specialist

**Key Features**:

- Queries Terraform registries
- Generates compliant configurations
- Manages workspaces

**Usage**:

```
@terraform "Create an AWS VPC module"
```

### Example 3: Dynatrace Expert

**Location**: `agents/dynatrace-expert.agent.md`

**Purpose**: Observability and security analysis

**Key Features**:

- Incident root cause analysis
- Deployment impact analysis
- Performance regression detection

**Usage**:

```
@dynatrace-expert "Analyze deployment impact"
```

### Example 4: PagerDuty Incident Responder

**Location**: `agents/pagerduty-incident-responder.agent.md`

**Purpose**: Automated incident response

**Key Features**:

- Retrieves incident details
- Identifies recent code changes
- Suggests remediation PRs

**Usage**:

```
@pagerduty-incident-responder "Respond to incident INC-12345"
```

---

## Workflow Diagrams

### Agent Execution Flow

```
┌─────────────────┐
│   User Request  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Copilot  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent Matcher  │──→ No Agent Found → Default Copilot
└────────┬────────┘
         │ Agent Found
         ▼
┌─────────────────┐
│ Load Agent Config│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Initialize MCP   │
│   Servers       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute Agent   │
│    Logic        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return to User  │
└─────────────────┘
```

### Agent Lifecycle

```
┌──────────────┐
│   Creation   │──→ Define purpose, create file
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Testing    │──→ Manual + automated tests
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Deployment  │──→ Validate, update docs, commit
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Maintenance  │──→ Monitor, update, deprecate
└──────────────┘
       │
       └──────────→ Back to Testing for updates
```

### Council Deliberation Flow

```
┌─────────────┐
│  Proposal   │
└──────┬──────┘
       │
       ▼
┌────────────────────────────────┐
│     Distribute to Council      │
└──────┬─────────────────┬───────┘
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Agent A    │   │  Agent B    │
│   Vote      │   │   Vote      │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────┬─────┬──────┘
            │     │
            ▼     ▼
       ┌─────────────┐
       │   Tally     │
       │   Votes     │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │  Decision   │
       └─────────────┘
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Agent Not Found

**Symptom**: Copilot doesn't recognize agent mention

**Solutions**:

1. Verify agent file is in `agents/` directory
1. Check file naming follows `.agent.md` convention
1. Ensure frontmatter is valid YAML
1. Restart VS Code

#### Issue 2: MCP Server Connection Failed

**Symptom**: Agent can't connect to MCP server

**Solutions**:

1. Verify MCP server is running
1. Check environment variables
1. Validate configuration
1. Review server logs

#### Issue 3: Tool Access Denied

**Symptom**: Agent can't access tools

**Solutions**:

1. Verify tools listed in frontmatter
1. Check user permissions
1. Ensure MCP server exposes tools

#### Issue 4: Slow Agent Response

**Symptom**: Agent takes too long

**Solutions**:

1. Optimize MCP server calls
1. Add caching layer
1. Use async execution
1. Profile agent execution

#### Issue 5: Inconsistent Results

**Symptom**: Different results for same input

**Solutions**:

1. Review for determinism
1. Fix random behavior
1. Add input validation
1. Log intermediate steps

### Debugging Tools

**Agent Logger:**

```python
import logging

def setup_agent_logging(agent_name: str, level: int = logging.DEBUG):
    logger = logging.getLogger(f"agent.{agent_name}")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
```

### Getting Help

**Internal Resources:**

- [Agent Examples](../ai_framework/agents/)
- [MCP Server Documentation](https://modelcontextprotocol.io/)<!-- link:docs.modelcontextprotocol -->
- [GitHub Copilot Documentation](https://docs.github.com/copilot)<!-- link:docs.github_copilot -->

**Community Support:**

- GitHub Discussions
- Internal Slack: `#agents-dev`
- Office hours: Thursdays 2PM UTC

---

## Appendix

### Glossary

- **Agent**: Specialized AI assistant with domain-specific capabilities
- **MCP**: Model Context Protocol for external tool integration
- **Frontmatter**: YAML metadata at beginning of agent files
- **Skill**: Discrete, reusable agent capability
- **Council**: Group of agents that deliberate on decisions
- **Swarm**: Set of agents executing tasks in parallel
- **Tool**: Function exposed by MCP server

### References

- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)<!-- link:github.awesome_copilot -->
- [Model Context Protocol](https://modelcontextprotocol.io/)<!-- link:docs.modelcontextprotocol -->
- [GitHub Copilot Docs](https://docs.github.com/copilot)<!-- link:docs.github_copilot -->
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Version History

- **1.0.0** (2024-11-24): Initial release
  - Documented BaseAgent pattern
  - Added Skills System pattern
  - Included Agent Orchestration pattern
  - Added TypeScript Agents pattern
  - Comprehensive lifecycle documentation
  - Best practices and troubleshooting

---

**Maintained by**: ivi374forivi Organization\
**Last Updated**:
2024-11-24\
**License**: MIT
