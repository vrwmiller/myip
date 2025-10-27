#!/bin/zsh
# Create and activate Python virtual environment, then install dependencies
/opt/homebrew/bin/python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Alias to run the tool easily
alias myip='python myip.py'
alias bandsintown='python bandsintown.py --app_id bandsintown@gmail.com'
alias mediawiki='python mediawiki.py'
alias stoic='python stoic.py'
alias myopen='./myopen.sh'
alias weather='python weather.py'

alias random='python random.py'
