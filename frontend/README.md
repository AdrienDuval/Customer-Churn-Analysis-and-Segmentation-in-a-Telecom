# Churn Prediction Frontend

A modern React-based frontend application for the Churn Prediction API.

## Features

- 🎯 **Model Selection**: Easily switch between different ML models (Logistic Regression, Random Forest, Gradient Boosting)
- 📊 **Single Prediction**: Predict churn for individual customers with an intuitive form
- 📦 **Batch Prediction**: Process multiple customers at once with JSON input
- 📈 **Results Display**: Visual representation of predictions with probability bars and risk levels
- 🔍 **Status Monitoring**: Real-time API health and model status
- 📚 **API Documentation**: Direct links to backend API documentation

## Development

### Prerequisites

- Node.js 18+ and npm

### Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Production Build

```bash
npm run build
```

The built files will be in the `dist` directory.

## Docker

The frontend is automatically built and served via Docker when using `docker-compose up`.

The frontend will be available at `http://localhost` (port 80) and automatically proxies API requests to the backend.
