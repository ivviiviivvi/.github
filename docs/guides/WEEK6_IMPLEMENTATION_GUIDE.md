# Week 6: Repository Expansion Implementation Guide

**Status:** Ready for implementation\
**Start Date:** February 22,
2026\
**Duration:** 7 days\
**Deliverable:** 1-2 pilot repositories with
workflows deployed

______________________________________________________________________

## Overview

Week 6 focuses on expanding workflow automation from the main `.github`
repository to 1-2 pilot repositories within the organization. This controlled
expansion validates the system's adaptability and prepares for wider deployment.

### Objectives

1. **Select** optimal pilot repositories using data-driven evaluation
1. **Customize** workflows to each repository's specific needs
1. **Deploy** in phases (passive observation → active automation)
1. **Monitor** intensively to ensure success
1. **Document** lessons learned for future expansions

### Success Criteria

- [ ] 1-2 repositories successfully onboarded
- [ ] Workflow success rate >95% in pilot repositories
- [ ] Team satisfaction >8.0/10
- [ ] Zero rollbacks required
- [ ] Documentation complete for future expansions

______________________________________________________________________

## Tools and Scripts

### 1. Repository Evaluation Script

**Location:** `automation/scripts/evaluate_repository.py`

**Purpose:** Automatically evaluates repositories for pilot readiness

**Usage:**

```bash
# Evaluate a single repository
python3 automation/scripts/evaluate_repository.py <owner/repo>

# Evaluate all organization repositories
python3 automation/scripts/evaluate_repository.py --all <org>
```

**Evaluation Criteria:**

| Category       | Weight | Key Factors                                |
| -------------- | ------ | ------------------------------------------ |
| Activity       | 30%    | Commits, PRs, issues, development velocity |
| Documentation  | 20%    | CODEOWNERS, CONTRIBUTING.md presence       |
| Size           | 15%    | Stars, forks, community size               |
| Health         | 15%    | Issue/PR volume (not too many or too few)  |
| Community      | 10%    | External contributors, engagement          |
| Infrastructure | 10%    | Existing .github setup, label system       |

**Scoring:**

- **80-100:** EXCELLENT - Highly recommended for pilot
- **60-79:** GOOD - Suitable for pilot
- **40-59:** FAIR - Consider after improvements
- **0-39:** POOR - Not recommended

**Output:**

- Console: Detailed evaluation with category scores
- JSON file: `<owner>_<repo>_evaluation.json`

### 2. Workflow Generator Script

**Location:** `automation/scripts/generate_pilot_workflows.py`

**Purpose:** Generates customized workflows from configuration file

**Usage:**

```bash
python3 automation/scripts/generate_pilot_workflows.py \
  automation/config/pilot-<repo-name>-config.yml
```

**Generated Files:**

- `generated_workflows/issue-triage.yml`
- `generated_workflows/auto-assign-reviewers.yml`
- `generated_workflows/stale-management.yml`

**Customizations Applied:**

- Label mapping (repository-specific labels)
- CODEOWNERS integration (team assignments)
- Stale detection parameters (grace periods, exempt labels)
- Slack notification priorities (P1/P2/P3)
- Path-based reviewer assignment rules

### 3. Quick Setup Script

**Location:** `setup_week6.sh`

**Purpose:** Streamlines Week 6 setup process

**Usage:**

```bash
# Full workflow: evaluate + configure + generate
./setup_week6.sh <owner/repo>

# Evaluate all org repos
./setup_week6.sh --all <org>

# Setup only (make scripts executable)
./setup_week6.sh --setup-only
```

**What it does:**

1. Checks prerequisites (gh CLI, Python 3, jq)
1. Makes scripts executable
1. Runs repository evaluation
1. Creates pilot configuration from template
1. Applies basic customizations (owner, repo name, date)

______________________________________________________________________

## Configuration Template

**Location:** `automation/config/pilot-repo-config-template.yml`

