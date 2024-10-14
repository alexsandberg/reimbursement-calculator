import pandas as pd

from datetime import datetime
from src.reimbursement.project import Project, ProjectSet

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        projectSet = ProjectSet()
        for _, row in data.iterrows():
            # TODO: error handling
            project_number = int(row['project_number'])
            city_cost = row['city_cost']
            start_date = datetime.strptime(row["start_date"], "%m/%d/%y")
            end_date = datetime.strptime(row["end_date"], "%m/%d/%y")
            project = Project(project_number, city_cost, start_date, end_date)
            projectSet.add_project(project)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return projectSet
