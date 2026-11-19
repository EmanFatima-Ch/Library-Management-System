import books
import search


def setup_function():
    books.books.clear()
    books.books.extend([
        {"id": 1, "title": "Dune", "author": "Frank Herbert",
         "available": True},
        {"id": 2, "title": "Dune Messiah", "author": "Frank Herbert",
         "available": False},
        {"id": 3, "title": "Foundation", "author": "Isaac Asimov",
         "available": True},
    ])


def test_search_is_case_insensitive_and_returns_matches():
    assert [book["id"] for book in search.search_by_title("dUnE")] == [1, 2]
    assert [book["id"] for book in search.search_by_author("asimov")] == [3]
    assert search.search_by_title("missing") == []
