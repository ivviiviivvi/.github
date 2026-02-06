# Repository Relocation Guide

This document tracks repositories that should be relocated to maintain proper
organizational structure.

## Pending Relocations

### metasystem-master

**Current Location:** `omni-dromenon-machina/metasystem-master` **Target
Location:** `{{ORG_NAME}}/metasystem-master`

**Reason for Relocation:** The `metasystem-master` repository is a development
orchestrator that manages multiple projects across the {{ORG_NAME}} ecosystem.
It does not belong in the `omni-dromenon-machina` organization, which is focused
on the artistic performance platform (Omni-Dromenon Engine).

**Contents:**

- Docker configurations for multi-project deployment
- Development orchestration scripts
- Project coordination documents
- CI/CD configuration
- Terraform infrastructure

**Dependencies:**

- Manages: `life-my--midst--in`, `gamified-coach-interface`,
  `trade-perpetual-future`
- Uses: `my--father-mother`, `mail_automation`, `mcp-servers`

### Transfer Instructions

#### Option 1: Repository Transfer (Recommended)

1. Go to: https://github.com/omni-dromenon-machina/metasystem-master/settings
1. Scroll to "Danger Zone"
1. Click "Transfer repository"
1. Enter `{{ORG_NAME}}` as the new owner
1. Confirm the transfer

**Note:** You must have owner/admin permissions on both organizations.

#### Option 2: Fork and Archive

If transfer is not possible:

1. Fork to {{ORG_NAME}}:

   ```bash
   gh repo fork omni-dromenon-machina/metasystem-master --org {{ORG_NAME}}
   ```

1. Update the fork to be independent:

   ```bash
   cd {{ORG_NAME}}/metasystem-master
   git remote remove upstream
   ```

1. Archive the original:

   ```bash
   gh repo edit omni-dromenon-machina/metasystem-master --archived
   ```

### Post-Relocation Tasks

After relocating:

- [ ] Update any CI/CD pipelines referencing the old location
- [ ] Update documentation in managed projects
- [ ] Add redirect notice to archived repository (if using Option 2)
- [ ] Update `4jp-metasystem.yaml` with new repository URLs
- [ ] Update `.github/docs/RELATED_REPOSITORIES.md`

______________________________________________________________________

## Completed Relocations

_No completed relocations yet._

______________________________________________________________________

## Organization Structure Reference

### {{ORG_NAME}} (Main Organization)

- `.github` - Organization configuration and automation
- Infrastructure and orchestration tools
- Development utilities
- Core platform projects

### omni-dromenon-machina (Artistic Platform)

- `.github` - Project-specific configuration
- `core-engine` - WebSocket performance server
- `performance-sdk` - React UI components
- Artist toolkits and examples

### 4444J99 (Personal Account)

- Personal forks and experiments
- Standalone projects
- Learning/tutorial repositories
