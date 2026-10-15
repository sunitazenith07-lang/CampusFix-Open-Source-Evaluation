"""Small command-line entry point used to explore CampusFix."""
from .service import filter_requests, list_requests, summary

def main() -> None:
    requests = list_requests()
    print("CampusFix — Community Helpdesk")
    print(f"Loaded {len(requests)} requests")
    print("\nRequests:")
    for item in requests:
        print(f"#{item.id} [{item.status} | {item.priority}] {item.title} ({item.category})")
    query = input("\nSearch title (Enter to skip): ").strip()
    status = input("Status filter (Open/In Progress/Resolved, Enter to skip): ").strip() or None
    priority = input("Priority filter (Low/Medium/High, Enter to skip): ").strip() or None
    try:
        matches = filter_requests(requests, query=query, status=status, priority=priority)
    except ValueError as error:
        print(f"Invalid filter: {error}")
        return
    if not matches:
        print("No requests match the selected criteria.")
    for item in matches:
        print(f"#{item.id}: {item.title} [{item.status} | {item.priority}]")
    print("\nSummary:", summary(requests))

if __name__ == "__main__":
    main()
