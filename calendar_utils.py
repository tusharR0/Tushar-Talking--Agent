import datetime
import os
from google.oauth2 import service_account # type: ignore
from googleapiclient.discovery import build # type: ignore

# Define the Google Calendar scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Dynamically load credentials from the same directory as this file
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

# Authenticate using service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Google Calendar service
service = build('calendar', 'v3', credentials=credentials)
calendar_id = 'tusharraut704@gmail.com'

# Placeholder function for available time slots
def get_free_slots():
    return ["Tomorrow 3PM", "Friday 4PM"]

# Function to book an event
def book_event(start_time, end_time, summary):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'}
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()
