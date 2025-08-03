from fastapi import FastAPI
from pydantic import BaseModel


# Instancing API app
app = FastAPI()


@app.post('/predict')
async def predict_house_price():
    pass