from database import Database


def test(db: Database, **kwargs):
    db.insert('users', message=kwargs['message'])
    return db.select(['name'], 'users')


funcs = {
    'test': test
}

db = Database('data/Database.json', functions=funcs)
print(db.run('test', message="Hello, World!"))
