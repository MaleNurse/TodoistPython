# TodoistPython
 Python script for pulling Todoist tasks to a text file, maybe more later.

`python task_list.py --api XXXXXX`

Creates "tasks.txt" with overdue and next 2 days of tasks e.g.:

```
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
If run in something like cron, it will keep the list updated. I utilize this to display on a KLWP wallpaper. Sorry for the messy code if someone actually looks at this, I have no clue what I"m doing.

[See the integrations menu in your Todoist account for your API key.](https://todoist.com/prefs/integrations)
