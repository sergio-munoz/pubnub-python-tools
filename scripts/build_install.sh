#!/bin/bash
# Dinamically build and install latest pip version.

# Get current directory parent dir
dir="$(pwd)"
parentdir="$(dirname "$dir")"

# Parse file containing version
file=${parentdir}/pubnub-python-tools/src/pubnub_python_tools/__about__.py
name=$(<"$file")       #the output of 'cat $file' is assigned to the $name variable
version=$(echo $name | cut -d \' -f2)

# Build package
hatch build

# Install package
pip install -U dist/pubnub_python_tools-${version}.tar.gz
