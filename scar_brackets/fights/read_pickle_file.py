import pickle
from pathlib import Path

pickle_file_path = Path(__file__).parent / "matches_data13874863.pkl"
with open(pickle_file_path, "rb") as f:
    matches_data = pickle.load(f)
    print(matches_data)
