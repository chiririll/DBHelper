import unittest
from database import Database


class TestMain(unittest.TestCase):
    def test_connection(self):
        db = Database("data/Database.json", DROP_TABLES=[], CHECK=True, UPDATE_COLUMNS=True)


if __name__ == '__main__':
    unittest.main()
