from database import Database

db = Database(open("Database.json", 'r'), DROP_TABLE=[], CHECK=True, UPDATE_COLUMNS=True)
