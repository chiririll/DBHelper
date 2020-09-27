import pymysql
import json
from os import environ as env


# TODO: Write scripts for managing


class Database:

    def __init__(self, database, **input_options):
        """
        :param database: File/string/dict/json with database structure
        :param input_options: Options and login data for database

        :key check: Check tables (create missing), should be boolean
        :key add_cols: Add new columns added to database info file, should be boolean
        :key update_cols: Update data types of columns, should be boolean
        :key remove_cols: Remove columns that not exists in database info file, should be boolean
        :key drop: List of tables to drop or string '*' (all), should be list or string
        :key use_warning: Require confirmation in console for dropping, should be boolean

        :key host: Hostname, should be string
        :key port: Port, should be int
        :key user: Username, should be string
        :key password: Password, should be string
        :key database: Name of database to work with, should be string
        :key db: Alias for database, should be string
        """

        # Global dicts #
        #   states (checked, etc)
        self._states = {
            'checked': False,
            'dropped': False,
            'cols_updated': False,
            'cols_added': False,
            'cols_removed': False
        }

        #   connection data (login, password, etc)
        self._connection_data = {
            'host': None,
            'port': 3306,
            'database': None,
            'db': None,
            'user': None,
            'password': None
        }

        #   options (update_columns, drop_table, etc)
        self._options = {
            'check': True,  # Checking database on missing tables
            'add_cols': True,  # Adding new columns
            'update_cols': False,  # Updating data tpe in columns
            'remove_cols': False,  # Removing unknown columns
            'drop': [],  # Dropping tables
            'use_warning': True  # Use warning before dropping
        }

        #   custom functions
        self._custom_functions = {}
        # --- #

        # Getting information about database #
        if type(database) is dict:
            self._data = database
        elif type(database) is str:
            # Json string
            if database[0] == '{':
                self._data = json.loads(database)
            # File path
            else:
                f = open(database)
                self._data = json.load(f)
                f.close()
        #   File reader
        else:
            self._data = json.loads(database.read())
        # --- #

        # Updating options
        #   Custom functions
        if 'functions' in input_options.keys():
            self._custom_functions = input_options['functions']
        #   Other options
        for opt in self._options.keys():
            # Checking environment
            if 'DBH_' + opt.upper() in env:
                if opt == 'drop':
                    self._options[opt] = env[opt].replace(' ', '').split(
                        ',')  # Getting list of tables to drop from environ
                elif env[opt].lower() in ['true', 'yes', 'y', '1']:
                    self._options[opt] = True  # Str to boolean
                elif env[opt].lower() in ['false', 'no', 'n', '0']:
                    self._options[opt] = False  # Str to boolean
            # Checking kwargs
            elif opt in input_options:
                self._options[opt] = input_options[opt]  # Getting option from kwargs

        # Getting connection info
        for field in self._connection_data.keys():
            # Checking environment
            if 'DBH_' + field.upper() in env:
                self._connection_data[field] = env['DBH_' + field.upper()]
            # Checking user options
            elif field in input_options:
                self._connection_data[field] = input_options[field]
            # Checking config file
            elif 'connection' in self._data.keys() and field in self._data['connection'].keys():
                self._connection_data[field] = self._data['connection'][field]

        # Starting first connection
        self._con = None
        if 'start_con' in input_options and not input_options['start_con']:
            pass
        else:
            self.begin()

    def __del__(self):
        self.end()

    # Connection #
    def begin(self):
        if self._con is not None and self._con.open:
            return

        self._con = pymysql.connect(**self._connection_data)

        self._drop_tables()
        self._check()

    def end(self):
        if self._con.open:
            self._con.close()

    # ----- #

    # Utils #
    def _get_db_tables(self):
        with self._con.cursor() as cur:
            cur.execute("SHOW TABLES")
            tables = []
            for el in cur.fetchall():
                tables.append(el[0])
        return tables

    def _gen_table_creating_cmd(self, table):
        columns = self._data['tables'][table]

        command = f"CREATE TABLE {table} ("
        for col, params in columns.items():
            if col == '_KEY':
                command += f'PRIMARY KEY({params})'
            elif col == '_ADDITION':
                command += params
            else:
                command += col + ' '
                if params == 'KEY':
                    command += "INT AUTO_INCREMENT NOT NULL PRIMARY KEY"
                else:
                    command += ' '.join(params)
            command += ', '
        return command[:-2] + ');'

    @staticmethod
    def _compare_data_types(local, db):
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
    def _prepare_vals(values: dict, **options):
        new_vals = {}
        for key, val in values.items():
            if type(val) == str and val != '*':
                new_vals[key] = f"\'{val}\'"
            elif val is None:
                new_vals[key] = "NULL"
            elif 'all_str' in options.keys() and options['all_str']:
                new_vals[key] = str(val)
        return new_vals

    # ----- #

    # Options #
    def _drop_tables(self):
        # If already dropped
        if self._states['dropped']:
            return

        # If drop all
        if len(self._options['drop']) > 0 and self._options['drop'][0] == '*':
            self._options['drop'] = self._get_db_tables()

        # If table list empty
        if not self._options['drop']:
            return

        # Confirming
        if self._options['use_warning']:
            print(f"Are you sure want to drop {', '.join(self._options['drop'])}? (y/n)")
            if input() != 'y':
                return

        # Executing SQL
        self._con.cursor().execute("DROP TABLE " + ', '.join(self._options['drop']))
        self._con.commit()

        # Changing states
        self._states['checked'] = False
        self._states['dropped'] = True

        # Recreating tables
        self._check()

    def _check(self):
        if self._states['checked'] or not self._options['check']:
            return

        with self._con.cursor() as cur:
            cur.execute("SHOW TABLES")
            tables_in_db = self._get_db_tables()

            # Checking tables
            for table in tables_in_db:
                # Skipping unknown tables
                if table not in self._data['tables'].keys():
                    continue

                # Getting list of columns in table
                cur.execute(f"DESCRIBE {table}")
                db_cols = {}
                for col_in_db in cur.fetchall():
                    db_cols[col_in_db[0]] = col_in_db[1:]

                # Removing unknown columns
                for col in db_cols.keys():
                    if col not in self._data['tables'][table].keys():
                        cur.execute(f"ALTER TABLE {table} DROP COLUMN {col};")

                # Checking columns
                for col in self._data['tables'][table].keys():
                    # Skipping keywords
                    if col.upper() in ['_ADDITION', '_KEY']:
                        continue

                    # Adding missing columns
                    if self._options['add_cols'] and col not in db_cols.keys():
                        cur.execute(f"ALTER TABLE {table} ADD {col} {' '.join(self._data['tables'][table][col])};")
                        continue

                    # Changing data type
                    if self._options['update_cols'] and not self._compare_data_types(self._data['tables'][table][col],
                                                                                     db_cols[col][0]):
                        cur.execute(
                            f"ALTER TABLE {table} MODIFY COLUMN {col} {' '.join(self._data['tables'][table][col])};")

            # Checking tables
            for table in self._data['tables']:
                if table not in tables_in_db:
                    cur.execute(self._gen_table_creating_cmd(table))
        # Committing changes
        self._con.commit()

    # ----- #

    # Methods #
    #   Custom functions
    def run(self, function, **kwargs):
        return self._custom_functions[function](self, **kwargs)

    def insert(self, table, **values):
        values = self._prepare_vals(values, all_str=True)
        request = f"INSERT INTO {table} ({', '.join(values.keys())}) VALUES ({', '.join(values.values())})"
        self.execute(request)

    def insert_or_update(self, table, **values):
        values = self._prepare_vals(values, all_str=True)

        request = f"INSERT INTO {table} ({', '.join(values.keys())}) VALUES ({', '.join(values.values())}) " \
                  f"ON DUPLICATE KEY UPDATE {', '.join(list(map(lambda pair: '='.join(pair), values.items())))}"
        self.execute(request)

    def select(self, table, columns, addition=""):
        request = f"SELECT {', '.join(columns)} FROM {table} {addition}"
        return self.execute(request)

    def update(self, table, condition="", **values):
        values = self._prepare_vals(values, all_str=True)
        request = f"UPDATE {table} SET {', '.join(list(map(lambda pair: '='.join(pair), values.items())))}"

        # Condition
        c = condition.split(' ')
        if c[0].upper() == 'WHERE':
            condition = ' '.join(c[1:])
        if len(condition) > 0:
            request = request + ' WHERE ' + condition

        self.execute(request)

    def delete(self, table, condition):
        request = f"DELETE FROM {table} WHERE {condition}"
        if condition == '*':
            request = f"DELETE * FROM {table}"
        self.execute(request)

    def execute(self, sql):
        self.begin()
        with self._con.cursor() as cur:
            cur.execute(sql)
            self._con.commit()
            resp = cur.fetchall()
            # if len(resp) == 1:
            #     return resp[0]
            return resp
    # ----- #
