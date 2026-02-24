#!/bin/bash
# Week 11 Phase 2 Deployment Script
# This script deploys labels and workflows to 5 additional repositories
#
# Security: All scripts use 1Password CLI for secure token retrieval.
# Tokens are only in memory during execution, never written to disk.

set -e  # Exit on any error

echo "=================================================="
echo "Week 11 Phase 2 Deployment"
echo "=================================================="
echo ""
echo "📊 Status Check:"
echo "   Phase 1: ✅ Complete (3 repositories)"
echo "   Phase 2: 🚀 Deploying (5 repositories)"
echo ""
echo "🔐 Scripts will securely retrieve GitHub token from:"
echo "   1Password CLI ONLY (item: master-org-token-011726)"
echo ""
echo "Prerequisites:"
echo "  1. Phase 1 completed and validated (48h monitoring)"
echo "  2. 1Password CLI authenticated"
echo "  3. GitHub token (master-org-token-011726) accessible"
echo ""

# Verify Phase 1 results exist
if [ ! -f "/workspace/results/week11-phase1-production.json" ]; then
    echo "❌ Phase 1 results not found. Complete Phase 1 first."
    exit 1
fi

echo "✅ Phase 1 results verified"
echo ""

cd /workspace/automation/scripts

# Step 1: Deploy labels automatically
echo "📋 Step 1: Deploying labels to 5 repositories..."
echo ""
python3 validate_labels.py \
  --config ../config/batch-onboard-week11-phase2-expansion.yml \
  --fix

echo ""
echo "✅ Labels deployed!"
echo ""

# Step 2: Verify all prerequisites
echo "🔍 Step 2: Running pre-deployment checklist..."
echo ""
python3 pre_deployment_checklist.py --phase 2

echo ""
echo "=================================================="
echo "✅ Pre-deployment checks passed!"
echo "=================================================="
echo ""

# Step 3: Deploy workflows
echo "🚀 Step 3: Deploying workflows to repositories..."
echo ""
python3 batch_onboard_repositories.py \
  --config ../config/batch-onboard-week11-phase2-expansion.yml \
  --output week11-phase2-production.json

echo ""
echo "=================================================="
echo "🎉 Phase 2 Deployment Complete!"
echo "=================================================="
echo ""
echo "Results saved to: week11-phase2-production.json"
echo ""
echo "Deployment Summary:"
echo "  Phase 1: 3 repositories ✅"
echo "  Phase 2: 5 repositories ✅"
echo "  Total:   8/12 repositories operational"
echo ""
echo "Next steps:"
echo "  1. Monitor repositories for 48 hours"
echo "  2. Verify workflow executions"
echo "  3. Proceed to Phase 3 after validation"
