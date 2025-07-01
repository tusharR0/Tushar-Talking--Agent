import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Read credentials JSON from environment variable
creds_json = os.environ.get("GOOGLE_CREDS_JSON")

if creds_json is None:
    raise ValueError("Environment variable GOOGLE_CREDS_JSON not set")

credentials = service_account.Credentials.from_service_account_info(
    json.loads(creds_json), scopes=SCOPES
)

service = build('calendar', 'v3', credentials=credentials)
calendar_id = 'tusharraut704@gmail.com'

def get_free_slots():
    return ["Tomorrow 3PM", "Friday 4PM"]

def book_event(start_time, end_time, summary):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'}
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()

