#!/usr/bin/env python3
"""Workflow Analyzer - Generate comprehensive workflow inventory and analysis.

This script analyzes all GitHub Actions workflows in .github/workflows/
and generates a detailed inventory report.
"""

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

import yaml


def analyze_workflow(file_path: Path) -> Optional[dict[str, Any]]:
    """Analyze a single workflow file."""
    try:
        with open(file_path) as f:
            workflow = yaml.safe_load(f)

        if not workflow:
            return None

        # Extract key information
        name = workflow.get("name", "Unnamed")

        # Handle YAML 'on' key - PyYAML converts 'on:' to boolean True
        on_value = workflow.get("on") or workflow.get(True)
        if isinstance(on_value, dict):
            triggers = list(on_value.keys())
        elif on_value is not None:
            triggers = [on_value]
        else:
            triggers = ["unknown"]

        jobs = list(workflow.get("jobs", {}).keys())

        # Calculate complexity score
        complexity = len(jobs) + len(str(workflow))  # Simple heuristic

        return {
            "file": file_path.name,
            "name": name,
            "triggers": triggers,
            "jobs": jobs,
            "job_count": len(jobs),
            "complexity": complexity,
            "has_schedule": "schedule" in triggers,
            "has_workflow_dispatch": "workflow_dispatch" in triggers,
            "has_push": "push" in triggers,
            "has_pull_request": "pull_request" in triggers,
        }
    except Exception as e:
        return {
            "file": file_path.name,
            "name": "ERROR",
            "error": str(e),
            "triggers": [],
            "jobs": [],
            "job_count": 0,
            "complexity": 0,
        }


def main():
    workflows_dir = Path(".github/workflows")

    if not workflows_dir.exists():
        print("Error: .github/workflows directory not found")
        return

    # Analyze all workflows
    workflows = []
    for file_path in sorted(workflows_dir.glob("*.y*ml")):
        result = analyze_workflow(file_path)
        if result:
            workflows.append(result)

    # Generate statistics
    total = len(workflows)
    with_errors = sum(1 for w in workflows if "error" in w)
    scheduled = sum(1 for w in workflows if w.get("has_schedule"))
    manual_dispatch = sum(1 for w in workflows if w.get("has_workflow_dispatch"))
    push_triggers = sum(1 for w in workflows if w.get("has_push"))
    pr_triggers = sum(1 for w in workflows if w.get("has_pull_request"))

    # Group by trigger type
    trigger_groups = defaultdict(list)
    for w in workflows:
        for trigger in w.get("triggers", []):
            trigger_groups[trigger].append(w["file"])

    # Generate report
    print("=" * 80)
    print("WORKFLOW INVENTORY ANALYSIS")
    print("=" * 80)
    print("\n📊 SUMMARY STATISTICS")
    print(f"  Total Workflows: {total}")
    print(f"  With Errors: {with_errors}")
    print(f"  Scheduled (cron): {scheduled}")
    print(f"  Manual Dispatch: {manual_dispatch}")
    print(f"  Push Triggers: {push_triggers}")
    print(f"  Pull Request Triggers: {pr_triggers}")

    print("\n🔄 TRIGGER DISTRIBUTION")
    for trigger, files in sorted(trigger_groups.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {trigger}: {len(files)} workflows")

    print("\n📋 DETAILED INVENTORY")
    print("-" * 80)

    for w in sorted(workflows, key=lambda x: x.get("complexity", 0), reverse=True):
        if "error" in w:
            print(f"\n❌ {w['file']}")
            print(f"   ERROR: {w['error']}")
        else:
            print(f"\n📄 {w['file']}")
            print(f"   Name: {w['name']}")
            print(
                f"   Triggers: {', '.join(w['triggers']) if w['triggers'] else 'None'}"  # noqa: E501
            )
            print(
                f"   Jobs: {w['job_count']} ({', '.join(w['jobs'][:3])}{'...' if len(w['jobs']) > 3 else ''})"  # noqa: E501
            )
            print(f"   Complexity Score: {w['complexity']}")

    print(f"\n{'=' * 80}")

    # Look for potential duplicates (same name)
    name_groups = defaultdict(list)
    for w in workflows:
        if "error" not in w:
            name_groups[w["name"]].append(w["file"])

    duplicates = {name: files for name, files in name_groups.items() if len(files) > 1}
    if duplicates:
        print("\n⚠️  POTENTIAL DUPLICATES (Same Workflow Name)")
        for name, files in duplicates.items():
            print(f"   '{name}': {', '.join(files)}")

    # High complexity workflows
    high_complexity = [w for w in workflows if w.get("complexity", 0) > 15000 and "error" not in w]
    if high_complexity:
        print("\n🔴 HIGH COMPLEXITY WORKFLOWS (>15KB)")
        for w in sorted(high_complexity, key=lambda x: x["complexity"], reverse=True)[:10]:
            print(f"   {w['file']}: {w['complexity']} ({w['job_count']} jobs)")

    # Workflows without manual dispatch
    no_dispatch = [w for w in workflows if not w.get("has_workflow_dispatch") and "error" not in w]
    if no_dispatch:
        print(f"\n💡 WORKFLOWS WITHOUT MANUAL DISPATCH: {len(no_dispatch)}")
        print("   (Consider adding workflow_dispatch for testing)")


if __name__ == "__main__":
    main()
