#!/bin/bash

# Variables
VENV=venv
PYTHON=$VENV/bin/python
PIP=$VENV/bin/pip

# Function to create a virtual environment
create_venv() {
    virtualenv $VENV
}

# Function to install dependencies
install_dependencies() {
    $PIP install -r requirements.txt
}

# Function to run tests
run_tests() {
    $TEST
}


# Function to clean up generated files
clean_up() {
    rm -rf $VENV
    find . -type d -name '__pycache__' -exec rm -r {} +
    find . -type d -name '*.egg-info' -exec rm -r {} +
    find . -type d -name '*.pytest_cache' -exec rm -r {} +
}

# Check command line arguments
case "$1" in
    venv)
        create_venv
        ;;
    install)
        create_venv
        install_dependencies
        ;;
    clean)
        clean_up
        ;;
    build)
        sudo chmod +x create_db.sh
        sudo cp create_db.sh /usr/local/bin/create_db
        if command -v create_db > /dev/null; then
            echo "Build is successful"
            echo "Usage: create_db -help"
        else
            echo "Build failed"
        fi
        ;;
    *)
        echo "Usage: $0 {venv|install|clean|build}"
        exit 1
        ;;
esac
