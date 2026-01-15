"""
FastAPI application for Churn Prediction Model.
"""
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import logging
import os
from contextlib import asynccontextmanager

from .models import (
    CustomerInput,
    PredictionResult,
    BatchPredictionRequest,
    BatchPredictionResponse,
    BatchPredictionResult,
    HealthResponse,
    ErrorResponse
)
from .services import get_model_service, get_model_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API version
API_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting up Churn Prediction API...")
    try:
        # Load all models on startup
        manager = get_model_manager()
        loaded_models = [k for k, v in manager.list_models().items() if v["loaded"]]
        logger.info(f"Models loaded successfully: {loaded_models}")
        if not loaded_models:
            logger.warning("No models loaded")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Churn Prediction API...")


# Create FastAPI app
app = FastAPI(
    title="Churn Prediction API",
    description="""
    A FastAPI application for predicting customer churn using a machine learning model.
    
    ## Features
    
    * Single customer prediction
    * Batch prediction with pagination
    * Comprehensive error handling
    * OpenAPI documentation
    
    ## Model
    
    The model is a Logistic Regression classifier trained on customer data with:
    - 20 features (4 numeric, 16 categorical)
    - Balanced class weights for better recall
    - Preprocessing pipeline with imputation and encoding
    """,
    version=API_VERSION,
    lifespan=lifespan,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    }
)

