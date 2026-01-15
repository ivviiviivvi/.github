# AI Framework

This directory holds reusable AI agent assets used across the organization.

## Structure

- `ai_framework/agents/` agent definitions (`*.agent.md`)
- `ai_framework/chatmodes/` chat mode definitions (`*.chatmode.md`)
- `ai_framework/collections/` curated bundles (`*.collection.yml`, `*.md`)
- `ai_framework/prompts/` prompt templates (`*.md`)

## Authoring Conventions

- Use valid YAML frontmatter delimited by `---` at the top of chatmodes/agents.
- Keep frontmatter keys lowercase and consistent across files.
- Prefer list values for fields like `tools` and `tags`.
- Keep descriptions short and user-facing.

## Related Docs

- `docs/README.chatmodes.md`
- `docs/README.agents.md`
- `docs/README.collections.md`
- `ai_framework/agents/DEVELOPMENT_GUIDE.md`
- `ai_framework/agents/SCHEMA.md`
- `ai_framework/prompts/SCHEMA.md`

## Phase 6 Status

Phase 6 is complete with normalized chatmodes, validation tooling, inventories,
and agent documentation updates.
