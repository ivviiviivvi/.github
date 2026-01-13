#!/bin/bash

# Workspace Migration Script
# Migrate from old workspace setup to new containerized setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Workspace Migration Tool${NC}"
echo ""

# Help message
show_help() {
  cat <<EOF
Workspace Migration Script

Migrate from old workspace setup to new containerized workspace.

Usage: $(basename "$0") [OPTIONS]

Options:
  -s, --source DIR        Source workspace directory
  -t, --target DIR        Target workspace directory (default: source-containerized)
  -m, --template NAME     Template to use (default: fullstack)
  -b, --backup            Create backup before migration
  -d, --dry-run          Show what would be done without making changes
  -h, --help             Show this help message

Examples:
  # Basic migration
  $(basename "$0") --source ./old-project

  # Migration with backup
  $(basename "$0") --source ./old-project --backup

  # Dry run to preview changes
  $(basename "$0") --source ./old-project --dry-run

EOF
}

# Default values
SOURCE_DIR=""
TARGET_DIR=""
TEMPLATE="fullstack"
BACKUP=false
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -s|--source)
      SOURCE_DIR="$2"
      shift 2
      ;;
    -t|--target)
      TARGET_DIR="$2"
      shift 2
      ;;
    -m|--template)
      TEMPLATE="$2"
      shift 2
      ;;
    -b|--backup)
      BACKUP=true
      shift
      ;;
    -d|--dry-run)
      DRY_RUN=true
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

# Validate source directory
if [ -z "$SOURCE_DIR" ]; then
  echo -e "${RED}Error: Source directory is required${NC}"
  show_help
  exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
  echo -e "${RED}Error: Source directory does not exist: $SOURCE_DIR${NC}"
  exit 1
fi

# Set target directory
if [ -z "$TARGET_DIR" ]; then
  TARGET_DIR="${SOURCE_DIR}-containerized"
fi

echo -e "${BLUE}Migration Plan:${NC}"
echo "  Source: $SOURCE_DIR"
echo "  Target: $TARGET_DIR"
echo "  Template: $TEMPLATE"
echo "  Backup: $BACKUP"
echo "  Dry Run: $DRY_RUN"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}"
  echo ""
fi

# Step 1: Backup if requested
if [ "$BACKUP" = true ] && [ "$DRY_RUN" = false ]; then
  echo -e "${BLUE}📦 Creating backup...${NC}"
  BACKUP_NAME="${SOURCE_DIR}-backup-$(date +%Y%m%d_%H%M%S)"
  cp -r "$SOURCE_DIR" "$BACKUP_NAME"
  echo -e "${GREEN}✅ Backup created: $BACKUP_NAME${NC}"
  echo ""
fi

# Step 2: Analyze source workspace
echo -e "${BLUE}🔍 Analyzing source workspace...${NC}"

# Detect technologies
USES_NODE=false
USES_PYTHON=false
USES_DATABASE=false
USES_DOCKER=false

if [ -f "$SOURCE_DIR/package.json" ]; then
  USES_NODE=true
  echo "  ✅ Detected: Node.js"
fi

if [ -f "$SOURCE_DIR/requirements.txt" ] || [ -f "$SOURCE_DIR/pyproject.toml" ]; then
  USES_PYTHON=true
  echo "  ✅ Detected: Python"
fi

if grep -r "postgres\|mysql\|mongodb" "$SOURCE_DIR" >/dev/null 2>&1; then
  USES_DATABASE=true
  echo "  ✅ Detected: Database usage"
fi

if [ -f "$SOURCE_DIR/Dockerfile" ] || [ -f "$SOURCE_DIR/docker-compose.yml" ]; then
  USES_DOCKER=true
  echo "  ⚠️  Detected: Existing Docker configuration"
fi

echo ""

# Step 3: Create target workspace
if [ "$DRY_RUN" = false ]; then
  echo -e "${BLUE}📁 Creating target workspace...${NC}"
  mkdir -p "$TARGET_DIR"
else
  echo -e "${BLUE}📁 Would create target workspace: $TARGET_DIR${NC}"
fi

# Step 4: Copy source files
if [ "$DRY_RUN" = false ]; then
  echo -e "${BLUE}📋 Copying source files...${NC}"
  rsync -av \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='dist' \
    --exclude='build' \
    "$SOURCE_DIR/" "$TARGET_DIR/"
else
  echo -e "${BLUE}📋 Would copy source files (excluding .git, node_modules, etc.)${NC}"
