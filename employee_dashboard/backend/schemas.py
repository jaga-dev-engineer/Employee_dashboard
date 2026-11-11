from pydantic import BaseModel


class Employee(BaseModel):
    serial_number: str
    employee_id: str
    name: str
    technical_skills: str
    yoe: str
    email: str
    doj_dep: str
    internal_external: str
    mapped_to_project: str
    billable_from: str
    client_name: str
    certification_name: str
    date_of_completion: str
    expected_date_of_completion: str
    profiles_uploaded: str
    contact_number: str


class SummaryResponse(BaseModel):
    total_employees: int
    mapped_employees: int
    employees_with_email: int
    internal_employees: int
    external_employees: int


class DistributionItem(BaseModel):
    label: str
    count: int
