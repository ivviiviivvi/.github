# Agent Development Guide

Use this guide when creating or updating agents in `ai_framework/agents/`.

## Authoring Checklist

- Add YAML frontmatter per `ai_framework/agents/SCHEMA.md`.
- Keep the description concise and user-facing.
- Prefer short, stable names that match the agent purpose.
- Include explicit tool usage guidance when tools are required.
- Avoid embedding credentials or secrets in agent definitions.

## File Naming

- Use kebab-case for filenames where possible.
- Keep names descriptive and consistent (e.g., `security-audit.agent.md`).

## Template

```markdown
---
name: {{Agent Name}}
description: {{One-sentence purpose}}
tools:
  - {{tool_1}}
tags:
  - {{tag_1}}
updated: {{YYYY-MM-DD}}
---

# {{Agent Name}}

{{Brief overview of responsibilities and usage.}}
```

## Inventory Updates

After changes, regenerate the inventory:

```bash
python automation/scripts/generate_agent_inventory.py
```
