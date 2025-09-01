#!/usr/bin/env bash
set -e

# This script sets up a virtual environment, installs dependencies, and starts the Flask app.
# It is intended for macOS and Linux users.

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Download it from https://www.python.org/downloads/"
  exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=web_app.py
flask run
