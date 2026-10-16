"""Reads and cleans the Excel file, reloading it when the source changes."""

import pandas as pd

from backend.config import COLUMNS, EXCEL_PATH

_cache_signature: tuple[str, int, int, int] | None = None
_cached_employees: pd.DataFrame | None = None


def get_workbook_version() -> str:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {EXCEL_PATH}")

    stat = EXCEL_PATH.stat()
    return f"{stat.st_mtime_ns}-{stat.st_ctime_ns}-{stat.st_size}"


def load_employees() -> pd.DataFrame:
    global _cache_signature, _cached_employees

    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {EXCEL_PATH}")

    stat = EXCEL_PATH.stat()
    signature = (
        str(EXCEL_PATH.resolve()),
        stat.st_mtime_ns,
        stat.st_ctime_ns,
        stat.st_size,
    )
    if _cached_employees is not None and _cache_signature == signature:
        return _cached_employees

    df = pd.read_excel(EXCEL_PATH, dtype=str)
    df.columns = df.columns.str.strip()

    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in Excel: {missing}")

    df = df[list(COLUMNS)].dropna(how="all").fillna("")
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    _cached_employees = df
    _cache_signature = signature
    return df


def to_records(df: pd.DataFrame) -> list[dict]:
    return df.rename(columns=COLUMNS).to_dict(orient="records")
