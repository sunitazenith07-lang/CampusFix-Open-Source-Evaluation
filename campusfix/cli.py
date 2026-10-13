from .service import list_requests, find_by_title, update_status, summary

def main():
    requests = list_requests()
    print("CampusFix — Community Helpdesk")
    print(f"Loaded {len(requests)} requests")
    print("\nRequests:")
    for r in requests:
        print(f"#{r.id} [{r.status} | {r.priority}] {r.title} ({r.category})")
    print("\nTitle search demo: type a word, or press Enter to skip.")
    query = input("> ").strip()
    if query:
        matches = find_by_title(query, requests)
        print(f"{len(matches)} match(es)")
        for r in matches:
            print(f"#{r.id}: {r.title}")
    print("\nSummary:", summary(requests))
    print("\nThis starter CLI is intentionally small. Improve the service and demonstrate your features.")

if __name__ == "__main__":
    main()
