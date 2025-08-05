from fastapi import FastAPI, HTTPException
from schemas import PropertyFeatures, PredictionResponse
from typing import Type
from pydantic import BaseModel
import os, time
import joblib
import pandas as pd
from datetime import datetime
# Settings
from config import MODELS_PATH, MODEL_NAME, MODEL_FEATURES, API_BASE_URL
from schemas import generate_dynamic_model
from utils import process_input_data

# Instancing API app
app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices in Seattle area. Powered by Sound Realty.",
    version="1.0.0"
)

# Loading pre-trained model
model = joblib.load(os.path.join(MODELS_PATH, MODEL_NAME))

# Input Features Schema
PropertyFeatures: Type[BaseModel] = generate_dynamic_model(MODEL_FEATURES)

# Prediction endpoint
@app.post('/predict', response_model=PredictionResponse)
async def predict_house_price(input_data: PropertyFeatures) -> dict: # type: ignore
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