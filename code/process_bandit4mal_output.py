import traceback
import argparse
from pathlib import Path
import csv
import json
from packaging import version
from datetime import datetime



### PARSE CSV FILE
def sort_filenames(filenames):
    """
    sort_filenames sorts filenames by name in alphabetical order and then by version number inside the alphabetical order.
    It expects a filename without the filetype behind it, so 'filename==version' and NOT 'filename==version.csv'
    
    Args:
        filenames (list): The filenames that need to be sorted without suffix
        
    Returns:
        sorted_filenames (list): A sorted list of all filenames
    """
    def sorting_key(filename):
        name, version_str = filename.split("==") # Split the filename into name and version
        parsed_version = version.parse(version_str) # Parse the version using packaging.version
        return (name, parsed_version) # Return a tuple for sorting

    sorted_filenames = sorted(filenames, key=sorting_key) # Sort filenames alphabetically and then by version number based on sorting key
    return sorted_filenames


def find_sorted_csv_filenames(results_folder):
    """
    find_csv_files finds all the csv files in a folder in sorted order

    Args:
        results_folder (Path): The path the result files have been saved to.

    Returns:
        sorted_filenames (list): Alphabetically and versionsorted filenames
    """

    csv_files = results_folder.glob('*.csv') # Get *.csv files in the directory.
    filenames = [file.stem for file in csv_files] # Get all filenames without full path and .csv ending.
    sorted_filenames = sort_filenames(filenames)

    return sorted_filenames


def parse_bandit_csv(file, date_info_dict): 
    try:   
        results_file_name = file.stem
        package_name, version_number = results_file_name.split("==")
        
        # Some date times might not be in the dict
        if (package_name, version_number) in date_info_dict:
            date_time = date_info_dict[(package_name, version_number)]
        else:
            date_time = None
        
        issues_count, issue_severity_count = None, None

        with open(file, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            if len(list(csv_reader)) == 0:
                issues_count = 0
                issue_severity_count = {"low": 0, "medium": 0, "high": 0, "critical": 0}

            else:
                if 'filename' and 'test_name' in csv_reader.fieldnames:
                    next(csv_reader, None) # skip the header line
                
                issues_count = (len(list(csv_reader)))
                issue_severity_count = {"low": 0, "medium": 0, "high": 0, "critical": 0}
                
                for row in csv_reader:
                    # TODO: Could hardcode less, but this is really easy to do
                    filename, test_name, test_id, issue_severity, issue_confidence, issue_cwe, \
                    issue_text, line_number, col_offset, end_col_offset, line_range, more_info = row
                    
                    # Increase the issue severity count per line
                    issue_severity_count[issue_severity.lower()] = issue_severity_count[issue_severity.lower()] + 1
                
            json_structure = {
                "package_name": package_name, #
                "package_version": version_number, #
                "datetime": date_time, #
                "num_issues": issues_count, # number of issues found by counting lines in csv
                "issue_severity": issue_severity_count,
            }  
            
            return json_structure
    except Exception as e:
        print(f"An error occurred while parsing Bandit CSV file '{file}': {e}")  
        
         # Get the traceback information
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # Print the traceback information, including the line number
        traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
        
        return None
              

def parse_timestamp(timestamp_str):
    try:
        datetime_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
        return {"date": datetime_obj.strftime("%Y-%m-%d"), 
                "time": datetime_obj.strftime("%H:%M")}
    except ValueError:
            # Handle the case where the timestamp format doesn't match
        return "Invalid timestamp format", ""
    
    
def get_package_datetime_info(date_info_file):
    date_info_dict = {}
    
    try:
        with open(date_info_file, 'r') as infh:
            reader = csv.reader(infh)
            next(reader)  # skip header line
            
            for row in reader:
                package_name = row[0].lower() # some packages use uppercase in names in this list
                version_number = row[1]
            
                date_info_dict.update({(package_name, version_number): parse_timestamp(row[2])})

            return date_info_dict
    except FileNotFoundError as e:
        print(f"File not found: %s" % date_info_file)
    except Exception as e:
        print(f"Un unexpected error occurred in `get_package_datetime_info`: {e}")
        


def process_csv_files(results_folder, date_info_file):
    # Check if the results folder does exist
    try:  
        if not results_folder.exists() or not results_folder.is_dir():
            raise FileNotFoundError("Given Bandit4Mal results folder does not exist.")
        elif not date_info_file.exists():
            raise FileNotFoundError("Given date info file {date_info_file} does not exist.")
        
        filenames       = find_sorted_csv_filenames(results_folder) # sorted filenames
        date_info_dict  = get_package_datetime_info(date_info_file) # (package, version): (date, timestamp)

        # print(date_info_dict)

        for filename in filenames:
            results_filename = results_folder / (filename + ".csv") 
            # print(results_filename)
            data = parse_bandit_csv(results_filename, date_info_dict)
            
            print(json.dumps(data, indent=2))

        # print(data)
        return None
    # Everything I want to do if results folder does not exist.
    except FileNotFoundError as e: 
        print(f"Error in `process_csv_files`: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in `process_csv_files`: {e}")
        return None



### ARGPARSE
# def parse_arguments():
#     parser = argparse.ArgumentParser(description="Extract information from CSV files.")
#     parser.add_argument(
#         "--results_folder", 
#         default="./results" if "--results_folder" not in sys.argv else None,
#         help="Path to the folder containing CSV files."
#     )
#     parser.add_argument(
#         "--date_info_file",
#         default=None,
#         help="Path to the file containing date information.",
#     )
#     return parser.parse_args()

def main():
    # args = parse_arguments()
    
    # if (args.results_folder == None and args.date_info_file == None)
    
    # Get the path of the current script
    script_path = Path(__file__).resolve()
    
    # strip the filename from the path
    script_directory = script_path.parent
    
    # Results path for Bandit4Mal script
    results_folder = script_directory / "results"
    date_info_file = script_directory / "list_libraries.csv" # might need to change it, so we can add this with argparse arguments if we want!
    
    print("Current script:", script_path)
    print("Current directory:", script_directory)
    print("Current date_info_file:", date_info_file)
    
    process_csv_files(results_folder, date_info_file)
    
    

if __name__ == "__main__":
    main()