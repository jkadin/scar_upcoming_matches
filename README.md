Create a list of upcoming matches from all open tournaments using a username and API key from Challonge or compatible API, show the next 10 open matches, and add start times.

## Setup

1. Clone the repository and navigate into it.
2. Run the following commands to set up your virtual environment and database:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

## Configuration

API Credentials and an optional alternate URI can be specified in an `.env` file:

```
CHALLONGE_USERNAME=user
CHALLONGE_API_KEY=key
CHALLONGE_CUSTOM_URL=api.challonge.com/v1
```

## Running the Server

To run server:

```bash
python manage.py runserver
```

## Data Updates

To get updates from tournaments (set up in cron or systemd to run every 30s or so):

```bash
scar_brackets/update_data.sh
```