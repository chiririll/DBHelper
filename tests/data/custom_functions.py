from database import Database


def test(db: Database, **kwargs):
    db.insert('messages', message=kwargs['message'])
    return db.select(['message'], 'messages')[0][0]


cfuncs = {
    'test': test
}
