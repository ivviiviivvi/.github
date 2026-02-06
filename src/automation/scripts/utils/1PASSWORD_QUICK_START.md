# 1Password CLI Quick Reference for GitHub Projects

**Quick deployment using 1Password CLI to securely retrieve your GitHub PAT**

______________________________________________________________________

## 🚀 Fastest Method

```bash
cd /workspace/scripts
./deploy-with-1password.sh
```

That's it! The script handles everything.

______________________________________________________________________

## ⚙️ What It Does

1. ✅ Checks for 1Password CLI (`op`)
1. ✅ Signs you in if needed
1. ✅ Retrieves your GitHub PAT from 1Password
1. ✅ Exports it as `GH_TOKEN`
1. ✅ Runs the Python configuration script
1. ✅ Creates all 7 GitHub Projects
1. ✅ Logs everything to a file

______________________________________________________________________

## 🎯 Usage Options

### Dry Run (Test First)

```bash
./deploy-with-1password.sh --dry-run
```

Shows what would be created without making changes.

### Custom 1Password Reference

If your token is stored differently:

```bash
export OP_REFERENCE="op://YourVault/YourItem/fieldname"
./deploy-with-1password.sh
```

### Custom Organization

```bash
export ORG_NAME="your-org-name"
./deploy-with-1password.sh
```

______________________________________________________________________

## 📍 Finding Your 1Password Reference

### List your vaults

```bash
op vault list
```

### List items in a vault

```bash
op item list --vault Private
```

### View item details

```bash
op item get "GitHub PAT" --vault Private
```

### Test retrieving your token

```bash
op read "op://Private/GitHub PAT/credential"
```

Should output your token (first time will prompt for authentication).

______________________________________________________________________

## 🔧 1Password CLI Setup

### Install (if not already installed)

**macOS:**

```bash
brew install --cask 1password-cli
```

**Linux:**

```bash
# Debian/Ubuntu
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
  sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" | \
  sudo tee /etc/apt/sources.list.d/1password.list
sudo apt update && sudo apt install 1password-cli
```

**Windows:** Download from https://1password.com/downloads/command-line/

### Sign In

```bash
eval $(op signin)
```

Or with account shorthand:

```bash
eval $(op signin my)
```

### Check Version

```bash
op --version
```

### Check Authentication

```bash
op account get
```

______________________________________________________________________

## 🎓 Manual Method (Without Script)

If you prefer to run commands manually:

```bash
# 1. Sign in to 1Password
eval $(op signin)

# 2. Retrieve and export token
export GH_TOKEN=$(op read "op://Private/GitHub PAT/credential")

# 3. Verify token loaded (shows first 4 chars)
echo "Token: ${GH_TOKEN:0:4}..."

# 4. Run Python script
cd /workspace/scripts
python3 configure-github-projects.py --org {{ORG_NAME}}
```

______________________________________________________________________

## 🔍 Common 1Password References

Adjust these based on your setup:

| Vault   | Item Name       | Field      | Reference                            |
| ------- | --------------- | ---------- | ------------------------------------ |
| Private | GitHub PAT      | credential | `op://Private/GitHub PAT/credential` |
| Private | GitHub Token    | password   | `op://Private/GitHub Token/password` |
| Work    | GitHub          | token      | `op://Work/GitHub/token`             |
| Dev     | GitHub Projects | pat        | `op://Dev/GitHub Projects/pat`       |

______________________________________________________________________

## ❓ Troubleshooting

### "op: command not found"

Install 1Password CLI (see setup section above).

### "You are not currently signed in"

```bash
eval $(op signin)
```

### "not found in any vault"

Your 1Password reference is incorrect. Find it with:

```bash
op vault list
op item list --vault YourVaultName
op item get "Your Item Name" --vault YourVaultName
```

### "couldn't get details for item"

Check the exact item name and field:

```bash
op item get "GitHub PAT" --vault Private --format json
```

### Token not working

Verify the token has correct scopes:

- `project` (all scopes)
- `repo` (all scopes)
- `admin:org` (read)

Regenerate in GitHub Settings > Developer settings > Personal access tokens

______________________________________________________________________

## 📚 Additional Resources

- **1Password CLI Docs:** https://developer.1password.com/docs/cli/
- **GitHub Projects Deployment:**
  [GITHUB_PROJECTS_DEPLOYMENT.md](../../../../docs/guides/GITHUB_PROJECTS_DEPLOYMENT.md)
- **Complete Setup Guide:** [README_PROJECTS.md](README_PROJECTS.md)
- **Quick Reference:**
  [GITHUB_PROJECTS_QUICKREF.md](../../../../docs/guides/GITHUB_PROJECTS_QUICKREF.md)

______________________________________________________________________

## ✅ Quick Checklist

- [ ] 1Password CLI installed (`op --version`)
- [ ] Signed in to 1Password (`op account get`)
- [ ] GitHub PAT stored in 1Password
- [ ] Know your 1Password reference path
- [ ] Python 3.8+ installed
- [ ] `requests` library installed (`pip install requests`)

**Ready?**

```bash
cd /workspace/scripts && ./deploy-with-1password.sh
```

______________________________________________________________________

_Last Updated: January 18, 2026_
