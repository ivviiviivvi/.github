#!/usr/bin/env python3
"""Staggered walkthrough schedule planning helpers."""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

COMPLETED_STATUSES = {"completed", "skipped"}
DEFAULT_STAGGER_MINUTES = 5


def parse_bool(value: str | bool | None) -> bool:
    """Parse GitHub Actions boolean-like values."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def parse_iso_date(value: str | None) -> date:
    """Parse YYYY-MM-DD dates, defaulting to the current UTC date."""
    if not value:
        return datetime.now(timezone.utc).date()
    return date.fromisoformat(value)


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp with a trailing Z."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    """Load JSON from a path."""
    with path.open() as file:
        return json.load(file)


def write_json(path: Path, data: Any) -> None:
    """Write indented JSON to a path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


def load_schedule(path: Path) -> dict[str, Any] | None:
    """Load a schedule file if it exists and is valid JSON."""
    if not path.exists():
        return None
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"Schedule file must contain a JSON object: {path}")
    return data


def normalize_repo(repo: dict[str, Any]) -> dict[str, Any]:
    """Normalize repository metadata used by the scheduler."""
    full_name = str(repo.get("full_name") or repo.get("name") or "").strip()
    if not full_name:
        raise ValueError(f"Repository entry is missing full_name/name: {repo}")

    name = str(repo.get("name") or full_name.rsplit("/", maxsplit=1)[-1])
    size = int(repo.get("size") or 0)
    return {
        "name": name,
        "full_name": full_name,
        "size": size,
        "default_branch": repo.get("default_branch") or "main",
    }


def generate_schedule(
    repositories: list[dict[str, Any]],
    repos_per_day: int,
    start_date: date,
    stagger_minutes: int = DEFAULT_STAGGER_MINUTES,
) -> dict[str, Any]:
    """Generate a deterministic staggered schedule from repository metadata."""
    if repos_per_day < 1:
        raise ValueError("repos_per_day must be at least 1")

    repos = [normalize_repo(repo) for repo in repositories]
    repos.sort(key=lambda repo: (repo["size"], repo["full_name"].lower()))

    total_repos = len(repos)
    days_needed = (total_repos + repos_per_day - 1) // repos_per_day if total_repos else 0
    schedule: dict[str, Any] = {
        "version": "1.1",
        "generated_at": utc_timestamp(),
        "repos_per_day": repos_per_day,
        "total_repositories": total_repos,
        "schedule_days": days_needed,
        "schedule": {},
    }

    for day_offset in range(days_needed):
        scheduled_date = start_date + timedelta(days=day_offset)
        start_idx = day_offset * repos_per_day
        end_idx = min(start_idx + repos_per_day, total_repos)
        day_repos = repos[start_idx:end_idx]
        date_key = scheduled_date.isoformat()

        schedule["schedule"][date_key] = {
            "date": date_key,
            "repositories": [repo["full_name"] for repo in day_repos],
            "count": len(day_repos),
            "status": "pending",
            "stagger_minutes": stagger_minutes,
        }

    return schedule


def _is_pending_entry(entry: Any) -> bool:
    if not isinstance(entry, dict):
        return False
    repositories = entry.get("repositories") or []
    status = str(entry.get("status") or "pending").lower()
    return bool(repositories) and status not in COMPLETED_STATUSES


def pending_schedule_dates(schedule: dict[str, Any]) -> list[date]:
    """Return pending schedule dates in ascending order."""
    entries = schedule.get("schedule") or {}
    if not isinstance(entries, dict):
        return []

    pending_dates: list[date] = []
    for date_text, entry in entries.items():
        if not _is_pending_entry(entry):
            continue
        try:
            pending_dates.append(date.fromisoformat(str(date_text)))
        except ValueError:
            continue

    return sorted(pending_dates)


def plan_schedule(
    repositories: list[dict[str, Any]],
    existing_schedule: dict[str, Any] | None,
    repos_per_day: int,
    today: date,
    force: bool = False,
    stagger_minutes: int = DEFAULT_STAGGER_MINUTES,
) -> tuple[dict[str, Any], bool, str]:
    """Reuse an active schedule or generate a new one."""
    if force:
        return generate_schedule(repositories, repos_per_day, today, stagger_minutes), True, "forced"

    if existing_schedule and pending_schedule_dates(existing_schedule):
        return existing_schedule, False, "active schedule has pending batches"

    if existing_schedule:
        reason = "existing schedule has no pending batches"
    else:
        reason = "schedule file missing"

    return generate_schedule(repositories, repos_per_day, today, stagger_minutes), True, reason


