#!/bin/bash
# One-command deployment using GitHub CLI token
# Usage: ./deploy.sh [--dry-run]

set -e

cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}GitHub Projects Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if GitHub CLI is authenticated
if ! gh auth status &>/dev/null; then
    echo -e "${YELLOW}⚠${NC} GitHub CLI not authenticated"
    echo "Run: gh auth login"
    exit 1
fi

# Get token from GitHub CLI
export GH_TOKEN=$(gh auth token)
echo -e "${GREEN}✓${NC} Token retrieved from GitHub CLI"

# Determine mode
if [[ "$1" == "--dry-run" ]]; then
    echo -e "${YELLOW}⚠${NC} DRY RUN MODE (no changes will be made)"
    echo ""
    python3 configure-github-projects.py --org {{ORG_NAME}} --dry-run
else
    echo -e "${GREEN}✓${NC} Deploying to organization: {{ORG_NAME}}"
    echo ""

    # Create log file
    LOG_FILE="deployment-$(date +%Y%m%d-%H%M%S).log"

    # Run deployment
    python3 configure-github-projects.py --org {{ORG_NAME}} 2>&1 | tee "$LOG_FILE"

    echo ""
    echo -e "${GREEN}✓${NC} Deployment complete! Log saved to: $LOG_FILE"
    echo ""
    echo "Next steps:"
    echo "  1. View projects: https://github.com/orgs/{{ORG_NAME}}/projects"
    echo "  2. Configure views (see GITHUB_PROJECTS_DEPLOYMENT.md)"
    echo "  3. Set up automation rules"
    echo ""
fi
