import os, sys
import numpy as np
import pandas as pd
from flight.logger import logging
from flight.exception import FlightException
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from flight.constants import DATETIME_FORMAT, SCHEMA_FILE_PATH, CONFIG_FILE_PATH, ONE_DAY
from flight.utility import read_yaml, save_object, load_object, str_to_datetime


class DataTransformation:

    def __init__(self, data: dict):
        logging.info('Data Transformation Initialized')

        logging.info('Reading Schema File')
        self.schema = read_yaml(SCHEMA_FILE_PATH)
        self.data = data
        self.DataFrame = pd.DataFrame()

    def build_preprocessor(self) -> ColumnTransformer:
        logging.info('Building Preprocessor')
        try:
            logging.info('Reading Config File')
            config = read_yaml(CONFIG_FILE_PATH)

            logging.info('Preprocessor Build Started')
            preprocessor = ColumnTransformer(
                transformers=[
                    ('Scaler', StandardScaler(), self.schema['Numerical_Columns']),
                    ('encoder', OneHotEncoder(drop='first', dtype=np.int8), self.schema['Categorical_Columns'])
                ]
            )
            
            dataset_train_path = os.path.join(config['DATASET_DIRECTORY'], config['INTERIM_DATASET_DIRECTORY'], config['TRAIN_DATASET_FILE'])
            dataset_test_path = os.path.join(config['DATASET_DIRECTORY'], config['INTERIM_DATASET_DIRECTORY'], config['TEST_DATASET_FILE'])

            logging.info('Loading Train Dataset')
            df_train = pd.read_excel(dataset_train_path)

            logging.info('Loading Test Dataset')
            df_test = pd.read_excel(dataset_test_path)

            logging.info('Concatinating Train and Test dataset')
            df = pd.concat([df_train, df_test], axis=0, ignore_index=True)

            # changing low number of flighs (Airline) into 'Others'
            Others = self.schema['Other_Airlines']
            Airline_Filter = lambda x: 'Others' if x in Others else x
            df['Airline'] = df['Airline'].apply(Airline_Filter)

            df_features = df.drop(columns=['Price'])
            preprocessor.fit(df_features)

            logging.info('Preprocessor Build Successully')
            preprocessor_file = os.path.join(config['ARTIFACT_DIRECTORY'], config["PREPROCESSOR_FILE"])
            save_object(preprocessor_file, preprocessor)

            logging.info(f'Saving the preprocessor at {preprocessor_file}')
            return preprocessor

        except Exception as e:
            logging.error(e)
            raise FlightException(e, sys) from e


    def transform(self):
        logging.info('Loading Preprocessor')
        preprocessor = self.get_preprocessor()
        self.add_features()
        self.create_dataframe()
        logging.info('Transforming Data')
        transformed = preprocessor.transform(self.DataFrame)

        return pd.DataFrame(transformed, columns=self.schema['Processed_Column_Names'])

    def get_preprocessor(self) -> ColumnTransformer:
        logging.info('Reading Config file')
        config = read_yaml(CONFIG_FILE_PATH)

        preprocessor_file = os.path.join(config['ARTIFACT_DIRECTORY'], config["PREPROCESSOR_FILE"])
        if os.path.exists(preprocessor_file):
            preprocessor = load_object(preprocessor_file)
        else:
            preprocessor = self.build_preprocessor()

        return preprocessor

    def add_features(self):
        logging.info('Adding Feature into data.')

        if self.data['Airline'] in self.schema['Other_Airlines']:
            self.data['Airline'] = 'Others'

        depature_datetime_string = f"{self.data['Date_of_Journey']} {self.data['Dep_Hour']}:{self.data['Dep_Min']}"
        depature_datetime = str_to_datetime(depature_datetime_string, DATETIME_FORMAT)

        self.data['Journey_Day'] = depature_datetime.day
        self.data['Journey_Month'] = depature_datetime.month

        arrival_datetime_string = f"{self.data['Date_of_Journey']} {self.data['Arrival_Hour']}:{self.data['Arrival_Minute']}"
        arrival_datetime = str_to_datetime(arrival_datetime_string, DATETIME_FORMAT)

        if self.data['Arrive_Next_Day']:
            arrival_datetime += ONE_DAY

        flight_duration = arrival_datetime - depature_datetime

        minutes, seconds = divmod(flight_duration.seconds, 60)

        self.data['Duration_Hours'], self.data['Duration_Mins'] = divmod(minutes, 60)

        self.data['Arrival_Hour'] = arrival_datetime.hour
        self.data['Arrival_Mins'] = arrival_datetime.minute

        _ = self.data['Total_Stops']
        self.data['Total_Stops'] = self.schema['Total_Stops'][_]

    def create_dataframe(self):
        logging.info('Creating DataFrame Object')
        try:    
            for column in self.schema['Interim_Column_Names']:
                self.DataFrame[column] = [self.data[column]]
            logging.info('DataFrame Object Created Successfully')
        except Exception as e:
            logging.error(e)
            raise FlightException(e, sys) from e
