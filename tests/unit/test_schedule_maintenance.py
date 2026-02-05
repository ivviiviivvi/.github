#!/usr/bin/env python3
"""Unit tests for automation/scripts/schedule_maintenance.py

Focus: Verify re-exports from proactive_maintenance module.
Note: This module is a thin wrapper that re-exports from proactive_maintenance.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))


@pytest.mark.unit
class TestScheduleMaintenanceExports:
    """Test schedule_maintenance module exports."""

    def test_exports_maintenance_scheduler(self):
        """Test exports MaintenanceScheduler class."""
        from schedule_maintenance import MaintenanceScheduler

        assert MaintenanceScheduler is not None
        # Verify it's a class
        assert isinstance(MaintenanceScheduler, type)

    def test_exports_main_function(self):
        """Test exports main function."""
        from schedule_maintenance import main

        assert main is not None
        assert callable(main)

    def test_all_exports_list(self):
        """Test __all__ contains expected exports."""
        import schedule_maintenance

        assert hasattr(schedule_maintenance, "__all__")
        assert "MaintenanceScheduler" in schedule_maintenance.__all__
        assert "main" in schedule_maintenance.__all__

    def test_scheduler_has_expected_methods(self):
        """Test MaintenanceScheduler has expected methods."""
        from schedule_maintenance import MaintenanceScheduler

        # Check for key methods (actual method names from the class)
        assert hasattr(MaintenanceScheduler, "schedule_maintenance")
