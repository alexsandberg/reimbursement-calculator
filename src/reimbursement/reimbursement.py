from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict

from src.reimbursement.project import CityCost, ProjectSet

LOW_COST_TRAVEL_RATE = 45
HIGH_COST_TRAVEL_RATE = 55
LOW_COST_FULL_RATE = 75
HIGH_COST_FULL_RATE = 85


class RateType(Enum):
    FULL = "full"
    TRAVEL = "travel"


def is_low_cost_city(city_cost: CityCost) -> bool:
    return city_cost == CityCost.LOW


def get_travel_rate_for_city_type(city_cost: CityCost) -> int:
    return (
        LOW_COST_TRAVEL_RATE if is_low_cost_city(city_cost) else HIGH_COST_TRAVEL_RATE
    )


def get_full_rate_for_city_type(city_cost: CityCost) -> int:
    return LOW_COST_FULL_RATE if is_low_cost_city(city_cost) else HIGH_COST_FULL_RATE


def get_rate_by_rate_type_and_city_type(
    rate_type: RateType, city_cost: CityCost
) -> int:
    """
    Returns the day rate based on rate type (full or travel)
    and city type (high or low cost)
    """
    return (
        get_full_rate_for_city_type(city_cost)
        if rate_type == RateType.FULL
        else get_travel_rate_for_city_type(city_cost)
    )


def get_highest_rate_by_type(
    project_set: ProjectSet, project_numbers: List[int], rate_type: RateType
) -> int:
    """
    Given a rate type (full or travel) and a list of project numbers for a specific day
    returns the highest rate for that day
    """
    highest_rate = 0
    for project_number in project_numbers:
        project = project_set.get_project_by_number(project_number)
        rate = get_rate_by_rate_type_and_city_type(rate_type, project.get_city_cost())
        highest_rate = max(highest_rate, rate)
    return highest_rate


def get_projects_by_day_map(project_set: ProjectSet) -> Dict[datetime, List[int]]:
    """
    Returns a dictionary that maps every date in the full project set
    to a list of active project numbers for that day
    """
    projects_by_day = {}
    current_date = project_set.get_start_date()

    # loop over every day in the set and initialize each with an empty list
    while current_date <= project_set.get_end_date():
        projects_by_day[current_date] = []
        current_date += timedelta(days=1)

    # mark each day in the set with project numbers active on that day
    for project in project_set.get_projects().values():
        current_date = project.get_start_date()
        while current_date <= project.get_end_date():
            projects_by_day[current_date].append(project.get_project_number())
            current_date += timedelta(days=1)
    return projects_by_day


def calculate_reimbursement(project_set: ProjectSet) -> int:
    """
    Calculates reimbursement for the project set
    by iterating over every day in the set and determining the rate for that day
    """

    # mapping of each day in set to a list of project numbers for that day
    projects_by_day: Dict[datetime, List[int]] = get_projects_by_day_map(project_set)

    # stores the rate for each day in set
    rate_by_day: Dict[datetime, int] = {}

    for date, projects in projects_by_day.items():
        # don't overwrite rate if already set
        if date in rate_by_day:
            continue

        # date is a gap day
        if len(projects) == 0:
            rate_by_day[date] = 0

            # if there were any projects yesterday, update rate to be a travel day
            yesterday = date - timedelta(days=1)
            if yesterday in projects_by_day and len(projects_by_day[yesterday]) > 0:
                # there could be more than one project ending on same day
                rate_by_day[yesterday] = get_highest_rate_by_type(
                    project_set, projects_by_day[yesterday], RateType.TRAVEL
                )

            # if there are any projects tomorrow, set rate to be a travel day
            tomorrow = date + timedelta(days=1)
            if tomorrow in projects_by_day and len(projects_by_day[tomorrow]) > 0:
                # there could be more than one project starting on same day
                rate_by_day[tomorrow] = get_highest_rate_by_type(
                    project_set, projects_by_day[tomorrow], RateType.TRAVEL
                )

        else:
            # first day and last day of the set is a travel day, otherwise it's a full day
            rate_type = (
                RateType.TRAVEL
                if date == project_set.get_start_date()
                or date == project_set.get_end_date()
                else RateType.FULL
            )

            rate_by_day[date] = get_highest_rate_by_type(
                project_set, projects, rate_type
            )

    # print results of each day in the set
    for date, rate in rate_by_day.items():
        print(f"date: {str(date)}, rate: {rate}")

    # return summed reimbursement
    return sum(rate_by_day.values())
