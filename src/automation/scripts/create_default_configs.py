#!/usr/bin/env python3
"""Create default configuration files for Week 9 automation."""

import os
import yaml
from pathlib import Path


def create_defaults():
    """Create default configuration files if they don't exist."""

    defaults = {
        ".github/auto-merge.yml": {
            "auto_merge": {
                "enabled": True,
                "min_reviews": 1,
                "coverage_threshold": 80.0,
                "required_checks": [],
                "merge_strategy": "squash",
                "delete_branch": True,
                "notify_on_merge": True,
                "notify_on_failure": True,
            }
        },
        ".github/routing.yml": {
            "intelligent_routing": {
                "enabled": True,
                "factors": {
                    "expertise": 0.35,
                    "workload": 0.25,
                    "response_time": 0.20,
                    "availability": 0.15,
                    "performance": 0.05,
                },
                "max_assignments_per_user": 10,
                "fallback_strategy": ["round_robin", "random"],
                "exempt_labels": [],
            }
        },
        ".github/self-healing.yml": {
            "self_healing": {
                "enabled": True,
                "enable_auto_retry": True,
                "max_retry_attempts": 3,
                "initial_retry_delay": 60,
                "retry_backoff_multiplier": 2.0,
                "max_consecutive_failures": 3,
                "dependency_wait_time": 300,
                "create_issues_for_failures": True,
                "send_notifications": True,
            }
        },
        ".github/maintenance.yml": {
            "maintenance": {
                "enabled": True,
                "timing_predictor": "ml",
                "preferred_hours": [2, 3, 4],
                "preferred_days": [6, 0],
                "avoid_dates": [],
                "dependency_updates_enabled": True,
                "cleanup_enabled": True,
                "optimization_enabled": True,
                "notify_before_minutes": 30,
            }
        },
        ".github/analytics.yml": {
            "analytics": {
                "enabled": True,
                "default_model": "random_forest",
                "min_confidence": 0.6,
                "min_accuracy": 0.85,
                "training_lookback_days": 90,
                "retrain_schedule": "weekly",
            }
        },
        ".github/sla.yml": {
            "sla": {
                "enabled": True,
                "check_interval_minutes": 15,
                "thresholds": [
                    {
                        "priority": "P0",
                        "response_time_minutes": 5,
                        "resolution_time_hours": 4,
                        "success_rate_percentage": 99.0,
                        "availability_percentage": 99.9,
                    },
                    {
                        "priority": "P1",
                        "response_time_minutes": 30,
                        "resolution_time_hours": 24,
                        "success_rate_percentage": 95.0,
                        "availability_percentage": 99.0,
                    },
                    {
                        "priority": "P2",
                        "response_time_minutes": 120,
                        "resolution_time_hours": 72,
                        "success_rate_percentage": 90.0,
                        "availability_percentage": 98.0,
                    },
                    {
                        "priority": "P3",
                        "response_time_minutes": 480,
                        "resolution_time_hours": 168,
                        "success_rate_percentage": 85.0,
                        "availability_percentage": 95.0,
                    },
                ],
            }
        },
        ".github/incident.yml": {
            "incident_response": {
                "enabled": True,
                "create_github_issues": True,
                "auto_execute_runbooks": True,
                "severity_keywords": {
                    "SEV-1": ["outage", "data loss", "security breach"],
                    "SEV-2": ["broken feature", "performance degradation"],
                    "SEV-3": ["minor bug", "typo"],
                },
                "escalation_rules": {},
                "notification_channels": {
                    "SEV-1": ["slack", "email", "sms"],
                    "SEV-2": ["slack", "email"],
                    "SEV-3": ["slack"],
                },
            }
        },
    }

    for path, content in defaults.items():
        if not os.path.exists(path):
            print(f"Creating {path}...")
            with open(path, "w") as f:
                yaml.dump(content, f, default_flow_style=False)
        else:
            print(f"Skipping {path} (already exists)")


if __name__ == "__main__":
    create_defaults()
