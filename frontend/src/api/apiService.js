import axios from 'axios';

// In Docker, use /api which will be proxied to the backend
// In development, use the direct backend URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (window.location.hostname === 'localhost' && window.location.port === '3000' 
    ? 'http://localhost:8000' 
    : '/api');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async getHealth() {
    const response = await api.get('/health');
    return response.data;
  },

  // Get available models
  async getModels() {
    const response = await api.get('/models');
    return response.data;
  },

  // Get model info
  async getModelInfo(modelVersion) {
    const response = await api.get(`/model/info?model_version=${modelVersion}`);
    return response.data;
  },

  // Get sample data
  async getSampleData() {
    const response = await api.get('/sample-data');
    return response.data;
  },

  // Single prediction
  async predictSingle(customerData, modelVersion = 'v1_lr') {
    const response = await api.post(`/predict/${modelVersion}`, customerData);
    return response.data;
  },

  // Batch prediction
  async predictBatch(customers, modelVersion = 'v1_lr') {
    const response = await api.post(`/predict/batch?model_version=${modelVersion}`, {
      customers: customers
    });
    return response.data;
  },
};

export default apiService;
