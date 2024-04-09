import os, sys
from flight.entity.config_entity import DataTransformationConfig


from flight.logger import logging
from flight.exception import FlightException
from flight.utility import read_yaml
from flight.constants import *





class Configuration:
    '''
    Flight Fare Predictor Configuration Class
    '''

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH) -> None:
        self.config_info = read_yaml(file_path=config_file_path)



    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            data_transformation_artifact_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_KEY,
                self.time_stamp
            )
            
            

            transformed_test_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY]
            )

            transformed_train_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY]
            )

            preprocessor_object_file_path = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config[DATA_TRANSFORMATION_PREPROCESSOR_DIR_KEY],
                data_transformation_config[DATA_TRANSFORMATION_PREPROCESSOR_FILE_KEY]
            )

            logging.info('Data Transformation Config')
            return DataTransformationConfig(
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir,
                preprocessed_object_file_path=preprocessor_object_file_path
            )
        
        except Exception as e:
            raise FlightException(e, sys)



        
    
