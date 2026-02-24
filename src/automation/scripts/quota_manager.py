"""Quota Manager for GitHub Actions and API usage tracking.

Provides quota management for GitHub Actions workflows and API calls, including:
- Usage tracking per subscription/service
- Lock-based concurrency control (fcntl on Unix, directory lock on Windows)
- Task queue management for deferred operations
- Automatic quota reset based on daily/monthly cadence

Usage:
    from quota_manager import get_usage, increment_usage, reset_quotas

    # Check current usage
    usage = get_usage("github-api")

    # Increment usage
    increment_usage("github-api", amount=1)

    # Reset expired quotas
    reset_quotas()
"""

import json
import os
import sys
import time
from collections.abc import Generator
from contextlib import contextmanager, suppress
from datetime import datetime
from typing import Any

SUBSCRIPTIONS_FILE = ".github/subscriptions.json"
TASK_QUEUE_FILE = ".github/task_queue.json"
# Legacy lock directory for fallback
LOCK_DIR = ".github/state.lock"
# New lock file for fcntl
LOCK_FILE = ".github/quota.lock"

# Check if fcntl is available (Unix/Linux/macOS)
try:
    import fcntl

    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False


@contextmanager
def acquire_lock(timeout: int = 60) -> Generator[None, None, None]:
    """Acquires a lock to prevent concurrent modifications.
    Uses fcntl (flock) on Unix-like systems for robust process-based locking.
    Falls back to atomic directory creation on Windows or if fcntl is unavailable.  # noqa: E501.
    """
    start_time = time.time()

    if HAS_FCNTL:
        # FCNTL (Unix) Implementation
        # Ensure lock file exists
        if not os.path.exists(LOCK_FILE):
            try:
                # Create empty file
                with open(LOCK_FILE, "w") as _f:  # noqa: F841
                    pass
            except OSError:
                pass  # Might be created by another process concurrently

        fd = None
        try:
            fd = open(LOCK_FILE, "r+")
            while True:
                try:
                    # Try to acquire exclusive lock without blocking
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError as err:
                    # Lock held by another process
                    if time.time() - start_time >= timeout:
                        raise TimeoutError(f"Could not acquire lock on {LOCK_FILE}") from err
                    time.sleep(0.1)

            yield

        finally:
            if fd:
                # Release lock and close file
                with suppress(OSError):
                    fcntl.flock(fd, fcntl.LOCK_UN)
                fd.close()
    else:
        # Fallback (Windows/Non-Unix) Implementation
        while True:
            try:
                os.mkdir(LOCK_DIR)
                break
            except FileExistsError as err:
                if time.time() - start_time >= timeout:
                    raise TimeoutError(f"Could not acquire lock on {LOCK_DIR}") from err
                time.sleep(0.5)
        try:
            yield
        finally:
            with suppress(OSError):
                os.rmdir(LOCK_DIR)


def get_subscriptions() -> dict[str, Any]:
    """Reads the subscriptions file and returns the subscriptions data."""
    try:
        with open(SUBSCRIPTIONS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"subscriptions": []}


def get_usage(subscription_name: str) -> int:
    """Gets the current usage for a specific subscription."""
    data = get_subscriptions()
    for sub in data["subscriptions"]:
        if sub["name"] == subscription_name:
            return sub.get("usage", 0)
    return 0


def increment_usage(subscription_name: str, amount: int = 1) -> None:
    """Increments the usage for a specific subscription."""
    with acquire_lock():
        try:
            with open(SUBSCRIPTIONS_FILE) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"subscriptions": []}

        for sub in data["subscriptions"]:
            if sub["name"] == subscription_name:
                sub["usage"] = sub.get("usage", 0) + amount
                break

        with open(SUBSCRIPTIONS_FILE, "w") as f:
            json.dump(data, f, indent=2)


def reset_quotas() -> None:
    """Resets the usage for subscriptions based on their reset cadence."""
    with acquire_lock():
        try:
            with open(SUBSCRIPTIONS_FILE) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        today = datetime.now()
        for sub in data["subscriptions"]:
            try:
                last_reset = datetime.strptime(sub["last_reset"], "%Y-%m-%d")
            except ValueError:
                last_reset = None

            if last_reset is None:
                continue

            if sub["reset_cadence"] == "daily":
                if last_reset.date() != today.date():
                    sub["usage"] = 0
                    sub["last_reset"] = today.strftime("%Y-%m-%d")
            elif sub["reset_cadence"] == "monthly":
                if today.month != last_reset.month or today.year != last_reset.year:
                    sub["usage"] = 0
                    sub["last_reset"] = today.strftime("%Y-%m-%d")

        with open(SUBSCRIPTIONS_FILE, "w") as f:
            json.dump(data, f, indent=2)


def add_task_to_queue(task: dict[str, Any]) -> None:
    """Adds a task to the task queue."""
    with acquire_lock():
        try:
            with open(TASK_QUEUE_FILE) as f:
                queue = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            queue = []
        queue.append(task)
        with open(TASK_QUEUE_FILE, "w") as f:
            json.dump(queue, f, indent=2)


def get_tasks_from_queue() -> list[dict[str, Any]]:
    """Retrieves all tasks from the task queue."""
    try:
        with open(TASK_QUEUE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def remove_task_from_queue(task: dict[str, Any]) -> None:
    """Removes a specific task from the task queue."""
    with acquire_lock():
        try:
            with open(TASK_QUEUE_FILE) as f:
                queue = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        new_queue = [t for t in queue if t != task]

        with open(TASK_QUEUE_FILE, "w") as f:
            json.dump(new_queue, f, indent=2)


def main() -> None:
    """CLI entry point for quota management commands."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get_usage":
            print(get_usage(sys.argv[2]))
        elif command == "increment_usage":
            increment_usage(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1)
        elif command == "reset_quotas":
            reset_quotas()
        elif command == "add_task":
            add_task_to_queue(json.loads(sys.argv[2]))
        elif command == "get_tasks":
            print(json.dumps(get_tasks_from_queue()))
        elif command == "remove_task":
            remove_task_from_queue(json.loads(sys.argv[2]))


if __name__ == "__main__":
    main()
