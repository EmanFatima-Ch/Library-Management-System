import books


def setup_function():
    books.books.clear()


def test_add_remove_book():
    assert books.add_book(1, "Dune", "Frank Herbert")
    assert not books.add_book(1, "Other", "Writer")
    assert books.books[0]["available"] is True
    assert books.remove_book(1)
    assert books.books == []


def test_cannot_remove_borrowed_book():
    books.add_book(1, "Dune", "Frank Herbert")
    books.books[0]["available"] = False

    assert not books.remove_book(1)
    assert len(books.books) == 1
