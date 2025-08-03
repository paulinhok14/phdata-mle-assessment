# Get random data examples from data/future_unseen_examples.csv and send to API endpoint for service demonstration 
import pandas as pd
import os
import requests

# Environment Variables if any. Second @param is the default value
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')

# Path names
file_path = os.path.abspath(__file__)
repo_root = os.path.dirname(os.path.dirname(file_path))
models_path = os.path.join(repo_root, 'model')
data_path = os.path.join(repo_root, 'data')


# Read and return random input samples
def read_csv_random_input_samples(n_samples: int = 5) -> pd.DataFrame:
    df_future_unseen_examples = pd.read_csv(os.path.join(data_path, 'future_unseen_examples.csv'))
    df_random_unseen_examples = df_future_unseen_examples.sample(n=min(n_samples, len(df_future_unseen_examples)), random_state=42)
    
    return df_random_unseen_examples

# Requesting predictions from the API
def predict_property_price(property_data: dict) -> dict:
    pass


def main():

    # Reading random input samples
    read_csv_random_input_samples(n_samples=10)

    # Requesting predictions from the API

# Init main
if __name__ == "__main__":
    print("Reading random input samples from 'future_unseen_examples.csv'...")
    main()
    print("Random input samples read successfully.")