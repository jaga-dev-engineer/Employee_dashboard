from pydantic import BaseModel


class Employee(BaseModel):
    serial_number: str
    employee_id: str
    name: str
    email: str
    mapped_to_project: str
    location: str
    contact_number: str


class SummaryResponse(BaseModel):
    total_employees: int
    mapped_employees: int
    locations: int
    employees_with_email: int


class DistributionItem(BaseModel):
    label: str
    count: int
