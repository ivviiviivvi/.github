# Agent Tracking Architecture

## Overview

The {{ORG_NAME}}/.github repository uses multiple agent tracking systems to
coordinate automation, capture organizational knowledge, and prevent task
duplication. This document describes each system, their relationships, and their
purposes.

______________________________________________________________________

## System Components

### 1. Jules Learning Journal (`.jules/`)

**Purpose:** Captures performance optimizations and architectural learnings from
various specialized agents

**Location:** `.jules/` (consolidated in Phase 1.2 from previous `.Jules/` case
variant)

**Contents:**

- `bolt.md` - Performance optimization agent's learnings
- `palette.md` - UX/documentation agent's learnings
- `sentinel.md` - Security agent's learnings

**Format:** Each file uses dated journal entries with consistent structure:

```markdown
## YYYY-MM-DD - [Topic Title]

**Learning:** Description of what was learned
**Action:** Concrete action item or pattern to apply
```

**Usage Pattern:**

- Agents record learnings after completing significant work
- Serves as organizational memory and best practices documentation
- Referenced by future agents when tackling similar problems

#### Bolt - Performance Agent

**Focus Areas:**

- Query optimization (caching, SSRF prevention)
- Regex performance (pre-compilation strategies)
- SSL context overhead reduction
- TOCTOU vulnerability prevention

**Example Entry:**

```markdown
## 2026-01-09 - [Pre-compiling Regex in Loops]

**Learning:** Repeatedly calling `re.findall`, `re.split` or `any()` checks with
strings in a loop incurs significant overhead. Pre-compiling regex patterns as
class constants provided an ~18% performance improvement.

**Action:** When performing repeated text pattern matching, always pre-compile
regex patterns as class constants (`_PATTERN = re.compile(...)`) and use
`_PATTERN.search()` instead of inline method calls.
```

#### Palette - UX/Documentation Agent

**Focus Areas:**

- Mermaid diagram styling
- Markdown table consistency
- Collapsible sections in reports
- Alert grouping in dashboards

**Example Entry:**

```markdown
## 2025-12-17 - [Mermaid Diagram Styling]

**Learning:** Mermaid diagrams in GitHub Markdown can be styled using `classDef`
and `:::className` syntax for visually distinct layers.

**Action:** Apply this pattern to all future script-generated Mermaid diagrams
to improve readability and visual hierarchy.
```

#### Sentinel - Security Agent

**Focus Areas:**

- Code injection prevention
- DoS attack mitigation
- GitHub Actions security
- Input validation patterns

**Example Entry:**

```markdown
## 2025-02-18 - [Fix Code Injection in GitHub Actions]

**Vulnerability:** Unmitigated Code Injection in batch-pr-operations.yml via
direct interpolation in github-script action.

**Learning:** Direct interpolation of inputs in github-script allows code
injection. Always use environment variables to pass inputs.

**Prevention:** Map inputs to `env:` in workflow steps, access via
`process.env.VAR_NAME` within script to treat data as data, not code.
```

______________________________________________________________________

### 2. Mouthpiece Filter System

**Purpose:** Transforms natural human writing into structured AI prompts while
preserving voice and intent

**Location:** `automation/scripts/natural_language_prompt_filter.py` (641 lines)

**Relationship to Jules:** While not directly part of Jules tracking, Mouthpiece
Filter enables humans to communicate naturally with agents, which Jules and
other agents then process.

**Key Features:**

- Intent detection (creation, problem_solving, understanding, improvement,
  design)
- Concept extraction with pre-compiled regex patterns
- Metaphor preservation
- Tone analysis
- Structured prompt generation

**Architecture:**

```python
class MouthpieceFilter:
    """Transforms natural text into AI-optimized prompts"""

    # Pre-compiled patterns for performance (learned from Bolt)
    _CAPITALIZED_WORDS = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")
    _METAPHOR_PATTERN = re.compile(...)

    def transform(self, text: str) -> Dict[str, any]:
        """Main transformation pipeline"""
        analysis = self._analyze_text(text)
        structure = self._extract_structure(text, analysis)
        prompt = self._build_prompt(text, analysis, structure)
        return {...}
```

