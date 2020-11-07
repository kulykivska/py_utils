import json
from config.config import get_path_from_base


def load_json(file_path: str) -> dict:
    with open(get_path_from_base(file_path), 'r') as f:
        return json.load(f)
