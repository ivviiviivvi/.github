#!/bin/bash

################################################################################
# Bootstrap Video Walkthrough System - Organization-Wide Deployment
################################################################################
#
# This script deploys the video walkthrough generation infrastructure to all
# repositories in the Ivviiviivvi organization.
#
# Usage:
#   ./bootstrap-walkthrough-org.sh [OPTIONS]
#
# Options:
#   --org NAME              Organization name (default: Ivviiviivvi)
#   --token TOKEN           GitHub token for API access (default: $GITHUB_TOKEN)
#   --exclude REPO          Exclude specific repository (can be used multiple times)
#   --dry-run               Preview changes without making them
#   --batch-size N          Process N repositories at a time (default: 5)
#   --skip-archived         Skip archived repositories (default: true)
#   --skip-forks            Skip forked repositories (default: true)
#   --help                  Show this help message
#
# Environment Variables:
#   GITHUB_TOKEN            GitHub personal access token with repo permissions
#
# Examples:
#   # Preview deployment
#   ./bootstrap-walkthrough-org.sh --dry-run
#
#   # Deploy to specific organization
#   ./bootstrap-walkthrough-org.sh --org MyOrg --token $MY_TOKEN
#
#   # Exclude specific repositories
#   ./bootstrap-walkthrough-org.sh --exclude .github --exclude docs
#
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ORG_NAME="${ORG_NAME:-Ivviiviivvi}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
DRY_RUN=false
BATCH_SIZE=5
SKIP_ARCHIVED=true
SKIP_FORKS=true
EXCLUDED_REPOS=()
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Statistics
TOTAL_REPOS=0
PROCESSED_REPOS=0
SKIPPED_REPOS=0
FAILED_REPOS=0
SUCCESS_REPOS=0

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Video Walkthrough Bootstrap - Organization Deployment        ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

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

print_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Deploy video walkthrough generation infrastructure to all organization repositories.

OPTIONS:
    --org NAME              Organization name (default: Ivviiviivvi)
    --token TOKEN           GitHub token for API access
    --exclude REPO          Exclude specific repository (can be used multiple times)
    --dry-run               Preview changes without making them
    --batch-size N          Process N repositories at a time (default: 5)
    --skip-archived         Skip archived repositories (default: true)
    --skip-forks            Skip forked repositories (default: true)
    --help                  Show this help message

EXAMPLES:
    # Preview deployment
    $0 --dry-run

    # Deploy to specific organization
    $0 --org MyOrg --token \$MY_TOKEN

    # Exclude specific repositories
    $0 --exclude .github --exclude docs

ENVIRONMENT VARIABLES:
    GITHUB_TOKEN            GitHub personal access token with repo permissions

For more information, see .github/WALKTHROUGH_GUIDE.md
EOF
}

################################################################################
# Parse Command Line Arguments
################################################################################

while [[ $# -gt 0 ]]; do
    case $1 in
        --org)
            ORG_NAME="$2"
            shift 2
            ;;
        --token)
            GITHUB_TOKEN="$2"
            shift 2
            ;;
        --exclude)
            EXCLUDED_REPOS+=("$2")
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --batch-size)
            BATCH_SIZE="$2"
            shift 2
            ;;
        --skip-archived)
            SKIP_ARCHIVED=true
            shift
            ;;
        --skip-forks)
            SKIP_FORKS=true
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

################################################################################
# Validation
################################################################################

validate_environment() {
    print_info "Validating environment..."

    # Check for required commands
    local required_commands=("gh" "git" "jq" "curl")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            print_error "Required command not found: $cmd"
            echo "Please install $cmd and try again."
            exit 1
        fi
    done

    # Check GitHub token
    if [ -z "$GITHUB_TOKEN" ]; then
        print_error "GitHub token not provided"
        echo "Please set GITHUB_TOKEN environment variable or use --token option"
        exit 1
    fi

    # Validate GitHub token
    if ! gh auth status &> /dev/null; then
        print_error "GitHub CLI authentication failed"
        echo "Please run: gh auth login"
        exit 1
    fi

    # Check if workflow files exist
    local workflow_file="${REPO_ROOT}/.github/workflows/generate-walkthrough.yml"
    local config_file="${REPO_ROOT}/.github/walkthrough-config.yml"

    if [ ! -f "$workflow_file" ]; then
        print_error "Workflow file not found: $workflow_file"
        exit 1
    fi

    if [ ! -f "$config_file" ]; then
        print_error "Configuration file not found: $config_file"
        exit 1
    fi

    print_success "Environment validation complete"
}

################################################################################
# Repository Functions
################################################################################

is_excluded_repo() {
    local repo_name="$1"

    # Check exact matches
    for excluded in "${EXCLUDED_REPOS[@]}"; do
        if [ "$repo_name" = "$excluded" ]; then
            return 0
        fi
    done

    # Check patterns from config
    if [[ "$repo_name" =~ ^test-.* ]] || \
       [[ "$repo_name" =~ ^demo-.* ]] || \
       [[ "$repo_name" =~ .*-archive$ ]] || \
       [[ "$repo_name" =~ .*-deprecated$ ]]; then
        return 0
    fi

    return 1
}

