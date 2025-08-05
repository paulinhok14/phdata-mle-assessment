from fastapi import FastAPI
from typing import Type
from pydantic import BaseModel
import os, time
import joblib
import pandas as pd
from datetime import datetime
# Settings
from api.config import MODELS_PATH, MODEL_NAME, MODEL_VERSION, MODEL_FEATURES, ENDPOINT_INPUT_SCHEMA
from api.schemas import generate_dynamic_model, PredictionResponse
from api.utils import process_input_data

# Instancing API app
app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices in Seattle area. Powered by Sound Realty.",
    version="1.0.0"
)

# Loading pre-trained model
model = joblib.load(os.path.join(MODELS_PATH, MODEL_NAME))

# Input Features Schema
PropertyFeatures: Type[BaseModel] = generate_dynamic_model(ENDPOINT_INPUT_SCHEMA)

# Prediction endpoint
@app.post('/predict', response_model=PredictionResponse)
# async def predict_house_price(input_data: PropertyFeatures) -> dict: # type: ignore
async def predict_house_price(input_data: PropertyFeatures): # type: ignore

    start_time = time.time()

    # Processing input data
    processed_data = process_input_data(input_data)

    # Making prediction
    prediction_array = model.predict(processed_data)
    predicted_price = float(prediction_array[0])  # scalar    
    print(predicted_price)

    end_time = time.time()

    # Building response
    response = PredictionResponse(
        prediction=round(float(predicted_price), 2),
        confidence_score=None,  # Add if model provides it
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
        "model_loaded": model is not None,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION
    }