#!/bin/bash
set -e

echo "🚀 Setting up Full-Stack Development Environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update

# Install Node.js global packages
echo "📦 Installing Node.js global packages..."
npm install -g \
  typescript \
  ts-node \
  nodemon \
  prettier \
  eslint \
  jest \
  pm2 \
  npm-check-updates

# Install Python packages
echo "🐍 Installing Python packages..."
pip install --user \
  black \
  flake8 \
  mypy \
  pytest \
  pytest-cov \
  httpx \
  fastapi \
  uvicorn[standard] \
  sqlalchemy \
  alembic \
  redis \
  celery

# Setup git configuration
echo "⚙️ Configuring git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main
git config --global pull.rebase false

# Install pre-commit if config exists
if [ -f ".pre-commit-config.yaml" ]; then
  echo "🪝 Installing pre-commit hooks..."
  pip install --user pre-commit
  pre-commit install
  pre-commit install --hook-type commit-msg
fi

# Install project dependencies if they exist
if [ -f "package.json" ]; then
  echo "📦 Installing npm dependencies..."
  npm install
fi

if [ -f "requirements.txt" ]; then
  echo "🐍 Installing Python dependencies..."
  pip install -r requirements.txt
fi

if [ -f "pyproject.toml" ]; then
  echo "🐍 Installing Python project..."
  pip install -e .
fi

# Setup database schema if migrations exist
if [ -d "migrations" ] || [ -d "alembic" ]; then
  echo "🗄️ Running database migrations..."
  if [ -d "alembic" ]; then
    alembic upgrade head
  fi
  if [ -f "migrate.sh" ]; then
    ./migrate.sh
  fi
fi

# Create useful aliases
echo "🔧 Creating helpful aliases..."
cat >> ~/.bashrc <<'EOF'

# Development aliases
alias ll='ls -alF'
alias dc='docker-compose'
alias dce='docker-compose exec'
alias dcl='docker-compose logs -f'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias psql-dev='psql postgresql://devuser:devpass@postgres:5432/devdb'
alias redis-cli-dev='redis-cli -h redis -a devpass'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'

# Node aliases
alias nr='npm run'
alias nrd='npm run dev'
alias nrb='npm run build'
alias nrt='npm run test'

# Python aliases
alias py='python3'
alias venv='python3 -m venv'
alias activate='source venv/bin/activate'

EOF

# Create workspace directories
echo "📁 Creating workspace directories..."
mkdir -p logs tmp data

echo "✅ Full-Stack Development Environment setup complete!"
echo ""
echo "💡 Quick tips:"
echo "  Database: postgresql://devuser:devpass@postgres:5432/devdb"
echo "  Redis: redis://redis:6379 (password: devpass)"
echo "  MailHog UI: http://localhost:8025"
echo "  Adminer (DB UI): http://localhost:8080"
echo ""
echo "  Run 'npm run dev' to start development server"
echo "  Run 'psql-dev' to connect to PostgreSQL"
echo "  Run 'redis-cli-dev' to connect to Redis"
echo ""
echo "Happy coding! 🎉"
