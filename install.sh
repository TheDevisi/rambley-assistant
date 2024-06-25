#!/bin/bash

echo "Checking if Python 3.10 installed..."
if ! command -v python3.10 &> /dev/null; then
    echo "Python 3.10 not found. Installing Python 3.10..."

    if ! command -v python3.10 &> /dev/null; then
        echo "Failed to install Python 3.10. Please install Python 3.10 manually from python.org."
        exit 1
    fi
fi

python3.10 -m venv venv
source venv/bin/activate

echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Unexpected error"
    deactivate
    exit 1
fi

read -p "Please, enter your API key (see more on GitHub): " API_KEY
echo "Your API key: $API_KEY"

# Запись API ключа в settings.json
echo '{ "is_first_startup": false, "user_api_token": "'"$API_KEY"'" }' > settings.json

deactivate

echo "Success."
