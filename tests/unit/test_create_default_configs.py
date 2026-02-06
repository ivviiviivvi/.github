"""Unit tests for automation/scripts/create_default_configs.py

Focus: Default configuration file creation for Week 9 automation.
"""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

from create_default_configs import create_defaults


@pytest.mark.unit
class TestCreateDefaults:
    """Test create_defaults function."""

    def test_creates_auto_merge_config(self, tmp_path, monkeypatch, capsys):
        """Test creates auto-merge.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "auto-merge.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "auto_merge" in config
        assert config["auto_merge"]["enabled"] is True
        assert config["auto_merge"]["merge_strategy"] == "squash"

    def test_creates_routing_config(self, tmp_path, monkeypatch):
        """Test creates routing.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "routing.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "issue_assignment_router" in config
        assert config["issue_assignment_router"]["factors"]["expertise"] == 0.35

    def test_creates_self_healing_config(self, tmp_path, monkeypatch):
        """Test creates self-healing.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "self-healing.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "self_healing" in config
        assert config["self_healing"]["max_retry_attempts"] == 3

    def test_creates_maintenance_config(self, tmp_path, monkeypatch):
        """Test creates maintenance.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "maintenance.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "maintenance" in config
        assert config["maintenance"]["timing_predictor"] == "ml"

    def test_creates_analytics_config(self, tmp_path, monkeypatch):
        """Test creates analytics.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "analytics.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "analytics" in config
        assert config["analytics"]["default_model"] == "random_forest"

    def test_creates_sla_config(self, tmp_path, monkeypatch):
        """Test creates sla.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "sla.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "sla" in config
        assert len(config["sla"]["thresholds"]) == 4

    def test_creates_incident_config(self, tmp_path, monkeypatch):
        """Test creates incident.yml config."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_file = github_dir / "incident.yml"
        assert config_file.exists()

        config = yaml.safe_load(config_file.read_text())
        assert "incident_response" in config
        assert "SEV-1" in config["incident_response"]["severity_keywords"]

    def test_skips_existing_files(self, tmp_path, monkeypatch, capsys):
        """Test skips files that already exist."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        # Create existing file
        existing = github_dir / "auto-merge.yml"
        existing.write_text("existing: true")

        create_defaults()

        # Should not overwrite
        assert yaml.safe_load(existing.read_text()) == {"existing": True}

        captured = capsys.readouterr()
        assert "Skipping .github/auto-merge.yml (already exists)" in captured.out

    def test_prints_creation_message(self, tmp_path, monkeypatch, capsys):
        """Test prints message for each created file."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        captured = capsys.readouterr()
        assert "Creating .github/auto-merge.yml" in captured.out
        assert "Creating .github/routing.yml" in captured.out
        assert "Creating .github/self-healing.yml" in captured.out

    def test_all_configs_have_enabled_flag(self, tmp_path, monkeypatch):
        """Test all configs have enabled flag set to True."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config_files = [
            "auto-merge.yml",
            "routing.yml",
            "self-healing.yml",
            "maintenance.yml",
            "analytics.yml",
            "sla.yml",
            "incident.yml",
        ]

        for filename in config_files:
            config = yaml.safe_load((github_dir / filename).read_text())
            # Get the main key (first key in the dict)
            main_key = list(config.keys())[0]
            assert config[main_key]["enabled"] is True, f"{filename} should have enabled=True"

    def test_sla_thresholds_ordered_by_priority(self, tmp_path, monkeypatch):
        """Test SLA thresholds are ordered by priority."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config = yaml.safe_load((github_dir / "sla.yml").read_text())
        thresholds = config["sla"]["thresholds"]
        priorities = [t["priority"] for t in thresholds]
        assert priorities == ["P0", "P1", "P2", "P3"]

    def test_incident_notification_channels_escalate(self, tmp_path, monkeypatch):
        """Test incident notification channels escalate with severity."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        create_defaults()

        config = yaml.safe_load((github_dir / "incident.yml").read_text())
        channels = config["incident_response"]["notification_channels"]

        # SEV-1 should have most channels
        assert len(channels["SEV-1"]) >= len(channels["SEV-2"])
        assert len(channels["SEV-2"]) >= len(channels["SEV-3"])
