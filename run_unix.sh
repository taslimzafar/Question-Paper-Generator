#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting Streamlit application..."
streamlit run app.py

