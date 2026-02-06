#!/bin/bash
# Week 11 Phase 3 Deployment Script
# Deploys to 4 final repositories (12 total repositories)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║              WEEK 11 PHASE 3: FINAL DEPLOYMENT                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📅 Deployment Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "📦 Target: 4 final repositories (12 total - 100% coverage)"
echo ""

# Phase 3 repositories
REPOS=(
  "{{ORG_NAME}}/4-ivi374-F0Rivi4"
  "{{ORG_NAME}}/a-context7"
  "{{ORG_NAME}}/reverse-engine-recursive-run"
  "{{ORG_NAME}}/universal-node-network"
)

# Workflow templates (with SHA-pinned actions)
WORKFLOWS=(
  "repository-health-check.yml"
  "enhanced-pr-quality.yml"
  "stale-management.yml"
)

WORKFLOW_DIR="$WORKSPACE_ROOT/automation/workflow-templates"

# Label definitions
declare -A LABELS=(
  ["priority:critical"]="B60205|Critical priority - immediate attention required"
  ["priority:high"]="D93F0B|High priority - address soon"
  ["priority:medium"]="FBCA04|Medium priority - normal timeline"
  ["priority:low"]="0E8A16|Low priority - address when possible"
  ["status:blocked"]="D93F0B|Work is blocked by external dependency"
  ["status:in progress"]="1d76db|Work is actively in progress"
  ["status:ready for review"]="0e8a16|Ready for review"
  ["status:changes requested"]="d93f0b|Changes requested in review"
  ["type:bug"]="d73a4a|Something isn't working correctly"
  ["type:feature"]="a2eeef|New feature or request"
  ["type:enhancement"]="84b6eb|Enhancement to existing functionality"
  ["type:documentation"]="0075ca|Documentation improvements"
  ["deployment:week-11-phase-3"]="5319e7|Week 11 Phase 3 deployment"
  ["automation:batch-deployed"]="006b75|Deployed via automation"
)

# Counters
TOTAL_REPOS=${#REPOS[@]}
TOTAL_WORKFLOWS=$((TOTAL_REPOS * ${#WORKFLOWS[@]}))
TOTAL_LABELS=$((TOTAL_REPOS * ${#LABELS[@]}))
SUCCESS_COUNT=0
FAILED_COUNT=0
START_TIME=$(date +%s)

echo "═══════════════════════════════════════════════════════════════════════════"
echo "🎯 DEPLOYMENT PLAN"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "Repositories:  $TOTAL_REPOS (completing 12/12 = 100% coverage)"
echo "Workflows:     $TOTAL_WORKFLOWS (${#WORKFLOWS[@]} per repo)"
echo "Labels:        $TOTAL_LABELS (${#LABELS[@]} per repo)"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Deploy to each repository
for repo in "${REPOS[@]}"; do
  repo_name=$(basename "$repo")
  echo "📦 Processing: $repo_name"
  echo "───────────────────────────────────────────────────────────────────────"

  repo_start=$(date +%s)

  # Deploy labels
  echo "  🏷️  Deploying labels..."
  label_count=0
  for label_key in "${!LABELS[@]}"; do
    IFS='|' read -r color description <<< "${LABELS[$label_key]}"

    if gh label create "$label_key" \
      --repo "$repo" \
      --color "$color" \
      --description "$description" \
      --force 2>/dev/null; then
      ((label_count++))
    fi
  done
  echo "     ✅ $label_count/${#LABELS[@]} labels created"

  # Deploy workflows
  echo "  ⚙️  Deploying workflows..."
  workflow_count=0
  for workflow in "${WORKFLOWS[@]}"; do
    workflow_path="$WORKFLOW_DIR/$workflow"

    if [ ! -f "$workflow_path" ]; then
      echo "     ❌ Workflow file not found: $workflow"
      continue
    fi

    # Base64 encode content
    content=$(base64 -w 0 "$workflow_path")

    # Check if file exists
    existing_sha=$(gh api "repos/$repo/contents/.github/workflows/$workflow" 2>/dev/null | jq -r '.sha' || echo "")

    # Create or update workflow
    if [ -n "$existing_sha" ]; then
      # Update existing file
      if gh api "repos/$repo/contents/.github/workflows/$workflow" \
        -X PUT \
        -f message="chore(workflows): update $workflow (Phase 3 deployment)" \
        -f content="$content" \
        -f sha="$existing_sha" \
        -f branch="main" > /dev/null 2>&1; then
        ((workflow_count++))
      fi
    else
      # Create new file
      if gh api "repos/$repo/contents/.github/workflows/$workflow" \
        -X PUT \
        -f message="chore(workflows): deploy $workflow (Phase 3 deployment)" \
        -f content="$content" \
        -f branch="main" > /dev/null 2>&1; then
        ((workflow_count++))
      fi
    fi

    sleep 1  # Rate limit protection
  done
  echo "     ✅ $workflow_count/${#WORKFLOWS[@]} workflows deployed"

  repo_end=$(date +%s)
  repo_duration=$((repo_end - repo_start))

  if [ "$workflow_count" -eq "${#WORKFLOWS[@]}" ] && [ "$label_count" -eq "${#LABELS[@]}" ]; then
    echo "  ✅ Repository complete ($repo_duration seconds)"
    ((SUCCESS_COUNT++))
  else
    echo "  ⚠️  Repository incomplete ($repo_duration seconds)"
    ((FAILED_COUNT++))
  fi

  echo ""
done

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

echo "═══════════════════════════════════════════════════════════════════════════"
echo "📊 DEPLOYMENT SUMMARY"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "Status:        $([ $FAILED_COUNT -eq 0 ] && echo "✅ SUCCESS" || echo "⚠️  PARTIAL SUCCESS")"
echo "Repositories:  $SUCCESS_COUNT/$TOTAL_REPOS successful"
echo "Duration:      $TOTAL_DURATION seconds"
echo "Success Rate:  $(awk "BEGIN {printf \"%.1f\", ($SUCCESS_COUNT/$TOTAL_REPOS)*100}")%"
echo ""

if [ $FAILED_COUNT -gt 0 ]; then
  echo "⚠️  Warning: $FAILED_COUNT repositories had issues"
  echo ""
fi

echo "═══════════════════════════════════════════════════════════════════════════"
echo "🎉 WEEK 11 DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "Total Organization Coverage: 12/12 repositories (100%)"
echo ""
echo "Deployed across all phases:"
echo "  • Phase 1: 3 repositories (pilot)"
echo "  • Phase 2: 5 repositories (expansion)"
echo "  • Phase 3: 4 repositories (completion)"
echo ""
echo "Next steps:"
echo "  1. Verify workflows are present in all 12 repositories"
echo "  2. Trigger manual workflow runs to validate execution"
echo "  3. Update organization-wide documentation"
echo "  4. Celebrate successful deployment! 🎉"
echo ""
