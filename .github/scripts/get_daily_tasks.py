#!/usr/bin/env python3
"""
Daily task orchestrator script
Identifies tasks that should run today based on cron schedules
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from croniter import croniter


def get_daily_tasks(orchestration_file=".github/orchestration_tasks.json"):
    """Get tasks scheduled for today"""
    now = datetime.now()

    try:
        with open(orchestration_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(
            f"Error: Orchestration file not found: {orchestration_file}",
            file=sys.stderr,
        )
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in orchestration file: {e}", file=sys.stderr)
        return []

    daily_tasks = []

    for task in config.get("tasks", []):
        if not task.get("enabled", False):
            continue

        schedule = task.get("schedule", "")
        if not croniter.is_valid(schedule):
            print(
                f"Warning: Invalid cron schedule for task {task.get('id', 'unknown')}: {schedule}",
                file=sys.stderr,
            )
            continue

        try:
            cron = croniter(schedule, now)
            # Check if task should run today
            prev_run = cron.get_prev(datetime)
            if (now - prev_run).total_seconds() <= 86400:  # 24 hours
                daily_tasks.append(task)
        except Exception as e:
            print(
                f"Error processing task {task.get('id', 'unknown')}: {e}",
                file=sys.stderr,
            )
            continue

    return daily_tasks


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        orchestration_file = sys.argv[1]
    else:
        orchestration_file = ".github/orchestration_tasks.json"

    daily_tasks = get_daily_tasks(orchestration_file)

    print(f"Found {len(daily_tasks)} tasks scheduled for today")
    print(json.dumps(daily_tasks, indent=2))

    # Write to file for GitHub Actions (use RUNNER_TEMP if available)
    import tempfile

    output_dir = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir()))
    output_file = output_dir / "daily_tasks.json"
    with open(output_file, "w") as f:
        json.dump(daily_tasks, f)


if __name__ == "__main__":
    main()
