#!/bin/bash
# Start the Django SkiOx dashboard.

set -e
cd "$(dirname "$0")"

echo "Starting SkiOx Dashboard at http://127.0.0.1:8000/"
python3 manage.py runserver 127.0.0.1:8000
