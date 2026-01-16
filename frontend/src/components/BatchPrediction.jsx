import React, { useState, useEffect } from 'react';
import apiService from '../api/apiService';
import BatchPredictionResults from './BatchPredictionResults';

const SAMPLE_JSON = {
  "customers": [
    {
      "Gender": "Male",
      "Senior Citizen": "No",
      "Partner": "Yes",
      "Dependents": "No",
      "Phone Service": "Yes",
      "Multiple Lines": "No",
      "Internet Service": "Fiber optic",
      "Online Security": "No",
      "Online Backup": "Yes",
      "Device Protection": "No",
      "Tech Support": "No",
      "Streaming TV": "Yes",
      "Streaming Movies": "Yes",
      "Contract": "Month-to-month",
      "Paperless Billing": "Yes",
      "Payment Method": "Electronic check",
      "Tenure Months": 5,
      "Monthly Charges": 89.5,
      "Total Charges": 450.2,
      "CLTV": 3200
    },
    {
      "Gender": "Female",
      "Senior Citizen": "Yes",
      "Partner": "No",
      "Dependents": "No",
      "Phone Service": "Yes",
      "Multiple Lines": "Yes",
      "Internet Service": "DSL",
      "Online Security": "Yes",
      "Online Backup": "Yes",
      "Device Protection": "Yes",
      "Tech Support": "Yes",
      "Streaming TV": "No",
      "Streaming Movies": "No",
      "Contract": "Two year",
      "Paperless Billing": "No",
      "Payment Method": "Credit card (automatic)",
      "Tenure Months": 45,
      "Monthly Charges": 65.8,
      "Total Charges": 2961,
      "CLTV": 5800
    },
    {
      "Gender": "Male",
      "Senior Citizen": "No",
      "Partner": "No",
      "Dependents": "Yes",
      "Phone Service": "No",
      "Multiple Lines": "No phone service",
      "Internet Service": "Fiber optic",
      "Online Security": "No",
      "Online Backup": "No",
      "Device Protection": "No",
      "Tech Support": "No",
      "Streaming TV": "Yes",
      "Streaming Movies": "Yes",
      "Contract": "Month-to-month",
      "Paperless Billing": "Yes",
      "Payment Method": "Electronic check",
      "Tenure Months": 2,
      "Monthly Charges": 95.5,
      "Total Charges": 191,
      "CLTV": 2100
    },
    {
      "Gender": "Female",
      "Senior Citizen": "No",
      "Partner": "Yes",
      "Dependents": "Yes",
      "Phone Service": "Yes",
      "Multiple Lines": "Yes",
      "Internet Service": "DSL",
      "Online Security": "Yes",
      "Online Backup": "No",
      "Device Protection": "Yes",
      "Tech Support": "No",
      "Streaming TV": "No",
      "Streaming Movies": "No",
      "Contract": "One year",
      "Paperless Billing": "Yes",
      "Payment Method": "Bank transfer (automatic)",
      "Tenure Months": 24,
      "Monthly Charges": 72.3,
      "Total Charges": 1735.2,
      "CLTV": 4200
    },
    {
      "Gender": "Male",
      "Senior Citizen": "Yes",
      "Partner": "Yes",
      "Dependents": "No",
      "Phone Service": "Yes",
      "Multiple Lines": "No",
      "Internet Service": "No",
      "Online Security": "No internet service",
      "Online Backup": "No internet service",
      "Device Protection": "No internet service",
      "Tech Support": "No internet service",
      "Streaming TV": "No internet service",
      "Streaming Movies": "No internet service",
      "Contract": "Two year",
      "Paperless Billing": "No",
      "Payment Method": "Mailed check",
      "Tenure Months": 60,
      "Monthly Charges": 20.15,
      "Total Charges": 1209,
      "CLTV": 3500
    },
    {
      "Gender": "Female",
      "Senior Citizen": "No",
      "Partner": "No",
      "Dependents": "No",
      "Phone Service": "Yes",
      "Multiple Lines": "No",
      "Internet Service": "Fiber optic",
      "Online Security": "Yes",
      "Online Backup": "Yes",
      "Device Protection": "Yes",
      "Tech Support": "Yes",
      "Streaming TV": "Yes",
      "Streaming Movies": "Yes",
      "Contract": "One year",
      "Paperless Billing": "Yes",
      "Payment Method": "Credit card (automatic)",
      "Tenure Months": 12,
      "Monthly Charges": 105.65,
      "Total Charges": 1267.8,
      "CLTV": 4500
    }
  ]
};

function BatchPrediction({ selectedModel }) {
  const [jsonInput, setJsonInput] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-load sample data on component mount
  useEffect(() => {
    setJsonInput(JSON.stringify(SAMPLE_JSON, null, 2));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      let customers;
      try {
        const parsed = JSON.parse(jsonInput);
        // Handle both wrapped format with "customers" key and direct array
        if (parsed.customers && Array.isArray(parsed.customers)) {
          customers = parsed.customers;
        } else if (Array.isArray(parsed)) {
          customers = parsed;
        } else {
          // Single object - wrap in array
          customers = [parsed];
        }
      } catch (parseError) {
        throw new Error('Invalid JSON format. Please check your syntax.');
      }

      if (!Array.isArray(customers) || customers.length === 0) {
        throw new Error('Please provide at least one customer object.');
      }

      if (customers.length > 10000) {
        throw new Error('Maximum 10,000 customers allowed per batch.');
      }

      const prediction = await apiService.predictBatch(customers, selectedModel);
      setResults(prediction);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const loadSampleData = () => {
    setJsonInput(JSON.stringify(SAMPLE_JSON, null, 2));
    setError(null);
  };

  const clearInput = () => {
    setJsonInput('');
    setResults(null);
    setError(null);
  };

  return (
    <div>
      <h3>Prediction</h3>
      <div className="json-helper" style={{ marginBottom: '16px' }}>
        <strong>📋 JSON Format:</strong> Paste your customer data in JSON format. 
        Accepts either a "customers" array or a direct array of customer objects. 
        Sample data is pre-loaded for you.
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label style={{ fontSize: '13px', marginBottom: '8px', display: 'block', fontWeight: '600', color: '#3498db' }}>
            📄 JSON Input Field
          </label>
          <textarea
            className="batch-input"
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
            placeholder='Paste your JSON here. Example format: {"customers": [{"Gender": "Male", "Senior Citizen": "No", ...}]}'
            required
            spellCheck={false}
            style={{ 
              minHeight: '450px',
              fontSize: '13px',
              fontFamily: 'monospace'
            }}
          />
          {jsonInput && (
            <div style={{ marginTop: '8px', fontSize: '11px', color: '#27ae60' }}>
              ✓ {jsonInput.split('\n').length} lines loaded
            </div>
          )}
        </div>

        <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
          <button type="submit" className="btn btn-primary" disabled={loading || !jsonInput.trim()}>
            {loading ? '⏳ Processing...' : '🚀 Predict'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={loadSampleData}>
            📥 Load Sample
          </button>
          <button type="button" className="btn btn-secondary" onClick={clearInput}>
            🗑️ Clear
          </button>
        </div>
      </form>

      {error && <div className="error">❌ Error: {error}</div>}
      {results && <BatchPredictionResults results={results} />}
    </div>
  );
}

export default BatchPrediction;
