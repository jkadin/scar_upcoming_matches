import pickle
from pathlib import Path


tournament_urls = ["r5vq4p1l", "4vljhp3k"]
for tournament_url in tournament_urls:
    print("*****************************")
    pickle_file_path = Path(__file__).parent / f"tournaments{tournament_url}.pkl"
    print(pickle_file_path)
    with open(pickle_file_path, "rb") as f:
        tournaments = pickle.load(f)
    print(tournaments["id"], tournaments["name"])

print("=================================================================")

for tournament_url in tournament_urls:
    pickle_file_path = Path(__file__).parent / f"matches{tournament_url}.pkl"
    with open(pickle_file_path, "rb") as f:
        matches = pickle.load(f)
    print(len(matches))
    for match in matches:
        print(
            match.get("id"),
            match.get("state"),
            match.get("player1_id"),
            match.get("player2_id"),
            match.get("suggested_play_order"),
            match.get("calculated_play_order"),
            match.get("player1_is_prereq_match_loser"),
            match.get("player1_prereq_match_id"),
            match.get("player2_is_prereq_match_loser"),
            match.get("player2_prereq_match_id"),
        )
    print("*****************************")

print("#################################################################")

for tournament_url in tournament_urls:
    pickle_file_path = Path(__file__).parent / f"participants{tournament_url}.pkl"
    with open(pickle_file_path, "rb") as f:
        participants = pickle.load(f)
    print(len(participants))
    for participant in participants:
        print(participant.get("name"))
    print("*****************************")
