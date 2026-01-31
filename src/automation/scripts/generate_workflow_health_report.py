#!/usr/bin/env python3
"""Generate workflow health report for GitHub Actions workflows."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
METRICS_DIR = REPO_ROOT / "metrics" / "health"


def find_unpinned_actions(node: Any) -> list[str]:
    """Return list of workflow `uses:` entries pinned to @main/@master."""

    unpinned: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "uses" and isinstance(item, str):
                    uses_value = item.strip()
                    if "@" in uses_value:
                        ref = uses_value.split("@", 1)[1].split()[0]
                        if ref in {"main", "master"}:
                            unpinned.append(uses_value)
                walk(item)
        elif isinstance(value, list):
            for entry in value:
                walk(entry)

    walk(node)
    return unpinned


def main() -> None:
    health_report: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "overall_health": "excellent",
        "total_workflows": 0,
        "healthy_workflows": 0,
        "warnings": [],
        "errors": [],
        "recommendations": [],
        "metrics": {
            "security": {"score": 10, "issues": []},
            "performance": {"score": 9, "issues": []},
            "reliability": {"score": 9, "issues": []},
            "maintainability": {"score": 9, "issues": []},
        },
    }

    workflows = sorted(
        list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))
    )
    health_report["total_workflows"] = len(workflows)

    for workflow_file in workflows:
        workflow_name = workflow_file.name

        try:
            with workflow_file.open("r", encoding="utf-8") as handle:
                workflow = yaml.safe_load(handle) or {}
        except Exception as exc:  # pragma: no cover - defensive
            health_report["errors"].append(f"{workflow_name}: Parse error - {exc}")
            continue

        workflow_str = workflow_file.read_text(encoding="utf-8")

        if "permissions" not in workflow:
            health_report["warnings"].append(
                f"{workflow_name}: Missing explicit permissions"
            )
            health_report["metrics"]["security"]["score"] -= 0.1

        unpinned_actions = find_unpinned_actions(workflow)
        if unpinned_actions:
            health_report["errors"].append(
                f"{workflow_name}: Contains unpinned actions (@master/@main)"
            )
            health_report["metrics"]["security"]["score"] -= 0.5

        if "setup-python" in workflow_str and "cache:" not in workflow_str:
            health_report["recommendations"].append(
                f"{workflow_name}: Could benefit from pip caching"
            )

        if "setup-node" in workflow_str and "cache:" not in workflow_str:
            health_report["recommendations"].append(
                f"{workflow_name}: Could benefit from npm caching"
            )

        if "timeout-minutes" not in workflow_str:
            health_report["warnings"].append(
                f"{workflow_name}: Missing timeout configuration"
            )

        workflow_issues = [
            item
            for item in health_report["warnings"] + health_report["errors"]
            if workflow_name in item
        ]
        if not workflow_issues:
            health_report["healthy_workflows"] += 1

    if health_report["total_workflows"]:
        health_percentage = (
            health_report["healthy_workflows"] / health_report["total_workflows"] * 100
        )
        if health_percentage >= 95:
            health_report["overall_health"] = "excellent"
        elif health_percentage >= 85:
            health_report["overall_health"] = "good"
        elif health_percentage >= 70:
            health_report["overall_health"] = "fair"
        else:
            health_report["overall_health"] = "needs attention"
    else:
        health_report["overall_health"] = "unknown"

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    with (METRICS_DIR / "latest.json").open("w", encoding="utf-8") as handle:
        json.dump(health_report, handle, indent=2)

    print(f"Overall Health: {health_report['overall_health']}")
    print(
        f"Healthy Workflows: {health_report['healthy_workflows']}/"
        f"{health_report['total_workflows']}"
    )
    print(f"Errors: {len(health_report['errors'])}")
    print(f"Warnings: {len(health_report['warnings'])}")

    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"health={health_report['overall_health']}\n")
            handle.write(f"errors={len(health_report['errors'])}\n")
            handle.write(f"warnings={len(health_report['warnings'])}\n")


if __name__ == "__main__":
    main()