**Performance Optimizations:**

- Uses Bolt's regex pre-compilation pattern for ~18% speed improvement
- Caches concept extraction results to avoid redundant computation
- Efficient text processing with single-pass analysis where possible

**Usage:**

```bash
# Transform natural writing
python3 natural_language_prompt_filter.py "your natural writing here"

# From file
python3 natural_language_prompt_filter.py --file input.txt

# From stdin
echo "your text" | python3 natural_language_prompt_filter.py --stdin
```

______________________________________________________________________

### 3. Task Deduplication System

**Purpose:** Prevents cascading/redundant Jules tasks and tracks automated PRs

**Location:** `.github/scripts/task_deduplicator.py`

**State File:** `.github/task_state.json` (not committed, runtime only)

**Key Features:**

- Generates unique hash for each task (type + data)
- Tracks processed tasks with 24-hour deduplication window
- Registers PRs created by tasks
- Automatic cleanup of old records (7-day retention)

**Integration with Jules:**

- Jules workflow checks deduplication before processing
- Prevents Jules from creating duplicate tasks within same day
- Notifies users when duplicate requests are skipped

**API:**

```bash
# Check if task should be processed
python3 task_deduplicator.py check "task_type" '{"key":"value"}'

# Register a PR for a task
python3 task_deduplicator.py register_pr <pr_number> "task_type" '{"key":"value"}'

# Get active PRs for consolidation
python3 task_deduplicator.py get_active_prs [max_age_hours]

# Cleanup old records
python3 task_deduplicator.py cleanup [retention_days]
```

**Workflow Integration:**

```yaml
# In Jules workflow
- name: Check if task already processed
  id: check_duplicate
  run: |
    result=$(python3 .github/scripts/task_deduplicator.py check "jules_task" '{"issue": "${{ github.event.issue.number }}"}')
    echo "should_process=$result" >> $GITHUB_OUTPUT

- name: Process task
  if: steps.check_duplicate.outputs.should_process == 'true'
  run: # ... execute task
```

______________________________________________________________________

### 4. AgentSphere Deployment System

**Purpose:** Automatically deploys applications to AgentSphere cloud sandbox for
live demo generation

**Location:** `.github/agentsphere-config.yml`,
`.github/workflows/agentsphere-deployment.yml`

**Relationship to Agents:** Provides live environment for testing
agent-generated code

**Configuration:**

```yaml
enabled: true

global:
  api_endpoint: "https://api.agentsphere.dev/v1"
  startup_timeout: 60
  health_check_interval: 30
  max_retries: 3

  badge:
    style: "for-the-badge"
    color: "brightgreen"
    label: "Live Demo"
    position: "after-title"

  access:
    visibility: "public"
    require_auth: false
    rate_limit: 100
```

**Capabilities:**

- Automatic deployment on push
- Live demo badge generation
- Health checking
- Auto-restart on crash
- Public/private access control

______________________________________________________________________

### 5. Agent Documentation System

**Purpose:** Maintains registry of all custom agents with install badges and
metadata

**Location:** `docs/README.agents.md`, `automation/scripts/update_agent_docs.py`

**Agent Count:** 26 custom agents across multiple domains

**Categories:**

- **Infrastructure:** Terraform, Arm Migration, Workflow Optimizer
- **Security:** Security Audit, JFrog Security, Data Sanitization, StackHawk
- **Operations:** PagerDuty Responder, Dynatrace Expert, LaunchDarkly Cleanup
- **Development:** CSharpExpert, WinFormsExpert
- **Database:** Neon Migration, Neon Performance Analyzer
- **Data:** Data Forensics, Data Reclamation, Data Decommissioning
- **Documentation:** ADR Generator, Completionism Specialist
- **Governance:** GitHub Org Manager, Repository Setup
- **Analysis:** Nervous Archaeologist, Greener Grass Benchmark

**Agent Metadata Format:**

