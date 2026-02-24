#!/bin/bash
# Interactive guide for configuring GitHub Projects automation rules
# Guides through setting up 35+ automation rules across 7 projects

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Progress tracking
PROGRESS_FILE=".github-projects-automation-progress.txt"

# Initialize progress file
if [[ ! -f "$PROGRESS_FILE" ]]; then
    cat > "$PROGRESS_FILE" << 'EOF'
# GitHub Projects Automation Rules Configuration Progress
8|new-items-planned|TODO
8|pr-approved-review|TODO
8|pr-merged-deployed|TODO
8|item-closed-completed|TODO
8|auto-assign-language|TODO
9|new-docs-draft|TODO
9|pr-approved-review|TODO
9|pr-merged-published|TODO
9|set-doc-type|TODO
9|update-last-modified|TODO
10|new-workflow-ideation|TODO
10|pr-created-development|TODO
10|pr-approved-testing|TODO
10|pr-merged-active|TODO
10|workflow-label-type|TODO
10|bug-issues-bugfix|TODO
11|new-security-identified|TODO
11|pr-created-remediation|TODO
11|pr-approved-validation|TODO
11|pr-merged-resolved|TODO
11|security-label-finding|TODO
12|new-infra-planning|TODO
12|pr-created-implementation|TODO
12|pr-approved-testing|TODO
12|pr-merged-deployed|TODO
12|env-label-environment|TODO
12|infra-label-component|TODO
13|new-support-new|TODO
13|response-inprogress|TODO
13|solution-resolved|TODO
13|enhancement-feature|TODO
14|new-roadmap-backlog|TODO
14|prioritized-planned|TODO
14|inprogress-development|TODO
14|completed-shipped|TODO
EOF
fi

# Function to show progress
show_progress() {
    local total=$(wc -l < "$PROGRESS_FILE" | awk '{print $1-1}')  # Exclude header
    local completed=$(grep -c "|DONE$" "$PROGRESS_FILE" || echo 0)
    local percentage=$((completed * 100 / total))

    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}        GitHub Projects Automation Rules Configuration       ${CYAN}║${NC}"
    echo -e "${CYAN}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC}  Progress: ${GREEN}$completed${NC} / $total rules (${percentage}%)                        ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Function to configure a rule
configure_rule() {
    local project=$1
    local rule_id=$2
    local rule_name=$3
    local trigger=$4
    local action=$5

    # Check if already done
    if grep -q "^$project|$rule_id|DONE$" "$PROGRESS_FILE"; then
        echo -e "${GREEN}✓${NC} Rule already configured: $rule_name"
        return 0
    fi

    clear
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  Project #$project Automation Rule${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Rule Name:${NC} $rule_name"
    echo -e "${CYAN}Trigger:${NC} $trigger"
    echo -e "${CYAN}Action:${NC} $action"
    echo ""
    echo -e "${YELLOW}───────────────────────────────────────────────────────────────${NC}"
    echo -e "${YELLOW}STEP-BY-STEP INSTRUCTIONS:${NC}"
    echo -e "${YELLOW}───────────────────────────────────────────────────────────────${NC}"
    echo ""
    echo "1. Navigate to project settings:"
    echo -e "   ${BLUE}https://github.com/orgs/{{ORG_NAME}}/projects/$project/settings${NC}"
    echo ""
    echo "2. Click 'Workflows' in the left sidebar"
    echo ""
    echo "3. Click '+ New workflow' button"
    echo ""
    echo "4. Configure workflow:"
    echo -e "   ${CYAN}Trigger:${NC} $trigger"
    echo -e "   ${CYAN}Action:${NC} $action"
    echo ""
    echo "5. Test the workflow with a sample item"
    echo ""
    echo "6. Click 'Save workflow'"
    echo ""
    echo -e "${YELLOW}───────────────────────────────────────────────────────────────${NC}"
    echo ""

    read -p "$(echo -e ${GREEN}Press ENTER when you have completed this rule...${NC})"

    # Mark as done
    sed -i "s/^$project|$rule_id|TODO$/$project|$rule_id|DONE/" "$PROGRESS_FILE"
    echo -e "${GREEN}✓ Rule marked as complete!${NC}"
    sleep 1
}

