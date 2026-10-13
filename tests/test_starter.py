import json
from campusfix.models import Request
from campusfix.service import list_requests, summary
from campusfix.storage import load_requests, save_requests

def sample():
    return [
        Request(1, "Wi-Fi issue", "IT", "High", "Open", "Cannot connect"),
        Request(2, "Projector issue", "Classroom", "Medium", "Resolved", "No display"),
    ]

def test_request_to_dict_has_expected_fields():
    data = sample()[0].to_dict()
    assert data["id"] == 1
    assert data["title"] == "Wi-Fi issue"
    assert data["status"] == "Open"

def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "requests.json"
    original = sample()
    save_requests(original, path)
    loaded = load_requests(path)
    assert [r.to_dict() for r in loaded] == [r.to_dict() for r in original]

def test_list_requests_returns_copy_for_supplied_list():
    original = sample()
    returned = list_requests(original)
    assert returned == original
    assert returned is not original

def test_summary_contains_status_and_priority_buckets():
    result = summary(sample())
    assert result["by_status"]["Open"] == 1
    assert result["by_status"]["Resolved"] == 1
    assert result["by_priority"]["High"] == 1
    assert result["by_priority"]["Medium"] == 1
