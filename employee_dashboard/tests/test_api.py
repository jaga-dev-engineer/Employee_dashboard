import hashlib
import os

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Isolate tests from any developer or deployment credentials in the environment.
_TEST_SALT = bytes.fromhex("00112233445566778899aabbccddeeff")
_TEST_PASSWORD = "test-dashboard-password"
_TEST_DIGEST = hashlib.pbkdf2_hmac("sha256", _TEST_PASSWORD.encode(), _TEST_SALT, 310_000)
os.environ["LOGIN_EMAIL"] = "dashboard-test@example.com"
os.environ["LOGIN_PASSWORD_HASH"] = (
    f"pbkdf2_sha256$310000${_TEST_SALT.hex()}${_TEST_DIGEST.hex()}"
)
os.environ["SESSION_SECRET"] = "test-only-session-secret-that-is-long-enough"
os.environ["COOKIE_SECURE"] = "false"

from backend.config import COLUMNS, EXCEL_SHEET_NAME
from backend.main import app
from backend.services import excel_service


def employee_row(**overrides):
    row = {
        "#": "1",
        "Employee ID": "FD00001",
        "Employee Name": "Test Employee",
        "Technical Skills": "Python, SQL",
        "YOE": "5",
        "Email": "employee@example.com",
        "DOJ DEP": "2021-01-01",
        "Internal/External": "Internal",
        "Mapped to Project": "Project A",
        "Billable from": "2021-02-01",
        "Client Name": "Client A",
        "Certification Name": "Certification A",
        "Date of Completion": "2024-01-01",
        "Expected Date of Completion": "2025-01-01",
        "Profiles Uploaded": "Yes",
        "Contact Number": "1234567890",
    }
    return {**row, **overrides}


def write_workbook(path, rows):
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame(rows).to_excel(writer, sheet_name=EXCEL_SHEET_NAME, index=False)
        pd.DataFrame([{"Employee Name": "Wrong worksheet"}]).to_excel(
            writer, sheet_name="Other", index=False
        )


@pytest.fixture
def client(tmp_path, monkeypatch):
    workbook_path = tmp_path / "Employee_data.xlsx"
    write_workbook(workbook_path, [employee_row()])
    monkeypatch.setattr(excel_service, "EXCEL_PATH", workbook_path)

    with TestClient(app) as test_client:
        response = test_client.post(
            "/api/auth/login",
            json={"email": "dashboard-test@example.com", "password": _TEST_PASSWORD},
        )
        assert response.status_code == 200
        cookie = response.headers["set-cookie"].lower()
        assert "httponly" in cookie
        assert "samesite=lax" in cookie
        yield test_client


def test_dashboard_requires_login():
    with TestClient(app) as anonymous_client:
        response = anonymous_client.get("/", follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/login"
        assert anonymous_client.get("/employees.html", follow_redirects=False).status_code == 303
        assert anonymous_client.get("/api/employees").status_code == 401
        assert anonymous_client.get("/api/dashboard/summary").status_code == 401


def test_login_and_logout(client):
    assert client.get("/").status_code == 200
    assert client.get("/api/dashboard/summary").status_code == 200
    response = client.post("/api/auth/logout", follow_redirects=False)
    assert response.status_code == 204
    assert client.get("/api/employees").status_code == 401


def test_api_returns_only_columns_from_named_worksheet(client):
    employees = client.get("/api/employees").json()
    assert len(employees) == 1
    assert set(employees[0]) == set(COLUMNS.values())
    assert employees[0]["name"] == "Test Employee"
    assert employees[0]["technical_skills"] == "Python, SQL"

    summary = client.get("/api/dashboard/summary").json()
    assert summary == {
        "total_employees": 1,
        "mapped_employees": 1,
        "employees_with_email": 1,
        "internal_employees": 1,
        "external_employees": 0,
    }


def test_employee_filters_use_requested_columns(client, tmp_path, monkeypatch):
    workbook_path = tmp_path / "Employee_data.xlsx"
    write_workbook(
        workbook_path,
        [
            employee_row(),
            employee_row(
                **{
                    "#": "2",
                    "Employee ID": "FD00002",
                    "Employee Name": "External Employee",
                    "Internal/External": "External",
                    "Mapped to Project": "Project B",
                }
            ),
        ],
    )
    monkeypatch.setattr(excel_service, "EXCEL_PATH", workbook_path)

    external = client.get("/api/employees", params={"internal_external": "external"}).json()
    assert len(external) == 1
    assert external[0]["name"] == "External Employee"

    project = client.get("/api/employees", params={"mapped_to_project": "Project A"}).json()
    assert len(project) == 1
    assert project[0]["name"] == "Test Employee"


def test_project_mapping_counts(client, tmp_path, monkeypatch):
    workbook_path = tmp_path / "Employee_data.xlsx"
    write_workbook(
        workbook_path,
        [
            employee_row(),
            employee_row(**{"#": "2", "Employee ID": "FD00002"}),
            employee_row(**{"#": "3", "Mapped to Project": ""}),
        ],
    )
    monkeypatch.setattr(excel_service, "EXCEL_PATH", workbook_path)

    assert client.get("/api/dashboard/project-mapping").json() == [
        {"label": "Project A", "count": 2}
    ]


def test_workbook_version_changes_after_save(client, tmp_path, monkeypatch):
    workbook_path = tmp_path / "Employee_data.xlsx"
    monkeypatch.setattr(excel_service, "EXCEL_PATH", workbook_path)
    write_workbook(workbook_path, [employee_row()])
    first_version = client.get("/api/dashboard/version").json()["version"]

    write_workbook(workbook_path, [employee_row(**{"Employee Name": "Updated Employee"})])
    stat = workbook_path.stat()
    os.utime(workbook_path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))

    second_version = client.get("/api/dashboard/version").json()["version"]
    assert second_version != first_version
