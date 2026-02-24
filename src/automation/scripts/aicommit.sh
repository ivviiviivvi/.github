#!/bin/bash
#
# aicommit.sh - AI-powered commit message generator
#
# Generates Conventional Commits format messages using GitHub Copilot CLI
# or falls back to template-based generation.
#
# Usage:
#   ./scripts/aicommit.sh                    # Generate AI commit message
#   ./scripts/aicommit.sh "quick fix"        # Use custom message
#
# Requirements:
#   - git
#   - gh (GitHub CLI) with Copilot extension (optional but recommended)
#
# Author: AI-accelerated development workflow
# Version: 1.0.0

set -e

# ============================================================================
# Configuration
# ============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================

# Print colored message
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Print section header
print_header() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Check if gh copilot is available
has_gh_copilot() {
    if command -v gh &> /dev/null; then
        if gh copilot --help &> /dev/null; then
            return 0
        fi
    fi
    return 1
}

# Get staged files
get_staged_files() {
    git diff --cached --name-only
}

# Get diff stats
get_diff_stats() {
    git diff --cached --stat
}

# Determine scope from file paths
determine_scope() {
    local files="$1"

    # Check for common patterns
    if echo "$files" | grep -q "^\.github/workflows/"; then
        echo "ci"
    elif echo "$files" | grep -q "^\.github/"; then
        echo "github"
    elif echo "$files" | grep -q "^scripts/"; then
        echo "scripts"
    elif echo "$files" | grep -q "^docs/\|^.*\.md$"; then
        echo "docs"
    elif echo "$files" | grep -q "^tests\?/"; then
        echo "test"
    elif echo "$files" | grep -q "^src/api/\|^api/"; then
        echo "api"
    elif echo "$files" | grep -q "^src/auth/\|^auth/"; then
        echo "auth"
    elif echo "$files" | grep -q "^src/ui/\|^ui/\|^frontend/"; then
        echo "ui"
    elif echo "$files" | grep -q "^src/db/\|^database/\|^migrations/"; then
        echo "db"
    elif echo "$files" | grep -q "^src/"; then
        echo "core"
    elif echo "$files" | grep -q "requirements.*\.txt\|package\.json\|Gemfile\|go\.mod"; then
        echo "deps"
    elif echo "$files" | grep -q "Dockerfile\|docker-compose"; then
        echo "docker"
    elif echo "$files" | grep -q "\.ya?ml$"; then
        echo "config"
    else
        # Default: no scope
        echo ""
    fi
}

# Determine commit type from changes
determine_type() {
    local files="$1"
    local diff_content="$2"

    # Security-related changes
    if echo "$files" | grep -q "SECURITY\|bandit\|\.secrets"; then
        echo "security"
        return
    fi

    # Documentation changes
    if echo "$files" | grep -q "\.md$\|^docs/"; then
        echo "docs"
        return
    fi

    # Test changes
    if echo "$files" | grep -q "^tests\?/\|test_.*\.py\|.*_test\.py"; then
        echo "test"
        return
    fi

    # CI/CD changes
    if echo "$files" | grep -q "^\.github/workflows/\|\.travis\|\.circleci"; then
        echo "ci"
        return
    fi

    # Configuration changes
    if echo "$files" | grep -q "\.ya?ml$\|\.json$\|\.toml$\|\.ini$\|\.conf$"; then
        echo "chore"
        return
    fi

    # Dependency changes
    if echo "$files" | grep -q "requirements.*\.txt\|package\.json\|Gemfile\|go\.mod"; then
        echo "chore"
        return
    fi

    # Check diff for indicators
    if echo "$diff_content" | grep -qi "fix\|bug\|patch\|correct"; then
        echo "fix"
        return
    fi

    # Default to feat for code changes
    if echo "$files" | grep -q "\.py$\|\.js$\|\.ts$\|\.go$\|\.rb$\|\.java$"; then
        echo "feat"
        return
    fi

    # Default
    echo "chore"
}

