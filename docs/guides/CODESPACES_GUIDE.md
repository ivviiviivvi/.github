# GitHub Codespaces Configuration Guide

Complete guide for using GitHub Codespaces with this repository.

## Quick Start

### Create a Codespace

**Via Web**:

1. Go to repository on GitHub
1. Click "Code" → "Codespaces" tab
1. Click "Create codespace on main"

**Via CLI**:

```bash
gh codespace create --repo {{ORG_NAME}}/.github
```

**Via URL**:

```
https://github.dev/{{ORG_NAME}}/.github
```

## Configuration

Codespaces uses the same `.devcontainer` configuration as VS Code Desktop!

### Resource Configuration

Edit `.devcontainer/devcontainer.json`:

```json
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  }
}
```

**Available Machine Types**:

- 2-core: 8GB RAM, 32GB storage (Free tier)
- 4-core: 16GB RAM, 32GB storage
- 8-core: 32GB RAM, 64GB storage
- 16-core: 64GB RAM, 128GB storage
- 32-core: 128GB RAM, 256GB storage

### Timeout Configuration

**Set idle timeout**:

```bash
# Via CLI
gh codespace edit --idle-timeout 30m

# Via settings
# Settings → Codespaces → Default idle timeout
```

**Auto-delete after inactivity**:

```bash
# Via CLI
gh codespace edit --retention-period 7d
```

## Features

### Port Forwarding

Ports are automatically forwarded and accessible:

```json
{
  "forwardPorts": [3000, 5000, 8080],
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "notify",
      "visibility": "public"
    }
  }
}
```

**Access forwarded ports**:

- Private: Only you can access
- Organization: Anyone in org can access
- Public: Anyone with link can access

### Secrets

**Add secrets**:

```bash
# Via CLI
gh secret set API_KEY --repos {{ORG_NAME}}/.github

# Or via web
# Settings → Codespaces → Codespace secrets
```

**Use in devcontainer**:

```json
{
  "remoteEnv": {
    "API_KEY": "${localEnv:API_KEY}"
  }
}
```

### Dotfiles

**Auto-install dotfiles**:

1. Create a repo named `dotfiles`
1. Add your configurations
1. Codespaces will auto-clone and run `install.sh`

Example `dotfiles/install.sh`:

```bash
#!/bin/bash
ln -s ~/dotfiles/.bashrc ~/.bashrc
ln -s ~/dotfiles/.gitconfig ~/.gitconfig
```

### Extensions

**Pre-install extensions**:

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.python"
      ]
    }
  }
}
```

## Access Methods

### VS Code Desktop

Connect to Codespace from local VS Code:

```bash
# List codespaces
gh codespace list

# Connect via VS Code
gh codespace code -c <codespace-name>

# Or use VS Code UI
# Remote-Codespaces: Connect to Codespace
```

### Browser

Access via web:

```
https://github.dev/{{ORG_NAME}}/.github
```

Or from Codespace:

```
https://<codespace-name>.github.dev
```

### SSH

Connect via SSH:

```bash
# SSH into codespace
gh codespace ssh

# Copy files
gh codespace cp local-file.txt remote:/workspace/
gh codespace cp remote:/workspace/file.txt ./

# Port forward
gh codespace ports forward 3000:3000
```

### CLI

Execute commands:

```bash
# Run command in codespace
gh codespace ssh -c "npm test"

# Interactive shell
gh codespace ssh
```

## Management

### Lifecycle

**Stop codespace**:

```bash
gh codespace stop
```

**Start codespace**:

```bash
gh codespace start
```

**Delete codespace**:

```bash
gh codespace delete
```

**Rebuild container**:

```bash
# In codespace terminal
# F1 → Codespaces: Rebuild Container
```

### List Codespaces

```bash
# Via CLI
gh codespace list

# With details
gh codespace list --json | jq
```

### Logs

```bash
# View codespace logs
gh codespace logs

# Follow logs
gh codespace logs -f
```

## Cost Management

### Free Tier

**GitHub Free**:

- 120 core-hours/month
- 15GB storage

**GitHub Pro**:

- 180 core-hours/month
- 20GB storage

### Usage Tracking

```bash
# Check usage
gh api /user/codespaces/billing

