import unittest
from database import Database


class TestOptions(unittest.TestCase):

    # Dropping #
    def test_drop_all(self):
        db = Database('data/Database.json', drop='*', use_warning=False)
        self.assertEqual(db.execute("SHOW TABLES;")[0], 'messages')

    def test_drop_one(self):
        db = Database('data/Database.json', drop=['messages'], use_warning=False)
        self.assertEqual(db.execute("SHOW TABLES;")[0], 'messages')

    def test_drop_warn(self):
        db = Database('data/Database.json', drop=['messages'])
        self.assertEqual(db.execute("SHOW TABLES;")[0], 'messages')
    # ----- #

    # Columns #
    def test_columns(self):
        # Add
        db = Database('data/DB_COLS_ADD.json')
        self.assertEqual('test_col', db.execute("DESCRIBE messages")[2][0])

        # Change
        db = Database('data/DB_COLS_CHANGE.json', update_cols=True)
        self.assertEqual('varchar(4)', db.execute("DESCRIBE messages")[2][1])

        # Remove
        db = Database('data/Database.json', remove_cols=True)
        self.assertEqual(2, len(db.execute("DESCRIBE messages")))
    # ----- #

    # Check #
    def test_no_check(self):
        db = Database('data/DB_COLS_CHANGE.json')
        db.execute("DROP TABLE messages;")
        del db

        db = Database('data/DB_COLS_CHANGE.json', check=False)
        self.assertEqual(0, len(db.execute("SHOW TABLES;")))
    # ----- #
