#!/usr/bin/env python3
"""Enhanced ML Predictions for Workflow Optimization.

This module provides advanced machine learning capabilities for predicting
workflow outcomes with a target accuracy of 85% or higher.

Key Features:
- Commit size analysis for change impact prediction
- File count tracking to assess PR complexity
- Author history evaluation for reliability scoring
- Review count analysis for merge probability
- Test coverage correlation with success rates

ML Model Features:
1. commit_size - Lines of code changed (additions + deletions)
2. file_count - Number of files modified in the PR
3. author_history - Author's historical merge success rate
4. review_count - Number of reviews/reviewers on the PR
5. test_coverage - Percentage of code covered by tests

Accuracy Target: 85%+ prediction accuracy through:
- Feature engineering with expanded feature set
- Ensemble methods (Random Forest, Gradient Boosting)
- Cross-validation and hyperparameter tuning
- Continuous model retraining on new data

Usage:
    python enhanced_ml_predictions.py --owner ORG --repo REPO --predict --pr 123
    python enhanced_ml_predictions.py --owner ORG --repo REPO --train --days 90

Environment Variables:
    GITHUB_TOKEN: GitHub API token with repo access
"""

# Re-export from enhanced_analytics for compatibility
from enhanced_analytics import EnhancedAnalyticsEngine, main

# Re-export all functionality
__all__ = [
    "EnhancedAnalyticsEngine",
    "main",
]

if __name__ == "__main__":
    main()
