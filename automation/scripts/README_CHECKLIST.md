# Pre-Deployment Checklist Script

## Overview

`pre_deployment_checklist.py` is a comprehensive validation tool that verifies all prerequisites are met before executing workflow deployment. It performs 8 critical checks to ensure smooth deployment.

## Features

- ✅ **Configuration Validation**: Verify config files exist and are valid YAML
- 🔐 **Authentication Check**: Ensure GitHub CLI is authenticated
- 📦 **Dependency Verification**: Check Python packages are installed
- 📄 **Template Validation**: Confirm workflow templates exist
- 🔑 **Access Control**: Verify repository permissions
- 🏷️ **Label Verification**: Check labels are deployed (optional)
- 📊 **Phase Prerequisites**: Validate previous phases completed
- 🎯 **Exit Codes**: Return 0 on success, 1 on failure for scripting

## Usage

### Basic Check (Phase 1)

```bash
cd /workspace/automation/scripts
python3 pre_deployment_checklist.py --phase 1
```

**Example Output:**

```
🔍 Running pre-deployment checks for Phase 1...
================================================================================

✅ Configuration File: Found batch-onboard-week11-phase1-pilot.yml
✅ Configuration Valid: Configuration parsed successfully
✅ GitHub CLI: Authenticated and ready
✅ Python Dependencies: All required packages installed (pyyaml)
✅ Workflow Templates: All 3 workflow templates found
✅ Repository Access: All 3 repositories accessible
❌ Label Deployment: 1/3 repositories missing labels
   theoretical-specifications-first (missing 4 labels)
✅ Phase Prerequisites: Phase 1 is initial deployment

================================================================================
❌ 1 CHECK(S) FAILED (7/8 passed)

Fix the issues above before deploying.

💡 To deploy labels automatically:
   python3 validate_labels.py --config batch-onboard-week11-phase1-pilot.yml --fix
```

### Verbose Mode

Show detailed information for each check:

```bash
python3 pre_deployment_checklist.py --phase 1 --verbose
```

### Skip Label Validation

Useful for testing configuration without requiring labels:

```bash
python3 pre_deployment_checklist.py --phase 1 --skip-labels
```

### Check All Phases

```bash
# Phase 1
python3 pre_deployment_checklist.py --phase 1

# Phase 2
python3 pre_deployment_checklist.py --phase 2

# Phase 3
python3 pre_deployment_checklist.py --phase 3
```

## Validation Checks

### 1. Configuration File Exists

Verifies the phase-specific configuration file exists:
- Phase 1: `batch-onboard-week11-phase1-pilot.yml`
- Phase 2: `batch-onboard-week11-phase2-expansion.yml`
- Phase 3: `batch-onboard-week11-phase3-final.yml`

### 2. Configuration Valid

Checks:
- Valid YAML syntax
- Required keys present (`repositories`, `workflows`, `labels`)
- Configuration can be parsed

### 3. GitHub CLI Installed and Authenticated

Verifies:
- `gh` command is in PATH
- User is authenticated with GitHub
- Can execute GitHub API calls

### 4. Python Dependencies

Ensures required packages are installed:
- `pyyaml` for configuration parsing

### 5. Workflow Templates Exist

Checks that all workflow files referenced in config exist in:
- `automation/workflow-templates/`
- `workflow-templates/`
- `.github/workflows/`

### 6. Repository Access

Verifies:
- All target repositories are accessible
- User has read permissions
- Repositories exist

### 7. Labels Deployed

For each repository, checks:
- All required labels exist
- Labels are accessible via GitHub API

**Note**: Can be skipped with `--skip-labels` flag.

### 8. Phase Prerequisites

Validates:
- Phase 1: No prerequisites (initial deployment)
- Phase 2: Phase 1 should be verified manually as stable
- Phase 3: Phase 2 should be verified manually as stable

## Integration with Deployment Workflow

### Pre-Deployment Gate

Use as a gate before deployment:

