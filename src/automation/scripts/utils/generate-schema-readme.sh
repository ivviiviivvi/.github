#!/bin/bash
# Schema.org README Generator
# Automatically adds schema.org structured data to README files

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$REPO_ROOT/.schema-org"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Generate schema.org section for README
generate_schema_section() {
    cat << 'EOF'

---

## 📊 Structured Data

This repository uses [schema.org](https://schema.org) structured data for improved discoverability and machine-readability.

<details>
<summary>View Schema.org Metadata</summary>

### Organization
- [Organization Schema](.schema-org/organization.jsonld) - Organization information
- [Repository Schema](.schema-org/repository.jsonld) - Repository metadata
- [AI Framework Schema](.schema-org/ai-framework.jsonld) - AI framework details
- [Documentation Schema](.schema-org/documentation.jsonld) - Documentation metadata

### Benefits
- **Improved Discoverability**: Search engines and AI tools can better understand the repository
- **Machine-Readable**: Structured metadata for automated processing
- **Standards Compliance**: Following schema.org standards for code repositories
- **Enhanced Context**: Provides rich context for AI assistants and documentation tools

### Validation
```bash
# Validate schema.org files
python scripts/validate-schema-org.py
```

</details>

EOF
}

# Check if README has schema.org section
has_schema_section() {
    local readme="$1"
    grep -q "## 📊 Structured Data" "$readme" 2>/dev/null
}

# Add or update schema.org section in README
update_readme() {
    local readme="$1"

    if [ ! -f "$readme" ]; then
        log_warning "README not found: $readme"
        return 1
    fi

    log_info "Processing: $readme"

    if has_schema_section "$readme"; then
        log_info "Schema.org section already exists, skipping..."
        return 0
    fi

    # Backup original
    cp "$readme" "$readme.bak"

    # Append schema.org section
    generate_schema_section >> "$readme"

    log_success "Added schema.org section to $readme"
    return 0
}

main() {
    log_info "Schema.org README Generator"
    echo ""

    # Check if schema.org directory exists
    if [ ! -d "$SCHEMA_DIR" ]; then
        log_error "Schema.org directory not found: $SCHEMA_DIR"
        exit 1
    fi

    # Update main README
    update_readme "$REPO_ROOT/README.md"

    # Update AI framework README
    if [ -f "$REPO_ROOT/ai_framework/README.md" ]; then
        update_readme "$REPO_ROOT/ai_framework/README.md"
    fi

    # Update docs README if exists
    if [ -f "$REPO_ROOT/docs/README.md" ]; then
        update_readme "$REPO_ROOT/docs/README.md"
    fi

    echo ""
    log_success "Schema.org README generation complete!"
    log_info "Run 'python scripts/validate-schema-org.py' to validate the schema files"
}

main "$@"
