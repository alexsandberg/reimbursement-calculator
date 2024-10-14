import pandas as pd
import sys
from src.reimbursement.project import CityCost


def convert_to_city_cost_enum(city_cost: str) -> CityCost:
    try:
        return CityCost(city_cost)
    except ValueError:
        raise ValueError("Invalid city_cost. Valid values: low, high.")


def read_csv(file_path: str) -> pd.DataFrame:
    data = None
    try:
        # validate types and parse dates
        data = pd.read_csv(
            file_path,
            converters={"city_cost": convert_to_city_cost_enum}, # TODO: converters for other fields
        )
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    return data
