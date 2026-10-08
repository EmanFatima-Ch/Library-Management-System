# borrowing.py - Issue #3: Borrow and Return
# Uses the lists from books.py and members.py
# record = {"book_id": int, "member_id": int}

from books import books
from members import members

borrowed_records = []


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def find_member(member_id):
    for member in members:
        if member["id"] == member_id:
            return member
    return None
" this will find members"

def borrow_book(member_id, book_id):
    member = find_member(member_id)
    book = find_book(book_id)

    if member is None:
        print("Member not found.")
        return False
    if book is None:
        print("Book not found.")
        return False
    if not book["available"]:
        print("Sorry, this book is already borrowed.")
        return False

    book["available"] = False
    borrowed_records.append({"book_id": book_id, "member_id": member_id})
    print(f"{member['name']} borrowed '{book['title']}'.")
    return True


def return_book(member_id, book_id):
    for record in borrowed_records:
        if record["book_id"] == book_id and record["member_id"] == member_id:
            borrowed_records.remove(record)
            find_book(book_id)["available"] = True
            print("Book returned successfully.")
            return True

    print("No matching borrow record found.")
    return False


def view_borrowed_books():
    if not borrowed_records:
        print("No books are currently borrowed.")
        return

    print("\n--- Borrowed Books ---")
    for record in borrowed_records:
        book = find_book(record["book_id"])
        member = find_member(record["member_id"])
        print(f"'{book['title']}' borrowed by {member['name']}")
