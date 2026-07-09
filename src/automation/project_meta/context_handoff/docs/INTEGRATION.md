# Integration Guide

**Integrating Context Handoff System with Your Project**

______________________________________________________________________

## Overview

This guide covers integrating the Context Handoff System into various project
types and orchestration frameworks.

______________________________________________________________________

## Python Orchestrator Integration

### Basic Integration

Add context generation capability to your existing orchestrator:

````python
from pathlib import Path
from context_generator import ContextPayloadGenerator, CompressionLevel

class Orchestrator:
    def __init__(self, state_file=".orchestrator_state.json"):
        self.state_file = Path(state_file)
        self.context_gen = ContextPayloadGenerator(str(self.state_file))
        # ... existing initialization

    def checkpoint_for_handoff(self, level="standard"):
        """Create handoff checkpoint before token limit"""
        # Determine compression level
        level_enum = getattr(CompressionLevel, level.upper())

        # Generate context
        context = self.context_gen.generate_context(level_enum)

        # Save to file
        output_file = self.context_gen.save_context(
            "context_payload.json",
            level_enum
        )

        # Generate markdown report
        self._generate_handoff_report(context)

        # Display summary
        tokens = self.context_gen.get_token_count(context)
        print(f"\n{'='*60}")
        print("Handoff Checkpoint Created")
        print(f"{'='*60}")
        print(f"Level:       {level}")
        print(f"Tokens:      ~{tokens}")
        print(f"Output:      {output_file}")
        print(f"Report:      handoff_report.md")
        print(f"{'='*60}\n")

        return output_file

    def _generate_handoff_report(self, context):
        """Generate human-readable handoff report"""
        # Load template
        template_file = Path(__file__).parent / "templates" / "standard_handoff.md"

        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()

            # Populate template with context values
            report = self._populate_template(template, context)

            # Save report
            with open("handoff_report.md", 'w') as f:
                f.write(report)
        else:
            # Fallback: simple report
            self._generate_simple_report(context)

    def _populate_template(self, template, context):
        """Populate template with context values"""
        # Extract values from context
        replacements = {
            '{handoff_id}': context.get('handoff_id', 'N/A'),
            '{timestamp}': context.get('summary', {}).get('generated_at', 'N/A'),
            '{project_name}': context.get('summary', {}).get('project', 'N/A'),
            '{current_phase}': context.get('summary', {}).get('current_phase', 'N/A'),
            '{overall_progress}': context.get('summary', {}).get('progress', 'N/A'),
            '{tasks_complete}': str(context.get('summary', {}).get('tasks_complete', 0)),
            '{tasks_total}': str(context.get('summary', {}).get('tasks_total', 0)),
            # Add more replacements as needed
        }

        # Perform replacements
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, str(value))

        return template

    def _generate_simple_report(self, context):
        """Generate simple fallback report"""
        with open("handoff_report.md", 'w') as f:
            f.write("# Project Handoff Report\n\n")
            f.write(f"**Generated**: {context.get('summary', {}).get('generated_at')}\n\n")
            f.write(f"**Progress**: {context.get('summary', {}).get('progress')}\n\n")
            f.write("## Context\n\n")
            f.write("```json\n")
            import json
            f.write(json.dumps(context, indent=2))
            f.write("\n```\n")
````

### Automatic Checkpointing

Add automatic checkpoint creation based on token usage:

```python
class Orchestrator:
    def __init__(self):
        # ... existing code
        self.token_count = 0
        self.checkpoint_threshold = 150000  # 150k tokens

    def track_tokens(self, prompt_tokens, completion_tokens):
        """Track token usage and checkpoint if needed"""
        self.token_count += prompt_tokens + completion_tokens

        if self.token_count >= self.checkpoint_threshold:
            print(f"\n⚠️  Token limit approaching ({self.token_count} tokens)")
            print("Creating handoff checkpoint...")
            self.checkpoint_for_handoff("standard")
            print("✓ Ready for session handoff")
            return True

        return False

    def execute_task(self, task_id):
        """Execute task with token tracking"""
        # ... existing task execution

        # Track tokens (example - adapt to your LLM client)
        self.track_tokens(
            prompt_tokens=len(prompt) // 4,
            completion_tokens=len(response) // 4
        )
```

______________________________________________________________________

## CI/CD Integration

### GitHub Actions

Create workflow for automatic context generation:

