#!/usr/bin/env python3
"""Generate .meta.json files for GitHub Actions workflows.

This script analyzes all GitHub Actions workflows in .github/workflows/
and generates corresponding .meta.json metadata files following the
schema-org inspired format.
"""

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

# Layer classification rules based on workflow patterns
LAYER_RULES = {
    "core": [
        r"^ci",
        r"codeql",
        r"security",
        r"reusable",
        r"health-check",
        r"test-coverage",
        r"code-coverage",
        r"lint",
        r"^build",
    ],
    "interface": [
        r"auto-assign",
        r"auto-label",
        r"labeler",
        r"welcome",
        r"slack",
        r"pr-title",
        r"badge",
        r"email",
        r"dashboard",
        r"triage",
    ],
    "logic": [
        r"validate",
        r"quality",
        r"check",
        r"commit-tracking",
        r"link-checker",
        r"schema",
        r"pr-quality",
        r"safeguard",
    ],
    "application": [
        r"deploy",
        r"release",
        r"version",
        r"pages",
        r"docker",
        r"orchestrat",
        r"walkthrough",
        r"sbom",
    ],
}

# Role classification based on workflow name patterns
ROLE_PATTERNS = {
    "ci": [r"^ci", r"continuous-integration", r"build"],
    "security": [r"security", r"codeql", r"scan", r"vulnerability", r"secret"],
    "automation": [r"auto-", r"bot", r"scheduled", r"cron", r"orchestr"],
    "quality": [r"lint", r"quality", r"validate", r"check"],
    "deployment": [r"deploy", r"release", r"publish"],
    "testing": [r"test", r"coverage", r"mutation"],
    "documentation": [r"docs", r"pages", r"walkthrough", r"readme"],
    "ai": [r"claude", r"gemini", r"openai", r"grok", r"perplexity", r"jules"],
    "pr-management": [r"pr-", r"pull-request", r"merge", r"review"],
    "issue-management": [r"issue", r"triage", r"task"],
    "metrics": [r"metrics", r"monitoring", r"health", r"report"],
    "maintenance": [r"cleanup", r"nightly", r"maintenance", r"reset"],
}


def classify_layer(workflow_name: str, filename: str) -> str:
    """Determine the layer for a workflow based on its name and filename."""
    combined = f"{workflow_name.lower()} {filename.lower()}"

    # Check reusable workflows first
    if "reusable/" in filename:
        return "core"

    for layer, patterns in LAYER_RULES.items():
        for pattern in patterns:
            if re.search(pattern, combined):
                return layer

    # Default to logic layer
    return "logic"


def classify_role(workflow_name: str, filename: str) -> str:
    """Determine the role for a workflow based on its name."""
    combined = f"{workflow_name.lower()} {filename.lower()}"

    for role, patterns in ROLE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, combined):
                return role

    return "general"


def extract_triggers(workflow: dict) -> list[str]:
    """Extract trigger types from workflow definition."""
    # PyYAML parses unquoted 'on' as boolean True
    # So we need to check both 'on' and True as keys
    on_section = workflow.get("on") or workflow.get(True, {})

    if isinstance(on_section, str):
        return [on_section]
    elif isinstance(on_section, list):
        return on_section
    elif isinstance(on_section, dict):
        # Filter out sub-keys that are not actual triggers
        # workflow_call has inputs/outputs/secrets as sub-keys
        valid_triggers = [
            "push",
            "pull_request",
            "pull_request_target",
            "pull_request_review",
            "pull_request_review_comment",
            "issue_comment",
            "issues",
            "schedule",
            "workflow_dispatch",
            "workflow_call",
            "workflow_run",
            "release",
            "create",
            "delete",
            "fork",
            "gollum",
            "page_build",
            "project",
            "project_card",
            "project_column",
            "public",
            "registry_package",
            "repository_dispatch",
            "status",
            "watch",
            "check_run",
            "check_suite",
            "deployment",
            "deployment_status",
            "discussion",
            "discussion_comment",
            "label",
            "merge_group",
            "milestone",
        ]
        return [k for k in on_section.keys() if k in valid_triggers]

    return []


def generate_description(workflow: dict, name: str, role: str) -> str:
    """Generate a description based on workflow content."""
    # Try to extract from comments or generate based on structure
    triggers = extract_triggers(workflow)
    jobs = list(workflow.get("jobs", {}).keys())

    trigger_desc = ", ".join(triggers) if triggers else "manual"
    job_count = len(jobs)

    role_descriptions = {
        "ci": "Continuous integration workflow for building and testing",
        "security": "Security scanning and vulnerability detection",
        "automation": "Automated workflow for operational tasks",
        "quality": "Code quality validation and linting",
        "deployment": "Deployment and release management",
        "testing": "Test execution and coverage analysis",
        "documentation": "Documentation generation and publishing",
        "ai": "AI-assisted code review and analysis",
        "pr-management": "Pull request automation and management",
        "issue-management": "Issue triage and task management",
        "metrics": "Metrics collection and health monitoring",
        "maintenance": "Repository maintenance and cleanup",
        "general": "General-purpose workflow",
    }

    base_desc = role_descriptions.get(role, role_descriptions["general"])
    return f"{base_desc}. Triggered by {trigger_desc}, executes {job_count} job(s)."


