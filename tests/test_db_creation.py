import unittest
from database import Database


class TestDBCreation(unittest.TestCase):

    def test_foreign_key(self):
        db = Database("data/DB_FK.json", drop='*', use_warning=False)

        # Remove column
        db = Database('data/Database.json', remove_cols=True)
        cols = []
        for col in db.execute("DESCRIBE messages"):
            cols.append(col[0])
        self.assertEqual(['id', 'message', 'test_none'], cols)


if __name__ == '__main__':
    unittest.main()
