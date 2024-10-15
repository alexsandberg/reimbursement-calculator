from datetime import datetime
import pandas as pd
import sys
from src.reimbursement.project import CityCost


def validate_project_number(project_number: str) -> int:
    project_number_int = None

    try:
        project_number_int = int(project_number)
    except ValueError as exc:
        raise ValueError("Invalid project_number. Must be integer value.") from exc

    return project_number_int


def convert_to_city_cost_enum(city_cost: str) -> CityCost:
    try:
        return CityCost(city_cost)
    except ValueError as exc:
        raise ValueError("Invalid city_cost. Valid values: low, high.") from exc


def convert_datestr_to_datetime(datestr: str) -> datetime:
    try:
        return datetime.strptime(datestr, "%m/%d/%y")
    except ValueError as exc:
        raise ValueError("Invalid date string. Expected format: mm/dd/yy") from exc


def read_csv(file_path: str) -> pd.DataFrame:
    data = None
    try:
        # validate types and parse dates
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
