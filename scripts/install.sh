#!/usr/bin/env bash

# Create Python Venv and pip install pkgs
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements_dev.txt

# Copy env file 
cp env .env

# Setup keys using sed without neglecting Macs
if [ "$(uname)" == "Darwin" ]; then
    sed -i '' "s/PN_SUBSCRIBE_KEY=.*/PN_SUBSCRIBE_KEY=${1}/g" .env
    sed -i '' "s/PN_PUBLISH_KEY=.*/PN_PUBLISH_KEY=${2}/g" .env
    sed -i '' "s/PN_USER_ID=.*/PN_USER_ID=${3}/g" .env
else
    sed -i "s/PN_SUBSCRIBE_KEY=.*/PN_SUBSCRIBE_KEY=${1}/g" .env
    sed -i "s/PN_PUBLISH_KEY=.*/PN_PUBLISH_KEY=${2}/g" .env
    sed -i "s/PN_USER_ID=.*/PN_USER_ID=${3}/g" .env
fi

# Source environment variables
source .env
