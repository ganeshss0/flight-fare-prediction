import sys
from os import path
from flight.logger import logging
from flight.exception import FlightException
from sklearn.ensemble import RandomForestRegressor
from flight.constants import MODEL_PARAMETER_PATH, CONFIG_FILE_PATH
from flight.utility import read_yaml, get_dataset, save_object



class ModelTrainer:
    def __init__(self) -> None:
        logging.info('Reading Model Config File')
        self.model_config = read_yaml(MODEL_PARAMETER_PATH)
        self.config = read_yaml(CONFIG_FILE_PATH)

    def build_model(self):
        try:
            logging.info('Building Random Forest Model')
            self.model = RandomForestRegressor(**self.model_config['HyperParameter'])
        except Exception as e:
            logging.error(e)
            raise FlightException(e, sys) from e

    def train_model(self):
        try:
            logging.info('Training the model')
            dataset_path = path.join(
                self.config['DATASET_DIRECTORY'],
                self.config['PROCESSED_DATASET_DIRECTORY'],
                self.config['TRAIN_DATASET_FILE']
            )
            model_path = path.join(
                self.config['MODEL_DIRECTORY'],
                self.config['MODEL_FILE']
            )
            dataset = get_dataset(dataset_path)
            dataset_feature = dataset.drop(columns=['Price'])
            dataset_target = dataset['Price']
            self.model.fit(X=dataset_feature, y=dataset_target)
            save_object(model_path, self.model)
        except Exception as e:
            logging.error(e)
            raise FlightException(e, sys) from e