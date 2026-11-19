import books
import borrowing
import members


def setup_function():
    books.books.clear()
    members.members.clear()
    borrowing.borrowed_records.clear()


def test_borrow_and_return_book():
    books.add_book(1, "Dune", "Frank Herbert")
    members.register_member(2, "Ari")

    assert borrowing.borrow_book(2, 1)
    assert not books.books[0]["available"]
    assert not borrowing.borrow_book(2, 1)
    assert borrowing.return_book(2, 1)
    assert books.books[0]["available"]
    assert borrowing.borrowed_records == []


def test_reject_unknown_member_or_book():
    assert not borrowing.borrow_book(2, 1)
    members.register_member(2, "Ari")
    assert not borrowing.borrow_book(2, 1)
