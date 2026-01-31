#!/usr/bin/env python3
"""Unit tests for automation/scripts/generate_email_digest.py

Focus: HTML email digest generation from workflow metrics.
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts")
)

from generate_email_digest import (
    format_time_ago,
    generate_email,
    generate_summary,
    generate_trend_commentary,
    load_json,
    main,
)


@pytest.mark.unit
class TestLoadJson:
    """Test load_json function."""

    def test_loads_json_file(self, tmp_path):
        """Test loads JSON from file."""
        json_file = tmp_path / "data.json"
        json_file.write_text('{"key": "value"}')

        result = load_json(json_file)

        assert result == {"key": "value"}

    def test_loads_complex_json(self, tmp_path):
        """Test loads complex JSON structure."""
        data = {
            "workflows": {"successRate": 95, "totalRuns": 100},
            "issues": {"opened": 10, "closed": 8},
        }
        json_file = tmp_path / "data.json"
        json_file.write_text(json.dumps(data))

        result = load_json(json_file)

        assert result["workflows"]["successRate"] == 95


@pytest.mark.unit
class TestFormatTimeAgo:
    """Test format_time_ago function."""

    def test_days_ago(self):
        """Test formats days ago."""
        # 3 days ago
        timestamp = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()

        result = format_time_ago(timestamp)

        assert "3 days ago" in result

    def test_day_singular(self):
        """Test singular day."""
        timestamp = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()

        result = format_time_ago(timestamp)

        assert "1 day ago" in result

    def test_hours_ago(self):
        """Test formats hours ago."""
        timestamp = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()

        result = format_time_ago(timestamp)

        assert "5 hours ago" in result

    def test_hour_singular(self):
        """Test singular hour."""
        timestamp = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

        result = format_time_ago(timestamp)

        assert "1 hour ago" in result

    def test_minutes_ago(self):
        """Test formats minutes ago."""
        timestamp = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()

        result = format_time_ago(timestamp)

        assert "30 minutes ago" in result

    def test_minute_singular(self):
        """Test singular minute."""
        timestamp = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()

        result = format_time_ago(timestamp)

        assert "1 minute ago" in result

    def test_just_now(self):
        """Test formats just now."""
        timestamp = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()

        result = format_time_ago(timestamp)

        assert result == "just now"

    def test_handles_z_suffix(self):
        """Test handles Z timezone suffix."""
        timestamp = "2024-01-15T10:00:00Z"

        # Will work but result depends on current time
        result = format_time_ago(timestamp)

        assert "ago" in result or "just now" in result


@pytest.mark.unit
class TestGenerateSummary:
    """Test generate_summary function."""

    def test_excellent_performance(self):
        """Test excellent performance summary."""
        metrics = {"workflows": {"successRate": 98, "totalRuns": 100}}

        result = generate_summary(metrics)

        assert "excellent" in result
        assert "100 total executions" in result
        assert "98%" in result

    def test_strong_performance(self):
        """Test strong performance summary."""
        metrics = {"workflows": {"successRate": 92, "totalRuns": 50}}

        result = generate_summary(metrics)

        assert "strong" in result

    def test_good_performance(self):
        """Test good performance summary."""
        metrics = {"workflows": {"successRate": 87, "totalRuns": 200}}

        result = generate_summary(metrics)

        assert "good" in result

    def test_concerning_performance(self):
        """Test concerning performance summary."""
        metrics = {"workflows": {"successRate": 75, "totalRuns": 150}}

        result = generate_summary(metrics)

        assert "concerning" in result


@pytest.mark.unit
class TestGenerateTrendCommentary:
    """Test generate_trend_commentary function."""

    def test_positive_trend(self):
        """Test positive trend commentary."""
        metrics = {"workflows": {"successRate": 98}}  # Higher than prev_rate (95.2)

        direction, amount, commentary, sentiment = generate_trend_commentary(metrics)

        assert direction == "increased"
        assert sentiment == "positive"
        assert "improvements" in commentary

    def test_negative_trend(self):
        """Test negative trend commentary."""
        metrics = {"workflows": {"successRate": 90}}  # Lower than prev_rate (95.2)

        direction, amount, commentary, sentiment = generate_trend_commentary(metrics)

        assert direction == "decreased"
        assert sentiment == "negative"
        assert "investigating" in commentary

    def test_stable_trend(self):
        """Test stable trend commentary."""
        metrics = {"workflows": {"successRate": 95.2}}  # Equal to prev_rate

        direction, amount, commentary, sentiment = generate_trend_commentary(metrics)

        assert direction == "remained stable"
        assert sentiment == "neutral"
        assert "Consistent" in commentary


@pytest.mark.unit
class TestGenerateEmail:
    """Test generate_email function."""

    @pytest.fixture
    def sample_metrics(self):
        """Create sample metrics data."""
        return {
            "period": {"start": "2024-01-01", "end": "2024-01-07"},
            "workflows": {"successRate": 95, "totalRuns": 100},
            "issues": {"opened": 10, "closed": 8},
            "pullRequests": {"opened": 5, "merged": 4},
        }

    @pytest.fixture
    def sample_events(self):
        """Create sample events data."""
        return [
            {
                "name": "CI Pipeline Failed",
                "html_url": "https://github.com/org/repo/actions/runs/123",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "name": "Deploy Failed",
                "html_url": "https://github.com/org/repo/actions/runs/456",
                "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            },
        ]

    def test_generates_html_email(self, tmp_path, sample_metrics, sample_events):
        """Test generates HTML email file."""
        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text(json.dumps(sample_events))

        generate_email(metrics_file, events_file, output_file)

        assert output_file.exists()
        content = output_file.read_text()

        # Check HTML structure
        assert "<!DOCTYPE html>" in content
        assert "Weekly Workflow Digest" in content
        assert "2024-01-01" in content
        assert "2024-01-07" in content
        assert "95%" in content

    def test_includes_events_section(self, tmp_path, sample_metrics, sample_events):
        """Test includes events section when events exist."""
        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text(json.dumps(sample_events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        assert "Notable Events" in content
        assert "CI Pipeline Failed" in content

    def test_no_events_section_when_empty(self, tmp_path, sample_metrics):
        """Test no events section when events are empty."""
        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text("[]")

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        # Notable Events section should not appear
        assert "Notable Events" not in content

    def test_limits_events_to_five(self, tmp_path, sample_metrics):
        """Test limits events to top 5."""
        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        # Create 10 events
        events = [
            {
                "name": f"Event {i}",
                "html_url": f"https://github.com/org/repo/actions/runs/{i}",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            for i in range(10)
        ]

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text(json.dumps(events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        # Should only include first 5 events
        assert "Event 0" in content
        assert "Event 4" in content
        # Event 5+ should not be present
        assert "Event 5" not in content

    def test_escapes_html_in_metrics(self, tmp_path):
        """Test escapes HTML in metric values."""
        metrics = {
            "period": {"start": "<script>alert('xss')</script>", "end": "2024-01-07"},
            "workflows": {"successRate": 95, "totalRuns": 100},
            "issues": {"opened": 10, "closed": 8},
            "pullRequests": {"opened": 5, "merged": 4},
        }
        events = []

        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(metrics))
        events_file.write_text(json.dumps(events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        # Script tag should be escaped
        assert "<script>" not in content
        assert "&lt;script&gt;" in content

    def test_escapes_html_in_events(self, tmp_path, sample_metrics):
        """Test escapes HTML in event names."""
        events = [
            {
                "name": "<b>Malicious Event</b>",
                "html_url": "https://example.com/test",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ]

        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text(json.dumps(events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        # Bold tag should be escaped
        assert "<b>" not in content or "&lt;b&gt;" in content

    def test_calculates_issues_processed(self, tmp_path, sample_metrics, sample_events):
        """Test calculates issues processed as sum."""
        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text(json.dumps(sample_events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        # 10 opened + 8 closed = 18
        assert "18" in content

    def test_prints_output_path(self, tmp_path, sample_metrics, sample_events, capsys):
        """Test prints output file path."""
        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(sample_metrics))
        events_file.write_text(json.dumps(sample_events))

        generate_email(metrics_file, events_file, output_file)

        captured = capsys.readouterr()
        assert "Email digest generated" in captured.out


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_generates_email(self, tmp_path, monkeypatch):
        """Test main generates email with all args."""
        metrics = {
            "period": {"start": "2024-01-01", "end": "2024-01-07"},
            "workflows": {"successRate": 95, "totalRuns": 100},
            "issues": {"opened": 10, "closed": 8},
            "pullRequests": {"opened": 5, "merged": 4},
        }
        events = []

        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(metrics))
        events_file.write_text(json.dumps(events))

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "generate_email_digest.py",
                "--metrics",
                str(metrics_file),
                "--events",
                str(events_file),
                "--output",
                str(output_file),
            ],
        )

        main()

        assert output_file.exists()

    def test_main_missing_args(self, monkeypatch):
        """Test main exits with missing args."""
        monkeypatch.setattr(sys, "argv", ["generate_email_digest.py"])

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 2

    def test_main_missing_metrics_arg(self, monkeypatch):
        """Test main exits with missing metrics arg."""
        monkeypatch.setattr(
            sys, "argv", ["generate_email_digest.py", "--events", "e.json", "--output", "o.html"]
        )

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 2


@pytest.mark.unit
class TestEventHandling:
    """Test event handling edge cases."""

    def test_event_with_missing_name(self, tmp_path):
        """Test handles event with missing name."""
        metrics = {
            "period": {"start": "2024-01-01", "end": "2024-01-07"},
            "workflows": {"successRate": 95, "totalRuns": 100},
            "issues": {"opened": 10, "closed": 8},
            "pullRequests": {"opened": 5, "merged": 4},
        }
        events = [
            {
                "html_url": "https://example.com/test",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ]

        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(metrics))
        events_file.write_text(json.dumps(events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        assert "Unknown" in content

    def test_event_with_missing_url(self, tmp_path):
        """Test handles event with missing URL."""
        metrics = {
            "period": {"start": "2024-01-01", "end": "2024-01-07"},
            "workflows": {"successRate": 95, "totalRuns": 100},
            "issues": {"opened": 10, "closed": 8},
            "pullRequests": {"opened": 5, "merged": 4},
        }
        events = [
            {
                "name": "Test Event",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ]

        metrics_file = tmp_path / "metrics.json"
        events_file = tmp_path / "events.json"
        output_file = tmp_path / "digest.html"

        metrics_file.write_text(json.dumps(metrics))
        events_file.write_text(json.dumps(events))

        generate_email(metrics_file, events_file, output_file)

        content = output_file.read_text()
        assert "Test Event" in content
        assert "#" in content  # Fallback URL
