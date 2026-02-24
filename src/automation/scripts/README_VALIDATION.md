# Label Validation Script

## Overview

`validate_labels.py` is a pre-flight validation tool that checks whether all
required labels exist in target repositories before attempting workflow
deployment. This helps catch label-related issues early and provides an
automated way to create missing labels.

## Features

- ✅ **Validation Mode**: Check if all required labels exist with correct colors
- 🔧 **Fix Mode**: Automatically create or update missing/mismatched labels
- 📊 **Detailed Reporting**: Show status for each repository and label
- 🚀 **Pre-deployment Check**: Integrate into deployment workflow

## Usage

### Basic Validation

Check if labels exist in Phase 1 repositories:

```bash
cd /workspace/automation/scripts
python3 validate_labels.py --config ../config/batch-onboard-week11-phase1-pilot.yml
```

**Example Output:**

```
📋 Validating 12 labels across 3 repositories
👀 VALIDATION MODE

🔍 Validating {{ORG_NAME}}/theoretical-specifications-first...
  ✅ Found: week11/phase1
  ✅ Found: priority/critical
  ✅ Found: priority/high
  ❌ Missing: priority/medium
  ❌ Missing: priority/low
  ...
❌ 4 label issues found in {{ORG_NAME}}/theoretical-specifications-first

================================================================================
📊 VALIDATION SUMMARY
================================================================================
❌ FAIL {{ORG_NAME}}/theoretical-specifications-first           (4 issues)
✅ PASS {{ORG_NAME}}/system-governance-framework                (0 issues)
❌ FAIL {{ORG_NAME}}/trade-perpetual-future                     (2 issues)
================================================================================
❌ 2/3 repositories have label issues

💡 Tip: Run with --fix to automatically create/update labels
```

### Auto-Fix Mode

Automatically create or update labels:

```bash
python3 validate_labels.py \
  --config ../config/batch-onboard-week11-phase1-pilot.yml \
  --fix
```

**Example Output:**

```
📋 Validating 12 labels across 3 repositories
🔧 FIX MODE ENABLED

🔍 Validating {{ORG_NAME}}/theoretical-specifications-first...
  ❌ Missing: priority/medium
  ❌ Missing: priority/low

🔧 Fixing labels in {{ORG_NAME}}/theoretical-specifications-first...
  ✅ Created: priority/medium
  ✅ Created: priority/low
✅ All 12 labels validated for {{ORG_NAME}}/theoretical-specifications-first
...

================================================================================
✅ All repositories validated successfully!
```

## Integration with Deployment

### Pre-Deployment Validation

Before running the production deployment, validate labels:

```bash
# Validate Phase 1
python3 validate_labels.py \
  --config ../config/batch-onboard-week11-phase1-pilot.yml

# If validation passes, proceed with deployment
if [ $? -eq 0 ]; then
  python3 batch_onboard_repositories.py \
    --config ../config/batch-onboard-week11-phase1-pilot.yml \
    --output week11-phase1-production.json
fi
```

### Automated Label Creation

If you have appropriate permissions (PAT with `issues: write`):

```bash
# Create all missing labels automatically
python3 validate_labels.py \
  --config ../config/batch-onboard-week11-phase1-pilot.yml \
  --fix
```

## Configuration Format

The script reads labels from the same config files used by
`batch_onboard_repositories.py`:

```yaml
repositories:
  - "owner/repo1"
  - "owner/repo2"

labels:
  - name: "week11/phase1"
    color: "0E8A16"
    description: "Week 11 Phase 1 deployment"
  - name: "priority/critical"
    color: "d73a4a"
    description: "Critical priority"
  # ... more labels
```

## Exit Codes

- **0**: All validations passed
- **1**: One or more repositories have label issues

Use exit codes for scripting:

```bash
if python3 validate_labels.py --config ../config/phase1.yml; then
  echo "✅ Ready to deploy"
else
  echo "❌ Fix labels before deploying"
  exit 1
fi
```

## Validation Checks

The script validates:

1. **Label Existence**: Does the label exist in the repository?
1. **Color Match**: Does the color match the specification?
1. **Name Match**: Exact name matching (case-sensitive)

**Note**: Description mismatches are not considered errors (descriptions can be
updated without breaking functionality).

## Examples

### Check All Three Phases

```bash
# Phase 1 (3 repos)
python3 validate_labels.py --config ../config/batch-onboard-week11-phase1-pilot.yml

# Phase 2 (5 repos)
python3 validate_labels.py --config ../config/batch-onboard-week11-phase2-expansion.yml

# Phase 3 (4 repos)
python3 validate_labels.py --config ../config/batch-onboard-week11-phase3-final.yml
```

### Quick Fix All Phases

```bash
# Fix all phases at once
for phase in phase1-pilot phase2-expansion phase3-final; do
  echo "🔧 Fixing batch-onboard-week11-${phase}..."
  python3 validate_labels.py \
    --config ../config/batch-onboard-week11-${phase}.yml \
    --fix || echo "⚠️ Some labels failed for ${phase}"
done
```

### Validate Before Production

```bash
#!/bin/bash
# pre-deploy-check.sh

CONFIG="../config/batch-onboard-week11-phase1-pilot.yml"

echo "🔍 Validating labels..."
if python3 validate_labels.py --config "$CONFIG"; then
  echo "✅ Validation passed"
  echo "🚀 Starting deployment..."
  python3 batch_onboard_repositories.py --config "$CONFIG"
else
  echo "❌ Validation failed"
  echo "💡 Run with --fix to create missing labels:"
  echo "   python3 validate_labels.py --config $CONFIG --fix"
  exit 1
fi
```

## Troubleshooting

### GitHub CLI Not Authenticated

```
Error fetching labels from owner/repo: gh: must be authenticated
```

**Solution**: Authenticate with GitHub CLI:

```bash
gh auth login
```

### Permission Denied

```
Error creating label priority/high in owner/repo: HTTP 403
```

**Solution**: Ensure you have `issues: write` permission. Options:

1. Create a fine-grained PAT with `issues: write` permission
1. Use organization admin account
1. Deploy labels manually via Web UI (fallback)

### Label Already Exists

The script uses `--force` flag with `gh label create`, which updates existing
labels instead of failing. This is safe and ensures labels match specifications.

## Requirements

- **GitHub CLI** (`gh`) installed and authenticated
- **Python 3.8+** with `pyyaml` package
- **Repository access** with appropriate permissions

## See Also

- [WEEK_11_PHASE1_MANUAL_DEPLOYMENT_GUIDE.md](../../../docs/guides/WEEK_11_PHASE1_MANUAL_DEPLOYMENT_GUIDE.md)
  \- Manual label deployment via Web UI
- [WEEK_11_NEXT_STEPS_QUICK_REF.md](../../../docs/reports/WEEK_11_NEXT_STEPS_QUICK_REF.md)
  \- Quick reference for deployment
- [batch_onboard_repositories.py](batch_onboard_repositories.py) - Main
  deployment script