# Or via web
# Settings → Billing → Codespaces
```

### Optimization Tips

1. **Stop when not using**:

   ```bash
   gh codespace stop
   ```

1. **Set short idle timeout**:

   ```bash
   gh codespace edit --idle-timeout 30m
   ```

1. **Use smaller machine types**:

   - Development: 2-core
   - Building: 4-core
   - Heavy workloads: 8-core+

1. **Auto-delete old codespaces**:

   ```bash
   gh codespace edit --retention-period 7d
   ```

1. **Use prebuilds** (for frequent access):

   ```yaml
   # .github/workflows/codespaces-prebuild.yml
   on:
     push:
       branches: [main]
   ```

## Prebuilds

Speed up codespace creation with prebuilds.

### Enable Prebuilds

1. Go to repository settings
1. Codespaces → Set up prebuilds
1. Select branch and region
1. Configure prebuild triggers

### Prebuild Configuration

```yaml
# .github/workflows/codespaces-prebuild.yml
name: Codespaces Prebuild

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  prebuild:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Prebuild devcontainer
        run: |
          docker buildx build \
            --file .devcontainer/Dockerfile \
            --cache-from type=gha \
            --cache-to type=gha,mode=max \
            .
```

## Team Collaboration

### Shared Codespaces

1. Create codespace
1. Make it public:
   ```bash
   gh codespace edit --visibility org
   ```
1. Share URL with team

### Live Share

1. Install Live Share extension
1. Start session
1. Share link with collaborators
1. Collaborate in real-time

### Code Review in Codespace

```bash
# Create codespace from PR
gh pr checkout <pr-number>
gh codespace create

# Review and test
# Leave comments
# Approve or request changes
```

## Best Practices

### 1. Use Prebuilds

For frequently accessed repos, enable prebuilds to reduce startup time.

### 2. Commit Changes Regularly

Codespaces can be deleted accidentally. Commit and push often.

### 3. Use Secrets for Sensitive Data

Never commit secrets. Use Codespaces secrets or environment variables.

### 4. Set Appropriate Timeouts

Balance between cost and convenience:

- Active development: 30-60 minutes
- Occasional use: 15-30 minutes

### 5. Clean Up Unused Codespaces

```bash
# Delete all stopped codespaces
gh codespace list --json | \
  jq -r '.[] | select(.state == "Shutdown") | .name' | \
  xargs -I {} gh codespace delete -c {}
```

### 6. Use .gitignore

Ensure large files and dependencies aren't committed:

```
node_modules/
.venv/
*.log
.env
```

### 7. Optimize Container Image

Use multi-stage builds and minimize layers.

## Troubleshooting

### Codespace Won't Start

**Check status**:

```bash
gh codespace list
gh codespace logs
```

**Solutions**:

- Check devcontainer configuration
- Verify base image exists
- Review build logs

### Slow Performance

**Check resources**:

```bash
# In codespace terminal
top
df -h
docker stats
```

**Solutions**:

- Upgrade machine type
- Enable prebuilds
- Optimize container image

### Port Forwarding Issues

**Check ports**:

```bash
gh codespace ports
```

**Solutions**:

- Verify service is running
- Check firewall settings
- Try different port

### Connection Timeouts

**Solutions**:

- Check internet connection
- Verify GitHub status
- Try different browser

## Migration Guide

### From Local to Codespaces

1. **Push changes**:

   ```bash
   git add .
   git commit -m "WIP: migrate to codespace"
   git push
   ```

1. **Create codespace**:

   ```bash
   gh codespace create
   ```

1. **Continue work** in browser or VS Code

### From Codespaces to Local

1. **Commit changes** in codespace
1. **Pull changes** locally:
   ```bash
   git pull
   ```
1. **Reopen in local container**

## Advanced Usage

### Custom Lifecycle Scripts

```json
{
  "postCreateCommand": "npm install",
  "postStartCommand": "npm run dev",
  "postAttachCommand": "echo 'Ready!'"
}
```

### Multiple Containers

```yaml
# docker-compose.yml
services:
  app:
    build: .
  db:
    image: postgres
  cache:
    image: redis
```

### GPU Support

```json
{
  "hostRequirements": {
    "gpu": true
  }
}
```

## Resources

- [Codespaces Docs](https://docs.github.com/en/codespaces)
- [DevContainer Spec](https://containers.dev)
- [VS Code Remote](https://code.visualstudio.com/docs/remote/remote-overview)

## Support

- 📖 [Documentation](../INDEX.md)
- 💬
  [Discussions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions)<!-- link:github.discussions -->
- 🐛
  [Issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)<!-- link:github.issues -->

______________________________________________________________________

_Last Updated: 2024-01-01_
