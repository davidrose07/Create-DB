# Create-DB
Python project to convert different files to a database. Right now it uses a sqlite3 database. Future use will support Mysql and others.

# Python Version
3.10.12

# Files in the Project
create_db.py: Main Python script for file conversion.
create_db.sh: Shell script for command-line usage.
controller.py: Manages the core functionality.
db.py: Handles database interactions.
view.py: Manages the GUI components.
db_manager.py:  Handles CLI search options

# TODO:
test installer file on different distros
create options to use different kinds of databases
create a better GUI

# Installation
# Does not support all distros at the moment. You may have to manually install or just run python file directly 
run the bash script install.sh
may have to change permissions for the file
chmod +x install.sh

./install.sh install     install dependencies
./install.sh clean       clean to remove venv and other temporary files
./install.sh build       build the application


# Usage
Using the Shell Script
Run the shell script with the desired options:

-ui: Show Graphical User Interface.
-b: Browse for a file.
-f <file>: Specify the file to convert.
-h: Display the help message.


# Examples:
# This can also be run with the create_db.py file as well
./create_db.sh -b -ui 
./create_db.sh -ui -f <path_to_file> 
./create_db.sh -f <path_to_file>


# Running the Python Script Directly
Run the Python script with the desired options:

-ui or --ui: Display the user interface.
-b or --b: Browse for a file.
-f: The path to the file to be processed.

Examples:

python3 create_db.py -b -ui
python3 create_db.py <path_to_file> -ui
python3 create_db.py <path_to_file>


License
This project is currently not licensed.
