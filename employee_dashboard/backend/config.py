"""Central configuration: file paths and Excel column mapping."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

EXCEL_SHEET_NAME = "Data Practice Resources"
_configured_excel_path = Path(os.getenv("EXCEL_PATH", "Employee_data.xlsx")).expanduser()
EXCEL_PATH = (
    _configured_excel_path
    if _configured_excel_path.is_absolute()
    else BASE_DIR / _configured_excel_path
)
FRONTEND_DIR = BASE_DIR / "frontend"
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL", "").strip()
LOGIN_PASSWORD_HASH = os.getenv("LOGIN_PASSWORD_HASH", "")
SESSION_SECRET = os.getenv("SESSION_SECRET", "")
_cookie_secure_setting = os.getenv("COOKIE_SECURE", "true").strip().lower()
if _cookie_secure_setting not in {"1", "true", "yes", "0", "false", "no"}:
    raise RuntimeError("COOKIE_SECURE must be true or false.")
COOKIE_SECURE = _cookie_secure_setting in {"1", "true", "yes"}
_local_access_setting = os.getenv("LOCAL_ONLY_ACCESS", "false").strip().lower()
if _local_access_setting not in {"1", "true", "yes", "0", "false", "no"}:
    raise RuntimeError("LOCAL_ONLY_ACCESS must be true or false.")
LOCAL_ONLY_ACCESS = _local_access_setting in {"1", "true", "yes"}

# Excel column name -> API field name. Other worksheet columns are ignored.
COLUMNS = {
    "#": "serial_number",
    "Employee ID": "employee_id",
    "Employee Name": "name",
    "Technical Skills": "technical_skills",
    "YOE": "yoe",
    "Email": "email",
    "DOJ DEP": "doj_dep",
    "Internal/External": "internal_external",
    "Mapped to Project": "mapped_to_project",
    "Billable from": "billable_from",
    "Client Name": "client_name",
    "Certification Name": "certification_name",
    "Date of Completion": "date_of_completion",
    "Expected Date of Completion": "expected_date_of_completion",
    "Profiles Uploaded": "profiles_uploaded",
    "Contact Number": "contact_number",
}
