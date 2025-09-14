import json
import sys
import os
import re


WEEKLYSCHEDULEFILENAME = "weekly_schedule.json"
pattern = re.compile(r"^(?:[01]?\d|2[0-3]):[0-5]\d$")  # HH:MM or H:MM

def load_config(config_path="data/config.json"):
    with open(config_path, 'r') as f:
        return json.load(f)



# Example usage:

def get_weekday_data():
    data = {}
    print("Enter weekday and time pairs. Type 'done' when finished.", flush=True)
    while True:
        print("Enter a weekday (e.g., Monday): ", flush=True)
        weekday = input().strip()
        if weekday.lower() == 'done':
            break
        
        while True:
            print(f"Enter the time for {weekday} (e.g., 14:00): ", flush=True)
            time = input().strip()

            if pattern.match(time):
                break
            else:
                print("Invalid time format. Please use HH:MM (24-hour).", flush=True)
        data[weekday] = time
    return data

def save_to_json(data,json_directory):
    os.makedirs(json_directory, exist_ok=True)
    #print(f"{json_directory}")
    json_file = os.path.join(json_directory,WEEKLYSCHEDULEFILENAME)
    #print(f"{json_file}")
    path = os.path.abspath(json_file)
    #print(f"{path}")
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {WEEKLYSCHEDULEFILENAME}")


def main():
    config = load_config()
    print("Enter your weekly schedule.", flush=True)
    weekday_data = get_weekday_data()
    if weekday_data:
        json_directory = config["json_directory"]
        save_to_json(weekday_data,json_directory)
    else:
        print("No data entered. Nothing was saved.")

main()
