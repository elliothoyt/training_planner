import json
import os

# A constant filename – or load from your config.json
WEEKLYSCHEDULEFILENAME = "weekly_schedule.json"

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

    json_file = os.path.join(json_directory, WEEKLYSCHEDULEFILENAME)
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
    json_file = os.path.join(json_directory, WEEKLYSCHEDULEFILENAME)
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return {}

