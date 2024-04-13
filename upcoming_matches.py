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

# I need your .env file

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

    matches_list = [
        t["matches"] for t in sorted(tournaments.values(), key=most_recent_match_time)
    ]
    for i, ml in enumerate(matches_list):
        matches_list[i] = sorted(
            [m for m in ml if m["state"] == "open"],
            key=itemgetter("suggested_play_order"),
        )
    interleaved_with_fill = zip_longest(*matches_list)
    list_of_tuples = chain.from_iterable(interleaved_with_fill)
    remove_fill = [x for x in list_of_tuples if x is not None]
    return remove_fill


def create_svg_from_output(output):
    svg = []
    svg.append(
        r'<svg id="root" xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" xmlns:xlink="http://www.w3.org/1999/xlink">'
    )
    svg.append(
        r'<rect x="0" y="0" width="1920" height="1080" stroke="red" stroke-width="3px" fill="white"/>'
    )
    svg.append(
        r'<text x="0" y="6%" dominant-baseline="middle" text-anchor="middle" font-size="55" >'
    )
    for i, line in enumerate(output):
        if i == 0:
            svg.append(r'<tspan x="50%">' + line + r"</tspan>")
        else:
            svg.append(r'<tspan x="50%" dy="1.9em">' + line + r"</tspan>")
    svg.append(r"</text>")
    svg.append(r"</svg>")
    svg = "\n".join(svg)
    return svg


def main():
    challonge.set_credentials(
        os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_API_KEY")
    )

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
            matches[y]["player1_name"] = participants.get(match["player1_id"], {}).get(
                "name", "???"
            )
            matches[y]["player2_name"] = participants.get(match["player2_id"], {}).get(
                "name", "???"
            )
        tournaments[t]["matches"] = matches

    # Create combined match list
    ordered_matches = interleave_matches(tournaments)
    match_start = datetime.now() + NEXT_MATCH_START
    output = []
    for i, match in enumerate(ordered_matches[:10]):
        tournament_name = tournaments.get(match["tournament_id"], {}).get("name")
        output.append(
            "%s. %s vs %s - %s (%s)"
            % (
                i + 1,
                match["player1_name"],
                match["player2_name"],
                match_start.strftime("%I:%M %p"),
                tournament_name,
            )
        )
        match_start += MATCH_DELAY

    svg = create_svg_from_output(output)
    with open("current_matches.svg", mode="w") as f:
        f.write(svg)

    print("Current open match list written to 'current_matches.svg'")


if __name__ == "__main__":
    main()
