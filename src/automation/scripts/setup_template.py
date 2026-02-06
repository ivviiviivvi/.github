#!/usr/bin/env python3
"""Setup script for parameterizing the org .github template.

Reads static identity variables from .config/template-config.yml,
computes dynamic counts from the filesystem, and replaces all
{{VAR}} placeholders across the repository.

Usage:
    python src/automation/scripts/setup_template.py              # Full setup
    python src/automation/scripts/setup_template.py --dry-run    # Preview changes
    python src/automation/scripts/setup_template.py --counts-only # Refresh counts only
    python src/automation/scripts/setup_template.py --validate   # Check for remaining placeholders
"""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

# Repository root (assumes script is at src/automation/scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_PATH = REPO_ROOT / ".config" / "template-config.yml"

# Directories/files to skip during replacement
EXCLUDED_DIRS = {
    "node_modules",
    ".mypy_cache",
    "__pycache__",
    "htmlcov",
    ".git",
    ".ruff_cache",
    ".venv",
    "venv",
    ".tox",
    ".pytest_cache",
}

# Files to skip (relative to repo root)
EXCLUDED_FILES = {
    ".config/template-config.yml",
    "src/automation/scripts/setup_template.py",
}

# File extensions to process
PROCESSABLE_EXTENSIONS = {
    ".md",
    ".yml",
    ".yaml",
    ".py",
    ".json",
    ".sh",
    ".toml",
    ".txt",
    ".cfg",
    ".ini",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".java",
}

# Extensionless files to process (by name)
PROCESSABLE_FILENAMES = {
    "CODEOWNERS",
    ".lycheeignore",
    "Dockerfile",
    "Makefile",
    ".gitignore",
    ".dockerignore",
    ".editorconfig",
}

# Sections in pyproject.toml that use {{ }} for Jinja (must not be replaced)
JINJA_PATTERN = re.compile(r"\{\{change_type\}\}|\{\{scope\}\}|\{\{message\}\}|\{\{body\}\}|\{\{footer\}\}")


def load_config(config_path: Path) -> dict:
    """Load and return the template config YAML."""
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)


def compute_dynamic_counts(repo_root: Path) -> dict[str, str]:
    """Scan the filesystem to compute dynamic count variables."""
    counts = {}

    # Workflow counts
    wf_dir = repo_root / ".github" / "workflows"
    wf_files = list(wf_dir.glob("*.yml")) if wf_dir.exists() else []
    reusable_dir = wf_dir / "reusable"
    reusable_files = list(reusable_dir.glob("*.yml")) if reusable_dir.exists() else []
    counts["WORKFLOW_COUNT"] = str(len(wf_files) + len(reusable_files))
    counts["REUSABLE_TEMPLATE_COUNT"] = str(len(reusable_files))

    # AI framework counts
    ai_dir = repo_root / "src" / "ai_framework"
    agents = list((ai_dir / "agents").glob("*.agent.md")) if (ai_dir / "agents").exists() else []
    chatmodes = list((ai_dir / "chatmodes").glob("*.chatmode.md")) if (ai_dir / "chatmodes").exists() else []
    prompts = list((ai_dir / "prompts").glob("*.prompt.md")) if (ai_dir / "prompts").exists() else []
    collections = list((ai_dir / "collections").glob("*.collection.yml")) if (ai_dir / "collections").exists() else []
    counts["AGENT_COUNT"] = str(len(agents))
    counts["CHATMODE_COUNT"] = str(len(chatmodes))
    counts["PROMPT_COUNT"] = str(len(prompts))
    counts["COLLECTION_COUNT"] = str(len(collections))

    # Script count
    scripts_dir = repo_root / "src" / "automation" / "scripts"
    if scripts_dir.exists():
        script_files = [f for f in scripts_dir.glob("*.py") if f.name != "__init__.py"]
        counts["SCRIPT_COUNT"] = str(len(script_files))
    else:
        counts["SCRIPT_COUNT"] = "0"

    return counts


