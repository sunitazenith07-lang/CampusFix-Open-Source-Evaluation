import json
import pytest

from campusfix.models import Request, VALID_PRIORITIES, VALID_STATUSES
from campusfix.storage import load_requests, save_requests, find_request
from campusfix.service import (
    list_requests, update_status, find_by_title, filter_requests,
    summary,
)

def sample():
    return [
        Request(1, "Wi-Fi disconnects in library", "IT", "High", "Open", "Drops often"),
        Request(2, "Projector has no display", "Classroom", "Medium", "In Progress", "No image"),
        Request(3, "Lab keyboard missing", "Facilities", "Low", "Resolved", "Missing"),
        Request(4, "Student portal login fails", "IT", "High", "Open", "Cannot log in"),
        Request(5, "Wi-Fi access in auditorium", "IT", "Medium", "Resolved", "Guest network"),
        Request(6, "Broken chair in seminar room", "Facilities", "Low", "Open", "Unstable"),
    ]

# Model contract: 6 parameter cases
@pytest.mark.parametrize("field", ["id", "title", "category", "priority", "status", "description"])
def test_request_to_dict_contains_every_field(field):
    data = sample()[0].to_dict()
    assert field in data

@pytest.mark.parametrize("status,expected", [
    ("Open", True), ("In Progress", True), ("Resolved", False)
])
def test_is_open_matches_resolution_state(status, expected):
    item = sample()[0]
    item.status = status
    assert item.is_open() is expected

# Storage contract: 12 cases
def test_storage_round_trip(tmp_path):
    path = tmp_path / "requests.json"
    save_requests(sample(), path)
    assert [r.to_dict() for r in load_requests(path)] == [r.to_dict() for r in sample()]

def test_missing_storage_returns_empty_list(tmp_path):
    assert load_requests(tmp_path / "missing.json") == []

def test_storage_creates_parent_directories(tmp_path):
    path = tmp_path / "nested" / "deep" / "requests.json"
    save_requests(sample()[:1], path)
    assert path.exists()
    assert len(load_requests(path)) == 1

def test_storage_preserves_unicode(tmp_path):
    path = tmp_path / "requests.json"
    item = sample()[0]
    item.title = "Caf\u00e9 Wi-Fi \u2014 \u4e2d\u6587"
    save_requests([item], path)
    assert load_requests(path)[0].title == item.title

def test_storage_writes_a_json_list(tmp_path):
    path = tmp_path / "requests.json"
    save_requests(sample(), path)
    assert isinstance(json.loads(path.read_text(encoding="utf-8")), list)

def test_storage_rejects_non_list_json(tmp_path):
    path = tmp_path / "requests.json"
    path.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_requests(path)

