import unittest
from database import Database

from tests.data.custom_functions import functions


class TestMain(unittest.TestCase):
    def test_connection(self):
        db = Database("data/Database.json", FUNCTIONS=functions, DROP_TABLES=[], CHECK=True, UPDATE_COLUMNS=True)
        print(db.run('test', message="Hello, World!"))


if __name__ == '__main__':
    unittest.main()
