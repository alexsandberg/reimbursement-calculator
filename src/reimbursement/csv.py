import sys
from datetime import datetime

import pandas as pd
from src.reimbursement.project import CityCost


def validate_project_number(project_number: str) -> int:
    """Vaidates that project_number is an integer."""
    project_number_int = None

    try:
        project_number_int = int(project_number)
    except ValueError as exc:
        raise ValueError("Invalid project_number. Must be integer value.") from exc

    return project_number_int


def convert_to_city_cost_enum(city_cost: str) -> CityCost:
    """Validates city_cost and converts to CityCost enum value."""
    try:
        return CityCost(city_cost)
    except ValueError as exc:
        raise ValueError("Invalid city_cost. Valid values: low, high.") from exc


def convert_datestr_to_datetime(datestr: str) -> datetime:
    """Validates start_date or end_date and converts to datetime object."""
    try:
        return datetime.strptime(datestr, "%m/%d/%y")
    except ValueError as exc:
        raise ValueError("Invalid date string. Expected format: mm/dd/yy") from exc


def read_csv(file_path: str) -> pd.DataFrame:
    """Reads project set data from csv with data validation and conversion."""
    data = None
    try:
        data = pd.read_csv(
            file_path,
            converters={
                "project_number": validate_project_number,
                "city_cost": convert_to_city_cost_enum,
                "start_date": convert_datestr_to_datetime,
                "end_date": convert_datestr_to_datetime,
            },
        )
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    return data
