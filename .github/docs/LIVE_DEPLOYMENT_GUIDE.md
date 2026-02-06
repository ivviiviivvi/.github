# Live Deployment Guide

## Overview

This guide covers the automated deployment system that takes your applications
from GitHub repositories to live, running instances accessible via GitHub Pages,
Docker containers, or GitHub Codespaces.

## How Live Deployment Works

### Automatic Detection

When you push code to your repository, the deployment workflow automatically:

1. **Analyzes repository structure** (package.json, Dockerfile, etc.)
1. **Detects application type** (React, Flask, Express, etc.)
1. **Selects deployment strategy** (Pages, Docker, Codespaces, or None)
1. **Executes deployment** with appropriate tools and configuration
1. **Updates registry** with deployment status and URLs
1. **Creates PR** with deployment details

### Deployment Strategies

Four strategies are available, automatically selected based on your application:

| Strategy         | Description                          | Best For                         | Output             |
| ---------------- | ------------------------------------ | -------------------------------- | ------------------ |
| **Pages Direct** | Static site deployed to GitHub Pages | React, Vue, Angular, Static HTML | Live URL           |
| **Docker**       | Containerized deployment             | Express, Flask, Django APIs      | Docker image       |
| **Codespaces**   | Full dev environment                 | Microservices, complex apps      | Codespaces button  |
| **None**         | No live deployment                   | CLI tools, libraries             | Documentation only |

## Supported Deployment Strategies

### Strategy A: Pages Direct (Static Apps)

**Automatic Detection:**

- Presence of `package.json` with React, Vue, or Angular
- `index.html` without backend frameworks
- Next.js applications with static export

**Setup Requirements:**

1. Buildable to static files
1. Build outputs to `/build`, `/dist`, or `/out`
1. No server-side requirements

**Configuration Example:**

```yaml
# .github/app-deployment-config.yml
deployment_strategy: pages_direct
app_type: react
build:
  command: npm run build
  output_dir: build
  node_version: "20"
```

**Build Process:**

```bash
# Automatic steps:
1. npm ci
2. npm run build
3. Deploy to GitHub Pages
4. Access at: https://[username].github.io/[repo]
```

**Example Apps:**

- React single-page applications
- Vue.js projects
- Angular applications
- Static documentation sites
- Portfolio websites

**Customization:**

Create custom build configuration:

```yaml
# .github/app-deployment-config.yml
deployment_strategy: pages_direct
build:
  command: npm run build:prod
  output_dir: dist
  install_command: npm ci --production
environment_variables:
  REACT_APP_API_URL: https://api.example.com
  PUBLIC_URL: /my-app
```

### Strategy B: Docker (Backend Apps)

**Automatic Detection:**

- Presence of `Dockerfile`
- Backend frameworks (Express, Flask, Django, FastAPI)
- Node.js with server dependencies

**Setup Requirements:**

1. Valid `Dockerfile` in repository root
1. Application exposes a port
1. Health check endpoint (recommended)

**Dockerfile Example (Node.js):**

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

**Dockerfile Example (Python/Flask):**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

**Docker Hub Setup:**

1. Create account at https://hub.docker.com
1. Generate access token
1. Add to GitHub Secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_TOKEN`: Your access token

**Using GitHub Container Registry (Alternative):**

No setup required! Uses GitHub token automatically:

- Images pushed to: `ghcr.io/[username]/[repo]`
- Accessible with: `docker pull ghcr.io/[username]/[repo]`

**Running Your Docker Container:**

```bash
# Pull the image
docker pull ghcr.io/{{ORG_NAME}}/my-app:latest

# Run the container
docker run -d \
  --name my-app \
  -p 3000:3000 \
  -e NODE_ENV=production \
  ghcr.io/{{ORG_NAME}}/my-app:latest

# View logs
docker logs -f my-app

# Stop container
docker stop my-app
```

**Configuration:**

```yaml
# .github/app-deployment-config.yml
deployment_strategy: docker
port: 3000
docker:
  expose_ports:
    - 8080
  volumes:
    - ./data:/app/data
  build_args:
    NODE_ENV: production
health_check:
  enabled: true
  url: /health
  timeout: 30
