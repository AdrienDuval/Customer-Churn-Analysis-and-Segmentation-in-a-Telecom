"""
Service layer for model loading and prediction logic.
"""
import os
import pickle
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ModelService:
    """Service for loading and using the churn prediction model."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the model service.
        
        Args:
            model_path: Path to the model pickle file. If None, uses default path.
                       Can also be set via MODEL_PATH environment variable.
        """
        if model_path is None:
            # Check environment variable first
            model_path = os.getenv("MODEL_PATH")
            
            if model_path is None:
                # Default path relative to api directory - use v1 LR model
                base_dir = Path(__file__).parent.parent
                model_path = base_dir / "models" / "churn_model_v1_lr.pkl"
        
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the model from pickle file."""
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            logger.info(f"Model successfully loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None
    
    def predict_single(self, customer_data: dict) -> Tuple[int, float]:
        """
        Predict churn for a single customer.
        
        Args:
            customer_data: Dictionary with customer features (keys should have spaces, e.g., "Senior Citizen")
            
        Returns:
            Tuple of (prediction, probability)
            - prediction: 0 or 1 (no churn or churn)
            - probability: Probability of churn (0-1)
        """
        if not self.is_loaded():
            raise RuntimeError("Model is not loaded")
        
        try:
            # Convert to DataFrame - column names should already match (with spaces)
            # The input dict keys should match the training column names exactly
            df = pd.DataFrame([customer_data])
            
            # Ensure column order matches training (important for sklearn pipelines)
            expected_columns = [
                "Gender", "Senior Citizen", "Partner", "Dependents",
                "Phone Service", "Multiple Lines", "Internet Service",
                "Online Security", "Online Backup", "Device Protection",
                "Tech Support", "Streaming TV", "Streaming Movies",
                "Contract", "Paperless Billing", "Payment Method",
                "Tenure Months", "Monthly Charges", "Total Charges", "CLTV"
            ]
            
            # Check for missing columns
            missing_cols = set(expected_columns) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Reorder columns to match training order
            df = df.reindex(columns=expected_columns)
            
            # Get prediction and probability
            prediction = self.model.predict(df)[0]
            probability = self.model.predict_proba(df)[0, 1]
            
            return int(prediction), float(probability)
        
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def predict_batch(
        self, 
        customers_data: List[dict],
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Tuple[List[Tuple[int, float]], int]:
        """
        Predict churn for multiple customers.
        
        Args:
            customers_data: List of customer feature dictionaries
            page: Page number for pagination (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (predictions, total_count)
            - predictions: List of (prediction, probability) tuples
            - total_count: Total number of customers
        """
        if not self.is_loaded():
            raise RuntimeError("Model is not loaded")
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(customers_data)
            
            # Ensure column order matches training (important for sklearn pipelines)
            expected_columns = [
                "Gender", "Senior Citizen", "Partner", "Dependents",
                "Phone Service", "Multiple Lines", "Internet Service",
                "Online Security", "Online Backup", "Device Protection",
                "Tech Support", "Streaming TV", "Streaming Movies",
                "Contract", "Paperless Billing", "Payment Method",
                "Tenure Months", "Monthly Charges", "Total Charges", "CLTV"
            ]
            
            # Check for missing columns
            missing_cols = set(expected_columns) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Reorder columns to match training order
            df = df.reindex(columns=expected_columns)
            
            # Apply pagination if requested
            total_count = len(df)
            if page is not None and page_size is not None:
                start_idx = (page - 1) * page_size
                end_idx = start_idx + page_size
                df = df.iloc[start_idx:end_idx]
            
            # Get predictions and probabilities
            predictions = self.model.predict(df)
            probabilities = self.model.predict_proba(df)[:, 1]
            
            # Combine results
            results = [
                (int(pred), float(prob))
                for pred, prob in zip(predictions, probabilities)
            ]
            
            return results, total_count
        
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error during batch prediction: {str(e)}")
            raise ValueError(f"Batch prediction failed: {str(e)}")


# Global model service instances - one per model
_model_services: dict[str, ModelService] = {}


class ModelManager:
    """Manager for multiple model instances."""
    
    def __init__(self):
        """Initialize the model manager with available models."""
        self.base_dir = Path(__file__).parent.parent
        self.models_dir = self.base_dir / "models"
        self.available_models = {
            "v1_lr": "churn_model_v1_lr.pkl",
            "v2_rf": "churn_model_v2_rf.pkl",
            "v3_gb": "churn_model_v3_gb.pkl"
        }
        self._load_all_models()
    
    def _load_all_models(self):
        """Load all available models."""
        for model_key, model_file in self.available_models.items():
            model_path = self.models_dir / model_file
            if model_path.exists():
                try:
                    service = ModelService(model_path=str(model_path))
                    if service.is_loaded():
                        _model_services[model_key] = service
                        logger.info(f"Model {model_key} loaded successfully")
                    else:
                        logger.warning(f"Model {model_key} failed to load")
                except Exception as e:
                    logger.error(f"Error loading model {model_key}: {str(e)}")
            else:
                logger.warning(f"Model file not found: {model_path}")
    
    def get_model(self, model_version: str = "v1_lr") -> ModelService:
        """
        Get a model service by version.
        
        Args:
            model_version: Model version key (v1_lr, v2_rf, v3_gb)
            
        Returns:
            ModelService instance
            
        Raises:
            ValueError: If model version is not available
        """
        if model_version not in self.available_models:
            raise ValueError(
                f"Unknown model version: {model_version}. "
                f"Available: {list(self.available_models.keys())}"
            )
        
        if model_version not in _model_services:
            # Try to load it
            model_path = self.models_dir / self.available_models[model_version]
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            _model_services[model_version] = ModelService(model_path=str(model_path))
        
        return _model_services[model_version]
    
    def list_models(self) -> dict:
        """List all available models and their status."""
        result = {}
        for model_key in self.available_models.keys():
            is_loaded = model_key in _model_services and _model_services[model_key].is_loaded()
            result[model_key] = {
                "file": self.available_models[model_key],
                "loaded": is_loaded,
                "path": str(self.models_dir / self.available_models[model_key])
            }
        return result


# Global model manager instance
_model_manager: Optional[ModelManager] = None


def get_model_manager() -> ModelManager:
    """Get or create the global model manager instance."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager


def get_model_service(model_path: Optional[str] = None, model_version: Optional[str] = None) -> ModelService:
    """
    Get a model service instance.
    
    Args:
        model_path: Optional path to model file (legacy support)
        model_version: Optional model version (v1_lr, v2_rf, v3_gb)
        
    Returns:
        ModelService instance
    """
    if model_version is not None:
        manager = get_model_manager()
        return manager.get_model(model_version)
    
    if model_path is not None:
        # Create new instance with specified path
        return ModelService(model_path=model_path)
    
    # Default to v1_lr
    manager = get_model_manager()
    return manager.get_model("v1_lr")
