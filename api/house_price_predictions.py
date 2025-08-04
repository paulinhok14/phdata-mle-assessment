from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, create_model
from typing import Optional, Dict, Any
import os, time
import joblib
import pandas as pd
import json, requests
from datetime import datetime

# Path names
file_path = os.path.abspath(__file__)
repo_root = os.path.dirname(os.path.dirname(file_path))
models_path = os.path.join(repo_root, 'model')
data_path = os.path.join(repo_root, 'data')

# Settings
MODEL_NAME = 'model.pkl'
MODEL_VERSION = '0.1.0'
MODEL_FEATURES = json.load(open(os.path.join(models_path, 'model_features.json')))
# Environment Variables if any. Second @param is the default value
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')

# Instancing API app
app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices in Seattle area. Powered by Sound Realty.",
    version="1.0.0"
)

# Loading pre-trained model
model = joblib.load(os.path.join(models_path, MODEL_NAME))

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

# Preprocessing input data
def process_input_data(input_data: dict) -> pd.DataFrame:
    ''' Process input data to match model requirements.'''

    # Filtering initial input data (future_unseen_examples.csv) to match model features
    future_unseen_examples_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'sqft_above', 'sqft_basement', 'zipcode'] # Zipcode is needed only to match geocoords info, it will be dropped.
    df_future_unseen_examples_features = pd.DataFrame(input_data, columns=future_unseen_examples_features)

    # Extracting zipcode from input data
    zipcode = input_data['zipcode']

    # Adding geocoordinates based on zipcode
    try:
        demographic_data = pd.read_csv(os.path.join(data_path, 'zipcode_demographics.csv'))
        zipcode_data = demographic_data[demographic_data['zipcode'] == zipcode]
        if zipcode_data.empty:
            raise ValueError(f"No demographic data found for ZIP code: {zipcode}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading demographic data: {str(e)}")
    
    # Merging Data
    df_full_merged_data = pd.merge(
        left= df_future_unseen_examples_features,
        right=zipcode_data,
        left_on='zipcode',
        right_on='zipcode',
        how='left'
    )   

    return df_full_merged_data



# Prediction endpoint
@app.post('/predict', response_model=PredictionResponse)
async def predict_house_price(input_data: Dict[str, Any]) -> dict:
    start_time = time.time()

    # Processing input data
    processed_data = process_input_data(input_data)
    print(processed_data)

    # Making prediction

    # Building response
    # response = PredictionResponse(
    #        prediction=round(float(prediction), 2),
    #         confidence_score=None,  # Add if model provides it
    #         timestamp=datetime.now(),
    #         model_version=MODEL_VERSION,
    #         features_used=MODEL_FEATURES,
    #         metadata={
    #             "prediction_time_ms": round((time.time() - start_time) * 1000, 2),
    #             # "zipcode_input": property_data.zipcode
    #         }
    #     )
    
    # return response


# Health check endpoint
@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "model_loaded": model is not None
    }



# Creating full URL for Prediction request
url_price_prediction = f"{API_BASE_URL}/predict"

# Test endpoint - Commented out to prevent connection errors during startup
# test_json = {'bedrooms': 3.0, 'bathrooms': 2.5, 'sqft_living': 1560.0, 'sqft_lot': 4800.0, 'floors': 2.0, 'waterfront': 0.0, 'view': 0.0, 'condition': 4.0, 'grade': 7.0, 'sqft_above': 1560.0, 'sqft_basement': 0.0, 'yr_built': 1974.0, 'yr_renovated': 0.0, 'zipcode': 98001.0, 'lat': 47.2653, 'long': -122.285, 'sqft_living15': 1510.0, 
# 'sqft_lot15': 12240.0}
# response = requests.post(url_price_prediction, json=test_json)