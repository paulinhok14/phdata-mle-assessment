import os
import pandas as pd
from typing import Union
from pydantic import BaseModel
from fastapi import HTTPException
# Settings
from api.config import DATA_PATH

# Preprocessing input data
def process_input_data(input_data: Union[BaseModel, dict] ) -> pd.DataFrame:
    ''' Process input data to match model requirements.'''

    # Parsing Pydantic BaseModel input data to dict if it is not already a dict
    if isinstance(input_data, BaseModel):
        input_data = input_data.model_dump()

    # Filtering initial input data (future_unseen_examples.csv) to match model features
    future_unseen_examples_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'sqft_above', 'sqft_basement', 'zipcode'] # Zipcode is needed only to match geocoords info, it will be dropped.
    df_future_unseen_examples_features = pd.DataFrame([input_data], columns=future_unseen_examples_features)

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
        left= df_future_unseen_examples_features,
        right=zipcode_data,
        left_on='zipcode',
        right_on='zipcode',
        how='left'
    )   
    # Debug saving
    debug_path = os.path.join(DATA_PATH, 'debug_processed_input.xlsx')
    df_full_merged_data.to_excel(debug_path, index=False)

    return df_full_merged_data