# Add CORS middleware
# Get allowed origins from environment variable, default to all for development
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # In production, set CORS_ORIGINS env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid input",
            "detail": str(exc),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
    )


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request, exc):
    """Handle RuntimeError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Model error",
            "detail": str(exc),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )


# Routes
@app.get(
    "/",
    tags=["General"],
    summary="Root endpoint",
    description="Returns API information"
)
async def root():
    """Root endpoint."""
    return {
        "message": "Churn Prediction API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["General"],
    summary="Health check",
    description="Check API and model status"
)
async def health_check():
    """Health check endpoint."""
    try:
        model_service = get_model_service()
        model_loaded = model_service.is_loaded()
        
        return HealthResponse(
            status="healthy" if model_loaded else "degraded",
            model_loaded=model_loaded,
            version=API_VERSION
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            version=API_VERSION
        )


@app.get(
    "/models",
    tags=["General"],
    summary="List all available models",
    description="Get information about all available models"
)
async def list_models():
    """List all available models and their status."""
    try:
        manager = get_model_manager()
        return {
            "available_models": manager.list_models(),
            "default_model": "v1_lr"
        }
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving model information"
        )


@app.get(
    "/sample-data",
    tags=["General"],
    summary="Get sample customer data",
    description="Returns sample customer data in ready-to-use format for batch predictions. Copy and paste directly into /predict/batch endpoint."
)
async def get_sample_data():
    """Get sample customer data in wrapped format ready for batch predictions."""
    import json
    from pathlib import Path
    
    try:
        # Load sample data from file
        base_dir = Path(__file__).parent.parent
        sample_file = base_dir / "sample_data.json"
        
        if sample_file.exists():
            with open(sample_file, 'r') as f:
                sample_data = json.load(f)
            # Return in wrapped format ready for batch endpoint
            return {
                "customers": sample_data
            }
        else:
            # Return a single example if file doesn't exist
            return {
                "customers": [{
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
                }]
            }
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error loading sample data"
        )


@app.get(
    "/model/info",
    tags=["General"],
    summary="Model information",
    description="Get information about a specific model (default: v1_lr)"
)
async def model_info(model_version: str = Query("v1_lr", description="Model version: v1_lr, v2_rf, or v3_gb")):
    """Get information about a specific model."""
    try:
        model_service = get_model_service(model_version=model_version)
        if not model_service.is_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model {model_version} is not loaded"
            )
        
        return {
            "model_version": model_version,
            "model_path": str(model_service.model_path),
            "model_loaded": True,
            "model_type": type(model_service.model).__name__
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving model information"
        )


@app.post(
    "/predict",
    response_model=PredictionResult,
    tags=["Predictions"],
    summary="Single prediction (default model)",
    description="Predict churn for a single customer using default model (v1_lr)",
    responses={
        200: {"description": "Successful prediction"},
        400: {"description": "Invalid input data"},
        500: {"description": "Model prediction error"}
    }
)
async def predict_single(
    customer: CustomerInput,
    model_version: str = Query("v1_lr", description="Model version: v1_lr, v2_rf, or v3_gb")
):
    """
    Predict churn for a single customer.
    
    Returns:
    - churn_prediction: 0 (No churn) or 1 (Churn)
    - churn_probability: Probability of churn (0-1)
    - churn_label: "Yes" or "No"
    """
    try:
        model_service = get_model_service(model_version=model_version)
        
        if not model_service.is_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model {model_version} is not loaded"
            )
        
        # Convert Pydantic model to dict
        customer_dict = customer.model_dump(by_alias=True)
        
        # Make prediction
        prediction, probability = model_service.predict_single(customer_dict)
        
        return PredictionResult(
            churn_prediction=prediction,
            churn_probability=probability,
            churn_label="Yes" if prediction == 1 else "No"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during prediction"
        )


# Model-specific endpoints
@app.post(
    "/predict/v1_lr",
    response_model=PredictionResult,
    tags=["Predictions"],
    summary="Single prediction (Logistic Regression)",
    description="Predict churn using Logistic Regression model (v1_lr)"
)
async def predict_v1_lr(customer: CustomerInput):
    """Predict churn using Logistic Regression model."""
    return await predict_single(customer, model_version="v1_lr")


@app.post(
    "/predict/v2_rf",
    response_model=PredictionResult,
    tags=["Predictions"],
    summary="Single prediction (Random Forest)",
    description="Predict churn using Random Forest model (v2_rf)"
)
async def predict_v2_rf(customer: CustomerInput):
    """Predict churn using Random Forest model."""
    return await predict_single(customer, model_version="v2_rf")


@app.post(
    "/predict/v3_gb",
    response_model=PredictionResult,
    tags=["Predictions"],
    summary="Single prediction (Gradient Boosting)",
    description="Predict churn using Gradient Boosting model (v3_gb)"
)
async def predict_v3_gb(customer: CustomerInput):
    """Predict churn using Gradient Boosting model."""
    return await predict_single(customer, model_version="v3_gb")


@app.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    tags=["Predictions"],
    summary="Batch prediction",
    description="Predict churn for multiple customers with optional pagination",
    responses={
        200: {"description": "Successful batch prediction"},
        400: {"description": "Invalid input data"},
        500: {"description": "Model prediction error"}
    }
)
async def predict_batch(
    request: BatchPredictionRequest,
    page: Optional[int] = Query(
        None,
        ge=1,
        description="Page number (1-indexed). If not provided, returns all results."
    ),
    page_size: Optional[int] = Query(
        None,
        ge=1,
        le=1000,
        description="Number of items per page (max 1000). If not provided, returns all results."
    ),
    model_version: str = Query("v1_lr", description="Model version: v1_lr, v2_rf, or v3_gb")
):
    # Validate batch size
    if len(request.customers) > 10000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch size too large. Maximum 10000 customers allowed, got {len(request.customers)}"
        )
    """
    Predict churn for multiple customers.
    
    Supports pagination:
    - If both `page` and `page_size` are provided, results are paginated
    - If either is missing, all results are returned
    
    Returns:
    - total_customers: Total number of customers processed
    - predictions: List of prediction results
    - page, page_size, total_pages: Pagination info (if paginated)
    """
    try:
        model_service = get_model_service(model_version=model_version)
        
        if not model_service.is_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model {model_version} is not loaded"
            )
        
        # Convert Pydantic models to dicts
        customers_data = [
            customer.model_dump(by_alias=True)
            for customer in request.customers
        ]
        
        # Make batch prediction
        predictions, total_count = model_service.predict_batch(
            customers_data,
            page=page,
            page_size=page_size
        )
        
        # Calculate pagination info
        total_pages = None
        if page is not None and page_size is not None:
            total_pages = (total_count + page_size - 1) // page_size
        
        # Build response
        results = []
        start_idx = 0
        if page is not None and page_size is not None:
            start_idx = (page - 1) * page_size
        
        for idx, (pred, prob) in enumerate(predictions):
            customer_idx = start_idx + idx
            results.append(
                BatchPredictionResult(
                    customer_index=customer_idx,
                    input=request.customers[customer_idx],
                    prediction=PredictionResult.create(pred, prob)
                )
            )
        
        return BatchPredictionResponse(
            total_customers=total_count,
            predictions=results,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during batch prediction"
        )


@app.post(
    "/predict/batch/simple",
    tags=["Predictions"],
    summary="Simple batch prediction (JSON array)",
    description="Alternative endpoint that accepts a JSON array directly",
    response_model=List[PredictionResult]
)
async def predict_batch_simple(
    customers: List[CustomerInput],
    model_version: str = Query("v1_lr", description="Model version: v1_lr, v2_rf, or v3_gb")
):
    """
    Simple batch prediction endpoint that accepts a JSON array.
    
    This is an alternative to /predict/batch that accepts a simple array
    of customer objects without pagination.
    """
    # Validate batch size
    if len(customers) > 10000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch size too large. Maximum 10000 customers allowed, got {len(customers)}"
        )
    
    try:
        model_service = get_model_service(model_version=model_version)
        
        if not model_service.is_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model {model_version} is not loaded"
            )
        
        # Convert to dicts
        customers_data = [
            customer.model_dump(by_alias=True)
            for customer in customers
        ]
        
        # Make predictions
        predictions, _ = model_service.predict_batch(customers_data)
        
        # Build response
        results = [
            PredictionResult.create(pred, prob)
            for pred, prob in predictions
        ]
        
        return results
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during batch prediction"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, reload=True)
