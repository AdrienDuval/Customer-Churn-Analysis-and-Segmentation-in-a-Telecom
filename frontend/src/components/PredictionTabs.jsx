import React, { useState } from 'react';
import SinglePrediction from './SinglePrediction';
import BatchPrediction from './BatchPrediction';

function PredictionTabs({ selectedModel }) {
  const [activeTab, setActiveTab] = useState('batch');

  return (
    <div className="card">
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'single' ? 'active' : ''}`}
          onClick={() => setActiveTab('single')}
        >
          Single Prediction
        </button>
        <button
          className={`tab ${activeTab === 'batch' ? 'active' : ''}`}
          onClick={() => setActiveTab('batch')}
        >
          Batch Prediction
        </button>
      </div>
      {activeTab === 'single' ? (
        <SinglePrediction selectedModel={selectedModel} />
      ) : (
        <BatchPrediction selectedModel={selectedModel} />
      )}
    </div>
  );
}

export default PredictionTabs;
