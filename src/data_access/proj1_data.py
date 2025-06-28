import sys
import os
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException

class ProjData:

    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient(database_name = DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:

        # Export entire collection in Mongo DB as Pandas dataframe

        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            print("Start fetching data from Mongo DB")
            print("Collections: -- ", collection)
            df = pd.DataFrame(list(collection.find()))
            print(f"data fetched having {df.shape[0]} records")
            if "id" in df.columns.to_list():
                df = df.drop(columns = ["id"], axis = 1)
            df.replace({"na":np.nan}, inplace = True)
            return df
        
        except Exception as e:
            raise MyException(e, sys)
        
        
