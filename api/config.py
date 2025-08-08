# Configurable environment settings
import os
import json
import pandas as pd

# Paths
FILE_PATH = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(FILE_PATH))
MODELS_PATH = os.path.join(REPO_ROOT, 'model')
DATA_PATH = os.path.join(REPO_ROOT, 'data')

# Settings
APP_VERSION = '1.0.0'
MODEL_NAME = 'model.pkl'
MODEL_VERSION = '0.1.0'
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')

# Models config
MODEL_REQUIRED_FEATURES = json.load(open(os.path.join(MODELS_PATH, 'model_features.json')))
MAIN_ENDPOINT_INPUT_SCHEMA = pd.read_csv(os.path.join(DATA_PATH, 'future_unseen_examples.csv')).columns.tolist()
SALES_DATA_COLUMNS = pd.read_csv(os.path.join(DATA_PATH, 'kc_house_data.csv')).columns.tolist()
SALES_DATA_FEATURES = [feature for feature in SALES_DATA_COLUMNS if feature in MODEL_REQUIRED_FEATURES] + ['zipcode']