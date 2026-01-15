# Workspace & Containerization Protocols

> **Comprehensive protocols for lightweight local development with flexible
> remote access via VS Code Web, Desktop, and browser-based interfaces**

## Table of Contents

- [Overview](#overview)
- [Core Principles](#core-principles)
- [Architecture](#architecture)
- [Access Methods](#access-methods)
  - [VS Code Desktop](#vs-code-desktop)
  - [VS Code Web (GitHub Codespaces)](#vs-code-web-github-codespaces)
  - [Self-Hosted Code-Server](#self-hosted-code-server)
  - [Browser-Based Development](#browser-based-development)
- [Container Orchestration](#container-orchestration)
- [Workspace Lifecycle](#workspace-lifecycle)
- [Security & Compliance](#security--compliance)
- [Resource Management](#resource-management)
- [Templates & Presets](#templates--presets)
- [Automation & Scripts](#automation--scripts)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

This document defines the comprehensive workspace and containerization protocols
for the **ivi374forivi** organization. The goal is to:

1. **Keep local systems light** - Minimize dependencies on local machines
1. **Enable flexible access** - Work from any device via web or desktop
1. **Standardize environments** - Consistent development experience
1. **Isolate services** - Clean separation of concerns
1. **Maximize portability** - Work from anywhere, anytime

### Design Philosophy

**"Light Local, Heavy Remote, Universal Access"**

- Local machines act as thin clients
- Heavy computation happens in containers
- Access via any interface (web, desktop, SSH)
- State persists independently of access method
- Resources scale based on workload

---

## Core Principles

### 1. Workspace Isolation

Each project/workspace runs in isolated containers with:

- Dedicated filesystems
- Separate networks
- Independent service stacks
- Isolated dependencies

### 2. Stateless Local Systems

Local machines should:

- Require minimal software (browser, Docker, VS Code)
- Not store project dependencies
- Not run development services
- Be easily replaceable

### 3. State Persistence

All workspace state persists via:

- Named Docker volumes
- Git repositories
- Cloud-synced configurations
- Remote databases

### 4. Universal Access

Support multiple access patterns:

- **Desktop**: VS Code + Remote-Containers
- **Web**: GitHub Codespaces
- **Browser**: Code-server (self-hosted)
- **Terminal**: SSH + tmux
- **Mobile**: Browser-based (read-only)

### 5. Security First

- Secrets never stored locally
- Network isolation by default
- Access control at all layers
- Audit logging enabled
- Encrypted communications

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ACCESS LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ VS Code  │  │ Browser  │  │  Mobile  │  │   SSH    │   │
│  │ Desktop  │  │   Web    │  │ Browser  │  │ Terminal │   │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘   │
└────────┼─────────────┼─────────────┼─────────────┼─────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         │       ORCHESTRATION LAYER            │
         │  ┌────────────────────────────┐     │
         │  │   Docker / Docker Compose   │     │
         │  └────────────────────────────┘     │
         └──────────────────┬──────────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         │        WORKSPACE LAYER               │
         │  ┌──────────┐  ┌──────────┐         │
         │  │  Dev     │  │ Services │         │
         │  │Container │  │Container │         │
         │  └──────────┘  └──────────┘         │
         └──────────────────┬──────────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         │        PERSISTENCE LAYER             │
         │  ┌────────┐  ┌────────┐  ┌────────┐│
         │  │ Volumes│  │  Git   │  │ Cloud  ││
         │  │        │  │  Repos │  │ Storage││
         │  └────────┘  └────────┘  └────────┘│
         └─────────────────────────────────────┘
```

### Component Layers

#### 1. Access Layer

- **Purpose**: Provide multiple entry points
- **Components**: VS Code, browsers, terminals
- **Requirements**: Minimal local software

#### 2. Orchestration Layer

- **Purpose**: Manage container lifecycle
- **Components**: Docker, Docker Compose, Kubernetes (optional)
- **Requirements**: Container runtime only

#### 3. Workspace Layer

- **Purpose**: Provide development environments
- **Components**: DevContainers, service containers
- **Requirements**: Defined in compose files

#### 4. Persistence Layer

- **Purpose**: Store state and data
- **Components**: Volumes, repositories, cloud storage
- **Requirements**: Backup and sync strategy

---

## Access Methods

### VS Code Desktop

**Best For**: Primary development with full IDE features

#### Setup

1. **Install Prerequisites**:

   ```bash
   # Install Docker Desktop
   # macOS/Windows: https://www.docker.com/products/docker-desktop

   # Install VS Code
   # https://code.visualstudio.com/

   # Install Remote Development Extension Pack
   code --install-extension ms-vscode-remote.vscode-remote-extensionpack
   ```

1. **Clone and Open**:

   ```bash
   git clone <repository>
   cd <repository>
   code .
   ```

1. **Open in Container**:
   - Press `F1` or `Cmd/Ctrl+Shift+P`
   - Select: `Dev Containers: Reopen in Container`
   - Wait for build (first time only)

#### Configuration

VS Code Desktop uses `.devcontainer/devcontainer.json`:

```json
{
  "name": "My Workspace",
  "dockerComposeFile": "docker-compose.yml",
  "service": "workspace",
  "workspaceFolder": "/workspace",
  "remoteUser": "vscode"
}
```

#### Advantages

- ✅ Full IDE features
- ✅ Native performance
- ✅ Offline capable (after initial setup)
- ✅ Local debugging
- ✅ Rich extension ecosystem

#### Limitations

- ❌ Requires local Docker
- ❌ Initial container build time
- ❌ Local resource usage

---

### VS Code Web (GitHub Codespaces)

**Best For**: Quick access, collaboration, no local setup

#### Setup

1. **Create Codespace**:

   ```bash
   # Via GitHub UI
   # Repository → Code → Codespaces → Create codespace

   # Via GitHub CLI
   gh codespace create --repo ivviiviivvi/.github
   ```

1. **Access Methods**:
   - **Web**: https://github.dev or github.com/codespaces
   - **Desktop**: Connect via VS Code Desktop
   - **SSH**: `gh codespace ssh`

1. **Configuration**: Uses same `.devcontainer` as VS Code Desktop!

#### Advantages

- ✅ Zero local setup
- ✅ Access from anywhere
- ✅ Powerful cloud resources
- ✅ Built-in port forwarding
- ✅ Free tier available

#### Limitations

- ❌ Requires internet
- ❌ Costs for heavy usage
- ❌ Slight latency
- ❌ Idle timeout (default 30 min)

#### Resource Configuration

`.devcontainer/devcontainer.json`:

```json
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  }
}
```

#### Cost Management

**Free Tier**: 60 hours/month (2-core) **Pro**: 90 hours/month (included)

**Optimization**:

```bash
# Set default idle timeout
gh codespace edit --idle-timeout 30m

# Stop when not in use
gh codespace stop

# Delete when done
gh codespace delete
```

---

### Self-Hosted Code-Server

**Best For**: Self-hosted, team access, private cloud

#### Architecture

```
┌─────────────┐
│   Browser   │
│  (HTTPS)    │
└──────┬──────┘
       │
┌──────┴──────┐
│   Nginx     │
│  (Reverse   │
│   Proxy)    │
└──────┬──────┘
       │
┌──────┴──────┐
│code-server  │
│  Container  │
└──────┬──────┘
       │
┌──────┴──────┐
│  Workspace  │
│  Container  │
└─────────────┘
```

#### Setup

1. **Deploy Code-Server**:

Create `docker-compose.code-server.yml`:

```yaml
version: "3.9"

services:
  code-server:
    image: codercom/code-server:latest
    ports:
      - "8080:8080"
    volumes:
      - code-server-config:/home/coder/.config
      - code-server-data:/home/coder/project
    environment:
      - PASSWORD=${CODE_SERVER_PASSWORD}
      - SUDO_PASSWORD=${CODE_SERVER_PASSWORD}
      - PROXY_DOMAIN=${CODE_SERVER_DOMAIN}
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - code-server
    restart: unless-stopped

volumes:
  code-server-config:
  code-server-data:
```

2. **Configure Nginx**:

`nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream code-server {
        server code-server:8080;
    }

    server {
        listen 443 ssl http2;
        server_name code.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://code-server;
            proxy_set_header Host $host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection upgrade;
            proxy_set_header Accept-Encoding gzip;
        }
    }

    server {
        listen 80;
        server_name code.yourdomain.com;
        return 301 https://$host$request_uri;
    }
}
```

3. **Deploy**:

```bash
# Set environment variables
export CODE_SERVER_PASSWORD=$(openssl rand -base64 32)
export CODE_SERVER_DOMAIN=code.yourdomain.com

# Deploy
docker-compose -f docker-compose.code-server.yml up -d

# Access at https://code.yourdomain.com
```

#### Security Hardening

1. **Enable HTTPS**:

   ```bash
   # Use Let's Encrypt
   certbot certonly --standalone -d code.yourdomain.com
   ```

1. **Add Authentication Layer**:

   ```nginx
   # Add OAuth2 Proxy or Basic Auth
   auth_basic "Restricted Access";
   auth_basic_user_file /etc/nginx/.htpasswd;
   ```

1. **Network Isolation**:

   ```yaml
   networks:
     code-network:
       driver: bridge
       internal: false
   ```

#### Advantages

- ✅ Full control over infrastructure
- ✅ No usage limits
- ✅ Data sovereignty
- ✅ Team access with single instance
- ✅ Custom domain and branding

#### Limitations

- ❌ Requires server management
- ❌ Need to handle backups
- ❌ Security responsibility
- ❌ SSL certificate management

---

### Browser-Based Development

**Best For**: Quick edits, mobile access, reviewing code

#### GitHub.dev

**Quick Edit Mode**:

```bash
# Press '.' on any GitHub repo
# Or change .com to .dev in URL
# https://github.dev/ivviiviivvi/.github
```

**Features**:

- ✅ Instant access (no setup)
- ✅ VS Code web interface
- ✅ Git operations
- ✅ Extensions support
- ⚠️ No terminal access
- ⚠️ No build/run capability

#### StackBlitz

**For Web Projects**:

```bash
# Open project in StackBlitz
https://stackblitz.com/github/ivviiviivvi/.github
```

**Features**:

- ✅ Full Node.js environment
- ✅ NPM package installation
- ✅ Live preview
- ✅ Terminal access
- ⚠️ Web projects only
- ⚠️ Limited resources

#### GitPod

**Full Cloud IDE**:

```bash
# Prefix repo URL
https://gitpod.io/#https://github.com/ivviiviivvi/.github
```

**Configuration** (`.gitpod.yml`):

```yaml
image:
  file: .gitpod.Dockerfile

tasks:
  - init: npm install
    command: npm run dev

ports:
  - port: 3000
    onOpen: open-preview

vscode:
  extensions:
    - dbaeumer.vscode-eslint
    - esbenp.prettier-vscode
```

---

## Container Orchestration

### Multi-Container Architecture

#### Basic Structure

Every workspace consists of:

1. **Development Container** - Your coding environment
1. **Service Containers** - Databases, caches, queues
1. **Tool Containers** - Linters, builders, testers

#### Standard Compose File

`.devcontainer/docker-compose.yml`:

```yaml
version: "3.9"

# Define shared network
networks:
  workspace-network:
    driver: bridge

# Define persistent volumes
volumes:
  postgres-data:
  redis-data:
  workspace-cache:

services:
  # Main development container
  workspace:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      # Mount workspace
      - ..:/workspace:cached
      # Mount cache
      - workspace-cache:/home/vscode/.cache
      # Mount SSH keys (optional)
      - ${HOME}/.ssh:/home/vscode/.ssh:ro
    networks:
      - workspace-network
    command: sleep infinity
    environment:
      - NODE_ENV=development
      - PYTHONUNBUFFERED=1
    # Connect to service network
    depends_on:
      - postgres
      - redis
      - mailhog

  # Database service
  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    networks:
      - workspace-network
    environment:
      - POSTGRES_USER=devuser
      - POSTGRES_PASSWORD=devpass
      - POSTGRES_DB=devdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Cache service
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - workspace-network
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Mail testing
  mailhog:
    image: mailhog/mailhog:latest
    networks:
      - workspace-network
    ports:
      - "1025:1025" # SMTP
      - "8025:8025" # Web UI

  # Message queue (optional)
  rabbitmq:
    image: rabbitmq:3-management-alpine
    networks:
      - workspace-network
    ports:
      - "5672:5672" # AMQP
      - "15672:15672" # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=devuser
      - RABBITMQ_DEFAULT_PASS=devpass

  # Monitoring (optional)
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks:
      - workspace-network
    ports:
      - "9090:9090"
```

### Service Isolation

#### Network Isolation

```yaml
networks:
  # Public network (internet access)
  public:
    driver: bridge

  # Private network (no internet)
  private:
    driver: bridge
    internal: true

services:
  workspace:
    networks:
      - public
      - private

  database:
    networks:
      - private # Database has no internet access
```

#### Resource Limits

```yaml
services:
  workspace:
    deploy:
      resources:
        limits:
          cpus: "4.0"
          memory: 8G
        reservations:
          cpus: "2.0"
          memory: 4G

  postgres:
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
        reservations:
          cpus: "1.0"
          memory: 1G
```

### Health Checks

Every service should have health checks:

```yaml
services:
  api:
    image: my-api:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Dependency Management

Use `depends_on` with health checks:

```yaml
services:
  workspace:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
```

---

## Workspace Lifecycle

### Creation

#### 1. Template-Based Creation

```bash
# List available templates
ls .devcontainer/templates/

# Create from template
./scripts/create-workspace.sh \
  --template fullstack \
  --name my-project \
  --services postgres,redis,mailhog
```

#### 2. Custom Creation

```bash
# Initialize workspace
mkdir my-workspace
cd my-workspace

# Copy base devcontainer
cp -r ../.devcontainer/base .devcontainer

# Customize services
code .devcontainer/docker-compose.yml

# Open in container
code .
# Dev Containers: Reopen in Container
```

### Sharing

#### Method 1: Repository-Based

```bash
# Commit .devcontainer to repo
git add .devcontainer
git commit -m "feat: add devcontainer configuration"
git push

# Others can clone and open
git clone <repo>
code <repo>
# Dev Containers: Reopen in Container
```

#### Method 2: Codespace-Based

```bash
# Create shareable Codespace link
gh codespace create --repo <repo>
gh codespace view --json url

# Share URL with team
# Others can access same environment
```

### Backup

#### Automated Backup Strategy

```bash
#!/bin/bash
# scripts/backup-workspace.sh

BACKUP_DIR="${HOME}/.workspace-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WORKSPACE_NAME=$(basename $(pwd))

# Create backup directory
mkdir -p "${BACKUP_DIR}/${WORKSPACE_NAME}"

# Backup volumes
docker-compose ps -q | xargs -I {} docker inspect {} \
  --format '{{range .Mounts}}{{.Name}}{{end}}' | \
  xargs -I {} docker run --rm \
    -v {}:/source \
    -v ${BACKUP_DIR}/${WORKSPACE_NAME}:/backup \
    alpine tar czf /backup/${TIMESTAMP}-{}.tar.gz -C /source .

# Backup configuration
tar czf "${BACKUP_DIR}/${WORKSPACE_NAME}/${TIMESTAMP}-config.tar.gz" \
  .devcontainer .vscode

echo "Backup completed: ${BACKUP_DIR}/${WORKSPACE_NAME}/${TIMESTAMP}"
```

#### Restore Process

```bash
#!/bin/bash
# scripts/restore-workspace.sh

BACKUP_DIR="${HOME}/.workspace-backups"
WORKSPACE_NAME=$1
BACKUP_TIMESTAMP=$2

# List available backups if not specified
if [ -z "$BACKUP_TIMESTAMP" ]; then
  echo "Available backups:"
  ls -1 "${BACKUP_DIR}/${WORKSPACE_NAME}"
  exit 0
fi

# Restore volumes
# (Implementation details)

echo "Restore completed"
```

### Disposal

#### Clean Shutdown

```bash
# Stop containers gracefully
docker-compose down --timeout 30

# Remove orphaned containers
docker-compose down --remove-orphans

# Remove volumes (optional)
docker-compose down -v

# Clean up images
docker image prune -a -f
```

#### Complete Cleanup

```bash
#!/bin/bash
# scripts/cleanup-workspace.sh

# Stop all containers
docker-compose down -v --remove-orphans

# Remove workspace directory
cd ..
rm -rf ./my-workspace

# Clean Docker cache
docker system prune -a -f --volumes

echo "Workspace completely removed"
```

---

## Security & Compliance

### Secret Management

#### Never Store Secrets in Containers

**DON'T**:

```dockerfile
# ❌ NEVER DO THIS
ENV API_KEY=secret123
```

**DO**:

```yaml
# ✅ Use environment variables
services:
  workspace:
    environment:
      - API_KEY=${API_KEY}
```

#### Using Secret Management Tools

**Docker Secrets**:

```yaml
services:
  workspace:
    secrets:
      - api_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
```

**External Secret Managers**:

```bash
# AWS Secrets Manager
export API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id prod/api/key \
  --query SecretString \
  --output text)

# HashiCorp Vault
export API_KEY=$(vault kv get -field=key secret/api)
```

### Access Control

#### Authentication

```yaml
# Require password for code-server
services:
  code-server:
    environment:
      - PASSWORD=${CODE_SERVER_PASSWORD}
      - SUDO_PASSWORD=${CODE_SERVER_SUDO_PASSWORD}
```

#### Authorization

```yaml
# Role-based access
services:
  workspace:
    user: "1000:1000" # Non-root user
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### Network Security

#### Firewall Rules

```yaml
# Only expose necessary ports
services:
  postgres:
    # Don't expose ports externally
    expose:
      - "5432" # Only accessible within network
    # ports:  # Never do this for databases
    #   - "5432:5432"
```

#### TLS/SSL

```yaml
# Always use HTTPS
services:
  nginx:
    volumes:
      - ./ssl/cert.pem:/etc/nginx/ssl/cert.pem:ro
      - ./ssl/key.pem:/etc/nginx/ssl/key.pem:ro
```

### Audit Logging

```yaml
# Enable container logging
services:
  workspace:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "workspace,user"
```

### Compliance

#### GDPR Considerations

- Data location (EU regions)
- Right to erasure (volume deletion)
- Data portability (export features)
- Access logs (who accessed what)

#### SOC 2 Requirements

- Access control (authentication)
- Audit trails (logging)
- Encryption (TLS, volumes)
- Backup procedures

---

## Resource Management

### Container Resource Limits

```yaml
services:
  workspace:
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 8G
          pids: 1000
        reservations:
          cpus: "2"
          memory: 4G
```

### Volume Management

#### Volume Types

```yaml
volumes:
  # Named volume (Docker managed)
  data:

  # Bind mount (host filesystem)
  # - ./host-path:/container-path

  # Tmpfs (memory)
  # type: tmpfs
  # tmpfs:
  #   size: 1000000000  # 1GB
```

#### Volume Cleanup

```bash
# List unused volumes
docker volume ls -f dangling=true

# Remove unused volumes
docker volume prune -f

# Remove specific volume
docker volume rm volume_name
```

### Image Management

#### Multi-Stage Builds

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime stage
FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["node", "index.js"]
```

#### Layer Caching

```dockerfile
# Order by change frequency
FROM node:20-alpine

# Change rarely - first
RUN apk add --no-cache git

# Change sometimes - middle
COPY package*.json ./
RUN npm ci

# Change often - last
COPY . .
```

### Performance Optimization

#### Use Cache Mounts

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm install
```

#### Parallel Processing

```yaml
services:
  worker:
    deploy:
      replicas: 4
```

---

## Templates & Presets

### Basic Workspace

**Use Case**: Simple single-language projects

```yaml
# .devcontainer/docker-compose.yml
version: "3.9"

services:
  workspace:
    image: mcr.microsoft.com/devcontainers/base:ubuntu
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
```

### Full-Stack Workspace

**Use Case**: Web application with database and cache

```yaml
version: "3.9"

services:
  workspace:
    build: .
    volumes:
      - ..:/workspace:cached
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

### Data Science Workspace

**Use Case**: Python data analysis with Jupyter

```yaml
version: "3.9"

services:
  workspace:
    image: jupyter/datascience-notebook:latest
    ports:
      - "8888:8888"
    volumes:
      - ..:/home/jovyan/work:cached
      - jupyter-data:/home/jovyan
    environment:
      - JUPYTER_ENABLE_LAB=yes

  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  jupyter-data:
  postgres-data:
```

### Microservices Workspace

**Use Case**: Multiple services development

```yaml
version: "3.9"

services:
  # API Gateway
  gateway:
    build: ./services/gateway
    ports:
      - "8080:8080"

  # User Service
  user-service:
    build: ./services/users
    depends_on:
      - postgres

  # Order Service
  order-service:
    build: ./services/orders
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine

  redis:
    image: redis:7-alpine
```

---

## Automation & Scripts

### Workspace Setup Script

```bash
#!/bin/bash
# scripts/setup-workspace.sh

set -e

echo "🚀 Setting up workspace..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || {
  echo "❌ Docker not found. Please install Docker Desktop."
  exit 1
}

command -v code >/dev/null 2>&1 || {
  echo "❌ VS Code not found. Please install VS Code."
  exit 1
}

# Verify Docker is running
docker info >/dev/null 2>&1 || {
  echo "❌ Docker is not running. Please start Docker Desktop."
  exit 1
}

# Install VS Code extensions
echo "📦 Installing VS Code extensions..."
code --install-extension ms-vscode-remote.remote-containers
code --install-extension ms-azuretools.vscode-docker

# Create .env file if not exists
if [ ! -f .env ]; then
  echo "📝 Creating .env file..."
  cat > .env <<EOF
# Database
DATABASE_URL=postgresql://devuser:devpass@postgres:5432/devdb

# Redis
REDIS_URL=redis://redis:6379

# Development
NODE_ENV=development
LOG_LEVEL=debug
EOF
fi

echo "✅ Workspace setup complete!"
echo "💡 Run 'code .' and reopen in container to start developing"
```

### Health Check Script

```bash
#!/bin/bash
# scripts/health-check.sh

echo "🏥 Running health checks..."

# Check if containers are running
RUNNING=$(docker-compose ps --services --filter "status=running")
EXPECTED=$(docker-compose config --services)

if [ "$RUNNING" != "$EXPECTED" ]; then
  echo "❌ Not all services are running"
  docker-compose ps
  exit 1
fi

# Check database connection
docker-compose exec -T postgres pg_isready -U devuser || {
  echo "❌ PostgreSQL not ready"
  exit 1
}

# Check Redis connection
docker-compose exec -T redis redis-cli ping | grep -q PONG || {
  echo "❌ Redis not ready"
  exit 1
}

echo "✅ All health checks passed"
```

### Migration Script

```bash
#!/bin/bash
# scripts/migrate-workspace.sh

# Migrate from old workspace to new

OLD_WORKSPACE=$1
NEW_WORKSPACE=$2

echo "📦 Migrating workspace..."

# Stop old workspace
cd "$OLD_WORKSPACE"
docker-compose down

# Export volumes
docker run --rm \
  -v old_postgres_data:/source \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/postgres.tar.gz -C /source .

# Setup new workspace
cd "$NEW_WORKSPACE"
docker-compose up -d postgres

# Import volumes
docker run --rm \
  -v new_postgres_data:/target \
  -v $(pwd)/backup:/backup \
  alpine sh -c "cd /target && tar xzf /backup/postgres.tar.gz"

echo "✅ Migration complete"
```

---

## Best Practices

### 1. Keep Containers Small

```dockerfile
# Use Alpine variants
FROM node:20-alpine

# Clean up in same layer
RUN apk add --no-cache git && \
    npm install && \
    npm cache clean --force
```

### 2. Use Non-Root Users

```dockerfile
# Create non-root user
RUN adduser -D -u 1000 vscode

# Switch to non-root
USER vscode
```

### 3. Version Everything

```yaml
# Pin all versions
services:
  postgres:
    image: postgres:16.1-alpine # Not just '16' or 'latest'
```

### 4. Health Checks Always

```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 5. Graceful Shutdown

```dockerfile
# Handle signals properly
STOPSIGNAL SIGTERM
CMD ["node", "index.js"]
```

### 6. Use .dockerignore

```
.git
.github
node_modules
*.log
.env
.DS_Store
```

### 7. Document Everything

```yaml
# docker-compose.yml
services:
  # Main development container
  # Contains all development tools
  workspace:
    # ... configuration
```

### 8. Automate Repetitive Tasks

```bash
# Add to package.json
{
  "scripts": {
    "docker:up": "docker-compose up -d",
    "docker:down": "docker-compose down",
    "docker:logs": "docker-compose logs -f",
    "docker:clean": "docker-compose down -v"
  }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Container Won't Start

**Symptoms**: Container exits immediately

**Diagnosis**:

```bash
# Check logs
docker-compose logs workspace

# Check exit code
docker-compose ps
```

**Solutions**:

- Check Dockerfile syntax
- Verify base image exists
- Check for port conflicts
- Review environment variables

#### 2. Can't Connect to Services

**Symptoms**: Connection refused errors

**Diagnosis**:

```bash
# Check if service is running
docker-compose ps

# Check network
docker-compose exec workspace ping postgres

# Check ports
docker-compose port postgres 5432
```

**Solutions**:

- Use service name as hostname (not localhost)
- Verify service is healthy
- Check network configuration
- Ensure ports are exposed

#### 3. Slow Performance

**Symptoms**: Operations take too long

**Diagnosis**:

```bash
# Check resource usage
docker stats

# Check disk usage
docker system df
```

**Solutions**:

- Increase resource limits
- Use volume caching (`:cached`)
- Clean up unused resources
- Optimize Dockerfile layers

#### 4. Permission Errors

**Symptoms**: Cannot write to mounted volumes

**Diagnosis**:

```bash
# Check file ownership
ls -la /workspace

# Check user in container
docker-compose exec workspace id
```

**Solutions**:

- Match user UID in container to host
- Use non-root user
- Set correct permissions in Dockerfile

#### 5. Port Already in Use

**Symptoms**: Address already in use

**Diagnosis**:

```bash
# Find process using port
lsof -i :5432
# or
netstat -tulpn | grep 5432
```

**Solutions**:

- Kill process using port
- Change port mapping
- Use different port

### Debug Mode

Enable verbose logging:

```yaml
# docker-compose.yml
services:
  workspace:
    environment:
      - DEBUG=*
      - LOG_LEVEL=debug
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Recovery Procedures

#### Emergency Workspace Rebuild

```bash
# Nuclear option - rebuild everything
docker-compose down -v
docker system prune -a -f
docker-compose up --build --force-recreate
```

#### Restore from Backup

```bash
# Stop workspace
docker-compose down

# Restore volumes
./scripts/restore-workspace.sh my-workspace 20240101_120000

# Start workspace
docker-compose up -d
```

---

## Conclusion

These workspace and containerization protocols provide:

✅ **Lightweight local systems** - Minimal dependencies ✅ **Flexible access** -
Work from anywhere ✅ **Consistent environments** - Same setup everywhere ✅
**Secure isolation** - Protected services ✅ **Easy collaboration** - Share
workspaces instantly ✅ **Disaster recovery** - Backup and restore ✅ **Scalable
architecture** - Grow with your needs

### Next Steps

1. Review your current setup
1. Choose your primary access method
1. Set up your first workspace
1. Automate repetitive tasks
1. Share with your team

### Additional Resources

- [Development Environment Setup](./DEVELOPMENT_ENVIRONMENT_SETUP.md)
- [Docker Best Practices](./guides/DOCKER_BEST_PRACTICES.md)
- [Security Guide](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)

---

**Questions or Issues?**

- 📖 [Documentation](../docs/)
- 💬
  [Discussions](https://github.com/ivviiviivvi/.github/discussions)<!-- link:github.discussions -->
- 🐛
  [Issues](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

_Last Updated: 2024-01-01_
