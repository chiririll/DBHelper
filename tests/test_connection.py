import unittest
import json
from database import Database
from os import environ as env


class TestConnection(unittest.TestCase):

    def test_path(self):
        db = Database("data/Database.json")

    def test_dict(self):
        f = open("data/Database.json")
        data = json.load(f)
        f.close()
        db = Database(data)

    def test_string(self):
        f = open("data/Database.json")
        string = f.readlines()
        string = ' '.join(string)
        string = string.replace('\n', '').replace('\\', '')
        db = Database(string)

    def test_reader(self):
        f = open("data/Database.json")
        db = Database(f)
        f.close()

    def test_params(self):
        db = Database("data/DB_NC.json", host="localhost", user="root", password="", db="DBHelper")

    def test_environ(self):
        if 'DBH_HOST' in env.keys():
            db = Database("data/DB_NC.json")


if __name__ == '__main__':
    unittest.main()
