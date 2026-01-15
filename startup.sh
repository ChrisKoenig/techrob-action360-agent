#!/bin/bash

# TechRob Action360 Agent - Azure App Service Startup Script
# This script is executed by Azure App Service when the app starts

set -e

echo "Installing dependencies..."
pip install -r requirements.txt --no-cache-dir

echo "Starting TechRob Action360 Agent API..."
exec python run_api.py