```yaml
---
name: agent-name
description: "Brief description of agent purpose"
tools:
  - github/*
  - shell
model: claude-sonnet-4
---
# Agent Title

Agent instructions and implementation...
```

**Documentation Generator:**

```python
# automation/scripts/update_agent_docs.py
def extract_metadata(filepath):
    """Extract agent name, title, description from agent file"""
    # Parses YAML frontmatter and markdown

def generate_table(agents):
    """Generate markdown table with install badges"""
```

______________________________________________________________________

## Agent Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    User/Developer Input                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                ┌────────────────┐
                │ Mouthpiece     │  Transforms natural language
                │ Filter         │  into structured prompts
                └────────┬───────┘
                         │
                         ▼
                ┌────────────────┐
                │ Task           │  Checks if task already
                │ Deduplicator   │  processed (24hr window)
                └────────┬───────┘
                         │
                         ▼
                ┌────────────────┐
                │ Jules          │  Orchestrates task execution
                │ Orchestrator   │  (daily master workflow)
                └────────┬───────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐     ┌──────────┐
    │ Bolt   │      │Palette │     │ Sentinel │
    │(Perf)  │      │ (UX)   │     │ (Sec)    │
    └───┬────┘      └───┬────┘     └────┬─────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼ Record learnings
                  ┌──────────┐
                  │ .jules/  │  Journal entries for
                  │ *.md     │  organizational memory
                  └──────────┘
                        │
                        ▼
                ┌────────────────┐
                │ Custom Agents  │  26+ specialized agents
                │ (agents/)      │  leverage learnings
                └────────┬───────┘
                         │
                         ▼
                ┌────────────────┐
                │ AgentSphere    │  Deploy & test in
                │ Sandbox        │  live environment
                └────────────────┘
