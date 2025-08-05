# Configurable environment settings
import os
import json
import pandas as pd

FILE_PATH = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(FILE_PATH))
MODELS_PATH = os.path.join(REPO_ROOT, 'model')
DATA_PATH = os.path.join(REPO_ROOT, 'data')

# Settings
MODEL_NAME = 'model.pkl'
MODEL_VERSION = '0.1.0'
ENDPOINT_INPUT_SCHEMA = pd.read_csv(os.path.join(DATA_PATH, 'future_unseen_examples.csv')).columns.tolist()
MODEL_FEATURES = json.load(open(os.path.join(MODELS_PATH, 'model_features.json')))
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')
    

# Exporting the variables for direct import
def get_variables():
      
    return {
        'FILE_PATH': FILE_PATH,
        'REPO_ROOT': REPO_ROOT,
        'MODELS_PATH': MODELS_PATH,
        'DATA_PATH': DATA_PATH,
        'MODEL_NAME': MODEL_NAME,
        'MODEL_VERSION': MODEL_VERSION,
        'ENDPOINT_INPUT_SCHEMA': ENDPOINT_INPUT_SCHEMA,
        'MODEL_FEATURES': MODEL_FEATURES,
        'API_BASE_URL': API_BASE_URL
    }


# Exporting the variables for direct import
vars = get_variables()
FILE_PATH = vars['FILE_PATH']
REPO_ROOT = vars['REPO_ROOT']
MODELS_PATH = vars['MODELS_PATH']
DATA_PATH = vars['DATA_PATH']
MODEL_NAME = vars['MODEL_NAME']
MODEL_VERSION = vars['MODEL_VERSION']
ENDPOINT_INPUT_SCHEMA = vars['ENDPOINT_INPUT_SCHEMA']
MODEL_FEATURES = vars['MODEL_FEATURES']
API_BASE_URL = vars['API_BASE_URL']