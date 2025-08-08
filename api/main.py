from fastapi import FastAPI, HTTPException, Query
from typing import Type
from pydantic import BaseModel
import os, time
import joblib
import threading
from datetime import datetime
# Settings
from api.config import MODELS_PATH, MODEL_NAME, MODEL_VERSION, MODEL_REQUIRED_FEATURES, MAIN_ENDPOINT_INPUT_SCHEMA, APP_VERSION, SALES_DATA_FEATURES
from api.schemas import generate_dynamic_model, generate_sales_data_input_schema, PredictionResponse
from api.utils import process_input_data, process_sales_input_data

model_lock = threading.Lock()

# Instancing API app
app = FastAPI(
    title="Sound Realty's House Price Prediction Service",
    description="API for predicting house prices in Seattle area. Powered by Sound Realty.",
    version=APP_VERSION
)

# Loading pre-trained model
model = joblib.load(os.path.join(MODELS_PATH, MODEL_NAME))

# Main Input Features Schema
PropertyFeatures: Type[BaseModel] = generate_dynamic_model(MAIN_ENDPOINT_INPUT_SCHEMA)
SalesDataInputSchema: Type[BaseModel] = generate_sales_data_input_schema(SALES_DATA_FEATURES)

# Prediction endpoint
@app.post('/predict', response_model=PredictionResponse)
async def predict_house_price(payload: PropertyFeatures) -> dict: # type: ignore
    start_time = time.time()

    # Select model

    # Processing input data
    processed_data = process_input_data(payload)

    # Making prediction
    try:
        with model_lock:
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
                'features_used': MODEL_REQUIRED_FEATURES
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return response


# Bonus endpoint to predict based on reduced subset of kc_house_data.csv sales data
@app.post('/predict_bonus', response_model=PredictionResponse)
async def predict_based_on_sales_data(payload: SalesDataInputSchema) -> dict: # type: ignore
    """
    Bonus endpoint to predict house price based on a reduced subset of kc_house_data.csv sales data.
    """
    start_time = time.time()
    
    # Processing Sales Input Data
    processed_data = process_sales_input_data(payload)

    # Making prediction
    try:
        with model_lock:
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
                'features_used': MODEL_REQUIRED_FEATURES
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return response


# Change model endpoint
@app.api_route('/reload_model', methods=['GET', 'POST'])
def reload_model_endpoint(model_name: str = Query(default=MODEL_NAME)) -> dict:
    """
    Endpoint to reload the model from disk at runtime (zero-downtime)
    """
    global model, MODEL_NAME
    model_path = os.path.join(MODELS_PATH, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model file {model_name} not found.")
    with model_lock:
        model = joblib.load(model_path)
        MODEL_NAME = model_name  # Updating global so /health and responses shows correct version with updated model
    return {"status": "reloaded", "model_name": model_name}

        

# Health check endpoint
@app.get('/health')
async def health_check() -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "model_loaded": model is not None,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION
    }