import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os
import json

class DB:
    '''
    DB Class : class to handle database creation and query
    '''
    def __init__(self, file: str) -> None:
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

    def searchdb(self, text) -> list:
        '''
        Function: query database with the text provided. It searches all columns for the text provided and returns results
        :param: text - string of hte search parameters
        :return: list - the results of the query        
        '''
        results = []

        self.column_names = [description[0] for description in self.cursor.description]
       
        for col in self.column_names:
            try:
                query = f"SELECT * FROM {self.table_name} WHERE {col} LIKE '%" + text + "%'"
                self.cursor.execute(query)
                rows=self.cursor.fetchall()
                results.append(rows)
            except:
                pass
        return results
    
    def make_sql_file(self, output_file='your_data.sql'):
        '''
        Function: Creates a .sql file and saves it to the current directory
        :param: Default file location for now
        
        '''
        
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        self.table_names = [table[0] for table in tables]

        with open(output_file, 'w') as file:
            for table in self.table_names:
                self.cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'")
                create_table_statement = self.cursor.fetchone()[0]
                file.write(f"{create_table_statement};\n\n")
                
                self.cursor.execute(f"PRAGMA table_info({table})")
                columns_info = self.cursor.fetchall()
                column_names = [col[1] for col in columns_info]
                self.column_list = ", ".join(column_names)

                self.cursor.execute(f"SELECT * FROM {table}")
                rows = self.cursor.fetchall()
                
                for row in rows:
                    values_list = ", ".join([f"'{str(value)}'" if value is not None else 'NULL' for value in row])
                    insert_statement = f"INSERT INTO {table} ({self.column_list}) VALUES ({values_list});\n"
                    file.write(insert_statement)
        
        print(f"Data has been exported to {output_file}")

    def determine_file_type(self) -> str:
        '''
        Function: determine the file type to convert by splitting the extension and iterating through a dictionary
        :return: str
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
        self.df.to_sql(self.table_name, con=engine, if_exists='replace', index=True)
        print('Database creation successful!')

    def xml_to_sql(self) -> None:
        '''
        Function: convert a xml file to db
        '''
        try:
            self.df = pd.read_xml(self.file)
            self.make_table()
        except Exception as e:
            print(f'Exception in xml_to_sql: {e}')

    def csv_to_sql(self) -> None:
        '''
        Function: convert a csv file to db
        '''
        try:
            self.df = pd.read_csv(self.file)
            self.make_table()
        except Exception as e:
            print(f'Exception in csv_to_sql: {e}')

    def xcel_to_sql(self) -> None:
        '''
        Function: convert a xcel file to db
        '''
        try:
            self.df = pd.read_excel(self.file)
            self.make_table()
        except Exception as e:
            print(f'Exception in xcel_to_sql: {e}')

    def unpack_json(self, data):
        """
        Recursively unpack a nested JSON object.

        :param data: The JSON object (as a dictionary or list) to unpack.
        :return: A flattened list of dictionaries.
        """
        def flatten(x, name=''):
            out={}
            if isinstance(x, dict):
                for a in x:
                    out.update(flatten(x[a], name + a + '_'))
            elif isinstance(x, list):
                i = 0
                for a in x:
                    out.update(flatten(a, name + str(i) + '_'))
                    i += 1
            else:
                out[name[:-1]] = x
            return out

        if isinstance(data, dict):
            for key in data.keys():
                self.table_name = key
                data = data[key]

        if isinstance(data, list):
            return [flatten(item) for item in data]
        elif isinstance(data, dict):
            return [flatten(data)]
        else:
            raise ValueError("Input data must be a dictionary or a list of dictionaries.")


    def json_to_sql(self) -> None:
        """
        Function: convert a JSON file to a DataFrame.
        """
        try:
            with open(self.file, 'r') as f:
                json_data = json.load(f)

            unpacked_data = self.unpack_json(json_data)
            self.df = pd.DataFrame(unpacked_data)
            

            self.make_table()
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
        self.con = sqlite3.connect('data.db')
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
