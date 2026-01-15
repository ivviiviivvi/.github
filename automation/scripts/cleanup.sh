#!/usr/bin/env bash
# automation/scripts/cleanup.sh - Remove temporary and build artifacts
#
# DESCRIPTION:
#   Removes Python build artifacts, cache files, OS temp files, and editor
#   artifacts from the workspace. Safe to run at any time.
#
# USAGE:
#   ./automation/scripts/cleanup.sh [--dry-run] [--verbose]
#
# OPTIONS:
#   --dry-run   Show what would be deleted without deleting
#   --verbose   Show detailed output of deleted files
#
# EXAMPLES:
#   ./automation/scripts/cleanup.sh
#   ./automation/scripts/cleanup.sh --dry-run
#   ./automation/scripts/cleanup.sh --verbose
#
# EXIT CODES:
#   0 - Success
#   1 - Error occurred during cleanup

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
VERBOSE=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        --verbose)
            VERBOSE=true
            ;;
        --help|-h)
            grep '^#' "$0" | sed 's/^# //' | sed 's/^#//'
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $arg${NC}" >&2
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
done

# Function to delete with optional dry-run
delete_items() {
    local pattern="$1"
    local type="$2"
    local description="$3"

    echo -e "${YELLOW}🔍 Searching for $description...${NC}"

    if [ "$type" = "d" ]; then
        # Directories
        local items
        items=$(find . -type d -name "$pattern" 2>/dev/null || true)
        if [ -n "$items" ]; then
            local count
            count=$(echo "$items" | wc -l)
            if [ "$DRY_RUN" = true ]; then
                echo -e "${GREEN}[DRY RUN] Would delete $count directory(ies):${NC}"
                echo "$items"
            else
                if [ "$VERBOSE" = true ]; then
                    echo "$items"
                fi
                find . -type d -name "$pattern" -exec rm -rf {} + 2>/dev/null || true
                echo -e "${GREEN}✓ Deleted $count directory(ies)${NC}"
            fi
        else
            echo -e "${GREEN}✓ No $description found${NC}"
        fi
    else
        # Files
        local items
        items=$(find . -type f -name "$pattern" 2>/dev/null || true)
        if [ -n "$items" ]; then
            local count
            count=$(echo "$items" | wc -l)
            if [ "$DRY_RUN" = true ]; then
                echo -e "${GREEN}[DRY RUN] Would delete $count file(s):${NC}"
                echo "$items"
            else
                if [ "$VERBOSE" = true ]; then
                    echo "$items"
                fi
                find . -type f -name "$pattern" -delete 2>/dev/null || true
                echo -e "${GREEN}✓ Deleted $count file(s)${NC}"
            fi
        else
            echo -e "${GREEN}✓ No $description found${NC}"
        fi
    fi
}

echo -e "${GREEN}🧹 Starting cleanup...${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN MODE - No files will be deleted]${NC}"
fi
echo ""

# Python artifacts
delete_items "__pycache__" "d" "Python cache directories"
delete_items "*.pyc" "f" "Python bytecode files (.pyc)"
delete_items "*.pyo" "f" "Python optimized bytecode files (.pyo)"
delete_items "*.egg-info" "d" "Python egg-info directories"
delete_items ".pytest_cache" "d" "pytest cache directories"
delete_items ".mypy_cache" "d" "mypy cache directories"
delete_items ".coverage" "f" "coverage data files"
delete_items "htmlcov" "d" "HTML coverage report directories"

# OS artifacts
delete_items ".DS_Store" "f" "macOS metadata files"
delete_items "Thumbs.db" "f" "Windows thumbnail cache files"
delete_items "Desktop.ini" "f" "Windows desktop config files"

# Editor artifacts
delete_items "*~" "f" "editor backup files"
delete_items "*.swp" "f" "vim swap files"
delete_items "*.swo" "f" "vim swap files (alternate)"

echo ""
if [ "$DRY_RUN" = true ]; then
    echo -e "${GREEN}✅ Dry run complete - no files were deleted${NC}"
else
    echo -e "${GREEN}✅ Cleanup complete${NC}"
fi