def select_due_batch(
    schedule: dict[str, Any] | None,
    today: date,
) -> tuple[str | None, list[str], int]:
    """Select the earliest pending batch due on or before today."""
    if not schedule:
        return None, [], DEFAULT_STAGGER_MINUTES

    pending_dates = pending_schedule_dates(schedule)
    due_dates = [scheduled_date for scheduled_date in pending_dates if scheduled_date <= today]
    if not due_dates:
        return None, [], DEFAULT_STAGGER_MINUTES

    selected_date = min(due_dates).isoformat()
    entry = schedule["schedule"][selected_date]
    repositories = [str(repo) for repo in entry.get("repositories", [])]
    stagger_minutes = int(entry.get("stagger_minutes") or DEFAULT_STAGGER_MINUTES)
    return selected_date, repositories, stagger_minutes


def mark_completed(
    schedule: dict[str, Any],
    scheduled_date: str,
    completed_at: str | None = None,
) -> bool:
    """Mark a schedule date as completed."""
    if not scheduled_date:
        return False
    entries = schedule.get("schedule") or {}
    entry = entries.get(scheduled_date)
    if not isinstance(entry, dict):
        return False

    entry["status"] = "completed"
    entry["completed_at"] = completed_at or utc_timestamp()
    return True


def write_github_output(values: dict[str, Any]) -> None:
    """Append simple key/value outputs for GitHub Actions."""
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a") as file:
        for key, value in values.items():
            file.write(f"{key}={value}\n")


def command_plan(args: argparse.Namespace) -> int:
    repositories = load_json(Path(args.repositories))
    if not isinstance(repositories, list):
        raise ValueError("Repository file must contain a JSON array")

    schedule_path = Path(args.schedule_file)
    try:
        existing_schedule = load_schedule(schedule_path)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"Ignoring invalid existing schedule: {exc}")
        existing_schedule = None

    today = parse_iso_date(args.today)
    repos_per_day = int(args.repos_per_day)
    force = parse_bool(args.force)

    schedule, regenerated, reason = plan_schedule(
        repositories,
        existing_schedule,
        repos_per_day,
        today,
        force=force,
        stagger_minutes=int(args.stagger_minutes),
    )
    write_json(Path(args.output), schedule)

    print(f"Schedule regenerated: {str(regenerated).lower()} ({reason})")
    print(f"Total repositories: {schedule.get('total_repositories', 0)}")
    print(f"Schedule days: {schedule.get('schedule_days', 0)}")

    write_github_output(
        {
            "has_schedule": "true",
            "schedule_regenerated": str(regenerated).lower(),
            "schedule_days": schedule.get("schedule_days", 0),
            "total_repositories": schedule.get("total_repositories", 0),
        }
    )
    return 0


def command_due(args: argparse.Namespace) -> int:
    schedule = load_schedule(Path(args.schedule_file))
    today = parse_iso_date(args.today)
    scheduled_date, repositories, stagger_minutes = select_due_batch(schedule, today)

    repos_output = Path(args.repos_output)
    repos_output.write_text("\n".join(repositories) + ("\n" if repositories else ""))

    if repositories:
        print(f"Selected schedule date: {scheduled_date}")
        print(f"Repositories due: {len(repositories)}")
    else:
        print("No repositories are due for execution")

    write_github_output(
        {
            "repos_today": len(repositories),
            "schedule_date": scheduled_date or "",
            "stagger_minutes": stagger_minutes,
        }
    )
    return 0


def command_complete(args: argparse.Namespace) -> int:
    schedule_path = Path(args.schedule_file)
    schedule = load_schedule(schedule_path)
    if not schedule:
        print("No schedule found; nothing to mark complete")
        return 0

    changed = mark_completed(schedule, args.date, args.completed_at)
    if changed:
        write_json(schedule_path, schedule)
        print(f"Marked schedule date complete: {args.date}")
    else:
        print(f"Schedule date not found: {args.date}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Generate or reuse a staggered schedule")
    plan.add_argument("--repositories", required=True)
    plan.add_argument("--schedule-file", required=True)
    plan.add_argument("--output", required=True)
    plan.add_argument("--repos-per-day", required=True)
    plan.add_argument("--today")
    plan.add_argument("--force", default="false")
    plan.add_argument("--stagger-minutes", default=str(DEFAULT_STAGGER_MINUTES))
    plan.set_defaults(func=command_plan)

    due = subparsers.add_parser("due", help="Write repositories due for execution")
    due.add_argument("--schedule-file", required=True)
    due.add_argument("--repos-output", required=True)
    due.add_argument("--today")
    due.set_defaults(func=command_due)

    complete = subparsers.add_parser("complete", help="Mark a schedule date complete")
    complete.add_argument("--schedule-file", required=True)
    complete.add_argument("--date", required=True)
    complete.add_argument("--completed-at")
    complete.set_defaults(func=command_complete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
