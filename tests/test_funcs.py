import unittest
from database import Database


def test(db: Database, **kwargs):
    db.insert('messages', message=kwargs['message'])
    return db.select('messages', ['message'])[0][0]


cfuncs = {
    'test': test
}


class TestCustomFunctions(unittest.TestCase):

    def test_custom_functions(self):
        msg = 'test'
        db = Database("data/Database.json", functions=cfuncs, drop='*', use_warning=False)
        res = db.run('test', message=msg)
        self.assertEqual(msg, db.run('test', message=msg))

if __name__ == '__main__':
    unittest.main()
