import sys, os
import joblib
import numpy as np
import pandas as pd
from yaml import safe_load, dump
from flight.logger import logging
from flight.exception import FlightException
from flight.constants import *
from datetime import datetime

def read_yaml(file_path: str, encoding:str='utf-8') -> dict:
    '''Reads a YAML file and returns the contents as dictonary object.'''

    try:
        logging.info('Reading Config File')
        with open(file=file_path, encoding=encoding) as file:
            config: dict = safe_load(file)
        logging.info('Config File Reading Successfull')
        return config
        
    except Exception as e:
        raise FlightException(e, sys) from e


def write_yaml(file_path: str, data: dict, encoding: str='utf-8', **kwargs) -> str:
    '''Write a YAML file and return the file_path of written YAML file.'''
    try:
        if not file_path.endswith(('.yml', 'yaml')):
            file_path = file_path + '.yml'
        logging.info(f'Writing Data to YAML File at {file_path}')
        with open(file=file_path, mode='w', encoding=encoding) as file:
            dump(data=data, stream=file, encoding=encoding, **kwargs)
        logging.info('Writing Data to YAML File Successfull')
        
        return file_path
    
    except Exception as e:
        raise FlightException(e, sys) from e



def get_datasets(artifact_path: str, schema_file_path: str, date_string: str = None) -> list[tuple]:
    '''
    A function that can give a list of tuples of datasets after matching the given date_string to each data ingestion folder.
    * `artifact_path` : Data Ingestion Artifact Path
    * `schema_file_path` : Schema Configuration file path(schema.yml)
    * `date_string` : Matches the date string with available datasets, Default=None.

    If `date_string` gives the latest datasets available by Default(None), if string does not match it return empty list.
    '''
    try:
        schema = read_yaml(schema_file_path)
    

        folders = sorted(available_datasets(artifact_path), reverse=True)

        if date_string:
            matching_folder = [folder for folder in folders if date_string in folder]
        else:
            matching_folder = [folders[0]]

        def get_data_ingestion_folder() -> tuple[str]:
            config = read_yaml(CONFIG_FILE_PATH)
            ingestion_config = config[DATA_INGESTION_CONFIG_KEY]
            train_path = os.path.join(
                ingestion_config[INGESTION_DATA_DIR_KEY], 
                ingestion_config[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            test_path = os.path.join(
                ingestion_config[INGESTION_DATA_DIR_KEY], 
                ingestion_config[DATA_INGESTION_TEST_DIR_KEY]
            )
            return train_path, test_path

        
        datasets = []
        ingested_train_path, ingested_test_path = get_data_ingestion_folder()

        for folder in matching_folder:
            path = os.path.join(artifact_path, folder)
            if os.path.exists(path):
                train_path = os.path.join(path, ingested_train_path)
                file_name = os.listdir(train_path)[0]
                train_path = os.path.join(train_path, file_name)
                test_path = os.path.join(path, ingested_test_path, file_name)
                datasets.append(
                    (
                        pd.read_csv(train_path, dtype=schema[SCHEMA_COLUMNS_KEY]), 
                        pd.read_csv(test_path, dtype=schema[SCHEMA_COLUMNS_KEY])
                    )
                )
                
        
        return datasets
    except Exception as e:
        raise FlightException(e, sys)

def get_dataset(file_path: str, *args, **kwargs) -> pd.DataFrame:

    try:
        data = pd.read_excel(file_path, *args, **kwargs)

        return data
        
    except Exception as e:
        raise FlightException(e, sys)


def available_datasets(artifact_path: str):
    
    try:
        datasets = os.listdir(artifact_path)
    except Exception as e:
        raise FlightException(e, sys)

    print(f'Available Datasets Count: {len(datasets)}')
    return datasets



def save_object(filepath: str, object, *args, **kwargs):
    try:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        
        if isinstance(object, np.ndarray):
            np.save(file=filepath, arr=object, *args, **kwargs)

        else:
            if not filepath.endswith('.joblib'):
                filepath = filepath + '.joblib'
            joblib.dump(value=object, filename=filepath, *args, **kwargs)
        
        return filepath

    except Exception as e:
        raise FlightException(e, sys)
    
def load_object(filepath: str, *args, **kwargs):
    try:
       
        if filepath.endswith('.npy'):
            object = np.load(file=filepath, *args, **kwargs)
        
        else:
            object = joblib.load(filename=filepath, *args, **kwargs)
    
        return object

    except Exception as e:
        raise FlightException(e, sys)
    

def str_to_datetime(string, format):
    try:
        dt = datetime.strptime(string, format)
        return dt
    except Exception as e:
        logging.error(e)
        raise FlightException(e, sys)

