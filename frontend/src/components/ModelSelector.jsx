import React from 'react';

const MODEL_INFO = {
  v1_lr: {
    name: 'Logistic Regression',
    description: 'Fast and interpretable baseline model'
  },
  v2_rf: {
    name: 'Random Forest',
    description: 'Robust ensemble method with good generalization'
  },
  v3_gb: {
    name: 'Gradient Boosting',
    description: 'High-performance model with excellent accuracy'
  }
};

function ModelSelector({ selectedModel, onModelChange, models }) {
  const availableModels = Object.keys(MODEL_INFO).filter(
    model => models[model]?.loaded !== false
  );

  return (
    <div className="card">
      <h2>Model Selection</h2>
      <div className="model-selector">
        {availableModels.map(model => (
          <div
            key={model}
            className={`model-option ${selectedModel === model ? 'active' : ''}`}
            onClick={() => onModelChange(model)}
          >
            <div className="model-name">{MODEL_INFO[model].name}</div>
            <div className="model-id">{model}</div>
          </div>
        ))}
      </div>
      {MODEL_INFO[selectedModel] && (
        <div className="notes-section">
          <h4>Model Information</h4>
          <p><strong>{MODEL_INFO[selectedModel].name}</strong>: {MODEL_INFO[selectedModel].description}</p>
        </div>
      )}
    </div>
  );
}

export default ModelSelector;
