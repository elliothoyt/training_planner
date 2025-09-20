import pandas as pd
import datetime
from datetime import datetime, timedelta
import os.path
import json
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from tools import csvfilename


def load_config(config_path="data/config.json"):
    with open(config_path, 'r') as f:
        return json.load(f)

# If modifying these SCOPES, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def get_local_rfc3339_offset():
    tz_offset = datetime.now().astimezone().strftime('%z')
    return tz_offset[:3] + ':' + tz_offset[3:]  # e.g. "+02:00" or "-04:00"

def to_rfc3339(time_str):
  
    """Convert 'm/d/Y H:M' string to RFC3339 with local timezone."""
    dt = datetime.strptime(time_str, "%m/%d/%y %H:%M")
    tz_offset = datetime.now().astimezone().strftime('%z')
    tz_offset = tz_offset[:3] + ':' + tz_offset[3:]  # RFC3339 style
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + tz_offset





def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def add_event(service, summary, start, end, description='', location=''):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'UTC',  # Change if you want to use your local timezone
        },
        'end': {
            'dateTime': end,
            'timeZone': 'UTC',
        }
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")

def main():
    service = authenticate_google_calendar()
    config=load_config()
    csv_directory = os.path.abspath(config["csv_directory"])
    # Load CSV
    filename=csvfilename(csv_directory)
    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        try:
            # skip empty rows - might show up at the end of the csv file
            if pd.isna(row['summary']) or pd.isna(row['start_time']) or pd.isna(row['end_time']):
                continue  # just skip silently
            # combine date + time
            start_dt = to_rfc3339(row['start_time'])
            end_dt = to_rfc3339(row['end_time'])
            print({
                'summary': row['summary'],
                'start': start_dt,
                'end': end_dt
            })

            #add event
            add_event(
                service,
                summary=row['summary'],
                start=start_dt,
                end=end_dt,
                description=row.get('description', '')
            )
        except Exception as e:
            print(f"Failed to add event '{row['summary']}': {e}")




if __name__ == '__main__':
    main()
