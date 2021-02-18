##Pulls Overdue and next 2 day's of tasks from Todoist
##Done day-by-day for ease of concatenation/sorting of final list
##...and because I don't fucking know python
import requests
import json
import datetime
import re
import argparse
import sys

#define and require input of API key from command line
parser = argparse.ArgumentParser(description='API Key')
parser.add_argument('--api', type=str, help='Todoist API key')

args = parser.parse_args()

if not args.api:
    sys.exit("Please specify your API key with the --api flag")

#set tomrrows date in format e.g. 14 Feb for the API filter
twodays_t = datetime.datetime.today() + datetime.timedelta(days=2)
twodays = twodays_t.strftime("%d %b")

#API tasks URL
BASE_URL = "https://api.todoist.com/rest/v1/tasks"

#HTTP header w/ API token
headers = {
  "Authorization": "Bearer " + args.api
}

#set filter strings
params_overdue = {
  "filter": "overdue"
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
with open('tasks.txt', 'w') as f:
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
with open('tasks.txt', 'r') as f:
    lines = f.readlines()
with open('tasks.txt', 'w') as f:
    for line in lines:
        f.write(re.sub('^dict_values\(\[\'', '', line))

#remove ']) from text file line ends
with open('tasks.txt', 'r') as f:
    lines = f.readlines()
with open('tasks.txt', 'w') as f:
    for line in lines:
        f.write(re.sub('\'\]\)', '', line))
