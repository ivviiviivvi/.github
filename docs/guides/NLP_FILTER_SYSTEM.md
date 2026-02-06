# Mouthpiece Filter System

**Transform natural human expression into AI-optimized prompts while preserving
your unique voice.**

> _"Write like a human. Let the filter handle the rest."_

## Table of Contents

- [Overview](#overview)
- [Philosophy](#philosophy)
- [Components](#components)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Integration](#integration)
- [Best Practices](#best-practices)
- [FAQ](#faq)

## Overview

The Mouthpiece Filter System is a comprehensive toolkit that bridges the gap
between natural human expression and AI-optimized communication. It allows you
to write and speak in your authentic voice—with all its imperfections,
metaphors, and humanity—while automatically transforming that input into
structured, clear prompts that AI systems can understand and act upon.

### What It Does

- **Preserves Your Voice**: Keeps your unique style, metaphors, and emotional
  context
- **Extracts Intent**: Understands what you mean, not just what you say
- **Structures Information**: Organizes thoughts into clear, actionable formats
- **Optimizes for AI**: Creates prompts that AI systems can process effectively
- **Offers Flexibility**: Outputs in various formats (GitHub issues, specs,
  docs, etc.)

### What It Doesn't Do

- **Change Your Meaning**: Never alters your core intent
- **Force Formality**: Doesn't make everything corporate or sterile
- **Judge Expression**: Celebrates natural language, doesn't criticize it
- **Replace Thinking**: Enhances communication, doesn't replace human thought

## Philosophy

### Core Principles

1. **Human First, AI Second**

   - Humans should communicate naturally
   - AI should adapt to humans, not vice versa
   - Preserve humanity in every transformation

1. **Poetry to Precision**

   - Metaphors carry meaning
   - Emotions provide context
   - Imperfection is authentic
   - Clarity emerges from understanding

1. **Bridge, Don't Replace**

   - Enhance human expression
   - Maintain the original voice
   - Add structure without removing soul
   - Make AI understand humanity

### The "Blossoming" Metaphor

Think of your natural writing as seeds and buds—raw, authentic, full of
potential. The Mouthpiece Filter doesn't replace your plants with plastic
flowers. Instead, it helps them blossom into their full form: structured, clear,
ready to pollinate AI systems with your ideas.

## Components

The Mouthpiece System consists of four main components:

### 1. Core Filter Script (`scripts/natural_language_prompt_filter.py`)

A Python-based transformation engine that:

- Analyzes natural text for intent, concepts, and structure
- Extracts key requirements and objectives
- Preserves metaphors and emotional context
- Generates optimized prompts in multiple formats

**Use when**: You want programmatic transformation via CLI or scripts

### 2. Mouthpiece Chat Mode (`chatmodes/natural-language-prompt-translator.chatmode.md`)

An interactive AI persona specialized in natural language transformation:

- Conversational interface
- Real-time interpretation and transformation
- Iterative refinement
- Format flexibility

**Use when**: You want interactive, conversational transformation

### 3. Transform Prompt (`prompts/mouthpiece-transform.prompt.md`)

A quick-use prompt template for GitHub Copilot:

- Fast transformations
- Structured output
- Example-driven
- Copy-paste ready

**Use when**: You need quick transformations in Copilot Chat

### 4. Configuration System

Customizable settings to control:

- Poetry preservation level
- Voice maintenance
- Output format
- Analysis depth
- Style preferences

**Use when**: You have specific transformation preferences

## Getting Started

### Quick Start (5 minutes)

1. **Choose Your Interface**

   - CLI: Use the filter script directly
   - Copilot: Use the chat mode or prompt
   - Integration: Build into your workflow

1. **Try a Simple Transformation**

   ```bash
   # Using the CLI
   python scripts/natural_language_prompt_filter.py "need to build something that tracks user sessions and figures out what they're trying to do"
   ```

1. **Review the Output**

   - See your original text preserved
   - Check the optimized prompt
   - Notice preserved metaphors
   - Use the ready-to-go format

### Installation

The Mouthpiece System is part of your `.github` organization repository. No
installation needed!

**To use the Python script:**

```bash
# Make it executable
chmod +x scripts/natural_language_prompt_filter.py

# Run it
python scripts/natural_language_prompt_filter.py "your text here"
```

**To use in GitHub Copilot:**

```
# In Copilot Chat, reference the chatmode or prompt
@workspace /mouthpiece-transform [your natural text]
```

## Usage Examples

### Example 1: Vague Idea → GitHub Issue

**Input (natural):**

```
so i've been thinking about how our error messages kinda suck? like, when
something breaks, users just see "error 500" and they're like... what? maybe
we could make them more human? tell people what actually went wrong and what
they can do about it?
```

**Output (optimized):**

```markdown
# Improve: User-Friendly Error Messages

## Objective

Replace generic error codes with human-readable error messages that explain
what went wrong and provide actionable next steps for users.

## Requirements

- Replace generic error codes (e.g., "Error 500")
- Explain errors in plain, user-friendly language
- Provide actionable guidance for users
- Maintain technical accuracy while improving clarity

## Key Concepts

- Error messaging
- User experience
- Error handling
- User guidance

## Current Problem

Users currently see technical error codes without explanation, leading to
confusion and frustration.

## Success Criteria

- [ ] Error messages explain what happened in plain language
- [ ] Users receive actionable next steps
- [ ] Technical accuracy maintained
- [ ] User satisfaction with error handling improves

## Original Expression

> "maybe we could make them more human? tell people what actually went wrong
> and what they can do about it?"
```

### Example 2: Stream of Consciousness → Technical Spec

**Input (natural):**

```
thinking we need like a pipeline or something? data comes in from different
sources - APIs, webhooks, file uploads, whatever - and we need to normalize it,
validate it, transform it into our schema, then push it to the database. gotta
be fast tho, like real-time fast. and if something fails we can't lose data,
need to retry or queue it or something
```

**Output (optimized):**

```markdown
# Design: Real-Time Data Ingestion Pipeline

## Objective

Create a high-performance data ingestion pipeline that accepts data from
multiple sources, normalizes and validates it, transforms it to our schema,
and persists it to the database with fault tolerance.

## Requirements

### Input Sources

- REST APIs
- Webhooks
- File uploads
- Other configurable sources

### Processing Pipeline

- Data normalization across sources
- Schema validation
- Transformation to unified schema
- Database persistence

### Performance & Reliability

- Real-time processing capabilities
- Fault-tolerant with retry logic
- Message queuing for failed operations
- Zero data loss guarantee

## Technical Considerations

- High throughput requirements
- Multiple data source formats
- Schema transformation rules
- Error handling and retry strategies
- Queue management for failures

## Architecture Components

1. Input adapters (API, webhook, file handlers)
2. Normalization layer
3. Validation engine
4. Schema transformation service
5. Database writer
6. Retry queue system

## Success Criteria

- [ ] Supports all required input sources
- [ ] Real-time processing performance
- [ ] Schema validation and transformation working
- [ ] Fault tolerance with retry mechanism
- [ ] Zero data loss under normal failure scenarios
- [ ] Monitoring and alerting in place

## Original Vision

> "data comes in from different sources... gotta be fast tho, like real-time
> fast. and if something fails we can't lose data"
```

### Example 3: Poetic Description → User Story

**Input (natural):**

```
imagine: you're a gardener tending to your digital garden. you plant seeds
(projects), watch them grow, prune what's not working, harvest what blooms.
right now our users have no garden, just a chaotic wilderness. give them tools
to cultivate their project ecosystem.
```

**Output (optimized):**

```markdown
# User Story: Project Lifecycle Management Dashboard

## Story

**As a** user managing multiple projects
**I want** intuitive tools to manage my project lifecycle
**So that** I can easily create, nurture, and maintain my projects

## Background

Users currently lack a unified view and management interface for their
projects, leading to disorganization and difficulty maintaining project health.

## Acceptance Criteria

### Project Creation ("Planting Seeds")

- [ ] Simple project initialization workflow
- [ ] Template options for different project types
- [ ] Clear project setup guidance

### Project Monitoring ("Watching Growth")

- [ ] Dashboard showing all projects and their status
- [ ] Health indicators for each project
- [ ] Activity timeline and progress tracking

### Project Maintenance ("Pruning")

- [ ] Easy identification of stale or problematic areas
- [ ] Tools to archive or clean up unused projects
- [ ] Maintenance recommendations

### Success Metrics ("Harvesting")

- [ ] Completion tracking and milestones
- [ ] Success metrics visualization
- [ ] Project outcome analysis

## Design Philosophy

> "imagine: you're a gardener tending to your digital garden"

The interface should feel like tending a garden—intuitive, visual, rewarding.
Users should see their projects as living things that need care and attention,
not just database entries.

## Visual Concepts

- Use growth metaphors in UI
- Green/healthy vs. yellow/needs-attention indicators
- Timeline as growth progression
- Archiving as "composting" for future use

## Technical Notes

- Dashboard view with project cards
- Status visualization (healthy, needs attention, stale)
- Quick actions for common maintenance tasks
- Project health scoring algorithm
```

### Example 4: CLI Script Usage

```bash
# Basic transformation
python scripts/natural_language_prompt_filter.py "build me a thing that sends emails when stuff happens"

# From a file
python scripts/natural_language_prompt_filter.py --file my_thoughts.txt

# From stdin
echo "help me understand async/await" | python scripts/natural_language_prompt_filter.py --stdin

# JSON output
python scripts/natural_language_prompt_filter.py "create a user dashboard" --format json

# Just the prompt (no metadata)
python scripts/natural_language_prompt_filter.py "optimize our search" --format prompt_only

# Save to file
python scripts/natural_language_prompt_filter.py "add dark mode" --output task.md

# Custom configuration
python scripts/natural_language_prompt_filter.py "text here" --config my_config.json

# Disable poetry preservation
python scripts/natural_language_prompt_filter.py "text here" --no-poetry
```

## Configuration

### Default Configuration

```json
{
  "preserve_poetry": true,
  "extract_metaphors": true,
  "maintain_voice": true,
  "output_format": "structured",
  "include_analysis": true,
  "style": "conversational"
}
```

### Configuration Options

| Option              | Type    | Default            | Description                                     |
| ------------------- | ------- | ------------------ | ----------------------------------------------- |
| `preserve_poetry`   | boolean | `true`             | Keep metaphors and poetic language              |
| `extract_metaphors` | boolean | `true`             | Identify and preserve metaphorical expressions  |
| `maintain_voice`    | boolean | `true`             | Include original text to preserve voice         |
| `output_format`     | string  | `"structured"`     | Output format: `structured`, `markdown`, `json` |
| `include_analysis`  | boolean | `true`             | Include analysis metadata in output             |
| `style`             | string  | `"conversational"` | Style: `conversational`, `technical`, `hybrid`  |

### Custom Configuration File

Create a JSON file with your preferences:

```json
{
  "preserve_poetry": true,
  "extract_metaphors": false,
  "maintain_voice": true,
  "output_format": "markdown",
  "include_analysis": false,
  "style": "technical"
}
```

Use it:

```bash
python scripts/natural_language_prompt_filter.py "your text" --config my_config.json
```

## Integration

### GitHub Actions Workflow

Create a workflow that transforms issue descriptions automatically:

```yaml
name: Mouthpiece Transform

on:
  issues:
    types: [opened]

jobs:
  transform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Transform Issue Description
        run: |
          python scripts/natural_language_prompt_filter.py "${{ github.event.issue.body }}" \
            --format markdown \
            --output transformed.md

      - name: Comment with Transformation
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const transformed = fs.readFileSync('transformed.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Mouthpiece Transformation\n\n${transformed}`
            });
```

### Pre-commit Hook

Transform commit messages before committing:

```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg

COMMIT_MSG_FILE=$1

# Read the commit message
MSG=$(cat $COMMIT_MSG_FILE)

# Transform it
TRANSFORMED=$(python .github/scripts/natural_language_prompt_filter.py "$MSG" --format prompt_only --no-poetry)

# Write back
echo "$TRANSFORMED" > $COMMIT_MSG_FILE
```

### VS Code Integration

Create a task in `.vscode/tasks.json`:

```json
{
  "label": "Mouthpiece Transform",
  "type": "shell",
  "command": "python",
  "args": [
    "${workspaceFolder}/.github/scripts/natural_language_prompt_filter.py",
    "${selectedText}",
    "--format",
    "prompt_only"
  ],
  "presentation": {
    "reveal": "always",
    "panel": "new"
  }
}
```

## Best Practices

### Do's ✅

1. **Write Naturally**

   - Use your normal voice
   - Include metaphors if they help
   - Don't self-censor or over-polish

1. **Provide Context**

   - Mention what you're trying to achieve
   - Include relevant background
   - Express uncertainties

1. **Iterate**

   - Use the output as a starting point
   - Refine and adjust as needed
   - Combine with human review

1. **Preserve Humanity**

   - Keep meaningful metaphors
   - Maintain emotional context
   - Let your personality show

1. **Specify Format When Needed**

   - Mention "as GitHub issue" if needed
   - Specify "technical spec" for formal docs
   - Request "user story" for product work

### Don'ts ❌

1. **Don't Pre-optimize**

   - Don't write "for the AI"
   - Don't remove personality
   - Don't force formality

1. **Don't Lose Meaning**

   - Review transformations
   - Ensure intent is preserved
   - Adjust if meaning shifts

1. **Don't Skip Human Judgment**

   - AI assists, humans decide
   - Review before using
   - Add context the AI missed

1. **Don't Over-rely**

   - Use for appropriate tasks
   - Some things need direct communication
   - Know when to skip the filter

## FAQ

### Q: Will this make my writing sound robotic?

**A:** No! The opposite. The Mouthpiece Filter preserves your natural voice and
metaphors. It adds structure, not sterility.

### Q: What if I write something completely unclear?

**A:** The filter does its best to interpret intent, but it's not magic. If your
input is too vague, the output will ask clarifying questions or note
uncertainties.

### Q: Can I use this for code comments?

**A:** Yes! Transform verbal explanations into well-structured docstrings and
comments.

### Q: Does it work with other languages?

**A:** The current version is optimized for English, but the principles work
across languages. Contributions for multilingual support welcome!

### Q: How do I know if the transformation is accurate?

**A:** Always review the output. The system preserves your original text so you
can compare. Think of it as a draft, not a final product.

### Q: What if I want more technical output?

**A:** Use `--style technical` in the CLI or specify "make it technical" when
using the chat mode.

### Q: Can I contribute improvements?

**A:** Absolutely! This is open source. Contributions for better metaphor
detection, intent analysis, and output formats are welcome.

### Q: What data does it collect?

**A:** None. It's a local transformation tool. Nothing leaves your machine
unless you explicitly push it somewhere.

## Advanced Usage

### Chaining Transformations

```bash
# Natural → Structured → GitHub Issue Template
python scripts/natural_language_prompt_filter.py "$(cat idea.txt)" \
  --format markdown \
  --output temp.md

# Use the output in another process
gh issue create --title "New Feature" --body-file temp.md
```

### Batch Processing

```bash
# Transform all idea files
for file in ideas/*.txt; do
  python scripts/natural_language_prompt_filter.py \
    --file "$file" \
    --output "transformed/$(basename $file)"
done
```

### API Mode (Future Feature)

```python
from natural_language_prompt_filter import MouthpieceFilter

filter = MouthpieceFilter(config={"style": "technical"})
result = filter.transform("build a search feature")

print(result["prompt"])
print(result["metadata"])
```

## Contributing

Want to improve the Mouthpiece System?

- **Better metaphor detection**: Add patterns and indicators
- **Language support**: Expand beyond English
- **Output formats**: Add new format options
- **Integration examples**: Share your workflows
- **Documentation**: Improve guides and examples

See [CONTRIBUTING.md](../governance/CONTRIBUTING.md) for details.

## License

Part of the ivi374forivi organization `.github` repository. MIT License.

______________________________________________________________________

**Remember: Write like a human. The filter handles the rest. Let your
imperfections blossom into structured prompts.** 🌸
