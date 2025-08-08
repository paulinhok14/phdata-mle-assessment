import os
import pandas as pd
from typing import Union
from pydantic import BaseModel
from fastapi import HTTPException
# Settings
from api.config import DATA_PATH, MAIN_ENDPOINT_INPUT_SCHEMA, MODEL_REQUIRED_FEATURES

# Preprocessing input data
def process_input_data(input_data: Union[BaseModel, dict] ) -> pd.DataFrame:
    ''' Process input data to match model requirements.'''

    # Parsing Pydantic BaseModel input data to dict if it is not already a dict
    if isinstance(input_data, BaseModel):
        input_data = input_data.model_dump()

    # Filtering initial input data (future_unseen_examples.csv) to match model features
    df_future_unseen_examples_features = pd.DataFrame([input_data], columns=MAIN_ENDPOINT_INPUT_SCHEMA)

    # Extracting zipcode from input data
    zipcode = input_data['zipcode']

    # Adding geocoordinates based on zipcode
    try:
        demographic_data = pd.read_csv(os.path.join(DATA_PATH, 'zipcode_demographics.csv'))
        zipcode_data = demographic_data[demographic_data['zipcode'] == zipcode]
        if zipcode_data.empty:
            raise ValueError(f"No demographic data found for ZIP code: {zipcode}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading demographic data: {str(e)}")
    
    # Merging Data
    df_full_merged_data = pd.merge(
        left=df_future_unseen_examples_features,
        right=zipcode_data,
        left_on='zipcode',
        right_on='zipcode',
        how='left'
    )   

    # Getting only required columns for model predicting
    df_full_merged_data = df_full_merged_data[MODEL_REQUIRED_FEATURES]

    return df_full_merged_data


# Processing bonus endpoint data
def process_sales_data(input_data: Union[BaseModel, dict] ) -> pd.DataFrame:
    pass

# TO DO: Batch Processing
def process_batch_data(batch_size):
    pass