fi

# Step 5: Add devcontainer configuration
if [ "$DRY_RUN" = false ]; then
  echo -e "${BLUE}🐳 Adding DevContainer configuration...${NC}"
  
  TEMPLATE_DIR=".devcontainer/templates/$TEMPLATE"
  if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${RED}Error: Template not found: $TEMPLATE${NC}"
    exit 1
  fi
  
  mkdir -p "$TARGET_DIR/.devcontainer"
  cp -r "$TEMPLATE_DIR"/* "$TARGET_DIR/.devcontainer/"
  
  echo -e "${GREEN}✅ DevContainer configuration added${NC}"
else
  echo -e "${BLUE}🐳 Would add DevContainer configuration from template: $TEMPLATE${NC}"
fi

# Step 6: Migrate environment variables
if [ -f "$SOURCE_DIR/.env" ]; then
  if [ "$DRY_RUN" = false ]; then
    echo -e "${BLUE}🔧 Migrating environment variables...${NC}"
    cp "$SOURCE_DIR/.env" "$TARGET_DIR/.env"
    echo -e "${GREEN}✅ Environment variables migrated${NC}"
  else
    echo -e "${BLUE}🔧 Would migrate .env file${NC}"
  fi
fi

# Step 7: Update configurations
if [ "$DRY_RUN" = false ]; then
  echo -e "${BLUE}⚙️  Updating configurations...${NC}"
  
  # Update database URLs to use service names
  if [ -f "$TARGET_DIR/.env" ]; then
    sed -i 's/localhost:5432/postgres:5432/g' "$TARGET_DIR/.env"
    sed -i 's/127.0.0.1:5432/postgres:5432/g' "$TARGET_DIR/.env"
    sed -i 's/localhost:6379/redis:6379/g' "$TARGET_DIR/.env"
    sed -i 's/127.0.0.1:6379/redis:6379/g' "$TARGET_DIR/.env"
    echo "  ✅ Updated database connection strings"
  fi
else
  echo -e "${BLUE}⚙️  Would update configurations (database URLs, etc.)${NC}"
fi

# Step 8: Create migration guide
if [ "$DRY_RUN" = false ]; then
  echo -e "${BLUE}📝 Creating migration guide...${NC}"
  
  cat > "$TARGET_DIR/MIGRATION_GUIDE.md" <<EOF
# Migration Guide

This workspace was migrated from \`$SOURCE_DIR\` on $(date).

## Template Used

- Template: $TEMPLATE

## Technologies Detected

- Node.js: $USES_NODE
- Python: $USES_PYTHON
- Database: $USES_DATABASE

## Next Steps

1. **Review the configuration**:
   \`\`\`bash
   cd $TARGET_DIR
   cat .devcontainer/devcontainer.json
   cat .devcontainer/docker-compose.yml
   \`\`\`

2. **Update environment variables**:
   \`\`\`bash
   # Edit .env file
   code .env
   \`\`\`

3. **Open in DevContainer**:
   \`\`\`bash
   cd $TARGET_DIR
   code .
   # Press F1 → Dev Containers: Reopen in Container
   \`\`\`

4. **Test the setup**:
   - Verify all services are running
   - Run tests
   - Check database connections

## Changes Made

- Added DevContainer configuration
- Updated database connection strings (localhost → service names)
- Copied source files (excluding dependencies)

## Rollback

If you need to rollback, you can:

1. Use the backup (if created): \`$BACKUP_NAME\`
2. Or copy from source: \`$SOURCE_DIR\`

## Support

See [Workspace Protocols](docs/WORKSPACE_CONTAINERIZATION_PROTOCOLS.md) for more information.
EOF

  echo -e "${GREEN}✅ Migration guide created${NC}"
else
  echo -e "${BLUE}📝 Would create MIGRATION_GUIDE.md${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}✅ Migration complete!${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}This was a dry run. No changes were made.${NC}"
  echo "Run without --dry-run to perform the actual migration."
else
  echo "Next steps:"
  echo "  1. cd $TARGET_DIR"
  echo "  2. Review MIGRATION_GUIDE.md"
  echo "  3. code ."
  echo "  4. Reopen in Container"
  
  if [ "$BACKUP" = true ]; then
    echo ""
    echo "Backup available at: $BACKUP_NAME"
  fi
fi

echo ""
echo "📖 See docs/WORKSPACE_CONTAINERIZATION_PROTOCOLS.md for more information"
