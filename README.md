# Reimbursement Calculator

This project implements a reimbursement calculator in Python to satisfy the requirements listed below. It is a technical assessment as part of the interview process for a software consultancy.

# Requirements

Given a set of projects, calculate the reimbursement amount for the set. Each project has a start date and an end date. The first day of a project and the last day of a project are always "travel" days. Days in the middle of a project are "full" days. There are also two types of cities a project can be in, high cost cities and low cost cities.

* First day and last day of a project, or sequence of projects, is a travel day.
* Any day in the middle of a project, or sequence of projects, is considered a full day.
* If there is a gap between projects, then the days on either side of that gap are travel days.
* If two projects push up against each other, or overlap, then those days are full days as well.
* Any given day is only ever counted once, even if two projects are on the same day.
* A travel day is reimbursed at a rate of 45 dollars per day in a low cost city.
* A travel day is reimbursed at a rate of 55 dollars per day in a high cost city.
* A full day is reimbursed at a rate of 75 dollars per day in a low cost city.
* A full day is reimbursed at a rate of 85 dollars per day in a high cost city.

# Usage

First ensure you are using Python 3.9 or higher. Then activate a virtual environment and install the requirements:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To run the code, you must supply the path to a csv data file. Examples of valid data are located in [/data](https://github.com/alexsandberg/reimbursement-calculator/tree/main/data). Example:

```
$ python main.py ./data/set_1.csv
```

This will output the reimbursement results for each day in the project set, as well as the final reimbursement total.

```
$ python main.py ./data/set_1.csv
date: 09/01/2015, rate: $45
date: 09/02/2015, rate: $75
date: 09/03/2015, rate: $45
total reimbursement: $165
```

Some example cases of invalid data are provided in [/data/invalid_data](https://github.com/alexsandberg/reimbursement-calculator/tree/main/data/invalid_data). Example:

```
$ python main.py ./data/invalid_data/invalid_example_2.csv
An error occurred: Invalid city_cost. Valid values: low, high.
```