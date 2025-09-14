import json
import csv
from datetime import datetime, timedelta
import sys
import os
from weekconfig import FILENAMEJSON


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


def load_config(config_path="data/config.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

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

def prompt_for_event_details(data):
    events = []
    for weekday, time_str in data.items():
        try:
            event_date = get_next_week_date(weekday)
            # Combine date with time
            full_start_str = f"{event_date} {time_str}"
            start_dt = datetime.strptime(full_start_str, "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(hours=2)

            print(f"\nEvent on {weekday.title()} {event_date} at {time_str}")
            summary = input("  Enter summary: ").strip()
            description = input("  Enter description: ").strip()

            events.append({
                "start_time": start_dt.strftime("%Y-%m-%d %H:%M"),
                "end_time": end_dt.strftime("%Y-%m-%d %H:%M"),
                "summary": summary,
                "description": description
            })
        except Exception as e:
            print(f"Skipping {weekday}: {e}")
    return events

def csvfilename(csv_directory):
    today = datetime.today()
    # Monday is 0 in weekday(), Sunday is 6
    days_ahead = (0 - today.weekday()) % 7  # how many days to next Monday
    # if today is Monday, days_ahead=0, else days_ahead>0
    next_monday = today + timedelta(days=days_ahead)
    date_str = next_monday.strftime("%Y-%m-%d")  # or any format you like
    csv_name = f"{date_str}{BASEFILENAME}"
    csv_filename = os.path.join(csv_directory,csv_name)
    return csv_filename

def save_to_csv(events):
    
    filename=csvfilename()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["start_time", "end_time", "summary", "description"])
        writer.writeheader()
        writer.writerows(events)
    print(f"\nCSV saved as '{filename}'")

def main():
    try:
        print("load config")
        config=load_config()
        print("define CSV directory")
        csv_directory = os.path.abspath(config["csv_directory"])
        print("define json dir")        
        json_directory = os.path.abspath(config["json_directory"])
        print("load weekly schedule")
        data = load_json(json_directory,FILENAMEJSON)
        print(f"{data}")
        events = prompt_for_event_details(data)
        if events:
            save_to_csv(events,csv_directory)
        else:
            print("No events to save.")
    except FileNotFoundError:
        print("JSON file not found. Please run the first script to create '{FILENAMEJSON}'.")


main()
