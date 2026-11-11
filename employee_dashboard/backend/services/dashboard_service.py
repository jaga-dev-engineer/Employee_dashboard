"""Business logic: aggregations and filters used by the API."""
from backend.services.excel_service import get_workbook_version, load_employees, to_records


def get_data_version() -> dict[str, str]:
    return {"version": get_workbook_version()}


def get_summary() -> dict:
    df = load_employees()
    work_type = df["Internal/External"].str.casefold()
    return {
        "total_employees": int(len(df)),
        "mapped_employees": int((df["Mapped to Project"] != "").sum()),
        "employees_with_email": int((df["Email"] != "").sum()),
        "internal_employees": int((work_type == "internal").sum()),
        "external_employees": int((work_type == "external").sum()),
    }


def get_distribution_by_project_mapping() -> list[dict]:
    df = load_employees()
    mapping = df.loc[df["Mapped to Project"] != "", "Mapped to Project"]
    counts = mapping.value_counts().sort_values(ascending=False)
    return [{"label": label, "count": int(count)} for label, count in counts.items()]


def get_employees(
    mapped_to_project: str | None = None,
    internal_external: str | None = None,
) -> list[dict]:
    df = load_employees()
    if mapped_to_project:
        df = df[df["Mapped to Project"].str.lower() == mapped_to_project.strip().lower()]
    if internal_external:
        df = df[df["Internal/External"].str.casefold() == internal_external.strip().casefold()]
    return to_records(df)
