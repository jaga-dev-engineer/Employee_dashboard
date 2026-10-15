"""Business logic: aggregations and filters used by the API."""
from backend.services.excel_service import load_employees, to_records


def get_summary() -> dict:
    df = load_employees()
    return {
        "total_employees": int(len(df)),
        "mapped_employees": int(df["Mapped to Project"].str.upper().isin({"Y", "YES", "TRUE", "1"}).sum()),
        "locations": int(df.loc[df["Location"] != "", "Location"].nunique()),
        "employees_with_email": int((df["Email"] != "").sum()),
    }


def get_distribution_by_location() -> list[dict]:
    df = load_employees()
    df = df[df["Location"] != ""]
    counts = df.groupby("Location").size().sort_values(ascending=False)
    return [{"label": location, "count": int(count)} for location, count in counts.items()]


def get_distribution_by_project_mapping() -> list[dict]:
    df = load_employees()
    mapping = df["Mapped to Project"].replace("", "Not specified")
    counts = mapping.value_counts().sort_values(ascending=False)
    return [{"label": label, "count": int(count)} for label, count in counts.items()]


def get_employees(
    location: str | None = None,
    mapped_to_project: str | None = None,
) -> list[dict]:
    df = load_employees()
    if location:
        df = df[df["Location"].str.lower() == location.strip().lower()]
    if mapped_to_project:
        df = df[df["Mapped to Project"].str.lower() == mapped_to_project.strip().lower()]
    return to_records(df)
