#!/usr/bin/env bash

# Create Python Venv and pip install pkgs
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

# Copy env file 
cp env .env

# Setup keys using sed without neglecting Macs
if [ "$(uname)" == "Darwin" ]; then
    sed -i '' "s/pubnub_subscribe_key=.*/pubnub_subscribe_key=${1}/g" .env
    sed -i '' "s/pubnub_publish_key=.*/pubnub_publish_key=${2}/g" .env
    sed -i '' "s/pubnub_user_id=.*/pubnub_user_id=${3}/g" .env
else
    sed -i "s/pubnub_subscribe_key=.*/pubnub_subscribe_key=${1}/g" .env
    sed -i "s/pubnub_publish_key=.*/pubnub_publish_key=${2}/g" .env
    sed -i "s/pubnub_user_id=.*/pubnub_user_id=${3}/g" .env
fi

# Source environment variables
source .env