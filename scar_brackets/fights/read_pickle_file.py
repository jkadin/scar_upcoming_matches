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
    print(len(matches), type(matches))
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
