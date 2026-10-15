"""Central configuration: file paths and Excel column mapping."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

EXCEL_PATH = BASE_DIR / "Employee_data.xlsx"
FRONTEND_DIR = BASE_DIR / "frontend"
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL", "").strip()
LOGIN_PASSWORD_HASH = os.getenv("LOGIN_PASSWORD_HASH", "")
SESSION_SECRET = os.getenv("SESSION_SECRET", "")
_cookie_secure_setting = os.getenv("COOKIE_SECURE", "true").strip().lower()
if _cookie_secure_setting not in {"1", "true", "yes", "0", "false", "no"}:
    raise RuntimeError("COOKIE_SECURE must be true or false.")
COOKIE_SECURE = _cookie_secure_setting in {"1", "true", "yes"}

# Excel column name -> API field name
COLUMNS = {
    "S.no": "serial_number",
    "Employee ID": "employee_id",
    "Employee Name": "name",
    "Email": "email",
    "Mapped to Project": "mapped_to_project",
    "Location": "location",
    "Contact Number": "contact_number",
}
