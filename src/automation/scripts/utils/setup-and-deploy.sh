#!/bin/bash
# Interactive token setup and deployment
# This script guides you through the token setup process

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     GitHub Projects - Token Setup & Deploy        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if token already set
if [[ -n "$GH_TOKEN" ]] && [[ "$GH_TOKEN" == ghp_* ]]; then
    echo -e "${GREEN}✓${NC} Personal Access Token detected in GH_TOKEN"
    echo ""
    read -p "Use existing token? (y/n): " use_existing
    if [[ "$use_existing" =~ ^[Yy]$ ]]; then
        exec ./deploy.sh "$@"
    fi
fi

echo -e "${YELLOW}⚠${NC} Current GitHub CLI token (GITHUB_TOKEN) lacks permissions"
echo ""
echo "You need a Personal Access Token (PAT) with these scopes:"
echo "  • project (full control)"
echo "  • read:org (organization access)"
echo ""

# Offer options
echo "Choose your preferred method:"
echo ""
echo "  ${GREEN}1${NC} - I have a PAT in 1Password"
echo "  ${GREEN}2${NC} - I have a PAT in environment/clipboard"
echo "  ${GREEN}3${NC} - I need to generate a new PAT"
echo "  ${GREEN}4${NC} - Show me the full guide"
echo ""
read -p "Enter choice (1-4): " choice
echo ""

case $choice in
    1)
        # 1Password method
        echo -e "${BLUE}Method 1: Using 1Password${NC}"
        echo ""

        # Check if signed in
        if ! op account list &>/dev/null; then
            echo -e "${YELLOW}⚠${NC} Not signed in to 1Password"
            echo "Sign in now..."
            eval $(op signin)
        fi

        echo "Enter your 1Password reference path:"
        echo "Example: op://Private/GitHub PAT/password"
        echo ""
        read -p "Reference: " op_ref

        # Test retrieval
        echo ""
        echo "Testing token retrieval..."
        if token=$(op read "$op_ref" 2>/dev/null); then
            if [[ "$token" == ghp_* ]]; then
                echo -e "${GREEN}✓${NC} Token retrieved successfully"
                export GH_TOKEN="$token"
                export OP_REFERENCE="$op_ref"

                echo ""
                read -p "Run dry-run first? (recommended) (Y/n): " dry_run
                if [[ ! "$dry_run" =~ ^[Nn]$ ]]; then
                    ./deploy.sh --dry-run
                    echo ""
                    read -p "Deploy for real? (y/n): " confirm
                    if [[ "$confirm" =~ ^[Yy]$ ]]; then
                        ./deploy.sh
                    fi
                else
                    ./deploy.sh
                fi
            else
                echo -e "${RED}✗${NC} Retrieved token doesn't look like a PAT (should start with ghp_)"
                exit 1
            fi
        else
            echo -e "${RED}✗${NC} Failed to retrieve token from 1Password"
            echo "Check your reference path: $op_ref"
            exit 1
        fi
        ;;

    2)
        # Direct token method
        echo -e "${BLUE}Method 2: Direct Token${NC}"
        echo ""
        echo "Paste your Personal Access Token (starts with ghp_):"
        read -s token
        echo ""

        if [[ "$token" != ghp_* ]]; then
            echo -e "${RED}✗${NC} Token should start with ghp_"
            exit 1
        fi

        export GH_TOKEN="$token"
        echo -e "${GREEN}✓${NC} Token set"
        echo ""

        read -p "Run dry-run first? (recommended) (Y/n): " dry_run
        if [[ ! "$dry_run" =~ ^[Nn]$ ]]; then
            ./deploy.sh --dry-run
            echo ""
            read -p "Deploy for real? (y/n): " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                ./deploy.sh
            fi
        else
            ./deploy.sh
        fi
        ;;

    3)
        # Generate new token
        echo -e "${BLUE}Method 3: Generate New Token${NC}"
        echo ""
        echo "Opening GitHub token creation page..."
        echo ""
        echo "Required scopes:"
        echo "  ✓ project (full control)"
        echo "  ✓ read:org"
        echo ""

        # Open browser
        "$BROWSER" "https://github.com/settings/tokens/new?description=GitHub+Projects+Management&scopes=project,read:org" &>/dev/null &

        echo "After generating the token:"
        echo "  1. Copy the token (starts with ghp_)"
        echo "  2. Run this script again and choose option 1 or 2"
        echo ""
        echo "Or store in 1Password and set:"
        echo '  export OP_REFERENCE="op://Vault/Item/field"'
        echo "  ./deploy-with-1password.sh"
        ;;

    4)
        # Show full guide
        echo -e "${BLUE}Opening full guide...${NC}"
        echo ""
        if command -v bat &>/dev/null; then
            bat TOKEN_SETUP_GUIDE.md
        elif command -v less &>/dev/null; then
            less TOKEN_SETUP_GUIDE.md
        else
            cat TOKEN_SETUP_GUIDE.md
        fi
        ;;

    *)
        echo -e "${RED}✗${NC} Invalid choice"
        exit 1
        ;;
esac
