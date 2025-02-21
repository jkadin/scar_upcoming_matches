import challonge
import pickle
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()
challonge.set_credentials(
    os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_API_KEY")
)

tournament_urls = ["r5vq4p1l", "4vljhp3k"]
for tournament_url in tournament_urls:
    tournaments = challonge.tournaments.show(tournament=f"/{tournament_url}")
    pickle_file_path = Path(__file__).parent / f"tournaments{tournament_url}.pkl"
    with open(pickle_file_path, "wb") as f:
        pickle.dump(tournaments, f)

for tournament_url in tournament_urls:
    matches = challonge.matches.index(tournament=f"/{tournament_url}")
    pickle_file_path = Path(__file__).parent / f"matches{tournament_url}.pkl"
    with open(pickle_file_path, "wb") as f:
        pickle.dump(matches, f)

for tournament_url in tournament_urls:
    participants = challonge.participants.index(tournament=f"/{tournament_url}")
    pickle_file_path = Path(__file__).parent / f"participants{tournament_url}.pkl"
    with open(pickle_file_path, "wb") as f:
        pickle.dump(participants, f)
