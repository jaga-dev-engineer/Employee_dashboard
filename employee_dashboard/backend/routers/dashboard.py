from fastapi import APIRouter

from backend.schemas import DistributionItem, SummaryResponse
from backend.services import dashboard_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=SummaryResponse)
def summary():
    return dashboard_service.get_summary()


@router.get("/by-location", response_model=list[DistributionItem])
def by_location():
    return dashboard_service.get_distribution_by_location()


@router.get("/project-mapping", response_model=list[DistributionItem])
def project_mapping():
    return dashboard_service.get_distribution_by_project_mapping()
