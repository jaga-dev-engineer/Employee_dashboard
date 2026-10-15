from fastapi import APIRouter

from backend.schemas import Employee
from backend.services import dashboard_service

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get("", response_model=list[Employee])
def list_employees(location: str | None = None, mapped_to_project: str | None = None):
    return dashboard_service.get_employees(location, mapped_to_project)