**Structure:**

```yaml
repository:
  owner: "your-org"
  name: "pilot-repo-name"
  defaultBranch: "main"

customization:
  labels:
    "bug": "bug"
    "enhancement": "feature-request"
    # ... label mappings

  codeowners:
    exists: true
    path: ".github/CODEOWNERS"
    teams:
      - "@your-org/team-backend"

  stale:
    daysUntilStale: 60
    daysUntilClose: 7
    exemptLabels:
      - "pinned"
      - "security"

workflows:
  issueTriage:
    enabled: true
    priority: "P1"

  autoAssignReviewers:
    enabled: true
    priority: "P1"

  statusSync:
    enabled: true
    priority: "P2"

  staleManagement:
    enabled: true
    priority: "P2"

deployment:
  phase1:
    duration: "24 hours"
    mode: "passive"
    dryRun: true

  phase2:
    mode: "active"
    gradualActivation:
      - day: 1, workflows: ["issueTriage"]
      - day: 2, workflows: ["autoAssignReviewers"]
      - day: 3, workflows: ["statusSync"]
      - day: 4, workflows: ["staleManagement"]
```

______________________________________________________________________

## Deployment Process

### Phase 1: Selection & Preparation (Days 1-3)

**Day 1: Repository Evaluation**

1. Run evaluation script:

   ```bash
   ./setup_week6.sh --all <your-org>
   ```

1. Review results:

   ```bash
   cat <org>_repository_evaluation.json | jq '.[] | select(.totalScore >= 60)'
   ```

1. Select pilot repository (score ≥ 60, stakeholder agreement)

1. Create configuration:

   ```bash
   ./setup_week6.sh <owner/pilot-repo>
   ```

**Day 2: Customization**

1. Edit configuration file:

   ```bash
   code automation/config/pilot-<repo-name>-config.yml
   ```

1. Customize:

   - Map labels to repository conventions
   - Configure CODEOWNERS teams
   - Set stale detection parameters
   - Define workflow priorities
   - Add stakeholder information

1. Generate workflows:

   ```bash
   python3 automation/scripts/generate_pilot_workflows.py \
     automation/config/pilot-<repo-name>-config.yml
   ```

1. Review generated workflows in `generated_workflows/`

**Day 3: Pre-Deployment**

1. Create pilot branch in target repository:

   ```bash
   gh repo clone <owner/repo>
   cd <repo>
   git checkout -b workflow-automation-pilot
   ```

1. Copy workflows:

   ```bash
   mkdir -p .github/workflows
   cp ../generated_workflows/*.yml .github/workflows/
   ```

1. Add dry-run flags (Phase 1):

   - Add `if: false` to all action steps
   - Keep only logging steps active

1. Create PR:

   ```bash
   git add .github/workflows/
   git commit -m "feat: workflow automation pilot (Phase 1 - passive)"
   git push origin workflow-automation-pilot
   gh pr create --title "Workflow Automation Pilot - Phase 1" --draft
   ```

1. Announce to repository team (Slack, email)

### Phase 2: Passive Mode (Day 4)

**Duration:** 24 hours\
**Mode:** Observation only (dry-run)

1. **Deployment (2:00 PM UTC):**

   ```bash
   gh pr merge <pr-number> --squash --delete-branch
   ```

1. **Monitor every 6 hours:**

   - 2:00 PM, 8:00 PM, 2:00 AM, 8:00 AM
   - Check workflow executions
   - Review logs for correctness
   - Verify Slack notifications

1. **Go/No-Go Decision (next day 2:00 PM):**

   - All workflows executed without errors?
   - Logs show correct behavior?
   - No stakeholder concerns?
   - **Decision:** GO TO PHASE 3 / EXTEND PHASE 2 / ROLLBACK

### Phase 3: Active Mode - Gradual (Days 5-8)

**Day 5: Issue Triage Only**

