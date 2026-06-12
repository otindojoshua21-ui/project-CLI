import json
import os
from models.user import User

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def save_data(users: list[User]):
    """Persist users to JSON."""
    ensure_data_dir()

    with open(DATA_FILE, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=2)

def load_data():
    """Load users from JSON file."""
    ensure_data_dir()

    try:
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)

        users = [User.from_dict(u) for u in raw]

        if users:
            User._id_counter = max(u.id for u in users) + 1

        return users

    except (FileNotFoundError, json.JSONDecodeError):
        return []