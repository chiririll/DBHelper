import unittest
from database import Database


class TestIdReturning(unittest.TestCase):

    db = Database('data/Database.json', drop='*', use_warning=False)

    def test_insert(self):
        rid = self.db.insert('messages', message="Hello, World!", _return_id=True)
        print(rid)
        self.assertEqual(1, rid)

    def test_insert_or_update(self):
        rid = self.db.insert('messages', message="Hello, World 2!", _return_id=True)
        self.assertEqual(2, rid)


if __name__ == '__main__':
    unittest.main()