get_repositories() {
    print_info "Fetching repositories from organization: $ORG_NAME"

    local filter_archived=""
    local filter_forks=""

    if [ "$SKIP_ARCHIVED" = true ]; then
        filter_archived="--archived=false"
    fi

    if [ "$SKIP_FORKS" = true ]; then
        filter_forks="--no-forks"
    fi

    # Get repositories using GitHub CLI with pagination support
    # Default limit is high but should handle most organizations
    local repos=$(gh repo list "$ORG_NAME" \
        --limit 1000 \
        --json name,isArchived,isFork,isPrivate \
        $filter_archived \
        | jq -r '.[].name')

    # Warn if approaching limit
    local count=$(echo "$repos" | wc -l)
    if [ "$count" -ge 900 ]; then
        print_warning "Approaching repository limit (${count}/1000). Some repos may be missed."
        print_warning "Consider filtering by topic or other criteria."
    fi

    echo "$repos"
}

clone_repository() {
    local repo_name="$1"
    local temp_dir="$2"

    print_info "Cloning repository: $repo_name"

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY RUN] Would clone: $ORG_NAME/$repo_name"
        return 0
    fi

    gh repo clone "$ORG_NAME/$repo_name" "$temp_dir/$repo_name" -- --quiet 2>/dev/null || {
        print_error "Failed to clone repository: $repo_name"
        return 1
    }

    return 0
}

copy_workflow_files() {
    local repo_dir="$1"
    local repo_name="$2"

    print_info "Copying workflow files to: $repo_name"

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY RUN] Would copy workflow files to: $repo_name"
        return 0
    fi

    # Create .github/workflows directory if it doesn't exist
    mkdir -p "$repo_dir/.github/workflows"

    # Copy workflow file
    cp "${REPO_ROOT}/.github/workflows/generate-walkthrough.yml" \
       "$repo_dir/.github/workflows/" || {
        print_error "Failed to copy workflow file"
        return 1
    }

    # Copy configuration file
    cp "${REPO_ROOT}/.github/walkthrough-config.yml" \
       "$repo_dir/.github/" || {
        print_error "Failed to copy configuration file"
        return 1
    }

    print_success "Files copied successfully"
    return 0
}

create_pr() {
    local repo_dir="$1"
    local repo_name="$2"

    print_info "Creating pull request for: $repo_name"

    cd "$repo_dir" || return 1

    # Configure git
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"

    # Create branch
    local branch_name="feature/add-video-walkthrough-$(date +%Y%m%d)"
    local unique_suffix=""

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY RUN] Would create PR in: $repo_name"
        return 0
    fi

    # Check if branch already exists and add unique identifier
    if git ls-remote --heads origin "$branch_name" | grep -q "$branch_name"; then
        print_warning "Branch already exists: $branch_name"
        # Use repository name and timestamp for uniqueness
        unique_suffix="-${repo_name}-$(date +%H%M%S)"
        branch_name="${branch_name}${unique_suffix}"
    fi

    git checkout -b "$branch_name" 2>/dev/null || {
        print_error "Failed to create branch"
        return 1
    }

    # Add files
    git add .github/workflows/generate-walkthrough.yml .github/walkthrough-config.yml

    # Check if there are changes to commit
    if git diff --staged --quiet; then
        print_warning "No changes to commit for: $repo_name"
        return 0
    fi

    # Commit changes
    git commit -m "feat: add video walkthrough generation

This PR adds automated video walkthrough generation infrastructure to this repository.

Features:
- Automatic application detection
- AI-powered voiceover
- Automatic PR creation with video artifacts
- Configurable duration and style

For more information, see:
https://github.com/$ORG_NAME/.github/blob/main/.github/WALKTHROUGH_GUIDE.md" || {
        print_error "Failed to commit changes"
        return 1
    }

    # Push branch
    git push origin "$branch_name" || {
        print_error "Failed to push branch"
        return 1
    }

    # Create PR using GitHub CLI
    gh pr create \
        --title "feat: Add video walkthrough generation" \
        --body "## 🎥 Add Video Walkthrough Generation

This PR adds automated video walkthrough generation infrastructure to this repository.

### What's Included

- ✅ GitHub Actions workflow for automatic video generation
- ✅ Configuration file for customization
- ✅ Support for automatic application detection
- ✅ AI-powered voiceover with multiple styles
- ✅ Automatic PR creation with video artifacts

### Features

- **Automatic Detection**: Supports React, Vue, Angular, Python, Java, and more
- **Customizable**: Configure duration, voiceover style, and focus areas
- **Autonomous**: Runs automatically on code changes or manual trigger
- **Professional Output**: High-quality videos with subtitles

