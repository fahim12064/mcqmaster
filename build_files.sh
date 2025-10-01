#!/bin/bash
set -e

echo "===== Setting up Python environment ====="
# pip নিশ্চিত করা এবং আপডেট করা
python3.9 -m ensurepip --upgrade
python3.9 -m pip install --upgrade pip setuptools wheel

echo "===== Installing Python dependencies ====="
python3.9 -m pip install -r requirements.txt

echo "===== Collecting static files ====="
python3.9 manage.py collectstatic --noinput --clear

echo "===== Applying migrations ====="
python3.9 manage.py migrate --noinput

echo "===== Build completed successfully ====="
