import datetime
from datetime import datetime, timedelta
import json
import os
import csv
import sys
#Constants:

WELCOMETEXT="""Welcome to Training Planner v0.1. 
Use the "Configure Week Schedule" button to configure your typical weekly schedule
Then "Write Weekly Training Plan" to specify workouts for the upcoming week
The "Push Weekly Plan to GCal", which may prompt you for Google OAUTH



2025, Elliot Hoyt
"""

FILENAMEJSON="weekly_schedule.json"
BASEFILENAMECSV="weekly_training_plan.csv"
# Mapping weekday names to weekday indices (Monday=0, Sunday=6)
WEEKDAY_INDEX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
#Functions:

def load_config(config_path="data/config.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

def save_week_schedule(schedule):
    """
    Save weekly schedule to a JSON file.
    schedule: a list of dicts like [{"day":"Monday","time":"14:00"}, ...]
    json_directory: folder where JSON file should be saved.
    """
    # Make sure directory exists

    config=load_config()
    json_directory = os.path.abspath(config["json_directory"])
    os.makedirs(json_directory, exist_ok=True)

    # Convert schedule list to dict: {day: time}
    data = {}
    for item in schedule:
        day = item.get("day")
        time = item.get("time")
        if day and time:
            data[day] = time

    json_file = os.path.join(json_directory, FILENAMEJSON)
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Week schedule saved to {json_file}")
    return json_file

def load_week_schedule():
    """
    Load an existing week schedule JSON file if it exists.
    Returns dict {day: time} or {} if none.
    """
    config=load_config()
    json_directory = os.path.abspath(config["json_directory"])
    json_file = os.path.join(json_directory, FILENAMEJSON)
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return {}

def valid_time(t):
    try:
        datetime.strptime(t, "%H:%M")
        return True
    except ValueError:
        return False


def load_json(json_directory, filename=FILENAMEJSON):
    filename = os.path.join(json_directory, filename)
    print(f"{filename}")
    with open(filename, 'r') as f:
        return json.load(f)

def get_next_week_date(weekday_name):
    today = datetime.today()
    weekday_name_lower = weekday_name.strip().lower()
    if weekday_name_lower not in WEEKDAY_INDEX:
        raise ValueError(f"Invalid weekday: {weekday_name}")
    
    target_weekday = WEEKDAY_INDEX[weekday_name_lower]

    # Start of next week (next Monday)
    days_until_next_monday = (7 - today.weekday()) % 7
    days_until_next_monday = 7 if days_until_next_monday == 0 else days_until_next_monday
    next_monday = today + timedelta(days=days_until_next_monday)

    # Get date of the target weekday in next week
    days_offset = (target_weekday - 0)  # 0 = Monday
    target_date = next_monday + timedelta(days=days_offset)

    return target_date.date()

def csvfilename(csv_directory):
    today = datetime.today()
    # Monday is 0 in weekday(), Sunday is 6
    days_ahead = (0 - today.weekday()) % 7  # how many days to next Monday
    # if today is Monday, days_ahead=0, else days_ahead>0
    next_monday = today + timedelta(days=days_ahead)
    date_str = next_monday.strftime("%Y-%m-%d")  # or any format you like
    csv_name = f"{date_str}{BASEFILENAMECSV}"
    csv_filename = os.path.join(csv_directory,csv_name)
    return csv_filename

def events_to_csv(events):
    payload=[]
    for i in events:
        event_date = get_next_week_date(i["day"])
        full_start_str = f"{event_date} {i['time']}"
        start_dt = datetime.strptime(full_start_str, "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(hours=2)
        payload.append({
            "start_time": start_dt.strftime("%m/%d/%y %H:%M"),
            "end_time": end_dt.strftime("%m/%d/%y %H:%M"),
            "summary": i['summary'],
            "description": i['description']
        })
    return payload


def save_to_csv(events):
    config=load_config()
    payload=events_to_csv(events)
    csv_directory = os.path.abspath(config["csv_directory"])
    filename=csvfilename(csv_directory)
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["start_time", "end_time", "summary", "description"])
        writer.writeheader()
        writer.writerows(payload)
    print(f"\nCSV saved as '{filename}'")



