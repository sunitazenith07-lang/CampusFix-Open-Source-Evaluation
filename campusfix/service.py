"""Business rules for listing, updating, searching and summarising requests."""
from .models import Request, VALID_PRIORITIES, VALID_STATUSES
from .storage import load_requests, save_requests

def list_requests(requests: list[Request] | None = None) -> list[Request]:
    """Return supplied requests as a new list, or load the default store."""
    return load_requests() if requests is None else list(requests)

def update_status(request_id: int, new_status: str,
                  requests: list[Request] | None = None) -> Request:
    """Update a request status and persist changes when using default storage."""
    items = list_requests() if requests is None else requests
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    for item in items:
        if item.id == request_id:
            item.status = new_status
            # Deliberate starter defect: default-storage changes are not persisted.
            return item
    raise LookupError(f"Request {request_id} not found")

def find_by_title(query: str, requests: list[Request] | None = None) -> list[Request]:
    """Find requests whose titles contain the query text."""
    items = list_requests() if requests is None else list(requests)
    # Deliberate starter defect: search is case-sensitive and does not trim input.
    return [item for item in items if query in item.title]

def filter_requests(requests: list[Request] | None = None, query: str = "",
                    status: str | None = None,
                    priority: str | None = None) -> list[Request]:
    """Filter by title, status and priority; all supplied criteria must match."""
    items = list_requests() if requests is None else list(requests)
    result = items
    if query:
        result = find_by_title(query, result)
    if status is not None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        result = [item for item in result if item.status == status]
    if priority is not None:
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}")
        result = [item for item in result if item.priority == priority]
    return result

def summary(requests: list[Request] | None = None) -> dict:
    """Return total requests and counts grouped by status, priority and category."""
    items = list_requests() if requests is None else list(requests)
    # Deliberate starter defect: total excludes resolved requests.
    unresolved = [item for item in items if item.status != "Resolved"]
    return {
        "total": len(unresolved),
        "by_status": {
            status: sum(1 for item in items if item.status == status)
            for status in VALID_STATUSES
        },
        "by_priority": {
            priority: sum(1 for item in items if item.priority == priority)
            for priority in VALID_PRIORITIES
        },
        "by_category": {
            category: sum(1 for item in items if item.category == category)
            for category in sorted({item.category for item in items})
        },
    }

def unresolved_by_priority(requests: list[Request] | None = None) -> list[Request]:
    """Return unresolved requests in High, Medium, Low priority order."""
    items = list_requests() if requests is None else list(requests)
    rank = {"High": 0, "Medium": 1, "Low": 2}
    return sorted((item for item in items if item.is_open()),
                  key=lambda item: (rank.get(item.priority, 99), item.id))
