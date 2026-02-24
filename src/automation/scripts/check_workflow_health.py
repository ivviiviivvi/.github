#!/usr/bin/env python3
"""Check workflow health and configuration."""

import os
import re
from pathlib import Path

import yaml


def check_configs():
    """Check for missing configuration files."""
    required_configs = [
        ".github/auto-merge.yml",
        ".github/routing.yml",
        ".github/self-healing.yml",
        ".github/maintenance.yml",
        ".github/analytics.yml",
        ".github/sla.yml",
        ".github/incident.yml",
    ]

    print("Checking configuration files...")
    missing = []
    for config in required_configs:
        if not os.path.exists(config):
            missing.append(config)
            print(f"❌ Missing: {config}")
        else:
            print(f"✅ Found: {config}")
    return missing


def check_workflows():
    """Check workflow files for common errors."""
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ Workflow directory not found!")
        return

    print("\nChecking workflow files...")
    # Simplified regex patterns to avoid escaping hell
    deprecated_patterns = [
        (r"::set-output", "Deprecated set-output command"),
        (r"::save-state", "Deprecated save-state command"),
        (r"runs-on:\s*ubuntu-18.04", "Deprecated runner ubuntu-18.04"),
        (r"node-version: 12", "Deprecated Node.js 12"),
        (r"node-version: '12'", "Deprecated Node.js 12"),
        (r"node-version: \"12\"", "Deprecated Node.js 12"),
        (r"node-version: 16", "Deprecated Node.js 16"),
        (r"node-version: '16'", "Deprecated Node.js 16"),
        (r"node-version: \"16\"", "Deprecated Node.js 16"),
        (r"actions/checkout@v2", "Old checkout action (v2)"),
        (r"actions/setup-python@v2", "Old setup-python action (v2)"),
        (r"actions/setup-node@v2", "Old setup-node action (v2)"),
    ]

    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file) as f:
                content = f.read()

            # YAML syntax check
            try:
                yaml.safe_load(content)
            except yaml.YAMLError as e:
                print(f"❌ {workflow_file.name}: YAML Syntax Error - {e}")
                continue

            issues = []
            for pattern, desc in deprecated_patterns:
                if re.search(pattern, content):
                    issues.append(desc)

            if issues:
                print(f"⚠️  {workflow_file.name}: {', '.join(issues)}")

        except Exception as e:
            print(f"❌ {workflow_file.name}: Error reading file - {e}")


if __name__ == "__main__":
    check_configs()
    check_workflows()
