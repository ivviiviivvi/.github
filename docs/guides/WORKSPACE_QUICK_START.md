# Workspace & Containerization Quick Start

Get started with lightweight local systems and flexible remote access in 5
minutes.

## Choose Your Path

### 🖥️ Path 1: VS Code Desktop (Recommended for Primary Development)

**Best for**: Daily development with full IDE features

1. **Install Prerequisites**:

   - [Docker Desktop](https://www.docker.com/products/docker-desktop)<!-- link:docs.docker_desktop -->
   - [VS Code](https://code.visualstudio.com/)<!-- link:docs.vscode -->
   - [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)<!-- link:docs.vscode_remote_containers -->

1. **Clone and Open**:

   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   cd .github
   code .
   ```

1. **Reopen in Container**:

   - Press `F1` → `Dev Containers: Reopen in Container`
   - Wait for build (2-5 minutes first time)
   - Start coding!

**Time to productive**: 5-10 minutes

______________________________________________________________________

### 🌐 Path 2: GitHub Codespaces (Recommended for Quick Access)

**Best for**: Quick access, no local setup, collaboration

1. **Create Codespace**:

   ```bash
   gh codespace create --repo ivviiviivvi/.github
   ```

   Or via GitHub UI: Repository → Code → Codespaces → Create

1. **Start Coding**:

   - Opens automatically in browser
   - Or connect with VS Code Desktop
   - Full development environment ready

**Time to productive**: 2-3 minutes

**Cost**: Free tier includes 60 hours/month

______________________________________________________________________

### 🔧 Path 3: Self-Hosted Code-Server

**Best for**: Self-hosting, team access, no limits

1. **Deploy on Server**:

   ```bash
   # On your server
   git clone YOUR_REPO
   cd YOUR_REPO

   # Set password
   export CODE_SERVER_PASSWORD=$(openssl rand -base64 32)
   export CODE_SERVER_DOMAIN=code.yourdomain.com

   # Deploy
   docker-compose -f docker-compose.code-server.yml up -d
   ```

1. **Setup SSL** (recommended):

   ```bash
   certbot certonly --standalone -d code.yourdomain.com
   ```

1. **Access**:

   - Open `https://code.yourdomain.com`
   - Enter password
   - Start coding!

**Time to productive**: 15-30 minutes (including server setup)

______________________________________________________________________

### 📱 Path 4: Browser-Based (Quick Edits)

**Best for**: Quick edits, reviewing code, mobile access

1. **GitHub.dev** (instant):

   - Press `.` on any GitHub repository
   - Or visit `https://github.dev/ivviiviivvi/.github`
   - Edit files directly

1. **StackBlitz** (for web projects):

   - Visit `https://stackblitz.com/github/ivviiviivvi/.github`
   - Full Node.js environment

1. **GitPod**:

   - Visit `https://gitpod.io/#https://github.com/ivviiviivvi/.github`
   - Full cloud IDE

**Time to productive**: Instant

______________________________________________________________________

## Create New Workspace

### Interactive Mode

```bash
./scripts/workspace/create-workspace.sh --interactive
```

Follow the prompts:

1. Enter workspace name
1. Select template
1. Choose additional services

### Command Line Mode

```bash
# Basic workspace
./scripts/workspace/create-workspace.sh --name my-project

# Full-stack workspace
./scripts/workspace/create-workspace.sh \
  --template fullstack \
  --name web-app \
  --services postgres,redis
```

### Available Templates

1. **basic** - Simple single-language projects
1. **fullstack** - Web apps with database (Node.js, Python, PostgreSQL, Redis)
1. **datascience** - ML/AI with Jupyter (Python, PostgreSQL)
1. **microservices** - Distributed systems
1. **golang** - Go development
1. **rust** - Rust development
1. **java** - Java/Spring Boot
1. **dotnet** - .NET Core

______________________________________________________________________

## Common Tasks

### Check Workspace Health

```bash
./scripts/workspace/health-check.sh
```

### Start Services

```bash
# VS Code Desktop / Code-Server
docker-compose up -d

# Or use NPM script
npm run docker:up
```

### Stop Services

```bash
docker-compose down

# Or
npm run docker:down
```

### View Logs

```bash
docker-compose logs -f

# Or specific service
docker-compose logs -f postgres
```

### Connect to Database

```bash
# PostgreSQL
psql postgresql://devuser:devpass@localhost:5432/devdb  # pragma: allowlist secret

# Or use Adminer web UI
open http://localhost:8080
```

### Access Services

Common service ports:

- **Frontend**: <http://localhost:3000>
- **Backend API**: <http://localhost:3001>
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **MailHog UI**: <http://localhost:8025>
- **Adminer (DB UI)**: <http://localhost:8080>

______________________________________________________________________

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose down
docker-compose up --build
```

### Can't connect to services

```bash
# Check if running
docker-compose ps

# Use service name (not localhost) within container
# ✅ postgresql://devuser:devpass@postgres:5432/devdb
# ❌ postgresql://devuser:devpass@localhost:5432/devdb
```

### Port already in use

```bash
# Find and kill process
lsof -ti:5432 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "5433:5432"  # Use 5433 instead
```

### Performance issues

```bash
# Increase resources in .devcontainer/devcontainer.json
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb"
  }
}
```

______________________________________________________________________

## Next Steps

### Customize Your Workspace

1. **Add VS Code extensions** - Edit `.devcontainer/devcontainer.json`
1. **Add services** - Edit `docker-compose.yml`
1. **Add tools** - Edit `.devcontainer/post-create.sh`

### Learn More

- 📖
  [Complete Protocols](../architecture/WORKSPACE_CONTAINERIZATION_PROTOCOLS.md)
- 🚀 [Codespaces Guide](./CODESPACES_GUIDE.md)
- 🔧 [Code-Server Setup](./CODE_SERVER_SETUP.md)
- 🐳 [Docker Best Practices](DOCKER_BEST_PRACTICES.md)

### Get Help

- 💬
  [Discussions](https://github.com/ivviiviivvi/.github/discussions)<!-- link:github.discussions -->
- 🐛
  [Issues](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

______________________________________________________________________

## Comparison Matrix

| Feature             | VS Code Desktop | Codespaces   | Code-Server  | Browser     |
| ------------------- | --------------- | ------------ | ------------ | ----------- |
| **Setup Time**      | 5-10 min        | 2-3 min      | 15-30 min    | Instant     |
| **Local Resources** | Docker only     | None         | None         | None        |
| **Offline Capable** | ✅              | ❌           | ❌           | ❌          |
| **Full IDE**        | ✅              | ✅           | ✅           | Limited     |
| **Terminal**        | ✅              | ✅           | ✅           | Limited     |
| **Extensions**      | ✅              | ✅           | ✅           | Limited     |
| **Cost**            | Free            | Free tier    | Server cost  | Free        |
| **Team Access**     | Via Git         | ✅           | ✅           | Via Git     |
| **Best For**        | Daily dev       | Quick access | Self-hosting | Quick edits |

______________________________________________________________________

## Tips & Tricks

### 1. Use Aliases

Add to `.bashrc`:

```bash
alias dc='docker-compose'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
```

### 2. Customize Prompt

Show current container:

```bash
export PS1='[\u@container:\w]\$ '
```

### 3. Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

### 4. Hot Reload

For Node.js:

```json
{
  "scripts": {
    "dev": "nodemon src/index.js"
  }
}
```

### 5. Database Migrations

```bash
# Run migrations on startup
# Add to docker-compose.yml
command: sh -c "npm run migrate && npm run dev"
```

______________________________________________________________________

_Last Updated: 2024-01-01_
