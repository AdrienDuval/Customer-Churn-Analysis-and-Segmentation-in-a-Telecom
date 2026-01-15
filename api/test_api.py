"""
Simple test script to verify the API setup.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from api.services import get_model_service
    print("✓ Imports successful")
    
    # Test model loading
    try:
        model_service = get_model_service()
        if model_service.is_loaded():
            print("✓ Model loaded successfully")
        else:
            print("✗ Model failed to load")
    except Exception as e:
        print(f"✗ Model loading error: {e}")
    
    # Test sample prediction
    try:
        sample_data = {
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
        
        pred, prob = model_service.predict_single(sample_data)
        print(f"✓ Prediction successful: {pred} (probability: {prob:.3f})")
    except Exception as e:
        print(f"✗ Prediction error: {e}")
        
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
