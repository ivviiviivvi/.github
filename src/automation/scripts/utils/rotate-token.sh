#!/bin/bash
# Token rotation automation
# Usage: ./rotate-token.sh <token-name>

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TOKEN_NAME="${1:-}"
if [[ -z "$TOKEN_NAME" ]]; then
    echo -e "${RED}Error: Token name required${NC}"
    echo ""
    echo "Usage: $0 <token-name>"
    echo ""
    echo "Available tokens:"
    echo "  - org-label-sync-token"
    echo "  - org-project-admin-token"
    echo "  - org-repo-analysis-token"
    echo "  - org-onboarding-token"
    echo ""
    echo "Example: $0 org-label-sync-token"
    exit 1
fi

echo -e "${BLUE}🔄 Rotating token: ${TOKEN_NAME}${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get token information from TOKEN_REGISTRY.md
echo -e "${YELLOW}📋 Token Information:${NC}"
echo ""
echo "Please refer to docs/TOKEN_REGISTRY.md for required scopes:"
echo "  - org-label-sync-token: repo, workflow"
echo "  - org-project-admin-token: project, read:org"
echo "  - org-repo-analysis-token: repo:status, read:org"
echo "  - org-onboarding-token: repo, workflow, admin:org"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Generate new token
echo -e "${YELLOW}Step 1: Generate new token${NC}"
echo ""
echo "1. Go to: https://github.com/settings/tokens/new"
echo "2. Token name: ${TOKEN_NAME}-$(date +%Y%m%d)"
echo "3. Expiration: Match rotation schedule (see TOKEN_REGISTRY.md)"
echo "4. Select required scopes (see above)"
echo "5. Click 'Generate token' and copy it"
echo ""
read -p "Press Enter when you have the new token copied..."

# Step 2: Store in 1Password
echo ""
echo -e "${YELLOW}Step 2: Store in 1Password${NC}"
echo ""

# Check if 1Password CLI is authenticated
if ! op account list &>/dev/null; then
    echo -e "${RED}Error: 1Password CLI not authenticated${NC}"
    echo "Please run: eval \$(op signin)"
    exit 1
fi

# Check if item exists
if op item get "$TOKEN_NAME" --vault Personal &>/dev/null; then
    echo -e "${GREEN}✓${NC} Found existing item: ${TOKEN_NAME}"
    echo ""
    read -sp "Enter new token value: " NEW_TOKEN
    echo ""

    if [[ -z "$NEW_TOKEN" ]]; then
        echo -e "${RED}Error: Token value cannot be empty${NC}"
        exit 1
    fi

    # Update existing item
    echo -e "${BLUE}Updating 1Password item...${NC}"
    if op item edit "$TOKEN_NAME" "password=$NEW_TOKEN" --vault Personal &>/dev/null; then
        echo -e "${GREEN}✓${NC} Token updated in 1Password"
    else
        echo -e "${RED}Error: Failed to update 1Password item${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠${NC}  Item not found. Creating new item: ${TOKEN_NAME}"
    echo ""
    read -sp "Enter token value: " NEW_TOKEN
    echo ""

    if [[ -z "$NEW_TOKEN" ]]; then
        echo -e "${RED}Error: Token value cannot be empty${NC}"
        exit 1
    fi

    # Create new item
    echo -e "${BLUE}Creating 1Password item...${NC}"
    if op item create \
        --category "Password" \
        --title "$TOKEN_NAME" \
        --vault "Personal" \
        "password=$NEW_TOKEN" &>/dev/null; then
        echo -e "${GREEN}✓${NC} Token created in 1Password"
    else
        echo -e "${RED}Error: Failed to create 1Password item${NC}"
        exit 1
    fi
fi

# Step 3: Test new token
echo ""
echo -e "${YELLOW}Step 3: Test new token${NC}"
echo ""

# Retrieve token
echo -e "${BLUE}Retrieving token from 1Password...${NC}"
GH_TOKEN=$(op read "op://Personal/${TOKEN_NAME}/password" --reveal 2>/dev/null)

if [[ -z "$GH_TOKEN" ]]; then
    echo -e "${RED}Error: Failed to retrieve token${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Token retrieved (${#GH_TOKEN} characters)"

# Test authentication
echo -e "${BLUE}Testing authentication...${NC}"
RESPONSE=$(curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/user)

if echo "$RESPONSE" | jq -e '.login' &>/dev/null; then
    USERNAME=$(echo "$RESPONSE" | jq -r '.login')
    echo -e "${GREEN}✓${NC} Authentication successful: @${USERNAME}"

    # Check scopes
    SCOPES=$(curl -s -I -H "Authorization: token $GH_TOKEN" https://api.github.com/user | grep -i 'x-oauth-scopes' | cut -d' ' -f2- | tr -d '\r')
    if [[ -n "$SCOPES" ]]; then
        echo -e "${GREEN}✓${NC} Token scopes: ${SCOPES}"
    fi
else
    echo -e "${RED}Error: Authentication failed${NC}"
    echo "$RESPONSE" | jq -r '.message' 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

# Step 4: Dry-run test (if applicable)
echo ""
echo -e "${YELLOW}Step 4: Dry-run test${NC}"
echo ""

case "$TOKEN_NAME" in
    "org-label-sync-token")
        echo "Testing label sync script..."
        if python3 automation/scripts/sync_labels.py --dry-run 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Label sync dry-run successful"
        else
            echo -e "${YELLOW}⚠${NC}  Could not run dry-run test (script may need updates)"
        fi
        ;;
    "org-repo-analysis-token")
        echo "Testing web crawler script..."
        if python3 automation/scripts/web_crawler.py --help &>/dev/null; then
            echo -e "${GREEN}✓${NC} Web crawler script accessible"
        else
            echo -e "${YELLOW}⚠${NC}  Could not verify web crawler script"
        fi
        ;;
    "org-project-admin-token")
        echo "Testing project setup script..."
        if [[ -f scripts/configure-github-projects.py ]]; then
            echo -e "${GREEN}✓${NC} Project setup script found"
        else
            echo -e "${YELLOW}⚠${NC}  Project setup script not found"
        fi
        ;;
    "org-onboarding-token")
        echo "Testing onboarding script..."
        if [[ -f automation/scripts/batch_onboard_repositories.py ]]; then
            echo -e "${GREEN}✓${NC} Onboarding script found"
        else
            echo -e "${YELLOW}⚠${NC}  Onboarding script not found"
        fi
        ;;
    *)
        echo -e "${YELLOW}⚠${NC}  Unknown token type - skipping dry-run test"
        ;;
esac

# Step 5: Summary and next steps
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅ Token rotation complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Monitor logs for authentication errors (next 24 hours)"
echo "2. Revoke old token in 24-48 hours:"
echo "   → https://github.com/settings/tokens"
echo "3. Update TOKEN_REGISTRY.md:"
echo "   → Update 'Last Rotated' date"
echo "   → Update 'Expiration' date"
echo "   → Add entry to Audit Log section"
echo "4. Commit changes:"
echo "   → git add docs/TOKEN_REGISTRY.md"
echo "   → git commit -m 'chore: rotate ${TOKEN_NAME}'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Clear sensitive variable
unset GH_TOKEN
unset NEW_TOKEN
