# REQUIREMENTS ------------
# pip install requests
# -------------------------

# TODO:
# No validation done by assume everything is ok,
# But better to write validation logic too

import requests
import json
import os
import shutil

# Where the API is available
apiIndex = 'https://api.ce.pdn.ac.lk/people/v1'
# apiIndex = 'http://localhost:4001/people'

# Where the data is available
apiSource = 'https://people.ce.pdn.ac.lk/api/staff/'

# Split the email address into 2 fields
def emailFilter(email):
    if email != "":
        words = email.split('@')
        return { 'name':words[0], 'domain':words[1] }
    else:
        return { 'name': "", 'domain': "" }

# Delete the existing files first
def del_old_files():
    dir_path = "../people/v1/staff/"
    try:
        shutil.rmtree(dir_path)
    except error as e:
        print("Error !")

# Write the /staff/index.json
def write_index(staff_list):
    dict = {}

    for email in staff_list:
        raw = staff_list[email]
        email_id = email.split('@')[0]
        url = '{0}/staff/{1}/'.format(apiIndex,email_id)
        dict[email] = {
            'name': raw['name'],
            'url': url,
            'designation':  raw['designation']
        }

    filename = "../people/v1/staff/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(json.dumps(dict, indent = 4))

# Write the /staff/{email_id}/index.json files
def write_staff_pages(staff_list):
    for email in staff_list:
        raw_data = staff_list[email]
        email_id = email.split('@')[0]

        filename = "../people/v1/staff/" + email_id + "/index.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        data = {
            'name': raw_data['name'],
            'designation': raw_data['designation'],
            'email': raw_data['email'],
            'profile_url': raw_data['link'],
            'profile_image': raw_data['profile_image'],
            'urls': raw_data['urls'],
            'research_interests': raw_data['research_interests'],
        }

        with open(filename, "w") as f:
            f.write(json.dumps(data, indent = 4))

# Write the /staff/all/index.json file
def write_all(staff_list):
    data_all = {}
    sorted_data_all = {}

    filename = "../people/v1/staff/all/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    for email in staff_list:
        raw_data = staff_list[email]
        email_id = email.split('@')[0]

        raw_data = staff_list[email]
        data = {
            'name': raw_data['name'],
            'designation': raw_data['designation'],
            'email': raw_data['email'],
            'profile_url': raw_data['link'],
            'profile_image': raw_data['profile_image'],
            'urls': raw_data['urls'],
            'research_interests': raw_data['research_interests'],
        }
        data_all[email_id] = data

    # Sort in alphabatical order
    for key in sorted(data_all):
        sorted_data_all[key] = data_all[key]

    with open(filename, "w") as f:
        f.write(json.dumps(sorted_data_all, indent=4))


# ------------------------------------------------------------------------------

# Delete the existing files first
del_old_files()

r = requests.get(apiSource)
staff_list = {}

# Fetch data from the people.ce.pdn.ac.lk
if r.status_code==200:
    staff_list = json.loads(r.text)
    # print(staff_list)

    # Write the index file for the staff
    write_index(staff_list)

    # Create files for each staff member
    write_staff_pages(staff_list)

    # Create the aggregated index file
    write_all(staff_list)
