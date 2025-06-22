import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import MyException
from src.logger import logging
from src.data_access.proj1_data import ProjData

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)
        
    def export_data_into_feature_store(self) -> DataFrame:

        ## Exporting data into feature store

        try:
            logging.info(f"Exporting data from mongo db")
            my_data = ProjData()
            dataframe = my_data.export_collection_as_dataframe(collection_name = self.data_ingestion_config.collection_name, 
                                                               database_name=self.data_ingestion_config.database_name)
            logging.info(f"Shape of the dataframe {dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data to feature store file path {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index = False, header = True)
            return dataframe
        
        except Exception as e:
            raise MyException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:

        logging.info("initiated train test split by calling split_data_as_train_test method of Data_Ingestion class with data = {dataframe.shape}")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=123)
            logging.info("Perform train test split on data frame")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            train_set.to_csv(self.data_ingestion_config.testing_file_path, index = False, header = True)

            logging.info(f"Exported train and test file path.")
        
        except Exception as e:
            raise MyException(e, sys) from e

    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Entered initiated_data_ingestion method of Data_Ingestion class")

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongo db")

            self.split_data_as_train_test(dataframe)
            logging.info("Split the data into train test")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(train_file_path = self.data_ingestion_config.training_file_path, 
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e
