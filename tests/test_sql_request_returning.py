import unittest
from database import Database


class TestSQLRequests(unittest.TestCase):

    db = Database("data/Database.json")

    def test_insert(self):
        req = self.db.insert('test', value1="1", value2=2, _request=True)
        self.assertEqual("INSERT INTO test (value1, value2) VALUES ('1', 2);", req)

    def test_update(self):
        req = self.db.update('test', "id=123", something="hi", _request=True)
        self.assertEqual("UPDATE test SET something='hi' WHERE id=123;", req)

    def test_insert_or_update(self):
        req = self.db.insert_or_update('test', id=5, val2=125, _request=True)
        self.assertEqual("INSERT INTO test (id, val2) VALUES (5, 125) ON DUPLICATE KEY UPDATE id=5, val2=125;", req)

    def test_select(self):
        req = self.db.select('test', ['field1', 'field2'], _request=True)
        self.assertEqual("SELECT field1, field2 FROM test;", req)

    def test_delete(self):
        req = self.db.delete('test', "id=256", _request=True)
        self.assertEqual("DELETE FROM test WHERE id=256;", req)


if __name__ == "__main__":
    unittest.main()
