#!/usr/bin/env bash
# generate_context.sh - Generate context payload for AI session handoffs
#
# Usage:
#   ./generate_context.sh [LEVEL] [STATE_FILE]
#
# Arguments:
#   LEVEL       - Compression level: minimal, standard (default), or full
#   STATE_FILE  - Path to orchestrator state file (default: .orchestrator_state.json)
#
# Examples:
#   ./generate_context.sh                    # Standard level, default state file
#   ./generate_context.sh minimal            # Minimal level, default state file
#   ./generate_context.sh standard my_state.json  # Standard level, custom state file
#
# Environment Variables:
#   PYTHON      - Python executable to use (default: python3)
#   OUTPUT      - Output file path (default: context_payload.json)

set -euo pipefail

# Configuration
PYTHON="${PYTHON:-python3}"
LEVEL="${1:-standard}"
STATE_FILE="${2:-.orchestrator_state.json}"
OUTPUT="${OUTPUT:-context_payload.json}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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
    echo -e "${RED}✗${NC} $1" >&2
}

# Banner
echo "═══════════════════════════════════════════════════════"
echo "   AI Session Context Generator"
echo "   Token-Optimized Handoff System"
echo "═══════════════════════════════════════════════════════"
echo ""

# Validate compression level
case "$LEVEL" in
    minimal|standard|full)
        log_info "Compression level: $LEVEL"
        ;;
    *)
        log_error "Invalid compression level: $LEVEL"
        log_error "Valid levels: minimal, standard, full"
        exit 1
        ;;
esac

# Check if state file exists
if [[ ! -f "$STATE_FILE" ]]; then
    log_error "State file not found: $STATE_FILE"
    log_info "Please ensure the orchestrator state file exists"
    exit 1
fi

log_success "Found state file: $STATE_FILE"

# Check Python availability
if ! command -v "$PYTHON" &> /dev/null; then
    log_error "Python not found: $PYTHON"
    log_info "Please set PYTHON environment variable or install Python 3.7+"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$("$PYTHON" -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
log_info "Python version: $PYTHON_VERSION"

# Generate context using the Python CLI. Pass every caller-controlled value as
# an argument so paths cannot become Python source through shell interpolation.
log_info "Generating context payload..."

if "$PYTHON" "$SCRIPT_DIR/context_generator.py" \
    --state-file "$STATE_FILE" \
    --output "$OUTPUT" \
    --level "$LEVEL" \
    --show-tokens; then
    log_success "Context generation complete"
    log_info "Ready for AI session handoff"
    echo ""
    log_info "Next steps:"
    echo "  1. Review the generated context in: $OUTPUT"
    echo "  2. Use a handoff template from templates/ directory"
    echo "  3. Inject context into new AI session"
    echo ""
else
    log_error "Context generation failed"
    exit 1
fi
