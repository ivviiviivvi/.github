#!/usr/bin/env python3
"""Workflow Failure Prediction Model.

Collects historical workflow data and trains a machine learning model
to predict the likelihood of workflow failures.

Usage:
    python3 predict_workflow_failures.py --collect --days 90
    python3 predict_workflow_failures.py --train
    python3 predict_workflow_failures.py --predict owner/repo workflow-name
"""

import argparse
import hashlib
import hmac
import json
import logging
import os
import subprocess  # nosec B404
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

try:
    import joblib
except ImportError as err:
    raise SystemExit("joblib is required for model serialization. Install joblib to proceed.") from err


class WorkflowPredictor:
    """Predicts workflow failure probability using machine learning."""

    def __init__(self, model_path: str = "automation/ml/workflow_model.pkl"):
        """Initialize predictor with optional model path."""
        self.model_path = Path(model_path)
        self.model: Optional[RandomForestClassifier] = None
        self.feature_columns: list[str] = []
        # Secret for model signature - should be set via environment variable
        self._secret = os.getenv("ML_MODEL_SECRET", "default-insecure-secret").encode()

    def _generate_signature(self, data: bytes) -> str:
        """Generate HMAC signature for data."""
        return hmac.new(self._secret, data, hashlib.sha256).hexdigest()

    def _verify_signature(self, data: bytes, signature: str) -> bool:
        """Verify HMAC signature for data."""
        expected = self._generate_signature(data)
        return hmac.compare_digest(expected, signature)

    def collect_historical_data(self, days: int = 90) -> pd.DataFrame:
        """Collect historical workflow data from GitHub Actions.

        Args:
            days: Number of days of history to collect

        Returns:
            DataFrame with workflow execution data

        """
        print(f"Collecting {days} days of workflow data...")

        # Calculate date range
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)

        # Collect workflow runs via GitHub CLI
        try:
            result = subprocess.run(  # nosec B603 B607
                [
                    "gh",
                    "api",
                    "-H",
                    "Accept: application/vnd.github+json",
                    f"/repos/{self._get_current_repo()}/actions/runs",
                    "-",
                    f"created=>={start_date.isoformat()}Z",
                    "-",
                    "per_page=100",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            runs = json.loads(result.stdout)["workflow_runs"]

        except Exception as e:
            print(f"Error collecting data: {e}", file=sys.stderr)
            return pd.DataFrame()

        # Process runs into features
        records = []
        for run in runs:
            record = self._extract_features(run)
            if record:
                records.append(record)

        df = pd.DataFrame(records)
        print(f"Collected {len(df)} workflow runs")

        return df

    def _get_current_repo(self) -> str:
        """Get current repository name."""
        try:
            result = subprocess.run(  # nosec B603 B607
                ["gh", "repo", "view", "--json", "nameWithOwner"],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)["nameWithOwner"]
        except Exception as e:
            # SubprocessError: gh command failed
            # JSONDecodeError: invalid JSON response
            # KeyError: missing expected field
            # OSError: command not found or execution error
            logging.debug(f"Could not detect repository: {e}")
            return "ivviiviivvi/.github"  # Default

    def _extract_features(self, run: dict) -> Optional[dict]:
        """Extract features from workflow run."""
        try:
            created = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))

            # Extract features
            features = {
                # Temporal features
                "hour_of_day": created.hour,
                "day_of_week": created.weekday(),
                "is_weekend": 1 if created.weekday() >= 5 else 0,
                # Workflow features
                "workflow_id": run["workflow_id"],
                "workflow_name_hash": hash(run["name"]) % 10000,
                "event": run["event"],
                "event_hash": hash(run["event"]) % 100,
                # Repository features
                "run_number": run["run_number"],
                "run_attempt": run["run_attempt"],
                # Target variable
                "failed": 1 if run["conclusion"] == "failure" else 0,
            }

            return features

        except Exception as e:
            print(f"Error extracting features: {e}", file=sys.stderr)
            return None

    def prepare_features(self, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        """Prepare features for training.

        Args:
            df: DataFrame with workflow data

        Returns:
            Tuple of (X, y) features and labels

        """
        # Define feature columns
        self.feature_columns = [
            "hour_of_day",
            "day_of_week",
            "is_weekend",
            "workflow_id",
            "workflow_name_hash",
            "event_hash",
            "run_number",
            "run_attempt",
        ]

        X = df[self.feature_columns].values
        y = df["failed"].values

        return X, y

    def train(self, df: pd.DataFrame, test_size: float = 0.15) -> dict:
        """Train the prediction model.

        Args:
            df: DataFrame with workflow data
            test_size: Fraction of data for testing

        Returns:
            Dictionary with training metrics

        """
        print("Training prediction model...")

        # Prepare features
        X, y = self.prepare_features(df)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)

        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Failure rate: {y.mean():.1%}")

        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )

        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        _y_proba = self.model.predict_proba(X_test)[:, 1]  # noqa: F841

        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary")

        metrics: dict[str, Any] = {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "f1_score": float(f1),
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "failure_rate": float(y.mean()),
        }

        print("\nModel Performance:")
        print(f"  Accuracy: {accuracy:.1%}")
        print(f"  Precision: {precision:.1%}")
        print(f"  Recall: {recall:.1%}")
        print(f"  F1 Score: {f1:.1%}")

        # Feature importance
        importances = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_columns, importances))

        print("\nTop 5 Features:")
        for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {feature}: {importance:.3f}")

        metrics["feature_importance"] = feature_importance

        # Save model
        self.save_model()

        return metrics

    def predict(self, workflow_name: str | dict, repository: Optional[str] = None) -> float | dict:
        """Predict failure probability for a workflow or feature set.

        Args:
            workflow_name: Workflow name string or feature dict
            repository: Repository name (owner/repo) when predicting by workflow name

        Returns:
            Failure probability for feature dicts or a prediction summary for workflow names

        """
        if self.model is None:
            if self.model_path.exists():
                self.load_model()
            else:
                raise ValueError("Model not trained")

        if isinstance(workflow_name, dict):
            features = workflow_name
            X = np.array([[features[col] for col in self.feature_columns]])
            assert self.model is not None, "Model not loaded"  # nosec B101
            return float(self.model.predict_proba(X)[0, 1])

        if repository is None:
            raise ValueError("Repository is required for workflow prediction")

        # Create feature vector for current time
        now = datetime.now(timezone.utc)
        features = {
            "hour_of_day": now.hour,
            "day_of_week": now.weekday(),
            "is_weekend": 1 if now.weekday() >= 5 else 0,
            "workflow_id": 0,  # Unknown for prediction
            "workflow_name_hash": hash(workflow_name) % 10000,
            "event_hash": 0,  # Unknown for prediction
            "run_number": 0,  # Unknown for prediction
            "run_attempt": 1,  # Assume first attempt
        }

        X = np.array([[features[col] for col in self.feature_columns]])

        # Predict
        assert self.model is not None, "Model not loaded"  # nosec B101
        failure_prob = self.model.predict_proba(X)[0, 1]
        prediction = self.model.predict(X)[0]

        # Risk level
        if failure_prob < 0.05:
            risk_level = "LOW"
            color = "green"
        elif failure_prob < 0.15:
            risk_level = "MEDIUM"
            color = "yellow"
        elif failure_prob < 0.30:
            risk_level = "HIGH"
            color = "orange"
        else:
            risk_level = "CRITICAL"
            color = "red"

        result = {
            "workflow": workflow_name,
            "repository": repository,
            "timestamp": now.isoformat(),
            "failure_probability": float(failure_prob),
            "prediction": "FAILURE" if prediction == 1 else "SUCCESS",
            "risk_level": risk_level,
            "risk_color": color,
            "confidence": float(1 - abs(failure_prob - 0.5) * 2),
        }

        return result

    def assess_risk(self, features: dict) -> dict:
        """Assess risk level based on predicted failure probability."""
        probability = float(self.predict(features))

        if probability < 0.15:
            level = "LOW"
        elif probability < 0.30:
            level = "MEDIUM"
        elif probability < 0.60:
            level = "HIGH"
        else:
            level = "CRITICAL"

        return {"probability": probability, "level": level}

    def get_high_risk_workflows(self, threshold: float = 0.15) -> list[dict]:
        """Identify workflows at high risk of failure.

        Args:
            threshold: Probability threshold for high risk

        Returns:
            List of high-risk workflow predictions

        """
        # Get list of workflows
        try:
            result = subprocess.run(  # nosec B603 B607
                ["gh", "workflow", "list", "--json", "name"],
                capture_output=True,
                text=True,
                check=True,
            )
            workflows = json.loads(result.stdout)
        except Exception as e:
            print(f"Error listing workflows: {e}", file=sys.stderr)
            return []

        # Predict for each workflow
        high_risk = []
        repo = self._get_current_repo()

        for workflow in workflows:
            prediction = self.predict(workflow["name"], repo)
            if prediction["failure_probability"] >= threshold:
                high_risk.append(prediction)

        # Sort by probability descending
        high_risk.sort(key=lambda x: x["failure_probability"], reverse=True)

        return high_risk

    def save_model(self):
        """Save trained model to disk with security signature."""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            "model": self.model,
            "feature_columns": self.feature_columns,
        }

        # Serialize model data
        temp_path = self.model_path.with_suffix(".tmp")
        with open(temp_path, "wb") as f:
            joblib.dump(model_data, f)

        # Generate signature
        with open(temp_path, "rb") as f:
            data = f.read()
            signature = self._generate_signature(data)

        # Write signature file
        sig_path = self.model_path.with_suffix(".pkl.sig")
        with open(sig_path, "w") as f:
            f.write(signature)

        # Move to final path
        if self.model_path.exists():
            self.model_path.unlink()
        temp_path.rename(self.model_path)

        print(f"\nModel saved to {self.model_path}")

    def load_model(self):
        """Load trained model from disk with signature verification."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        sig_path = self.model_path.with_suffix(".pkl.sig")
        if not sig_path.exists():
            raise ValueError(f"Missing signature file: {sig_path}")

        with open(self.model_path, "rb") as f:
            data = f.read()

        with open(sig_path) as f:
            signature = f.read().strip()

        if not self._verify_signature(data, signature):
            raise ValueError("Model signature verification failed")

        with open(self.model_path, "rb") as f:
            model_data = joblib.load(f)

        self.model = model_data["model"]
        self.feature_columns = model_data["feature_columns"]

        print(f"Model loaded from {self.model_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Predict workflow failures using machine learning")
    parser.add_argument(
        "--collect",
        action="store_true",
        help="Collect historical workflow data",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Days of historical data to collect (default: 90)",
    )
    parser.add_argument("--train", action="store_true", help="Train the prediction model")
    parser.add_argument(
        "--predict",
        nargs=2,
        metavar=("REPO", "WORKFLOW"),
        help="Predict failure for specific workflow",
    )
    parser.add_argument("--high-risk", action="store_true", help="List high-risk workflows")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.15,
        help="Risk threshold for high-risk workflows (default: 0.15)",
    )
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    predictor = WorkflowPredictor()

    try:
        if args.collect:
            # Collect data
            df = predictor.collect_historical_data(args.days)

            # Save to file
            output_file = Path("automation/ml/workflow_data.csv")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_file, index=False)

            print(f"\nData saved to {output_file}")

        elif args.train:
            # Load data
            data_file = Path("automation/ml/workflow_data.csv")
            if not data_file.exists():
                print(
                    "Error: No data file found. Run with --collect first.",
                    file=sys.stderr,
                )
                sys.exit(1)

            df = pd.read_csv(data_file)

            # Train model
            metrics = predictor.train(df)

            # Save metrics
            metrics_file = Path("automation/ml/model_metrics.json")
            with open(metrics_file, "w") as f:
                # Convert numpy types to native Python types
                serializable_metrics = {
                    k: (float(v) if isinstance(v, (np.floating, np.integer)) else v)
                    for k, v in metrics.items()
                    if k != "feature_importance"
                }
                serializable_metrics["feature_importance"] = {
                    k: float(v) for k, v in metrics["feature_importance"].items()
                }
                json.dump(serializable_metrics, f, indent=2)

            print(f"\nMetrics saved to {metrics_file}")

        elif args.predict:
            # Predict for specific workflow
            repo, workflow = args.predict
            result = predictor.predict(workflow, repo)

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n{'=' * 60}")
                print(f"Workflow: {result['workflow']}")
                print(f"Repository: {result['repository']}")
                print(f"{'=' * 60}")
                print(f"Failure Probability: {result['failure_probability']:.1%}")
                print(f"Prediction: {result['prediction']}")
                print(
                    f"Risk Level: {result['risk_level']} ({result['risk_color']})"  # noqa: E501
                )
                print(f"Confidence: {result['confidence']:.1%}")
                print(f"{'=' * 60}")

        elif args.high_risk:
            # List high-risk workflows
            workflows = predictor.get_high_risk_workflows(args.threshold)

            if args.json:
                print(json.dumps(workflows, indent=2))
            else:
                print(f"\nHigh-Risk Workflows (threshold: {args.threshold:.0%}):")
                print(f"{'=' * 80}")

                if not workflows:
                    print("No high-risk workflows detected.")
                else:
                    for i, wf in enumerate(workflows, 1):
                        print(f"\n{i}. {wf['workflow']}")
                        print(
                            f"   Failure Probability: {wf['failure_probability']:.1%}"  # noqa: E501
                        )
                        print(f"   Risk Level: {wf['risk_level']}")
                        print(f"   Confidence: {wf['confidence']:.1%}")

                print(f"\n{'=' * 80}")
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
