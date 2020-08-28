import unittest
from database import Database


def test(db: Database, **kwargs):
    db.insert('messages', message=kwargs['message'])
    return db.select(['message'], 'messages')[0][0]


cfuncs = {
    'test': test
}


class TestCustomFunctions(unittest.TestCase):

    def test_custom_functions(self):
        msg = 'test'
        db = Database("data/Database.json", functions=cfuncs)
        res = db.run('test', message=msg)
        self.assertEqual(msg, db.run('test', message=msg))
