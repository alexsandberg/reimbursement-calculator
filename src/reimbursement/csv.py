import pandas as pd
import sys


def read_csv(file_path: str) -> pd.DataFrame:
    data = None
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    return data
