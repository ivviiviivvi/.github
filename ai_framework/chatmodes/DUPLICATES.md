# Chatmode Duplicate Audit

This audit flags potential overlaps for consolidation. It is a starting point,
not a removal list.

## Planning cluster (general)

Candidates:

- `ai_framework/chatmodes/plan.chatmode.md`
- `ai_framework/chatmodes/planner.chatmode.md`
- `ai_framework/chatmodes/task-planner.chatmode.md`
- `ai_framework/chatmodes/implementation-plan.chatmode.md`

Rationale:

All four describe "planning" or "implementation plan" behavior. The difference
is mostly tone and tooling requirements. Recommend choosing one canonical
general planner and re-scoping the others (or merging content) to avoid overlap.

## Planning cluster (IaC specific)

Related but specialized:

- `ai_framework/chatmodes/bicep-plan.chatmode.md`
- `ai_framework/chatmodes/terraform-azure-planning.chatmode.md`

Rationale:

Both are infrastructure planning modes with explicit file output paths. Keep
them separate but align on the shared planning schema and frontmatter.

## Planning cluster (tech debt)

Related but specialized:

- `ai_framework/chatmodes/tech-debt-remediation-plan.chatmode.md`

Rationale:

This is a planning variant for debt remediation. Keep separate but align with
the canonical planning structure (overview, steps, testing) if feasible.
