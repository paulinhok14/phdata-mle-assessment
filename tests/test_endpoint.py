# Get random data examples from data/future_unseen_examples.csv and send to API endpoint for service demonstration 
import pandas as pd
import os, sys
import requests
# Adding the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Settings
from api.config import API_BASE_URL, DATA_PATH


# Read and return random input samples
def read_csv_random_input_samples(n_samples: int = 5) -> pd.DataFrame:
    df_future_unseen_examples = pd.read_csv(os.path.join(DATA_PATH, 'future_unseen_examples.csv'))
    df_random_unseen_examples = df_future_unseen_examples.sample(n=min(n_samples, len(df_future_unseen_examples)), random_state=42)
    
    return df_random_unseen_examples

# Requesting predictions from the API
def predict_property_price(property_data: dict) -> dict:
    
    # Creating full URL for Prediction request
    url_price_prediction = f"{API_BASE_URL}/predict"

    # Requesting Property Predicted Price
    response = requests.post(url=url_price_prediction, json=property_data)
    
    # Debug
    print("Status:", response.status_code)
    print("Erros de validação:", response.json())


def main():

    # Reading random input samples
    df_random_samples = read_csv_random_input_samples(n_samples=3)

    # For each house data, requesting predictions from the API
    for index, row in df_random_samples.iterrows():
        json_data = row.to_dict()
        print(f"Requesting prediction for sample {index + 1}...")
        predict_property_price(json_data)
        


# Init main
if __name__ == "__main__":
    print("Reading random input samples from 'future_unseen_examples.csv'...")
    main()    
    print("Random input samples read successfully.")
