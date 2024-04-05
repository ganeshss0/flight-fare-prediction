import os, sys
from flight.entity.config_entity import DataIngestionConfig
from flight.exception import FlightException
from flight.logger import logging
from flight.entity.artifact_entity import DataIngestionArtifact




class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:

            logging.info('Data Ingestion Log Start'.center(50, '-'))
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise FlightException(e, sys) from e
        
    def download_data(self) -> str:
        try:
            pass
        except:
            pass
    
    def train_test_split(self) -> str:
        try:
            pass
        except:
            pass
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_file_path = self.download_data()
            data_ingestion_artifact = self.train_test_split()
            return data_ingestion_artifact
        except Exception as e:
            raise FlightException(e, sys) from e
        
    def __del__(self):
        logging.info('Data Ingestion Log Complete'.center(50, '-'))