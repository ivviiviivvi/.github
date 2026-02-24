#!/bin/bash
# Interactive guide for configuring GitHub Projects views
# This guides you through creating 42 views across 7 projects

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project configuration
declare -A PROJECTS=(
    ["8"]="AI Framework Development"
    ["9"]="Documentation & Knowledge"
    ["10"]="Workflow Automation"
    ["11"]="Security & Compliance"
    ["12"]="Infrastructure & DevOps"
    ["13"]="Community & Support"
    ["14"]="Product Roadmap"
)

# Progress tracking
PROGRESS_FILE=".github-projects-views-progress.txt"

# Initialize progress file if it doesn't exist
if [[ ! -f "$PROGRESS_FILE" ]]; then
    echo "# GitHub Projects Views Configuration Progress" > "$PROGRESS_FILE"
    echo "# Format: PROJECT_NUMBER|VIEW_NAME|STATUS" >> "$PROGRESS_FILE"
    for proj in 8 9 10 11 12 13 14; do
        for view in "Board" "Table" "Roadmap" "Priority" "Team" "Status"; do
            echo "$proj|$view|TODO" >> "$PROGRESS_FILE"
        done
    done
fi

# Function to show progress
show_progress() {
    local total=42
    local completed=$(grep -c "|DONE$" "$PROGRESS_FILE" || echo 0)
    local percentage=$((completed * 100 / total))

    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}             GitHub Projects Views Configuration             ${CYAN}║${NC}"
    echo -e "${CYAN}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC}  Progress: ${GREEN}$completed${NC} / $total views (${percentage}%)                        ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Function to mark view as done
mark_done() {
    local project=$1
    local view=$2
    sed -i "s/^$project|$view|TODO$/$project|$view|DONE/" "$PROGRESS_FILE"
}

# Function to configure a view
configure_view() {
    local project_num=$1
    local view_name=$2
    local project_title="${PROJECTS[$project_num]}"

    # Check if already done
    if grep -q "^$project_num|$view_name|DONE$" "$PROGRESS_FILE"; then
        echo -e "${GREEN}✓${NC} View already configured: $view_name"
        return 0
    fi

    clear
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  Configuring: Project #$project_num - $project_title${NC}"
    echo -e "${PURPLE}  View: $view_name${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    # View-specific instructions
    case "$view_name" in
        "Board")
            cat << 'EOF'
📋 BOARD VIEW CONFIGURATION
───────────────────────────────────────────────────────────────

Step 1: Navigate to Project
   → Open: https://github.com/orgs/{{ORG_NAME}}/projects/$PROJECT_NUM

Step 2: Create New View
   → Click "+ New view" button (top right)
   → Select "Board" layout

Step 3: Configure Board
   Name: Board
   Group by: Status
   Column field: Status

Step 4: Customize Columns
   ✓ Show all status values as columns
   ✓ Enable drag-and-drop between columns
   ✓ Hide empty columns: No (show all statuses)

Step 5: Card Display
   ✓ Show: Title
   ✓ Show: Labels
   ✓ Show: Assignees
   ✓ Show: Repository
   ✓ Compact mode: Off (show full cards)

Step 6: Sorting (within columns)
   Sort by: Priority (High → Low)
   Then by: Date added (Newest first)

Step 7: Save View
   → Click "Save changes"
   → Set as default view: Yes (for Board)

EOF
            ;;
        "Table")
            cat << 'EOF'
📊 TABLE VIEW CONFIGURATION
───────────────────────────────────────────────────────────────

Step 1: Navigate to Project
   → Open: https://github.com/orgs/{{ORG_NAME}}/projects/$PROJECT_NUM

Step 2: Create New View
   → Click "+ New view" button
   → Select "Table" layout

Step 3: Configure Table
   Name: Table

Step 4: Column Configuration
   Visible columns (in order):
   1. ☑ Title
   2. ☑ Status
   3. ☑ Priority
   4. ☑ Type
   5. ☑ Assignees
   6. ☑ Repository
   7. ☑ Labels
   8. ☑ Milestone
   9. ☑ Date added
   10. ☑ Last updated

   (Use column selector to show/hide)

Step 5: Sorting
   Primary: Status
   Secondary: Priority (High → Low)
   Tertiary: Last updated (Newest first)

Step 6: Filters
   → No default filters (show all items)

Step 7: Row Height
   → Medium (shows labels and key info)

Step 8: Save View
   → Click "Save changes"

EOF
            ;;
        "Roadmap")
            cat << 'EOF'
