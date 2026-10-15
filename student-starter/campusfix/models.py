"""Domain model for CampusFix helpdesk requests."""
from dataclasses import asdict, dataclass

VALID_STATUSES = ("Open", "In Progress", "Resolved")
VALID_PRIORITIES = ("Low", "Medium", "High")

@dataclass
class Request:
    """A single helpdesk request reported by a campus community member."""
    id: int
    title: str
    category: str
    priority: str
    status: str
    description: str

    def to_dict(self) -> dict:
        """Return a JSON-friendly representation without changing the object."""
        return asdict(self)

    @classmethod
    def from_dict(cls, row: dict) -> "Request":
        """Build a request from a record loaded from storage."""
        required = {"id", "title", "category", "priority", "status", "description"}
        missing = required.difference(row)
        if missing:
            raise ValueError(f"Missing request fields: {', '.join(sorted(missing))}")
        return cls(**{key: row[key] for key in required})

    def is_open(self) -> bool:
        """Return whether this request still needs attention."""
        return self.status != "Resolved"
