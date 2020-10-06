import unittest
from database import Database


class TestRequests(unittest.TestCase):

    db = Database("data/Database.json", check=False)

    def test_insert(self):
        req = self.db.insert('test', id=1, _request=True)
        self.assertEqual("INSERT INTO test (id) VALUES (1);", req)
        print(req)

    def test_insert_or_update(self):
        req = self.db.insert_or_update('test', id=1, _request=True)
        self.assertEqual("INSERT INTO test (id) VALUES (1) ON DUPLICATE KEY UPDATE id=1;", req)
        print(req)

    def test_select(self):
        req = self.db.select('test', ['messages'], _request=True)
        self.assertEqual("SELECT messages FROM test;", req)
        print(req)

    def test_update(self):
        req = self.db.update('test', "id=1", message="Testing", _request=True)
        self.assertEqual("UPDATE test SET message='Testing' WHERE id=1;", req)
        print(req)

    def test_delete(self):
        req = self.db.delete('test', "id=4", _request=True)
        self.assertEqual("DELETE FROM test WHERE id=4;", req)


if __name__ == '__main__':
    unittest.main()