📈 ROADMAP VIEW CONFIGURATION
───────────────────────────────────────────────────────────────

Step 1: Navigate to Project
   → Open: https://github.com/orgs/{{ORG_NAME}}/projects/$PROJECT_NUM

Step 2: Create New View
   → Click "+ New view" button
   → Select "Roadmap" layout

Step 3: Configure Roadmap
   Name: Roadmap

Step 4: Date Fields
   Start date: Date added
   End date: Target date (if available, else use milestone)

Step 5: Grouping
   Group by: Status
   Show groups as: Swimlanes

Step 6: Timeline Scale
   Zoom level: Quarters
   Show today line: Yes
   Show weekends: No

Step 7: Item Display
   ✓ Show: Title
   ✓ Show: Priority (as color)
   ✓ Show: Assignees
   ✓ Show progress bars (if available)

Step 8: Color Coding
   Color by: Priority
   - Critical: Red
   - High: Orange
   - Medium: Yellow
   - Low: Gray

Step 9: Save View
   → Click "Save changes"

EOF
            ;;
        "Priority")
            cat << 'EOF'
🎯 PRIORITY VIEW CONFIGURATION
───────────────────────────────────────────────────────────────

Step 1: Navigate to Project
   → Open: https://github.com/orgs/{{ORG_NAME}}/projects/$PROJECT_NUM

Step 2: Create New View
   → Click "+ New view" button
   → Select "Board" layout

Step 3: Configure Priority Board
   Name: Priority
   Group by: Priority

Step 4: Column Order
   Columns (left to right):
   1. 🔥 Critical
   2. ⚡ High
   3. 📊 Medium
   4. 🔽 Low
   5. (No Priority)

Step 5: Card Display
   ✓ Show: Title
   ✓ Show: Status (as label)
   ✓ Show: Type
   ✓ Show: Assignees
   ✓ Show: Due date (if available)

Step 6: Sorting (within columns)
   Sort by: Status
   Then by: Date added (Oldest first - FIFO)

Step 7: Filters
   → No default filters
   → Can add quick filters for status

Step 8: Save View
   → Click "Save changes"

EOF
            ;;
        "Team")
            cat << 'EOF'
👥 TEAM VIEW CONFIGURATION
───────────────────────────────────────────────────────────────

Step 1: Navigate to Project
   → Open: https://github.com/orgs/{{ORG_NAME}}/projects/$PROJECT_NUM

Step 2: Create New View
   → Click "+ New view" button
   → Select "Board" layout

Step 3: Configure Team Board
   Name: Team
   Group by: Assignees

Step 4: Column Configuration
   Show columns for:
   ✓ Each team member
   ✓ Unassigned items (separate column)

Step 5: Card Display
   ✓ Show: Title
   ✓ Show: Status
   ✓ Show: Priority
   ✓ Show: Type
   ✓ Show: Labels

Step 6: Sorting (within columns)
   Sort by: Priority (High → Low)
   Then by: Status

Step 7: Workload Indicators
   ✓ Show item count per assignee
   ✓ Highlight overloaded assignments (>10 items)

Step 8: Filters
   Quick filter options:
   - Active items only (exclude closed)
   - This milestone
   - This sprint

Step 9: Save View
   → Click "Save changes"

EOF
            ;;
        "Status")
            cat << 'EOF'
📦 STATUS VIEW CONFIGURATION
───────────────────────────────────────────────────────────────

Step 1: Navigate to Project
   → Open: https://github.com/orgs/{{ORG_NAME}}/projects/$PROJECT_NUM

Step 2: Create New View
   → Click "+ New view" button
   → Select "Table" layout

Step 3: Configure Status Table
   Name: Status
   Group by: Status (collapsed groups)

Step 4: Column Configuration
   Essential columns only:
   1. ☑ Title
   2. ☑ Status
   3. ☑ Priority
   4. ☑ Type
   5. ☑ Assignees
   6. ☑ Last updated

Step 5: Grouping Display
   Show groups: Collapsed by default
   Show group counts: Yes
   Show empty groups: No

Step 6: Sorting (within groups)
   Sort by: Priority (High → Low)
   Then by: Last updated (Recent first)

Step 7: Filters
   Default filter: Status != Completed
   (Show active work only)

Step 8: Summary Stats
   ✓ Enable summary row
   ✓ Show: Total items per status
   ✓ Show: Items by priority

Step 9: Save View
   → Click "Save changes"

