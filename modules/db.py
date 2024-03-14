from abc import ABC, abstractclassmethod
from sqlalchemy import create_engine
import pandas as pd
# import mysql
import logging

class DbInterface(ABC):
    @abstractclassmethod
    def create_engine(self):
        pass

    @abstractclassmethod
    def get_connection(self):
        pass

    @abstractclassmethod
    def insert_data_from_dataframe(self, df:pd.DataFrame):
        pass


class Db(DbInterface):
    def __init__(self, driver:str, db_user:str, db_pw:str, db_server:str, db_port:str, db_name:str) -> None:
        self.__driver = driver
        self.__db_user = db_user
        self.__db_pw = db_pw
        self.__db_server = db_server
        self.__db_port = db_port
        self.__db_name = db_name
        self.__engine = None
        self.__connection = None
        super().__init__()
    
    def create_engine(self):
        connection_string = f"mysql+{self.__driver}://{self.__db_user}:{self.__db_pw}@{self.__db_server}:{self.__db_port}/{self.__db_name}"
        try:
            self.__engine = create_engine(connection_string, echo=True)
        except:
            raise ConnectionError("Fail to create engine")
    
    def get_connection(self):
        try:
            self.__connection = self.__engine.connect()
        except:
            raise ConnectionError("Connection with DB failed")
        
    def insert_data_from_dataframe(self, df:pd.DataFrame, table:str, if_exists:str="append"):
        try:
            df.to_sql(table, self.__engine, if_exists=if_exists, index=False)
            return (1, f"INSERT data to {table} success!")
        except Exception as e:
            return (0, str(e))


class DbService:
    def __init__(self, db: Db) -> None:
        self.__db = db

    def run_all(self, df:pd.DataFrame, table:str):
        try:
            self.__db.create_engine()
        except Exception as e:
            logging.error(f"Fail to create engine:\n{str(e)}")
            return 0

        
        status, msgStatus = self.__db.insert_data_from_dataframe(df, table)

        if status:
            logging.info(msgStatus)
        else:
            logging.error(msgStatus)
            return 0
        
        return 1
