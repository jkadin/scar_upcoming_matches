import os
import sys
from itertools import chain, zip_longest
from datetime import datetime, timedelta
from operator import itemgetter

from dotenv import load_dotenv
import challonge

# Dotenv lets you create a file named ".env" in the same directory as this file, and populate it with data that gets added you your env vars.
# The challonge username and api keys are pulled from here or from env vars, so for local debugging you can use one set of data (and add it to your .gitignore)
# but on the live server you can either use your own .env file or just set env vars in the control panel or launcher
load_dotenv()

NEXT_MATCH_START = timedelta(minutes=1)
MATCH_DELAY = timedelta(minutes=3)

def most_recent_match_time(tournament):
    most_recent_match_time = datetime.min
    for m in tournament["matches"]:
        if m["state"] != "complete":
            continue
        match_time = m["updated_at"].replace(tzinfo=None)
        if match_time > most_recent_match_time:
            most_recent_match_time = match_time
    return most_recent_match_time


def interleave_matches(tournaments):
    least_recent_tournaments = []

    matches_list = [t["matches"] for t in sorted(tournaments.values(), key=most_recent_match_time)]
    for i, ml in enumerate(matches_list):
        matches_list[i] = sorted([m for m in ml if m["state"] == "open"], key=itemgetter("suggested_play_order"))
    interleaved_with_fill = zip_longest(*matches_list)
    list_of_tuples = chain.from_iterable(interleaved_with_fill)
    remove_fill = [x for x in list_of_tuples if x is not None]
    return remove_fill


def main():
    challonge.set_credentials(os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_API_KEY"))
    
    tournaments = challonge.tournaments.index(state="in_progress")
    if not tournaments:
        print("No in-progress tournaments found.")
        sys.exit()
    tournaments = {t["id"]: t for t in tournaments}

    for t in tournaments:
        # Populate matches
        matches = challonge.matches.index(t, state="all")
        # Populate participants
        participants = challonge.participants.index(t)
        participants = {p["id"]: p for p in participants}
        for y, match in enumerate(matches):
            matches[y]["player1_name"] = participants.get(match["player1_id"], {}).get("name", "???")
            matches[y]["player2_name"] = participants.get(match["player2_id"], {}).get("name", "???")
        tournaments[t]["matches"] = matches

    # Create combined match list
    ordered_matches = interleave_matches(tournaments)
    match_start = datetime.now() + NEXT_MATCH_START
    for i, match in enumerate(ordered_matches[:10]):
        tournament_name = tournaments.get(match["tournament_id"], {}).get("name")
        print("%s. %s VS %s - %s, %s" % (i + 1, match["player1_name"], match["player2_name"], match_start.strftime("%I:%M %p"), tournament_name))
        match_start += MATCH_DELAY


if __name__ == "__main__":
    main()
