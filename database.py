import pymysql
from json import load
from os import environ as env


class Database:

    def __init__(self, database, **options):
        # Variables
        self.update_columns = True
        # Database tables not checked yet
        self.checked = False

        # Getting information about database
        if type(database) is not dict:
            if database[0] == '{':
                self.data = load(database)
            else:
                self.data = load(open(database, 'r'))
        else:
            self.data = database

        # Starting first connection
        self.con = self.begin(True)

        # Checking options
        options_list = {
            'UPDATE_COLUMNS': self.upd_cols,
            'DROP_TABLES': self.drop_table,
            'CHECK': self.check
        }

        for option, func in options_list.items():
            # Checking environment
            if 'DBH_' + option in env:
                func(env[option])
            # Checking params
            elif option in options:
                func(options[option])

    def __del__(self):
        self.end()

# Connection
    def begin(self, first=False):
        if 'connection' in self.data:
            con = pymysql.connect(**self.data['connection'])
        else:
            params = {}
            for key in env.keys():
                if len(key) > 3 and key[:3] == "DB_":
                    try:
                        val = int(env[key])
                    except ValueError:
                        val = env[key]
                    params[key[3:].lower()] = val
            con = pymysql.connect(**params)
        if first:
            return con
        self.con = con

    def end(self):
        if self.con.open:
            self.con.close()
# ---

# Utils
    def get_db_tables(self):
        with self.con.cursor() as cur:
            cur.execute("SHOW TABLES")
            tables = []
            for el in cur.fetchall():
                tables.append(el[0])
        return tables

    def get_create_cmd(self, table):
        columns = self.data['tables'][table]

        command = f"CREATE TABLE {table} ("
        for col, params in columns.items():
            if col == '_KEY':
                command += f'PRIMARY KEY({params})'
            elif col == '_ADDITION':
                command += params
            else:
                command += col + ' '
                if params == 'KEY':
                    command += "INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY"
                else:
                    command += ' '.join(params)
            command += ', '
        return command[:-2] + ');'

    @staticmethod
    def compare_data_types(local, db):
        if local == 'KEY':
            return True
        local = local[0]

        local = local.upper()
        db = db.upper()

        if '(' not in local:
            if local == db.split('(', 1)[0]:
                return True
            return False

        if local == db:
            return True
        return False

    @staticmethod
    def prepare_vals(values: dict):
        new_vals = {}
        for key, val in values.items():
            if type(val) == str and val != '*':
                new_vals[key] = f"'{val}'"
        return new_vals
# ---

# Options
    def upd_cols(self, val=True):
        if val in ['True', 'TRUE', 'true', '1', 'yes', 'y', True, 1]:
            self.update_columns = True
        else:
            self.update_columns = False

    def drop_table(self, tables="[]"):
        if type(tables) is str:
            tables.replace(' ', '')
            tables.replace('[', '')
            tables.replace(']', '')
            tables = tables.split(',')

        if len(tables) > 0 and tables[0] == '*':
            tables = self.get_db_tables()

        if not tables:
            return

        print(f"Are you sure want to drop {', '.join(tables)}? (y/n)")
        if input() != 'y':
            return

        self.con.cursor().execute("DROP TABLE " + ', '.join(tables))
        self.con.commit()
        self.checked = False
        self.check()

    def check(self, val='1'):
        if self.checked or val not in ['True', 'TRUE', 'true', '1', 'yes', 'y', True, 1]:
            return

        with self.con.cursor() as cur:
            cur.execute("SHOW TABLES")

            tables_in_db = self.get_db_tables()

            for table in tables_in_db:
                if table not in self.data['tables'].keys():
                    continue

                # Checking columns
                if not self.update_columns:
                    continue

                cur.execute(f"DESCRIBE {table}")
                db_cols = {}
                for col_in_db in cur.fetchall():
                    db_cols[col_in_db[0]] = col_in_db[1:]

                # TODO: check params
                for col in self.data['tables'][table].keys():
                    if col in ['_ADDITION', '_KEY']:
                        continue

                    if col not in db_cols.keys():
                        cur.execute(f"ALTER TABLE {table} ADD {col} {' '.join(self.data['tables'][table][col])};")
                        continue

                    if not self.compare_data_types(self.data['tables'][table][col], db_cols[col][0]):
                        cur.execute(f"ALTER TABLE {table} MODIFY COLUMN {col} {' '.join(self.data['tables'][table][col])};")

            # Checking tables
            for table in self.data['tables']:
                if table not in tables_in_db:
                    cur.execute(self.get_create_cmd(table))
        self.con.commit()

# Methods
    def insert(self, table, **values):
        values = self.prepare_vals(values)
        request = f"INSERT INTO {table}({', '.join(values.keys())}) VALUES({', '.join(values.values())})"
        self.execute(request)

    def select(self, columns, table, addition=""):
        request = f"SELECT {', '.join(columns)} FROM {table} {addition}"
        return self.execute(request)

    def update(self, table, **values):
        request = f"UPDATE {table} SET "

        for key, val in values.items():
            # Skipping special keys
            if type(val) == str and val in ['_cond']:
                continue

            if type(val) == str and val != '*':
                request += key + ' = ' + f"'{val}'" + ', '
            else:
                request += key + ' = ' + val + ', '

        # Checking special keys
        if '_cond' in values.keys():
            request = request[:-2] + ' WHERE ' + values['_cond']
        self.execute(request)

    def delete(self, table, condition):
        request = f"DELETE FROM {table} WHERE {condition}"
        if condition == '*':
            request = f"DELETE * FROM {table}"
        self.execute(request)

    def execute(self, sql):
        with self.con.cursor() as cur:
            cur.execute(sql)
            self.con.commit()
            resp = cur.fetchall()
            if len(resp) == 1:
                return resp[0]
            return resp
