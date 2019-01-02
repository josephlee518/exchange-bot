"""
PyMongo를 랩핑해서 사용하는 클래스입니다. 
"""
import configparser
from pymongo import MongoClient
from pymongo.cursor import CursorType

class MongoDB:
    def __init__(self, credencials=None):
        """
        모든 설정은 conf 폴더의 config.ini를 읽어서 진행합니다.
        """
        self._config = configparser.ConfigParser()
        self._config.read('../conf/config.ini')
        self._cursor = MongoClient(host=self._config['MONGODB']['DB_IP'], port=int(self._config['MONGODB']['DB_PORT']))
        self._db = self._cursor[self._config['MONGODB']['DB_NAME']]
        self._col = self._db[self._config['MONGODB']['DB_COL']]
    
    def insert_items(self, datas=None):
        """
        Insert Many Document into Mongo
        """
        if datas is None:
            raise Exception("There are No Document, check and try again")
        result_ids = self._col.insert_many(datas)
        return result_ids.inserted_ids

    def insert_item(self, data=None):
        """
        Insert One Document into Mongo
        """
        if data is None:
            raise Exception("There are No Document, check and try again")
        
        result_id = self._col.insert_one(data).inserted_id
        return result_id

    def find_item(self, condition=None):
        """
        Find More than One Document from Mongo
        """
        if condition is None:
            condition = {}
        return self._col.find_one(condition)
        
    def find_items(self, condition=None):
        """
        Find One Document from Mongo
        """
        if condition is None:
            condition = {}
        return self._col.find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)

    def delete_items(self, condition=None):
        """
        Delete Items from Mongo
        """
        if condition is None:
            condition = {}
        return self._col.delete_many(condition)


    def update_items(self, prev_data=None, update_value=None):
        """
        Find and Update items from Mongo
        """
        if prev_data is None:
            raise Exception("There are no prev_data, Check and Try Again")
        if update_value is None:
            raise Exception("There are no Update Value, Check and Try Again")
        return self._col.update_many(filter=prev_data, update=update_value)

    def aggregate(self, pipeline=None):
        """
        Aggregate Items and get Result from Mongo
        """
        if pipeline is None:
            raise Exception("Need To pipeline")
        return self._col.aggregate(pipeline)