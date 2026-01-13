# 🛠️ Organization Management Scripts

This directory contains automation scripts that bring the AI GitHub Management
Protocol to life.

## 📁 Scripts Overview

### 🕷️ `web_crawler.py`

**Purpose**: Comprehensive organization health monitoring and analysis

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

### 🎨 `ecosystem_visualizer.py`

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

### 🔄 `quota_manager.py`

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

## 🔧 Dependencies

### Python Packages

```bash
pip install requests
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
```

## 🤝 Contributing

Improvements to these scripts should:

- Follow the AI GitHub Management Protocol modules
- Include error handling and logging
- Update this README
- Add tests where applicable

## 📚 Related Documentation

- [AI Implementation Guide](../docs/AI_IMPLEMENTATION_GUIDE.md)
- [for-ai-implementation.txt](../for-ai-implementation.txt) - Complete AI
  protocol
- [Repository Setup Checklist](../docs/REPOSITORY_SETUP_CHECKLIST.md)

---

**🎉 Bringing the organization to life, one analysis at a time!**
