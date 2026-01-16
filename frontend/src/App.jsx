import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ModelSelector from './components/ModelSelector';
import BatchPrediction from './components/BatchPrediction';
import StatusPanel from './components/StatusPanel';
import apiService from './api/apiService';
import './index.css';

function App() {
  const [selectedModel, setSelectedModel] = useState('v1_lr');
  const [models, setModels] = useState({});
  const [healthStatus, setHealthStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInitialData();
    // Refresh health status every 30 seconds
    const interval = setInterval(() => {
      checkHealth();
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [healthData, modelsData] = await Promise.all([
        apiService.getHealth(),
        apiService.getModels()
      ]);
      setHealthStatus(healthData);
      setModels(modelsData.available_models || {});
    } catch (error) {
      console.error('Error loading initial data:', error);
      setHealthStatus({ status: 'unhealthy', model_loaded: false });
    } finally {
      setLoading(false);
    }
  };

  const checkHealth = async () => {
    try {
      const healthData = await apiService.getHealth();
      setHealthStatus(healthData);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({ status: 'unhealthy', model_loaded: false });
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading application...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <Header />
      <StatusPanel healthStatus={healthStatus} />
      <ModelSelector
        selectedModel={selectedModel}
        onModelChange={setSelectedModel}
        models={models}
      />
      <BatchPrediction selectedModel={selectedModel} />
    </div>
  );
}

export default App;
