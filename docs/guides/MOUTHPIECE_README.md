# 🎭 Mouthpiece Filter System

**Transform your poetry into prompts. Let your imperfections blossom.**

> _"Allow me to write and speak in my human imperfections, a filter turns my
> poetry into blossomed prompts for AI"_

## What is Mouthpiece?

The Mouthpiece Filter System is a comprehensive toolkit that lets you
communicate with AI in your natural, human voice. Write with imperfections, use
metaphors, express uncertainty—the filter transforms your authentic expression
into structured, AI-optimized prompts while preserving your humanity.

### The Problem

AI systems work best with clear, structured, precise prompts. Humans think and
communicate with metaphors, emotions, uncertainty, and imperfection. Most prompt
engineering advice asks humans to change how they think and write.

### Our Solution

**Don't change yourself. Change the interface.**

The Mouthpiece Filter bridges the gap:

- **You write** naturally, with all your human imperfections
- **The filter transforms** your writing into AI-optimized formats
- **Your voice is preserved** in the final output
- **AI understands** and acts on your intent

## Quick Start

### 1. Use the CLI Filter

```bash
# Transform natural writing into structured prompts
python scripts/mouthpiece_filter.py "your natural writing here"

# Example
python scripts/mouthpiece_filter.py "need something that watches our APIs and screams when they die, like a canary in a coal mine but for microservices"
```

### 2. Use the Chat Mode

In GitHub Copilot or Claude:

```
Load the mouthpiece.chatmode.md and chat naturally!
```

### 3. Use the Prompt Template

In Copilot Chat:

```
/mouthpiece-transform [your natural text]
```

## Components

| Component                                                              | Purpose                   | When to Use                              |
| ---------------------------------------------------------------------- | ------------------------- | ---------------------------------------- |
| **[Filter Script](../../src/automation/scripts/mouthpiece_filter.py)** | CLI transformation engine | Programmatic use, scripting, automation  |
| **[Chat Mode](../ai_framework/chatmodes/mouthpiece.chatmode.md)**      | Interactive AI persona    | Conversational transformation, iteration |
| **[Prompt Template](README.prompts.md)**                               | Quick transformation      | Fast, one-off transformations            |
| **[Documentation](MOUTHPIECE_SYSTEM.md)**                              | Complete guide            | Learning, reference, integration         |
| **[Examples](mouthpiece-examples.md)**                                 | Real transformations      | Inspiration, patterns, learning          |

## Features

### ✨ What It Does

- **Preserves Your Voice**: Keeps metaphors, emotion, and personal style
- **Extracts Intent**: Understands what you mean, not just what you say
- **Structures Information**: Organizes thoughts into clear formats
- **Optimizes for AI**: Creates effective prompts automatically
- **Multiple Formats**: GitHub issues, specs, docs, user stories, and more

### 🎯 Key Capabilities

1. **Intent Detection**: Automatically identifies creation, problem-solving,
   understanding, improvement, design, or analysis intents

1. **Concept Extraction**: Pulls out key concepts, requirements, and action
   items from natural text

1. **Metaphor Preservation**: Recognizes and preserves meaningful metaphorical
   language

1. **Multi-Format Output**: Generates structured prompts, markdown, or JSON

1. **Configuration**: Customizable to match your preferences and needs

## Examples

### Example 1: Stream of Consciousness → Structured Prompt

**Input:**

```
thinking we should maybe add tests? like unit tests for the api handlers,
integration tests for the full flows, maybe some e2e stuff with playwright?
```

**Output:**

```markdown
# Create: Comprehensive Testing Suite

## Objective

Implement comprehensive testing coverage including unit, integration, and
end-to-end tests for the application.

## Requirements

- Add unit tests for API handlers
- Implement integration tests for full workflows
- Create end-to-end tests using Playwright

## Key Concepts

- Unit testing
- Integration testing
- End-to-end testing
- API handlers
- Playwright
```

### Example 2: Poetic Vision → GitHub Issue

**Input:**

```
imagine if our data could flow like water, finding its way through the system,
pooling where it needs to rest, rushing where speed matters. visualize this.
```

**Output:**

```markdown
# Create: Data Flow Visualization System

## Objective

Build a visualization system that represents data flow through the system
using water-flow metaphors for intuitive understanding.

## Requirements

- Visualize data movement through system components
- Identify bottleneck locations (pooling points)
- Highlight high-throughput pathways (rushing areas)
- Real-time, dynamic updates

## Design Philosophy

> "like water, finding its way through the system"

The visualization should feel organic and natural, using water-flow metaphors
to make complex data flows immediately understandable.
```

See **[more examples](mouthpiece-examples.md)** for additional transformations.

## Usage

### CLI Script

```bash
# Basic usage
python scripts/mouthpiece_filter.py "your text here"

# From a file
python scripts/mouthpiece_filter.py --file thoughts.txt

# From stdin
echo "your text" | python scripts/mouthpiece_filter.py --stdin

# JSON output
python scripts/mouthpiece_filter.py "text" --format json

# Save to file
python scripts/mouthpiece_filter.py "text" --output result.md

# Custom config
python scripts/mouthpiece_filter.py "text" --config my-config.json

# Disable poetry preservation
python scripts/mouthpiece_filter.py "text" --no-poetry
```

