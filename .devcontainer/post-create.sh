#!/bin/bash
set -euo pipefail

echo "🚀 Setting up development environment..."

# Install 1Password CLI (op) for consistent secret sourcing (local + Codespaces).
# In Codespaces/devcontainers, desktop app integration is usually unavailable,
# so Secrets Automation (OP_SERVICE_ACCOUNT_TOKEN) is the recommended auth method.
echo "🔐 Ensuring 1Password CLI (op) is installed..."
if ! command -v op >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y curl gpg

  sudo install -d -m 0755 /usr/share/keyrings
  curl -fsSL https://downloads.1password.com/linux/keys/1password.asc | gpg --dearmor | sudo tee /usr/share/keyrings/1password-archive-keyring.gpg >/dev/null

  arch="$(dpkg --print-architecture)"
  echo "deb [arch=${arch} signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/${arch} stable main" \
    | sudo tee /etc/apt/sources.list.d/1password.list >/dev/null

  sudo apt-get update
  sudo apt-get install -y 1password-cli
else
  echo "✅ 1Password CLI already installed: $(op --version)"
fi

# Install global npm packages
echo "📦 Installing global npm packages..."
npm install -g \
  typescript \
  ts-node \
  nodemon \
  prettier \
  eslint \
  jest \
  @stryker-mutator/core \
  semantic-release \
  @commitlint/cli \
  @commitlint/config-conventional

# Install Python packages
echo "🐍 Installing Python packages..."
pip install --user \
  black \
  flake8 \
  mypy \
  pytest \
  pytest-cov \
  bandit \
  safety \
  pre-commit \
  python-semantic-release

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
if [ -f ".pre-commit-config.yaml" ]; then
  pre-commit install
  pre-commit install --hook-type commit-msg
fi

# Setup git configuration
echo "⚙️ Configuring git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main
git config --global pull.rebase false

# Install project dependencies if they exist
if [ -f "package.json" ]; then
  echo "📦 Installing npm dependencies..."
  npm install
fi

if [ -f "requirements.txt" ]; then
  echo "🐍 Installing Python dependencies..."
  pip install -r requirements.txt
fi

if [ -f "go.mod" ]; then
  echo "🔵 Installing Go dependencies..."
  go mod download
fi

if [ -f "Cargo.toml" ]; then
  echo "🦀 Building Rust project..."
  cargo build
fi

echo "✅ Development environment setup complete!"
echo ""
echo "💡 Quick tips:"
echo "  - Run 'npm test' to run tests"
echo "  - Run 'pre-commit run --all-files' to check code quality"
echo "  - Use 'gh' command for GitHub CLI"
echo "  - Database: postgresql://postgres:postgres@localhost:5432/devdb"
echo "  - Redis: redis://localhost:6379"
echo "  - MailHog UI: http://localhost:8025"
