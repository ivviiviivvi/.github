#!/bin/bash
# Pre-deployment verification script
# Checks all prerequisites before deploying GitHub Projects

# Don't exit on error - we want to check everything
set +e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

echo "========================================="
echo "GitHub Projects Deployment Verification"
echo "========================================="
echo ""

CHECKS_PASSED=0
CHECKS_FAILED=0

# Check 1: Python 3.8+
log_info "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log_success "Python $PYTHON_VERSION installed"
    ((CHECKS_PASSED++))
else
    log_error "Python 3 not found"
    ((CHECKS_FAILED++))
fi

# Check 2: requests library
log_info "Checking requests library..."
if python3 -c "import requests" &> /dev/null; then
    log_success "requests library installed"
    ((CHECKS_PASSED++))
else
    log_error "requests library not found (run: pip install requests)"
    ((CHECKS_FAILED++))
fi

# Check 3: GitHub CLI
log_info "Checking GitHub CLI..."
if command -v gh &> /dev/null; then
    GH_VERSION=$(gh --version | head -1 | cut -d' ' -f3)
    log_success "GitHub CLI $GH_VERSION installed"
    ((CHECKS_PASSED++))
else
    log_warning "GitHub CLI not found (optional but recommended)"
fi

# Check 4: GitHub CLI authentication
log_info "Checking GitHub authentication..."
if gh auth status &> /dev/null; then
    GH_USER=$(gh api user --jq .login 2>/dev/null || echo "unknown")
    log_success "Authenticated as: $GH_USER"
    ((CHECKS_PASSED++))
else
    log_warning "GitHub CLI not authenticated (may need GH_TOKEN)"
fi

# Check 5: 1Password CLI
log_info "Checking 1Password CLI..."
if command -v op &> /dev/null; then
    OP_VERSION=$(op --version 2>/dev/null || echo "unknown")
    log_success "1Password CLI $OP_VERSION installed"
    ((CHECKS_PASSED++))

    # Check 1Password authentication
    log_info "Checking 1Password authentication..."
    if op account list &> /dev/null; then
        log_success "Signed in to 1Password"
        ((CHECKS_PASSED++))
    else
        log_warning "Not signed in to 1Password (run: eval \$(op signin))"
    fi
else
    log_warning "1Password CLI not found (can use manual token instead)"
fi

# Check 6: Organization access
log_info "Checking organization access..."
if gh api orgs/{{ORG_NAME}} --jq .login &> /dev/null; then
    log_success "Can access organization: {{ORG_NAME}}"
    ((CHECKS_PASSED++))
else
    log_warning "Cannot verify org access (may need proper token scopes)"
fi

# Check 7: Existing projects
log_info "Checking for existing projects..."
EXISTING_PROJECTS=$(gh api graphql -f query='
  query {
    organization(login: "{{ORG_NAME}}") {
      projectsV2(first: 100) {
        totalCount
      }
    }
  }
' --jq '.data.organization.projectsV2.totalCount' 2>/dev/null || echo "0")

if [[ "$EXISTING_PROJECTS" == "0" ]]; then
    log_success "No existing projects (clean slate)"
    ((CHECKS_PASSED++))
else
    log_warning "$EXISTING_PROJECTS projects already exist"
fi

# Check 8: Scripts present
log_info "Checking deployment scripts..."
if [[ -f "configure-github-projects.py" ]] && [[ -x "configure-github-projects.py" ]]; then
    log_success "Python script present and executable"
    ((CHECKS_PASSED++))
else
    log_error "configure-github-projects.py not found or not executable"
    ((CHECKS_FAILED++))
fi

if [[ -f "deploy-with-1password.sh" ]] && [[ -x "deploy-with-1password.sh" ]]; then
    log_success "1Password deployment script ready"
    ((CHECKS_PASSED++))
else
    log_warning "deploy-with-1password.sh not found or not executable"
fi

echo ""
echo "========================================="
echo "Verification Summary"
echo "========================================="
echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"
if [[ $CHECKS_FAILED -gt 0 ]]; then
    echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
fi
echo ""

if [[ $CHECKS_FAILED -eq 0 ]]; then
    log_success "All critical checks passed! Ready to deploy."
    echo ""
    echo "Next steps:"
    echo "  1. Test with dry run:"
    echo "     ./deploy-with-1password.sh --dry-run"
    echo ""
    echo "  2. Deploy for real:"
    echo "     ./deploy-with-1password.sh"
    echo ""
    exit 0
else
    log_error "Some checks failed. Fix issues above before deploying."
    exit 1
fi
