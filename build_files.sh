#!/bin/bash

# build_files.sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt

echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear
