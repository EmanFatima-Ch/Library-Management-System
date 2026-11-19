"""RFC 6238-compatible time-based one-time password helpers."""

import base64
import hashlib
import hmac
import os
import struct
import time


def generate_secret():
    """Return a random Base32 secret suitable for authenticator apps."""
    return base64.b32encode(os.urandom(20)).decode("ascii").rstrip("=")


def generate_totp(secret, timestamp=None, period=30, digits=6):
    """Generate a TOTP code for the supplied secret and time."""
    if period <= 0 or digits <= 0:
        raise ValueError("Period and digit count must be positive.")
    normalized = secret.strip().upper()
    normalized += "=" * ((8 - len(normalized) % 8) % 8)
    key = base64.b32decode(normalized, casefold=True)
    counter = int((time.time() if timestamp is None else timestamp) // period)
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    binary = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(binary % (10 ** digits)).zfill(digits)


def verify_totp(secret, code, timestamp=None, window=1, period=30, digits=6):
    """Verify a TOTP code, allowing adjacent time steps for clock drift."""
    if not isinstance(code, str) or not code.isdigit():
        return False
    if len(code) != digits or window < 0:
        return False
    current_time = time.time() if timestamp is None else timestamp
    return any(
        hmac.compare_digest(
            generate_totp(
                secret, current_time + offset * period, period, digits
            ),
            code,
        )
        for offset in range(-window, window + 1)
    )