def generate_subjects(name: str, layer: str, role: str, triggers: list[str]) -> list[str]:
    """Generate dc:subject keywords for the workflow."""
    subjects = set()

    # Add layer
    subjects.add(layer)

    # Add role
    subjects.add(role.replace("-", " "))

    # Add common keywords from name
    name_lower = name.lower()
    keywords = [
        ("ci", "continuous-integration"),
        ("pr", "pull-request"),
        ("security", "security"),
        ("test", "testing"),
        ("lint", "linting"),
        ("deploy", "deployment"),
        ("release", "release"),
        ("auto", "automation"),
        ("review", "review"),
        ("quality", "quality"),
        ("coverage", "coverage"),
        ("docker", "docker"),
        ("pages", "pages"),
        ("schedule", "scheduled"),
    ]

    for keyword, subject in keywords:
        if keyword in name_lower:
            subjects.add(subject)

    # Add trigger-based keywords
    for trigger in triggers:
        if trigger == "schedule":
            subjects.add("scheduled")
        elif trigger == "workflow_dispatch":
            subjects.add("manual")
        elif trigger == "push":
            subjects.add("push-triggered")
        elif trigger == "pull_request":
            subjects.add("pr-triggered")

    return sorted(list(subjects))


def generate_canonical_name(filename: str, layer: str, role: str) -> str:
    """Generate canonical name in format layer.role.domain.yml."""
    # Extract domain from filename
    base_name = Path(filename).stem
    domain_parts = base_name.replace("-", ".").split(".")

    # Take first meaningful part as domain
    domain = domain_parts[0] if domain_parts else "workflow"

    return f"{layer}.{role}.{domain}.yml"


def generate_metadata(file_path: Path) -> Optional[dict[str, Any]]:
    """Generate metadata for a single workflow file."""
    try:
        with open(file_path) as f:
            workflow = yaml.safe_load(f)

        if not workflow:
            return None

        filename = file_path.name
        name = workflow.get("name", filename.replace(".yml", "").replace("-", " ").title())

        triggers = extract_triggers(workflow)
        layer = classify_layer(name, str(file_path))
        role = classify_role(name, str(file_path))
        description = generate_description(workflow, name, role)
        subjects = generate_subjects(name, layer, role, triggers)
        canonical = generate_canonical_name(filename, layer, role)

        # Generate deterministic UUID based on filename
        namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # URL namespace
        identifier = uuid.uuid5(namespace, f"workflow:{filename}")

        today = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

        metadata = {
            "profile": "full",
            "name": name,
            "identifier": f"urn:uuid:{identifier}",
            "version": "1.0.0",
            "description": description,
            "functioncalled": {
                "canonical": canonical,
                "layer": layer,
                "role": role,
                "domain": Path(filename).stem.split("-")[0],
            },
            "schema:type": "SoftwareSourceCode",
            "encodingFormat": "application/x-yaml",
            "programmingLanguage": "YAML",
            "runtimePlatform": "GitHub Actions",
            "triggers": triggers,
            "dateCreated": "2024-01-01T00:00:00Z",
            "dateModified": today,
            "dc:subject": subjects,
        }

        return metadata

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def main():
    """Main entry point."""
    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print("Error: .github/workflows directory not found")
        print("Run this script from the repository root")
        return

    # Count stats
    created = 0
    skipped = 0
    errors = 0

    # Process all workflow files
    for file_path in sorted(workflows_dir.glob("*.yml")):
        # Skip reusable subdirectory for now
        if "reusable/" in str(file_path):
            continue

        meta_path = file_path.with_suffix(".yml.meta.json")

        # Check if meta file already exists
        if meta_path.exists():
            print(f"⏭️  Skipping {file_path.name} (meta exists)")
            skipped += 1
            continue

        metadata = generate_metadata(file_path)

        if metadata:
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)
                f.write("\n")  # Trailing newline
            print(f"✅ Created {meta_path.name}")
            created += 1
        else:
            print(f"❌ Error processing {file_path.name}")
            errors += 1

    # Process reusable workflows
    reusable_dir = workflows_dir / "reusable"
    if reusable_dir.exists():
        for file_path in sorted(reusable_dir.glob("*.yml")):
            meta_path = file_path.with_suffix(".yml.meta.json")

            if meta_path.exists():
                print(f"⏭️  Skipping reusable/{file_path.name} (meta exists)")
                skipped += 1
                continue

            metadata = generate_metadata(file_path)

            if metadata:
                with open(meta_path, "w") as f:
                    json.dump(metadata, f, indent=2)
                    f.write("\n")
                print(f"✅ Created reusable/{meta_path.name}")
                created += 1
            else:
                print(f"❌ Error processing reusable/{file_path.name}")
                errors += 1

    print("\n" + "=" * 60)
    print(f"📊 Summary: Created {created}, Skipped {skipped}, Errors {errors}")
    print("=" * 60)


if __name__ == "__main__":
    main()
