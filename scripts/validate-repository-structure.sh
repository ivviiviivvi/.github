#!/bin/bash
# Repository Structure Validation Script
# Validates repository structure against organizational standards
# Version: 1.0.0

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
CHECKS=0

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Repository Structure Validation          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo "Repository: $REPO_ROOT"
echo ""

# Function to check if a file exists
check_file_required() {
    local file=$1
    local description=$2
    CHECKS=$((CHECKS + 1))
    
    if [ -f "$REPO_ROOT/$file" ]; then
        echo -e "${GREEN}✓${NC} $description: $file"
    else
        echo -e "${RED}✗${NC} $description: $file (MISSING)"
        ERRORS=$((ERRORS + 1))
    fi
}

# Function to check if a file exists (warning only)
check_file_recommended() {
    local file=$1
    local description=$2
    CHECKS=$((CHECKS + 1))
    
    if [ -f "$REPO_ROOT/$file" ]; then
        echo -e "${GREEN}✓${NC} $description: $file"
        return 0
    else
        echo -e "${YELLOW}!${NC} $description: $file (recommended)"
        WARNINGS=$((WARNINGS + 1))
        return 1
    fi
}

# Function to check if a directory exists
check_dir_recommended() {
    local dir=$1
    local description=$2
    CHECKS=$((CHECKS + 1))
    
    if [ -d "$REPO_ROOT/$dir" ]; then
        echo -e "${GREEN}✓${NC} $description: $dir/"
    else
        echo -e "${YELLOW}!${NC} $description: $dir/ (recommended)"
        WARNINGS=$((WARNINGS + 1))
    fi
}

# Function to check for problematic files in root
check_root_clutter() {
    local pattern=$1
    local description=$2
    CHECKS=$((CHECKS + 1))
    
    cd "$REPO_ROOT"
    local files=$(find . -maxdepth 1 -type f -name "$pattern" 2>/dev/null || true)
    
    if [ -n "$files" ]; then
        echo -e "${YELLOW}!${NC} Found $description in root (should be in subdirectory):"
        echo "$files" | sed 's/^/  /'
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}✓${NC} No $description in root"
    fi
}

# Function to check for build artifacts
check_artifacts() {
    local dir=$1
    local description=$2
    CHECKS=$((CHECKS + 1))
    
    if [ -d "$REPO_ROOT/$dir" ]; then
        if grep -q "^$dir/\?$" "$REPO_ROOT/.gitignore" 2>/dev/null || \
           grep -q "^/$dir/\?$" "$REPO_ROOT/.gitignore" 2>/dev/null || \
           grep -q "^$dir/$" "$REPO_ROOT/.gitignore" 2>/dev/null || \
           grep -q "^/$dir/$" "$REPO_ROOT/.gitignore" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $description properly gitignored: $dir/"
        else
            echo -e "${YELLOW}!${NC} $description should be in .gitignore: $dir/"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

# ==================== Required Files ====================
echo -e "\n${BLUE}[Required Files]${NC}"
check_file_required "README.md" "Repository overview"
check_file_required "LICENSE" "License file"
check_file_required ".gitignore" "Git ignore rules"

# ==================== Recommended Core Files ====================
echo -e "\n${BLUE}[Recommended Core Files]${NC}"
check_file_recommended "CONTRIBUTING.md" "Contribution guidelines" || \
    check_file_recommended "docs/governance/CONTRIBUTING.md" "Contribution guidelines (alt location)"
check_file_recommended "CODE_OF_CONDUCT.md" "Code of conduct" || \
    check_file_recommended "docs/governance/CODE_OF_CONDUCT.md" "Code of conduct (alt location)"
check_file_recommended "SECURITY.md" "Security policy" || \
    check_file_recommended "docs/governance/SECURITY.md" "Security policy (alt location)"
check_file_recommended "CHANGELOG.md" "Version history"

# ==================== Recommended Directories ====================
echo -e "\n${BLUE}[Recommended Directories]${NC}"
check_dir_recommended "docs" "Documentation directory"
check_dir_recommended "tests" "Test directory"
check_dir_recommended ".github" "GitHub configuration"

# ==================== GitHub Configuration ====================
if [ -d "$REPO_ROOT/.github" ]; then
    echo -e "\n${BLUE}[GitHub Configuration]${NC}"
    check_dir_recommended ".github/workflows" "GitHub Actions workflows"
    check_file_recommended ".github/CODEOWNERS" "Code ownership"
    check_file_recommended ".github/dependabot.yml" "Dependabot configuration"
fi

# ==================== Documentation Structure ====================
if [ -d "$REPO_ROOT/docs" ]; then
    echo -e "\n${BLUE}[Documentation Structure]${NC}"
    check_file_recommended "docs/README.md" "Documentation index"
    check_dir_recommended "docs/guides" "User guides"
    check_dir_recommended "docs/reference" "Reference documentation"
fi

# ==================== Root Clutter Checks ====================
echo -e "\n${BLUE}[Root Directory Organization]${NC}"
check_root_clutter "STATUS_*.md" "status files"
check_root_clutter "REPORT_*.md" "report files"
check_root_clutter "*_COMPLETE.md" "completion status files"
check_root_clutter "MONITORING_*.md" "monitoring files"
check_root_clutter "DEPLOYMENT_*.md" "deployment files"
check_root_clutter "WEEK*_*.md" "weekly report files"
check_root_clutter "PHASE*_*.md" "phase report files"

# Check for test result files
CHECKS=$((CHECKS + 1))
cd "$REPO_ROOT"
test_files=$(find . -maxdepth 1 -type f -name "test-results*.json" 2>/dev/null || true)
if [ -n "$test_files" ]; then
    echo -e "${YELLOW}!${NC} Test result files should be in reports/ or gitignored:"
    echo "$test_files" | sed 's/^/  /'
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✓${NC} No test result files in root"
fi

# ==================== Build Artifacts ====================
echo -e "\n${BLUE}[Build Artifacts Check]${NC}"
check_artifacts "node_modules" "node_modules"
check_artifacts "dist" "dist/"
check_artifacts "build" "build/"
check_artifacts "target" "target/"
check_artifacts ".venv" ".venv/"
check_artifacts "venv" "venv/"
check_artifacts "coverage" "coverage/"

# Check for __pycache__
CHECKS=$((CHECKS + 1))
if [ -d "$REPO_ROOT/__pycache__" ]; then
    if grep -q "__pycache__" "$REPO_ROOT/.gitignore" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} __pycache__ properly gitignored"
    else
        echo -e "${YELLOW}!${NC} __pycache__ should be in .gitignore"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# ==================== Special Files Check ====================
