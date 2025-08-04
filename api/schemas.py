from pydantic import BaseModel, Field, create_model
from typing import Optional, Dict, Any
import json, os
from datetime import datetime

# Settings
MODEL_NAME = 'model.pkl'
MODEL_VERSION = '0.1.0'
MODEL_FEATURES = json.load(open(os.path.join(models_path, 'model_features.json')))
# Environment Variables if any. Second @param is the default value
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')

# Dynamic Model creating in order to have scalability without liability
def generate_dynamic_model(features: list) -> BaseModel:
    fields = {feature: (Optional[float], ...) for feature in features}
    return create_model("PropertyFeatures", **fields)

# Input Features Model
PropertyFeatures = generate_dynamic_model(MODEL_FEATURES)

# Response Model
class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted house price in USD")
    confidence_score: Optional[float] = Field(None, description="Model confidence score (if available)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")
    model_version: str = Field(default="1.0.0", description="Model version used")
    features_used: list = Field(default_factory=list, description="List of features used for prediction")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")