# Generate commit message using templates
generate_template_message() {
    local files="$1"

    # Determine type and scope
    local type
    type=$(determine_type "$files" "$(git diff --cached)")
    local scope
    scope=$(determine_scope "$files")

    # Count changes
    local num_files
    num_files=$(echo "$files" | wc -l)

    # Generate description
    local description=""

    if [ "$type" = "docs" ]; then
        description="update documentation"
    elif [ "$type" = "test" ]; then
        description="add/update tests"
    elif [ "$type" = "fix" ]; then
        description="resolve issue in $scope"
    elif [ "$type" = "feat" ]; then
        description="add new functionality"
    elif [ "$type" = "security" ]; then
        description="address security vulnerability"
    elif [ "$type" = "chore" ]; then
        if echo "$files" | grep -q "requirements.*\.txt\|package\.json"; then
            description="update dependencies"
        else
            description="update configuration"
        fi
    else
        description="update $scope"
    fi

    # Build message
    if [ -n "$scope" ]; then
        echo "${type}(${scope}): ${description}"
    else
        echo "${type}: ${description}"
    fi
}

# Generate commit message using GitHub Copilot
generate_copilot_message() {
    print_info "Generating commit message with GitHub Copilot..."

    # Get diff
    local diff_output
    diff_output=$(git diff --cached)

    # Create prompt for Copilot
    local prompt="Generate a conventional commit message for these changes. Use format: type(scope): description

Types: feat, fix, docs, style, refactor, test, chore, security, perf
Description should be imperative mood (e.g., 'add' not 'added')
Keep it under 72 characters.

Changes:
$diff_output
"

    # Create secure temporary file
    local tmp_file
    tmp_file=$(mktemp)
    trap 'rm -f "$tmp_file"' EXIT

    # Try to use gh copilot suggest
    if echo "$prompt" | gh copilot suggest --target shell 2>/dev/null | grep -E "^(feat|fix|docs|style|refactor|test|chore|security|perf)" > "$tmp_file"; then
        cat "$tmp_file"
        return 0
    fi

    return 1
}

# ============================================================================
# Main Function
# ============================================================================

main() {
    print_header "AI Commit Message Generator"

    # Check for staged changes
    if ! git diff --cached --quiet; then
        :  # Has staged changes
    else
        print_error "No staged changes found."
        print_info "Stage changes with: git add <files>"
        exit 1
    fi

    # Get staged files
    local staged_files
    staged_files=$(get_staged_files)
    local num_files
    num_files=$(echo "$staged_files" | wc -l)

    print_info "Staged files: $num_files"
    echo "$staged_files" | sed 's/^/  - /'
    echo ""

    # Show diff stats
    print_info "Changes:"
    get_diff_stats | sed 's/^/  /'
    echo ""

    # Generate commit message
    local commit_msg=""

    # Check if user provided message
    if [ $# -gt 0 ]; then
        commit_msg="$*"
        print_info "Using provided message: $commit_msg"
    else
        # Try GitHub Copilot first
        if has_gh_copilot; then
            commit_msg=$(generate_copilot_message)

            if [ $? -eq 0 ] && [ -n "$commit_msg" ]; then
                print_success "Generated with GitHub Copilot"
            else
                print_warning "Copilot generation failed, using template"
                commit_msg=$(generate_template_message "$staged_files" "$(get_diff_stats)")
            fi
        else
            print_info "GitHub Copilot not available, using template"
            commit_msg=$(generate_template_message "$staged_files" "$(get_diff_stats)")
        fi
    fi

    # Show generated message
    print_header "Generated Commit Message"
    echo -e "${GREEN}$commit_msg${NC}"
    echo ""

    # Confirm with user
    print_info "Commit with this message? [Y/n/e(dit)] "
    read -r response

    case "$response" in
        [nN]*)
            print_warning "Commit cancelled."
            exit 0
            ;;
        [eE]*)
            print_info "Enter your commit message:"
            read -r custom_msg
            if [ -z "$custom_msg" ]; then
                print_error "Empty message, commit cancelled."
                exit 1
            fi
            commit_msg="$custom_msg"
            ;;
        *)
            # Default: yes
            ;;
    esac

    # Commit
    print_info "Committing..."

    if git commit -m "$commit_msg"; then
        print_success "Committed successfully!"
        echo ""
        print_info "Last commit:"
        git log -1 --oneline
    else
        print_error "Commit failed!"
        exit 1
    fi
}

# ============================================================================
# Entry Point
# ============================================================================

main "$@"
