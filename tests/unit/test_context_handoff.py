"""Regression tests for the preserved context-handoff generator."""

import json
from pathlib import Path

import pytest

from src.automation.project_meta.context_handoff.context_generator import (
    CompressionLevel,
    ContextPayloadGenerator,
)

EXAMPLE_STATE = (
    Path(__file__).parents[2]
    / "src"
    / "automation"
    / "project_meta"
    / "context_handoff"
    / "examples"
    / ".orchestrator_state.json"
)


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


def test_saved_context_is_newline_terminated(tmp_path):
    """Generated receipts comply with repository EOF formatting."""
    generator = ContextPayloadGenerator(str(EXAMPLE_STATE))
    output = tmp_path / "context.json"

    generator.save_context(str(output), CompressionLevel.MINIMAL)

    raw = output.read_bytes()
    assert raw.endswith(b"\n")
    assert isinstance(json.loads(raw), dict)
