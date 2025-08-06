from pydantic import BaseModel, Field, create_model
from typing import Optional, Dict, Any
from datetime import datetime
# Settings
from api.config import MODEL_NAME, MODEL_VERSION

# Dynamic Model creating in order to have scalability without liability
def generate_dynamic_model(features: list) -> BaseModel:
    fields = {feature: (Optional[float], ...) for feature in features}
    return create_model("PropertyFeatures", **fields)

# Response Model
class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted house price in USD")
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")
    model_name: str = Field(default=MODEL_NAME, description="Model name used to prediction")
    model_version: str = Field(default=MODEL_VERSION, description="Model version used")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")