### Usage

1. **Manual Trigger**: Go to Actions → Generate Video Walkthrough → Run workflow
2. **Automatic**: Push changes to main/develop branches
3. **Configuration**: Edit \`.github/walkthrough-config.yml\` to customize

### Documentation

For detailed information, see the [Walkthrough Guide](https://github.com/$ORG_NAME/.github/blob/main/.github/WALKTHROUGH_GUIDE.md).

### Testing

After merging, you can trigger the workflow manually to generate your first walkthrough:

1. Go to the Actions tab
2. Select \"Generate Video Walkthrough\"
3. Click \"Run workflow\"
4. Review the generated PR with video artifacts

---

**Generated by**: Video Walkthrough Bootstrap Script
**Organization**: $ORG_NAME
**Date**: $(date +%Y-%m-%d)" \
        --head "$branch_name" \
        --label "automated,documentation,enhancement" || {
        print_error "Failed to create PR"
        return 1
    }

    print_success "PR created successfully for: $repo_name"
    return 0
}

process_repository() {
    local repo_name="$1"
    local temp_dir="$2"

    echo ""
    print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_info "Processing repository: $repo_name"
    print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Check if repository should be excluded
    if is_excluded_repo "$repo_name"; then
        print_warning "Skipping excluded repository: $repo_name"
        SKIPPED_REPOS=$((SKIPPED_REPOS + 1))
        return 0
    fi

    # Clone repository
    if ! clone_repository "$repo_name" "$temp_dir"; then
        FAILED_REPOS=$((FAILED_REPOS + 1))
        return 1
    fi

    local repo_dir="$temp_dir/$repo_name"

    # Copy workflow files
    if ! copy_workflow_files "$repo_dir" "$repo_name"; then
        FAILED_REPOS=$((FAILED_REPOS + 1))
        return 1
    fi

    # Create PR
    if ! create_pr "$repo_dir" "$repo_name"; then
        FAILED_REPOS=$((FAILED_REPOS + 1))
        return 1
    fi

    SUCCESS_REPOS=$((SUCCESS_REPOS + 1))
    PROCESSED_REPOS=$((PROCESSED_REPOS + 1))

    print_success "Successfully processed: $repo_name"
    return 0
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header

    # Validate environment
    validate_environment

    # Show configuration
    echo ""
    print_info "Configuration:"
    echo "  Organization: $ORG_NAME"
    echo "  Dry Run: $DRY_RUN"
    echo "  Batch Size: $BATCH_SIZE"
    echo "  Skip Archived: $SKIP_ARCHIVED"
    echo "  Skip Forks: $SKIP_FORKS"
    echo "  Excluded Repos: ${EXCLUDED_REPOS[*]:-none}"
    echo ""

    # Get repositories
    local repos=$(get_repositories)
    TOTAL_REPOS=$(echo "$repos" | wc -l)

    if [ -z "$repos" ]; then
        print_error "No repositories found in organization: $ORG_NAME"
        exit 1
    fi

    print_success "Found $TOTAL_REPOS repositories"

    # Confirm before proceeding
    if [ "$DRY_RUN" = false ]; then
        echo ""
        print_warning "This will create PRs in $TOTAL_REPOS repositories."
        read -p "Do you want to continue? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Aborted by user"
            exit 0
        fi
    fi

    # Create temporary directory
    local temp_dir=$(mktemp -d)
    trap "rm -rf $temp_dir" EXIT

    # Process repositories
    local count=0
    for repo in $repos; do
        count=$((count + 1))

        print_info "Progress: $count/$TOTAL_REPOS"

        process_repository "$repo" "$temp_dir" || true

        # Batch processing delay
        if [ $((count % BATCH_SIZE)) -eq 0 ] && [ "$DRY_RUN" = false ]; then
            print_info "Batch complete. Waiting 10 seconds..."
            sleep 10
        fi
    done

    # Print summary
    echo ""
    echo ""
    print_header
    print_info "Deployment Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Total Repositories: $TOTAL_REPOS"
    echo "  Processed: $PROCESSED_REPOS"
    echo "  Successful: $SUCCESS_REPOS"
    echo "  Skipped: $SKIPPED_REPOS"
    echo "  Failed: $FAILED_REPOS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [ $FAILED_REPOS -gt 0 ]; then
        echo ""
        print_warning "Some repositories failed to process. Please review the logs above."
        exit 1
    fi

    if [ "$DRY_RUN" = true ]; then
        echo ""
        print_info "Dry run complete. Run without --dry-run to apply changes."
    else
        echo ""
        print_success "Deployment complete! PRs have been created in all repositories."
        print_info "Next steps:"
        echo "  1. Review and merge the PRs in each repository"
        echo "  2. Test the workflow by manually triggering it"
        echo "  3. Monitor the first few video generations"
        echo "  4. Adjust configuration as needed"
    fi
}

# Run main function
main
