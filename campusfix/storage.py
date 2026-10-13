import json
from pathlib import Path
from .models import Request

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "requests.json"

def load_requests(path=DATA_FILE):
    """Load requests from JSON. Missing files produce an empty list."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        rows = json.load(f)
    return [Request(**row) for row in rows]

def save_requests(requests, path=DATA_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in requests], f, indent=2, ensure_ascii=False)
