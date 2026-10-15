"""Login and logout endpoints for the employee dashboard."""

import hmac
import time
from threading import Lock

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from backend.auth_utils import verify_password
from backend.config import LOGIN_EMAIL, LOGIN_PASSWORD_HASH

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
_ATTEMPT_WINDOW_SECONDS = 15 * 60
_MAX_FAILED_ATTEMPTS = 5
_failed_attempts: dict[str, tuple[float, int]] = {}
_attempts_lock = Lock()


class LoginCredentials(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=1024)


@router.post("/login")
def login(credentials: LoginCredentials, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    with _attempts_lock:
        expired = [
            ip
            for ip, (first_attempt, _) in _failed_attempts.items()
            if now - first_attempt >= _ATTEMPT_WINDOW_SECONDS
        ]
        for ip in expired:
            _failed_attempts.pop(ip, None)
        first_attempt, failures = _failed_attempts.get(client_ip, (now, 0))
        if now - first_attempt >= _ATTEMPT_WINDOW_SECONDS:
            first_attempt, failures = now, 0
        if failures >= _MAX_FAILED_ATTEMPTS:
            raise HTTPException(status_code=429, detail="Too many login attempts. Try again later.")

    email_matches = hmac.compare_digest(
        credentials.email.strip().casefold().encode("utf-8"),
        LOGIN_EMAIL.casefold().encode("utf-8"),
    )
    password_matches = verify_password(credentials.password, LOGIN_PASSWORD_HASH)
    if not (email_matches and password_matches):
        with _attempts_lock:
            first_attempt, failures = _failed_attempts.get(client_ip, (now, 0))
            if now - first_attempt >= _ATTEMPT_WINDOW_SECONDS:
                first_attempt, failures = now, 0
            _failed_attempts[client_ip] = (first_attempt, failures + 1)
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")

    with _attempts_lock:
        _failed_attempts.pop(client_ip, None)
    request.session.clear()
    request.session["authenticated"] = True
    return {"redirect_url": "/"}


@router.post("/logout", status_code=204)
def logout(request: Request):
    request.session.clear()
