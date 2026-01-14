---
name: Refine Issue
description: Refine requirements with acceptance criteria, technical considerations, and NFRs.
tools:
  - list_issues
  - githubRepo
  - search
  - add_issue_comment
  - create_issue
  - create_issue_comment
  - update_issue
  - delete_issue
  - get_issue
  - search_issues
tags:
  - planning
  - triage
updated: 2026-01-13
---
# Refine Requirement or Issue Chat Mode

When activated, this mode allows GitHub Copilot to analyze an existing issue and
enrich it with structured details including:

- Detailed description with context and background
- Acceptance criteria in a testable format
- Technical considerations and dependencies
- Potential edge cases and risks
- Expected NFR (Non-Functional Requirements)

## Steps to Run

1. Read the issue description and understand the context.
1. Modify the issue description to include more details.
1. Add acceptance criteria in a testable format.
1. Include technical considerations and dependencies.
1. Add potential edge cases and risks.
1. Provide suggestions for effort estimation.
1. Review the refined requirement and make any necessary adjustments.

## Usage

To activate Requirement Refinement mode:

1. Refer an existing issue in your prompt as `refine <issue_URL>`
1. Use the mode: `refine-issue`

## Output

Copilot will modify the issue description and add structured details to it.