EOF
            ;;
    esac

    echo ""
    echo -e "${YELLOW}───────────────────────────────────────────────────────────────${NC}"
    echo -e "${YELLOW}Replace ${PURPLE}\$PROJECT_NUM${YELLOW} with: ${GREEN}$project_num${NC}"
    echo -e "${YELLOW}Project URL: ${BLUE}https://github.com/orgs/{{ORG_NAME}}/projects/$project_num${NC}"
    echo -e "${YELLOW}───────────────────────────────────────────────────────────────${NC}"
    echo ""

    # Wait for user confirmation
    read -p "$(echo -e ${GREEN}Press ENTER when you have completed this view configuration...${NC})"

    # Mark as done
    mark_done "$project_num" "$view_name"
    echo -e "${GREEN}✓ View marked as complete!${NC}"
    sleep 1
}

# Main menu
main_menu() {
    while true; do
        clear
        show_progress

        echo -e "${BLUE}┌────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${BLUE}│${NC}  Select a project to configure:                           ${BLUE}│${NC}"
        echo -e "${BLUE}└────────────────────────────────────────────────────────────┘${NC}"
        echo ""

    for num in $(printf '%s\n' "${!PROJECTS[@]}" | sort -n); do
            local title="${PROJECTS[$num]}"
            local completed=$(grep -c "^$num|.*|DONE$" "$PROGRESS_FILE" || echo 0)
            local emoji=""
            case $completed in
                0) emoji="⏳" ;;
                [1-5]) emoji="🔄" ;;
                6) emoji="✅" ;;
            esac
            printf "  ${emoji} %2d. %-40s (%d/6 views)\n" "$num" "$title" "$completed"
        done

        echo ""
        echo -e "${BLUE}  A.${NC} Configure all projects (auto-mode)"
        echo -e "${BLUE}  P.${NC} Show progress report"
        echo -e "${BLUE}  R.${NC} Reset progress (start over)"
        echo -e "${BLUE}  Q.${NC} Quit"
        echo ""

        read -p "$(echo -e ${CYAN}Select option:${NC}) " choice

        case "$choice" in
            [8-9]|1[0-4])
                if [[ -n "${PROJECTS[$choice]}" ]]; then
                    configure_project "$choice"
                fi
                ;;
            A|a)
                auto_configure_all
                ;;
            P|p)
                show_detailed_progress
                ;;
            R|r)
                reset_progress
                ;;
            Q|q)
                echo ""
                echo -e "${GREEN}Configuration session saved. Run this script again to continue.${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option. Please try again.${NC}"
                sleep 2
                ;;
        esac
    done
}

# Configure all views for a project
configure_project() {
    local project_num=$1
    local views=("Board" "Table" "Roadmap" "Priority" "Team" "Status")

    for view in "${views[@]}"; do
        configure_view "$project_num" "$view"
    done

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Project #$project_num configuration complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    read -p "${CYAN}Press ENTER to continue...${NC}"
}

# Auto-configure all projects
auto_configure_all() {
    for proj in 8 9 10 11 12 13 14; do
        configure_project "$proj"
    done
}

# Show detailed progress
show_detailed_progress() {
    clear
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  Detailed Progress Report${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    for proj in 8 9 10 11 12 13 14; do
        echo -e "${PURPLE}Project #$proj: ${PROJECTS[$proj]}${NC}"
        for view in "Board" "Table" "Roadmap" "Priority" "Team" "Status"; do
            if grep -q "^$proj|$view|DONE$" "$PROGRESS_FILE"; then
                echo -e "  ${GREEN}✓${NC} $view"
            else
                echo -e "  ${YELLOW}⏳${NC} $view"
            fi
        done
        echo ""
    done

    read -p "$(echo -e ${CYAN}Press ENTER to continue...${NC})"
}

# Reset progress
reset_progress() {
    echo ""
    read -p "${RED}Are you sure you want to reset all progress? (y/N):${NC} " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        rm -f "$PROGRESS_FILE"
        echo -e "${GREEN}Progress reset. Reinitializing...${NC}"
        sleep 1
        # Reinitialize will happen automatically
    fi
}

# Start
clear
echo -e "${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        GitHub Projects Views Configuration Guide             ║
║                                                               ║
║  This interactive guide will help you configure 42 views     ║
║  across 7 GitHub Projects. Each view has detailed            ║
║  step-by-step instructions.                                  ║
║                                                               ║
║  ⏱️  Estimated time: 6-9 hours total                          ║
║  📊 Views per project: 6                                      ║
║  🎯 Total views: 42                                           ║
║                                                               ║
║  Your progress is automatically saved!                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""
read -p "$(echo -e ${GREEN}Press ENTER to begin...${NC})"

main_menu
