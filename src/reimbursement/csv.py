import pandas as pd

from src.reimbursement.project import Project, ProjectSet

def read_csv(file_path):
    data = None
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data