### Configuration

Create a `mouthpiece-config.json`:

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

Options:

- **preserve_poetry**: Keep metaphors and poetic language (default: `true`)
- **extract_metaphors**: Identify metaphorical expressions (default: `true`)
- **maintain_voice**: Include original text (default: `true`)
- **output_format**: `structured`, `markdown`, or `json` (default: `structured`)
- **include_analysis**: Include analysis metadata (default: `true`)
- **style**: `conversational`, `technical`, or `hybrid` (default:
  `conversational`)

## Integration

### GitHub Actions

```yaml
name: Transform Issue
on:
  issues:
    types: [opened]

jobs:
  transform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Transform
        run: |
          python scripts/mouthpiece_filter.py "${{ github.event.issue.body }}"
```

### Pre-commit Hook

```bash
#!/bin/bash
MSG=$(cat $1)
TRANSFORMED=$(python .github/scripts/mouthpiece_filter.py "$MSG" --format prompt_only)
echo "$TRANSFORMED" > $1
```

### API (Python)

```python
from scripts.mouthpiece_filter import MouthpieceFilter

filter = MouthpieceFilter(config={"style": "technical"})
result = filter.transform("your natural text")
print(result["prompt"])
```

## Philosophy

### Core Beliefs

1. **Humans should stay human**

   - Preserve natural expression
   - Celebrate imperfection
   - Honor authentic voice

1. **AI should adapt to humans**

   - Not the other way around
   - Bridge the communication gap
   - Make technology accessible

1. **Poetry carries meaning**

   - Metaphors provide context
   - Emotion conveys priority
   - Imperfection shows authenticity

1. **Structure emerges from understanding**

   - Intent reveals requirements
   - Clarity comes from interpretation
   - Organization follows comprehension

### The Blossoming Metaphor

Your natural writing is like seeds and buds—raw, authentic, full of potential.
The Mouthpiece Filter doesn't replace your plants with plastic flowers. It helps
them blossom into their full form: structured, clear, ready to pollinate AI
systems with your ideas while staying rooted in your authentic expression.

## Documentation

- **[Complete Guide](MOUTHPIECE_SYSTEM.md)** - Full system documentation
- **[Examples](mouthpiece-examples.md)** - Real-world transformations
- **[Chat Mode](../ai_framework/chatmodes/mouthpiece.chatmode.md)** -
  Interactive persona
- **[Prompt Template](README.prompts.md)** - Quick reference

## Best Practices

### Do's ✅

- Write naturally and authentically
- Use metaphors if they help you express ideas
- Express uncertainty when you feel it
- Include emotional context
- Specify output format when needed

### Don'ts ❌

- Don't pre-optimize your writing
- Don't remove your personality
- Don't force formality
- Don't skip reviewing the output
- Don't over-rely without human judgment

## FAQ

**Q: Will this make my writing robotic?** A: No! It preserves your voice and
metaphors while adding structure.

**Q: Do I need to be technical?** A: Not at all. Write naturally. The filter
handles the translation.

**Q: What if my writing is unclear?** A: The filter interprets intent, but
always review the output for accuracy.

**Q: Can I customize the transformation?** A: Yes! Use configuration files or
CLI flags to control behavior.

**Q: Does it work offline?** A: Yes, the CLI filter is fully local and
offline-capable.

## Contributing

Want to improve Mouthpiece?

- Better metaphor detection
- Additional output formats
- Language support beyond English
- Integration examples
- Documentation improvements

See [CONTRIBUTING.md](../governance/CONTRIBUTING.md) for guidelines.

## Examples Gallery

### Simple Requests

```
"hey can you add a dark mode toggle?"
→ Structured feature implementation prompt
```

### Urgent Problems

```
"login's totally broken, users can't sign in!"
→ Critical bug fix prompt with investigation steps
```

### Poetic Visions

```
"imagine if code could tell stories about its evolution"
→ Feature design with preserved vision and technical specs
```

### Stream of Consciousness

```
"thinking maybe we need like a pipeline? data comes in, gets transformed,
goes to the database, gotta be fast though"
→ Technical architecture specification
```

See **[full examples](mouthpiece-examples.md)** for complete transformations.

## License

Part of the ivi374forivi organization `.github` repository. MIT License.

______________________________________________________________________

## Get Started Now

```bash
# Try it!
python scripts/mouthpiece_filter.py "your natural thoughts here"
```

**Write like a human. Let the filter handle the rest.**

**Your imperfections aren't bugs—they're features.** 🌸

______________________________________________________________________

<div align="center">

**[Documentation](MOUTHPIECE_SYSTEM.md)** •
**[Examples](mouthpiece-examples.md)** •
**[Chat Mode](../ai_framework/chatmodes/mouthpiece.chatmode.md)** •
**[Prompt](README.prompts.md)**

_Built with ❤️ for humans who want to stay human_

</div>
