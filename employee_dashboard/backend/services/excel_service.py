"""Reads the configured Excel worksheet without modifying its source."""

import pandas as pd

from backend.config import COLUMNS, EXCEL_PATH, EXCEL_SHEET_NAME

_cache_signature: tuple[str, int, int, int] | None = None
_cached_employees: pd.DataFrame | None = None


def _read_employees(source: str) -> pd.DataFrame:
    with pd.ExcelFile(source) as workbook:
        if EXCEL_SHEET_NAME not in workbook.sheet_names:
            available_sheets = ", ".join(workbook.sheet_names) or "none"
            raise ValueError(
                f"Worksheet '{EXCEL_SHEET_NAME}' was not found in {EXCEL_PATH}. "
                f"Available worksheets: {available_sheets}. "
                "Sync the correct SharePoint workbook and update EXCEL_PATH in .env."
            )
        df = pd.read_excel(workbook, sheet_name=EXCEL_SHEET_NAME, dtype=str)
    df.columns = df.columns.astype(str).str.strip()

    missing = [column for column in COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in Excel: {missing}")

    df = df[list(COLUMNS)].dropna(how="all").fillna("")
    for column in df.columns:
        df[column] = df[column].astype(str).str.strip()
    return df


def get_workbook_version() -> str:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(
            f"Excel workbook not found at {EXCEL_PATH}. "
            "Set EXCEL_PATH in the project's .env file to the synced workbook."
        )

    stat = EXCEL_PATH.stat()
    return f"{stat.st_mtime_ns}-{stat.st_ctime_ns}-{stat.st_size}"


def load_employees() -> pd.DataFrame:
    global _cache_signature, _cached_employees

    if not EXCEL_PATH.exists():
        raise FileNotFoundError(
            f"Excel workbook not found at {EXCEL_PATH}. "
            "Set EXCEL_PATH in the project's .env file to the synced workbook."
        )

    stat = EXCEL_PATH.stat()
    signature = (
        str(EXCEL_PATH.resolve()),
        stat.st_mtime_ns,
        stat.st_ctime_ns,
        stat.st_size,
    )
    if _cached_employees is not None and _cache_signature == signature:
        return _cached_employees

    df = _read_employees(str(EXCEL_PATH))
    _cached_employees = df
    _cache_signature = signature
    return df


def to_records(df: pd.DataFrame) -> list[dict]:
    return df.rename(columns=COLUMNS).to_dict(orient="records")
