import sys
from src.reimbursement.csv import read_csv
from src.reimbursement.reimbursement import calculate_reimbursement

def main():
    if len(sys.argv) != 2:
        print("Incorrect arguments supplied. Intended usage: python main.py <csv_file_path>")
    else:
        csv_file_path = sys.argv[1]
        set = read_csv(csv_file_path)
        total = calculate_reimbursement(set)
        print(f'total reimbursement: {total}')

if __name__ == "__main__":
    main()
