from dataclasses import dataclass, asdict

@dataclass
class Request:
    id: int
    title: str
    category: str
    priority: str
    status: str
    description: str

    def to_dict(self):
        return asdict(self)
