import sys
import pandas as pd

from datetime import datetime, timedelta
from typing import List

# TODO: break into modules

class Project:
    def __init__(self, project_number, city_cost, start_date: datetime, end_date: datetime):
        self.project_number = project_number
        self.city_cost = city_cost
        self.start_date = start_date
        self.end_date = end_date

    # TODO: add getter methods

class Set:
    def __init__(self):
        self.projects = {}
        self.start_date = None
        self.end_date = None
    
    def add_project(self, project: Project):
        self.projects[project.project_number] = project

        # update set start_date if project start_date is earliest in set
        if self.start_date == None or project.start_date < self.start_date:
            self.start_date = project.start_date
        
        # update set end_date if project end_date is latest in set
        if self.end_date == None or project.end_date > self.end_date:
            self.end_date = project.end_date

    def get_projects(self):
        return self.projects
    
    def get_project_by_number(self, project_number: int) -> Project:
        return self.projects[project_number]
    
    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

LOW_COST_TRAVEL_RATE = 45
HIGH_COST_TRAVEL_RATE = 55
LOW_COST_FULL_RATE = 75
HIGH_COST_FULL_RATE = 85

def get_travel_rate_for_city_type(city_cost):
    return LOW_COST_TRAVEL_RATE if city_cost == 'low' else HIGH_COST_TRAVEL_RATE

def get_full_rate_for_city_type(city_cost):
    return LOW_COST_FULL_RATE if city_cost == 'low' else HIGH_COST_FULL_RATE
    
def get_highest_full_day_rate(set: Set, project_numbers: List[int]) -> int:
    highest_rate = 0
    for project_number in project_numbers:
        project = set.get_project_by_number(project_number)
        rate = get_full_rate_for_city_type(project.city_cost)
        highest_rate = max(highest_rate, rate)
    return highest_rate

# repetitive code: refactor to combine with get_highest_full_day_rate
def get_highest_travel_day_rate(set: Set, project_numbers: List[int]) -> int:
    highest_rate = 0
    for project_number in project_numbers:
        project = set.get_project_by_number(project_number)
        rate = get_full_rate_for_city_type(project.city_cost)
        highest_rate = max(highest_rate, rate)
    return highest_rate     

# dictionary that maps each day in the set to a list of projects on that day
def init_projects_by_day_map(set: Set):
    projects_by_day = {}
    current_date = set.get_start_date()

    # loop over every day in the set and initialize each with an empty list
    while (current_date <= set.get_end_date()):
        projects_by_day[current_date] = []
        current_date += timedelta(days=1)
    
    # mark each day with project numbers
    for project in set.get_projects().values():
        current_date = project.start_date
        while (current_date <= project.end_date):
            projects_by_day[current_date].append(project.project_number)
            current_date += timedelta(days=1)
    return projects_by_day

def calculate_reimbursement(set: Set) -> int:
    projects_by_day = init_projects_by_day_map(set)
    rate_by_day = {}

    for date, projects in projects_by_day.items():
        # don't overwrite rate if already set
        if date in rate_by_day:
            continue

        number_of_projects = len(projects)
        if number_of_projects == 0:
            # date is a gap day
            rate_by_day[date] = 0

            # if there were any projects yesterday, update rate to be a travel day
            yesterday = date - timedelta(days=1)
            if yesterday in projects_by_day and len(projects_by_day[yesterday]) != 0:
                # there could be more than one project ending on same day
                rate_by_day[yesterday] = get_highest_travel_day_rate(set, projects_by_day[yesterday])

            # if there are any projects tomorrow, set rate to be a travel day
            tomorrow = date + timedelta(days=1)
            if tomorrow in projects_by_day and len(projects_by_day[tomorrow]) != 0:
                # there could be more than one project ending on same day
                rate_by_day[tomorrow] = get_highest_travel_day_rate(set, projects_by_day[tomorrow])

        elif number_of_projects == 1:
            project_number = projects[0]
            project = set.get_project_by_number(project_number)
    
            # first day and last day of the set is a travel day
            if date == set.get_start_date() or date == set.get_end_date():
                rate_by_day[date] = get_travel_rate_for_city_type(project.city_cost)
            else:
                # it must be a full day
                rate_by_day[date] = get_full_rate_for_city_type(project.city_cost)

        else:
            # since there's overlap, this is a full day at the highest rate
            rate_by_day[date] = get_highest_full_day_rate(set, projects)

    for date, rate in rate_by_day.items():
        print(f'date: {str(date)}, rate: {rate}')

    # return summed reimbursement
    return sum(rate_by_day.values())

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        set = Set()
        for _, row in data.iterrows():
            # TODO: error handling
            project_number = int(row['project_number'])
            city_cost = row['city_cost']
            start_date = datetime.strptime(row["start_date"], "%m/%d/%y")
            end_date = datetime.strptime(row["end_date"], "%m/%d/%y")
            project = Project(project_number, city_cost, start_date, end_date)
            set.add_project(project)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return set

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect arguments supplied. Intended usage: python main.py <csv_file_path>")
    else:
        csv_file_path = sys.argv[1]
        set = read_csv(csv_file_path)
        total = calculate_reimbursement(set)
        print(f'total reimbursement: {total}')
