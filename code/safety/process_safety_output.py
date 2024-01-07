import traceback
import sys
import time
import string

from pathlib import Path
import json
import csv
from packaging import version
from datetime import datetime
import pprint as pp # pretty print for easier json print

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
                package_name = row[0].lower().replace('.', '-').replace('_', '-') # some packages use uppercase . or _ in names in this list
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

def parse_safety_json_output(json_dict: dict, date_info_file: dict):
    try:
        date_info_dict  = get_package_datetime_info(date_info_file) # (package, version): (date, timestamp)
        safety_list = []
        safety_dict = {}
        
        for entry in json_dict["vulnerabilities"]:
            package_name    = entry["package_name"]
            version_number  = entry["analyzed_version"]
            severity        = str(entry["severity"]).upper() if entry["severity"] is not None else "NULL"
            issue_severity_count_dict = {"NULL": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
            
            if (package_name.lower(), version_number) in date_info_dict:
                published_date_time = date_info_dict[(package_name.lower(), version_number)]
            else:
                published_date_time = {"date": None, "time": None}
                
            safety_dict_key = (package_name, version_number)
            
            # print(safety_dict_key)
            
            # check if this tupe in
            if safety_dict_key in safety_dict:
                # Get the index of the package information in the list with an extra dict 
                # instead of looping through the list every time.
                info_idx = safety_dict.get((package_name, version_number))               
                package_info = safety_list[info_idx]

                if (package_info.get("pkg_name") == package_name and package_info.get("pkg_version") == version_number):
                    package_info["num_issues"] += 1 # increment number of issues for that package
                    package_info["issue_severity"][severity] += 1
                    safety_list[info_idx] = package_info
                    
            else:
                # check if the severity value is in the list I gave. 
                if severity in ["NULL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]:
                    issue_severity_count_dict[severity] = 1

                json_structure = {
                    "pkg_name": package_name, #
                    "pkg_version": version_number, #
                    "published": published_date_time, #
                    "num_issues": 1, # number of issues found by counting lines in csv
                    "issue_severity": issue_severity_count_dict,
                }
                    
                safety_list.append(json_structure)
                # Add to the dictionary the (package_name, version_number) tuple with the index in the list as a value.
                # This way if it's not in the right order I can easily find the index of something I want to upgrade
                idx = len(safety_list) - 1
                safety_dict.update({safety_dict_key: idx})
                
        sorted_data = sorted(safety_list, key=lambda x: (x["pkg_name"], version.parse(x["pkg_version"]))) # Sorted by name and then version numbers.
        return sorted_data
        
                      
    except Exception as e:
        print(f"An error has occured while parsing the Safety file: {e}")
        
        # Get the traceback information
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # Print the traceback information, including the line number
        traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
        
        return None


def parse_alternative_json_output(json_dict: dict, date_info_file: dict):
    try:
        # pp.pprint(json_dict)
        date_info_dict  = get_package_datetime_info(date_info_file) # (package, version): (date, timestamp)
        safety_list = []
        safety_dict = {}
        
        # Loop through whole output
        for scan in json_dict:
            for entry_nr, entry in enumerate(scan["vulnerabilities"]):
                package_name    = entry["package_name"]
                version_number  = entry["analyzed_version"]
                severity        = str(entry["severity"]).upper() if entry["severity"] is not None else "NULL"
                issue_severity_count_dict = {"NULL": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
                
                if (package_name.lower(), version_number) in date_info_dict:
                    published_date_time = date_info_dict[(package_name.lower(), version_number)]
                else:
                    published_date_time = {"date": None, "time": None}
                    
                safety_dict_key = (package_name, version_number)
                
                # print(safety_dict_key)
                
                # check if this tupe in
                if safety_dict_key in safety_dict:
                    # Get the index of the package information in the list with an extra dict 
                    # instead of looping through the list every time.
                    info_idx = safety_dict.get((package_name, version_number))               
                    package_info = safety_list[info_idx]

                    if (package_info.get("pkg_name") == package_name and package_info.get("pkg_version") == version_number):
                        package_info["num_issues"] += 1 # increment number of issues for that package
                        package_info["issue_severity"][severity] += 1
                        safety_list[info_idx] = package_info
                        
                else:
                    # check if the severity value is in the list I gave. 
                    if severity in ["NULL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]:
                        issue_severity_count_dict[severity] = 1

                    json_structure = {
                        "pkg_name": package_name, #
                        "pkg_version": version_number, #
                        "published": published_date_time, #
                        "num_issues": 1, # number of issues found by counting lines in csv
                        "issue_severity": issue_severity_count_dict,
                    }
                        
                    safety_list.append(json_structure)
                    # Add to the dictionary the (package_name, version_number) tuple with the index in the list as a value.
                    # This way if it's not in the right order I can easily find the index of something I want to upgrade
                    idx = len(safety_list) - 1
                    safety_dict.update({safety_dict_key: idx})
                    
        sorted_data = sorted(safety_list, key=lambda x: (x["pkg_name"], version.parse(x["pkg_version"]))) # Sorted by name and then version numbers.
        return sorted_data
            
        

    
    except Exception as e:
        print(f"An error has occured while parsing the Safety file: {e}")
        exc_type, exc_value, exc_traceback = sys.exc_info() # Get the traceback information  
        traceback.print_tb(exc_traceback, limit=1, file=sys.stderr) # Print the traceback information, including the line number
        return None
    


def extract_information():
    json_file_path, date_info_file, script_directory = get_data_path("safety_set.json", "list_libraries.csv")

    # print("JSON file path:", json_file_path)
    # print("Current directory:", script_directory)
    # print("date_info_file:", date_info_file)

    json_dict = load_json_file(json_file_path)
    # pp.pprint(json_dict["vulnerabilities"])
    # data = parse_safety_json_output(json_dict, date_info_file)
    data = parse_alternative_json_output(json_dict, date_info_file)

    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    extract_information()