```bash
#!/bin/bash
# deploy-phase1.sh

echo "🔍 Running pre-deployment checks..."
if python3 pre_deployment_checklist.py --phase 1; then
  echo "✅ All checks passed"
  echo "🚀 Starting deployment..."
  python3 batch_onboard_repositories.py \
    --config ../config/batch-onboard-week11-phase1-pilot.yml \
    --output week11-phase1-production.json
else
  echo "❌ Pre-deployment checks failed"
  echo "Fix the issues above before deploying."
  exit 1
fi
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Pre-deployment validation
  run: |
    cd automation/scripts
    python3 pre_deployment_checklist.py --phase 1
  
- name: Deploy workflows
  if: success()
  run: |
    cd automation/scripts
    python3 batch_onboard_repositories.py \
      --config ../config/batch-onboard-week11-phase1-pilot.yml
```

### Complete Workflow

```bash
# Full deployment pipeline
for phase in 1 2 3; do
  echo "=== Phase $phase ==="
  
  # Pre-flight checks
  if ! python3 pre_deployment_checklist.py --phase $phase; then
    echo "Phase $phase checks failed. Stopping."
    exit 1
  fi
  
  # Deploy
  python3 batch_onboard_repositories.py \
    --config "../config/batch-onboard-week11-phase${phase}-*.yml"
  
  # Verify
  echo "Phase $phase deployed. Verify before continuing."
  read -p "Press Enter to continue to next phase..."
done
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--phase N` | Deployment phase to validate (1, 2, or 3) - **Required** |
| `--skip-labels` | Skip label deployment validation |
| `--verbose` or `-v` | Show detailed output for each check |

## Exit Codes

- **0**: All checks passed - safe to deploy
- **1**: One or more checks failed - do not deploy

Use in scripts:

```bash
if python3 pre_deployment_checklist.py --phase 1; then
  # Proceed with deployment
  deploy_workflows
else
  # Alert and stop
  send_alert "Pre-deployment checks failed"
  exit 1
fi
```

## Troubleshooting

### GitHub CLI Not Authenticated

```
❌ GitHub CLI: Not authenticated
   Run: gh auth login
```

**Solution**: Run `gh auth login` and follow prompts.

### Configuration File Missing

```
❌ Configuration File: Missing batch-onboard-week11-phase1-pilot.yml
   Expected at: /workspace/automation/config/...
```

**Solution**: Ensure you're running from correct directory or config file exists.

### Repository Access Denied

```
❌ Repository Access: 1/3 repositories inaccessible
   Cannot access: owner/private-repo
```

**Solution**: Check repository exists and you have read permissions.

### Labels Not Deployed

```
❌ Label Deployment: 2/3 repositories missing labels
   theoretical-specifications-first (missing 4 labels)
   trade-perpetual-future (missing 2 labels)
```

**Solutions**:

1. **Auto-fix**: `python3 validate_labels.py --config ... --fix`
2. **Manual**: Deploy via Web UI (see manual deployment guide)
3. **Skip**: Use `--skip-labels` flag (not recommended for production)

### Workflow Templates Missing

```
❌ Workflow Templates: 1 workflow(s) not found
   Missing: enhanced-pr-quality.yml
```

**Solution**: Verify workflow template files exist in expected directories.

## Requirements

- **Python 3.8+**
- **pyyaml** package (`pip install pyyaml`)
- **GitHub CLI** (`gh`) installed and authenticated
- **Repository access** to target repositories

## See Also

- [validate_labels.py](README_VALIDATION.md) - Label validation and deployment
- [batch_onboard_repositories.py](../../docs/WEEK_11_PHASE1_STATUS.md) - Main deployment script
- [WEEK_11_DEPLOYMENT_READINESS.md](../../docs/WEEK_11_DEPLOYMENT_READINESS.md) - Complete deployment plan
- [WEEK_11_NEXT_STEPS_QUICK_REF.md](../../docs/WEEK_11_NEXT_STEPS_QUICK_REF.md) - Quick reference guide

## Examples

### Quick Check Before Deployment

```bash
# Validate everything is ready
python3 pre_deployment_checklist.py --phase 1 && \
  python3 batch_onboard_repositories.py \
    --config ../config/batch-onboard-week11-phase1-pilot.yml
```

### Check All Phases at Once

```bash
#!/bin/bash
echo "Validating all phases..."
for phase in 1 2 3; do
  echo ""
  echo "=== Phase $phase ==="
  python3 pre_deployment_checklist.py --phase $phase --skip-labels
done
```

### Verbose Check with Label Validation

```bash
# Get detailed information about each check
python3 pre_deployment_checklist.py --phase 1 --verbose
```
