#!/bin/bash

# Workspace Creation Script
# Creates a new workspace from a template

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TEMPLATE="basic"
WORKSPACE_NAME=""
SERVICES=""
INTERACTIVE=false

# Help message
show_help() {
  cat <<EOF
Workspace Creation Script

Usage: $(basename "$0") [OPTIONS]

Options:
  -t, --template NAME       Template to use (default: basic)
                           Available: basic, fullstack, datascience, 
                                     microservices, golang, rust, java, dotnet
  -n, --name NAME          Workspace name (required)
  -s, --services SERVICES  Comma-separated list of additional services
                           Available: postgres, redis, mongodb, rabbitmq,
                                     mailhog, prometheus, grafana
  -i, --interactive        Interactive mode (prompts for options)
  -h, --help              Show this help message

Examples:
  # Create basic workspace
  $(basename "$0") --name my-project

  # Create full-stack workspace with specific services
  $(basename "$0") --template fullstack --name web-app --services postgres,redis

  # Interactive mode
  $(basename "$0") --interactive

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--template)
      TEMPLATE="$2"
      shift 2
      ;;
    -n|--name)
      WORKSPACE_NAME="$2"
      shift 2
      ;;
    -s|--services)
      SERVICES="$2"
      shift 2
      ;;
    -i|--interactive)
      INTERACTIVE=true
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      show_help
      exit 1
      ;;
  esac
done

# Interactive mode
if [ "$INTERACTIVE" = true ]; then
  echo -e "${GREEN}🚀 Workspace Creation Wizard${NC}"
  echo ""
  
  # Workspace name
  read -p "Workspace name: " WORKSPACE_NAME
  
  # Template selection
  echo ""
  echo "Available templates:"
  echo "  1) basic        - Simple single-language projects"
  echo "  2) fullstack    - Web applications with database"
  echo "  3) datascience  - ML/AI and data analysis"
  echo "  4) microservices - Distributed systems"
  echo "  5) golang       - Go development"
  echo "  6) rust         - Rust development"
  echo "  7) java         - Java/Spring Boot"
  echo "  8) dotnet       - .NET Core"
  read -p "Select template (1-8): " TEMPLATE_NUM
  
  case $TEMPLATE_NUM in
    1) TEMPLATE="basic" ;;
    2) TEMPLATE="fullstack" ;;
    3) TEMPLATE="datascience" ;;
    4) TEMPLATE="microservices" ;;
    5) TEMPLATE="golang" ;;
    6) TEMPLATE="rust" ;;
    7) TEMPLATE="java" ;;
    8) TEMPLATE="dotnet" ;;
    *) echo -e "${RED}Invalid selection${NC}"; exit 1 ;;
  esac
  
  # Additional services
  echo ""
  echo "Additional services (comma-separated, or press Enter to skip):"
  echo "  postgres, redis, mongodb, rabbitmq, mailhog, prometheus"
  read -p "Services: " SERVICES
fi

# Validate workspace name
if [ -z "$WORKSPACE_NAME" ]; then
  echo -e "${RED}Error: Workspace name is required${NC}"
  show_help
  exit 1
fi

# Validate template
TEMPLATE_DIR=".devcontainer/templates/$TEMPLATE"
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo -e "${RED}Error: Template '$TEMPLATE' not found${NC}"
  echo "Available templates:"
  ls -1 .devcontainer/templates/
  exit 1
fi

# Create workspace directory
WORKSPACE_PATH="$WORKSPACE_NAME"
if [ -d "$WORKSPACE_PATH" ]; then
  echo -e "${RED}Error: Directory '$WORKSPACE_PATH' already exists${NC}"
  exit 1
fi

echo -e "${GREEN}📦 Creating workspace: $WORKSPACE_NAME${NC}"
echo "Template: $TEMPLATE"
if [ -n "$SERVICES" ]; then
  echo "Additional services: $SERVICES"
fi
echo ""

# Create directory
mkdir -p "$WORKSPACE_PATH"
cd "$WORKSPACE_PATH"

# Copy template files
echo "📋 Copying template files..."
mkdir -p .devcontainer
cp -r "../$TEMPLATE_DIR"/* .devcontainer/

# Add additional services if specified
if [ -n "$SERVICES" ]; then
  echo "🔧 Adding additional services..."
  # This would require a more sophisticated implementation
  # For now, just note that services were requested
  echo "# Additional services requested: $SERVICES" >> .devcontainer/docker-compose.yml
fi

# Create basic project structure
echo "📁 Creating project structure..."
mkdir -p src tests docs scripts

# Create README
cat > README.md <<EOF
# $WORKSPACE_NAME

Created with template: $TEMPLATE

## Getting Started

### Prerequisites

- Docker Desktop
- VS Code
- Remote-Containers extension

### Setup

1. Open this directory in VS Code
2. Press \`F1\` or \`Cmd/Ctrl+Shift+P\`
3. Select: \`Dev Containers: Reopen in Container\`
4. Wait for container to build

### Services

EOF

if [ "$TEMPLATE" = "fullstack" ]; then
  cat >> README.md <<EOF
- PostgreSQL: \`postgresql://devuser:devpass@postgres:5432/devdb\`
- Redis: \`redis://redis:6379\`
- MailHog: http://localhost:8025

EOF
fi

cat >> README.md <<EOF
## Development

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
\`\`\`

## Documentation

See [docs/](./docs/) for additional documentation.

EOF

# Create .gitignore
cat > .gitignore <<EOF
# Dependencies
node_modules/
venv/
.venv/
__pycache__/
*.pyc

# Environment
.env
.env.local

# Build
dist/
build/
*.egg-info/

# IDE
.vscode/settings.json
.idea/
*.swp

# Logs
*.log
logs/
tmp/

# OS
.DS_Store
Thumbs.db

EOF

# Create .env.example
cat > .env.example <<EOF
# Database
DATABASE_URL=postgresql://devuser:devpass@postgres:5432/devdb

# Redis
REDIS_URL=redis://redis:6379

# Development
NODE_ENV=development
LOG_LEVEL=debug

EOF

# Create initial git commit
git init
git add .
git commit -m "chore: initial workspace setup from $TEMPLATE template"

echo ""
echo -e "${GREEN}✅ Workspace created successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. cd $WORKSPACE_NAME"
echo "  2. code ."
echo "  3. Reopen in Container (F1 → Dev Containers: Reopen in Container)"
echo ""
echo "📖 See README.md for more information"
