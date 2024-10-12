import sys
import pandas as pd

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        for _, row in data.iterrows():
            print('--------- project ---------')
            print(f'project_number: {row.project_number}')
            print(f'city_cost: {row.city_cost}')
            print(f'start_date: {row.start_date}')
            print(f'end_date: {row.end_date}')
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect arguments supplied. Intended usage: python main.py <csv_file_path>")
    else:
        csv_file_path = sys.argv[1]
        read_csv(csv_file_path)
