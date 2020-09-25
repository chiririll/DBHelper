# PyMySQL Helper
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f7336b74b07f41c594b4ce4a9050b321)](https://www.codacy.com/manual/sstive/DBHelper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sstive/DBHelper&amp;utm_campaign=Badge_Grade)

## Connecting to database

    from DBHelper import Database 
    
    db = Database(JSON, OPTIONS)

Instead of json you can use path to file with json, dict or file reader. 

## Json example

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
### Special keys

- **_KEY** - Primary key

- **_ADDITION** - SQL code that adds to creating table request

## Connection data

Connection data (host, port, database name, user, password) can be added to: 

- config file (Database.json),  
- options (when initialising database object)
- environ (in uppercase and with prefix DBH_) 

## Options

Also can be added to environ in uppercase and with prefix DBH_ (e.g. DBH_DROP). 
Default value is **bold**.

- **functions** (Dict with function name and function) - Add custom function that can be executed with method run

- **check** (**True**/False) - Check tables in database. If table not in database, it creates.

- **add_cols** (**True**/False) - Add new columns from config 

- **update_cols** (True/**False**) - Changing data type in columns if it was changed in config

- **remove_cols** (True/**False**) - Remove columns not appeared in config 

- **drop** (List of tables or '*') - Drop tables (environ example: "Users, Photos, Stats")

- **use_warning** (**True**/False) - Use confirmation while dropping tables 

## Methods

### Default sql methods

- **insert**(_str_ table, _kwargs_ values)

- **select**(_str_ table, _list_ columns, _str_ addition=" ") - Addition example: "WHERE x > 0"

- **update**(_str_ table, _str_ condition, _kwargs_ values)

- **insert_or_update**(_str_ table, _kwargs_ values)

- **delete**(_str_ table, _str_ condition)

- **execute**(_str_ sql_code)

### Advanced methods

- **db.run**(_str_ function_name, _kwargs_ params) - Run custom function added with option _functions_

## Custom Functions 

Custom function can be executed with method: 
- **db.run**(_str_ function_name, _kwargs_ params)

### Example code

    from DBHelper import Database
    
    def test(db: Database, **kwargs):
        db.insert('facts', name='test' fact=kwargs['message'])
        return db.select('facts', ['name'])
    
    funcs = {
        'test': test
    }
    
    db = Database('data/Database.json', functions=funcs)
    print(db.run('test', message="Hello, World!"))
