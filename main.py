"""Command-line entry point for the library management system."""

import getpass

import authentication
import books
import borrowing
import members
import search
import storage


def _read_integer(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None


def _save_data(database_path):
    storage.save_data(
        database_path,
        books.books,
        members.members,
        borrowing.borrowed_records,
        authentication.users,
    )


def _authenticate(database_path):
    if not authentication.users:
        print("No accounts exist. Create the first account.")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        secret = authentication.register_user(username, password)
        if secret is None:
            print("Account could not be created.")
            return False
        print("Authenticator setup secret: " + secret)
        print("Add this secret to an authenticator app before continuing.")
        _save_data(database_path)

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    code = input("Authenticator code: ").strip()
    if authentication.authenticate(username, password, code):
        return True
    print("Invalid username, password, or authenticator code.")
    return False


def _show_menu():
    print(
        "\n1. Add book\n"
        "2. View books\n"
        "3. Remove book\n"
        "4. Register member\n"
        "5. View members\n"
        "6. Borrow book\n"
        "7. Return book\n"
        "8. View borrowed books\n"
        "9. Search books\n"
        "0. Save and exit"
    )


def run_cli(database_path=storage.DEFAULT_DATABASE):
    """Run the interactive, persistent library application."""
    storage.load_data(
        database_path,
        books.books,
        members.members,
        borrowing.borrowed_records,
        authentication.users,
    )
    print("Library Management System")
    if not _authenticate(database_path):
        return

    while True:
        _show_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            book_id = _read_integer("Book ID: ")
            if book_id is not None:
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                books.add_book(book_id, title, author)
                _save_data(database_path)
        elif choice == "2":
            books.view_books()
        elif choice == "3":
            book_id = _read_integer("Book ID: ")
            if book_id is not None and books.remove_book(book_id):
                _save_data(database_path)
        elif choice == "4":
            member_id = _read_integer("Member ID: ")
            if member_id is not None:
                members.register_member(
                    member_id, input("Member name: ").strip()
                )
                _save_data(database_path)
        elif choice == "5":
            members.view_members()
        elif choice == "6":
            member_id = _read_integer("Member ID: ")
            book_id = _read_integer("Book ID: ")
            if (member_id is not None and book_id is not None
                    and borrowing.borrow_book(member_id, book_id)):
                _save_data(database_path)
        elif choice == "7":
            member_id = _read_integer("Member ID: ")
            book_id = _read_integer("Book ID: ")
            if (member_id is not None and book_id is not None
                    and borrowing.return_book(member_id, book_id)):
                _save_data(database_path)
        elif choice == "8":
            borrowing.view_borrowed_books()
        elif choice == "9":
            keyword = input("Search keyword: ").strip()
            field = input("Search by title or author? ").strip().lower()
            if field == "title":
                search.search_by_title(keyword)
            elif field == "author":
                search.search_by_author(keyword)
            else:
                print("Choose either title or author.")
        elif choice == "0":
            _save_data(database_path)
            print("Library data saved.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    run_cli()
