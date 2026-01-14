# Agent Lifecycle and Orchestration

## Lifecycle Stages

1. **Intent capture**: clarify the request, goals, and constraints.
2. **Scope definition**: identify affected files, tools, and required outputs.
3. **Planning**: outline steps, dependencies, and success criteria.
4. **Execution**: perform tool-driven work with minimal, reversible changes.
5. **Validation**: run checks or inspections relevant to the task.
6. **Review**: summarize outcomes, risks, and next actions.
7. **Handoff**: provide artifacts and leave a clear trail for follow-up.

## Orchestration Guidance

- Prefer a single primary agent; delegate only when specialized expertise is required.
- Keep tool usage minimal and traceable.
- Use inventories and schemas to keep assets consistent across teams.
- If an agent requires MCP servers, validate connectivity before actions.

## Audit Trail

- Record command outputs that inform decisions.
- Note any skipped steps and why.
- Ensure any generated files are linked in summaries.
