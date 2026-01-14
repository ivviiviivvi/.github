# 🛠️ Organization Management Scripts

This directory contains automation scripts that bring the AI GitHub Management
Protocol to life.

## 📁 Scripts Overview

### 🕷️ `web_crawler.py` 🔒

**Status**: 790 lines, security-hardened, SSRF protection\
**Type Safety**: In
progress (28 mypy --strict errors remaining)

**Purpose**: Comprehensive organization health monitoring and analysis with
security-critical SSRF attack prevention

**Implements**:

- **AI-GH-06**: Ecosystem Integration & Architecture Monitoring
- **AI-GH-07**: Observability & System Health
- **AI-GH-08**: Strategic Analysis & Risk Mitigation

**Features**:

- 🔍 Crawls all markdown documentation
- 🌐 Validates external links
- 📊 Analyzes repository health metrics
- 🗺️ Maps the entire ecosystem
- 🔦 Identifies blind spots (unknown risks)
- 💥 Identifies shatter points (single points of failure)
- 📝 Generates comprehensive JSON and Markdown reports

**Security Features** (Sentinel's learnings in `.jules/sentinel.md`):

- 🔒 SSRF attack prevention
- 🛡️ DNS rebinding protection
- 🚫 IP address validation (blocks private/localhost/multicast)
- ✅ SSL/TLS certificate verification
- 🏎️ DoS prevention via `preload_content=False`
- 🔗 Connection pooling with pinned IPs

**Performance Optimizations** (Bolt's learnings in `.jules/bolt.md`):

- ⚡ Cached DNS resolution
- ⚡ Cached IP safety checks
- ⚡ Reusable SSL contexts
- ⚡ Connection pool reuse (TCP Keep-Alive)
- ⚡ Parallel link checking with ThreadPoolExecutor

**Usage**:

```bash
# Basic analysis (no link validation)
python scripts/web_crawler.py

# Full analysis with link validation (slow)
python scripts/web_crawler.py --validate-links

# Specify custom directory
python scripts/web_crawler.py --base-dir /path/to/repo

# With custom GitHub token
python scripts/web_crawler.py --github-token ghp_xxx --org-name myorg
```

**Environment Variables**:

- `GITHUB_TOKEN`: GitHub API token (required for repository analysis)
- `GITHUB_REPOSITORY`: Repository in format `owner/repo`

**Output**:

- `reports/org_health_YYYYMMDD_HHMMSS.json` - Full JSON report
- `reports/org_health_YYYYMMDD_HHMMSS.md` - Markdown summary

---

### 🎨 `ecosystem_visualizer.py` ✅

**Status**: 812 lines, fully type-hinted, mypy --strict compliant\
**Phase
3.2**: ✅ COMPLETE

**Purpose**: Generate visual dashboards and diagrams of the ecosystem

**Implements**:

- **AI-GH-06**: Dynamic ecosystem mapping
- **AI-GH-07**: Repository analytics visualization

**Features**:

- 📊 Creates interactive Mermaid diagrams
- 🎯 Generates comprehensive dashboards
- 🏆 Calculates health scores and badges
- 📈 Visualizes trends and metrics
- ⚙️ Configurable workflow display limit for optimal diagram readability
- ⚡ Performance-optimized with regex pre-compilation (Bolt's learning)

**Configuration**:

- `MAX_DIAGRAM_WORKFLOWS`: Controls how many workflows appear in the Mermaid
  diagram (default: 10)
  - All workflows are still listed in the "Active Workflows" section
  - Can be adjusted by modifying the class constant if needed for larger
    displays
  - Users are notified when workflows exceed the display limit

**Usage**:

```bash
# Generate dashboard from latest report
python scripts/ecosystem_visualizer.py --find-latest

# Generate from specific report
python scripts/ecosystem_visualizer.py --report reports/org_health_20241116.json

# Custom output location
python scripts/ecosystem_visualizer.py --find-latest --output reports/MY_DASHBOARD.md
```

**Output**:

- `reports/DASHBOARD.md` - Visual dashboard with Mermaid diagrams
- Health badge in Shields.io format

---

### 🏷️ `sync_labels.py` ✅

**Status**: 369 lines, fully type-hinted, mypy compliant\
**Phase 3.2**: ✅
COMPLETE

**Purpose**: Synchronizes GitHub labels across organization repositories using a
YAML definition file

**Features**:

- Organization-wide label management
- Repository exclusion support
- Dry-run mode for safety
- Detailed operation statistics
- Error handling and reporting

**Usage**:

```bash
# Dry run (preview changes)
python sync_labels.py --org ivviiviivvi --dry-run

# Actually sync labels
python sync_labels.py --org ivviiviivvi --token $GITHUB_TOKEN

# Exclude specific repositories
python sync_labels.py --org ivviiviivvi --exclude repo1,repo2
```

**Configuration**: `seed.yaml` - Label definitions (name, color, description)

---

### 🎨 `mouthpiece_filter.py`

**Status**: 641 lines, well-documented, performance-optimized

**Purpose**: Transforms natural human writing into structured AI prompts while
preserving voice and intent

**Capabilities**:

- Intent detection (creation, problem_solving, understanding, improvement,
  design)
- Concept extraction with pre-compiled regex patterns (~18% faster)
- Metaphor preservation
- Tone analysis (formal, casual, technical, mixed)
- Structured prompt generation
- JSON/Markdown output formats

**Usage**:

```bash
# Transform text inline
python mouthpiece_filter.py "your natural writing here"

# From file
python mouthpiece_filter.py --file input.txt

# From stdin
echo "your text" | python mouthpiece_filter.py --stdin
```

---

### 🔄 `quota_manager.py`

**Status**: Needs type hint and docstring audit

**Purpose**: Manage API quotas for AI workflow integrations

**Features**:

- Tracks usage across multiple AI providers
- Prevents quota exhaustion
- Implements rate limiting

**Usage**: Automatically invoked by AI workflows

---

### 📦 `commit_changes.sh`

**Purpose**: Automated git commit helper

**Usage**: Used by workflows to commit generated reports and artifacts

---

### ✅ `validate_chatmode_frontmatter.py`

**Purpose**: Validate YAML frontmatter for chatmode definitions

**Usage**:

```bash
python automation/scripts/validate_chatmode_frontmatter.py
```

Auto-fix legacy description lines:

```bash
python automation/scripts/validate_chatmode_frontmatter.py --fix
```

---

### 📋 `generate_chatmode_inventory.py`

**Purpose**: Generate a chatmode inventory table from frontmatter

**Usage**:

```bash
python automation/scripts/generate_chatmode_inventory.py
```

---

### 🔒 `manage_lock.sh`

**Purpose**: File-based locking mechanism for concurrent workflows

**Usage**: Prevents race conditions in parallel automation

---

## 🚀 Automated Workflows

These scripts are automatically triggered by GitHub Actions:

### Weekly Organization Health Crawl

**Workflow**: `.github/workflows/org-health-crawler.yml` **Schedule**: Every
Monday at 00:00 UTC **Actions**:

1. Runs full health analysis
1. Uploads reports as artifacts
1. Commits reports to repository
1. Creates GitHub issues for critical findings

### Manual Triggers

You can manually trigger workflows from the Actions tab:

- **Organization Health Crawler** - Run on-demand with optional link validation

## 📊 Reports Structure

All reports are saved to the `reports/` directory:

```
reports/
├── DASHBOARD.md                    # Latest ecosystem dashboard
├── org_health_20241116_120000.json # Full health report (JSON)
├── org_health_20241116_120000.md   # Summary report (Markdown)
└── .gitkeep
```

### Report Contents

**JSON Report Structure**:

```json
{
  "timestamp": "2024-11-16T12:00:00Z",
  "organization": "ivi374forivi",
  "link_validation": {
    "total_links": 150,
    "valid": 145,
    "broken": 5,
    "broken_links": [...]
  },
  "repository_health": {
    "total_repos": 10,
    "active_repos": 8,
    "stale_repos": 2,
    "repositories": [...]
  },
  "ecosystem_map": {
    "workflows": [...],
    "copilot_agents": [...],
    "copilot_instructions": [...],
    "technologies": [...]
  },
  "blind_spots": [...],
  "shatter_points": [...]
}
```

## � Additional Utilities

### `update_agent_docs.py`

**Purpose**: Updates `docs/README.agents.md` with agent metadata

**Usage**:

```bash
python update_agent_docs.py
```

**Process**:

1. Scans `ai_framework/agents/` for `*.agent.md` files
1. Extracts metadata from YAML frontmatter
1. Generates markdown table with install badges
1. Updates `docs/README.agents.md`

---

### `auto-docs.py`

**Status**: 17KB, needs type hint review

**Purpose**: Automatically generates documentation from code and GitHub metadata

**Features**:

- README generation
- API documentation
- Workflow documentation
- Agent registry updates

---

## 🔧 Dependencies

### Python Packages

**Core**:

```bash
pip install requests urllib3 PyGitHub PyYAML
```

**Type Stubs** (for mypy --strict compliance):

```bash
pip install types-requests
```

**Development**:

```bash
pip install pytest mypy flake8 bandit black
```

### System Requirements

- Python 3.11+
- Git
- GitHub CLI (`gh`) for some features (optional)

## 🎯 AI GitHub Management Protocol Mapping

| Module                             | Script                                      | Workflow                                     |
| ---------------------------------- | ------------------------------------------- | -------------------------------------------- |
| **AI-GH-06**: Ecosystem Monitoring | `web_crawler.py`, `ecosystem_visualizer.py` | `org-health-crawler.yml`                     |
| **AI-GH-07**: System Health        | `web_crawler.py`                            | `org-health-crawler.yml`, `repo-metrics.yml` |
| **AI-GH-08**: Risk Analysis        | `web_crawler.py`                            | `org-health-crawler.yml`                     |

## 📈 Health Scoring

The health score (0-100) is calculated based on:

| Factor              | Weight | Criteria                                            |
| ------------------- | ------ | --------------------------------------------------- |
| Repository Activity | 40%    | Percentage of repos updated in last 90 days         |
| Link Validity       | 30%    | Percentage of working documentation links           |
| Critical Alerts     | 30%    | Penalty for critical blind spots and shatter points |

**Score Ranges**:

- 🟢 **80-100**: Excellent
- 🟢 **60-79**: Good
- 🟡 **40-59**: Fair
- 🟠 **20-39**: Poor
- 🔴 **0-19**: Critical

## 🚨 Alerting

Critical findings trigger automated GitHub issues with:

- `health-alert` label
- `priority: high` label
- Detailed analysis and recommendations
- Link to full report

## 🔐 Security

- Scripts require `GITHUB_TOKEN` with appropriate permissions
- No secrets are logged or committed
- All API calls respect rate limits
- Reports may contain sensitive organizational data - review before sharing

## 📝 Development

### Code Quality Standards (Phase 3.2)

**Python Scripts**:

- ✅ Type hints on all functions (PEP 484)
- ✅ Docstrings on all public functions (Google/NumPy style)
- ✅ Pass `mypy --strict` (goal: all scripts)
- ✅ Pass `flake8` with max-line-length=88
- ✅ Pass `bandit` security scan
- ✅ 80%+ test coverage (goal)

**Current Status**:

- `ecosystem_visualizer.py`: ✅ mypy --strict compliant
- `sync_labels.py`: ✅ Type annotations complete
- `web_crawler.py`: 🔄 In progress (28 mypy errors remaining)
- Other scripts: ⏸️ Pending audit

### Adding New Scripts

1. Use proper shebang: `#!/usr/bin/env python3`
1. Add module docstring with purpose and description
1. Add type hints to all functions
1. Add unit tests in `test_script_name.py`
1. Update this README

### Performance Best Practices

Apply learnings from `.jules/bolt.md`:

1. **Pre-compile regex patterns** at class level
1. **Cache expensive operations** with `functools.lru_cache`
1. **Use connection pooling** for HTTP requests
1. **Profile before optimizing** with `cProfile`

### Security Best Practices

Apply learnings from `.jules/sentinel.md`:

1. **Validate all inputs** (URLs, file paths, user data)
1. **Prevent SSRF attacks** (block private IPs, validate schemes)
1. **Use environment variables** for secrets (never hardcode tokens)
1. **Prevent code injection** (sanitize shell command inputs)

### Adding New Analysis

1. Add analysis function to `web_crawler.py`
1. Update `run_full_analysis()` method
1. Add results to report structure
1. Update visualizer to display new metrics

### Testing Locally

```bash
# Set up environment
export GITHUB_TOKEN=your_token_here
export GITHUB_REPOSITORY=owner/repo

# Run crawler
python scripts/web_crawler.py --base-dir .

# Generate dashboard
python scripts/ecosystem_visualizer.py --find-latest

# Run type checking
mypy --strict ecosystem_visualizer.py
mypy --strict sync_labels.py

# Run tests
pytest test_*.py -v
```

## 🤝 Contributing

Improvements to these scripts should:

- Follow the AI GitHub Management Protocol modules
- Include error handling and logging
- Update this README
- Add tests where applicable

## 🧪 Testing

### Test Scripts

- `test_ecosystem_visualizer.py`: Unit tests for dashboard generation
- `test_web_crawler_security.py`: Security tests for SSRF protection
- `test_ssrf_logic.py`: SSRF protection logic validation
- `test_ssrf_protection.py`: Additional SSRF tests
- `test_quota_lock.py`: Quota locking mechanism tests

### Running Tests

```bash
# All tests
pytest automation/scripts/test_*.py -v

# Specific test file
pytest automation/scripts/test_web_crawler_security.py -v

# With coverage
pytest automation/scripts/ --cov=automation/scripts --cov-report=html
```

### Test Coverage Goals

**Current Status**:

- `ecosystem_visualizer.py`: ✅ Tests exist
- `web_crawler.py`: ✅ Security tests comprehensive
- `sync_labels.py`: ⚠️ Needs tests
- `auto-docs.py`: ⚠️ Needs tests
- `quota_manager.py`: ✅ Lock tests exist
- `mouthpiece_filter.py`: ⚠️ Needs tests

**Target**: 80%+ coverage for all production scripts

---

## 📚 Related Documentation

- [AGENT_TRACKING.md](../../docs/AGENT_TRACKING.md) - Agent system architecture
  (Phase 3.1)
- [CLEANUP_ROADMAP.md](../../CLEANUP_ROADMAP.md) - Codebase cleanup plan
- [.jules/bolt.md](../../.jules/bolt.md) - Performance optimization learnings
- [.jules/sentinel.md](../../.jules/sentinel.md) - Security learnings
- [AI Implementation Guide](../../docs/AI_IMPLEMENTATION_GUIDE.md)
- [for-ai-implementation.txt](../../for-ai-implementation.txt) - Complete AI
  protocol

---

**🎉 Bringing the organization to life, one analysis at a time!**

**Last Updated**: 2026-01-14 (Phase 3.2 - Python Script Audit)
