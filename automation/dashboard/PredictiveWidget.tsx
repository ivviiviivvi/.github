// Dashboard Widget for Predictive Analytics
// Displays real-time failure risk predictions

import React, { useEffect, useState } from "react";
import "./PredictiveWidget.css";

interface Prediction {
  workflow: string;
  repository: string;
  timestamp: string;
  failure_probability: number;
  prediction: string;
  risk_level: string;
  risk_color: string;
  confidence: number;
}

interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  training_samples: number;
  test_samples: number;
}

const PredictiveWidget: React.FC = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    fetchPredictions();
    fetchMetrics();

    // Refresh every 5 minutes
    const interval = setInterval(
      () => {
        fetchPredictions();
      },
      5 * 60 * 1000,
    );

    return () => clearInterval(interval);
  }, []);

  const fetchPredictions = async () => {
    setIsRefreshing(true);
    try {
      const response = await fetch("/api/predictions/high-risk");
      if (!response.ok) throw new Error("Failed to fetch predictions");

      const data = await response.json();
      setPredictions(data.slice(0, 5)); // Top 5
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await fetch("/api/predictions/metrics");
      if (!response.ok) throw new Error("Failed to fetch metrics");

      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      console.error("Failed to fetch metrics:", err);
    }
  };

  const getRiskIcon = (riskLevel: string): string => {
    switch (riskLevel) {
      case "LOW":
        return "✅";
      case "MEDIUM":
        return "⚠️";
      case "HIGH":
        return "🔶";
      case "CRITICAL":
        return "🔴";
      default:
        return "❓";
    }
  };

  const getRiskClass = (riskColor: string): string => {
    return `risk-${riskColor}`;
  };

  if (loading) {
    return (
      <div className="predictive-widget loading">
        <div className="spinner"></div>
        <p>Loading predictions...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="predictive-widget error">
        <h3>⚠️ Error Loading Predictions</h3>
        <p>{error}</p>
        <button onClick={fetchPredictions}>Retry</button>
      </div>
    );
  }

  return (
    <div className="predictive-widget">
      <div className="widget-header">
        <h3>🔮 Predictive Analytics</h3>
        {metrics && (
          <div className="model-accuracy">
            Model Accuracy: {(metrics.accuracy * 100).toFixed(1)}%
          </div>
        )}
      </div>

      <div className="predictions-list">
        {predictions.length === 0 ? (
          <div className="no-predictions">
            <p>✨ No high-risk workflows detected</p>
            <p className="subtitle">All systems operating normally</p>
          </div>
        ) : (
          predictions.map((pred, index) => (
            <div
              key={`${pred.workflow}-${index}`}
              className={`prediction-item ${getRiskClass(pred.risk_color)}`}
            >
              <div className="prediction-header">
                <span className="risk-icon">
                  {getRiskIcon(pred.risk_level)}
                </span>
                <span className="workflow-name">{pred.workflow}</span>
              </div>

              <div className="prediction-details">
                <div className="detail-row">
                  <span className="label">Risk Level:</span>
                  <span className={`value ${getRiskClass(pred.risk_color)}`}>
                    {pred.risk_level}
                  </span>
                </div>

                <div className="detail-row">
                  <span className="label">Failure Probability:</span>
                  <span className="value">
                    {(pred.failure_probability * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="detail-row">
                  <span className="label">Confidence:</span>
                  <span className="value">
                    {(pred.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              <div
                className="progress-bar"
                role="progressbar"
                aria-valuenow={Math.round(pred.failure_probability * 100)}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={`Failure probability: ${(pred.failure_probability * 100).toFixed(1)}%`}
              >
                <div
                  className={`progress-fill ${getRiskClass(pred.risk_color)}`}
                  style={{ width: `${pred.failure_probability * 100}%` }}
                ></div>
              </div>
            </div>
          ))
        )}
      </div>

      {metrics && (
        <div className="widget-footer">
          <div className="metrics-summary">
            <div className="metric">
              <span className="metric-label">Precision</span>
              <span className="metric-value">
                {(metrics.precision * 100).toFixed(0)}%
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Recall</span>
              <span className="metric-value">
                {(metrics.recall * 100).toFixed(0)}%
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Training Samples</span>
              <span className="metric-value">
                {metrics.training_samples.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      )}

      <div className="widget-actions">
        <button
          onClick={fetchPredictions}
          className="refresh-btn"
          disabled={isRefreshing}
          aria-busy={isRefreshing}
          aria-label={
            isRefreshing ? "Refreshing predictions..." : "Refresh predictions"
          }
        >
          {isRefreshing ? "⏳ Refreshing..." : "🔄 Refresh"}
        </button>
        <a href="/predictions" className="view-all-btn">
          View All →
        </a>
      </div>
    </div>
  );
};

export default PredictiveWidget;
