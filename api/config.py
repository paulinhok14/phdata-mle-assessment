# Configurable environment settings
import os
import json

def set_environment_variables():
    """Set all environment variables for the application"""
    
    # Path names
    FILE_PATH = os.path.abspath(__file__)
    REPO_ROOT = os.path.dirname(os.path.dirname(FILE_PATH))
    MODELS_PATH = os.path.join(REPO_ROOT, 'model')
    DATA_PATH = os.path.join(REPO_ROOT, 'data')
    
    # Settings
    MODEL_NAME = 'model.pkl'
    MODEL_VERSION = '0.1.0'
    MODEL_FEATURES = json.load(open(os.path.join(MODELS_PATH, 'model_features.json')))
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')
    
    # Set as environment variables
    os.environ['MODELS_PATH'] = MODELS_PATH
    os.environ['DATA_PATH'] = DATA_PATH
    os.environ['MODEL_NAME'] = MODEL_NAME
    os.environ['MODEL_VERSION'] = MODEL_VERSION
    os.environ['API_BASE_URL'] = API_BASE_URL
    os.environ['MODEL_FEATURES'] = json.dumps(MODEL_FEATURES)


# Exporting the variables for direct import
def get_variables():
    set_environment_variables()
      
    return {
        'FILE_PATH': FILE_PATH,
        'REPO_ROOT': REPO_ROOT,
        'MODELS_PATH': MODELS_PATH,
        'DATA_PATH': DATA_PATH,
        'MODEL_NAME': MODEL_NAME,
        'MODEL_VERSION': MODEL_VERSION,
        'MODEL_FEATURES': MODEL_FEATURES,
        'API_BASE_URL': API_BASE_URL
    }

# Auto-setting when imported
set_environment_variables()

# Exporting the variables for direct import
vars = get_variables()
FILE_PATH = vars['FILE_PATH']
REPO_ROOT = vars['REPO_ROOT']
MODELS_PATH = vars['MODELS_PATH']
DATA_PATH = vars['DATA_PATH']
MODEL_NAME = vars['MODEL_NAME']
MODEL_VERSION = vars['MODEL_VERSION']
MODEL_FEATURES = vars['MODEL_FEATURES']
API_BASE_URL = vars['API_BASE_URL']