#!/usr/bin/env python3
"""Generate a unified manifest for the organization .github repository.

This tool aggregates information from multiple sources:
- Workflow registry (workflow-registry.json)
- AI agents (*.agent.md)
- Chatmodes (*.chatmode.md)
- Prompts (*.prompt.md)
- Collections (*.collection.yml)

Output: docs/registry/manifest.json

Usage:
    python generate_manifest.py
    python generate_manifest.py --output custom/path/manifest.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_frontmatter(content: str) -> dict[str, Any]:
    """Parse YAML frontmatter from markdown content."""
    lines = content.splitlines()
    data: dict[str, Any] = {}

    if not lines or lines[0].strip() != "---":
        return data

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return data

    i = 1
    while i < end_idx:
        line = lines[i].rstrip()
        if not line or line.lstrip().startswith("#"):
            i += 1
            continue

        # Handle list values (key:\n  - item1\n  - item2)
        if re.match(r"^[a-z0-9_-]+:\s*$", line):
            key = line.split(":", 1)[0].strip()
            values: list[str] = []
            j = i + 1
            while j < end_idx and lines[j].startswith("  - "):
                values.append(lines[j].replace("  - ", "", 1).strip())
                j += 1
            data[key] = values
            i = j
            continue

        # Handle simple key: value pairs
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            # Remove quotes if present
            if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                value = value[1:-1]
            data[key.strip()] = value

        i += 1

    return data


def count_files(directory: Path, pattern: str) -> int:
    """Count files matching a pattern."""
    return len(list(directory.glob(pattern)))


def scan_agents(agents_dir: Path) -> dict[str, Any]:
    """Scan agents directory for statistics."""
    if not agents_dir.exists():
        return {"total": 0, "files": []}

    files = []
    for path in sorted(agents_dir.glob("*.agent.md")):
        content = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        files.append(
            {
                "file": path.name,
                "name": fm.get("name", path.stem),
                "description": fm.get("description", ""),
            }
        )

    return {"total": len(files), "files": files}


def scan_chatmodes(chatmodes_dir: Path) -> dict[str, Any]:
    """Scan chatmodes directory for statistics."""
    if not chatmodes_dir.exists():
        return {"total": 0, "files": []}

    files = []
    for path in sorted(chatmodes_dir.glob("*.chatmode.md")):
        content = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        files.append(
            {
                "file": path.name,
                "name": fm.get("name", path.stem),
                "description": fm.get("description", ""),
            }
        )

    return {"total": len(files), "files": files}


def scan_prompts(prompts_dir: Path) -> dict[str, Any]:
    """Scan prompts directory for statistics."""
    if not prompts_dir.exists():
        return {"total": 0, "files": []}

    files = []
    for path in sorted(prompts_dir.glob("*.prompt.md")):
        content = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        files.append(
            {
                "file": path.name,
                "name": fm.get("name", path.stem),
                "mode": fm.get("mode", ""),
                "description": fm.get("description", ""),
            }
        )

    return {"total": len(files), "files": files}


def scan_collections(collections_dir: Path) -> dict[str, Any]:
    """Scan collections directory for statistics."""
    if not collections_dir.exists():
        return {"total": 0, "files": []}

    files = []
    for pattern in ["*.collection.yml", "*.yml"]:
        for path in sorted(collections_dir.glob(pattern)):
            if path.name.endswith(".collection.yml") or not any(
                p.name == path.stem + ".collection.yml"
                for p in collections_dir.glob("*.collection.yml")
            ):
                files.append({"file": path.name})

    # Deduplicate
    seen = set()
    unique_files = []
    for f in files:
        if f["file"] not in seen:
            seen.add(f["file"])
            unique_files.append(f)

    return {"total": len(unique_files), "files": unique_files}


def load_workflow_registry(registry_path: Path) -> dict[str, Any]:
    """Load existing workflow registry."""
    if not registry_path.exists():
        return {
            "total": 0,
            "with_metadata": 0,
            "orphans": 0,
            "by_layer": {},
        }

    try:
        with open(registry_path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("statistics", {})
    except (json.JSONDecodeError, OSError):
        return {
            "total": 0,
            "with_metadata": 0,
            "orphans": 0,
            "by_layer": {},
        }


def find_orphaned_meta(workflows_dir: Path) -> list[str]:
    """Find .meta.json files without corresponding workflow files."""
    orphans = []
    for meta_path in workflows_dir.glob("**/*.meta.json"):
        # Determine expected workflow file
        workflow_name = meta_path.name.replace(".meta.json", "")
        workflow_path = meta_path.parent / workflow_name

        if not workflow_path.exists():
            orphans.append(str(meta_path.relative_to(workflows_dir)))

    return orphans


def find_missing_metadata(workflows_dir: Path) -> list[str]:
    """Find workflow files without corresponding .meta.json files."""
    missing = []
    for workflow_path in workflows_dir.glob("**/*.yml"):
        if workflow_path.name.endswith(".meta.json"):
            continue

        meta_path = workflow_path.parent / (workflow_path.name + ".meta.json")
        if not meta_path.exists():
            missing.append(str(workflow_path.relative_to(workflows_dir)))

    return missing


def build_manifest(root: Path, output: Path) -> dict[str, Any]:
    """Build the unified manifest."""
    # Paths
    ai_framework = root / "src" / "ai_framework"
    workflows_dir = root / ".github" / "workflows"
    registry_path = root / "docs" / "registry" / "workflow-registry.json"

    # Scan components
    agents = scan_agents(ai_framework / "agents")
    chatmodes = scan_chatmodes(ai_framework / "chatmodes")
    prompts = scan_prompts(ai_framework / "prompts")
    collections = scan_collections(ai_framework / "collections")
    workflow_stats = load_workflow_registry(registry_path)

    # Health checks
    orphaned_meta = find_orphaned_meta(workflows_dir) if workflows_dir.exists() else []
    missing_meta = (
        find_missing_metadata(workflows_dir) if workflows_dir.exists() else []
    )

    # Build manifest
    manifest: dict[str, Any] = {
        "$schema": "./manifest.schema.json",
        "generated": datetime.now(timezone.utc).isoformat(),
        "generator": "generate_manifest.py",
        "version": "1.0.0",
        "organization": "ivviiviivvi",
        "statistics": {
            "workflows": {
                "total": workflow_stats.get(
                    "total_workflows", workflow_stats.get("total", 0)
                ),
                "with_metadata": workflow_stats.get("with_metadata", 0),
                "by_layer": workflow_stats.get("by_layer", {}),
            },
            "agents": {"total": agents["total"]},
            "chatmodes": {"total": chatmodes["total"]},
            "prompts": {"total": prompts["total"]},
            "collections": {"total": collections["total"]},
        },
        "registries": {
            "workflows": "workflow-registry.json",
        },
        "health": {
            "orphaned_metadata": orphaned_meta[:10],  # Limit to first 10
            "missing_metadata_count": len(missing_meta),
        },
        "components": {
            "agents": agents["files"][:20],  # Summary, not full list
            "chatmodes_count": chatmodes["total"],
            "prompts_count": prompts["total"],
            "collections_count": collections["total"],
        },
    }

    return manifest


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate unified manifest for org .github repository"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for manifest.json",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output or root / "docs" / "registry" / "manifest.json"

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    # Build and write manifest
    manifest = build_manifest(root, output)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Print summary
    stats = manifest["statistics"]
    print(f"Manifest generated: {output}")
    print(f"  Workflows: {stats['workflows']['total']}")
    print(f"  Agents: {stats['agents']['total']}")
    print(f"  Chatmodes: {stats['chatmodes']['total']}")
    print(f"  Prompts: {stats['prompts']['total']}")
    print(f"  Collections: {stats['collections']['total']}")

    health = manifest["health"]
    if health["orphaned_metadata"]:
        print(f"  Orphaned metadata: {len(health['orphaned_metadata'])}")
    if health["missing_metadata_count"]:
        print(f"  Missing metadata: {health['missing_metadata_count']}")


if __name__ == "__main__":
    main()
