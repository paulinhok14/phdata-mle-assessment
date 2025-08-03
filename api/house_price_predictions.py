from fastapi import FastAPI
from pydantic import BaseModel
import os

# Path names
file_path = os.path.abspath(__file__)
print(file_path)

# Instancing API app
app = FastAPI()

# Input Features
class InputFeatures(BaseModel):
    pass


# Adding complementary demographic data
def add_complementary_data():
    pass

# Prediction endpoint
@app.post('/predict')
async def predict_house_price():
    pass

