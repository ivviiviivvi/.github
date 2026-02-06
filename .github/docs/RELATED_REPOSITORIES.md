# Related Repositories

This document catalogs repositories across the {{ORG_NAME}} ecosystem and their
relationships to this `.github` organization repository.

## Repository Categories

### Integrated into .github

These repositories have been consolidated into this `.github` repo:

| Repository                  | Source       | Status     | Notes                                    |
| --------------------------- | ------------ | ---------- | ---------------------------------------- |
| ospo-reusable-workflows     | 4444J99      | Integrated | Reusable workflow patterns extracted     |
| system-governance-framework | {{ORG_NAME}} | Integrated | Governance templates and AI handoff docs |
| log-commit-preserve         | {{ORG_NAME}} | Integrated | Commitizen configuration and workflows   |

### Active Dependencies

These are used as GitHub Actions or dependencies:

| Repository             | Source                                | Usage                    |
| ---------------------- | ------------------------------------- | ------------------------ |
| issue-parser           | 4444J99 (fork of github/issue-parser) | `project-automation.yml` |
| git-auto-commit-action | 4444J99 (fork of stefanzweifel/)      | 5 workflows              |
| combine-prs            | 4444J99 (fork of github/combine-prs)  | `combine-prs.yml`        |

### Specialized Tools (Keep Separate)

These serve distinct purposes and should remain independent:

#### auto-revision-epistemic-engine

- **URL:** https://github.com/{{ORG_NAME}}/auto-revision-epistemic-engine
- **Purpose:** Self-governing orchestration framework with 8 phases
- **Features:** Human Review Gates (HRGs), RBAC, SLA enforcement, ethical audits
- **Use Case:** Advanced scenarios requiring governance-first orchestration

#### theoretical-specifications-first

- **URL:** https://github.com/{{ORG_NAME}}/theoretical-specifications-first
- **Purpose:** Spec-Driven Development (SDD) toolkit
- **Features:** `specify` CLI, template generation, AI agent integration
- **Use Case:** Development methodology for spec-first approaches

#### cognitive-archaelogy-tribunal

- **URL:** https://github.com/{{ORG_NAME}}/cognitive-archaelogy-tribunal
- **Purpose:** Ecosystem archaeology and audit tool
- **Features:** Archive scanning, AI context aggregation, knowledge graphs
- **Use Case:** Organizational discovery and knowledge management

### Pending Relocation

| Repository        | Current Location      | Target       | Reason                                     |
| ----------------- | --------------------- | ------------ | ------------------------------------------ |
| metasystem-master | omni-dromenon-machina | {{ORG_NAME}} | Development orchestrator, not art platform |

See [REPOSITORY_RELOCATION.md](./REPOSITORY_RELOCATION.md) for transfer
instructions.

### External Organizations

#### omni-dromenon-machina

Artistic performance platform organization. Keeps separate governance.

| Repository                   | Purpose                                |
| ---------------------------- | -------------------------------------- |
| .github                      | Project-specific community health      |
| core-engine                  | Real-time WebSocket performance server |
| performance-sdk              | React UI component library             |
| artist-toolkit-and-templates | Artist resources                       |

______________________________________________________________________

## Usage Patterns

### Using Reusable Workflows

```yaml
jobs:
  label:
    uses: {{ORG_NAME}}/.github/.github/workflows/reusable-labeler.yml@main
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Referencing Governance Tools

For advanced governance needs:

```bash
# Clone the epistemic engine for local use
gh repo clone {{ORG_NAME}}/auto-revision-epistemic-engine

# Use SDD toolkit
gh repo clone {{ORG_NAME}}/theoretical-specifications-first
```

### Running Ecosystem Analysis

```bash
# Audit your organizational history
gh repo clone {{ORG_NAME}}/cognitive-archaelogy-tribunal
cd cognitive-archaelogy-tribunal
python -m tribunal.scan --sources all
```

______________________________________________________________________

## Decision Matrix

When to use each resource:

| Need                               | Use                              |
| ---------------------------------- | -------------------------------- |
| Standard CI/CD, labeling, releases | `.github` reusable workflows     |
| PR title validation                | `reusable-pr-title.yml`          |
| Version management                 | Commitizen workflows             |
| Complex governance with oversight  | auto-revision-epistemic-engine   |
| Spec-first development             | theoretical-specifications-first |
| Organizational archaeology         | cognitive-archaelogy-tribunal    |
| Artistic performance systems       | omni-dromenon-machina repos      |

______________________________________________________________________

## Maintenance

This document should be updated when:

- New repositories are integrated or created
- Repository relationships change
- External dependencies are updated
- Relocation tasks are completed

Last Updated: 2026-01-23
