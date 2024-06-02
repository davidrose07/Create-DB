#!/bin/bash

# Variables
VENV=venv
PYTHON=python3.10
PIP=$VENV/bin/pip

# Function to create a virtual environment
create_venv() {
    if command -v $PYTHON > /dev/null 2>&1; then
        virtualenv $VENV
    else
        echo "Python 3.10.12 is not installed. Please install Python 3.10.12 and try again."
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    $PIP install -r requirements.txt
}


# Function to clean up generated files
clean_up() {
    rm -rf $VENV
    find . -type d -name '__pycache__' -exec rm -r {} +
    find . -type d -name '*.egg-info' -exec rm -r {} +
    find . -type d -name '*.pytest_cache' -exec rm -r {} +
}

# Function to determine the appropriate bin directory
determine_bin_dir() {
    if [ -d "/usr/local/bin" ]; then
        BIN_DIR="/usr/local/bin"
    elif [ -d "/usr/bin" ]; then
        BIN_DIR="/usr/bin"
    elif [ -d "/opt/bin" ]; then
        BIN_DIR="/opt/bin"
    else
        echo "No suitable bin directory found. Please ensure one of /usr/local/bin, /usr/bin, or /opt/bin exists."
        exit 1
    fi
}

# Check command line arguments
case "$1" in
    install)
        create_venv
        install_dependencies
        ;;
    clean)
        clean_up
        ;;
    build)
        sudo chmod +x create_db.sh
        sudo cp create_db.sh $BIN_DIR/create_db
        if command -v create_db > /dev/null; then
            echo "Build is successful"
            echo "Usage: create_db -help"
        else
            echo "Build failed"
        fi
        ;;
    *)
        echo "Usage: $0 {install|clean|build}"
        exit 1
        ;;
esac
