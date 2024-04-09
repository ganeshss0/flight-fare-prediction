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



def get_dataset(file_path: str, *args, **kwargs) -> pd.DataFrame:

    try:
        data = pd.read_excel(file_path, *args, **kwargs)

        return data
        
    except Exception as e:
        raise FlightException(e, sys)




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

