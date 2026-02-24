#!/usr/bin/env bash
#
# validate-repository-structure.sh - Validate repository structure against standards
#
# Usage: ./scripts/validate-repository-structure.sh [--strict]
#
# Options:
#   --strict    Fail on warnings (default: warnings don't fail)
#
# Exit codes:
#   0 - All checks passed
#   1 - Errors found
#   2 - Warnings found (only with --strict)
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
ERRORS=0
WARNINGS=0
PASSES=0

# Options
STRICT_MODE=false
[ "${1:-}" = "--strict" ] && STRICT_MODE=true

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSES++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

error() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

header() {
    echo ""
    echo -e "${CYAN}━━━ $1 ━━━${NC}"
}

# =============================================================================
# Checks
# =============================================================================

header "Required Files"

# README.md
[ -f "README.md" ] && pass "README.md exists" || error "README.md is missing"

# LICENSE
[ -f "LICENSE" ] && pass "LICENSE exists" || error "LICENSE is missing"

# .gitignore
[ -f ".gitignore" ] && pass ".gitignore exists" || error ".gitignore is missing"

header "Recommended Structure"

# .github directory
[ -d ".github" ] && pass ".github/ directory exists" || warn ".github/ directory is missing"

# .github/workflows
[ -d ".github/workflows" ] && pass ".github/workflows/ exists" || warn ".github/workflows/ is missing"

# docs directory
[ -d "docs" ] && pass "docs/ directory exists" || warn "docs/ directory is missing"

# tests directory
[ -d "tests" ] && pass "tests/ directory exists" || warn "tests/ directory is missing"

# scripts directory
[ -d "scripts" ] && pass "scripts/ directory exists" || warn "scripts/ directory is missing"

header "Root Directory Clutter"

# Count root files (excluding hidden and directories)
ROOT_FILE_COUNT=$(find . -maxdepth 1 -type f ! -name ".*" | wc -l)
if [ "$ROOT_FILE_COUNT" -le 15 ]; then
    pass "Root has $ROOT_FILE_COUNT files (max 15)"
else
    warn "Root has $ROOT_FILE_COUNT files (recommended max 15)"
fi

# Check for status/completion files in root
STATUS_FILES=$(find . -maxdepth 1 -name "*STATUS*" -o -name "*COMPLETE*" -o -name "*DONE*" -o -name "*PHASE[0-9]*" 2>/dev/null | grep -v "^\./\." || true)
if [ -z "$STATUS_FILES" ]; then
    pass "No status files in root"
else
    warn "Status files found in root (should be in reports/ or archive/):"
    echo "$STATUS_FILES" | while read -r f; do echo "       $f"; done
fi

# Check for test result files in root
TEST_RESULTS=$(find . -maxdepth 1 -name "test-results*" -o -name "coverage*" -o -name "*.log" 2>/dev/null | grep -v "^\./\." || true)
if [ -z "$TEST_RESULTS" ]; then
    pass "No test results in root"
else
    warn "Test result files found in root (should be in reports/ or gitignored):"
    echo "$TEST_RESULTS" | while read -r f; do echo "       $f"; done
fi

header "Build Artifacts"

# Check if common build directories exist and are gitignored
check_gitignored() {
    local pattern="$1"
    local description="$2"

    if [ -d "$pattern" ] || [ -f "$pattern" ]; then
        if grep -q "^${pattern}" .gitignore 2>/dev/null || grep -q "^${pattern}/" .gitignore 2>/dev/null; then
            pass "$description is gitignored"
        else
            warn "$description exists but is not gitignored"
        fi
    else
        pass "$description not present or properly ignored"
    fi
}

check_gitignored "dist" "dist/"
check_gitignored "build" "build/"
check_gitignored "node_modules" "node_modules/"
check_gitignored "__pycache__" "__pycache__/"
check_gitignored ".venv" ".venv/"
check_gitignored "venv" "venv/"
check_gitignored ".env" ".env"

header "File Naming"

# Check for files with spaces in names
FILES_WITH_SPACES=$(find . -name "* *" -not -path "./.git/*" 2>/dev/null || true)
if [ -z "$FILES_WITH_SPACES" ]; then
    pass "No files with spaces in names"
else
    warn "Files with spaces in names found:"
    echo "$FILES_WITH_SPACES" | head -5 | while read -r f; do echo "       $f"; done
fi

# Check for uppercase extensions
UPPERCASE_EXT=$(find . -type f -name "*.[A-Z]*" -not -path "./.git/*" 2>/dev/null | head -5 || true)
if [ -z "$UPPERCASE_EXT" ]; then
    pass "No uppercase file extensions"
else
    warn "Files with uppercase extensions found (use lowercase):"
    echo "$UPPERCASE_EXT" | while read -r f; do echo "       $f"; done
fi

header "Special Files"

# CHANGELOG.md
[ -f "CHANGELOG.md" ] && pass "CHANGELOG.md exists" || info "CHANGELOG.md is recommended"

# CONTRIBUTING.md (root or docs/)
if [ -f "CONTRIBUTING.md" ] || [ -f "docs/CONTRIBUTING.md" ] || [ -f "docs/governance/CONTRIBUTING.md" ]; then
    pass "CONTRIBUTING.md exists"
else
    info "CONTRIBUTING.md is recommended"
fi

# SECURITY.md
[ -f "SECURITY.md" ] && pass "SECURITY.md exists" || info "SECURITY.md is recommended"

# =============================================================================
# Summary
# =============================================================================

header "Summary"

echo ""
echo -e "  ${GREEN}Passed:${NC}   $PASSES"
echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "  ${RED}Errors:${NC}   $ERRORS"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ Validation failed with $ERRORS error(s)${NC}"
    echo ""
    echo "See docs/reference/REPOSITORY_STRUCTURE.md for standards."
    exit 1
elif [ "$WARNINGS" -gt 0 ] && [ "$STRICT_MODE" = true ]; then
    echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warning(s) (strict mode)${NC}"
    echo ""
    echo "See docs/reference/REPOSITORY_ORGANIZATION_QUICK_REF.md for quick fixes."
    exit 2
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warning(s)${NC}"
    echo ""
    echo "See docs/reference/REPOSITORY_ORGANIZATION_QUICK_REF.md for quick fixes."
    exit 0
else
    echo -e "${GREEN}✅ All checks passed!${NC}"
    exit 0
fi
