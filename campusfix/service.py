from .storage import load_requests, save_requests

VALID_STATUSES = {"Open", "In Progress", "Resolved"}
VALID_PRIORITIES = {"Low", "Medium", "High"}

def list_requests(requests=None):
    return load_requests() if requests is None else list(requests)

def update_status(request_id, new_status, requests=None):
    """Update one request's status and persist it."""
    items = list_requests() if requests is None else requests
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    for item in items:
        if item.id == request_id:
            item.status = new_status
            # BUG: the changed list is not persisted when default storage is used.
            if requests is not None:
                return item
            return item
    raise LookupError(f"Request {request_id} not found")

def find_by_title(query, requests=None):
    """Find requests whose titles contain query."""
    items = list_requests() if requests is None else requests
    # BUG: search is case-sensitive.
    return [r for r in items if query in r.title]

def summary(requests=None):
    """Return a small count summary for requests."""
    items = list_requests() if requests is None else requests
    # BUG: total incorrectly counts only unresolved requests.
    unresolved = [r for r in items if r.status != "Resolved"]
    return {
        "total": len(unresolved),
        "by_status": {status: sum(1 for r in items if r.status == status)
                      for status in sorted(VALID_STATUSES)},
        "by_priority": {priority: sum(1 for r in items if r.priority == priority)
                        for priority in sorted(VALID_PRIORITIES)},
    }
