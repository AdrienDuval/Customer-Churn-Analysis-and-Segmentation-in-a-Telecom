# Setup Instructions

## Quick Start with Docker

1. **Ensure models are in the correct location:**
   ```bash
   # Create models directory if it doesn't exist
   mkdir -p models
   
   # Copy model files from notebooks directory (if they exist there)
   # The API expects these files:
   # - models/churn_model_v1_lr.pkl
   # - models/churn_model_v2_rf.pkl
   # - models/churn_model_v3_gb.pkl
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development Setup

### Backend Development

```bash
cd api
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000 and proxy API requests to http://localhost:8000

## Model Files

The API expects model files in the `models/` directory:
- `churn_model_v1_lr.pkl` - Logistic Regression model
- `churn_model_v2_rf.pkl` - Random Forest model
- `churn_model_v3_gb.pkl` - Gradient Boosting model

If your models are in a different location (e.g., `notebooks/`), copy them to the `models/` directory before starting Docker.
