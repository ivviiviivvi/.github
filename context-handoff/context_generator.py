#!/usr/bin/env python3
"""
Context Payload Generator for Orchestrator State
Generates token-optimized context for AI session handoffs

This module provides a production-ready framework for seamless context transfer
across AI sessions in complex multi-phase projects, achieving 500-2,000 token
handoffs with zero information loss for critical state.

Usage:
    from context_generator import ContextPayloadGenerator, CompressionLevel

    gen = ContextPayloadGenerator()
    context = gen.generate_context(CompressionLevel.STANDARD)
    gen.save_context('context_payload.json', CompressionLevel.STANDARD)
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class CompressionLevel(Enum):
    """Compression levels for context generation"""

    MINIMAL = "minimal"  # ~500 tokens - Critical state only
    STANDARD = "standard"  # ~1200 tokens - Recommended for most cases
    FULL = "full"  # ~2000 tokens - Comprehensive handoff


class ContextPayloadGenerator:
    """Generate context payloads from orchestrator state

    This class reads orchestrator state from a JSON file and generates
    token-optimized context payloads suitable for AI session handoffs.

    Attributes:
        state_file (Path): Path to the orchestrator state JSON file
        state (Dict[str, Any]): Loaded orchestrator state

    Example:
        >>> gen = ContextPayloadGenerator(".orchestrator_state.json")
        >>> context = gen.generate_context(CompressionLevel.STANDARD)
        >>> tokens = gen.get_token_count(context)
        >>> print(f"Generated context with {tokens} tokens")
    """

    def __init__(self, state_file: str = ".orchestrator_state.json"):
        """Initialize the context payload generator

        Args:
            state_file: Path to the orchestrator state JSON file

        Raises:
            FileNotFoundError: If state file does not exist
        """
        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load orchestrator state from JSON file

        Returns:
            Dictionary containing the orchestrator state

        Raises:
            FileNotFoundError: If state file does not exist
            json.JSONDecodeError: If state file is not valid JSON
        """
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_context(
        self, level: CompressionLevel = CompressionLevel.STANDARD
    ) -> Dict[str, Any]:
        """Generate context payload at specified compression level

        Args:
            level: Compression level (MINIMAL, STANDARD, or FULL)

        Returns:
            Dictionary containing the context payload

        Example:
            >>> gen = ContextPayloadGenerator()
            >>> context = gen.generate_context(CompressionLevel.MINIMAL)
        """
        if level == CompressionLevel.MINIMAL:
            return self._generate_minimal()
        elif level == CompressionLevel.STANDARD:
            return self._generate_standard()
        else:
            return self._generate_full()

    def _generate_minimal(self) -> Dict[str, Any]:
        """Generate minimal context (~500 tokens)

        Includes only critical state for immediate resumption:
        - Current phase and task
        - Active/failed tasks
        - Next eligible tasks

        Returns:
            Minimal context dictionary
        """
        tasks = self.state.get("tasks", {})
        context = self.state.get("context", {})

        total = len(tasks)
        completed = len(context.get("completed_tasks", []))
        progress = int((completed / total * 100)) if total > 0 else 0

        return {
            "summary": {
                "phase": context.get("current_phase"),
                "progress": f"{progress}%",
                "task": context.get("active_tasks", [None])[0],
            },
            "active": context.get("active_tasks", []),
            "failed": [
                f"{tid}: {tasks.get(tid, {}).get('error', {}).get('type', 'Error')}"
                for tid in context.get("failed_tasks", [])
            ],
            "next": self._get_eligible_tasks()[:3],
        }

    def _generate_standard(self) -> Dict[str, Any]:
        """Generate standard context (~1200 tokens)

        Includes comprehensive state for robust resumption:
        - Summary with progress metrics
        - Execution state (active, blocked, failed tasks)
        - Critical context (errors, decisions, warnings)
        - DAG snapshot (phase progress, critical path)

        Returns:
            Standard context dictionary
        """
        tasks = self.state.get("tasks", {})
        context = self.state.get("context", {})

        return {
            "version": "1.0.0",
            "handoff_id": f"handoff_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "summary": {
                "project": self.state.get("metadata", {}).get("project_name"),
                "current_phase": context.get("current_phase"),
                "progress": self._generate_minimal()["summary"]["progress"],
                "tasks_complete": len(context.get("completed_tasks", [])),
                "tasks_total": len(tasks),
                "generated_at": datetime.utcnow().isoformat() + "Z",
            },
            "execution_state": {
                "active_tasks": context.get("active_tasks", []),
                "blocked_tasks": self._get_blocked_tasks(),
                "failed_tasks": context.get("failed_tasks", []),
                "next_eligible": self._get_eligible_tasks()[:5],
            },
            "critical_context": {
                "errors": self._format_errors()[-3:],
                "user_decisions": self._get_recent_decisions(3),
                "warnings": self._get_warnings(),
            },
            "dag_snapshot": {
                "phases_completed": self._get_completed_phases(),
                "current_phase_progress": self._get_phase_progress(),
                "critical_path": self._get_critical_path()[:5],
            },
        }

    def _generate_full(self) -> Dict[str, Any]:
        """Generate full context (~2000 tokens)

        Includes all standard context plus:
        - File state (artifacts, required files, disk usage)
        - Environment information (OS, Python, packages)

        Returns:
            Full context dictionary
        """
        standard = self._generate_standard()
        standard["file_state"] = {
            "artifacts": self._get_artifacts()[-5:],
            "required": self._get_required_files(),
            "disk_mb": self._calculate_disk_usage(),
        }
        standard["environment"] = {
            "os": self._get_os_info(),
            "python": self._get_python_version(),
            "packages": self._get_key_packages(),
        }
        return standard

    def _get_eligible_tasks(self) -> List[str]:
        """Get tasks eligible for execution

        A task is eligible if:
        - Status is "pending"
        - All dependencies are completed

        Returns:
            List of eligible task IDs, sorted alphabetically
        """
        tasks = self.state.get("tasks", {})
        completed = set(self.state.get("context", {}).get("completed_tasks", []))
        eligible = []
        for tid, task in tasks.items():
            if task.get("status") == "pending":
                deps = task.get("dependencies", [])
                if all(d in completed for d in deps):
                    eligible.append(tid)
        return sorted(eligible)

    def _get_blocked_tasks(self) -> List[str]:
        """Get tasks blocked by failed dependencies

        A task is blocked if:
        - Status is "pending"
        - At least one dependency has failed

        Returns:
            List of blocked task IDs
        """
        tasks = self.state.get("tasks", {})
        completed = set(self.state.get("context", {}).get("completed_tasks", []))
        failed = set(self.state.get("context", {}).get("failed_tasks", []))
        blocked = []
        for tid, task in tasks.items():
            if task.get("status") == "pending":
                deps = task.get("dependencies", [])
                if any(d in failed for d in deps):
                    blocked.append(tid)
        return blocked

    def _format_errors(self) -> List[Dict[str, Any]]:
        """Format recent errors for context payload

        Returns:
            List of error dictionaries with task_id, type, and message
        """
        errors = self.state.get("error_tracking", {}).get("errors", [])
        return [
            {
                "task_id": e.get("task_id"),
                "type": e.get("error_type"),
                "message": e.get("message")[:100],  # Truncate long messages
            }
            for e in errors
        ]

    def _get_recent_decisions(self, limit: int) -> List[Dict[str, Any]]:
        """Get recent user decisions

        Args:
            limit: Maximum number of decisions to return

        Returns:
            List of recent decision dictionaries
        """
        decisions = self.state.get("user_customizations", {}).get(
            "runtime_decisions", []
        )
        return [
            {"prompt": d.get("prompt"), "choice": d.get("decision", {}).get("choice")}
            for d in sorted(
                decisions,
                key=lambda x: x.get("decision", {}).get("decided_at", ""),
                reverse=True,
            )[:limit]
        ]

    def _get_warnings(self) -> List[str]:
        """Get environment warnings

        Checks for:
        - Python version compatibility
        - Missing dependencies

        Returns:
            List of warning messages
        """
        warnings = []
        env = self.state.get("environment_config", {})
        python_ver = (
            env.get("runtime_environment", {}).get("python", {}).get("version", "")
        )
        if python_ver and python_ver < "3.10":
            warnings.append(f"Python {python_ver} detected, 3.10+ recommended")
        missing = env.get("dependencies", {}).get("missing_dependencies", [])
        if missing:
            warnings.append(f"{len(missing)} missing dependencies")
        return warnings

    def _get_completed_phases(self) -> List[str]:
        """Get list of completed phases

        A phase is completed if all its tasks are successful.

        Returns:
            List of completed phase IDs
        """
        phases = self.state.get("dag", {}).get("phases", {})
        tasks = self.state.get("tasks", {})
        completed = []
        for pid, phase in phases.items():
            if all(
                tasks.get(tid, {}).get("status") == "success"
                for tid in phase.get("tasks", [])
            ):
                completed.append(pid)
        return completed

    def _get_phase_progress(self) -> Dict[str, Any]:
        """Get current phase progress

        Returns:
            Dictionary with total, complete, and percentage
        """
        phase_id = self.state.get("context", {}).get("current_phase")
        if not phase_id:
            return {}
        phases = self.state.get("dag", {}).get("phases", {})
        phase_tasks = phases.get(phase_id, {}).get("tasks", [])
        tasks = self.state.get("tasks", {})
        completed = sum(
            1 for tid in phase_tasks if tasks.get(tid, {}).get("status") == "success"
        )
        return {
            "total": len(phase_tasks),
            "complete": completed,
            "pct": int((completed / len(phase_tasks) * 100)) if phase_tasks else 0,
        }

    def _get_critical_path(self) -> List[str]:
        """Identify critical path tasks

        Uses number of dependents as priority metric.

        Returns:
            List of task IDs sorted by criticality (most critical first)
        """
        tasks = self.state.get("tasks", {})
        priority = [
            (tid, len(task.get("dependents", [])))
            for tid, task in tasks.items()
            if task.get("status") != "success"
        ]
        priority.sort(key=lambda x: x[1], reverse=True)
        return [tid for tid, _ in priority]

    def _get_artifacts(self) -> List[Dict[str, str]]:
        """Get produced artifacts

        Returns:
            List of artifact dictionaries with path and producer
        """
        files = self.state.get("filesystem_state", {}).get("files", {})
        return [
            {"path": path, "by": info.get("produced_by")}
            for path, info in files.items()
            if info.get("produced_by")
        ]

    def _get_required_files(self) -> List[str]:
        """Get required files that exist

        Returns:
            List of file paths
        """
        files = self.state.get("filesystem_state", {}).get("files", {})
        return [p for p, i in files.items() if i.get("required_by") and i.get("exists")]

    def _calculate_disk_usage(self) -> int:
        """Calculate disk usage in MB

        Returns:
            Disk usage in megabytes
        """
        usage = (
            self.state.get("filesystem_state", {})
            .get("disk_usage", {})
            .get("total_bytes", 0)
        )
        return int(usage / (1024 * 1024))

    def _get_os_info(self) -> str:
        """Get OS information

        Returns:
            OS type and version string
        """
        os = (
            self.state.get("environment_config", {})
            .get("system_info", {})
            .get("os", {})
        )
        return f"{os.get('type')} {os.get('version')}"

    def _get_python_version(self) -> str:
        """Get Python version

        Returns:
            Python version string
        """
        return (
            self.state.get("environment_config", {})
            .get("runtime_environment", {})
            .get("python", {})
            .get("version", "unknown")
        )

    def _get_key_packages(self) -> Dict[str, str]:
        """Get key package versions

        Includes common data science and ML packages:
        - numpy
        - pandas
        - torch
        - tensorflow

        Returns:
            Dictionary mapping package names to versions
        """
        packages = (
            self.state.get("environment_config", {})
            .get("dependencies", {})
            .get("python_packages", [])
        )
        key = {}
        for pkg in packages:
            if pkg.get("name") in ["numpy", "pandas", "torch", "tensorflow"]:
                key[pkg["name"]] = pkg["version"]
        return key

    def save_context(
        self,
        output: str = "context_payload.json",
        level: CompressionLevel = CompressionLevel.STANDARD,
    ) -> Path:
        """Save context to file

        Args:
            output: Output file path
            level: Compression level

        Returns:
            Path to the saved file

        Example:
            >>> gen = ContextPayloadGenerator()
            >>> path = gen.save_context("context.json", CompressionLevel.MINIMAL)
            >>> print(f"Saved to {path}")
        """
        context = self.generate_context(level)
        output_path = Path(output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(context, f, separators=(",", ":"))
            f.write("\n")
        return output_path

    def get_token_count(self, context: Dict[str, Any]) -> int:
        """Estimate token count for context

        Uses approximation of 4 characters per token, which is
        accurate for JSON payloads.

        Args:
            context: Context dictionary

        Returns:
            Estimated token count

        Example:
            >>> gen = ContextPayloadGenerator()
            >>> context = gen.generate_context(CompressionLevel.STANDARD)
            >>> tokens = gen.get_token_count(context)
            >>> print(f"Estimated tokens: {tokens}")
        """
        return len(json.dumps(context, separators=(",", ":"))) // 4


def main():
    """Command-line interface for context generation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate AI session handoff context from orchestrator state"
    )
    parser.add_argument(
        "--state-file",
        default=".orchestrator_state.json",
        help="Path to orchestrator state file (default: .orchestrator_state.json)",
    )
    parser.add_argument(
        "--output",
        default="context_payload.json",
        help="Output file path (default: context_payload.json)",
    )
    parser.add_argument(
        "--level",
        choices=["minimal", "standard", "full"],
        default="standard",
        help="Compression level (default: standard)",
    )
    parser.add_argument(
        "--show-tokens", action="store_true", help="Display estimated token count"
    )

    args = parser.parse_args()

    try:
        gen = ContextPayloadGenerator(args.state_file)
        level_map = {
            "minimal": CompressionLevel.MINIMAL,
            "standard": CompressionLevel.STANDARD,
            "full": CompressionLevel.FULL,
        }

        output_path = gen.save_context(args.output, level_map[args.level])
        context = gen.generate_context(level_map[args.level])

        print(f"✓ Context generated successfully")
        print(f"  Level: {args.level}")
        print(f"  Output: {output_path}")

        if args.show_tokens:
            tokens = gen.get_token_count(context)
            print(f"  Estimated tokens: {tokens}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error generating context: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