# Project #8: AI Framework Development
configure_project_8() {
    echo -e "${PURPLE}Configuring Project #8: AI Framework Development${NC}"

    configure_rule "8" "new-items-planned" \
        "New items → Planned status" \
        "Item added to project" \
        "Set Status = 🎯 Planned"

    configure_rule "8" "pr-approved-review" \
        "PR approved → Code Review" \
        "Pull request: Review approved" \
        "Set Status = 👀 Code Review"

    configure_rule "8" "pr-merged-deployed" \
        "PR merged → Deployed" \
        "Pull request: Merged" \
        "Set Status = 🚀 Deployed"

    configure_rule "8" "item-closed-completed" \
        "Item closed → Completed" \
        "Issue/PR: Closed" \
        "Set Status = ✔️ Completed"

    configure_rule "8" "auto-assign-language" \
        "Auto-assign Language from labels" \
        "Item added OR Label added" \
        "Set Language field based on label:
   - python → Python
   - typescript/javascript → TypeScript
   - java → Java
   - csharp/dotnet → C#
   - golang → Go
   - rust → Rust"
}

# Project #9: Documentation & Knowledge
configure_project_9() {
    echo -e "${PURPLE}Configuring Project #9: Documentation & Knowledge${NC}"

    configure_rule "9" "new-docs-draft" \
        "New docs → Draft" \
        "Item added to project" \
        "Set Status = ✍️ Writing"

    configure_rule "9" "pr-approved-review" \
        "PR approved → Review" \
        "Pull request: Review approved" \
        "Set Status = 👀 Review"

    configure_rule "9" "pr-merged-published" \
        "PR merged → Published" \
        "Pull request: Merged" \
        "Set Status = 📤 Published"

    configure_rule "9" "set-doc-type" \
        "Set Document Type from path" \
        "Item added" \
        "Set Document Type based on file path:
   - docs/guides/ → 📖 Guide
   - docs/architecture/ → 🏛️ Architecture
   - docs/reference/ → 🔧 Technical Reference
   - docs/tutorials/ → 📚 Tutorial
   - CONTRIBUTING.md, CODE_OF_CONDUCT.md → 📋 Policy
   - README.md, QUICKSTART.md → 🎯 Quick Start"

    configure_rule "9" "update-last-modified" \
        "Update Last Updated date" \
        "Pull request: Merged (docs changed)" \
        "Set Last Updated = Today"
}

# Project #10: Workflow Automation
configure_project_10() {
    echo -e "${PURPLE}Configuring Project #10: Workflow Automation${NC}"

    configure_rule "10" "new-workflow-ideation" \
        "New workflows → Ideation" \
        "Item added to project" \
        "Set Status = 💡 Ideation"

    configure_rule "10" "pr-created-development" \
        "PR created → In Development" \
        "Pull request: Opened" \
        "Set Status = 🏗️ In Development"

    configure_rule "10" "pr-approved-testing" \
        "PR approved → Testing" \
        "Pull request: Review approved" \
        "Set Status = 🧪 Testing"

    configure_rule "10" "pr-merged-active" \
        "PR merged → Active" \
        "Pull request: Merged" \
        "Set Status = ✅ Active"

    configure_rule "10" "workflow-label-type" \
        "Workflow label → Automation Type" \
        "Label added: workflow" \
        "Set Type = 🔄 Workflow"

    configure_rule "10" "bug-issues-bugfix" \
        "Bug issues → Bug Fix" \
        "Label added: bug" \
        "Set Type = 🐛 Bug Fix"
}

# Project #11: Security & Compliance
configure_project_11() {
    echo -e "${PURPLE}Configuring Project #11: Security & Compliance${NC}"

    configure_rule "11" "new-security-identified" \
        "New security items → Identified" \
        "Item added to project" \
        "Set Status = 🔍 Identified"

    configure_rule "11" "pr-created-remediation" \
        "PR created → Remediation in Progress" \
        "Pull request: Opened" \
        "Set Status = 🔧 Remediation in Progress"

    configure_rule "11" "pr-approved-validation" \
        "PR approved → Validation" \
        "Pull request: Review approved" \
        "Set Status = ✓ Validation"

    configure_rule "11" "pr-merged-resolved" \
        "PR merged → Resolved" \
        "Pull request: Merged" \
        "Set Status = ✅ Resolved"

    configure_rule "11" "security-label-finding" \
        "Security label → Finding type" \
        "Label added: security" \
        "Set Type = 🔒 Security Finding"
}

# Project #12: Infrastructure & DevOps
configure_project_12() {
    echo -e "${PURPLE}Configuring Project #12: Infrastructure & DevOps${NC}"

    configure_rule "12" "new-infra-planning" \
        "New infra items → Planning" \
        "Item added to project" \
        "Set Status = 📋 Planning"

    configure_rule "12" "pr-created-implementation" \
        "PR created → Implementation" \
        "Pull request: Opened" \
        "Set Status = 🏗️ Implementation"

    configure_rule "12" "pr-approved-testing" \
        "PR approved → Testing" \
        "Pull request: Review approved" \
        "Set Status = 🧪 Testing"

    configure_rule "12" "pr-merged-deployed" \
        "PR merged → Deployed" \
        "Pull request: Merged" \
        "Set Status = 🚀 Deployed"

    configure_rule "12" "env-label-environment" \
        "Environment label → field" \
        "Label matches: production, staging, development" \
        "Set Environment field from label"

    configure_rule "12" "infra-label-component" \
        "Infrastructure label → component" \
        "Label added: infrastructure" \
        "Set Type = 🏗️ Infrastructure Component"
}

