#!/bin/bash
# GitHub Projects Creation Script
# Creates all 7 comprehensive projects for the {{ORG_NAME}} organization
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
# - Organization admin permissions
# - Personal access token with project:write scope
#
# Usage: ./create-github-projects.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ORG_NAME="{{ORG_NAME}}"
REPO_NAME=".github"

# Project definitions
declare -A PROJECTS=(
    ["ai-framework"]="🤖 AI Framework Development|Development and maintenance of AI agents, MCP servers, custom instructions, and AI tooling|public"
    ["documentation"]="📚 Documentation & Knowledge|Documentation ecosystem including 133+ docs, guides, and knowledge base articles|public"
    ["workflow-automation"]="⚙️ Workflow & Automation|CI/CD pipelines, 98+ GitHub Actions workflows, and process automation|public"
    ["security-compliance"]="🔒 Security & Compliance|Security scanning, vulnerability tracking, incident response, and compliance|private"
    ["infrastructure-devops"]="🏗️ Infrastructure & DevOps|Infrastructure as code, cloud resources, deployments, and platform operations|public"
    ["community-engagement"]="👥 Community & Engagement|Open source community, contributor engagement, and support requests|public"
    ["product-roadmap"]="🚀 Product Roadmap|Strategic initiatives, feature planning, release management, and organizational roadmap|public"
)

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
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

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if gh is installed
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed. Please install it first."
        log_info "Visit: https://cli.github.com/"
        exit 1
    fi

    # Check if authenticated
    if ! gh auth status &> /dev/null; then
        log_error "Not authenticated with GitHub CLI."
        log_info "Run: gh auth login"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

create_project() {
    local project_key=$1
    local project_data=${PROJECTS[$project_key]}

    IFS='|' read -r title description visibility <<< "$project_data"

    log_info "Creating project: $title"

    # Create the project using GitHub CLI
    # Note: Projects V2 require GraphQL API calls
    local project_id
    project_id=$(gh api graphql -f query="
        mutation {
            createProjectV2(input: {
                ownerId: \"$(gh api graphql -f query='query { organization(login: \"'$ORG_NAME'\") { id } }' --jq '.data.organization.id')\"
                title: \"$title\"
                repositoryId: \"$(gh api repos/$ORG_NAME/$REPO_NAME --jq '.node_id')\"
            }) {
                projectV2 {
                    id
                    number
                    url
                }
            }
        }
    " --jq '.data.createProjectV2.projectV2.number' 2>&1)

    if [ $? -eq 0 ]; then
        log_success "Created project #$project_id: $title"
        echo "$project_key|$project_id" >> .project-ids.txt
    else
        log_error "Failed to create project: $title"
        log_error "Error: $project_id"
        return 1
    fi
}

create_all_projects() {
    log_info "Creating all projects for $ORG_NAME..."
    echo "# Project IDs for $ORG_NAME" > .project-ids.txt

    for project_key in "${!PROJECTS[@]}"; do
        create_project "$project_key" || true
        sleep 2  # Rate limiting
    done

    log_success "All projects created"
    log_info "Project IDs saved to .project-ids.txt"
}

display_summary() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "                  PROJECT CREATION SUMMARY"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""

    if [ -f .project-ids.txt ]; then
        log_info "Created projects:"
        while IFS='|' read -r key id; do
            if [ "$key" != "#" ]; then
                IFS='|' read -r title _ _ <<< "${PROJECTS[$key]}"
                echo "  • $title (#$id)"
                echo "    https://github.com/orgs/$ORG_NAME/projects/$id"
            fi
        done < .project-ids.txt
    fi

    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    log_info "Next steps:"
    echo "  1. Configure project fields (run: ./configure-project-fields.sh)"
    echo "  2. Create project views (run: ./create-project-views.sh)"
    echo "  3. Set up automation rules (run: ./setup-project-automation.sh)"
    echo "  4. Migrate existing issues/PRs (run: ./migrate-to-projects.sh)"
    echo ""
    log_info "Documentation: docs/GITHUB_PROJECTS_IMPLEMENTATION.md"
}

# Main execution
main() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "       GitHub Projects Setup for $ORG_NAME"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""

    check_prerequisites

    log_warning "This will create 7 new GitHub Projects in the $ORG_NAME organization."
    read -p "Continue? (y/n) " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Aborted by user"
        exit 0
    fi

    create_all_projects
    display_summary

    log_success "Setup complete!"
}

# Run main function
main "$@"
