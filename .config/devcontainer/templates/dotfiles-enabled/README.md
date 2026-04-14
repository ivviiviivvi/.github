# Dotfiles-Enabled DevContainer Template

A development container pre-configured with personal dotfiles for consistent
development environments across all organization repositories.

## Features

- **Chezmoi Integration**: Automatically applies dotfiles from
  [4444J99/dotfiles](https://github.com/4444J99/dotfiles)
- **Modern CLI Tools**: starship, eza, bat, fzf, zoxide, atuin, ripgrep
- **Neovim + LazyVim**: Pre-configured editor with LSP support
- **1Password CLI**: For secure secrets management
- **Multi-language Support**: Node.js 20, Python 3.11, Go 1.21

## Usage

### Option 1: Copy Template

Copy this template to your repository's `.devcontainer/` directory:

```bash
cp -r .devcontainer/templates/dotfiles-enabled/* your-repo/.devcontainer/
```

### Option 2: Reference in devcontainer.json

Reference the setup script from your own devcontainer:

```json
{
  "postCreateCommand": "curl -sL https://raw.githubusercontent.com/{{ORG_NAME}}/.github/main/.devcontainer/templates/dotfiles-enabled/setup.sh | bash"
}
```

### Option 3: Use with GitHub Codespaces

Add to your repository settings → Codespaces → Default devcontainer
configuration.

## Customization

### Use Different Dotfiles Repo

Set the `DOTFILES_REPO` environment variable:

```json
{
  "containerEnv": {
    "DOTFILES_REPO": "your-username/your-dotfiles"
  }
}
```

### Skip Dotfiles

To use the template without dotfiles:

```json
{
  "containerEnv": {
    "SKIP_DOTFILES": "true"
  }
}
```

## Included Tools

| Tool       | Purpose                  |
| ---------- | ------------------------ |
| `chezmoi`  | Dotfile management       |
| `starship` | Cross-shell prompt       |
| `eza`      | Modern `ls` replacement  |
| `bat`      | Syntax-highlighted `cat` |
| `fzf`      | Fuzzy finder             |
| `zoxide`   | Smart directory jumping  |
| `atuin`    | Shell history search     |
| `nvim`     | Neovim with LazyVim      |
| `op`       | 1Password CLI            |

## Shell Aliases (from dotfiles)

```bash
ls  → eza --icons
ll  → eza -la --icons --git
cat → bat --paging=never
z   → zoxide (smart cd)
gs  → git status -sb
gl  → git log --oneline --graph
```

## Key Bindings

| Key      | Action                       |
| -------- | ---------------------------- |
| `Ctrl+R` | Fuzzy search history (atuin) |
| `Ctrl+T` | Fuzzy find files (fzf)       |
| `Alt+C`  | Fuzzy cd directory (fzf)     |

## Requirements

- GitHub Codespaces or VS Code with Dev Containers extension
- (Optional) 1Password account for secrets via `op signin`
