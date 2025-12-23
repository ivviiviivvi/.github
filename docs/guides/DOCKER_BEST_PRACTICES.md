# Docker & Container Best Practices

Comprehensive guide for containerization and Docker best practices in this repository.

## Table of Contents

- [Dockerfile Best Practices](#dockerfile-best-practices)
- [Multi-Stage Builds](#multi-stage-builds)
- [Security Hardening](#security-hardening)
- [Image Optimization](#image-optimization)
- [Docker Compose](#docker-compose)
- [CI/CD Integration](#cicd-integration)
- [Health Checks](#health-checks)
- [Secrets Management](#secrets-management)

---

## Dockerfile Best Practices

### 1. Use Official Base Images

```dockerfile
# Good: Use official images
FROM node:20-alpine

# Avoid: Random images from Docker Hub
FROM some-random-user/node:latest
```

### 2. Specify Exact Versions

```dockerfile
# Good: Pin to specific version
FROM python:3.11.6-slim

# Avoid: Using 'latest' tag
FROM python:latest
```

### 3. Use .dockerignore

Create a `.dockerignore` file to exclude unnecessary files:

```
.git
.github
.gitignore
.vscode
node_modules
__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache
.coverage
htmlcov
dist
build
*.egg-info
.env
.env.local
README.md
docs/
tests/
*.md
```

### 4. Minimize Layers

```dockerfile
# Good: Combine commands
RUN apt-get update && \
    apt-get install -y \
        package1 \
        package2 \
    && rm -rf /var/lib/apt/lists/*

# Avoid: Multiple RUN commands
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
```

### 5. Order Layers by Change Frequency

```dockerfile
FROM node:20-alpine

# Layers that change less frequently first
WORKDIR /app

# Copy dependency files (changes rarely)
COPY package*.json ./
RUN npm ci --only=production

# Copy source code (changes frequently)
COPY . .

# Build and run
RUN npm run build
CMD ["npm", "start"]
```

---

## Multi-Stage Builds

### Node.js Example

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build
RUN npm prune --production

# Stage 2: Production
FROM node:20-alpine

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Python Example

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["python", "app.py"]
```

### Go Example

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Production
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy the binary from builder
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
```

---

## Security Hardening

### 1. Run as Non-Root User

```dockerfile
# Create and use non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### 2. Use Read-Only Root Filesystem

```dockerfile
# In docker-compose.yml or run command
docker run --read-only --tmpfs /tmp myimage
```

```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    read_only: true
    tmpfs:
      - /tmp
```

### 3. Scan for Vulnerabilities

```bash
# Using Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myimage:latest

# Using Snyk
snyk container test myimage:latest
```

### 4. Don't Include Secrets

```dockerfile
# Bad: Don't do this
ENV API_KEY=secret123

# Good: Use Docker secrets or environment variables at runtime
# Set at runtime: docker run -e API_KEY=$API_KEY myimage
```

### 5. Minimize Attack Surface

```dockerfile
# Remove unnecessary packages
RUN apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*
```

---

## Image Optimization

### 1. Use Alpine Linux

```dockerfile
FROM node:20-alpine  # ~180MB instead of
FROM node:20         # ~950MB
```

### 2. Use Distroless Images

```dockerfile
FROM gcr.io/distroless/nodejs20-debian11
COPY --from=builder /app /app
WORKDIR /app
CMD ["index.js"]
```

### 3. Optimize Layer Caching

```dockerfile
# Copy only what's needed for dependency installation first
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Then copy the rest
COPY . .
```

### 4. Use BuildKit

```bash
# Enable BuildKit for better caching and parallelization
DOCKER_BUILDKIT=1 docker build -t myimage .
```

### 5. Compress Images

```dockerfile
# Use --squash flag (experimental)
docker build --squash -t myimage .

# Or use dive to analyze layers
dive myimage:latest
```

---

## Docker Compose

### Development Setup

```yaml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
      args:
        NODE_ENV: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

### Production Setup

```yaml
version: '3.9'

services:
  app:
    image: myapp:${VERSION:-latest}
    restart: always
    read_only: true
    tmpfs:
      - /tmp
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    secrets:
      - api_key
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

secrets:
  api_key:
    external: true
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ steps.meta.outputs.version }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## Health Checks

### Dockerfile HEALTHCHECK

```dockerfile
# Node.js
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Python
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python healthcheck.py || exit 1

# Simple HTTP check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### Health Check Script (healthcheck.js)

```javascript
const http = require('http');

const options = {
  host: 'localhost',
  port: 3000,
  path: '/health',
  timeout: 2000
};

const req = http.request(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
});

req.on('error', () => {
  process.exit(1);
});

req.end();
```

---

## Secrets Management

### Using Docker Secrets

```bash
# Create a secret
echo "my-secret-value" | docker secret create api_key -

# Use in service
docker service create \
  --secret api_key \
  --name myapp \
  myimage
```

### Using Environment Files

```bash
# .env file (never commit to git!)
API_KEY=secret123
DATABASE_URL=postgresql://...

# Use with docker-compose
docker-compose --env-file .env up
```

### Using Build Secrets

```dockerfile
# Dockerfile
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm install

# Build command
docker build --secret id=npm_token,src=$HOME/.npmrc .
```

---

## Best Practices Checklist

- [ ] Use official base images
- [ ] Pin specific versions (no `:latest`)
- [ ] Use multi-stage builds
- [ ] Run as non-root user
- [ ] Include health checks
- [ ] Use .dockerignore
- [ ] Minimize layers
- [ ] Scan for vulnerabilities
- [ ] Use secrets properly
- [ ] Add labels and metadata
- [ ] Configure resource limits
- [ ] Implement logging
- [ ] Test images before deployment
- [ ] Document build process

---

**Last Updated**: 2024-11-08
