#!/bin/bash
# Complete automation and content migration for GitHub Projects

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORG="{{ORG_NAME}}"
REPO=".github"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     GitHub Projects: Complete Automation & Migration        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found"
    exit 1
fi
echo "  ✓ Python 3"

if ! python3 -c "import requests" 2>/dev/null; then
    echo "✗ Python requests library not found"
    echo "  Run: pip install requests"
    exit 1
fi
echo "  ✓ requests library"

if [ -z "$GH_TOKEN" ]; then
    echo ""
    echo "⚠️  GH_TOKEN environment variable not set"
    echo ""
    echo "Choose token source:"
    echo "  1) Retrieve from 1Password"
    echo "  2) Enter token manually"
    read -p "Choice [1]: " choice
    choice=${choice:-1}

    if [ "$choice" = "1" ]; then
        if ! command -v op &> /dev/null; then
            echo "✗ 1Password CLI not found"
            exit 1
        fi

        echo "Retrieving token from 1Password..."
        export GH_TOKEN=$(op read "op://Personal/org-project-admin-token/password")
        echo "  ✓ Token loaded from 1Password"
    else
        echo ""
        read -sp "Enter GitHub token: " GH_TOKEN
        export GH_TOKEN
        echo ""
        echo "  ✓ Token set"
    fi
fi

echo "  ✓ GitHub token configured"
echo ""

# Menu
while true; do
    echo "What would you like to do?"
    echo ""
    echo "  1) Add existing issues/PRs to projects (recommended first)"
    echo "  2) View automation rules setup guide"
    echo "  3) Open automation setup in browser"
    echo "  4) View project statistics"
    echo "  5) Exit"
    echo ""
    read -p "Choice [1]: " action
    action=${action:-1}

    case $action in
        1)
            echo ""
            echo "╔══════════════════════════════════════════════════════════════╗"
            echo "║        Adding Issues/PRs to Projects                        ║"
            echo "╚══════════════════════════════════════════════════════════════╝"
            echo ""
            echo "Options:"
            echo "  1) Dry run (show what would be added)"
            echo "  2) Add all open items"
            echo "  3) Add open issues only"
            echo "  4) Add open PRs only"
            echo "  5) Add all items (open + closed)"
            echo ""
            read -p "Choice [1]: " add_action
            add_action=${add_action:-1}

            case $add_action in
                1)
                    echo ""
                    python3 "$SCRIPT_DIR/add-items-to-projects.py" \
                        --org "$ORG" \
                        --repo "$REPO" \
                        --dry-run
                    ;;
                2)
                    echo ""
                    python3 "$SCRIPT_DIR/add-items-to-projects.py" \
                        --org "$ORG" \
                        --repo "$REPO"
                    ;;
                3)
                    echo ""
                    python3 "$SCRIPT_DIR/add-items-to-projects.py" \
                        --org "$ORG" \
                        --repo "$REPO" \
                        --issues-only
                    ;;
                4)
                    echo ""
                    python3 "$SCRIPT_DIR/add-items-to-projects.py" \
                        --org "$ORG" \
                        --repo "$REPO" \
                        --prs-only
                    ;;
                5)
                    echo ""
                    python3 "$SCRIPT_DIR/add-items-to-projects.py" \
                        --org "$ORG" \
                        --repo "$REPO" \
                        --state all
                    ;;
            esac
            echo ""
            ;;

        2)
            echo ""
            if command -v bat &> /dev/null; then
                bat "$SCRIPT_DIR/setup-automation-rules.md"
            elif command -v less &> /dev/null; then
                less "$SCRIPT_DIR/setup-automation-rules.md"
            else
                cat "$SCRIPT_DIR/setup-automation-rules.md"
            fi
            echo ""
            ;;

        3)
            echo ""
            echo "Opening automation setup pages..."
            echo ""
            echo "Project #8 - AI Framework Development"
            echo "  https://github.com/orgs/$ORG/projects/8/workflows"
            echo ""
            echo "Project #9 - Documentation & Knowledge"
            echo "  https://github.com/orgs/$ORG/projects/9/workflows"
            echo ""
            echo "Project #10 - Workflow Automation"
            echo "  https://github.com/orgs/$ORG/projects/10/workflows"
            echo ""
            echo "Project #11 - Security & Compliance"
            echo "  https://github.com/orgs/$ORG/projects/11/workflows"
            echo ""
            echo "Project #12 - Infrastructure & DevOps"
            echo "  https://github.com/orgs/$ORG/projects/12/workflows"
            echo ""
            echo "Project #13 - Community & Support"
            echo "  https://github.com/orgs/$ORG/projects/13/workflows"
            echo ""
            echo "Project #14 - Product Roadmap"
            echo "  https://github.com/orgs/$ORG/projects/14/workflows"
            echo ""

            if [ "$BROWSER" ]; then
                read -p "Open in browser? [y/N]: " open_browser
                if [ "$open_browser" = "y" ] || [ "$open_browser" = "Y" ]; then
                    for i in {8..14}; do
                        "$BROWSER" "https://github.com/orgs/$ORG/projects/$i/workflows" &
                        sleep 1
                    done
                fi
            fi
            ;;

        4)
            echo ""
            echo "╔══════════════════════════════════════════════════════════════╗"
            echo "║              Project Statistics                              ║"
            echo "╚══════════════════════════════════════════════════════════════╝"
            echo ""
            echo "Fetching project data..."
            echo ""

            # Use GitHub CLI to get stats
            if command -v gh &> /dev/null; then
                for i in {8..14}; do
                    echo "Project #$i:"
                    gh api graphql -f query='
                    query {
                        organization(login: "'"$ORG"'") {
                            projectV2(number: '"$i"') {
                                title
                                items {
                                    totalCount
                                }
                            }
                        }
                    }' --jq '.data.organization.projectV2 | "  \(.title)\n  Items: \(.items.totalCount)"' 2>/dev/null || echo "  Unable to fetch"
                    echo ""
                done
            else
                echo "Install GitHub CLI (gh) to view statistics"
            fi
            ;;

        5)
            echo ""
            echo "✅ Done!"
            echo ""
            echo "Next steps:"
            echo "  1. Review the automation rules setup guide"
            echo "  2. Configure automation rules for each project"
            echo "  3. Test the automations with sample issues"
            echo ""
            exit 0
            ;;

        *)
            echo "Invalid choice"
            ;;
    esac
done