def test_storage_surfaces_malformed_json(tmp_path):
    path = tmp_path / "requests.json"
    path.write_text("[broken", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_requests(path)

def test_storage_rejects_missing_required_fields(tmp_path):
    path = tmp_path / "requests.json"
    path.write_text('[{"id": 1, "title": "Missing fields"}]', encoding="utf-8")
    with pytest.raises(ValueError):
        load_requests(path)

@pytest.mark.parametrize("request_id,expected", [(1, 1), (2, 2), (6, 6), (999, None)])
def test_find_request_by_id(request_id, expected):
    found = find_request(sample(), request_id)
    assert (found.id if found else None) == expected

def test_save_does_not_mutate_input_list(tmp_path):
    original = sample()
    before = [r.to_dict() for r in original]
    save_requests(original, tmp_path / "requests.json")
    assert [r.to_dict() for r in original] == before

# List and status update contract: 10 cases
def test_list_requests_returns_a_new_list():
    items = sample()
    result = list_requests(items)
    assert result == items and result is not items

@pytest.mark.parametrize("status", VALID_STATUSES)
def test_update_status_accepts_each_valid_status(status):
    items = sample()
    updated = update_status(1, status, items)
    assert updated.status == status

@pytest.mark.parametrize("status", ["closed", "", "Done"])
def test_update_status_rejects_invalid_status(status):
    with pytest.raises(ValueError):
        update_status(1, status, sample())

def test_update_status_rejects_unknown_id():
    with pytest.raises(LookupError):
        update_status(999, "Open", sample())

def test_update_status_persists_when_using_default_storage(monkeypatch):
    import campusfix.service as service
    items = sample()
    saved = []
    monkeypatch.setattr(service, "load_requests", lambda: items)
    monkeypatch.setattr(service, "save_requests", lambda rows: saved.append(list(rows)))
    service.update_status(1, "Resolved")
    assert len(saved) == 1
    assert saved[0][0].status == "Resolved"

# Title search contract: 17 cases
@pytest.mark.parametrize("query", [
    "wi-fi", "WI-FI", "Wi-Fi", "library", "LIBRARY", "LiBrArY",
    "STUDENT PORTAL", "student portal"
])
def test_title_search_is_case_insensitive(query):
    matches = find_by_title(query, sample())
    assert matches

@pytest.mark.parametrize("query", [" Wi-Fi", "Wi-Fi ", "  library  ", " portal "])
def test_title_search_trims_surrounding_whitespace(query):
    assert find_by_title(query, sample())

@pytest.mark.parametrize("query,expected_ids", [
    ("Wi-Fi", [1, 5]), ("projector", [2]), ("chair", [6])
])
def test_title_search_returns_all_matching_substrings(query, expected_ids):
    assert [r.id for r in find_by_title(query, sample())] == expected_ids

def test_empty_title_query_returns_all_requests():
    assert len(find_by_title("", sample())) == 6

def test_title_search_returns_empty_for_no_match():
    assert find_by_title("spaceship", sample()) == []

# Filtering contract: 22 cases
@pytest.mark.parametrize("status,expected", [
    ("Open", [1, 4, 6]), ("In Progress", [2]), ("Resolved", [3, 5])
])
def test_filter_by_status(status, expected):
    assert [r.id for r in filter_requests(sample(), status=status)] == expected

@pytest.mark.parametrize("priority,expected", [
    ("High", [1, 4]), ("Medium", [2, 5]), ("Low", [3, 6])
])
def test_filter_by_priority(priority, expected):
    assert [r.id for r in filter_requests(sample(), priority=priority)] == expected

@pytest.mark.parametrize("status,priority,expected", [
    ("Open", "High", [1, 4]), ("Open", "Low", [6]),
    ("Resolved", "Medium", [5]), ("In Progress", "Medium", [2]),
    ("Resolved", "High", []), ("In Progress", "Low", []),
])
def test_status_and_priority_filters_combine(status, priority, expected):
    assert [r.id for r in filter_requests(sample(), status=status, priority=priority)] == expected

@pytest.mark.parametrize("query,status,priority,expected", [
    ("wifi", "Open", "High", [1]), ("WIFI", "Resolved", "Medium", [5]),
    ("projector", "In Progress", "Medium", [2]), ("chair", "Open", "Low", [6]),
])
def test_search_status_and_priority_all_combine(query, status, priority, expected):
    assert [r.id for r in filter_requests(sample(), query, status, priority)] == expected

@pytest.mark.parametrize("status", ["Done", "", "closed"])
def test_filter_rejects_invalid_status(status):
    with pytest.raises(ValueError):
        filter_requests(sample(), status=status)

@pytest.mark.parametrize("priority", ["Urgent", "", "P0"])
def test_filter_rejects_invalid_priority(priority):
    with pytest.raises(ValueError):
        filter_requests(sample(), priority=priority)

def test_filter_blank_query_does_not_remove_results():
    assert len(filter_requests(sample(), query="")) == 6

def test_filter_no_matches_returns_empty_list():
    assert filter_requests(sample(), query="nonexistent") == []

# Summary contract: 9 cases
def test_summary_total_includes_resolved_requests():
    assert summary(sample())["total"] == 6

@pytest.mark.parametrize("status,expected", [("Open", 3), ("In Progress", 1), ("Resolved", 2)])
def test_summary_counts_each_status(status, expected):
    assert summary(sample())["by_status"][status] == expected

@pytest.mark.parametrize("priority,expected", [("High", 2), ("Medium", 2), ("Low", 2)])
def test_summary_counts_each_priority(priority, expected):
    assert summary(sample())["by_priority"][priority] == expected

@pytest.mark.parametrize("category,expected", [("IT", 3), ("Classroom", 1), ("Facilities", 2)])
def test_summary_counts_each_category(category, expected):
    assert summary(sample())["by_category"][category] == expected

def test_summary_handles_empty_list():
    result = summary([])
    assert result["total"] == 0
    assert all(value == 0 for value in result["by_status"].values())
    assert all(value == 0 for value in result["by_priority"].values())
    assert result["by_category"] == {}

# Filter robustness contract: 4 cases
def test_filter_preserves_original_order():
    result = filter_requests(sample(), status="Open")
    assert [r.id for r in result] == [1, 4, 6]

def test_filter_does_not_mutate_source_list():
    original = sample()
    before = [r.to_dict() for r in original]
    filter_requests(original, status="Open", priority="High")
    assert [r.to_dict() for r in original] == before

def test_filter_with_no_criteria_returns_all_requests():
    assert [r.id for r in filter_requests(sample())] == [1, 2, 3, 4, 5, 6]

def test_filter_uses_default_storage_when_no_list_is_supplied(monkeypatch):
    import campusfix.service as service
    items = sample()
    monkeypatch.setattr(service, "load_requests", lambda: items)
    assert [r.id for r in service.filter_requests(status="Open")] == [1, 4, 6]

# Extended edge-case contract: deliberately tests interactions across modules.
def test_model_round_trip_preserves_all_values():
    item = sample()[0]
    assert Request.from_dict(item.to_dict()) == item

@pytest.mark.parametrize("query,expected_ids", [
    ("wifi", [1, 5]), ("Wi-Fi", [1, 5]), ("  LIBRARY  ", [1]),
])
def test_search_normalizes_query_and_title(query, expected_ids):
    assert [r.id for r in find_by_title(query, sample())] == expected_ids

def test_search_none_is_treated_as_empty_query():
    assert len(find_by_title(None, sample())) == 6

def test_search_does_not_match_description_only():
    assert find_by_title("Drops often", sample()) == []

@pytest.mark.parametrize("query,status,priority,expected", [
    ("wifi", "Open", "High", [1]),
    ("wifi", "Resolved", "Medium", [5]),
    ("portal", "Open", "High", [4]),
    ("chair", "Resolved", "Low", []),
])
def test_combined_filters_are_case_insensitive(query, status, priority, expected):
    assert [r.id for r in filter_requests(sample(), query, status, priority)] == expected

def test_filter_rejects_invalid_priority_without_returning_partial_results():
    with pytest.raises(ValueError):
        filter_requests(sample(), status="Open", priority="Critical")

def test_update_status_does_not_change_other_records():
    items = sample()
    before = [r.to_dict() for r in items[1:]]
    update_status(1, "Resolved", items)
    assert [r.to_dict() for r in items[1:]] == before

def test_update_status_keeps_same_id_and_title():
    items = sample()
    updated = update_status(2, "Resolved", items)
    assert (updated.id, updated.title) == (2, "Projector has no display")

def test_update_status_default_storage_survives_reload(tmp_path, monkeypatch):
    import campusfix.service as service
    path = tmp_path / "requests.json"
    save_requests(sample(), path)
    monkeypatch.setattr(service, "load_requests", lambda: load_requests(path))
    monkeypatch.setattr(service, "save_requests", lambda rows: save_requests(rows, path))
    service.update_status(1, "Resolved")
    assert load_requests(path)[0].status == "Resolved"

def test_summary_totals_equal_sum_of_status_counts():
    result = summary(sample())
    assert result["total"] == sum(result["by_status"].values())

def test_summary_counts_categories_case_consistently():
    items = sample()
    items.append(Request(7, "Extra", "it", "Low", "Open", "Example"))
    result = summary(items)
    assert result["by_category"].get("IT", 0) + result["by_category"].get("it", 0) == 4

def test_storage_rejects_duplicate_ids(tmp_path):
    path = tmp_path / "requests.json"
    rows = [sample()[0].to_dict(), sample()[0].to_dict()]
    path.write_text(json.dumps(rows), encoding="utf-8")
    with pytest.raises(ValueError):
        load_requests(path)

def test_storage_rejects_non_object_record(tmp_path):
    path = tmp_path / "requests.json"
    path.write_text(json.dumps(["not-an-object"]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_requests(path)

def test_storage_rejects_invalid_status_in_record(tmp_path):
    path = tmp_path / "requests.json"
    row = sample()[0].to_dict()
    row["status"] = "Done"
    path.write_text(json.dumps([row]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_requests(path)

def test_storage_rejects_invalid_priority_in_record(tmp_path):
    path = tmp_path / "requests.json"
    row = sample()[0].to_dict()
    row["priority"] = "Urgent"
    path.write_text(json.dumps([row]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_requests(path)

def test_save_and_load_preserve_order(tmp_path):
    path = tmp_path / "requests.json"
    save_requests(sample(), path)
    assert [r.id for r in load_requests(path)] == [1, 2, 3, 4, 5, 6]

def test_unresolved_priority_view_excludes_resolved_and_sorts(monkeypatch):
    from campusfix.service import unresolved_by_priority
    result = unresolved_by_priority(sample())
    assert [r.id for r in result] == [1, 4, 2, 6]

def test_unresolved_priority_view_is_not_mutating_source():
    from campusfix.service import unresolved_by_priority
    items = sample()
    before = [r.to_dict() for r in items]
    unresolved_by_priority(items)
    assert [r.to_dict() for r in items] == before
