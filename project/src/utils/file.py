import json
from pathlib import Path

FILE = Path(__file__).parent.parent / "data.json"

def read_data():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "users": [],
            "products": [],
            "orders": [],
            "reviews": [],
            "shops": []
        }

def write_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)