#!/bin/bash
set -e

echo "🚀 Setting up Data Science Environment..."

# Update system
echo "📦 Updating system packages..."
apt-get update

# Install Python data science packages
echo "🐍 Installing Python data science packages..."
pip install --user \
  numpy \
  pandas \
  scipy \
  scikit-learn \
  matplotlib \
  seaborn \
  plotly \
  jupyter \
  jupyterlab \
  ipywidgets \
  tensorflow \
  torch \
  keras \
  xgboost \
  lightgbm \
  catboost \
  statsmodels \
  mlflow \
  dvc \
  great-expectations \
  sqlalchemy \
  psycopg2-binary \
  redis \
  boto3 \
  s3fs \
  pyarrow \
  fastparquet \
  openpyxl \
  python-dotenv

# Install development tools
echo "🔧 Installing development tools..."
pip install --user \
  black \
  ruff \
  mypy \
  pytest \
  pytest-cov \
  ipdb \
  memory-profiler \
  line-profiler

# Setup git configuration
echo "⚙️ Configuring git..."
git config --global core.editor "code --wait"
git config --global init.defaultBranch main
git config --global pull.rebase false

# Create useful directory structure
echo "📁 Creating directory structure..."
mkdir -p \
  notebooks \
  data/raw \
  data/processed \
  data/interim \
  data/external \
  models \
  reports \
  src

# Create .gitignore for data files
cat > data/.gitignore <<'EOF'
# Ignore all data files
*
# Except this file
!.gitignore
# And README
!README.md
EOF

# Create data README
cat > data/README.md <<'EOF'
# Data Directory

## Structure

- `raw/` - Original, immutable data
- `processed/` - Cleaned and transformed data
- `interim/` - Intermediate data transformations
- `external/` - Data from third-party sources

## Guidelines

1. Never modify raw data
2. Document all transformations
3. Keep data out of version control (see .gitignore)
4. Use DVC for data versioning (optional)
EOF

# Create sample notebook
cat > notebooks/00-setup.ipynb <<'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Setup & Configuration\n",
    "\n",
    "Verify environment setup and test connections."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "print(f\"Python: {sys.version}\")\n",
    "print(f\"NumPy: {np.__version__}\")\n",
    "print(f\"Pandas: {pd.__version__}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test database connection\n",
    "import os\n",
    "from sqlalchemy import create_engine\n",
    "\n",
    "db_url = os.getenv('DATABASE_URL')\n",
    "engine = create_engine(db_url)\n",
    "\n",
    "with engine.connect() as conn:\n",
    "    result = conn.execute(\"SELECT 1\")\n",
    "    print(\"Database connection: OK\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Environment Ready!\n",
    "\n",
    "You can now start your data science work."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

# Create useful aliases
echo "🔧 Creating helpful aliases..."
cat >> ~/.bashrc <<'EOF'

# Data science aliases
alias jlab='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser'
alias nb='jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser'
alias py='python3'
alias ipy='ipython'

# Database aliases
alias psql-dev='psql postgresql://devuser:devpass@postgres:5432/devdb'

# MLflow
alias mlflow-ui='mlflow ui --host 0.0.0.0 --port 8080'

EOF

echo "✅ Data Science Environment setup complete!"
echo ""
echo "💡 Quick tips:"
echo "  Jupyter Lab: http://localhost:8888"
echo "  MLflow UI: http://localhost:8080"
echo "  Database: postgresql://devuser:devpass@postgres:5432/devdb"
echo "  Adminer (DB UI): http://localhost:8081"
echo ""
echo "  Run 'jlab' to start Jupyter Lab"
echo "  Notebooks are in: notebooks/"
echo "  Data directory: data/"
echo "  Models directory: models/"
echo ""
echo "Happy analyzing! 📊"