```yaml
# .github/workflows/context-handoff.yml
name: Context Handoff Generation

on:
  workflow_dispatch:
    inputs:
      level:
        description: "Compression level"
        required: true
        default: "standard"
        type: choice
        options:
          - minimal
          - standard
          - full
  schedule:
    # Generate context every 4 hours during work days
    - cron: "0 9-17/4 * * 1-5"

jobs:
  generate-context:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Generate context
        run: |
          cd context-handoff
          ./generate_context.sh ${{ github.event.inputs.level || 'standard' }}

      - name: Validate context
        run: |
          cd context-handoff/tests
          python validate_context.py ../context_payload.json

      - name: Upload context artifact
        uses: actions/upload-artifact@v3
        with:
          name: context-payload-${{ github.run_number }}
          path: |
            context-handoff/context_payload.json
            context-handoff/handoff_report.md
          retention-days: 30

      - name: Create issue on failure
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Context generation failed',
              body: 'Automated context generation failed. Check workflow run.'
            })
```

### GitLab CI

```yaml
# .gitlab-ci.yml
generate_context:
  stage: build
  image: python:3.10
  script:
    - cd context-handoff
    - ./generate_context.sh standard
    - cd tests
    - python validate_context.py ../context_payload.json
  artifacts:
    paths:
      - context-handoff/context_payload.json
      - context-handoff/handoff_report.md
    expire_in: 30 days
  only:
    - schedules
    - web
```

______________________________________________________________________

## CLI Integration

### Add to Existing CLI

```python
# cli.py
import click
from context_generator import ContextPayloadGenerator, CompressionLevel

@click.group()
def cli():
    """Project CLI"""
    pass

@cli.command()
@click.option('--level', type=click.Choice(['minimal', 'standard', 'full']),
              default='standard', help='Compression level')
@click.option('--output', default='context_payload.json', help='Output file')
@click.option('--state-file', default='.orchestrator_state.json',
              help='Orchestrator state file')
def handoff(level, output, state_file):
    """Generate context handoff"""
    try:
        gen = ContextPayloadGenerator(state_file)
        level_enum = getattr(CompressionLevel, level.upper())

        output_path = gen.save_context(output, level_enum)
        context = gen.generate_context(level_enum)
        tokens = gen.get_token_count(context)

        click.echo(f"✓ Context generated: {output_path}")
        click.echo(f"  Level: {level}")
        click.echo(f"  Tokens: ~{tokens}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        return 1

if __name__ == '__main__':
    cli()
```

Usage:

```bash
python cli.py handoff --level standard
```

______________________________________________________________________

## Jupyter Notebook Integration

### Cell Magic for Context Generation

```python
# In your notebook
from IPython.core.magic import register_line_magic
from context_generator import ContextPayloadGenerator, CompressionLevel

@register_line_magic
def handoff(level):
    """Generate context handoff from notebook"""
    level = level or 'standard'
    gen = ContextPayloadGenerator('.orchestrator_state.json')
    level_enum = getattr(CompressionLevel, level.upper())

    gen.save_context('context_payload.json', level_enum)
    context = gen.generate_context(level_enum)
    tokens = gen.get_token_count(context)

    print(f"✓ Context generated ({tokens} tokens)")
    return context

# Usage in notebook:
# %handoff standard
```

______________________________________________________________________

## Docker Integration

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy context handoff system
COPY context-handoff/ /app/context-handoff/

# Copy your project files
COPY . /app/

# Set up environment
ENV PYTHONPATH=/app/context-handoff:$PYTHONPATH

# Generate context on container start
CMD ["bash", "-c", "cd /app/context-handoff && ./generate_context.sh standard"]
```

### Docker Compose

```yaml
version: "3.8"

services:
  orchestrator:
    build: .
    volumes:
      - ./.orchestrator_state.json:/app/.orchestrator_state.json:ro
      - ./context_payload.json:/app/context-handoff/context_payload.json
    environment:
      - PYTHON=python3
      - LEVEL=standard
```

______________________________________________________________________

## Web API Integration

### Flask Endpoint

```python
from flask import Flask, jsonify, request
from context_generator import ContextPayloadGenerator, CompressionLevel

app = Flask(__name__)

