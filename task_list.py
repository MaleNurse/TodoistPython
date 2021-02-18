##Pulls Overdue and next 2 day's of tasks from Todoist
##Done day-by-day for ease of concatenation/sorting of final list
##...and because I don't fucking know python
import requests
import json
import datetime
import re
import argparse
import sys
import os.path

#define and require input of API key from command line
def arg_parsing():
    parser = argparse.ArgumentParser(description='Todoist Text List Generator')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-a', '--apikey', type=str, help='Todoist API key', required=True)
    optional.add_argument('-o', '--output', type=str, help='Path and/or name for text file')
    return parser.parse_args()

args = arg_parsing()

#exit and bitch if API key wasn't supplied
if not args.apikey:
    sys.exit("Please specify your API key with the --api flag")

#set regex patterns for files ending in ".txt" or paths ending in "/"
file_pattern = re.compile(".*\.txt$")
path_pattern = re.compile(".*\\$")

#if out not supplied use default
if not args.output:
    text_file = "task_list.txt"
#if filename and path were supplied, use it
elif file_pattern.match(args.output):
    text_file = args.output
#if a path ending with "/" was supplied, use it with a default filename
elif path_pattern.match(args.output):
    text_file = args.output + "task_list.txt"
#other wise assume that a path was supplied that wasn't ended with "/"
else:
    text_file = args.output + "/task_list.txt"

#check if the supplied/default path exists and if we can write to it
def test_path():
    try:
        open(text_file, 'w')
        return True
    except OSError:
        return False

if not test_path():
    sys.exit("\nInvalid path or insufficient permissions")

#set 2 days in the future's date in format "14 Feb" for the API filter
twodays_t = datetime.datetime.today() + datetime.timedelta(days=2)
twodays = twodays_t.strftime("%d %b")

#API tasks URL
BASE_URL = "https://api.todoist.com/rest/v1/tasks"

#HTTP header w/ API token
headers = {
  "Authorization": "Bearer " + args.apikey
}

#set filter strings
params_overdue = {
  "filter": "overdue|yesterday" #yesterday req b/c API doesn't think it's overdue...
}

params_today = {
  "filter": "today"
}

params_tomorrow = {
  "filter": "tomorrow"
}

params_twodays = {
  "filter": twodays
}

#send reqeusts to Todoist
response_overdue = requests.get(BASE_URL, headers=headers, params=params_overdue)
response_today = requests.get(BASE_URL, headers=headers, params=params_today)
response_tomorrow = requests.get(BASE_URL, headers=headers, params=params_tomorrow)
response_twodays = requests.get(BASE_URL, headers=headers, params=params_twodays)

#Check response code and exit if error
if response_today.status_code == 403 or response_overdue.status_code == 403 or response_tomorrow.status_code == 403 or response_twodays.status_code == 403:
    sys.exit("API returned '403 Forbidden'. Check API key")
elif response_today.status_code == 204 or response_overdue.status_code == 204 or response_tomorrow.status_code == 204 or response_twodays.status_code == 204:
    sys.exit("API returned no data")
elif response_today.status_code != 200 or response_overdue.status_code != 200 or response_tomorrow.status_code != 200 or response_twodays.status_code != 200:
    print(response_today.status_code)
    print(response_overdue.status_code)
    print(response_tomorrow.status_code)
    print(response_twodays.status_code)
    sys.exit("Unknown error from API, See HTTP status codes above")

#place API response text in JSON array
json_array_overdue = json.loads(response_overdue.text)
json_array_today = json.loads(response_today.text)
json_array_tomorrow = json.loads(response_tomorrow.text)
json_array_twodays = json.loads(response_twodays.text)

#init task arrays
tasks_overdue = []
tasks_today = []
tasks_tomorrow = []
tasks_twodays = []

#pull only the "content" key (i.e. the task name)
for item in json_array_overdue:
    task_details = {"content":None}
    task_details['content'] = item['content']
    tasks_overdue.append(task_details)

for item in json_array_today:
    task_details = {"content":None}
    task_details['content'] = item['content']
    tasks_today.append(task_details)

for item in json_array_tomorrow:
    task_details = {"content":None}
    task_details['content'] = item['content']
    tasks_tomorrow.append(task_details)

for item in json_array_twodays:
    task_details = {"content":None}
    task_details['content'] = item['content']
    tasks_twodays.append(task_details)

#write the task list line-by-line in a text file, omitting date headers w/o tasks
with open(text_file, 'w') as f:
    if tasks_overdue:
        f.write("OVERDUE:\n")
        for item in tasks_overdue:
            f.write("%s\n" % item.values())
        f.write("\n")
    if tasks_today:
        f.write("Today:\n")
        for item in tasks_today:
            f.write("%s\n" % item.values())
        f.write("\n")
    if tasks_tomorrow:
        f.write("Tomorrow:\n")
        for item in tasks_tomorrow:
            f.write("%s\n" % item.values())
        f.write("\n")
    if tasks_twodays:
        f.write("In 2 Days:\n")
        for item in tasks_twodays:
            f.write("%s\n" % item.values())

#remove dict_values([' from text file line beginnings
with open(text_file, 'r') as f:
    lines = f.readlines()
with open(text_file, 'w') as f:
    for line in lines:
        f.write(re.sub("^dict_values\(\[\'", '', line))

#remove ']) from text file line ends
with open(text_file, 'r') as f:
    lines = f.readlines()
with open(text_file, 'w') as f:
    for line in lines:
        f.write(re.sub("\'\]\)", '', line))
