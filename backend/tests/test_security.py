from app.security import create_access_token, decode_access_token, hash_password, verify_password


def test_hashed_password_is_not_plain_text():
    assert hash_password("secret123") != "secret123"


def test_correct_password_verifies():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)


def test_wrong_password_does_not_verify():
    hashed = hash_password("secret123")
    assert not verify_password("wrong-password", hashed)


def test_token_round_trip_returns_user_id():
    token = create_access_token(42)
    assert decode_access_token(token) == 42


def test_expired_token_is_rejected():
    token = create_access_token(42, expires_in_minutes=-1)
    assert decode_access_token(token) is None


def test_tampered_token_is_rejected():
    token = create_access_token(42)
    assert decode_access_token(token + "x") is None