@app.route('/api/handoff', methods=['GET'])
def generate_handoff():
    """Generate context handoff via API"""
    level = request.args.get('level', 'standard')
    state_file = request.args.get('state_file', '.orchestrator_state.json')

    try:
        gen = ContextPayloadGenerator(state_file)
        level_enum = getattr(CompressionLevel, level.upper())

        context = gen.generate_context(level_enum)
        tokens = gen.get_token_count(context)

        return jsonify({
            'success': True,
            'context': context,
            'tokens': tokens,
            'level': level
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from context_generator import ContextPayloadGenerator, CompressionLevel

app = FastAPI()

class HandoffRequest(BaseModel):
    level: str = 'standard'
    state_file: str = '.orchestrator_state.json'

@app.post('/api/handoff')
async def generate_handoff(request: HandoffRequest):
    """Generate context handoff"""
    try:
        gen = ContextPayloadGenerator(request.state_file)
        level_enum = getattr(CompressionLevel, request.level.upper())

        context = gen.generate_context(level_enum)
        tokens = gen.get_token_count(context)

        return {
            'success': True,
            'context': context,
            'tokens': tokens,
            'level': request.level
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

______________________________________________________________________

## Monitoring Integration

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
handoff_generated = Counter('handoff_generated_total', 'Total handoffs generated', ['level'])
handoff_tokens = Histogram('handoff_tokens', 'Token count distribution', ['level'])
handoff_errors = Counter('handoff_errors_total', 'Total handoff errors')

class MonitoredOrchestrator:
    def checkpoint_for_handoff(self, level="standard"):
        """Create handoff with monitoring"""
        try:
            # Generate context
            gen = ContextPayloadGenerator('.orchestrator_state.json')
            level_enum = getattr(CompressionLevel, level.upper())
            context = gen.generate_context(level_enum)

            # Record metrics
            tokens = gen.get_token_count(context)
            handoff_generated.labels(level=level).inc()
            handoff_tokens.labels(level=level).observe(tokens)

            # Save context
            gen.save_context('context_payload.json', level_enum)

            return context

        except Exception as e:
            handoff_errors.inc()
            raise
```

______________________________________________________________________

## Testing Integration

### pytest Integration

```python
# test_context_handoff.py
import pytest
from context_generator import ContextPayloadGenerator, CompressionLevel

@pytest.fixture
def example_state(tmp_path):
    """Create example state file"""
    state_file = tmp_path / ".orchestrator_state.json"
    # ... create example state
    return str(state_file)

def test_minimal_context(example_state):
    """Test minimal context generation"""
    gen = ContextPayloadGenerator(example_state)
    context = gen.generate_context(CompressionLevel.MINIMAL)

    assert 'summary' in context
    assert 'active' in context
    assert 'failed' in context
    assert 'next' in context

    tokens = gen.get_token_count(context)
    assert tokens <= 500, f"Token count {tokens} exceeds minimal target"

def test_standard_context(example_state):
    """Test standard context generation"""
    gen = ContextPayloadGenerator(example_state)
    context = gen.generate_context(CompressionLevel.STANDARD)

    assert 'version' in context
    assert 'execution_state' in context
    assert 'critical_context' in context
    assert 'dag_snapshot' in context

    tokens = gen.get_token_count(context)
    assert tokens <= 1200, f"Token count {tokens} exceeds standard target"

def test_full_context(example_state):
    """Test full context generation"""
    gen = ContextPayloadGenerator(example_state)
    context = gen.generate_context(CompressionLevel.FULL)

    assert 'file_state' in context
    assert 'environment' in context

    tokens = gen.get_token_count(context)
    assert tokens <= 2000, f"Token count {tokens} exceeds full target"
```

______________________________________________________________________

## Best Practices

### When to Integrate

1. **Before deploying to production** - Test with your actual orchestrator state
1. **During initial development** - Set up early for consistent handoffs
1. **When scaling up** - Essential for projects with >50 tasks

### Integration Checklist

- [ ] Install context handoff system in project
- [ ] Adapt orchestrator to save state in required format
- [ ] Add checkpoint_for_handoff() method to orchestrator
- [ ] Configure automatic checkpointing (token limit or time-based)
- [ ] Set up CI/CD for periodic context generation
- [ ] Add monitoring/metrics for handoff quality
- [ ] Document handoff procedures for team
- [ ] Test with actual project state
- [ ] Validate token counts meet targets

### Common Pitfalls

1. **State file format mismatch** - Ensure your orchestrator saves complete
   state
1. **Missing fields** - Validate state file has all required fields
1. **Token count drift** - Monitor and adjust compression level as project grows
1. **Stale state** - Ensure state file is updated before generating context
1. **Template misalignment** - Keep templates in sync with schema changes

______________________________________________________________________

## Support

For integration assistance:

- Review examples in `examples/` directory
- Check test suite in `tests/` directory
- Consult schema documentation in `docs/SCHEMA.md`
- Open issues for integration questions

______________________________________________________________________

_Context Handoff System v1.0.0_
