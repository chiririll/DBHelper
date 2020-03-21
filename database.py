import json
import pymysql


class Database:

    def __init__(self, database):
        if type(database) is not dict:
            self.data = json.load(database)
        else:
            self.data = database

        if 'port' not in self.data.keys():
            self.data['port'] = 3306
        if 'charset' not in self.data.keys():
            self.data['charset'] = 'utf8mb4'

        self.con = pymysql.connections.Connection

    def begin(self):
        self.con = pymysql.connect(
            host=self.data['host'],
            db=self.data['name'],
            user=self.data['user'],
            password=self.data['password'],
            charset=self.data['charset'],
            port=self.data['port']
        )

    def end(self):
        self.con = pymysql.connections.Connection
