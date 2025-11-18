# Quick Start Guide

**Get started with Context Handoff System in 5 minutes**

---

## Installation

### Step 1: Copy Context Handoff to Your Project

```bash
# Option A: Clone the repository
git clone https://github.com/ivi374forivi/.github.git
cp -r .github/context-handoff /path/to/your/project/

# Option B: Download specific directory
# (If you only need the context-handoff system)
```

### Step 2: Verify Installation

```bash
cd /path/to/your/project/context-handoff
ls -la
```

You should see:
```
context_generator.py
generate_context.sh
templates/
examples/
tests/
docs/
README.md
```

---

## First Context Generation

### Step 3: Create Orchestrator State File

Create `.orchestrator_state.json` in your project root:

```json
{
  "metadata": {
    "project_name": "My Project",
    "version": "1.0.0"
  },
  "context": {
    "current_phase": "phase_01",
    "active_tasks": ["task_001"],
    "completed_tasks": [],
    "failed_tasks": []
  },
  "tasks": {
    "task_001": {
      "name": "My First Task",
      "status": "pending",
      "dependencies": [],
      "dependents": []
    }
  },
  "dag": {
    "phases": {
      "phase_01": {
        "name": "Phase 1",
        "tasks": ["task_001"]
      }
    }
  }
}
```

Or use the example:
```bash
cp context-handoff/examples/.orchestrator_state.json .
```

### Step 4: Generate Your First Context

```bash
cd context-handoff
./generate_context.sh standard
```

Output:
```
═══════════════════════════════════════════════════════
   AI Session Context Generator
   Token-Optimized Handoff System
═══════════════════════════════════════════════════════

ℹ Compression level: standard
✓ Found state file: .orchestrator_state.json
ℹ Python version: 3.10.0
ℹ Generating context payload...

───────────────────────────────────────────────────────
Context generated successfully
───────────────────────────────────────────────────────
Level:           standard
Output:          context_payload.json
Estimated tokens: 1187
───────────────────────────────────────────────────────

Token budget:    Good
✓ Context generation complete
```

### Step 5: Review Generated Context

```bash
# View the JSON payload
cat context_payload.json

# Or pretty-print it
python -m json.tool context_payload.json
```

---

## Using the Context

### Step 6: Create a Handoff Message

Use one of the templates:

```bash
# Copy template
cp templates/standard_handoff.md my_handoff.md

# Manually populate with values from context_payload.json
# Or write a script to automate this
```

### Step 7: Inject into AI Session

In your new AI session, paste the handoff message:

```markdown
# AI Session Handoff

**Handoff ID**: handoff_20250115_143000
**Project**: My Project

## Current State
- **Phase**: phase_01 (0% complete)
- **Progress**: 0% (0/1 tasks)
- **Active**: task_001
- **Failed**: None
- **Next**: task_001

## Validation Required
Before proceeding, confirm:
1. Current phase: phase_01
2. Current task: task_001
3. Any blocking errors? No

Reply "CONFIRMED" with brief summary.
```

---

## Testing

### Step 8: Run Tests

```bash
cd context-handoff/tests
./test_workflow.sh
```

This will:
1. Generate contexts at all compression levels
2. Validate each generated context
3. Display results

### Step 9: Validate Context

```bash
cd context-handoff/tests
python validate_context.py ../context_payload.json
```

Output:
```
============================================================
Context Validation Report
============================================================
File:        ../context_payload.json
Level:       standard
Token count: 1187 (target: ≤1200)
Status:      ✅ PASS

✓ All validations passed
✓ Token efficiency: 86.0% reduction from naive
============================================================
```

---

## Integration

### Step 10: Add to Your Orchestrator

```python
from context_generator import ContextPayloadGenerator, CompressionLevel

class MyOrchestrator:
    def __init__(self):
        self.context_gen = ContextPayloadGenerator('.orchestrator_state.json')

    def create_handoff(self):
        """Create handoff checkpoint"""
        context = self.context_gen.generate_context(CompressionLevel.STANDARD)
        self.context_gen.save_context('context_payload.json')
        print(f"✓ Handoff created ({self.context_gen.get_token_count(context)} tokens)")
```

---

## Next Steps

### Explore Compression Levels

Try different compression levels to find the right balance:

```bash
# Minimal (~500 tokens) - Quick handoffs
./generate_context.sh minimal

# Standard (~1200 tokens) - Recommended
./generate_context.sh standard

# Full (~2000 tokens) - Comprehensive
./generate_context.sh full
```

### Customize Templates

Edit templates to match your workflow:

```bash
cd templates
# Edit standard_handoff.md, add custom fields
```

### Automate Generation

Add to your workflow:

```python
# In your main loop
if token_count > 150000:
    orchestrator.create_handoff()
    print("Ready for session handoff!")
```

---

## Common Issues

### Issue: "State file not found"

**Solution**: Ensure `.orchestrator_state.json` exists in parent directory

```bash
pwd  # Check current directory
ls ../.orchestrator_state.json  # Verify state file exists
```

### Issue: "Token count too high"

**Solution**: Use lower compression level

```bash
./generate_context.sh minimal  # Instead of standard
```

### Issue: "Python not found"

**Solution**: Set PYTHON environment variable

```bash
export PYTHON=python3.10
./generate_context.sh standard
```

---

## Compression Level Comparison

| Level | Tokens | Use Case | Generation Time |
|-------|--------|----------|-----------------|
| **Minimal** | ~500 | Quick handoffs | <30 seconds |
| **Standard** | ~1200 | Regular sessions | <1 minute |
| **Full** | ~2000 | Multi-day breaks | <2 minutes |

---

## Example Workflow

### Daily Development

```bash
# Morning: Resume from previous day
cat yesterday_handoff.md  # Review context
python orchestrator.py resume

# During work: Monitor token usage
python orchestrator.py status

# Evening: Create handoff for tomorrow
cd context-handoff
./generate_context.sh standard
# Create handoff message for tomorrow
```

### Long-Running Projects

```bash
# Weekly: Full context snapshot
./generate_context.sh full

# Daily: Standard handoffs
./generate_context.sh standard

# Hourly: Quick checkpoints
./generate_context.sh minimal
```

---

## Resources

- **Full Documentation**: See [README.md](README.md)
- **Integration Guide**: See [docs/INTEGRATION.md](docs/INTEGRATION.md)
- **Schema Reference**: See [docs/SCHEMA.md](docs/SCHEMA.md)
- **Example State**: See [examples/.orchestrator_state.json](examples/.orchestrator_state.json)

---

## Getting Help

- Review examples in `examples/` directory
- Run test workflow: `tests/test_workflow.sh`
- Check validation: `tests/validate_context.py`
- Read detailed docs in `docs/` directory

---

**You're all set!** 🎉

Start generating context handoffs and enjoy seamless AI session coordination.

---

*Context Handoff System v1.0.0*
*Quick Start Guide*
