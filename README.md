# System & Software Security - Assignment 2

--------------

# Setup

1. Create and enter a virtual environment through the commands

```python
python3 -m venv venv
source ./venv/bin/activate
```

2. Install Bandit4mal with the command

```python
pip install bandit
```

3. Install Safety with the command

```python
pip install safety
```

4. To prepare the dataset (for reproducing with a new dataset), run the Python file ```create_subset.py``` to generate the following files:
```
subset_data.csv
subset_requirements.txt
```
These were generated from ```list_libraries.csv```, which is the original dataset used by Alfadel et al. For the scope of this project, we only use a subset of 1% of the dataset, which is randomly sampled by ```create_subset.py```.

```Subset_data.csv``` contains package data, including package names, versions and release dates.
```Subset_requirements.txt``` contains the same packages as subset_data.csv, but in requirements.txt format, like: ```{packagename}=={versionnr}```. The requirements file will be used by Bandit4mal and Safety, whereas the data file is used to label the results with dates.

NOTE: The currently present ```subset_data.csv``` and ```subset_requirements.txt``` were used by us for analysis. Running ```create_subset.py``` would overwrite those files and generate new datasets.

5. Copy these two files in the bandit folder and the safety folder. Copy the ```subset_data.csv``` into the graphs folder.

# Running Bandit4Mal

1. With the ```subset_requirements.txt``` present in the local folder, run ```./bandit_run.sh```.
2.  The script does for every package in the requirements file:
    1. ```pip download {packagename}=={versionnr}```
    2. Extract its contents given a tar.gz or zip. If a whl is given, then it is renamed to zip, then extracted
    3. Move into the extracted folder
    4. ```bandit -r . -f csv | tail -n +2 >> ../../results/$1.csv```. This simply runs bandit recursively, outputs a csv file, and removes the headers from the csv. Then it is saved to ```{packagename}=={versionnr}.csv```
    5. Delete the extracted folder and the tar.gz/zip

After the script is done running, there should be a results folder present containing csv files for Bandit runs of each package in the requirements file that was successful. Cases where a package cannot be downloaded or does not exist in pip are skipped automatically. 

NOTE: The contents of the results folder are not deleted when running ```bandit_run.sh```. The data is appended. Make sure to delete this folder manually if you want to obtain new data without using ours.


# Running Safety

Instead of needing a script, running safety is a lot easier:

```
safety check -r subset_requirements.txt --output json > safety_set.json
```

For the next step, make sure that either this command is run inside the safety folder or that the .json is moved into the safety folder for preprocessing.

# Data analysis

## Preprocessing the results

### Bandit4mal

After running Bandit4mal, we end up with a results folder with lots of .csv files. We can preprocess these by running the ```process_bandit4mal_output.py``` file. This script does require the ```list_libraries.csv``` to be present to fix any lost dates during the run. The script scans for all csv files present in the results folder and formats them to json. The output is a file named ```bandit_results.json```, which can be used for generating the graphs.

Make sure to copy/move this ```bandit_results.json``` into the graphs folder.

### Safety 

After running Safety, we end up with a ```safety_set.json``` file. We can preprocess this file with ```process_safety_output.py``` to format it in the same structure as the bandit json, such that we can reuse graph generation code easily. Just like Bandit, this script does require the ```list_libraries.csv``` to be present to fix the lost dates. To structurise our data in the generated ```safety_results.json``` for graph generation, we get rid of all vulnerability information, except the severity level, date and version of the package.

Make sure to copy/move ```safety_results.json``` into the graphs folder.

## Generating graphs

Inside the graphs folder, there is a notebook file ```security_plots.ipynb```, which contains all the code we used to generate various graphs. Ensure that the ```subset_data.csv```, ```bandit_results.json``` and ```safety_results.json``` files are present in the graphs folder. 

# Repo structure

The repository contains the following files in the ```code``` directory: 
* Package data
    - ```list_libraries.csv```
    - ```subset_data.csv``` (can be generated)
    - ```subset_requirements.txt``` (can be generated)

* Scripts
    - ```create_subset.py```

* Folders
    - bandit
        - Scripts
            - ```bandit_run.sh```
            - ```process_bandit4mal.output.py```
        - Data
            - ```results``` (can be generated)
    - safety
        - Scripts
            - ```safety_run.sh```
            - ```process_safety_output.py```
        - Data
            - ```safety_set.json``` (can be generated)
    - graphs
        - Scripts
            - ```security_plots.ipynb```
        - Data
            - ```bandit_results.json``` (can be generated)
            - ```safety_results.json``` (can be generated)