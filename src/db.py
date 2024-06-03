import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os,sys
import json
from pandas import json_normalize


class DB:
    '''
    DB Class : class to handle database creation and query
    '''
    def __init__(self, file:str) -> None:
        '''
        Init Function: setup db connection and handle file to convert
        :param: file - file to convert 
        '''
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

    def determine_file_type(self) -> dict:
        '''
        Function: determine the file type to convert by splitting the extension and iterating through a dictionary
        :return: dict
        '''
        _, file_extension = os.path.splitext(self.file)
        file_types = {
            '.csv': 'CSV file',
            '.json': 'JSON file',
            '.xml': 'XML file',
            '.xlsx': 'Excel file',
            '.sql': 'SQL file',
        }
        return file_types.get(file_extension.lower(), 'Unknown file type')

    def make_table(self) -> None:
        '''
        Function: create a table based on the data in the file provided
        '''
        connection_string = f'sqlite:///{self.db_file}'
        engine = create_engine(connection_string)
        print(f'Make table:  ' ,self.df.to_sql(self.table_name, con=engine, if_exists='replace', index=False))
        

    def xml_to_sql(self) -> None:
        '''
        Function: convert a xml file to db
        '''
        try:
            self.df = pd.read_xml(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in xml_to_sql: {e}')

    def csv_to_sql(self) -> None:
        '''
        Function: convert a csv file to db
        '''
        try:
            self.df = pd.read_csv(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in csv_to_sql: {e}')

    def xcel_to_sql(self) -> None:
        '''
        Function: convert a xcel file to db
        '''
        try:
            self.df = pd.read_excel(self.file)
            self.make_table()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in xcel_to_sql: {e}')

    def unpack_json(self, data, parent_key='', sep='.'):
        """
        Recursively unpack a nested JSON object.

        :param: data - The JSON object (as a dictionary) to unpack.
        :param: parent_key - The base key string for the current level of recursion.
        :param: sep -  The separator between keys for nested objects.
        :return: A dictionary with flattened keys.
        """
        temp_data = set()
        temp_values = []

        if isinstance(data, dict):
            for keys in data.keys():
                parent_key = keys  # Table name or multiple table names
                for items in data[parent_key]:
                    if isinstance(items, dict):
                        row = {}
                        for k, v in items.items():
                            temp_data.add(k)
                            row[k] = v
                        temp_values.append(row)
                self.table_name = parent_key
                columns = list(temp_data)
                rows = temp_values  # Ensure rows have values corresponding to columns
                return pd.DataFrame(rows, columns=columns)
        else:
            try:
                self.df = pd.read_json(self.file)
                self.make_table()
                print('Database creation successful!')
            except Exception as e:
                print(f'Exception in json_to_sql: {e}')
            
    
    def json_to_sql(self) -> None:
        '''
        Function: convert a json file to db
        '''
        try:
            with open(self.file, 'r') as f:
                json_data = json.load(f)
            
            unpacked_data = self.unpack_json(json_data)

            self.df= pd.json_normalize(unpacked_data)
            for item in self.df.items():
                print(item)
                        
        except json.JSONDecodeError as e:
            print(f'JSON decode error: {e}')
        except FileNotFoundError as e:
            print(f'File not found: {e}')
        except Exception as e:
            print(f'Exception in json_to_sql: {e}')
       

    def sql(self) -> None:
        '''
        Function: read sql file and create db
        '''
        try:
            with open(self.file, 'r') as file:
                sql_script = file.read()
            self.cursor.executescript(sql_script)
            self.con.commit()
            print('Database creation successful!')
        except Exception as e:
            print(f'Exception in sql: {e}')
    
    def read_db(self):
        '''
        Function: Query all items from the db and return results
        :return: list
        '''
        self.con= sqlite3.connect('data.db')
        self.cursor = self.con.cursor()
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = self.cursor.fetchall()
        return rows
    
    def get_schema(self) -> dict:
        '''
        Function: Query the schema details from the db and return dictionary results
        :return: dict
        '''
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
    

    



