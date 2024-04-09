import os
from datetime import datetime, date, timedelta
import inspect


# ROOT_DIR = os.getcwd()
CURRENT_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir, os.pardir))
os.chdir(ROOT_DIR)

CONFIG_DIR = 'config'
CONFIG_FILE = 'config.yaml'
SCHEMA_FILE = 'schema.yaml'
MODEL_PARAMETER_FILE = 'model.yaml'

CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
SCHEMA_FILE_PATH = os.path.join(CONFIG_DIR, SCHEMA_FILE)
MODEL_PARAMETER_PATH = os.path.join(CONFIG_DIR, MODEL_PARAMETER_FILE)

# current_dir = os.path.dirname(inspect.getfile(inspect.currentframe())) 

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
START_DATE = date(2019, 3, 1)
DATETIME_FORMAT = '%Y-%m-%d %H:%M'
ONE_DAY = timedelta(days=1)


HOURS_STRINGS = [
    '00', '01', '02', '03', '04', '05', '06', '07', 
    '08', '09', '10', '11', '12', '13', '14', '15', 
    '16', '17', '18', '19', '20', '21', '22', '23'
    ]
MINUTES_STRINGS = [
    '00', '01', '02', '03', '04', '05', '06', '07', 
    '08', '09', '10', '11', '12', '13', '14', '15', 
    '16', '17', '18', '19', '20', '21', '22', '23', 
    '24', '25', '26', '27', '28', '29', '30', '31', 
    '32', '33', '34', '35', '36', '37', '38', '39', 
    '40', '41', '42', '43', '44', '45', '46', '47', 
    '48', '49', '50', '51', '52', '53', '54', '55', 
    '56', '57', '58', '59'
    ]

# Data Transformation Variable
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_ARTIFACT_KEY = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = 'transformed_dir'
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSOR_DIR_KEY = 'preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSOR_FILE_KEY = 'preprocessor_object_file_name'
