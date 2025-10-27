#!/bin/zsh
# Create and activate Python virtual environment, then install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
