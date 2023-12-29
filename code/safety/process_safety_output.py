import traceback
from pathlib import Path
import json
import csv
from packaging import version
from datetime import datetime
import pprint # pretty print for easier json print

# PARSE PATH
def get_data_path(json_filename = None, date_info_filename = None):
    script_path = Path(__file__).resolve()
    script_directory    = script_path.parent
    json_file           = script_directory / json_filename
    date_info_file      = script_directory / date_info_filename
    
    return json_file, date_info_file, script_directory

# PARSE DATETIME
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


# PARSE JSON
def load_json_file(file):
        with open(file, encoding='utf-8') as json_file:
            data = json.load(json_file)         
            return data

def parse_safety_json_output(json_dict: dict):
    pprint.pprint(type(json_dict["vulnerabilities"][0]))

def main():
    json_file_path, date_info_file, script_directory = get_data_path("safety_set.json", "list_libraries.csv")

    print("JSON file path:", json_file_path)
    print("Current directory:", script_directory)
    print("date_info_file:", date_info_file)

    json_dict = load_json_file(json_file_path)
    
    parse_safety_json_output(json_dict)


if __name__ == "__main__":
    main()