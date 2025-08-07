from fastapi import FastAPI, HTTPException
from typing import Type
from pydantic import BaseModel
import os, time
import joblib
from datetime import datetime
# Settings
from api.config import MODELS_PATH, MODEL_NAME, MODEL_VERSION, MODEL_FEATURES, ENDPOINT_INPUT_SCHEMA, APP_VERSION
from api.schemas import generate_dynamic_model, PredictionResponse, SalesDataInputSchema
from api.utils import process_input_data

# Instancing API app
app = FastAPI(
    title="Sound Realty's House Price Prediction Service",
    description="API for predicting house prices in Seattle area. Powered by Sound Realty.",
    version=APP_VERSION
)

# Loading pre-trained model
model = joblib.load(os.path.join(MODELS_PATH, MODEL_NAME))

# Input Features Schema
PropertyFeatures: Type[BaseModel] = generate_dynamic_model(ENDPOINT_INPUT_SCHEMA)

# Prediction endpoint
@app.post('/predict', response_model=PredictionResponse)
async def predict_house_price(payload: PropertyFeatures) -> dict: # type: ignore
    start_time = time.time()

    # Select model

    # Processing input data
    processed_data = process_input_data(payload)

    # Making prediction
    try:
        prediction_array = model.predict(processed_data)
        predicted_price = float(prediction_array[0])    

        # Building response
        response = PredictionResponse(
            prediction=round(float(predicted_price), 2),
            timestamp=datetime.now(),
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            metadata={
                'prediction_time_ms': round((time.time() - start_time) * 1000, 2),
                'features_used': MODEL_FEATURES
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return response

# Bonus endpoint to predict based on reduced subset of kc_house_data.csv sales data
@app.post('/predict_bonus', response_model=PredictionResponse)
async def predict_based_on_sales_data(payload: SalesDataInputSchema) -> dict:
    """
    Bonus endpoint to predict house price based on a reduced subset of kc_house_data.csv sales data.
    This endpoint is for demonstration purposes and uses a simplified input schema.
    """
    start_time = time.time()


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