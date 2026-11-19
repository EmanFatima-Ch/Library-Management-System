import authentication
import books
import borrowing
import members
import storage


def setup_function():
    books.books.clear()
    members.members.clear()
    borrowing.borrowed_records.clear()
    authentication.users.clear()


def test_save_and_load_all_records(tmp_path):
    database_path = str(tmp_path / "library.db")
    books.books.append(
        {"id": 1, "title": "Dune", "author": "Frank Herbert",
         "available": False}
    )
    members.members.append({"id": 2, "name": "Ari"})
    borrowing.borrowed_records.append({"book_id": 1, "member_id": 2})
    authentication.users.append({
        "username": "reader",
        "password_hash": "hash",
        "totp_secret": "SECRET",
    })
    storage.save_data(
        database_path, books.books, members.members,
        borrowing.borrowed_records, authentication.users,
    )

    books.books.clear()
    members.members.clear()
    borrowing.borrowed_records.clear()
    authentication.users.clear()
    storage.load_data(
        database_path, books.books, members.members,
        borrowing.borrowed_records, authentication.users,
    )

    assert books.books[0]["id"] == 1
    assert books.books[0]["available"] is False
    assert members.members == [{"id": 2, "name": "Ari"}]
    assert borrowing.borrowed_records == [
        {"book_id": 1, "member_id": 2}
    ]
    assert authentication.users[0]["username"] == "reader"
