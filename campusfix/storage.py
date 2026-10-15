"""JSON storage helpers for CampusFix."""
import json
from pathlib import Path
from typing import Iterable
from .models import Request

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "requests.json"

def load_requests(path: Path = DATA_FILE) -> list[Request]:
    """Load request records. A missing file is treated as an empty store."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        rows = json.load(handle)
    if not isinstance(rows, list):
        raise ValueError("Request storage must contain a JSON list")
    return [Request.from_dict(row) for row in rows]

def save_requests(requests: Iterable[Request], path: Path = DATA_FILE) -> None:
    """Persist request records as readable UTF-8 JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [request.to_dict() for request in requests]
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)

def find_request(requests: Iterable[Request], request_id: int) -> Request | None:
    """Return a request by ID, or None when it does not exist."""
    return next((item for item in requests if item.id == request_id), None)
