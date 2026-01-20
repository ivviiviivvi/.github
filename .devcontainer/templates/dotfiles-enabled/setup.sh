#!/bin/bash
set -euo pipefail

echo "🚀 Setting up dotfiles-enabled development environment..."

# ─────────────────────────────────────────────────────────────────────────────
# Install chezmoi and apply dotfiles
# ─────────────────────────────────────────────────────────────────────────────

DOTFILES_REPO="${DOTFILES_REPO:-4444J99/dotfiles}"

echo "📦 Installing chezmoi..."
if ! command -v chezmoi &>/dev/null; then
  sh -c "$(curl -fsLS get.chezmoi.io)" -- -b /usr/local/bin
fi

echo "🏠 Applying dotfiles from ${DOTFILES_REPO}..."
chezmoi init --apply "https://github.com/${DOTFILES_REPO}.git" || {
  echo "⚠️  Dotfiles apply failed (may need 1Password) - continuing with defaults"
}

# ─────────────────────────────────────────────────────────────────────────────
# Install modern CLI tools (matching dotfiles config)
# ─────────────────────────────────────────────────────────────────────────────

echo "🛠️  Installing modern CLI tools..."

# Install using apt where possible
sudo apt-get update
sudo apt-get install -y \
  zsh \
  tmux \
  fzf \
  ripgrep \
  fd-find \
  bat \
  jq \
  curl \
  unzip

# Symlink fd and bat (Ubuntu uses different names)
sudo ln -sf /usr/bin/fdfind /usr/local/bin/fd 2>/dev/null || true
sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null || true

# Install starship prompt
if ! command -v starship &>/dev/null; then
  echo "⭐ Installing starship..."
  curl -sS https://starship.rs/install.sh | sh -s -- -y
fi

# Install eza (modern ls)
if ! command -v eza &>/dev/null; then
  echo "📁 Installing eza..."
  sudo mkdir -p /etc/apt/keyrings
  wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
  echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
  sudo apt-get update
  sudo apt-get install -y eza
fi

# Install zoxide (smart cd)
if ! command -v zoxide &>/dev/null; then
  echo "📂 Installing zoxide..."
  curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash
  sudo mv ~/.local/bin/zoxide /usr/local/bin/ 2>/dev/null || true
fi

# Install atuin (shell history)
if ! command -v atuin &>/dev/null; then
  echo "📜 Installing atuin..."
  curl -sS https://raw.githubusercontent.com/atuinsh/atuin/main/install.sh | bash
  sudo mv ~/.atuin/bin/atuin /usr/local/bin/ 2>/dev/null || true
fi

# Install neovim (latest)
if ! command -v nvim &>/dev/null; then
  echo "📝 Installing neovim..."
  curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux64.tar.gz
  sudo tar -C /opt -xzf nvim-linux64.tar.gz
  sudo ln -sf /opt/nvim-linux64/bin/nvim /usr/local/bin/nvim
  rm nvim-linux64.tar.gz
fi

# ─────────────────────────────────────────────────────────────────────────────
# Install 1Password CLI (for secrets)
# ─────────────────────────────────────────────────────────────────────────────

echo "🔐 Installing 1Password CLI..."
if ! command -v op &>/dev/null; then
  curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
    sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" | \
    sudo tee /etc/apt/sources.list.d/1password.list
  sudo apt-get update
  sudo apt-get install -y 1password-cli
fi

# ─────────────────────────────────────────────────────────────────────────────
# Configure shell
# ─────────────────────────────────────────────────────────────────────────────

echo "🐚 Setting zsh as default shell..."
sudo chsh -s /bin/zsh vscode 2>/dev/null || true

# Source dotfiles if zshrc exists
if [ -f "$HOME/.zshrc" ]; then
  echo "✅ Dotfiles zshrc installed"
else
  echo "⚠️  No .zshrc found - using system defaults"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Git configuration
# ─────────────────────────────────────────────────────────────────────────────

echo "⚙️  Configuring git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# ─────────────────────────────────────────────────────────────────────────────
# Install project dependencies
# ─────────────────────────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "✅ Dotfiles-enabled environment ready!"
echo ""
echo "💡 Available tools:"
echo "  - starship  : Custom prompt with git info"
echo "  - eza       : Modern ls (aliased as ls)"
echo "  - bat       : Syntax-highlighted cat"
echo "  - fzf       : Fuzzy finder (Ctrl+R, Ctrl+T)"
echo "  - zoxide    : Smart cd (z <dir>)"
echo "  - atuin     : Shell history search"
echo "  - nvim      : Neovim with LazyVim"
echo "  - chezmoi   : Dotfile management"
echo ""
echo "🔑 For 1Password secrets: op signin"
