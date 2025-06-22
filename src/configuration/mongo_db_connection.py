import os
import pymongo
import certifi
import sys

from src.exception import MyException 
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()

class MongoDBClient:

    ## Eastablishing connection with MongoDB client

    client = None

    def __init__(self, database_name:str=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Evironment variable {MONGODB_URL_KEY} is not set")
                
                print("Started to make MongoDB connectoin")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            
            self.client = MongoDBClient.client
            self.databse = self.client[database_name]
            self.database_name = database_name
            logging.info("Mongo DB connection is successful")

        except Exception as e:
            raise MyException(e, sys)
        
        

                    
