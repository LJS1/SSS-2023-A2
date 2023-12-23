# This is a sample Python script.
import csv
import random

# run npm install -g snyk to install snyk globally (requires node.js)
# run 'snyk auth' to login before we start

def get_total_packages():
    all_data=[]
    pkgs=[]
    line_nums = []
    pkg_name = None
    with open('list_libraries.csv') as f:
        plines = f.readlines()
    i = 0
    for pline in plines:
        package_data = pline.split(",")
        date = package_data[2].split(" ")[0]
        package_data[2] = date
        all_data.append(package_data[0:3])
        if(package_data[0] != pkg_name):
            pkg_name = package_data[0]
            pkgs.append(package_data[0])
            line_nums.append(i)
        i += 1
    return all_data, line_nums

def create_subset(all_data, pkg_lines, size):
    pkgs_with_versions = []
    chose_lines = random.sample(pkg_lines, int(len(pkg_lines)*size))
    for line in chose_lines:
        l = 0
        while all_data[line][0] == all_data[line+l][0]:
            pkg_data = all_data[line+l]
            pkgs_with_versions.append(pkg_data)
            l+=1
    # write csv for data
    with open('subset_data.csv', 'w', newline="") as f:
        writer = csv.writer(f, lineterminator= '\n')
        writer.writerows(pkgs_with_versions)
    # write requirements for testing
    with open("subset_requirements.txt", "w") as file:
        for line in pkgs_with_versions:
            file.write(line[0]+"=="+line[1] )
            file.write("\n")

if __name__ == '__main__':
    all_data, line_nums = get_total_packages()
    print(len(line_nums))
    print(line_nums[4])
    subset_size = 0.01
    subset = create_subset(all_data, line_nums, subset_size)