1. Remove dry-run flag from `issue-triage.yml`
1. Deploy via PR
1. Monitor intensively (every 2 hours)
1. Collect metrics:
   - Issues triaged
   - Labels applied correctly (%)
   - False positives
   - Team feedback

**Day 6: Add Auto-Assign Reviewers**

1. Remove dry-run flag from `auto-assign-reviewers.yml`
1. Deploy via PR
1. Monitor intensively (every 2 hours)
1. Collect metrics:
   - PRs auto-assigned
   - Correct reviewers (%)
   - Team feedback

**Day 7: Add Status Sync**

1. Remove dry-run flag from `status-sync.yml`
1. Deploy via PR
1. Monitor normally (2x daily)
1. Collect metrics

**Day 8: Add Stale Management + Review**

1. Remove dry-run flag from `stale-management.yml`
1. Deploy via PR
1. Monitor normally (2x daily)
1. **End of Week Review (5:00 PM UTC):**
   - Technical metrics check
   - Team feedback collection
   - Retrospective
   - Monthly Review Meeting prep

______________________________________________________________________

## Monitoring and Metrics

### Intensive Monitoring (Phase 3 Days 1-2)

**Frequency:** Every 2 hours during business hours

**Checks:**

- [ ] Workflow execution count
- [ ] Success rate
- [ ] Error logs
- [ ] Slack notification delivery
- [ ] P1 response time (if applicable)
- [ ] Team feedback (ad-hoc)

**Alert Thresholds:**

- Any failure → immediate Slack alert
- Response time >30 min for P1 → escalate

### Normal Monitoring (Phase 3 Days 3-4)

**Frequency:** 2x daily (9 AM, 5 PM UTC)

**Checks:**

- [ ] Workflow execution count
- [ ] Success rate
- [ ] Error rate
- [ ] Cumulative metrics

**Alert Thresholds:**

- 2+ failures in 6 hours → investigate
- Response time >60 min for P1 → escalate

### Success Metrics

| Metric                | Target   | Timeframe   | Source          |
| --------------------- | -------- | ----------- | --------------- |
| Workflow Success Rate | >95%     | 3 days      | GitHub Actions  |
| Notification Delivery | >99%     | 3 days      | Slack logs      |
| P1 Response Time      | \<30 min | 3 days      | Manual tracking |
| Team Satisfaction     | >8.0/10  | End of week | Survey          |
| False Positives       | \<5%     | 3 days      | Manual review   |

______________________________________________________________________

## Rollback Procedure

### Trigger Conditions

- Workflow success rate \<90%
- Multiple critical failures
- Strongly negative team feedback
- Stakeholder request

### Immediate Rollback (\<5 minutes)

```bash
# Disable all workflows
gh workflow disable issue-triage.yml --repo <owner/repo>
gh workflow disable auto-assign-reviewers.yml --repo <owner/repo>
gh workflow disable status-sync.yml --repo <owner/repo>
gh workflow disable stale-management.yml --repo <owner/repo>
```

### Post-Rollback Actions

1. **Notify stakeholders** in #workflow-alerts
1. **Create incident issue** with rollback details
1. **Document root cause** within 24 hours
1. **Fix and plan re-attempt** (24-48 hours)

______________________________________________________________________

## Deliverables

### Documentation

- [ ] `automation/config/pilot-<repo-name>-config.yml` - Configuration
- [ ] `generated_workflows/*.yml` - Generated workflows
- [ ] `docs/WEEK6_PILOT_RESULTS.md` - Results summary
- [ ] `reports/week6-pilot-metrics.json` - Metrics data
- [ ] `reports/week6-survey-results.csv` - Survey responses

### Presentation Materials

- [ ] Monthly Review Meeting slides (10 slides)
- [ ] Live demo of pilot repository workflows
- [ ] Metrics dashboard screenshots
- [ ] Team feedback summary

______________________________________________________________________

