import unittest
from database import Database


class TestCommands(unittest.TestCase):

    db = Database('data/Database.json', drop='*', use_warning=False)

    # Inserting values
    def test_insert(self):
        self.db.delete('messages', "id=1")
        self.db.insert('messages', message="Testing insert", id=1)
        message = self.db.select('messages', ['message'], "WHERE id=1")[0][0]
        self.assertEqual("Testing insert", message)

    # Updating values
    def test_update(self):
        self.db.insert_or_update('messages', id=2, message="Testing")

        self.db.update('messages', "id=2", message="Testing update")
        message = self.db.select('messages', ['message'], "WHERE id=2")[0][0]
        self.assertEqual("Testing update", message)

        self.db.update('messages', "WHERE id=2", message="Testing update 2")
        message = self.db.select('messages', ['message'], "WHERE id=2")[0][0]
        self.assertEqual("Testing update 2", message)

    # Adding new or changing
    def test_insert_or_update(self):
        self.db.insert_or_update('messages', message="Testing insert or update", id=3)
        message = self.db.select('messages', ['message'], "WHERE id=3")[0][0]
        self.assertEqual("Testing insert or update", message)

        self.db.insert_or_update('messages', message="Testing insert or update second time", id=3)
        message = self.db.select('messages', ['message'], "WHERE id=3")[0][0]
        self.assertEqual("Testing insert or update second time", message)

    # Deleting
    def test_delete(self):
        self.db.insert_or_update('messages', message="Testing deleting", id=4)
        self.db.delete('messages', "id=4")
        messages = self.db.select('messages', '*')
        self.assertEqual(0, len(messages))


if __name__ == '__main__':
    unittest.main()
