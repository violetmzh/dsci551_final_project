import os.path as path
import json
import sqlite3 as db


class Database:
    def __init__(self, file_path):
        self.database_path = path.join(path.dirname(path.realpath(__file__)), file_path)
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = db.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def create_data_table(self, sql):
        query_text = sql
        self.cursor.executescript(query_text)

    def drop_data_table(self):
        query_text = "DROP TABLE IF EXISTS AirIndex;"
        self.cursor.executescript(query_text)

    def query(self, sql):
        query_text = sql
        self.cursor.execute(query_text)
        data = self.cursor.fetchall()
        return data

    def add_data(self, sql, tup):
        query_text = sql
        params = tup
        try:
            self.cursor.execute(query_text, params)
            self.connection.commit()
            return json.dumps({
                'code': 200,
                'msg': 'success'
            })
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)})

    def update_data(self, sql, tup):
        query_text = sql
        params = tup
        try:
            self.cursor.execute(query_text, params)
            result = self.cursor.fetchall()
            self.connection.commit()
            return json.dumps({
                'code': 200,
                'msg': 'success'
            })
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)})

    def remove_data(self, sql):
        query_text = sql
        try:
            self.cursor.execute(query_text)
            result = self.cursor.fetchall()
            self.connection.commit()
            return json.dumps({
                'code': 200,
                'msg': 'success'
            })
        except Exception as e:
            return json.dumps({"code": 500, "msg": str(e)})

    def disconnect(self):
        self.connection.close()
