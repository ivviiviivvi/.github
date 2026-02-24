#!/bin/bash
# Token Segmentation Migration Script
# Implements recommendations from MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Token Segmentation Migration                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "This script implements token segmentation to replace the single"
echo "master-org-token with purpose-specific tokens for better security."
echo ""

# Check 1Password CLI
if ! command -v op &> /dev/null; then
    echo "✗ 1Password CLI not found"
    echo "  Install: brew install --cask 1password-cli"
    exit 1
fi

# Check if signed in
if ! op account list &> /dev/null; then
    echo "✗ Not signed in to 1Password"
    echo "  Run: eval \$(op signin)"
    exit 1
fi

echo "✓ 1Password CLI ready"
echo ""

# Token definitions based on MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md
declare -A TOKEN_DEFINITIONS=(
    ["org-label-sync-token"]="repo,workflow"
    ["org-project-admin-token"]="project,read:org"
    ["org-repo-analysis-token"]="repo:status,read:org"
    ["org-onboarding-token"]="repo,workflow,admin:org"
)

declare -A TOKEN_PURPOSES=(
    ["org-label-sync-token"]="Label synchronization across organization repositories"
    ["org-project-admin-token"]="GitHub Projects creation and management"
    ["org-repo-analysis-token"]="Read-only repository health checks and metrics"
    ["org-onboarding-token"]="Automated repository onboarding and setup"
)

declare -A TOKEN_EXPIRATION=(
    ["org-label-sync-token"]="90 days"
    ["org-project-admin-token"]="90 days"
    ["org-repo-analysis-token"]="180 days"
    ["org-onboarding-token"]="60 days"
)

echo "═══════════════════════════════════════════════════════════════"
echo "Phase 1: Token Creation Guide"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cat << 'EOF'
You need to create 4 purpose-specific tokens in GitHub:

1. Go to: https://github.com/settings/tokens/new
2. For each token below:
   - Click "Generate new token (classic)"
   - Set the name, expiration, and scopes as shown
   - Generate and copy the token
   - Store in 1Password (we'll help with that)

EOF

for token_name in "${!TOKEN_DEFINITIONS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Token: $token_name"
    echo "Purpose: ${TOKEN_PURPOSES[$token_name]}"
    echo "Scopes: ${TOKEN_DEFINITIONS[$token_name]}"
    echo "Expiration: ${TOKEN_EXPIRATION[$token_name]}"
    echo ""
done

echo "═══════════════════════════════════════════════════════════════"
echo "Phase 2: Store Tokens in 1Password"
echo "═══════════════════════════════════════════════════════════════"
echo ""

read -p "Have you created the tokens? [y/N]: " tokens_created

if [[ "$tokens_created" != "y" && "$tokens_created" != "Y" ]]; then
    echo ""
    echo "Please create the tokens first, then run this script again."
    echo ""
    echo "Quick commands to store tokens after creation:"
    echo ""
    for token_name in "${!TOKEN_DEFINITIONS[@]}"; do
        echo "  op item create \\"
        echo "    --category='Password' \\"
        echo "    --title='$token_name' \\"
        echo "    --vault='Personal' \\"
        echo "    --generate-password='on-create' \\"
        echo "    username='github-token' \\"
        echo "    password='<paste-token-here>'"  # pragma: allowlist secret
        echo ""
    done
    exit 0
fi

echo ""
echo "Let's store the tokens in 1Password..."
echo ""

for token_name in "${!TOKEN_DEFINITIONS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Token: $token_name"
    echo "Purpose: ${TOKEN_PURPOSES[$token_name]}"
    echo ""

    # Check if token already exists
    if op item get "$token_name" --vault Personal &> /dev/null; then
        echo "⚠ Token already exists in 1Password"
        read -p "Update it? [y/N]: " update_token

        if [[ "$update_token" == "y" || "$update_token" == "Y" ]]; then
            echo "Paste the token value (will not be displayed):"
            read -s token_value
            echo ""

            op item edit "$token_name" --vault Personal password="$token_value"
            echo "✓ Token updated"
        else
            echo "- Skipped"
        fi
    else
        echo "Paste the token value (will not be displayed):"
        read -s token_value
        echo ""

        op item create \
            --category="Password" \
            --title="$token_name" \
            --vault="Personal" \
            "password=$token_value" \
            "username=github-token"

        echo "✓ Token stored in 1Password"
    fi
    echo ""
done

echo "═══════════════════════════════════════════════════════════════"
echo "Phase 3: Validate Tokens"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ -f "$SCRIPT_DIR/../automation/scripts/validate_tokens.py" ]; then
    echo "Running token validation..."
    python3 "$SCRIPT_DIR/../automation/scripts/validate_tokens.py"
else
    echo "⚠ Token validation script not found"
    echo "Manually verify tokens with:"
    echo ""
    for token_name in "${!TOKEN_DEFINITIONS[@]}"; do
        echo "  TOKEN=\$(op read \"op://Personal/$token_name/password\")"
        echo "  curl -H \"Authorization: token \$TOKEN\" https://api.github.com/user"
        echo ""
    done
