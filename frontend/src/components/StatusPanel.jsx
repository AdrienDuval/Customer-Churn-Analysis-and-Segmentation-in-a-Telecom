import React from 'react';

function StatusPanel({ healthStatus }) {
  if (!healthStatus) return null;

  const getStatusClass = (status) => {
    switch (status) {
      case 'healthy':
        return 'status-healthy';
      case 'degraded':
        return 'status-degraded';
      default:
        return 'status-unhealthy';
    }
  };

  return (
    <div className="card">
      <h2>System Status</h2>
      <div className="status-info">
        <div className="status-info-item">
          <strong>Status:</strong>
          <span className={`status-badge ${getStatusClass(healthStatus.status)}`}>
            {healthStatus.status || 'Unknown'}
          </span>
        </div>
        <div className="status-info-item">
          <strong>Model:</strong>
          <span className={`status-badge ${healthStatus.model_loaded ? 'status-healthy' : 'status-unhealthy'}`}>
            {healthStatus.model_loaded ? 'Loaded' : 'Not Loaded'}
          </span>
        </div>
        {healthStatus.version && (
          <div className="status-info-item">
            <strong>Version:</strong>
            <span>{healthStatus.version}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default StatusPanel;
