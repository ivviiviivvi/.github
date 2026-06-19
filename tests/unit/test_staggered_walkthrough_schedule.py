"""Tests for staggered walkthrough schedule planning."""

from datetime import date

import pytest

from src.automation.scripts.staggered_walkthrough_schedule import (
    generate_schedule,
    mark_completed,
    plan_schedule,
    select_due_batch,
)


@pytest.fixture
def repositories():
    return [
        {"name": "large-app", "full_name": "organvm/large-app", "size": 500},
        {"name": "small-app", "full_name": "organvm/small-app", "size": 10},
        {"name": "medium-app", "full_name": "organvm/medium-app", "size": 100},
    ]


@pytest.mark.unit
def test_generate_schedule_distributes_repositories_by_day(repositories):
    schedule = generate_schedule(repositories, repos_per_day=2, start_date=date(2026, 6, 1))

    assert schedule["schedule_days"] == 2
    assert schedule["schedule"]["2026-06-01"]["repositories"] == [
        "organvm/small-app",
        "organvm/medium-app",
    ]
    assert schedule["schedule"]["2026-06-02"]["repositories"] == ["organvm/large-app"]


@pytest.mark.unit
def test_plan_schedule_reuses_active_schedule_instead_of_rolling_forward(repositories):
    existing = generate_schedule(repositories, repos_per_day=1, start_date=date(2026, 6, 1))

    planned, regenerated, reason = plan_schedule(
        repositories,
        existing,
        repos_per_day=1,
        today=date(2026, 6, 2),
    )

    assert regenerated is False
    assert "pending batches" in reason
    assert planned["schedule"].keys() == existing["schedule"].keys()
    assert "2026-06-01" in planned["schedule"]


@pytest.mark.unit
def test_plan_schedule_regenerates_after_all_batches_complete(repositories):
    existing = generate_schedule(repositories, repos_per_day=3, start_date=date(2026, 6, 1))
    mark_completed(existing, "2026-06-01", "2026-06-01T01:00:00Z")

    planned, regenerated, reason = plan_schedule(
        repositories,
        existing,
        repos_per_day=3,
        today=date(2026, 6, 8),
    )

    assert regenerated is True
    assert reason == "existing schedule has no pending batches"
    assert list(planned["schedule"]) == ["2026-06-08"]


@pytest.mark.unit
def test_select_due_batch_catches_up_oldest_pending_batch(repositories):
    schedule = generate_schedule(repositories, repos_per_day=1, start_date=date(2026, 6, 1))

    scheduled_date, due_repositories, stagger_minutes = select_due_batch(schedule, date(2026, 6, 3))

    assert scheduled_date == "2026-06-01"
    assert due_repositories == ["organvm/small-app"]
    assert stagger_minutes == 5


@pytest.mark.unit
def test_mark_completed_updates_selected_date(repositories):
    schedule = generate_schedule(repositories, repos_per_day=1, start_date=date(2026, 6, 1))

    changed = mark_completed(schedule, "2026-06-01", "2026-06-01T01:00:00Z")

    assert changed is True
    assert schedule["schedule"]["2026-06-01"]["status"] == "completed"
    assert schedule["schedule"]["2026-06-01"]["completed_at"] == "2026-06-01T01:00:00Z"