```

### Strategy C: Codespaces (Complex Apps)

**Automatic Detection:**

- Presence of `docker-compose.yml`
- Multiple services/microservices
- Existing `.devcontainer/devcontainer.json`

**Setup Requirements:**

1. GitHub account with Codespaces access
1. Repository with complex architecture
1. Optional: Custom devcontainer configuration

**devcontainer.json Setup:**

The workflow auto-generates this file if it doesn't exist:

```json
{
  "name": "My App",
  "image": "mcr.microsoft.com/devcontainers/universal:latest",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-python.python"
      ]
    }
  },
  "forwardPorts": [3000, 5000, 8080],
  "postCreateCommand": "npm install && pip install -r requirements.txt"
}
```

**Custom Configuration:**

```yaml
# .github/app-deployment-config.yml
deployment_strategy: codespaces
codespaces:
  machine_size: large # default, large, xlarge
  features:
    - node
    - python
    - docker-in-docker
    - git
  extensions:
    - dbaeumer.vscode-eslint
    - esbenp.prettier-vscode
    - ms-python.python
  post_create_command: |
    npm install
    pip install -r requirements.txt
    docker-compose up -d database
```

**Using Codespaces:**

1. Click "Open in GitHub Codespaces" badge in README
1. Wait for environment to build (2-5 minutes first time)
1. Start developing immediately
1. All ports auto-forwarded to web browser

**Example Use Cases:**

- Microservices with multiple containers
- Full-stack apps with database
- Applications requiring specific dev tools
- Complex build processes

### Strategy D: None (CLI/Libraries)

**Automatic Detection:**

- `"bin"` field in package.json
- `entry_points` in setup.py
- No web server dependencies
- No Dockerfile or static build output

**What Happens:**

- No live deployment created
- Video walkthrough remains primary showcase
- Documentation and source code highlighted
- Installation instructions generated

**Configuration:**

```yaml
# .github/app-deployment-config.yml
deployment_strategy: none
app_type: cli
```

**Example Apps:**

- Command-line utilities
- npm packages
- Python libraries
- Build tools
- Developer utilities

## Deployment Requirements by Strategy

### Pages Direct Requirements

✅ **Required:**

- Buildable to static HTML/CSS/JS
- No server-side runtime dependencies
- Build command in package.json

❌ **Not Supported:**

- Server-side rendering (SSR)
- Database connections
- File system writes
- WebSocket servers

### Docker Requirements

✅ **Required:**

- Valid Dockerfile
- Application binds to 0.0.0.0 (not localhost)
- Exposed port documented

📝 **Recommended:**

- Health check endpoint
- Graceful shutdown handling
- Environment variable configuration
- Multi-stage builds for efficiency

❌ **Limitations:**

- Max image size: 10GB
- Must be publicly accessible or use GitHub Container Registry

### Codespaces Requirements

✅ **Required:**

- GitHub account with Codespaces access
- Repository \<10GB
- Valid devcontainer.json or auto-generated

💰 **Costs:**

- Free tier: 120 core-hours/month
- Paid plans: Usage-based billing
- Billing details: https://github.com/pricing

❌ **Limitations:**

- Not suitable for simple static sites
- Requires GitHub authentication
- Environment builds take time (2-5 min)

## Troubleshooting

### App Won't Start

**Pages Direct Issues:**

```bash
# Check build logs in GitHub Actions
# Common issues:
1. Build command fails
2. Wrong output directory
3. Missing environment variables
4. Base URL configuration

# Solutions:
# Update _config.yml or app-deployment-config.yml
build:
  command: npm run build
  output_dir: build  # or dist, out
environment_variables:
  PUBLIC_URL: /repo-name
```

**Docker Issues:**

```bash
# Test locally first:
docker build -t myapp .
docker run -p 3000:3000 myapp

# Common issues:
1. Port not exposed in Dockerfile
2. App binding to localhost instead of 0.0.0.0
3. Missing dependencies in Dockerfile

# Solutions:
# Dockerfile: Ensure EXPOSE directive
EXPOSE 3000

# Application code:
# ❌ Wrong:
app.listen(3000, 'localhost')

# ✅ Correct:
app.listen(3000, '0.0.0.0')
```

### Port Conflicts

**Issue:** Application fails to start due to port already in use.

**Solution:**

```yaml
# .github/app-deployment-config.yml
port: 8080  # Change to available port

# Update application code:
const PORT = process.env.PORT || 8080;
```

### Docker Build Failures

**Issue:** Docker build fails during CI.

**Diagnosis:**

```bash
# Check build logs in GitHub Actions
# Look for:
- Missing dependencies
- Network timeouts
- Permission errors
- Disk space issues
```

**Solutions:**

```dockerfile
# Use multi-stage builds to reduce size
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
CMD ["npm", "start"]

