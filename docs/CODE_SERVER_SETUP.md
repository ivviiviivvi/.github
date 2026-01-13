# Self-Hosted Code-Server Setup Guide

Complete guide for setting up and managing self-hosted VS Code in the browser using code-server.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Configuration](#configuration)
- [Security](#security)
- [Deployment Options](#deployment-options)
- [Management](#management)
- [Troubleshooting](#troubleshooting)

---

## Overview

**code-server** is VS Code running on a remote server, accessible through a browser. Perfect for:

- ✅ Self-hosted development environments
- ✅ Team access to shared environments
- ✅ Development from any device
- ✅ Full control over infrastructure
- ✅ No usage limits or costs

### Architecture

```
┌─────────────┐
│   Browser   │  (HTTPS)
└──────┬──────┘
       │
┌──────┴──────┐
│   Nginx     │  (Reverse Proxy + SSL)
└──────┬──────┘
       │
┌──────┴──────┐
│code-server  │  (VS Code in browser)
└──────┬──────┘
       │
┌──────┴──────┐
│  Workspace  │  (Development environment)
└─────────────┘
```

---

## Prerequisites

### Server Requirements

**Minimum**:
- 2 CPU cores
- 4GB RAM
- 20GB storage
- Ubuntu 20.04+ or similar

**Recommended**:
- 4+ CPU cores
- 8GB+ RAM
- 50GB+ storage
- SSD storage

### Software Requirements

- Docker & Docker Compose
- Domain name (for SSL)
- SSH access to server

---

## Installation Methods

### Method 1: Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.9'

networks:
  code-network:
    driver: bridge

volumes:
  code-config:
  code-data:
  workspace:

services:
  code-server:
    image: codercom/code-server:latest
    container_name: code-server
    restart: unless-stopped
    networks:
      - code-network
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - code-config:/home/coder/.config
      - code-data:/home/coder/.local
      - workspace:/home/coder/project
    environment:
      - PASSWORD=${CODE_SERVER_PASSWORD}
      - SUDO_PASSWORD=${CODE_SERVER_PASSWORD}
      - PROXY_DOMAIN=${CODE_SERVER_DOMAIN}
      - TZ=UTC
    command: --auth password

  nginx:
    image: nginx:alpine
    container_name: code-nginx
    restart: unless-stopped
    networks:
      - code-network
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - code-server
```

### Method 2: Standalone Installation

```bash
# Install on Ubuntu/Debian
curl -fsSL https://code-server.dev/install.sh | sh

# Start service
sudo systemctl enable --now code-server@$USER

# Check status
sudo systemctl status code-server@$USER
```

### Method 3: Binary Installation

```bash
# Download latest release
VERSION=$(curl -s https://api.github.com/repos/coder/code-server/releases/latest | grep -Po '"tag_name": "v\K[^"]*')
curl -fOL https://github.com/coder/code-server/releases/download/v$VERSION/code-server_${VERSION}_amd64.deb

# Install
sudo dpkg -i code-server_${VERSION}_amd64.deb

# Configure
mkdir -p ~/.config/code-server
cat > ~/.config/code-server/config.yaml <<EOF
bind-addr: 127.0.0.1:8080
auth: password
password: YOUR_SECURE_PASSWORD
cert: false
EOF

# Start
code-server
```

---

## Configuration

### Basic Configuration

Create `.env` file:

```bash
# Security
CODE_SERVER_PASSWORD=$(openssl rand -base64 32)
CODE_SERVER_DOMAIN=code.yourdomain.com

# Optional: HTTPS (if not using reverse proxy)
# CODE_SERVER_CERT=/path/to/cert.pem
# CODE_SERVER_CERT_KEY=/path/to/key.pem
```

### Nginx Reverse Proxy

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=code:10m rate=10r/s;
    
    # Upstream
    upstream code-server {
        server code-server:8080;
    }

    # HTTP redirect to HTTPS
    server {
        listen 80;
        server_name code.yourdomain.com;
        
        # Let's Encrypt ACME challenge
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name code.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # WebSocket support
        location / {
            proxy_pass http://code-server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket headers
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # Timeouts
            proxy_connect_timeout 7d;
            proxy_send_timeout 7d;
            proxy_read_timeout 7d;

            # Rate limiting
            limit_req zone=code burst=20 nodelay;
        }
    }
}
```

### VS Code Settings

Create `settings.json` (mounted at `/home/coder/.local/share/code-server/User/settings.json`):

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "workbench.colorTheme": "Default Dark+",
  "terminal.integrated.shell.linux": "/bin/bash",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
```

### Extensions

Pre-install extensions:

```bash
# Via Docker build
FROM codercom/code-server:latest

# Install extensions
RUN code-server --install-extension dbaeumer.vscode-eslint \
    && code-server --install-extension esbenp.prettier-vscode \
    && code-server --install-extension ms-python.python \
    && code-server --install-extension GitHub.copilot
```

Or via script:

```bash
#!/bin/bash
# install-extensions.sh

EXTENSIONS=(
  "dbaeumer.vscode-eslint"
  "esbenp.prettier-vscode"
  "ms-python.python"
  "GitHub.copilot"
)

for ext in "${EXTENSIONS[@]}"; do
  code-server --install-extension "$ext"
done
```

---

## Security

### 1. HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d code.yourdomain.com

# Copy to nginx directory
sudo cp /etc/letsencrypt/live/code.yourdomain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/code.yourdomain.com/privkey.pem ./ssl/

# Auto-renewal
sudo crontab -e
# Add: 0 0 * * * certbot renew --quiet
```

### 2. Authentication

**Built-in Password**:
```yaml
environment:
  - PASSWORD=${CODE_SERVER_PASSWORD}
```

**OAuth2 Proxy** (Recommended for teams):

```yaml
services:
  oauth2-proxy:
    image: quay.io/oauth2-proxy/oauth2-proxy:latest
    command:
      - --provider=github
      - --email-domain=*
      - --upstream=http://code-server:8080
      - --http-address=0.0.0.0:4180
    environment:
      OAUTH2_PROXY_CLIENT_ID: ${GITHUB_CLIENT_ID}
      OAUTH2_PROXY_CLIENT_SECRET: ${GITHUB_CLIENT_SECRET}
      OAUTH2_PROXY_COOKIE_SECRET: ${COOKIE_SECRET}
    ports:
      - "4180:4180"
```

### 3. Firewall

```bash
# Allow only necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable

# Block direct access to code-server
# (only accessible via nginx)
```

### 4. Access Control

**IP Whitelist** (nginx):
```nginx
location / {
    # Allow specific IPs
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
    
    proxy_pass http://code-server;
}
```

### 5. Security Headers

Already included in nginx config above.

### 6. Regular Updates

```bash
# Update code-server
docker-compose pull
docker-compose up -d

# Or for standalone
curl -fsSL https://code-server.dev/install.sh | sh
```

---

## Deployment Options

### Option 1: DigitalOcean Droplet

```bash
# Create droplet
doctl compute droplet create code-server \
  --region nyc1 \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --ssh-keys YOUR_SSH_KEY_ID

# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Install Docker
curl -fsSL https://get.docker.com | sh

# Deploy
git clone YOUR_REPO
cd YOUR_REPO
docker-compose up -d
```

### Option 2: AWS EC2

```bash
# Launch EC2 instance
# t3.medium (2 vCPU, 4GB RAM)
# Ubuntu 22.04 AMI
# Security group: 80, 443, 22

# SSH into instance
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install and deploy
# (same as above)
```

### Option 3: Self-Hosted Server

```bash
# On your server
# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone repo and deploy
git clone YOUR_REPO
cd YOUR_REPO
docker-compose up -d
```

### Option 4: Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: code-server
  template:
    metadata:
      labels:
        app: code-server
    spec:
      containers:
      - name: code-server
        image: codercom/code-server:latest
        ports:
        - containerPort: 8080
        env:
        - name: PASSWORD
          valueFrom:
            secretKeyRef:
              name: code-server-secret
              key: password
        volumeMounts:
        - name: workspace
          mountPath: /home/coder/project
      volumes:
      - name: workspace
        persistentVolumeClaim:
          claimName: code-server-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: code-server
spec:
  selector:
    app: code-server
  ports:
  - port: 8080
    targetPort: 8080
  type: LoadBalancer
```

---

## Management

### Start/Stop

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f code-server
```

### Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/code-server"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup volumes
docker run --rm \
  -v code-data:/source \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/code-data-${TIMESTAMP}.tar.gz -C /source .

docker run --rm \
  -v workspace:/source \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/workspace-${TIMESTAMP}.tar.gz -C /source .

echo "Backup completed: $BACKUP_DIR"
```

### Restore

```bash
#!/bin/bash
# restore.sh

BACKUP_FILE=$1

docker run --rm \
  -v code-data:/target \
  -v $(dirname $BACKUP_FILE):/backup \
  alpine sh -c "cd /target && tar xzf /backup/$(basename $BACKUP_FILE)"

echo "Restore completed"
```

### Monitoring

```bash
# Resource usage
docker stats code-server

# Logs
docker logs -f code-server

# Health check
curl -f http://localhost:8080/healthz || exit 1
```

---

## Troubleshooting

### Can't Access Code-Server

**Check if running**:
```bash
docker-compose ps
docker logs code-server
```

**Check firewall**:
```bash
sudo ufw status
```

**Check DNS**:
```bash
dig code.yourdomain.com
```

### Performance Issues

**Increase resources**:
```yaml
services:
  code-server:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

**Check resource usage**:
```bash
docker stats
```

### SSL Certificate Issues

**Test certificate**:
```bash
openssl s_client -connect code.yourdomain.com:443
```

**Renew certificate**:
```bash
sudo certbot renew
```

### WebSocket Connection Failed

**Check nginx config**:
```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

---

## Best Practices

1. **Use HTTPS** - Always encrypt traffic
2. **Strong passwords** - Use password generator
3. **Regular backups** - Automate backups
4. **Monitor resources** - Set up alerts
5. **Keep updated** - Regular security updates
6. **Limit access** - Use IP whitelist or VPN
7. **Use OAuth** - For team access

---

## Resources

- [code-server Documentation](https://coder.com/docs/code-server)
- [VS Code Web](https://code.visualstudio.com/docs/remote/vscode-server)
- [Docker Docs](https://docs.docker.com/)

## Support

- 📖 [Main Protocols](./WORKSPACE_CONTAINERIZATION_PROTOCOLS.md)
- 💬 [Discussions](https://github.com/ivviiviivvi/.github/discussions)
- 🐛 [Issues](https://github.com/ivviiviivvi/.github/issues)

---

*Last Updated: 2024-01-01*
