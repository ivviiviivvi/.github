#!/usr/bin/env bash

# Version Control Standards Validation Script
# Validates branch names, commit messages, and markdown style
# Usage: ./scripts/validate-standards.sh [--branch] [--commits] [--markdown]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

# Helper functions
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    ((ERRORS++))
}

warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
    ((WARNINGS++))
}

success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

info() {
    echo "INFO: $1"
}

# Validate branch name
validate_branch_name() {
    local branch_name="${1:-$(git rev-parse --abbrev-ref HEAD)}"
    
    info "Validating branch name: $branch_name"
    
    # Skip validation for protected branches
    if [[ "$branch_name" == "main" ]] || [[ "$branch_name" == "master" ]] || [[ "$branch_name" == "develop" ]]; then
        info "Skipping validation for protected branch: $branch_name"
        return 0
    fi
    
    # Valid patterns according to VERSION_CONTROL_STANDARDS.md
    local valid_patterns=(
        "^(develop|experimental|production|maintenance|deprecated|archive)/(feature|bugfix|hotfix|enhancement|refactor|docs|test|chore)/[a-z0-9-]+(/[a-z0-9-]+)?(/[a-z0-9-]+)?$"
        "^release/v[0-9]+\.[0-9]+\.[0-9]+(-[a-z0-9.-]+)?$"
        "^maintenance/v[0-9]+-maintenance$"
        "^maintenance/v[0-9]+\.x/[a-z0-9-]+$"
        "^archive/[a-z0-9-]+/[a-z0-9-]+$"
    )
    
    local valid=false
    for pattern in "${valid_patterns[@]}"; do
        if [[ "$branch_name" =~ $pattern ]]; then
            valid=true
            success "Branch name matches pattern: $pattern"
            break
        fi
    done
    
    if [ "$valid" = false ]; then
        error "Branch name '$branch_name' does not follow naming conventions"
        echo "Expected format: <lifecycle>/<type>/<component>[/<subcomponent>]"
        echo "Examples:"
        echo "  - develop/feature/user-authentication"
        echo "  - production/hotfix/critical-security-fix"
        echo "  - release/v1.2.0"
        echo "See VERSION_CONTROL_STANDARDS.md for details"
        return 1
    fi
    
    return 0
}

# Validate commit messages
validate_commit_messages() {
    local base_branch="${1:-origin/develop}"
    
    info "Validating commit messages against $base_branch"
    
    # Check if base branch exists
    if ! git rev-parse --verify "$base_branch" > /dev/null 2>&1; then
        warning "Base branch '$base_branch' not found, skipping commit validation"
        return 0
    fi
    
    # Get commits in current branch not in base branch
    local commits
    commits=$(git log "$base_branch"..HEAD --pretty=format:"%H|%s" 2>/dev/null || echo "")
    
    if [ -z "$commits" ]; then
        info "No commits to validate"
        return 0
    fi
    
    local invalid_count=0
    while IFS= read -r line; do
        if [ -z "$line" ]; then
            continue
        fi
        
        local hash=$(echo "$line" | cut -d'|' -f1)
        local message=$(echo "$line" | cut -d'|' -f2-)
        
        # Skip merge commits
        if [[ "$message" =~ ^Merge ]]; then
            continue
        fi
        
        # Conventional Commits pattern
        # Format: type(scope): subject or type: subject
        if [[ ! "$message" =~ ^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?:\ .+ ]]; then
            error "Invalid commit message format: $hash: $message"
            ((invalid_count++))
        else
            success "Valid commit: $message"
        fi
    done <<< "$commits"
    
    if [ $invalid_count -gt 0 ]; then
        echo ""
        echo "Expected format: <type>(<scope>): <subject>"
        echo "Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
        echo "Examples:"
        echo "  - feat(auth): add OAuth2 authentication"
        echo "  - fix: resolve memory leak"
        echo "  - docs: update installation guide"
        echo "See VERSION_CONTROL_STANDARDS.md for details"
        return 1
    fi
    
    return 0
}

# Validate markdown style (check for emoji)
validate_markdown_style() {
    info "Validating markdown style"
    
    # Find all markdown files
    local md_files
    md_files=$(find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*")
    
    if [ -z "$md_files" ]; then
        info "No markdown files found"
        return 0
    fi
    
    local emoji_found=false
    while IFS= read -r file; do
        # Check for emoji characters (actual emoji, not box-drawing/geometric)
        # Focus on emoji faces, symbols, and objects ranges
        # Skip files that don't exist or aren't readable
        if [ ! -f "$file" ] || [ ! -r "$file" ]; then
            warning "Cannot read file: $file"
            continue
        fi
        
        if python3 -c "
import re, sys
try:
    with open('$file', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        sys.exit(0 if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', content) else 1)
except Exception as e:
    print(f'Error reading file: {e}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null; then
            error "Emoji found in $file (violates MARKDOWN_STYLE_GUIDE.md)"
            emoji_found=true
        fi
    done <<< "$md_files"
    
    if [ "$emoji_found" = true ]; then
        echo ""
        echo "Our style guide prohibits emoji in documentation"
        echo "See MARKDOWN_STYLE_GUIDE.md section 'No Visual Embellishments'"
        return 1
    fi
    
    success "No emoji found in markdown files"
    return 0
}

# Main function
main() {
    local validate_all=true
    local validate_branch_flag=false
    local validate_commits_flag=false
    local validate_markdown_flag=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --branch)
                validate_branch_flag=true
                validate_all=false
                shift
                ;;
            --commits)
                validate_commits_flag=true
                validate_all=false
                shift
                ;;
            --markdown)
                validate_markdown_flag=true
                validate_all=false
                shift
                ;;
            --help)
                echo "Usage: $0 [--branch] [--commits] [--markdown]"
                echo ""
                echo "Options:"
                echo "  --branch    Validate branch name only"
                echo "  --commits   Validate commit messages only"
                echo "  --markdown  Validate markdown style only"
                echo "  --help      Show this help message"
                echo ""
                echo "If no options specified, validates all standards"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    echo "================================"
    echo "Version Control Standards Check"
    echo "================================"
    echo ""
    
    # Run validations
    if [ "$validate_all" = true ] || [ "$validate_branch_flag" = true ]; then
        validate_branch_name || true
        echo ""
    fi
    
    if [ "$validate_all" = true ] || [ "$validate_commits_flag" = true ]; then
        validate_commit_messages || true
        echo ""
    fi
    
    if [ "$validate_all" = true ] || [ "$validate_markdown_flag" = true ]; then
        validate_markdown_style || true
        echo ""
    fi
    
    # Summary
    echo "================================"
    echo "Validation Summary"
    echo "================================"
    if [ $ERRORS -eq 0 ]; then
        success "All checks passed!"
        if [ $WARNINGS -gt 0 ]; then
            echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
        fi
        exit 0
    else
        echo -e "${RED}Errors: $ERRORS${NC}"
        if [ $WARNINGS -gt 0 ]; then
            echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
        fi
        exit 1
    fi
}

# Run main function
main "$@"
