#!/usr/bin/env python3

from src.controller import *
from PyQt5.QtWidgets import QApplication
import sys, argparse


def main(file_path, show_ui, browse) -> None:
            
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
    parser.add_argument("-b", "--b", action="store_true", help="Display the user interface.")


    args = parser.parse_args()

    if len(sys.argv) < 2:
        print('Program requires a file name\npython3 create_db.py <filename>\n-help or --help to display options')
    else:
        main(args.f, args.ui, args.b)













