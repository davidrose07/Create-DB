#!/bin/bash

# Default values
UI=false
BROWSE=false
FILE=""
OPTIONS=""

# Function to display usage information
display_usage() {
  echo "Create DB is a tool to convert multiple different file formats into a SQL database"
  echo "Usage: create_db [options] [file]"
  echo "Options:"
  echo "  -ui         Show Graphical User Interface (default: $UI)"
  echo "  -b          Browse for a file (default: $BROWSE)"
  echo "  -f <file>   Specify the file to convert"
  echo "  -h          Display this help message"
}

# Parse command line options
while getopts ":uibf:h" opt; do
  case $opt in
    u) UI=true ;;
    b) BROWSE=true ;;
    f) FILE=$OPTARG ;;
    h) display_usage
       exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2
        exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2
       exit 1 ;;
  esac
done


#Handle options
if $UI && $BROWSE; then
  OPTIONS="src/create_db.py -ui -b"
elif $UI && [ -n "$FILE" ]; then
  OPTIONS="src/create_db.py -ui $FILE"
elif $UI; then
  OPTIONS="src/create_db.py -ui"
elif $BROWSE; then
  OPTIONS="src/create_db.py -b"
elif [ -n "$FILE" ]; then
# Get the directory of the input file
  input_dir=$(dirname "$FILE")
  $FILE="$input_dir/$FILE"
  OPTIONS="src/create_db.py -f $FILE"
else
  echo "No valid options provided. Use -h for help."
  exit 1
fi

# Add your file conversion logic here
echo "Converting file: $FILE"
python3 $OPTIONS
