from books import books


def print_results(results):
    if not results:
        print("No matching books found.")
        return

    print("\n--- Search Results ---")
    for book in results:
        status = "Available" if book["available"] else "Borrowed"
        print(f"ID: {book['id']} | {book['title']} by {book['author']} | {status}")
def search_by_title(keyword):
    """Find books whose title contains the keyword (not case-sensitive)."""
    results = [b for b in books if keyword.lower() in b["title"].lower()]
    print_results(results)
    return results


def search_by_author(keyword):
    """Find books whose author contains the keyword (not case-sensitive)."""
    results = [b for b in books if keyword.lower() in b["author"].lower()]
    print_results(results)
    return results