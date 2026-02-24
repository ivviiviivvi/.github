#!/usr/bin/env python3
"""Build a FUNCTIONcalled registry from workflow metadata sidecar files.

This tool scans for .meta.json files and builds a registry catalog of all
workflows with their metadata, hashes, and FUNCTIONcalled classifications.

Usage:
    python workflow-registry-builder.py --root .github/workflows --out registry/workflow-registry.json
    python workflow-registry-builder.py --root . --include-orphans
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def compute_hash(filepath: Path) -> str | None:
    """Compute SHA256 hash of a file."""
    try:
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None


def load_metadata(meta_path: Path) -> dict[str, Any]:
    """Load metadata from a sidecar file."""
    try:
        with open(meta_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def find_workflow_files(root: Path) -> list[Path]:
    """Find all YAML workflow files."""
    files: list[Path] = []
    for pattern in ["*.yml", "*.yaml"]:
        files.extend(root.glob(f"**/{pattern}"))
    return sorted(files)


def build_registry(root: Path, include_orphans: bool = False) -> dict[str, Any]:
    """Build a registry from metadata files.

    Args:
        root: Root directory to scan
        include_orphans: Include workflows without metadata sidecars

    """
    root = root.resolve()
    resources: list[dict[str, Any]] = []

    # Track workflows with metadata
    workflows_with_meta: set[Path] = set()

    # Find all metadata files
    for meta_path in sorted(root.glob("**/*.meta.json")):
        # Determine the workflow file path
        meta_name = meta_path.name
        if meta_name.endswith(".yml.meta.json") or meta_name.endswith(".yaml.meta.json"):
            workflow_name = meta_name[: -len(".meta.json")]
        else:
            continue  # Skip non-workflow metadata

        workflow_path = meta_path.parent / workflow_name
        workflows_with_meta.add(workflow_path)

        # Load metadata
        meta = load_metadata(meta_path)

        # Build entry
        entry: dict[str, Any] = {
            "name": meta.get("name", workflow_name),
            "path": str(workflow_path.relative_to(root)),
            "meta": str(meta_path.relative_to(root)),
        }

        # Add hash if workflow exists
        file_hash = compute_hash(workflow_path)
        if file_hash:
            entry["hash"] = file_hash

        # Add FUNCTIONcalled classification
        if "functioncalled" in meta:
            fc = meta["functioncalled"]
            entry["functioncalled"] = {
                "canonical": fc.get("canonical"),
                "layer": fc.get("layer"),
                "role": fc.get("role"),
                "domain": fc.get("domain"),
            }

        # Add version
        if "version" in meta:
            entry["version"] = meta["version"]

        # Add profile
        if "profile" in meta:
            entry["profile"] = meta["profile"]

        resources.append(entry)

    # Optionally include orphan workflows (no metadata)
    if include_orphans:
        for workflow_path in find_workflow_files(root):
            if workflow_path not in workflows_with_meta:
                entry = {
                    "name": workflow_path.name,
                    "path": str(workflow_path.relative_to(root)),
                    "meta": None,
                    "orphan": True,
                }
                file_hash = compute_hash(workflow_path)
                if file_hash:
                    entry["hash"] = file_hash
                resources.append(entry)

    # Build registry
    registry: dict[str, Any] = {
        "$schema": "https://example.com/schemas/workflow-registry.schema.json",
        "generated": datetime.now(timezone.utc).isoformat(),
        "generator": "workflow-registry-builder.py",
        "root": str(root),
        "statistics": {
            "total_workflows": len(resources),
            "with_metadata": len(workflows_with_meta),
            "orphans": len(resources) - len(workflows_with_meta) if include_orphans else 0,
            "by_layer": {},
        },
        "resources": resources,
    }

    # Compute layer statistics
    layer_counts: dict[str, int] = {}
    for entry in resources:
        if "functioncalled" in entry and entry["functioncalled"].get("layer"):
            layer = entry["functioncalled"]["layer"]
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
    registry["statistics"]["by_layer"] = layer_counts

    return registry


def main():
    parser = argparse.ArgumentParser(description="Build a FUNCTIONcalled registry from workflow metadata files")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(".github/workflows"),
        help="Root directory to scan (default: .github/workflows)",
    )
    parser.add_argument(
        "--out", type=Path, default=Path("registry/workflow-registry.json"), help="Output registry file path"
    )
    parser.add_argument("--include-orphans", action="store_true", help="Include workflows without metadata sidecars")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty print JSON output (default: true)")

    args = parser.parse_args()

    # Build registry
    print(f"Scanning {args.root} for workflow metadata...")
    registry = build_registry(args.root, args.include_orphans)

    # Ensure output directory exists
    out_path = args.out.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Write registry
    with open(out_path, "w") as f:
        if args.pretty:
            json.dump(registry, f, indent=2)
        else:
            json.dump(registry, f)

    # Summary
    stats = registry["statistics"]
    print(f"✅ Registry written to {args.out}")
    print(f"   Total workflows: {stats['total_workflows']}")
    print(f"   With metadata: {stats['with_metadata']}")
    if args.include_orphans:
        print(f"   Orphans: {stats['orphans']}")
    if stats["by_layer"]:
        print("   By layer:")
        for layer, count in sorted(stats["by_layer"].items()):
            print(f"     - {layer}: {count}")


if __name__ == "__main__":
    main()