## Troubleshooting

### Issue: Evaluation script fails to run

**Cause:** Missing GitHub CLI or insufficient permissions

**Solution:**

```bash
# Check gh is installed and authenticated
gh --version
gh auth status

# Re-authenticate if needed
gh auth login
```

### Issue: Generated workflows have syntax errors

**Cause:** Invalid configuration file format

**Solution:**

```bash
# Validate YAML syntax
yamllint automation/config/pilot-<repo>-config.yml

# Check required fields are present
python3 -c "import yaml; yaml.safe_load(open('pilot-config.yml'))"
```

### Issue: Workflows don't trigger in passive mode

**Cause:** Branch protection or webhook issues

**Solution:**

1. Check Actions are enabled: Repository Settings → Actions → Allow all actions
1. Verify webhook delivery: Settings → Webhooks → Recent Deliveries
1. Check workflow file syntax: `.github/workflows/<workflow>.yml`

### Issue: Slack notifications not delivered

**Cause:** Missing or incorrect webhook secret

**Solution:**

```bash
# Verify secret exists
gh secret list --repo <owner/repo>

# Update secret if needed
gh secret set SLACK_WEBHOOK_ALERTS --repo <owner/repo>
```

______________________________________________________________________

## Next Steps After Week 6

### Week 7-8: Enhancements (if pilot successful)

Based on Week 6 results:

1. **Expand to 2-3 more repositories** using lessons learned
1. **Implement A/B test** for stale grace period (7 vs 10 days)
1. **Add dashboard enhancements** (trends, heatmaps)
1. **Launch email digest** feature for stakeholders
1. **Begin predictive analytics** research

### Documentation to Create

- [ ] Expansion playbook (template for future pilots)
- [ ] Customization guide (common patterns)
- [ ] Troubleshooting guide (expand with new issues)
- [ ] Best practices document (lessons learned)

______________________________________________________________________

## Resources

### Reference Documentation

- WEEK6_REPOSITORY_EXPANSION_GUIDE.md - Original planning guide
- WEEK6_DEPLOYMENT_CHECKLIST.md - Detailed checklist
- [PRODUCTION_WORKFLOW_INTEGRATION.md](../workflows/PRODUCTION_WORKFLOW_INTEGRATION.md)
  \- Integration patterns
- [SLACK_INTEGRATION_TRAINING.md](SLACK_INTEGRATION_TRAINING.md) - Training
  materials

### Tools

- [evaluate_repository.py](../../src/automation/scripts/evaluate_repository.py)
  \- Evaluation script
- [generate_pilot_workflows.py](../../src/automation/scripts/generate_pilot_workflows.py)
  \- Generator script
- setup_week6.sh - Quick setup script

### Templates

- [pilot-repo-config-template.yml](../../src/automation/config/pilot-repo-config-template.yml)
  \- Configuration template

______________________________________________________________________

## Quick Reference

### Commands

```bash
# Evaluate repository
python3 automation/scripts/evaluate_repository.py <owner/repo>

# Create configuration
./setup_week6.sh <owner/repo>

# Generate workflows
python3 automation/scripts/generate_pilot_workflows.py automation/config/pilot-config.yml

# Create pilot branch
gh repo clone <owner/repo>
cd <repo> && git checkout -b workflow-automation-pilot

# Deploy to pilot
gh pr create --title "Workflow Automation Pilot" --draft
gh pr merge <pr-number> --squash --delete-branch

# Monitor workflows
gh run list --repo <owner/repo> --limit 20

# Disable workflow (rollback)
gh workflow disable <workflow-name>.yml --repo <owner/repo>
```

### Key Contacts

- **Deployment Lead:** @workflow-team
- **Escalation:** #workflow-alerts (Slack)
- **Questions:** #pilot-<repo-name> (Slack)

______________________________________________________________________

_Week 6 Implementation Guide v1.0 - Created 2026-02-22_