# Clean up after installs
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Use .dockerignore to exclude files
# Create .dockerignore:
node_modules
.git
.env
*.md
tests/
```

### Codespaces Issues

**Issue:** Codespaces environment fails to build.

**Solutions:**

1. **Check devcontainer.json syntax:**

```bash
# Validate JSON
cat .devcontainer/devcontainer.json | jq .
```

2. **Reduce features:**

```json
{
  "image": "mcr.microsoft.com/devcontainers/universal:latest",
  "features": {
    // Remove unnecessary features
    "ghcr.io/devcontainers/features/node:1": {}
  }
}
```

3. **Use simpler base image:**

```json
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu"
}
```

### Performance Optimization

**Pages Direct:**

```yaml
# Enable caching
build:
  cache_dependencies: true

# Use production builds
environment_variables:
  NODE_ENV: production

# Compress assets
advanced:
  compression: true
```

**Docker:**

```dockerfile
# Layer caching optimization
# Copy dependencies first (changes less frequently)
COPY package*.json ./
RUN npm ci

# Copy application code last (changes frequently)
COPY . .

# Use alpine images (smaller size)
FROM node:20-alpine

# Multi-stage builds
FROM node:20-alpine AS builder
# ... build steps ...
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
```

**Codespaces:**

```yaml
# Use smaller machine size when possible
codespaces:
  machine_size: default # Not large

  # Minimize post-create commands
  post_create_command: "npm ci" # Use ci instead of install
```

## Performance Tips per Strategy

### Pages Direct Performance

1. **Optimize Bundle Size:**

```bash
# Analyze bundle
npm run build -- --profile
npx webpack-bundle-analyzer
```

2. **Code Splitting:**

```javascript
// React lazy loading
const Component = React.lazy(() => import("./Component"));
```

3. **Image Optimization:**

```bash
# Use WebP format
# Lazy load images
<img loading="lazy" src="image.jpg" />
```

### Docker Performance

1. **Reduce Image Size:**

```dockerfile
# Use alpine images
FROM node:20-alpine

# Multi-stage builds
FROM builder AS final

# Remove dev dependencies
RUN npm prune --production
```

2. **Layer Caching:**

```dockerfile
# Order matters! Change less → change more
COPY package*.json ./
RUN npm ci
COPY . .
```

3. **Health Checks:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1
```

### Codespaces Performance

1. **Prebuilds:**

```yaml
# .github/workflows/codespaces-prebuild.yml
# Enable prebuilds for faster startup
```

2. **Optimize Post-Create:**

```json
{
  "postCreateCommand": "npm ci --prefer-offline"
}
```

## Cost Considerations

### Pages Direct

- **Cost:** FREE
- **Bandwidth:** 100GB/month
- **Build minutes:** 2000 minutes/month (free tier)

### Docker (GitHub Container Registry)

- **Storage:** 500MB free, then $0.25/GB/month
- **Bandwidth:** Unlimited for public packages
- **Build minutes:** Uses GitHub Actions minutes

### Codespaces

- **Free tier:** 120 core-hours/month
- **Paid:**
  - 2-core: $0.18/hour
  - 4-core: $0.36/hour
  - 8-core: $0.72/hour
- **Storage:** $0.07/GB/month

## Security Considerations

### All Strategies

1. **Never commit secrets:**

```bash
# Use GitHub Secrets
${{ secrets.API_KEY }}
```

2. **Validate inputs:**

```javascript
// Sanitize user input
const sanitized = DOMPurify.sanitize(userInput);
```

3. **Use HTTPS:**

```yaml
security:
  https_enabled: true
```

### Docker-Specific

1. **Scan images:**

```bash
docker scan myapp:latest
```

2. **Use official base images:**

```dockerfile
FROM node:20-alpine  # Official Node image
```

3. **Run as non-root:**

```dockerfile
USER node
```

### Codespaces-Specific

1. **Limit scope:**

```json
{
  "customizations": {
    "codespaces": {
      "repositories": {
        "owner/repo": {
          "permissions": ["contents:read"]
        }
      }
    }
  }
}
```

## Related Documentation

- AgentSphere Setup Guide
- [GitHub Pages Setup Guide](GITHUB_PAGES_SETUP.md)
- [Docker Documentation](https://docs.docker.com)
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)<!-- link:docs.github_actions -->

## Getting Help

- **Issues:**
  [Report a problem](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->
- **Discussions:**
  [Ask questions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions)<!-- link:github.discussions -->
- **Documentation:** [Main README](../../README.md)
