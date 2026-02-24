#!/bin/bash

# Setup script for configuring git commit tracking
# This script sets up the commit message template for the local repository

set -e

echo "Setting up commit tracking configuration..."

# Set commit message template
if [ -f ".github/.gitmessage" ]; then
    git config commit.template .github/.gitmessage
    echo "✓ Commit message template configured"
else
    echo "✗ Error: .github/.gitmessage not found"
    exit 1
fi

# Optional: Set up commit message length limits
read -p "Do you want to set commit message length limits? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git config core.commentChar ";"
    echo "✓ Comment character set to ';'"
fi

# Display current configuration
echo ""
echo "Current Git Configuration:"
echo "=========================="
git config --get commit.template && echo "Commit template: $(git config --get commit.template)" || echo "Commit template: Not set"

echo ""
echo "Setup complete! You can now use 'git commit' to see the template."
echo "For more information, see CONTRIBUTING.md"
