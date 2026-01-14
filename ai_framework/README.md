# AI Framework

This directory holds reusable AI agent assets used across the organization.

## Structure

- `ai_framework/agents/` agent definitions (`*.agent.md`)
- `ai_framework/chatmodes/` chat mode definitions (`*.chatmode.md`)
- `ai_framework/collections/` curated bundles (`*.collection.yml`, `*.md`)

## Authoring Conventions

- Use valid YAML frontmatter delimited by `---` at the top of chatmodes/agents.
- Keep frontmatter keys lowercase and consistent across files.
- Prefer list values for fields like `tools` and `tags`.
- Keep descriptions short and user-facing.

## Related Docs

- `docs/README.chatmodes.md`
- `docs/README.agents.md`
- `docs/README.collections.md`

## Phase 6 Next Steps

- Audit chatmodes for duplicates and consolidate where appropriate.
- Normalize frontmatter to a single schema and validate.
- Add per-folder indexes if listings grow.
