#!/bin/bash
# Week 6 Quick Setup Script
# Automates initial preparation for repository expansion

set -e

echo "🚀 Week 6 Repository Expansion - Quick Setup"
echo "=============================================="
echo ""

# Check prerequisites
echo "✅ Checking prerequisites..."

if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) not found. Install from https://cli.github.com"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "⚠️  Warning: jq not found (optional, for JSON processing)"
fi

echo "✅ All prerequisites found"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x automation/scripts/evaluate_repository.py
chmod +x automation/scripts/generate_pilot_workflows.py
echo "✅ Scripts are now executable"
echo ""

# Check if user provided a repository
if [ -z "$1" ]; then
    echo "📋 Usage Options:"
    echo ""
    echo "  1. Evaluate a specific repository:"
    echo "     ./setup_week6.sh <owner/repo>"
    echo ""
    echo "  2. Evaluate all organization repositories:"
    echo "     ./setup_week6.sh --all <org>"
    echo ""
    echo "  3. Run setup only (no evaluation):"
    echo "     ./setup_week6.sh --setup-only"
    echo ""
    exit 0
fi

# Handle different modes
if [ "$1" == "--setup-only" ]; then
    echo "✅ Setup complete!"
    echo ""
    echo "📝 Next steps:"
    echo "  1. Evaluate repositories:"
    echo "     python3 automation/scripts/evaluate_repository.py <owner/repo>"
    echo "  2. Create configuration from template:"
    echo "     cp automation/config/pilot-repo-config-template.yml \\"
    echo "        automation/config/pilot-<repo-name>-config.yml"
    echo "  3. Generate workflows:"
    echo "     python3 automation/scripts/generate_pilot_workflows.py \\"
    echo "        automation/config/pilot-<repo-name>-config.yml"
    echo ""
    exit 0
fi

# Evaluate repository
if [ "$1" == "--all" ]; then
    if [ -z "$2" ]; then
        echo "❌ Error: --all requires organization name"
        exit 1
    fi

    echo "🔍 Evaluating all repositories in organization: $2"
    python3 automation/scripts/evaluate_repository.py --all "$2"

    echo ""
    echo "✅ Evaluation complete!"
    echo "📊 Results saved to: ${2}_repository_evaluation.json"
    echo ""
    echo "📝 Next steps:"
    echo "  1. Review results in ${2}_repository_evaluation.json"
    echo "  2. Select pilot repository (score ≥ 60)"
    echo "  3. Create configuration:"
    echo "     cp automation/config/pilot-repo-config-template.yml \\"
    echo "        automation/config/pilot-<repo-name>-config.yml"
    echo "  4. Run this script again with selected repository"
    echo ""
else
    echo "🔍 Evaluating repository: $1"
    python3 automation/scripts/evaluate_repository.py "$1"

    REPO_NAME=$(echo "$1" | sed 's/\//_/g')

    echo ""
    echo "✅ Evaluation complete!"
    echo "📊 Results saved to: ${REPO_NAME}_evaluation.json"
    echo ""

    # Ask if user wants to continue with configuration
    read -p "📝 Create pilot configuration for this repository? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        CONFIG_FILE="automation/config/pilot-${REPO_NAME}-config.yml"

        if [ -f "$CONFIG_FILE" ]; then
            echo "⚠️  Configuration file already exists: $CONFIG_FILE"
            read -p "Overwrite? (y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "❌ Skipping configuration creation"
                exit 0
            fi
        fi

        echo "📝 Creating configuration file: $CONFIG_FILE"
        cp automation/config/pilot-repo-config-template.yml "$CONFIG_FILE"

        # Extract repository info
        OWNER=$(echo "$1" | cut -d'/' -f1)
        REPO=$(echo "$1" | cut -d'/' -f2)

        # Basic customization (replace placeholders)
        if command -v sed &> /dev/null; then
            sed -i.bak "s/your-org/$OWNER/g" "$CONFIG_FILE"
            sed -i.bak "s/pilot-repo-name/$REPO/g" "$CONFIG_FILE"
            sed -i.bak "s/2026-02-22/$(date +%Y-%m-%d)/g" "$CONFIG_FILE"
            rm -f "${CONFIG_FILE}.bak"

            echo "✅ Configuration file created with basic customization"
        else
            echo "✅ Configuration file created (manual customization needed)"
        fi

        echo ""
        echo "📝 Next steps:"
        echo "  1. Edit configuration file:"
        echo "     code $CONFIG_FILE"
        echo "  2. Customize:"
        echo "     - Label mappings"
        echo "     - CODEOWNERS settings"
        echo "     - Stale detection parameters"
        echo "     - Stakeholder information"
        echo "  3. Generate workflows:"
        echo "     python3 automation/scripts/generate_pilot_workflows.py $CONFIG_FILE"
        echo ""
    else
        echo "⏭️  Skipping configuration creation"
        echo ""
        echo "📝 To create later, run:"
        echo "   cp automation/config/pilot-repo-config-template.yml \\"
        echo "      automation/config/pilot-${REPO_NAME}-config.yml"
        echo ""
    fi
fi

echo "🎉 Week 6 setup complete!"