def build_variable_map(config: dict, counts: dict[str, str]) -> dict[str, str]:
    """Build the unified variable map from config + dynamic counts + derived vars."""
    variables = {}

    # Static vars from config
    org = config.get("org", {})
    variables["ORG_NAME"] = org.get("name", "{{ORG_NAME}}")
    variables["ORG_DISPLAY_NAME"] = org.get("display_name", "{{ORG_DISPLAY_NAME}}")
    variables["ORG_WEBSITE"] = org.get("website", "{{ORG_WEBSITE}}")
    variables["ORG_EMAIL_DOMAIN"] = org.get("email_domain", "{{ORG_EMAIL_DOMAIN}}")

    repo = config.get("repo", {})
    variables["REPO_NAME"] = repo.get("name", "{{REPO_NAME}}")
    variables["NPM_SCOPE"] = repo.get("npm_scope", "{{NPM_SCOPE}}")

    social = config.get("social", {})
    variables["DISCORD_INVITE"] = social.get("discord_invite", "{{DISCORD_INVITE}}")

    product = config.get("product", {})
    variables["PRODUCT_NAME"] = product.get("name", "{{PRODUCT_NAME}}")
    variables["API_ENDPOINT"] = product.get("api_endpoint", "{{API_ENDPOINT}}")

    teams = config.get("teams", {})
    variables["TEAM_LEADERSHIP"] = teams.get("leadership", "{{TEAM_LEADERSHIP}}")
    variables["TEAM_ENGINEERING"] = teams.get("engineering", "{{TEAM_ENGINEERING}}")
    variables["TEAM_DEVOPS"] = teams.get("devops", "{{TEAM_DEVOPS}}")
    variables["TEAM_SECURITY"] = teams.get("security", "{{TEAM_SECURITY}}")

    # Derived vars
    org_name = variables["ORG_NAME"]
    variables["ORG_GITHUB_URL"] = f"https://github.com/{org_name}"
    variables["ORG_GITHUB_IO_URL"] = f"https://{org_name}.github.io"

    # Dynamic counts
    variables.update(counts)

    return variables


def should_skip_path(path: Path, repo_root: Path) -> bool:
    """Check whether a file path should be skipped."""
    rel = path.relative_to(repo_root)
    rel_str = str(rel)

    # Skip excluded directories
    for part in rel.parts:
        if part in EXCLUDED_DIRS:
            return True

    # Skip excluded files
    if rel_str in EXCLUDED_FILES:
        return True

    # Skip archive reports JSON (historical snapshots)
    if "docs/archive/reports/" in rel_str and rel_str.endswith(".json"):
        return True

    # Skip non-text extensions (unless filename is in the allowlist)
    if path.suffix not in PROCESSABLE_EXTENSIONS and path.name not in PROCESSABLE_FILENAMES:
        return True

    # Skip binary/lock files
    if path.name in {"package-lock.json"}:
        return True

    return False


def is_jinja_line(line: str) -> bool:
    """Check if a line contains Jinja template syntax (commitizen)."""
    return bool(JINJA_PATTERN.search(line))


def replace_in_content(content: str, variables: dict[str, str], counts_only: bool = False) -> str:
    """Replace {{VAR}} placeholders in content.

    If counts_only is True, only replace count-related variables.
    Preserves Jinja syntax used by commitizen in pyproject.toml.
    """
    count_vars = {
        "WORKFLOW_COUNT",
        "REUSABLE_TEMPLATE_COUNT",
        "AGENT_COUNT",
        "CHATMODE_COUNT",
        "PROMPT_COUNT",
        "COLLECTION_COUNT",
        "SCRIPT_COUNT",
    }

    lines = content.split("\n")
    result_lines = []
    for line in lines:
        if is_jinja_line(line):
            result_lines.append(line)
            continue
        for var_name, var_value in variables.items():
            if counts_only and var_name not in count_vars:
                continue
            placeholder = "{{" + var_name + "}}"
            if placeholder in line:
                line = line.replace(placeholder, var_value)
        result_lines.append(line)
    return "\n".join(result_lines)


def find_processable_files(repo_root: Path) -> list[Path]:
    """Find all files that should be processed for placeholder replacement."""
    files = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for filename in filenames:
            filepath = Path(dirpath) / filename
            if not should_skip_path(filepath, repo_root):
                files.append(filepath)
    return sorted(files)


KNOWN_VARIABLES = {
    "ORG_NAME",
    "ORG_DISPLAY_NAME",
    "ORG_WEBSITE",
    "ORG_EMAIL_DOMAIN",
    "REPO_NAME",
    "NPM_SCOPE",
    "DISCORD_INVITE",
    "PRODUCT_NAME",
    "API_ENDPOINT",
    "TEAM_LEADERSHIP",
    "TEAM_ENGINEERING",
    "TEAM_DEVOPS",
    "TEAM_SECURITY",
    "ORG_GITHUB_URL",
    "ORG_GITHUB_IO_URL",
    "WORKFLOW_COUNT",
    "REUSABLE_TEMPLATE_COUNT",
    "AGENT_COUNT",
    "CHATMODE_COUNT",
    "PROMPT_COUNT",
    "COLLECTION_COUNT",
    "SCRIPT_COUNT",
}


