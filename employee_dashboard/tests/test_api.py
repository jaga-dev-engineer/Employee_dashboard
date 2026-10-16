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

from backend.config import COLUMNS
from backend.main import app
from backend.services import excel_service


@pytest.fixture
def client():
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
    response = client.post(
        "/api/auth/logout",
        follow_redirects=False,
    )
    assert response.status_code == 204
    assert client.get("/api/employees").status_code == 401


def test_invalid_login_is_rejected():
    with TestClient(app) as anonymous_client:
        response = anonymous_client.post(
            "/api/auth/login",
            json={"email": "dashboard-test@example.com", "password": "incorrect-password"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Email or password is incorrect."


def test_api_uses_employee_data_columns(client):
    employees = client.get("/api/employees").json()
    assert employees
    assert set(employees[0]) == set(COLUMNS.values())

    summary = client.get("/api/dashboard/summary").json()
    assert summary["total_employees"] == len(employees)
    assert summary["mapped_employees"] == sum(
        employee["mapped_to_project"].upper() in {"Y", "YES", "TRUE", "1"}
        for employee in employees
    )
    assert summary["locations"] == len(
        {employee["location"] for employee in employees if employee["location"]}
    )


def test_location_and_mapping_aggregations(client):
    locations = client.get("/api/dashboard/by-location").json()
    location_counts = [item["count"] for item in locations]
    assert location_counts == sorted(location_counts, reverse=True)
    assert all(item["label"] for item in locations)

    mappings = client.get("/api/dashboard/project-mapping").json()
    assert sum(item["count"] for item in mappings) == client.get("/api/dashboard/summary").json()["total_employees"]


def test_workbook_version_changes_after_save(client, tmp_path, monkeypatch):
    workbook_path = tmp_path / "Employee_data.xlsx"
    monkeypatch.setattr(excel_service, "EXCEL_PATH", workbook_path)
    row = {
        "S.no": "1",
        "Employee ID": "FD00001",
        "Employee Name": "Version Check",
        "Managers": "Manager One",
        "Email": "version@example.com",
        "Mapped to Project": "N",
        "Location": "Pune",
        "Contact Number": "1234567890",
    }
    pd.DataFrame([row]).to_excel(workbook_path, index=False)
    first_version = client.get("/api/dashboard/version").json()["version"]

    pd.DataFrame([{**row, "Managers": "Manager Two"}]).to_excel(workbook_path, index=False)
    stat = workbook_path.stat()
    os.utime(workbook_path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))

    second_version = client.get("/api/dashboard/version").json()["version"]
    assert second_version != first_version


def test_manager_counts_and_filter(client):
    employees = client.get("/api/employees").json()
    manager_counts = client.get("/api/dashboard/by-manager").json()
    expected = {}
    for employee in employees:
        if employee["manager"]:
            expected[employee["manager"]] = expected.get(employee["manager"], 0) + 1

    assert {row["label"]: row["count"] for row in manager_counts} == expected
    assert [row["count"] for row in manager_counts] == sorted(
        (row["count"] for row in manager_counts), reverse=True
    )

    manager = manager_counts[0]["label"]
    response = client.get("/api/employees", params={"manager": manager})
    assert response.status_code == 200
    assert response.json()
    assert all(employee["manager"] == manager for employee in response.json())
    assert len(response.json()) == expected[manager]


def test_employee_filters(client):
    employees = client.get("/api/employees").json()
    location = next(employee["location"] for employee in employees if employee["location"])
    response = client.get("/api/employees", params={"location": location})
    assert response.status_code == 200
    assert all(employee["location"] == location for employee in response.json())

    mapped_value = next(
        employee["mapped_to_project"] for employee in employees if employee["mapped_to_project"]
    )
    response = client.get("/api/employees", params={"mapped_to_project": mapped_value})
    assert response.status_code == 200
    assert all(employee["mapped_to_project"] == mapped_value for employee in response.json())


def test_saved_workbook_changes_are_loaded(client, tmp_path, monkeypatch):
    workbook_path = tmp_path / "Employee_data.xlsx"
    monkeypatch.setattr(excel_service, "EXCEL_PATH", workbook_path)

    first_row = {
        "S.no": "1",
        "Employee ID": "FD00001",
        "Employee Name": "Initial Name",
        "Managers": "Initial Manager",
        "Email": "initial@example.com",
        "Mapped to Project": "N",
        "Location": "Pune",
        "Contact Number": "1234567890",
    }
    pd.DataFrame([first_row]).to_excel(workbook_path, index=False)
    assert client.get("/api/employees").json()[0]["name"] == "Initial Name"

    updated_row = {
        **first_row,
        "Employee ID": "FD00002",
        "Employee Name": "Updated Name",
        "Managers": "Updated Manager",
    }
    pd.DataFrame([updated_row]).to_excel(workbook_path, index=False)
    stat = workbook_path.stat()
    os.utime(workbook_path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))

    employees = client.get("/api/employees").json()
    assert employees[0]["employee_id"] == "FD00002"
    assert employees[0]["name"] == "Updated Name"
    assert employees[0]["manager"] == "Updated Manager"
    manager_counts = client.get("/api/dashboard/by-manager").json()
    assert manager_counts == [{"label": "Updated Manager", "count": 1}]