fi

echo "═══════════════════════════════════════════════════════════════"
echo "Phase 4: Update Scripts"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "The following scripts need to be updated to use specific tokens:"
echo ""
echo "  ✓ scripts/complete-project-setup.sh → org-project-admin-token"
echo "  ✓ automation/scripts/sync_labels.py → org-label-sync-token"
echo "  ✓ automation/scripts/web_crawler.py → org-repo-analysis-token"
echo "  ✓ DEPLOY_PHASE*.sh → org-onboarding-token"
echo ""

read -p "Auto-update scripts now? [y/N]: " update_scripts

if [[ "$update_scripts" == "y" || "$update_scripts" == "Y" ]]; then
    echo ""
    echo "Creating migration script..."

    cat > "$SCRIPT_DIR/update-token-references.sh" << 'SCRIPT_EOF'
#!/bin/bash
# Update script token references

set -e

# Backup files
echo "Creating backups..."
for file in \
    scripts/complete-project-setup.sh \
    automation/scripts/sync_labels.py \
    automation/scripts/web_crawler.py \
    DEPLOY_PHASE1.sh \
    DEPLOY_PHASE2.sh \
    DEPLOY_PHASE3.sh
do
    if [ -f "$file" ]; then
        cp "$file" "$file.backup-$(date +%Y%m%d)"
        echo "  ✓ $file"
    fi
done

echo ""
echo "Updating token references..."

# Update complete-project-setup.sh
if [ -f scripts/complete-project-setup.sh ]; then
    sed -i.tmp 's|master-org-token-011726|org-project-admin-token|g' scripts/complete-project-setup.sh
    rm -f scripts/complete-project-setup.sh.tmp
    echo "  ✓ scripts/complete-project-setup.sh"
fi

# Update sync_labels.py
if [ -f automation/scripts/sync_labels.py ]; then
    sed -i.tmp 's|master-org-token-011726|org-label-sync-token|g' automation/scripts/sync_labels.py
    rm -f automation/scripts/sync_labels.py.tmp
    echo "  ✓ automation/scripts/sync_labels.py"
fi

# Update web_crawler.py
if [ -f automation/scripts/web_crawler.py ]; then
    sed -i.tmp 's|master-org-token-011726|org-repo-analysis-token|g' automation/scripts/web_crawler.py
    rm -f automation/scripts/web_crawler.py.tmp
    echo "  ✓ automation/scripts/web_crawler.py"
fi

# Update DEPLOY scripts
for phase in 1 2 3; do
    if [ -f "DEPLOY_PHASE${phase}.sh" ]; then
        sed -i.tmp 's|master-org-token-011726|org-onboarding-token|g' "DEPLOY_PHASE${phase}.sh"
        rm -f "DEPLOY_PHASE${phase}.sh.tmp"
        echo "  ✓ DEPLOY_PHASE${phase}.sh"
    fi
done

echo ""
echo "✓ Token references updated"
echo ""
echo "Backup files created with .backup-$(date +%Y%m%d) extension"
SCRIPT_EOF

    chmod +x "$SCRIPT_DIR/update-token-references.sh"

    read -p "Run the update script now? [y/N]: " run_update

    if [[ "$run_update" == "y" || "$run_update" == "Y" ]]; then
        cd /workspace
        "$SCRIPT_DIR/update-token-references.sh"
        echo ""
        echo "✓ Scripts updated!"
    else
        echo ""
        echo "Update script created at: $SCRIPT_DIR/update-token-references.sh"
        echo "Run it when ready: cd /workspace && $SCRIPT_DIR/update-token-references.sh"
    fi
else
    echo "Skipped. Update manually or run this script again later."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Phase 5: Update TOKEN_REGISTRY.md"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ -f "/workspace/docs/TOKEN_REGISTRY.md" ]; then
    echo "✓ TOKEN_REGISTRY.md exists"
    echo ""
    echo "Next step: Update the registry with creation dates:"
    echo "  - Set 'Created' date to today ($(date +%Y-%m-%d))"
    echo "  - Set 'Expiration' dates based on rotation schedule"
    echo "  - Move master-org-token-011726 to 'Deprecated' section"
else
    echo "⚠ TOKEN_REGISTRY.md not found"
    echo "The registry should be at: /workspace/docs/TOKEN_REGISTRY.md"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Summary"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "✓ Token definitions reviewed"
echo "✓ Storage plan confirmed"
echo ""
echo "Next steps:"
echo "  1. Verify all tokens work correctly"
echo "  2. Test updated scripts"
echo "  3. Update TOKEN_REGISTRY.md"
echo "  4. Schedule master token deprecation (30 days)"
echo "  5. Monitor for any issues"
echo ""
echo "Documentation:"
echo "  - Token Registry: /workspace/docs/TOKEN_REGISTRY.md"
echo "  - Analysis: /workspace/docs/MASTER_ORG_TOKEN_CONTEXTUAL_AWARENESS_ANALYSIS.md"
echo ""
