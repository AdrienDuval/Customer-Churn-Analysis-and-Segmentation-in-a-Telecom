from __future__ import annotations
"""
Pydantic models for request and response schemas.
"""
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class Gender(str, Enum):
    """Gender options."""
    MALE = "Male"
    FEMALE = "Female"


class YesNo(str, Enum):
    """Yes/No options for binary categorical features."""
    YES = "Yes"
    NO = "No"


class InternetService(str, Enum):
    """Internet service options."""
    DSL = "DSL"
    FIBER_OPTIC = "Fiber optic"
    NO = "No"


class MultipleLines(str, Enum):
    """Multiple lines options."""
    YES = "Yes"
    NO = "No"
    NO_PHONE_SERVICE = "No phone service"


class Contract(str, Enum):
    """Contract type options."""
    MONTH_TO_MONTH = "Month-to-month"
    ONE_YEAR = "One year"
    TWO_YEAR = "Two year"


class PaymentMethod(str, Enum):
    """Payment method options."""
    BANK_TRANSFER = "Bank transfer (automatic)"
    CREDIT_CARD = "Credit card (automatic)"
    ELECTRONIC_CHECK = "Electronic check"
    MAILED_CHECK = "Mailed check"


class CustomerInput(BaseModel):
    """Input schema for a single customer prediction."""
    Gender: Annotated[Gender, Field(..., description="Customer gender")]
    Senior_Citizen: Annotated[YesNo, Field(..., alias="Senior Citizen", description="Whether customer is a senior citizen")]
    Partner: Annotated[YesNo, Field(..., description="Whether customer has a partner")]
    Dependents: Annotated[YesNo, Field(..., description="Whether customer has dependents")]
    Phone_Service: Annotated[YesNo, Field(..., alias="Phone Service", description="Whether customer has phone service")]
    Multiple_Lines: Annotated[MultipleLines, Field(..., alias="Multiple Lines", description="Multiple lines service")]
    Internet_Service: Annotated[InternetService, Field(..., alias="Internet Service", description="Type of internet service")]
    Online_Security: Annotated[YesNo, Field(..., alias="Online Security", description="Online security service")]
    Online_Backup: Annotated[YesNo, Field(..., alias="Online Backup", description="Online backup service")]
    Device_Protection: Annotated[YesNo, Field(..., alias="Device Protection", description="Device protection service")]
    Tech_Support: Annotated[YesNo, Field(..., alias="Tech Support", description="Tech support service")]
    Streaming_TV: Annotated[YesNo, Field(..., alias="Streaming TV", description="Streaming TV service")]
    Streaming_Movies: Annotated[YesNo, Field(..., alias="Streaming Movies", description="Streaming movies service")]
    Contract: Annotated[Contract, Field(..., description="Contract type")]
    Paperless_Billing: Annotated[YesNo, Field(..., alias="Paperless Billing", description="Paperless billing option")]
    Payment_Method: Annotated[PaymentMethod, Field(..., alias="Payment Method", description="Payment method")]
    Tenure_Months: int = Field(..., ge=0, alias="Tenure Months", description="Number of months customer has been with company")
    Monthly_Charges: float = Field(..., ge=0, alias="Monthly Charges", description="Monthly charges amount")
    Total_Charges: Optional[float] = Field(None, ge=0, alias="Total Charges", description="Total charges amount")
    CLTV: float = Field(..., ge=0, description="Customer Lifetime Value")

    model_config = ConfigDict(
        populate_by_name=True,  # Allows using both field name and alias
        json_schema_extra={
            "example": {
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
        }
    )


class PredictionResult(BaseModel):
    """Single prediction result."""
    churn_prediction: int = Field(..., description="Predicted churn (0 = No, 1 = Yes)")
    churn_probability: float = Field(..., ge=0, le=1, description="Probability of churn (0-1)")
    churn_label: str = Field(..., description="Human-readable churn prediction")
    
    @classmethod
    def create(cls, prediction: int, probability: float):
        """Create a PredictionResult with automatically computed label."""
        return cls(
            churn_prediction=prediction,
            churn_probability=probability,
            churn_label="Yes" if prediction == 1 else "No"
        )


class BatchPredictionRequest(BaseModel):
    """Request schema for batch predictions."""
    customers: List[CustomerInput] = Field(..., min_items=1, description="List of customers to predict")


class BatchPredictionResult(BaseModel):
    """Result for a single customer in batch prediction."""
    customer_index: int = Field(..., description="Index of customer in input list")
    input: CustomerInput = Field(..., description="Original customer input")
    prediction: PredictionResult = Field(..., description="Prediction result")


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions."""
    total_customers: int = Field(..., description="Total number of customers processed")
    predictions: List[BatchPredictionResult] = Field(..., description="List of predictions")
    page: Optional[int] = Field(None, ge=1, description="Current page number (if paginated)")
    page_size: Optional[int] = Field(None, ge=1, description="Page size (if paginated)")
    total_pages: Optional[int] = Field(None, ge=1, description="Total number of pages (if paginated)")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
