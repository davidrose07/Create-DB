#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from view import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from db import DB
import sys

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):    
    def __init__(self, file=None, show_ui=False, browse=False) -> None:
        super().__init__()
        self.setupUi(self)
        self.file = file

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
            self.displaySchema()
        else:
            self.print_readout()

    def print_readout(self):
        table_color = '34'  # Blue
        column_color = '32'  # Green
        type_color = '33'  # Yellow

        schema_info = self.db.get_schema()
        for table,columns in schema_info.items():
            print(self.colored_text(f'Table: {table}', table_color))
            for column in columns:
                column_name = self.colored_text(f'\tColumn: {column[0]:<20}', column_color)
                column_type = self.colored_text(f'\tType: {column[1]:<20}',type_color)
                print(f'{column_name}{column_type}')
        sys.exit(0)

    def colored_text(self, text, color_code):
        return f"\033[{color_code}m{text}\033[0m"

    def displaySchema(self):
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

    def setupTable(self):
        data = self.db.read_db()
        column_names = [description[0] for description in self.db.cursor.description]
        
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        self.tableWidget.setRowCount(len(data))
        
        for row_index, row_data in enumerate(data):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        
        

        
        

