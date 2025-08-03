from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os, time
import joblib
import pandas as pd
import json
from datetime import datetime

# Path names
file_path = os.path.abspath(__file__)
repo_root = os.path.dirname(os.path.dirname(file_path))
models_path = os.path.join(repo_root, 'model')
data_path = os.path.join(repo_root, 'data')

# Settings
MODEL_NAME = 'model.pkl'
MODEL_VERSION = ''
MODEL_FEATURES = json.load(open(os.path.join(models_path, 'model_features.json')))

# Instancing API app
app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices in Seattle area. Powered by Sound Realty.",
    version="1.0.0"
)

# Loading pre-trained model
model = joblib.load(os.path.join(models_path, MODEL_NAME))

# Input Features Model
class PropertyFeatures(BaseModel):
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms")
    bathrooms: float = Field(..., ge=0, description="Number of bathrooms")
    sqft_living: int = Field(..., gt=0, description="Square footage of living space")
    sqft_lot: int = Field(..., gt=0, description="Square footage of lot")
    floors: float = Field(..., ge=0, description="Number of floors")
    sqft_above: int = Field(..., ge=0, description="Square footage above ground")
    sqft_basement: int = Field(..., ge=0, description="Square footage of basement")
    zipcode: str = Field(..., description="ZIP code of the property")

# Response Model
class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted house price in USD")
    confidence_score: Optional[float] = Field(None, description="Model confidence score (if available)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")
    model_version: str = Field(default="1.0.0", description="Model version used")
    features_used: list = Field(default_factory=list, description="List of features used for prediction")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

# Adding complementary demographic data
def add_complementary_data(zipcode: str) -> pd.DataFrame:
    """Add demographic data for the given ZIP code"""
    try:
        demographic_data = pd.read_csv(os.path.join(data_path, 'zipcode_demographics.csv'))
        zipcode_data = demographic_data[demographic_data['zipcode'] == zipcode]
        if zipcode_data.empty:
            raise ValueError(f"No demographic data found for ZIP code: {zipcode}")
        return zipcode_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading demographic data: {str(e)}")

# Prediction endpoint
@app.post('/predict', response_model=PredictionResponse)
async def predict_house_price():
    start_time = time.time()

    # Making prediction

    # Building response
    response = PredictionResponse(
           # prediction=round(float(prediction), 2),
            #confidence_score=None,  # Add if model provides it
            timestamp=datetime.now(),
            model_version=MODEL_VERSION,
            features_used=MODEL_FEATURES,
            metadata={
                "prediction_time_ms": round((time.time() - start_time) * 1000, 2),
                # "zipcode_input": property_data.zipcode
            }
        )
    
    return response


# Health check endpoint
@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "model_loaded": model is not None
    }

add_complementary_data()