"""SQLite persistence helpers for library and authentication data."""

import json
import sqlite3

DEFAULT_DATABASE = "library.db"

_TABLES = {
    "books": """
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL,
            available INTEGER NOT NULL
        )
    """,
    "members": """
        CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY, name TEXT NOT NULL
        )
    """,
    "borrowed_records": """
        CREATE TABLE IF NOT EXISTS borrowed_records (
            book_id TEXT NOT NULL, member_id TEXT NOT NULL
        )
    """,
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, password_hash TEXT NOT NULL,
            totp_secret TEXT NOT NULL
        )
    """,
}


def _identifier(value):
    return json.dumps(value, separators=(",", ":"))


def _decode_identifier(value):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return value


def load_data(database_path, book_list, member_list, borrow_list, user_list):
    """Load persisted records into the supplied compatibility lists."""
    with sqlite3.connect(database_path) as connection:
        for statement in _TABLES.values():
            connection.execute(statement)
        loaded_books = [
            {"id": _decode_identifier(row[0]), "title": row[1],
             "author": row[2], "available": bool(row[3])}
            for row in connection.execute(
                "SELECT id, title, author, available FROM books"
            )
        ]
        loaded_members = [
            {"id": _decode_identifier(row[0]), "name": row[1]}
            for row in connection.execute("SELECT id, name FROM members")
        ]
        loaded_borrows = [
            {"book_id": _decode_identifier(row[0]),
             "member_id": _decode_identifier(row[1])}
            for row in connection.execute(
                "SELECT book_id, member_id FROM borrowed_records"
            )
        ]
        loaded_users = [
            {"username": row[0], "password_hash": row[1],
             "totp_secret": row[2]}
            for row in connection.execute(
                "SELECT username, password_hash, totp_secret FROM users"
            )
        ]
    book_list[:] = loaded_books
    member_list[:] = loaded_members
    borrow_list[:] = loaded_borrows
    user_list[:] = loaded_users


def save_data(database_path, book_list, member_list, borrow_list, user_list):
    """Atomically replace persisted records with the supplied lists."""
    with sqlite3.connect(database_path) as connection:
        for statement in _TABLES.values():
            connection.execute(statement)
        statements = (
            ("books", "INSERT INTO books VALUES (?, ?, ?, ?)",
             [(_identifier(book["id"]), book["title"], book["author"],
               int(book["available"])) for book in book_list]),
            ("members", "INSERT INTO members VALUES (?, ?)",
             [(_identifier(member["id"]), member["name"])
              for member in member_list]),
            ("borrowed_records",
             "INSERT INTO borrowed_records VALUES (?, ?)",
             [(_identifier(record["book_id"]),
               _identifier(record["member_id"])) for record in borrow_list]),
            ("users", "INSERT INTO users VALUES (?, ?, ?)",
             [(user["username"], user["password_hash"], user["totp_secret"])
              for user in user_list]),
        )
        for table, insert_sql, rows in statements:
            connection.execute("DELETE FROM " + table)
            connection.executemany(insert_sql, rows)
