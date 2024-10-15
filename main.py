import sys

from src.reimbursement.csv import read_csv
from src.reimbursement.project import load_data_to_project_set
from src.reimbursement.reimbursement import calculate_reimbursement


def main():
    if len(sys.argv) != 2:
        print(
            "Incorrect arguments supplied. Intended usage: python main.py <csv_file_path>"
        )
    else:
        csv_file_path = sys.argv[1]
        data_frame = read_csv(csv_file_path)
        project_set = load_data_to_project_set(data_frame)
        total = calculate_reimbursement(project_set)
        print(f"total reimbursement: {total}")


if __name__ == "__main__":
    main()
