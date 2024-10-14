from datetime import datetime
from enum import Enum
from pandas import DataFrame
from typing import Dict


class CityCost(Enum):
    HIGH = "high"
    LOW = "low"


class Project:
    def __init__(
        self,
        project_number: int,
        city_cost: CityCost,
        start_date: datetime,
        end_date: datetime,
    ):
        self.project_number = project_number
        self.city_cost = city_cost
        self.start_date = start_date
        self.end_date = end_date

    # TODO: add getter methods


class ProjectSet:
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.start_date = None
        self.end_date = None

    def add_project(self, project: Project):
        self.projects[project.project_number] = project

        # update set start_date if project start_date is earliest in set
        if self.start_date is None or project.start_date < self.start_date:
            self.start_date = project.start_date

        # update set end_date if project end_date is latest in set
        if self.end_date is None or project.end_date > self.end_date:
            self.end_date = project.end_date

    def get_projects(self) -> Dict[int, Project]:
        return self.projects

    def get_project_by_number(self, project_number: int) -> Project:
        return self.projects[project_number]

    def get_start_date(self) -> datetime:
        return self.start_date

    def get_end_date(self) -> datetime:
        return self.end_date


def load_data_to_project_set(data_frame: DataFrame) -> ProjectSet:
    project_set = ProjectSet()
    for _, row in data_frame.iterrows():
        # TODO: error handling
        project_number = int(row["project_number"])
        city_cost = row["city_cost"]
        start_date = datetime.strptime(row["start_date"], "%m/%d/%y")
        end_date = datetime.strptime(row["end_date"], "%m/%d/%y")
        project = Project(project_number, city_cost, start_date, end_date)
        project_set.add_project(project)
    return project_set
