import json
import sys
import os

import pandas as pd
import numpy as np
from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e, sys)
        
    def val_number_of_cols(self, dataframe: DataFrame) -> bool:

        try:
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            logging.info(f"Required columns present: {status}")
            return status
        except Exception as e:
            raise MyException(e, sys)
        
    def is_column_exist(self, df:DataFrame) -> bool:

        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in df.columns:
                    missing_numerical_columns.append(column)
            
            for column in self._schema_config["categorical_columns"]:
                if column not in df.columns:
                    missing_categorical_columns.append(column)
            
            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")

            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing numerical column: {missing_categorical_columns}")

            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True

        except Exception as e:
            raise MyException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_data_validation(self) -> DataIngestionArtifact:

        try:
            validation_error_msg = ""
            logging.info("Data Validation Started")
            train_df, test_df = (DataValidation.read_data(self.data_ingestion_artifact.train_file_path),
                                 DataValidation.read_data(self.data_ingestion_artifact.test_file_path))
            
            status = self.val_number_of_cols(dataframe=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All required columns present in training dataframe: {status}")

            
            status = self.val_number_of_cols(dataframe=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe. "
            else:
                logging.info(f"All required columns present in testing dataframe: {status}")

            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All categorical/int columns present in training dataframe: {status}")

            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."
            else:
                logging.info(f"All categorical/int columns present in testing dataframe: {status}")

            val_status = len(validation_error_msg) == 0

            data_validation_artifact = DataValidationArtifact(
                validation_status = val_status,
                message = validation_error_msg,
                validation_report_file = self.data_validation_config.validation_report_file_path
            )


            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)


            validation_report = {
                "validation_status": val_status,
                "message": validation_error_msg.strip()
            }
            
            with open(self.data_validation_config.validation_report_file_path, "w") as report_files:
                json.dump(validation_report, report_files, indent=4)

            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
            
            
        
    