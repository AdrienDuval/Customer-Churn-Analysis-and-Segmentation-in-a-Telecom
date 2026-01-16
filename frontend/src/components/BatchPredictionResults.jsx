import React from 'react';

function BatchPredictionResults({ results }) {
  const { predictions, total_customers, page, page_size, total_pages } = results;
  const churnCount = predictions.filter(p => p.prediction.churn_prediction === 1).length;
  const noChurnCount = total_customers - churnCount;

  return (
    <div className="result-card" style={{ marginTop: '20px' }}>
      <h4>Results</h4>
      <div className="status-info" style={{ marginBottom: '16px', padding: '12px', background: '#ebf5fb', borderRadius: '4px' }}>
        <div className="status-info-item">
          <strong>Total:</strong>
          <span style={{ color: '#2c3e50', fontWeight: '600' }}>{total_customers} customers</span>
        </div>
        <div className="status-info-item">
          <strong>Churn:</strong>
          <span className="status-badge status-churn">{churnCount}</span>
        </div>
        <div className="status-info-item">
          <strong>No Churn:</strong>
          <span className="status-badge status-no-churn">{noChurnCount}</span>
        </div>
        {page && page_size && (
          <div className="status-info-item">
            <strong>Page:</strong>
            <span style={{ color: '#3498db', fontWeight: '600' }}>{page} of {total_pages || 1}</span>
          </div>
        )}
      </div>

      <div style={{ maxHeight: '500px', overflowY: 'auto', border: '1px solid #e1e8ed', borderRadius: '4px' }}>
        <table className="predictions-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Prediction</th>
              <th>Probability</th>
              <th>Risk</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((pred, idx) => {
              const prob = pred.prediction.churn_probability;
              const probPercent = (prob * 100).toFixed(1);
              const riskLevel = prob > 0.7 ? 'High' : prob > 0.4 ? 'Medium' : 'Low';
              
              return (
                <tr key={idx} style={{ 
                  background: idx % 2 === 0 ? '#ffffff' : '#f8f9fa'
                }}>
                  <td style={{ fontWeight: '600', color: '#3498db' }}>{pred.customer_index + 1}</td>
                  <td>
                    <span className={`status-badge ${pred.prediction.churn_prediction === 1 ? 'status-churn' : 'status-no-churn'}`}>
                      {pred.prediction.churn_label}
                    </span>
                  </td>
                  <td style={{ fontWeight: '600', color: prob > 0.5 ? '#e74c3c' : '#27ae60' }}>
                    {probPercent}%
                  </td>
                  <td>
                    <span className={`status-badge ${
                      riskLevel === 'High' ? 'status-churn' : 
                      riskLevel === 'Medium' ? 'status-degraded' : 
                      'status-no-churn'
                    }`}>
                      {riskLevel}
                    </span>
                  </td>
                  <td style={{ fontSize: '11px', color: '#5a6c7d' }}>
                    {pred.input.Gender}, {pred.input['Senior Citizen']}, Tenure: {pred.input['Tenure Months']}mo
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="notes-section" style={{ marginTop: '16px' }}>
        <h4>Summary</h4>
        <p>
          <strong>Analysis:</strong> Out of {total_customers} customers, <span style={{ color: '#e74c3c', fontWeight: '600' }}>{churnCount}</span> ({((churnCount / total_customers) * 100).toFixed(1)}%) are predicted to churn.
        </p>
        <p style={{ marginTop: '6px' }}>
          <strong>Recommendation:</strong> Focus retention efforts on <span style={{ color: '#e74c3c', fontWeight: '600' }}>High</span> and <span style={{ color: '#f39c12', fontWeight: '600' }}>Medium</span> risk customers. 
          Consider segmenting by risk level and applying targeted retention strategies.
        </p>
      </div>
    </div>
  );
}

export default BatchPredictionResults;
