#!/usr/bin/env bash
# test_workflow.sh - Test the complete context handoff workflow
#
# This script demonstrates the full workflow:
# 1. Generate context from example state
# 2. Validate the generated context
# 3. Display results

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "════════════════════════════════════════════════════════"
echo "   Context Handoff System - Workflow Test"
echo "════════════════════════════════════════════════════════"
echo ""

# Test all three compression levels
for LEVEL in minimal standard full; do
    echo -e "${BLUE}Testing $LEVEL compression level...${NC}"
    echo ""

    # Copy example state to test directory
    cp "$PROJECT_DIR/examples/.orchestrator_state.json" "$PROJECT_DIR/tests/.orchestrator_state.json"

    # Change to test directory
    cd "$PROJECT_DIR/tests"

    # Generate context
    OUTPUT="context_${LEVEL}.json"
    PYTHON="${PYTHON:-python3}"

    $PYTHON - <<EOF
import sys
sys.path.insert(0, '$PROJECT_DIR')

from context_generator import ContextPayloadGenerator, CompressionLevel

level_map = {
    'minimal': CompressionLevel.MINIMAL,
    'standard': CompressionLevel.STANDARD,
    'full': CompressionLevel.FULL
}

gen = ContextPayloadGenerator('.orchestrator_state.json')
gen.save_context('$OUTPUT', level_map['$LEVEL'])
context = gen.generate_context(level_map['$LEVEL'])
tokens = gen.get_token_count(context)

print(f"✓ Generated {tokens} tokens")
EOF

    echo ""

    # Validate context
    echo -e "${BLUE}Validating generated context...${NC}"
    python validate_context.py "$OUTPUT"

    echo ""
    echo "----------------------------------------"
    echo ""
done

# Cleanup
rm -f .orchestrator_state.json

echo -e "${GREEN}✓ All tests completed successfully${NC}"
echo ""
echo "Generated files:"
ls -lh context_*.json

echo ""
echo "Next steps:"
echo "  1. Review generated contexts: context_minimal.json, context_standard.json, context_full.json"
echo "  2. Compare token counts across compression levels"
echo "  3. Integrate into your orchestrator"
