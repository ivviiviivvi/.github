"""Regression tests for the preserved context-handoff generator."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).parents[2]
CONTEXT_HANDOFF = ROOT / "src" / "automation" / "project_meta" / "context-handoff"
EXAMPLE_STATE = CONTEXT_HANDOFF / "examples" / ".orchestrator_state.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load a module from the canonical, CLI-friendly context-handoff path."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator_module = load_module("context_handoff_generator", CONTEXT_HANDOFF / "context_generator.py")
validator_module = load_module("context_handoff_validator", CONTEXT_HANDOFF / "tests" / "validate_context.py")
CompressionLevel = generator_module.CompressionLevel
ContextPayloadGenerator = generator_module.ContextPayloadGenerator
ContextValidator = validator_module.ContextValidator


def test_only_documented_context_handoff_path_exists():
    """The repository keeps one owner path for context-handoff behavior."""
    assert CONTEXT_HANDOFF.is_dir()
    assert not CONTEXT_HANDOFF.with_name("context_handoff").exists()


@pytest.mark.parametrize(
    ("level", "required_fields", "token_limit"),
    [
        (CompressionLevel.MINIMAL, {"summary", "active", "failed", "next"}, 500),
        (
            CompressionLevel.STANDARD,
            {"version", "handoff_id", "summary", "execution_state", "critical_context", "dag_snapshot"},
            1200,
        ),
        (
            CompressionLevel.FULL,
            {
                "version",
                "handoff_id",
                "summary",
                "execution_state",
                "critical_context",
                "dag_snapshot",
                "file_state",
                "environment",
            },
            2000,
        ),
    ],
)
def test_example_state_generates_each_supported_level(level, required_fields, token_limit):
    """The preserved example must exercise every advertised compression level."""
    generator = ContextPayloadGenerator(str(EXAMPLE_STATE))

    context = generator.generate_context(level)

    assert required_fields <= context.keys()
    assert generator.get_token_count(context) <= token_limit


def test_pending_decision_without_timestamp_is_supported():
    """Pending decisions sort safely alongside timestamped decisions."""
    generator = ContextPayloadGenerator(str(EXAMPLE_STATE))

    context = generator.generate_context(CompressionLevel.STANDARD)

    decisions = context["critical_context"]["user_decisions"]
    assert any(decision["choice"] == "pending" for decision in decisions)


def test_failed_dependency_is_reported_as_blocked(tmp_path):
    """Pending tasks with failed dependencies appear in the blocked set."""
    state = {
        "tasks": {
            "failed": {"status": "failed"},
            "blocked": {"status": "pending", "dependencies": ["failed"]},
            "eligible": {"status": "pending", "dependencies": []},
        },
        "context": {"completed_tasks": [], "failed_tasks": ["failed"]},
    }
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps(state), encoding="utf-8")

    generator = ContextPayloadGenerator(str(state_file))

    assert generator._get_blocked_tasks() == ["blocked"]


def test_saved_context_is_newline_terminated(tmp_path):
    """Generated receipts comply with repository EOF formatting."""
    generator = ContextPayloadGenerator(str(EXAMPLE_STATE))
    output = tmp_path / "context.json"

    generator.save_context(str(output), CompressionLevel.MINIMAL)

    raw = output.read_bytes()
    assert raw.endswith(b"\n")
    assert isinstance(json.loads(raw), dict)


def test_shell_wrapper_treats_hostile_output_path_as_data(tmp_path):
    """Quote-bearing output paths cannot become Python source."""
    hostile_name = "context');__import__('pathlib').Path('owned').write_text('x');#.json"
    output = tmp_path / hostile_name
    env = os.environ.copy()
    env.update({"OUTPUT": str(output), "PYTHON": sys.executable})

    result = subprocess.run(
        [str(CONTEXT_HANDOFF / "generate_context.sh"), "minimal", str(EXAMPLE_STATE)],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert output.is_file()
    assert not (tmp_path / "owned").exists()


def test_validator_rejects_payload_over_token_target(tmp_path):
    """Token targets are acceptance criteria, not advisory warnings."""
    payload = {
        "summary": {"phase": "test", "progress": "0%"},
        "active": [],
        "failed": [],
        "next": [],
        "oversized": "x" * 3000,
    }
    payload_file = tmp_path / "oversized.json"
    payload_file.write_text(json.dumps(payload), encoding="utf-8")

    valid, errors, warnings = ContextValidator(str(payload_file)).validate_all()

    assert not valid
    assert not errors
    assert any("exceeds target" in warning for warning in warnings)
