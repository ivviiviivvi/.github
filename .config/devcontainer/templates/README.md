# DevContainer Templates

Pre-configured DevContainer templates for different project types.

## Available Templates

### 1. Basic Workspace

**Location**: `basic/` **Use Case**: Simple single-language projects
**Includes**: Base Ubuntu image, Git, basic tools

### 2. Full-Stack Web

**Location**: `fullstack/` **Use Case**: Web applications with database
**Includes**: Node.js, Python, PostgreSQL, Redis, MailHog

### 3. Data Science

**Location**: `datascience/` **Use Case**: ML/AI and data analysis **Includes**:
Python, Jupyter, PostgreSQL, data science libraries

### 4. Microservices

**Location**: `microservices/` **Use Case**: Distributed systems development
**Includes**: Multiple service containers, message queue, monitoring

### 5. Mobile Development

**Location**: `mobile/` **Use Case**: React Native, Flutter development
**Includes**: Android SDK, iOS tools, emulators

### 6. Go Development

**Location**: `golang/` **Use Case**: Go microservices and APIs **Includes**:
Go, PostgreSQL, Redis, air (hot reload)

### 7. Rust Development

**Location**: `rust/` **Use Case**: Rust applications **Includes**: Rust
toolchain, cargo tools, PostgreSQL

### 8. Java Development

**Location**: `java/` **Use Case**: Java/Spring Boot applications **Includes**:
JDK, Maven/Gradle, PostgreSQL, Redis

### 9. .NET Development

**Location**: `dotnet/` **Use Case**: ASP.NET Core applications **Includes**:
.NET SDK, SQL Server, Redis

### 10. Cloud Native

**Location**: `cloud-native/` **Use Case**: Kubernetes-native development
**Includes**: kubectl, helm, kind, docker-in-docker

### 11. Dotfiles-Enabled

**Location**: `dotfiles-enabled/` **Use Case**: Consistent personal dev
environment **Includes**: Chezmoi dotfiles integration, modern CLI tools
(starship, eza, bat, fzf, zoxide, atuin), Neovim + LazyVim, 1Password CLI

This template automatically applies personal dotfiles from
[4444J99/dotfiles](https://github.com/4444J99/dotfiles) for consistent shell
configuration across all org repositories.

## Usage

### Option 1: Copy Template

```bash
# Copy template to your project
cp -r .devcontainer/templates/fullstack/* .devcontainer/

# Customize as needed
code .devcontainer/devcontainer.json

# Open in container
code .
# Dev Containers: Reopen in Container
```

### Option 2: Use Script

```bash
# Use the workspace creation script
./scripts/create-workspace.sh --template fullstack --name my-project
```

### Option 3: Manual Selection (VS Code)

1. Open Command Palette (F1)
1. Select: `Dev Containers: Add Dev Container Configuration Files...`
1. Choose template from list
1. Customize options
1. Reopen in container

## Template Structure

Each template contains:

```
template-name/
├── devcontainer.json      # Main configuration
├── docker-compose.yml     # Service orchestration
├── Dockerfile            # Custom image (if needed)
├── post-create.sh        # Setup script
└── README.md             # Template-specific docs
```

## Customization

### Modify Resources

Edit `devcontainer.json`:

```json
{
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  }
}
```

### Add Services

Edit `docker-compose.yml`:

```yaml
services:
  mongodb:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
```

### Add Tools

Edit `post-create.sh`:

```bash
# Install additional tools
npm install -g yarn pnpm
pip install black flake8
```

## Best Practices

1. **Start with a template** - Don't build from scratch
1. **Customize minimally** - Keep it simple
1. **Version everything** - Pin all versions
1. **Document changes** - Update README
1. **Test thoroughly** - Rebuild container after changes

## Creating Custom Templates

See Template Development Guide

## Support

- 📖
  [Main Protocols](../../../docs/architecture/WORKSPACE_CONTAINERIZATION_PROTOCOLS.md)
- 💬
  [Discussions](https://github.com/ivviiviivvi/.github/discussions)<!-- link:github.discussions -->
- 🐛
  [Issues](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->
