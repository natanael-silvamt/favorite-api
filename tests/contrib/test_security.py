from datetime import timedelta

import jwt
import pytest

from src.contrib.security import ALGORITHM, create_access_token, get_password_hash, pwd_context, verify_password


def test_security_create_access_token_with_success(mock_settings, mock_datetime) -> None:
    test_subject = "user123"
    test_expires_delta = timedelta(minutes=30)

    token = create_access_token(subject=test_subject, expires_delta=test_expires_delta)
    decoded = jwt.decode(token, mock_settings.SECRET_KEY, algorithms=[ALGORITHM])

    assert isinstance(token, str)
    assert decoded['sub'] == test_subject
    assert decoded['exp'] == int((mock_datetime + test_expires_delta).timestamp())


@pytest.mark.usefixtures('mock_datetime')
def test_security_create_access_token_with_non_string_subject(mock_settings) -> None:
    test_subject = 12345
    test_expires_delta = timedelta(minutes=30)

    token = create_access_token(subject=test_subject, expires_delta=test_expires_delta)
    decoded = jwt.decode(token, mock_settings.SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == str(test_subject)


def test_security_verify_password_with_success() -> None:
    plain_password = "my-password"
    hashed_password = pwd_context.hash(plain_password)

    result = verify_password(plain_password=plain_password, hashed_password=hashed_password)

    assert result is True


def test_security_verify_password_with_incorrect() -> None:
    plain_password = "my-password"
    wrong_password = "wrong-password"
    hashed_password = pwd_context.hash(plain_password)

    result = verify_password(plain_password=wrong_password, hashed_password=hashed_password)

    assert result is False


def test_security_get_password_hash_with_success() -> None:
    password = "secure-password"

    hashed = get_password_hash(password=password)

    assert isinstance(hashed, str)
    assert hashed != password
    assert pwd_context.verify(password, hashed) is True
