import unittest
from os import environ as env
from database import Database


class TestOptions(unittest.TestCase):

    # Dropping #
    def test_drop_all(self):
        env['DBH_DROP'] = "*"
        env['DBH_USE_WARNING'] = "n"
        db = Database('data/Database.json')
        del env['DBH_DROP']
        del env['DBH_USE_WARNING']
        self.assertEqual(db.execute("SHOW TABLES;")[0][0], 'messages')

    def test_drop_one(self):
        env['DBH_DROP'] = "messages"
        env['DBH_USE_WARNING'] = "false"
        db = Database('data/Database.json')
        del env['DBH_DROP']
        del env['DBH_USE_WARNING']
        self.assertEqual(db.execute("SHOW TABLES;")[0][0], 'messages')

    # ----- #

    # Columns #
    def test_columns(self):
        # Add
        db = Database('data/DB_COLS_ADD.json')
        self.assertEqual('test_col', db.execute("DESCRIBE messages")[2][0])

        # Change
        env['DBH_UPDATE_COLS'] = "true"
        db = Database('data/DB_COLS_CHANGE.json')
        del env['DBH_UPDATE_COLS']
        self.assertEqual('varchar(4)', db.execute("DESCRIBE messages")[2][1])

        # Remove
        env['DBH_REMOVE_COLS'] = "True"
        db = Database('data/Database.json')
        cols = []
        for col in db.execute("DESCRIBE messages"):
            cols.append(col[0])
        del env['DBH_REMOVE_COLS']
        self.assertEqual(['id', 'message', 'test_none'], cols)
    # ----- #

    # Check #
    def test_no_check(self):
        db = Database('data/DB_COLS_CHANGE.json')
        db.execute("DROP TABLE messages;")
        del db

        env['DBH_CHECK'] = "0"
        db = Database('data/DB_COLS_CHANGE.json')
        del env['DBH_CHECK']
        self.assertEqual(0, len(db.execute("SHOW TABLES;")))
    # ----- #


if __name__ == '__main__':
    unittest.main()
