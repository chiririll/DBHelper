from database import Database

db = Database(open("Database.json", 'r'))
db.begin()
