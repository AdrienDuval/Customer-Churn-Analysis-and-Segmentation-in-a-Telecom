import React, { useState } from 'react';
import apiService from '../api/apiService';
import PredictionResult from './PredictionResult';

const initialFormData = {
  Gender: 'Male',
  'Senior Citizen': 'No',
  Partner: 'Yes',
  Dependents: 'No',
  'Phone Service': 'Yes',
  'Multiple Lines': 'No',
  'Internet Service': 'Fiber optic',
  'Online Security': 'No',
  'Online Backup': 'Yes',
  'Device Protection': 'No',
  'Tech Support': 'No',
  'Streaming TV': 'Yes',
  'Streaming Movies': 'Yes',
  Contract: 'Month-to-month',
  'Paperless Billing': 'Yes',
  'Payment Method': 'Electronic check',
  'Tenure Months': 5,
  'Monthly Charges': 89.5,
  'Total Charges': 450.2,
  CLTV: 3200
};

function SinglePrediction({ selectedModel }) {
  const [formData, setFormData] = useState(initialFormData);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: field.includes('Months') || field.includes('Charges') || field === 'CLTV' 
        ? (value === '' ? '' : parseFloat(value)) 
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const prediction = await apiService.predictSingle(formData, selectedModel);
      setResult(prediction);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const loadSampleData = async () => {
    try {
      const sampleData = await apiService.getSampleData();
      if (sampleData.customers && sampleData.customers.length > 0) {
        setFormData(sampleData.customers[0]);
      }
    } catch (err) {
      setError('Failed to load sample data');
    }
  };

  return (
    <div>
      <h3>Single Prediction</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>Gender</label>
            <select
              value={formData.Gender}
              onChange={(e) => handleInputChange('Gender', e.target.value)}
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          <div className="form-group">
            <label>Senior Citizen</label>
            <select
              value={formData['Senior Citizen']}
              onChange={(e) => handleInputChange('Senior Citizen', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </div>

          <div className="form-group">
            <label>Partner</label>
            <select
              value={formData.Partner}
              onChange={(e) => handleInputChange('Partner', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </div>

          <div className="form-group">
            <label>Dependents</label>
            <select
              value={formData.Dependents}
              onChange={(e) => handleInputChange('Dependents', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </div>

          <div className="form-group">
            <label>Phone Service</label>
            <select
              value={formData['Phone Service']}
              onChange={(e) => handleInputChange('Phone Service', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </div>

          <div className="form-group">
            <label>Multiple Lines</label>
            <select
              value={formData['Multiple Lines']}
              onChange={(e) => handleInputChange('Multiple Lines', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No phone service">No phone service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Internet Service</label>
            <select
              value={formData['Internet Service']}
              onChange={(e) => handleInputChange('Internet Service', e.target.value)}
            >
              <option value="DSL">DSL</option>
              <option value="Fiber optic">Fiber optic</option>
              <option value="No">No</option>
            </select>
          </div>

          <div className="form-group">
            <label>Online Security</label>
            <select
              value={formData['Online Security']}
              onChange={(e) => handleInputChange('Online Security', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Online Backup</label>
            <select
              value={formData['Online Backup']}
              onChange={(e) => handleInputChange('Online Backup', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Device Protection</label>
            <select
              value={formData['Device Protection']}
              onChange={(e) => handleInputChange('Device Protection', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Tech Support</label>
            <select
              value={formData['Tech Support']}
              onChange={(e) => handleInputChange('Tech Support', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Streaming TV</label>
            <select
              value={formData['Streaming TV']}
              onChange={(e) => handleInputChange('Streaming TV', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Streaming Movies</label>
            <select
              value={formData['Streaming Movies']}
              onChange={(e) => handleInputChange('Streaming Movies', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          <div className="form-group">
            <label>Contract</label>
            <select
              value={formData.Contract}
              onChange={(e) => handleInputChange('Contract', e.target.value)}
            >
              <option value="Month-to-month">Month-to-month</option>
              <option value="One year">One year</option>
              <option value="Two year">Two year</option>
            </select>
          </div>

          <div className="form-group">
            <label>Paperless Billing</label>
            <select
              value={formData['Paperless Billing']}
              onChange={(e) => handleInputChange('Paperless Billing', e.target.value)}
            >
              <option value="No">No</option>
              <option value="Yes">Yes</option>
            </select>
          </div>

          <div className="form-group">
            <label>Payment Method</label>
            <select
              value={formData['Payment Method']}
              onChange={(e) => handleInputChange('Payment Method', e.target.value)}
            >
              <option value="Bank transfer (automatic)">Bank transfer (automatic)</option>
              <option value="Credit card (automatic)">Credit card (automatic)</option>
              <option value="Electronic check">Electronic check</option>
              <option value="Mailed check">Mailed check</option>
            </select>
          </div>

          <div className="form-group">
            <label>Tenure Months</label>
            <input
              type="number"
              value={formData['Tenure Months']}
              onChange={(e) => handleInputChange('Tenure Months', e.target.value)}
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label>Monthly Charges</label>
            <input
              type="number"
              step="0.01"
              value={formData['Monthly Charges']}
              onChange={(e) => handleInputChange('Monthly Charges', e.target.value)}
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label>Total Charges</label>
            <input
              type="number"
              step="0.01"
              value={formData['Total Charges'] || ''}
              onChange={(e) => handleInputChange('Total Charges', e.target.value)}
              min="0"
            />
          </div>

          <div className="form-group">
            <label>CLTV (Customer Lifetime Value)</label>
            <input
              type="number"
              step="0.01"
              value={formData.CLTV}
              onChange={(e) => handleInputChange('CLTV', e.target.value)}
              min="0"
              required
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Processing...' : 'Run Prediction'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={loadSampleData}>
            Load Sample
          </button>
        </div>
      </form>

      {error && <div className="error">Error: {error}</div>}
      {result && <PredictionResult result={result} />}
    </div>
  );
}

export default SinglePrediction;
