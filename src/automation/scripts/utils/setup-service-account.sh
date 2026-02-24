#!/bin/bash
# 1Password Service Account Setup
# Eliminates the need for manual 'op signin' during Phase 3

set -euo pipefail

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          🔐 1Password Service Account Setup - No More Signin! 🔐            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

This will set up automated 1Password authentication for Phase 3 monitoring.

EOF

echo "📋 Prerequisites:"
echo "   1. 1Password account with service account feature"
echo "   2. Ability to create service accounts (admin/owner role)"
echo ""

read -p "Do you have admin access to create service accounts? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "⚠️  You need admin access. Contact your 1Password admin or:"
    echo "   - Use your personal account: https://my.1password.com"
    echo ""
    exit 1
fi

echo ""
echo "🚀 Step 1: Create Service Account"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "1. Open: https://my.1password.com/developer-tools/service-accounts"
echo "2. Click 'Create Service Account'"
echo "3. Name: '{{ORG_NAME}}-automation-phase3'"
echo "4. Grant access to 'Personal' vault (or your tokens vault)"
echo "5. Set permissions: Read-only (we only need to read tokens)"
echo "6. Click 'Create Service Account'"
echo "7. Copy the service account token (starts with 'ops_')"
echo ""

read -p "Press Enter when you have copied the service account token..."
echo ""

echo "🔑 Step 2: Save Service Account Token"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Paste your service account token (it will be hidden):"
read -s OP_TOKEN
echo ""

if [[ ! $OP_TOKEN =~ ^ops_ ]]; then
    echo ""
    echo "❌ Token should start with 'ops_'. Please try again."
    echo ""
    exit 1
fi

# Test the token
echo ""
echo "🧪 Step 3: Testing Service Account"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

export OP_SERVICE_ACCOUNT_TOKEN="$OP_TOKEN"

if op account list &>/dev/null; then
    echo "✅ Service account authenticated successfully!"
    echo ""
else
    echo "❌ Service account authentication failed."
    echo "   Please check:"
    echo "   - Token copied correctly"
    echo "   - Service account has vault access"
    echo "   - Token not revoked/expired"
    echo ""
    exit 1
fi

# Save to shell profile
echo ""
echo "💾 Step 4: Save to Shell Profile"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Add this to your shell profile to make it permanent:"
echo ""
echo "# 1Password Service Account (Phase 3 Monitoring)"
echo "export OP_SERVICE_ACCOUNT_TOKEN='$OP_TOKEN'"
echo ""

# Detect shell
SHELL_PROFILE=""
if [[ -n "${BASH_VERSION:-}" ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
elif [[ -n "${ZSH_VERSION:-}" ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    echo "Detected shell profile: $SHELL_PROFILE"
    echo ""
    read -p "Add to $SHELL_PROFILE automatically? (y/n) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "" >> "$SHELL_PROFILE"
        echo "# 1Password Service Account (Phase 3 Monitoring)" >> "$SHELL_PROFILE"
        echo "export OP_SERVICE_ACCOUNT_TOKEN='$OP_TOKEN'" >> "$SHELL_PROFILE"
        echo "" >> "$SHELL_PROFILE"

        echo "✅ Added to $SHELL_PROFILE"
        echo ""
        echo "⚠️  Reload your shell or run:"
        echo "   source $SHELL_PROFILE"
        echo ""
    fi
fi

# Export for current session
export OP_SERVICE_ACCOUNT_TOKEN="$OP_TOKEN"

echo ""
echo "✅ Step 5: Verify Token Access"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "Testing access to tokens..."
echo ""

# Test each token
for token_name in org-label-sync-token org-project-admin-token org-onboarding-token org-repo-analysis-token; do
    if op read "op://Personal/$token_name/password" --reveal &>/dev/null; then
        echo "  ✅ $token_name: Accessible"
    else
        echo "  ❌ $token_name: NOT accessible (check vault permissions)"
    fi
done

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║                      ✅ SERVICE ACCOUNT READY! ✅                        ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 You can now run Phase 3 scripts without 'op signin'!"
echo ""
echo "Try it:"
echo "  PYTHONPATH=/workspace/automation/scripts python3 scripts/validate-tokens.py"
echo ""
echo "For current terminal session, run:"
echo "  export OP_SERVICE_ACCOUNT_TOKEN='$OP_TOKEN'"
echo ""
echo "For all future sessions, reload your shell:"
echo "  source $SHELL_PROFILE"
echo ""
