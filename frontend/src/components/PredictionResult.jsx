import React from 'react';

function PredictionResult({ result }) {
  const probabilityPercent = (result.churn_probability * 100).toFixed(1);

  return (
    <div className="result-card">
      <h4>Prediction Result</h4>
      <div className="result-item">
        <span className="result-label">Prediction</span>
        <span className={`status-badge ${result.churn_prediction === 1 ? 'status-churn' : 'status-no-churn'}`}>
          {result.churn_label}
        </span>
      </div>
      <div className="result-item">
        <span className="result-label">Probability</span>
        <span className="result-value" style={{ color: result.churn_prediction === 1 ? '#e74c3c' : '#27ae60' }}>
          {probabilityPercent}%
        </span>
      </div>
      <div style={{ marginTop: '12px' }}>
        <div className="probability-bar">
          <div
            className="probability-fill"
            style={{ 
              width: `${probabilityPercent}%`,
              background: result.churn_prediction === 1 
                ? 'linear-gradient(90deg, #e74c3c 0%, #c0392b 100%)'
                : 'linear-gradient(90deg, #3498db 0%, #2980b9 100%)'
            }}
          >
            {probabilityPercent}%
          </div>
        </div>
      </div>
      <div className="notes-section" style={{ marginTop: '12px' }}>
        <h4>Interpretation</h4>
        <p>
          {result.churn_prediction === 1 ? (
            <>
              <strong style={{ color: '#c0392b' }}>High Risk:</strong> This customer has a {probabilityPercent}% probability of churning.
              Consider proactive retention strategies such as offering discounts, improved service packages, or
              personalized outreach.
            </>
          ) : (
            <>
              <strong style={{ color: '#27ae60' }}>Low Risk:</strong> This customer has a {probabilityPercent}% probability of churning,
              indicating they are likely to remain. Continue providing quality service to maintain satisfaction.
            </>
          )}
        </p>
      </div>
    </div>
  );
}

export default PredictionResult;
