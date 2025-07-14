Create a list of upcoming matches from all open tournaments using a username and API key from Challonge, show the next 10 open matches, and add start times.

To set up: 
clone repo
`python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate`


To run server:
`python manage.py runserver`


To get updates from challonge (set up in cron or systemd to run every 30s or so):
`scar_brackets/update_data.sh`