```

______________________________________________________________________

## Organizational Benefits

### 1. Knowledge Preservation

- Agent learnings persist across sessions and contributors
- Best practices codified in accessible journal format
- Security vulnerabilities and fixes documented
- Performance optimizations captured and reusable

### 2. Task Efficiency

- Deduplication prevents wasted compute and PR noise
- Single daily PR consolidation reduces review burden
- Automated cleanup maintains system health

### 3. Quality Assurance

- Security patterns from Sentinel prevent vulnerabilities
- Performance patterns from Bolt optimize hot paths
- UX patterns from Palette improve user experience
- Documentation patterns ensure consistency

### 4. Developer Experience

- Natural language input via Mouthpiece Filter
- 26+ specialized agents for domain-specific tasks
- Live demos via AgentSphere deployment
- Clear agent documentation with install badges

______________________________________________________________________

## Maintenance and Validation

### Daily Operations

**Automated:**

- Task deduplication runs on every Jules invocation
- PR consolidation runs daily at 1 AM UTC
- Cleanup of old task records (7-day retention)
- AgentSphere health checks every 30 seconds

**Manual Review:**

- Weekly review of `.jules/*.md` journal entries
- Monthly audit of agent effectiveness metrics
- Quarterly evaluation of agent portfolio

### Validation Tests

**Current State:** No automated validation tests (Phase 3.1 action item)

**Proposed Tests:**

1. **Journal Entry Validation**

   ```python
   # tests/test_jules_journal.py
   def test_journal_entry_format():
       """Verify all .jules/*.md entries follow standard format"""

   def test_no_duplicate_dates():
       """Ensure no duplicate date entries"""

   def test_learning_action_pairs():
       """Verify each learning has corresponding action"""
   ```

1. **Task Deduplication Tests**

   ```python
   # tests/test_task_deduplication.py
   def test_duplicate_detection():
       """Verify tasks are correctly identified as duplicates"""

   def test_24_hour_window():
       """Ensure deduplication window works correctly"""

   def test_cleanup_retention():
       """Verify old records are cleaned up after 7 days"""
   ```

1. **Agent Metadata Validation**

   ```python
   # tests/test_agent_metadata.py
   def test_all_agents_have_frontmatter():
       """Verify all agent files have valid YAML frontmatter"""

   def test_agent_descriptions():
       """Ensure all agents have non-empty descriptions"""

   def test_readme_sync():
       """Verify README.agents.md is in sync with agent files"""
   ```

______________________________________________________________________

## Future Enhancements

### Proposed Consolidation (Phase 3.1)

**Option A: Expand .jules/ Directory**

```
.jules/
├── README.md              # Overview of Jules system
├── journals/              # Learning journals
│   ├── bolt.md
│   ├── palette.md
│   └── sentinel.md
├── config/                # Configuration
│   ├── task_state.json   # Move from .github/
│   └── deduplication.yml # Deduplication rules
└── scripts/              # Related scripts
    ├── task_deduplicator.py  # Move from .github/scripts/
    └── journal_validator.py  # New validation script
```

**Option B: Create Top-Level ai_agents/ Directory**

```
ai_agents/
├── README.md             # Agent system overview
├── jules/                # Jules orchestrator
│   ├── tracker.json
│   ├── bolt.md
│   ├── palette.md
│   └── sentinel.md
├── custom/               # Custom agents (from agents/)
│   ├── CSharpExpert.agent.md
│   ├── terraform.agent.md
│   └── ...
├── mouthpiece/           # Mouthpiece system
│   └── filter.py         # Move from automation/scripts/
└── docs/
    ├── AGENT_ARCHITECTURE.md
    └── AGENT_TRACKING.md  # This document
```

**Recommendation:** Option A (expand `.jules/`) maintains existing structure
while improving organization.

### Additional Improvements

1. **Agent Interaction Visualization**

   - Generate Mermaid diagrams of agent relationships
   - Track which agents invoke other agents
   - Monitor agent success/failure rates

1. **Learning Search and Retrieval**

   - Index journal entries for fast lookup
   - Implement semantic search across learnings
   - Auto-suggest relevant learnings when similar tasks detected

1. **Agent Performance Metrics**

   - Track execution time per agent
   - Measure task success rates
   - Monitor resource consumption
   - Dashboard for agent health

1. **Collaborative Learning**

   - Cross-reference learnings across agents
   - Identify contradictions or conflicts
   - Suggest consolidation of related patterns
   - Versioning for learning evolution

______________________________________________________________________

## Related Documentation

- JULES_CASCADE_PREVENTION.md - Daily orchestrator and PR consolidation
- JULES_CASCADE_PREVENTION_QUICK_REF.md - Quick reference guide
- JULES_IMPLEMENTATION_SUMMARY.md - Implementation details
- [README.agents.md](../README.agents.md) - Custom agent registry
- [AGENT_ARCHITECTURE_GUIDE.md](../guides/AGENT_ARCHITECTURE_GUIDE.md) -
  Building custom agents
- NLP_FILTER_SYSTEM.md - Mouthpiece filter documentation

______________________________________________________________________

## Troubleshooting

### Journal Entry Conflicts

**Problem:** Git merge conflicts in `.jules/*.md` files

**Solution:** Both entries should typically be preserved

```bash
# Keep both entries during merge
git checkout --ours .jules/bolt.md
git checkout --theirs .jules/bolt.md
# Manually merge both entries with proper date ordering
```

### Task Deduplication False Positives

**Problem:** Legitimate tasks being marked as duplicates

**Solution:** Refine task hash generation to include more differentiating
factors

```python
# In task_deduplicator.py
def _generate_task_hash(task_type: str, task_data: Dict) -> str:
    # Add more fields to make hash more specific
    key_fields = ["issue_number", "pr_number", "specific_file", "timestamp"]
    # ...
```

### Missing Agent Documentation

**Problem:** New agents not appearing in README.agents.md

**Solution:** Run documentation generator

```bash
python3 automation/scripts/update_agent_docs.py
git add docs/README.agents.md
git commit -m "docs: update agent registry"
```

______________________________________________________________________

**Last Updated:** 2026-01-14\
**Phase:** 3.1 - Agent Tracking Systems
Consolidation\
**Status:** Documentation Complete, Validation Tests Pending
