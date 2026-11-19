"""Password authentication and account management."""

import hashlib
import hmac
import os

import two_factor

users = []
_HASH_ITERATIONS = 200000


def _hash_password(password, salt=None):
    if not isinstance(password, str) or not password:
        raise ValueError("Password must not be empty.")
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt),
        _HASH_ITERATIONS,
    ).hex()
    return "{}${}${}".format(_HASH_ITERATIONS, salt, digest)


def _verify_password(password, encoded_hash):
    try:
        iterations, salt, expected = encoded_hash.split("$", 2)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt),
            int(iterations),
        ).hex()
    except (AttributeError, TypeError, ValueError):
        return False
    return hmac.compare_digest(actual, expected)


def register_user(username, password, secret=None):
    """Register a user and return their TOTP setup secret, or None if taken."""
    username = username.strip() if isinstance(username, str) else ""
    if not username or not isinstance(password, str) or not password:
        raise ValueError("Username and password must not be empty.")
    if any(user["username"] == username for user in users):
        return None
    secret = secret or two_factor.generate_secret()
    users.append({
        "username": username,
        "password_hash": _hash_password(password),
        "totp_secret": secret,
    })
    return secret


def authenticate(username, password, code):
    """Return whether password and time-based one-time code are valid."""
    user = next(
        (item for item in users if item["username"] == username), None
    )
    if user is None or not _verify_password(password, user["password_hash"]):
        return False
    return two_factor.verify_totp(user["totp_secret"], code)