echo -e "\n${BLUE}[Special Files]${NC}"

# Check for .env files
CHECKS=$((CHECKS + 1))
if [ -f "$REPO_ROOT/.env" ]; then
    if grep -q "^\.env$" "$REPO_ROOT/.gitignore" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} .env is gitignored"
    else
        echo -e "${RED}✗${NC} .env exists but not gitignored (SECURITY RISK)"
        ERRORS=$((ERRORS + 1))
    fi
elif [ -f "$REPO_ROOT/.env.example" ]; then
    echo -e "${GREEN}✓${NC} .env.example template provided"
fi

# ==================== Naming Convention Checks ====================
echo -e "\n${BLUE}[Naming Conventions]${NC}"

# Check for spaces in filenames
CHECKS=$((CHECKS + 1))
cd "$REPO_ROOT"
files_with_spaces=$(find . -type f -name "* *" ! -path "./.git/*" ! -path "./node_modules/*" 2>/dev/null || true)
if [ -n "$files_with_spaces" ]; then
    echo -e "${YELLOW}!${NC} Files with spaces in names (use kebab-case or snake_case):"
    echo "$files_with_spaces" | head -5 | sed 's/^/  /'
    [ $(echo "$files_with_spaces" | wc -l) -gt 5 ] && echo "  ... and $(( $(echo "$files_with_spaces" | wc -l) - 5 )) more"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✓${NC} No files with spaces in names"
fi

# ==================== Archive Directory Check ====================
if [ -d "$REPO_ROOT/archive" ]; then
    echo -e "\n${BLUE}[Archive Directory]${NC}"
    check_file_recommended "archive/README.md" "Archive documentation"
fi

# ==================== Summary ====================
echo -e "\n${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Validation Summary                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo "Total checks:  $CHECKS"
echo -e "${GREEN}Passed:        $(($CHECKS - $ERRORS - $WARNINGS))${NC}"
echo -e "${YELLOW}Warnings:      $WARNINGS${NC}"
echo -e "${RED}Errors:        $ERRORS${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ Repository structure is excellent!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}! Repository structure is good, but has some recommendations${NC}"
    echo "  Review warnings above to improve organization"
    exit 0
else
    echo -e "${RED}✗ Repository structure has issues that should be addressed${NC}"
    echo "  Fix errors above to meet organizational standards"
    exit 1
fi