# Project #13: Community & Support
configure_project_13() {
    echo -e "${PURPLE}Configuring Project #13: Community & Support${NC}"

    configure_rule "13" "new-support-new" \
        "New support items → New" \
        "Item added to project" \
        "Set Status = 🆕 New"

    configure_rule "13" "response-inprogress" \
        "Response provided → In Progress" \
        "Comment added by team member" \
        "Set Status = 🔄 In Progress"

    configure_rule "13" "solution-resolved" \
        "Solution provided → Resolved" \
        "Issue: Closed as completed" \
        "Set Status = ✅ Resolved"

    configure_rule "13" "enhancement-feature" \
        "Enhancement → Feature Request" \
        "Label added: enhancement" \
        "Set Type = ⭐ Feature Request"
}

# Project #14: Product Roadmap
configure_project_14() {
    echo -e "${PURPLE}Configuring Project #14: Product Roadmap${NC}"

    configure_rule "14" "new-roadmap-backlog" \
        "New roadmap items → Backlog" \
        "Item added to project" \
        "Set Status = 📋 Backlog"

    configure_rule "14" "prioritized-planned" \
        "Prioritized → Planned" \
        "Priority set to High or Critical" \
        "Set Status = 🎯 Planned"

    configure_rule "14" "inprogress-development" \
        "In progress → In Development" \
        "Pull request: Opened" \
        "Set Status = 🏗️ In Development"

    configure_rule "14" "completed-shipped" \
        "Completed → Shipped" \
        "Pull request: Merged + Issue: Closed" \
        "Set Status = 🚀 Shipped"
}

# Main menu
main_menu() {
    while true; do
        clear
        show_progress

        echo -e "${BLUE}┌────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${BLUE}│${NC}  Select a project to configure automation rules:         ${BLUE}│${NC}"
        echo -e "${BLUE}└────────────────────────────────────────────────────────────┘${NC}"
        echo ""

        echo "  8. AI Framework Development (5 rules)"
        echo "  9. Documentation & Knowledge (5 rules)"
        echo "  10. Workflow Automation (6 rules)"
        echo "  11. Security & Compliance (5 rules)"
        echo "  12. Infrastructure & DevOps (6 rules)"
        echo "  13. Community & Support (4 rules)"
        echo "  14. Product Roadmap (4 rules)"
        echo ""
        echo -e "${BLUE}  A.${NC} Configure all projects (auto-mode)"
        echo -e "${BLUE}  P.${NC} Show progress report"
        echo -e "${BLUE}  Q.${NC} Quit"
        echo ""

        read -p "$(echo -e ${CYAN}Select option:${NC}) " choice

        case "$choice" in
            8) configure_project_8 ;;
            9) configure_project_9 ;;
            10) configure_project_10 ;;
            11) configure_project_11 ;;
            12) configure_project_12 ;;
            13) configure_project_13 ;;
            14) configure_project_14 ;;
            A|a)
                for p in 8 9 10 11 12 13 14; do
                    configure_project_$p
                done
                ;;
            P|p)
                show_detailed_progress
                ;;
            Q|q)
                echo ""
                echo -e "${GREEN}Configuration session saved. Run this script again to continue.${NC}"
                echo ""
                exit 0
                ;;
        esac
    done
}

# Show detailed progress
show_detailed_progress() {
    clear
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  Automation Rules Progress Report${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    for proj in 8 9 10 11 12 13 14; do
        local total=$(grep -c "^$proj|" "$PROGRESS_FILE")
        local done=$(grep -c "^$proj|.*|DONE$" "$PROGRESS_FILE" || echo 0)
        echo -e "${PURPLE}Project #$proj:${NC} $done/$total rules complete"
    done

    echo ""
    read -p "$(echo -e ${CYAN}Press ENTER to continue...${NC})"
}

# Start
clear
echo -e "${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     GitHub Projects Automation Rules Configuration           ║
║                                                               ║
║  This guide helps you configure 35+ automation rules         ║
║  across 7 GitHub Projects.                                   ║
║                                                               ║
║  ⏱️  Estimated time: 3-4 hours total                          ║
║  📊 Total rules: 35+                                          ║
║                                                               ║
║  Progress is automatically saved!                            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""
read -p "$(echo -e ${GREEN}Press ENTER to begin...${NC})"

main_menu
