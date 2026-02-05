#!/usr/bin/env python3
"""Unit tests for automation/scripts/enhanced_ml_predictions.py

Focus: Verify re-exports from enhanced_analytics module.
Note: This module is a thin wrapper that re-exports from enhanced_analytics.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))


@pytest.mark.unit
class TestEnhancedMlPredictionsExports:
    """Test enhanced_ml_predictions module exports."""

    def test_exports_enhanced_analytics_engine(self):
        """Test exports EnhancedAnalyticsEngine class."""
        from enhanced_ml_predictions import EnhancedAnalyticsEngine

        assert EnhancedAnalyticsEngine is not None
        # Verify it's a class
        assert isinstance(EnhancedAnalyticsEngine, type)

    def test_exports_main_function(self):
        """Test exports main function."""
        from enhanced_ml_predictions import main

        assert main is not None
        assert callable(main)

    def test_all_exports_list(self):
        """Test __all__ contains expected exports."""
        import enhanced_ml_predictions

        assert hasattr(enhanced_ml_predictions, "__all__")
        assert "EnhancedAnalyticsEngine" in enhanced_ml_predictions.__all__
        assert "main" in enhanced_ml_predictions.__all__

    def test_engine_has_expected_methods(self):
        """Test EnhancedAnalyticsEngine has expected methods."""
        from enhanced_ml_predictions import EnhancedAnalyticsEngine

        # Check for key methods (actual method names from the class)
        assert hasattr(EnhancedAnalyticsEngine, "predict")
        assert hasattr(EnhancedAnalyticsEngine, "train_models")
