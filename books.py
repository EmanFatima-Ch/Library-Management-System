books = []


def add_book(book_id, title, author):
    """Add a new book. Returns True if added, False if the ID already exists."""
    for book in books:
        if book["id"] == book_id:
            print("A book with this ID already exists.")
            return False

    books.append({"id": book_id, "title": title, "author": author, "available": True})
    print(f"Book '{title}' added.")
    return True


def view_books():
    """Print all books."""
    if not books:
        print("No books in the library.")
        return

    print("\n--- All Books ---")
    for book in books:
        status = "Available" if book["available"] else "Borrowed"
        print(f"ID: {book['id']} | {book['title']} by {book['author']} | {status}")


def remove_book(book_id):
    """Remove a book by ID. Returns True if removed, False otherwise."""
    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                print("This book is currently borrowed and cannot be removed.")
                return False
            books.remove(book)
            print(f"Book '{book['title']}' removed.")
            return True

    print("Book not found.")
    return False
