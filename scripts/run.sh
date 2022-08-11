#!/usr/bin/env bash

# Create Python Venv and pip install pkgs
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

# Copy env file 
cp env .env

# Setup keys using sed without neglecting Macs
if [ "$(uname)" == "Darwin" ]; then
    sed -i '' "s/subscribe_key=.*/subscribe_key=${1}/g" .env
    sed -i '' "s/publish_key=.*/publish_key=${2}/g" .env
else
    sed -i "s/subscribe_key=.*/subscribe_key=${1}/g" .env
    sed -i "s/publish_key=.*/publish_key=${2}/g" .env
fi

# Source environment variables
source .env

# Run Python App
python3 run_app.py