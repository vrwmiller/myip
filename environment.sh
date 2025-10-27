#!/bin/zsh
# Create and activate Python virtual environment, then install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Alias to run the tool easily
alias myip='python myip.py'
