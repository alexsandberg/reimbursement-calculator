from src.reimbursement.project import Project

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
