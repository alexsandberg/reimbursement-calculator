from datetime import datetime
from enum import Enum
from typing import Dict

from pandas import DataFrame


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

    def get_project_number(self):
        return self.project_number

    def get_city_cost(self):
        return self.city_cost

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


class ProjectSet:
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.start_date = None
        self.end_date = None

    def add_project(self, project: Project):
        """
        Adds a project to the set.
        Projects are stored as a dictionary that maps
        the project number to the Project instance.
        """
        self.projects[project.get_project_number()] = project

        # update set start_date if project start_date is earliest in set
        if self.start_date is None or project.get_start_date() < self.start_date:
            self.start_date = project.get_start_date()

        # update set end_date if project end_date is latest in set
        if self.end_date is None or project.get_end_date() > self.end_date:
            self.end_date = project.get_end_date()

    def get_projects(self) -> Dict[int, Project]:
        return self.projects

    def get_project_by_number(self, project_number: int) -> Project:
        return self.projects[project_number]

    def get_start_date(self) -> datetime:
        return self.start_date

    def get_end_date(self) -> datetime:
        return self.end_date


def load_data_to_project_set(data_frame: DataFrame) -> ProjectSet:
    """Loads Pandas DataFrame from csv as a new ProjectSet instance."""
    project_set = ProjectSet()
    for _, row in data_frame.iterrows():
        project_set.add_project(
            Project(row.project_number, row.city_cost, row.start_date, row.end_date)
        )
    return project_set