def validate_remaining_placeholders(repo_root: Path) -> list[tuple[str, int, str]]:
    """Find any remaining {{VAR}} placeholders from our known variable set."""
    placeholder_re = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
    results = []
    for filepath in find_processable_files(repo_root):
        try:
            content = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        for i, line in enumerate(content.split("\n"), 1):
            if is_jinja_line(line):
                continue
            for match in placeholder_re.finditer(line):
                var_name = match.group(1)
                if var_name in KNOWN_VARIABLES:
                    rel = str(filepath.relative_to(repo_root))
                    results.append((rel, i, match.group()))
    return results


def run_setup(repo_root: Path, dry_run: bool = False, counts_only: bool = False) -> dict[str, int]:
    """Run the template setup process.

    Returns a dict with stats: files_scanned, files_changed, replacements_made.
    """
    config = load_config(repo_root / ".config" / "template-config.yml")
    counts = compute_dynamic_counts(repo_root)
    variables = build_variable_map(config, counts)

    # Filter out variables that are still set to their own placeholder
    active_vars = {}
    for k, v in variables.items():
        placeholder = "{{" + k + "}}"
        if v != placeholder:
            active_vars[k] = v

    if not active_vars:
        print("No variables configured yet. Edit .config/template-config.yml first.")
        return {"files_scanned": 0, "files_changed": 0, "replacements_made": 0}

    files = find_processable_files(repo_root)
    stats = {"files_scanned": len(files), "files_changed": 0, "replacements_made": 0}

    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        new_content = replace_in_content(content, active_vars, counts_only=counts_only)
        if new_content != content:
            stats["files_changed"] += 1
            # Count individual replacements
            for var_name, _var_value in active_vars.items():
                if counts_only and var_name not in {
                    "WORKFLOW_COUNT",
                    "REUSABLE_TEMPLATE_COUNT",
                    "AGENT_COUNT",
                    "CHATMODE_COUNT",
                    "PROMPT_COUNT",
                    "COLLECTION_COUNT",
                    "SCRIPT_COUNT",
                }:
                    continue
                placeholder = "{{" + var_name + "}}"
                stats["replacements_made"] += content.count(placeholder) - new_content.count(placeholder)

            rel = str(filepath.relative_to(repo_root))
            if dry_run:
                print(f"  Would modify: {rel}")
            else:
                filepath.write_text(new_content, encoding="utf-8")
                print(f"  Modified: {rel}")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Setup template: replace placeholders with configured values.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--counts-only", action="store_true", help="Only refresh dynamic count placeholders")
    parser.add_argument("--validate", action="store_true", help="Check for remaining unreplaced placeholders")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root directory (default: auto-detected)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    if args.validate:
        print(f"Validating placeholders in {repo_root}...")
        remaining = validate_remaining_placeholders(repo_root)
        if remaining:
            print(f"\nFound {len(remaining)} unreplaced placeholder(s):")
            for filepath, line_no, placeholder in remaining:
                print(f"  {filepath}:{line_no}: {placeholder}")
            sys.exit(1)
        else:
            print("All placeholders have been replaced.")
            sys.exit(0)

    mode = "DRY RUN" if args.dry_run else ("COUNTS ONLY" if args.counts_only else "FULL SETUP")
    print(f"Running template setup ({mode}) in {repo_root}...")

    if not args.counts_only:
        config = load_config(repo_root / ".config" / "template-config.yml")
        variables = build_variable_map(config, compute_dynamic_counts(repo_root))
        # Show current variable values
        print("\nVariable map:")
        for k, v in sorted(variables.items()):
            placeholder = "{{" + k + "}}"
            status = "(not configured)" if v == placeholder else v
            print(f"  {k}: {status}")
        print()

    stats = run_setup(repo_root, dry_run=args.dry_run, counts_only=args.counts_only)

    print(
        f"\nDone. Scanned {stats['files_scanned']} files, "
        f"{'would modify' if args.dry_run else 'modified'} {stats['files_changed']} files, "
        f"{stats['replacements_made']} replacements."
    )

    if args.dry_run:
        print("\nThis was a dry run. No files were modified.")
        print("Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
