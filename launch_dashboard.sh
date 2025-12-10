#!/bin/bash

# SAMI Transfer Bot Dashboard Launcher
# This script activates the virtual environment and launches the Streamlit dashboard

echo "🚀 Starting SAMI Transfer Bot Dashboard..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Launch Streamlit
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0

echo "Dashboard stopped."
