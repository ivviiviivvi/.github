#!/usr/bin/env python3
"""
Task Deduplication System
Prevents cascading and redundant task generation from Jules and automated workflows.
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path

class TaskDeduplicator:
    """Manages task deduplication to prevent redundant work"""
    
    def __init__(self, state_file=".github/task_state.json"):
        self.state_file = Path(state_file)
        self.state = self._load_state()
    
    def _load_state(self):
        """Load existing task state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Corrupted state file {self.state_file}: {e}", file=sys.stderr)
                print("Creating new state file...", file=sys.stderr)
                return {
                    "processed_tasks": {},
                    "active_prs": [],
                    "last_cleanup": None
                }
            except Exception as e:
                print(f"Error loading state file: {e}", file=sys.stderr)
                raise
        return {
            "processed_tasks": {},
            "active_prs": [],
            "last_cleanup": None
        }
    
    def _save_state(self):
        """Save task state"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _generate_task_hash(self, task_type, task_data):
        """Generate unique hash for a task"""
        # Normalize task data
        normalized = f"{task_type}:{json.dumps(task_data, sort_keys=True)}"
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def _is_task_recent(self, task_hash, hours=24):
        """Check if task was processed recently"""
        if task_hash not in self.state["processed_tasks"]:
            return False
        
        timestamp = self.state["processed_tasks"][task_hash]
        processed_time = datetime.fromisoformat(timestamp)
        
        # Check if within time window
        return datetime.now() - processed_time < timedelta(hours=hours)
    
    def should_process_task(self, task_type, task_data, dedupe_window_hours=24):
        """
        Determine if task should be processed or is a duplicate
        
        Args:
            task_type: Type of task (e.g., 'jules_issue', 'pr_review', 'orchestrated_task')
            task_data: Dictionary containing task details
            dedupe_window_hours: Hours to check for duplicates (default 24)
        
        Returns:
            tuple: (should_process: bool, reason: str)
        """
        task_hash = self._generate_task_hash(task_type, task_data)
        
        # Check if already processed recently
        if self._is_task_recent(task_hash, dedupe_window_hours):
            return False, f"Task already processed within last {dedupe_window_hours} hours"
        
        # Task is new, mark as processed
        self.state["processed_tasks"][task_hash] = datetime.now().isoformat()
        self._save_state()
        
        return True, "Task is new and should be processed"
    
    def register_pr(self, pr_number, task_type, task_hash):
        """Register a PR as created for a specific task"""
        pr_entry = {
            "pr_number": pr_number,
            "task_type": task_type,
            "task_hash": task_hash,
            "created_at": datetime.now().isoformat()
        }
        
        self.state["active_prs"].append(pr_entry)
        self._save_state()
    
    def get_active_prs_for_consolidation(self, max_age_hours=24):
        """Get list of PRs that should be consolidated"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        active_prs = []
        for pr in self.state["active_prs"]:
            created_time = datetime.fromisoformat(pr["created_at"])
            if created_time >= cutoff_time:
                active_prs.append(pr["pr_number"])
        
        return active_prs
    
    def cleanup_old_tasks(self, retention_days=7):
        """Remove old task records"""
        cutoff_time = datetime.now() - timedelta(days=retention_days)
        
        # Clean up processed tasks
        tasks_to_remove = []
        for task_hash, timestamp in self.state["processed_tasks"].items():
            processed_time = datetime.fromisoformat(timestamp)
            if processed_time < cutoff_time:
                tasks_to_remove.append(task_hash)
        
        for task_hash in tasks_to_remove:
            del self.state["processed_tasks"][task_hash]
        
        # Clean up old PR records
        prs_to_remove = []
        for i, pr in enumerate(self.state["active_prs"]):
            created_time = datetime.fromisoformat(pr["created_at"])
            if created_time < cutoff_time:
                prs_to_remove.append(i)
        
        for i in sorted(prs_to_remove, reverse=True):
            self.state["active_prs"].pop(i)
        
        self.state["last_cleanup"] = datetime.now().isoformat()
        self._save_state()
        
        return len(tasks_to_remove), len(prs_to_remove)


def main():
    """CLI interface for task deduplicator"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: task_deduplicator.py <command> [args...]")
        print("Commands:")
        print("  check <task_type> <task_json>  - Check if task should be processed")
        print("  register_pr <pr_number> <task_type> <task_json>  - Register a PR")
        print("  get_active_prs [max_age_hours]  - Get PRs for consolidation")
        print("  cleanup [retention_days]  - Clean up old records")
        sys.exit(1)
    
    deduplicator = TaskDeduplicator()
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 4:
            print("Usage: task_deduplicator.py check <task_type> <task_json>")
            sys.exit(1)
        
        task_type = sys.argv[2]
        task_data = json.loads(sys.argv[3])
        
        should_process, reason = deduplicator.should_process_task(task_type, task_data)
        
        result = {
            "should_process": should_process,
            "reason": reason
        }
        print(json.dumps(result))
        sys.exit(0 if should_process else 1)
    
    elif command == "register_pr":
        if len(sys.argv) < 5:
            print("Usage: task_deduplicator.py register_pr <pr_number> <task_type> <task_json>")
            sys.exit(1)
        
        pr_number = int(sys.argv[2])
        task_type = sys.argv[3]
        task_data = json.loads(sys.argv[4])
        task_hash = deduplicator._generate_task_hash(task_type, task_data)
        
        deduplicator.register_pr(pr_number, task_type, task_hash)
        print(f"Registered PR #{pr_number} for task type '{task_type}'")
    
    elif command == "get_active_prs":
        max_age_hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        active_prs = deduplicator.get_active_prs_for_consolidation(max_age_hours)
        print(json.dumps(active_prs))
    
    elif command == "cleanup":
        retention_days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        tasks_removed, prs_removed = deduplicator.cleanup_old_tasks(retention_days)
        print(f"Cleanup complete: removed {tasks_removed} tasks and {prs_removed} PRs")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
