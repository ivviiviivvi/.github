#!/bin/bash
# Deploy GitHub Projects using 1Password CLI for token retrieval
# Usage: ./deploy-with-1password.sh

set -e

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if 1Password CLI is installed
if ! command -v op &> /dev/null; then
    log_error "1Password CLI (op) not found"
    echo ""
    echo "Install instructions:"
    echo "  macOS:  brew install --cask 1password-cli"
    echo "  Linux:  https://developer.1password.com/docs/cli/get-started/"
    echo ""
    exit 1
fi

log_success "1Password CLI found: $(op --version)"

# Check if signed in to 1Password
if ! op account get &> /dev/null; then
    log_warning "Not signed in to 1Password"
    log_info "Signing in to 1Password..."
    eval $(op signin)
fi

log_success "Signed in to 1Password"

# Retrieve GitHub PAT from 1Password
log_info "Retrieving GitHub PAT from 1Password..."

# Default 1Password reference - adjust if your setup is different
OP_REFERENCE="${OP_REFERENCE:-op://Private/GitHub PAT/credential}"

log_info "Using 1Password reference: $OP_REFERENCE"
log_warning "If this is incorrect, set OP_REFERENCE environment variable"
log_info "Example: export OP_REFERENCE='op://YourVault/YourItem/fieldname'"
echo ""

# Retrieve token
if ! GH_TOKEN=$(op read "$OP_REFERENCE" 2>&1); then
    log_error "Failed to retrieve token from 1Password"
    echo ""
    echo "Error: $GH_TOKEN"
    echo ""
    echo "To find your token location:"
    echo "  1. List vaults:  op vault list"
    echo "  2. List items:   op item list --vault YourVaultName"
    echo "  3. View item:    op item get 'GitHub PAT' --vault YourVaultName"
    echo ""
    exit 1
fi

export GH_TOKEN

log_success "Token retrieved successfully: ${GH_TOKEN:0:4}..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 not found"
    exit 1
fi

log_success "Python found: $(python3 --version)"

# Check if requests library is installed
if ! python3 -c "import requests" &> /dev/null; then
    log_warning "requests library not found"
    log_info "Installing requests..."
    pip install requests
fi

log_success "requests library available"

# Determine dry run mode
DRY_RUN=""
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN="--dry-run"
    log_warning "Running in DRY RUN mode (no changes will be made)"
    echo ""
fi

# Get organization name
ORG_NAME="${ORG_NAME:-{{ORG_NAME}}}"
log_info "Target organization: $ORG_NAME"

# Confirm before proceeding (unless dry run)
if [[ -z "$DRY_RUN" ]]; then
    echo ""
    echo "This will create 7 GitHub Projects in organization: $ORG_NAME"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Deployment cancelled"
        exit 0
    fi
fi

echo ""
log_info "Starting GitHub Projects deployment..."
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Run the Python configuration script
if python3 configure-github-projects.py --org "$ORG_NAME" $DRY_RUN 2>&1 | tee projects-deployment-$(date +%Y%m%d-%H%M%S).log; then
    echo ""
    log_success "Deployment completed successfully!"
    echo ""

    if [[ -z "$DRY_RUN" ]]; then
        log_info "View your projects at: https://github.com/orgs/$ORG_NAME/projects"
        echo ""
        log_info "Next steps:"
        echo "  1. Configure views in each project"
        echo "  2. Set up automation rules"
        echo "  3. Train your team"
        echo "  4. Start adding items"
        echo ""
        log_info "See GITHUB_PROJECTS_DEPLOYMENT.md for detailed checklist"
    else
        log_info "Dry run completed. Review the output above."
        log_info "To deploy for real, run without --dry-run flag"
    fi
else
    echo ""
    log_error "Deployment failed! Check the log file for details."
    exit 1
fi
