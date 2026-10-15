"""Create the local .env file for the dashboard's single login account."""

import getpass
import re
import secrets
from pathlib import Path

from backend.auth_utils import hash_password
from backend.config import BASE_DIR


def main() -> None:
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        raise SystemExit(f"{env_path} already exists; refusing to overwrite credentials.")

    email = input("Dashboard login email: ").strip()
    if not re.fullmatch(r"[^@\s=]+@[^@\s=]+\.[^@\s=]+", email) or len(email) > 254:
        raise SystemExit("Enter a valid email address.")

    password = getpass.getpass("Dashboard password (at least 12 characters): ")
    if len(password) < 12:
        raise SystemExit("Password must be at least 12 characters.")
    if password != getpass.getpass("Confirm dashboard password: "):
        raise SystemExit("Passwords did not match.")

    env_contents = "\n".join(
        (
            f"LOGIN_EMAIL={email}",
            f"LOGIN_PASSWORD_HASH={hash_password(password)}",
            f"SESSION_SECRET={secrets.token_urlsafe(48)}",
            "COOKIE_SECURE=false",
            "",
        )
    )
    env_path.write_text(env_contents, encoding="utf-8")
    print(f"Created {env_path}. Keep it private; it contains the session secret and password hash.")
    print("COOKIE_SECURE is false for local HTTP testing; set it to true on an HTTPS host.")


if __name__ == "__main__":
    main()
