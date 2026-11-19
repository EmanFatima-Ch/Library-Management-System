import authentication
import two_factor


def setup_function():
    authentication.users.clear()


def test_totp_rfc_vector_and_time_window():
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"

    assert two_factor.generate_totp(
        secret, timestamp=59, period=30, digits=8
    ) == "94287082"
    code = two_factor.generate_totp(secret, timestamp=59)
    assert two_factor.verify_totp(secret, code, timestamp=59)
    assert not two_factor.verify_totp(
        secret, "invalid", timestamp=59
    )


def test_account_requires_password_and_totp():
    secret = authentication.register_user("reader", "correct horse")
    code = two_factor.generate_totp(secret)

    assert authentication.authenticate("reader", "correct horse", code)
    assert not authentication.authenticate("reader", "wrong", code)
    assert not authentication.authenticate("reader", "correct horse", "000")
    assert authentication.register_user("reader", "another") is None
