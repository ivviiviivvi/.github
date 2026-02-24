#!/bin/bash
# Quick deployment - just needs token from 1Password
set -e

cd "$(dirname "$0")"

echo "════════════════════════════════════════════════════════"
echo "  GitHub Projects Deployment"
echo "════════════════════════════════════════════════════════"
echo ""
echo "1Password Share Link:"
echo "https://share.1password.com/s#QgANMqAHCG-UZynAwiu20zbZCgS0GqQPG8-yf_vnmbc"
echo ""
echo "Please open the link above, copy the token, and paste it here:"
echo ""
read -s -p "GitHub PAT (starts with ghp_): " GH_TOKEN
echo ""
echo ""

# Validate token format
if [[ ! "$GH_TOKEN" =~ ^ghp_ ]]; then
    echo "❌ Token should start with 'ghp_'"
    echo "Please check the token and try again"
    exit 1
fi

export GH_TOKEN

echo "✅ Token validated"
echo ""
echo "Running deployment to {{ORG_NAME}} organization..."
echo ""

# Deploy
python3 configure-github-projects.py --org {{ORG_NAME}} 2>&1 | tee "deployment-$(date +%Y%m%d-%H%M%S).log"

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. View projects: https://github.com/orgs/{{ORG_NAME}}/projects"
echo "  2. Configure views (see ../docs/GITHUB_PROJECTS_DEPLOYMENT.md)"
echo "  3. Set up automation rules"
echo "════════════════════════════════════════════════════════"
