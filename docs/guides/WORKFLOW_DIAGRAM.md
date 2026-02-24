# Workflow Architecture Diagram

## Complete Pipeline Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEVELOPER PUSHES CODE TO MAIN                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌────────────────┐ ┌────────────┐ ┌─────────────────┐
│   PHASE 1      │ │  PHASE 2   │ │    PHASE 3      │
│  Walkthrough   │ │ AgentSphere│ │ Live Deployment │
│  Generation    │ │  + Pages   │ │   Strategies    │
│   (Existing)   │ │            │ │                 │
└───────┬────────┘ └─────┬──────┘ └────────┬────────┘
        │                │                  │
        │                │                  │
        ▼                ▼                  ▼
┌────────────────────────────────────────────────────┐
│              PARALLEL EXECUTION                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1️⃣  agentsphere-deployment.yml                    │
│     ├─ Detect app type                            │
│     ├─ Create .agentsphere.yml                    │
│     ├─ Register with AgentSphere API              │
│     ├─ Add badge to README                        │
│     └─ Create PR with demo link                   │
│                                                     │
│  2️⃣  deploy-to-pages-live.yml                     │
│     ├─ Detect deployment strategy                 │
│     ├─ Strategy A: Pages Direct                   │
│     │   └─ Build → Deploy to Pages                │
│     ├─ Strategy B: Docker                         │
│     │   └─ Trigger docker-build-push              │
│     ├─ Strategy C: Codespaces                     │
│     │   └─ Create devcontainer config             │
│     └─ Strategy D: None (CLI/Library)             │
│                                                     │
│  3️⃣  docker-build-push.yml (if Dockerfile)        │
│     ├─ Build Docker image                         │
│     ├─ Push to GitHub Container Registry          │
│     ├─ Generate run instructions                  │
│     └─ Update deployment metadata                 │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│           SCHEDULED / TRIGGERED UPDATES             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  4️⃣  generate-pages-index.yml (every 6 hours)     │
│     ├─ Query GitHub API for all repos             │
│     ├─ Collect walkthrough metadata               │
│     ├─ Generate walkthroughs.yml                  │
│     ├─ Create/update index pages                  │
│     └─ Auto-commit changes                        │
│                                                     │
│  5️⃣  build-pages-site.yml (after walkthrough)     │
│     ├─ Aggregate all metadata                     │
│     ├─ Build Jekyll static site                   │
│     ├─ Generate video gallery                     │
│     └─ Deploy to GitHub Pages                     │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  FINAL OUTPUTS                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🎬 Video Tutorial        ✅ Generated              │
│  🚀 AgentSphere Demo      ✅ Badge in README        │
│  🌐 GitHub Pages Gallery  ✅ Live at *.github.io    │
│  📱 Live App Demo         ✅ Strategy-dependent     │
│  🔍 Searchable Index      ✅ Auto-updated           │
│  📚 Documentation         ✅ Comprehensive          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Data Flow

```
Repository Files
    ↓
┌─────────────────┐
│ Detection Logic │ → App Type (React, Flask, etc.)
│ in Workflows    │ → Deployment Strategy (A/B/C/D)
│                 │ → Port Configuration
└────────┬────────┘
         ↓
┌─────────────────┐
│ Configuration   │ → .agentsphere.yml
│ Generation      │ → app-deployment-config.yml
│                 │ → devcontainer.json
└────────┬────────┘
         ↓
┌─────────────────┐
│ Deployment      │ → GitHub Pages (Strategy A)
│ Execution       │ → Docker Image (Strategy B)
│                 │ → Codespaces (Strategy C)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Metadata        │ → walkthroughs.yml
│ Collection      │ → app-deployments.yml
│                 │ → Gallery Index
└────────┬────────┘
         ↓
┌─────────────────┐
│ Jekyll Build    │ → Static HTML/CSS/JS
│ & Deploy        │ → Live Gallery Site
└────────┬────────┘
         ↓
    User Access
    (Browser)
```

## File Dependencies

```
_config.yml
    ↓
docs/_layouts/default.html
    ↓
docs/_includes/walkthrough_gallery.html
    ├─ docs/_data/walkthroughs.yml
    └─ docs/_data/app-deployments.yml

docs/_layouts/app-demo.html
    ↓
docs/_includes/live-app-embed.html
```

## Workflow Triggers

| Workflow                   | Event                     | Frequency               |
| -------------------------- | ------------------------- | ----------------------- |
| agentsphere-deployment.yml | push to main              | On every push           |
| deploy-to-pages-live.yml   | push to main              | On every push           |
| docker-build-push.yml      | push to main + Dockerfile | On push with Dockerfile |
| generate-pages-index.yml   | schedule                  | Every 6 hours           |
| build-pages-site.yml       | workflow_run              | After walkthrough       |

## Strategy Selection Logic

```
Repository Analysis
    ↓
Has package.json with React/Vue/Angular? → Strategy A (Pages Direct)
    ↓
Has Dockerfile? → Strategy B (Docker)
    ↓
Has docker-compose.yml? → Strategy C (Codespaces)
    ↓
Has bin in package.json? → Strategy D (None - CLI)
    ↓
Default → Strategy A or B based on file analysis
```

## Output Locations

```
Generated Files (in each repo):
├── .agentsphere.yml
├── .devcontainer/devcontainer.json
├── DOCKER_RUN.md
├── docker-metadata.json
└── .github/deployments/docker.yml

Registry Files (in .github repo):
├── docs/_data/walkthroughs.yml
├── docs/_data/app-deployments.yml
├── docs/index.md
└── docs/tutorials/index.md

Live Outputs:
├── https://agentsphere.dev/{{ORG_NAME}}/[repo]
├── https://{{ORG_NAME}}.github.io
├── https://{{ORG_NAME}}.github.io/[repo] (Strategy A)
└── ghcr.io/{{ORG_NAME}}/[repo]:latest (Strategy B)
```

______________________________________________________________________

**Legend:**

- ✅ = Completed
- → = Data flow
- ├─ = Dependency
- ▼ = Sequential flow
- 1️⃣ 2️⃣ 3️⃣ = Workflow number
