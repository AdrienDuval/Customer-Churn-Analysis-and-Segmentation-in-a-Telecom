# Data Science Project  
## Customer Churn Analysis and Segmentation in a Telecom / SaaS Context

## Table of Contents

- [Quick Start](#quick-start) ⚡
- [API Documentation](#api-documentation)
- [Context and Business Background](#1-context-and-business-background)
- [Problem Statement](#2-problem-statement)
- [Dataset Description](#3-dataset-description)

---

## 1. Context and Business Background {#1-context-and-business-background}

Telecom and SaaS companies operate on a **subscription-based business model**, where recurring revenue depends on customers staying over time.

When a customer leaves the company (a phenomenon known as **customer churn**):
- future recurring revenue is lost,
- customer acquisition costs are wasted,
- operational and marketing costs increase.

Reducing churn is therefore a **major business priority**, as retaining existing customers is significantly cheaper than acquiring new ones.

This project addresses this challenge using data science techniques to:
1. **Understand different types of customers**, and  
2. **Predict which customers are likely to leave**, so that preventive actions can be taken.

---

## 2. Problem Statement {#2-problem-statement}

The project is structured around the following key business questions:

> **How can a Telecom / SaaS company better understand its customers and predict churn in order to reduce revenue loss and improve retention strategies?**

This problem is approached from two complementary angles:
- **Unsupervised learning** to identify natural customer segments,
- **Supervised learning** to predict customer churn.

---

## 3. Dataset Description {#3-dataset-description}

### 3.1 Dataset Overview

The dataset used is the **Telco Customer Churn dataset**, which contains information about customers of a Telecom/SaaS company.

Key characteristics:
- **7,043 customers**
- **33 variables**
- Mix of **categorical and numerical features**
- Clear churn indicators

Each row represents one customer, with attributes related to:
- demographic information,
- subscription and contract details,
- service usage,
- billing and payment behavior,
- churn outcome.

---

## Quick Start {#quick-start}

### Prerequisites
- Docker installed ([Download Docker](https://www.docker.com/get-started))

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd FinalProject

# Start the API
docker-compose up --build
```

The API will be available at **http://localhost:8000**

---

## API Documentation

### Available Models

The API provides access to three trained models:
- **v1_lr**: Logistic Regression
- **v2_rf**: Random Forest  
- **v3_gb**: Gradient Boosting

### Getting Sample Data

To get sample customer data for testing:

```http
GET /sample-data
```

**Response:**
```json
{
  "message": "Sample customer data",
  "count": 3,
  "data": [
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
    }
  ]
}
```

You can also use the sample data files in the project root:
- `sample_data.json` - Array format (for `/predict/batch/simple`)
- `sample_data_batch.json` - Wrapped format (for `/predict/batch`)

### Prediction Endpoints

#### Single Prediction

```http
POST /predict/v1_lr
POST /predict/v2_rf
POST /predict/v3_gb
```

**Request Body:** Customer data (use data from `/sample-data` endpoint)

**Response:**
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.85,
  "churn_label": "Yes"
}
```

- `churn_prediction`: 0 (No churn) or 1 (Churn)
- `churn_probability`: Probability of churn (0-1)
- `churn_label`: "Yes" or "No"

#### Batch Prediction

```http
POST /predict/batch?model_version=v1_lr
```

**Request Body:**
```json
{
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
      "Total Charges": 2961.0,
      "CLTV": 5800
    }
  ]
}
```

**Response:**
```json
{
  "total_customers": 2,
  "predictions": [
    {
      "customer_index": 0,
      "input": {
        "Gender": "Male",
        "Senior Citizen": "No",
        ...
      },
      "prediction": {
        "churn_prediction": 1,
        "churn_probability": 0.85,
        "churn_label": "Yes"
      }
    },
    {
      "customer_index": 1,
      "input": {
        "Gender": "Female",
        "Senior Citizen": "Yes",
        ...
      },
      "prediction": {
        "churn_prediction": 0,
        "churn_probability": 0.23,
        "churn_label": "No"
      }
    }
  ]
}
```

**Alternative: Simple Batch (Direct Array)**

If you prefer to send an array directly without the wrapper:

```http
POST /predict/batch/simple?model_version=v1_lr
```

**Request Body:** Direct array (same customer objects, but without the `{"customers": [...]}` wrapper)

### Other Endpoints

- `GET /health` - Check API and model status
- `GET /models` - List all available models and their status
- `GET /model/info?model_version=v1_lr` - Get information about a specific model

### Testing the API

1. **Open interactive documentation:**
   - Navigate to http://localhost:8000/docs in your browser
   - This provides a Swagger UI to test all endpoints

2. **Get sample data:**
   ```bash
   curl http://localhost:8000/sample-data
   ```

3. **Make a single prediction:**
   ```bash
   # Use the first customer from sample_data.json
   curl -X POST "http://localhost:8000/predict/v1_lr" \
     -H "Content-Type: application/json" \
     -d '{
       "Gender": "Male",
       "Senior Citizen": "No",
       ...
     }'
   ```

4. **Make batch predictions (multiple customers):**
   ```bash
   # Use sample_data_batch.json (wrapped format)
   curl -X POST "http://localhost:8000/predict/batch?model_version=v1_lr" \
     -H "Content-Type: application/json" \
     -d @sample_data_batch.json
   ```

5. **Or use the interactive docs:**
   - Click on `/sample-data` endpoint to get sample data
   - Copy the entire response (it's already in the correct format)
   - Paste it directly into `/predict/batch?model_version=v1_lr` endpoint
   - For single prediction: Extract one customer object and use `/predict/v1_lr`, `/predict/v2_rf`, or `/predict/v3_gb`

---

## Quick Reference

**Start API:**
```bash
docker-compose up --build
```

**Access API:**
- Interactive docs: http://localhost:8000/docs
- Get sample data: `GET /sample-data`
- Make prediction: `POST /predict/v1_lr` (or v2_rf, v3_gb)

**Sample data files:**
- `sample_data.json` - Array format (for batch/simple endpoint)
- `sample_data_batch.json` - Wrapped format (for batch endpoint)
