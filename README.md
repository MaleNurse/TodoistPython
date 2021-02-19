# TodoistPython
 Python script for pulling Todoist tasks to a text file, maybe more later.

`python task_list.py --a APIKEY [--o OUTPUT]`

If no filename or path specified in OUTPUT, creates "task_list.txt" in current directory with overdue and next 2 days of tasks; e.g.:

```
OVERDUE:
Have sex

Today:
EAQ
435 Response, reading
python parser, package list

Tomorrow:
Recycling
cancel outback Sirius
Drug Cards
air filters
CH202 Paper

In 2 Days:
N248 paper
```
If run in something like cron, it will keep the list updated. I utilize this to display on a KLWP wallpaper so I don't have to use a widget and can animate/hide it.

Example cron entry for updates every 15min:
`*/15 * * * *   python /home/zach/TodoistPython/task_list.py -a XXXXXXXXXXXXXXXX -o /var/www/html/tasks.txt >/var/log/todoist.log 2>&1` 

Sorry for the messy code if someone actually looks at this; I have no clue what I'm doing.

[See the integrations menu in your Todoist account for your API key.](https://todoist.com/prefs/integrations)
