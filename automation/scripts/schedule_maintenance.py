#!/usr/bin/env python3
"""Maintenance Scheduler with ML-Based Timing Prediction.

This module provides ML-based prediction of optimal maintenance windows
to minimize disruption and maximize efficiency. It analyzes repository
activity patterns to find low-impact times for maintenance tasks.

Key Features:
- ML predict optimal maintenance timing based on historical patterns
- Window selection that minimizes disruption to developers
- Activity pattern analysis for intelligent scheduling
- Impact score calculation for each potential window

The scheduler uses machine learning to:
1. Predict low-activity periods
2. Identify optimal maintenance timing windows
3. Minimize disruption by avoiding peak usage times
4. Calculate confidence scores for predictions

Usage:
    python schedule_maintenance.py --owner ORG --repo REPO --task-type TYPE

Environment Variables:
    GITHUB_TOKEN: GitHub API token with repo access
"""

# Re-export everything from proactive_maintenance for backward compatibility
from proactive_maintenance import (
    MaintenanceScheduler,
    main,
)

# Additional exports for direct usage
__all__ = [
    "MaintenanceScheduler",
    "main",
]

if __name__ == "__main__":
    main()
