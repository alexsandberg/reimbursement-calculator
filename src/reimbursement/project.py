from datetime import datetime

class Project:
    def __init__(self, project_number, city_cost, start_date: datetime, end_date: datetime):
        self.project_number = project_number
        self.city_cost = city_cost
        self.start_date = start_date
        self.end_date = end_date

    # TODO: add getter methods
