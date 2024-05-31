import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os,sys


class DB:
    def __init__(self, file:str) -> None:
        self.db_file = 'data.db'
        self.df = None
        self.file = file
        self.file_path = self.determine_file_type()
        self.table_name = os.path.splitext(os.path.basename(self.file))[0]

        try:
            self.con = sqlite3.connect(self.db_file)
            self.cursor = self.con.cursor()
        except:
            os.mkdir(self.db_file)
        finally:
            self.con = sqlite3.connect(self.db_file)
            self.cursor = self.con.cursor()

        if self.file_path == 'CSV file':
            self.csv_to_sql()
        elif self.file_path == 'XML file':
            self.xml_to_sql()
        elif self.file_path == 'Excel file':
            self.xcel_to_sql()
        elif self.file_path == 'JSON file':
            self.json_to_sql()
        elif self.file_path == 'SQL file':
            self.sql()
        else:
            print(f'Unsupported file type: {self.file_path}')

    def determine_file_type(self):
        _, file_extension = os.path.splitext(self.file)
        file_types = {
            '.csv': 'CSV file',
            '.json': 'JSON file',
            '.xml': 'XML file',
            '.xlsx': 'Excel file',
            '.sql': 'SQL file',
        }
        return file_types.get(file_extension.lower(), 'Unknown file type')

    def make_table(self):
        connection_string = f'sqlite:///{self.db_file}'
        engine = create_engine(connection_string)
        self.df.to_sql(self.table_name, con=engine, if_exists='replace', index=False)

    def xml_to_sql(self):
        try:
            self.df = pd.read_xml(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in xml_to_sql: {e}')
        return

    def csv_to_sql(self):
        try:
            self.df = pd.read_csv(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in csv_to_sql: {e}')
        return

    def xcel_to_sql(self):
        try:
            self.df = pd.read_excel(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in xcel_to_sql: {e}')
        return

    def json_to_sql(self):
        try:
            self.df = pd.read_json(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in json_to_sql: {e}')
        return

    def sql(self):
        try:
            with open(self.file, 'r') as file:
                sql_script = file.read()
            self.cursor.executescript(sql_script)
            self.con.commit()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in sql: {e}')
        return
    
    def read_db(self):
        self.con= sqlite3.connect('data.db')
        self.cursor = self.con.cursor()
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = self.cursor.fetchall()
        return rows
    
    def get_schema(self):
        schema_info = {}
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            for table in tables:
                table_name = table[0]
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                columns = self.cursor.fetchall()
                schema_info[table_name] = [(col[1], col[2]) for col in columns]
            return schema_info
        except Exception as e:
            return f"Exception in get_schema: {e}"
    

    



