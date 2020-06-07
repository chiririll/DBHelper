# PyMySQL Helper

## Connecting to database

    from database import Database
    
    db = Database(JSON, OPTIONS)

Instead of json you can use path or dict. 

### Json example

    {
      "connection": {
        "db": "test",
        "port": 3301,
        "host": "localhost",
        "user": "user",
        "password": "password"
      },
    
      "tables": {
        "users": {
          "id": "KEY",
          "name": ["VARCHAR(30)", "NOT NULL"],
          "email": ["VARCHAR(50)", "NOT NULL", "UNIQUE"],
          "password": ["VARCHAR(32)", "NOT NULL"],
          "regDate": ["INT", "UNSIGNED"]
        },
        "groups_t": {
          "id": ["TINYINT", "UNSIGNED"],
          "name": ["VARCHAR(32)", "UNIQUE", "NOT NULL"],
          "participants": ["TEXT"],
          "_KEY": "id"
        },
        "facts": {
          "name": ["VARCHAR(30)", "NOT NULL"],
          "fact": ["TEXT"],
          "rating": ["TINYINT", "UNSIGNED"],
          "_ADDITION": "CHECK(rating > 1)"
        }
      }
    }

### Options

- **UPDATE_COLUMNS** *(True/False)* - changing data type in column 
- **DROP_TABLES** _(List of tables or *)_ - dropping tables in list (if * it drops all tables) 
- **CHECK** *(True/False)* - Check tables in database. If table not in database, it creates.

  