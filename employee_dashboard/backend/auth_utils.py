"""Password hashing utilities for the single configured dashboard account."""

import hashlib
import hmac
import secrets

HASH_ITERATIONS = 310_000
_HASH_NAME = "pbkdf2_sha256"


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, HASH_ITERATIONS)
    return f"{_HASH_NAME}${HASH_ITERATIONS}${salt.hex()}${digest.hex()}"


def validate_password_hash(encoded_hash: str) -> None:
    try:
        name, iterations_text, salt_text, digest_text = encoded_hash.split("$")
        iterations = int(iterations_text)
        salt = bytes.fromhex(salt_text)
        digest = bytes.fromhex(digest_text)
    except (ValueError, TypeError) as exc:
        raise RuntimeError("LOGIN_PASSWORD_HASH is invalid. Run setup_login.py to create credentials.") from exc

    if (
        name != _HASH_NAME
        or iterations != HASH_ITERATIONS
        or len(salt) != 16
        or len(digest) != hashlib.sha256().digest_size
    ):
        raise RuntimeError("LOGIN_PASSWORD_HASH is invalid. Run setup_login.py to create credentials.")


def verify_password(password: str, encoded_hash: str) -> bool:
    validate_password_hash(encoded_hash)
    _, iterations_text, salt_text, digest_text = encoded_hash.split("$")
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_text),
        int(iterations_text),
    )
    return hmac.compare_digest(digest.hex(), digest_text)
