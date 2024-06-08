#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from view import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from db import DB
from db_manager import DBManager
import sys
from colorama import init, Fore, Style

init(autoreset=True)

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):
    '''
    Main Application : Controller Class    
    '''    
    def __init__(self, file=None, show_ui=False, browse=False) -> None:
        '''
        Init Function: setup the ui and handle options
        :param: file - the file to convert
        :param: show_ui - options to display the user interface or use command line
        :param: browse - option to use file explorer to find a file
        '''
        super().__init__()
        self.setupUi(self)
        self.file = file
        self.ui = show_ui
        self.data = None
        self.column_names = None

        self.table_color = Fore.BLUE
        self.column_color = Fore.GREEN
        self.type_color = Fore.YELLOW

        if browse:
            self.options = QFileDialog.Options()
            self.options |= QFileDialog.DontUseNativeDialog
            filename, _ = QFileDialog.getOpenFileName(self, 'Browse File', "/home", "csv files(*.csv);;json Files(*.json);;xml files(*.xml);;excel files(*.xlsx);;Sql Files(*.sql))", options=self.options)
            if filename:
                self.file =filename

        if self.file != None:  
            self.db = DB(self.file)
        else:
            print('Program requires a file name\npython3 create_db.py <filename>\n-help or --help to display options')
            sys.exit(0)
        
        if show_ui:
            self.show()
            self.setupTable()
            self.lineEdit_search.textChanged.connect(lambda ev: self.search(ev,self.lineEdit_search.text()))
            self.displaySchema()
            self.print_readout()
        else:
            self.print_readout()

    def colored_text(self, text, color):
        return f"{color}{text}{Style.RESET_ALL}"
    
    def print_readout(self) -> None:
        '''
        Function: print readout of the schema in the command line in colored format
        
        '''
        
        schema_info = self.db.get_schema()
        for table,columns in schema_info.items():
            print(self.colored_text(f'Table: {table}: schema', self.table_color))
            for column in columns:
                column_name = self.colored_text(f'\tColumn: {column[0]:<20}', self.column_color)
                column_type = self.colored_text(f'\tType: {column[1]:<20}',self.type_color)
                print(f'{column_name}{column_type}')

        data = self.db.read_db()
        #column_names = [self.colored_text(description[0], self.column_color) for description in self.db.cursor.description]
        column_names = [description[0] for description in self.db.cursor.description]

        self.db.make_sql_file()

        if not self.ui:
            """ print(f'\n\n')
            print(self.colored_text('*' * 56, self.table_color))
            print("\t".join(column_names))

            for row in data:
                print(self.colored_text("\t".join(map(str, row)), self.type_color)) """
            db_manager= DBManager(data, column_names)
            db_manager.run()

        
        sys.exit(0)
        
            


    """ def colored_text(self, text, color_code) -> str:
        '''
        Function: returns a colored formated text
        :param: text - the text to color
        :param: color_code - the color of the text
        :return: str of the formatted text        
        '''

        formatted_text = f"\033[{color_code}m{text}\033[0m"
        return formatted_text """

    def displaySchema(self) -> None:
        '''
        Function: displays the schema in the tablewidget for the user interface        
        '''

        schema_info = self.db.get_schema()
        
        self.schemaTableWidget.setColumnCount(3)
        self.schemaTableWidget.setHorizontalHeaderLabels(["Table Name", "Column Name", "Column Type"])
        
        row = 0
        for table, columns in schema_info.items():
            for column in columns:
                self.schemaTableWidget.insertRow(row)
                self.schemaTableWidget.setItem(row, 0, QTableWidgetItem(table))
                self.schemaTableWidget.setItem(row, 1, QTableWidgetItem(column[0]))
                self.schemaTableWidget.setItem(row, 2, QTableWidgetItem(column[1]))
                row += 1

    def setupTable(self) -> None:
        '''
        Function: retrieves data from the database and displays it in the tablewidget for the user interface        
        '''

        self.data = self.db.read_db()
        self.column_names = [description[0] for description in self.db.cursor.description]
        
        self.tableWidget.setColumnCount(len(self.column_names))
        self.tableWidget.setHorizontalHeaderLabels(self.column_names)
        self.tableWidget.setRowCount(len(self.data))
        
        for row_index, row_data in enumerate(self.data):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        
        
    def search(self, event, text):
        '''
        Function: filter results in the tableWidget as your typing
        :param: text - text of the lineEdit
        
        '''
        text = text.strip()
        if text == "":
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            self.setupTable()
            return
        rows = self.db.searchdb(text)
        
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        flattened_rows = [item for sublist in rows if sublist for item in sublist]

        seen_rows = set()
        unique_rows = []
        for row in flattened_rows:
            if row not in seen_rows:
                unique_rows.append(row)
                seen_rows.add(row)

        if unique_rows:
            self.tableWidget.setRowCount(len(unique_rows))

            for row_index, row_data in enumerate(unique_rows):
                for col_index, col_data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))


        
        

