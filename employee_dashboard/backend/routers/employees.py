from fastapi import APIRouter

from backend.schemas import Employee
from backend.services import dashboard_service

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get("", response_model=list[Employee])
def list_employees(
    mapped_to_project: str | None = None,
    internal_external: str | None = None,
):
    return dashboard_service.get_employees(mapped_to_project, internal_external)
