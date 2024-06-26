#!/usr/bin/env python3

from controller import *
from PyQt5.QtWidgets import QApplication
import sys, argparse


def main(file_path, show_ui, browse) -> None:
    '''
    Main Function to start the application. uses parsed arguements to handle bash script or run directly from python with command line arguements

    :param: file_path - file to convert
    :param: show_ui -   options to display the user interface or use command line
    :param: browse -    option to use file explorer to find a file    
    '''
    

    if show_ui:
        application = QApplication([sys.argv])
        controller=Controller(file_path, show_ui=True, browse=browse)
        application.exec_()
    else:
        application = QApplication([sys.argv])
        controller=Controller(file_path, show_ui=False, browse=browse)
        application.exec_()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files and optionally display a UI.")
    parser.add_argument("-f", nargs='?', default=None, help="The path to the file to be processed.")
    parser.add_argument("-ui", "--ui", action="store_true", help="Display the user interface.")
    parser.add_argument("-b", "--b", action="store_true", help="Browse for a file.")


    args = parser.parse_args()

    if not args.f and not args.b:
        print('Program requires a file name or browse option\npython3 create_db.py -f <filename> or -b\n-help or --help to display options')
    else:
        main(args.f, args.ui, args.b)













