import datetime
import os
from google.oauth2 import service_account  # type: ignore
from googleapiclient.discovery import build  # type: ignore

# 🔐 Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# ✅ Path to credentials.json (must match uploaded path in Render)
SERVICE_ACCOUNT_FILE = "credentials.json"

# ✅ Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# ✅ Build the Google Calendar service
service = build('calendar', 'v3', credentials=credentials)

# ✅ Calendar ID (usually 'primary' or email)
calendar_id = 'tusharraut704@gmail.com'

# ✅ Optional: Return dummy free slots
def get_free_slots():
    return ["Tomorrow 3PM", "Friday 4PM"]

# ✅ Function to book an event
def book_event(start_time, end_time, summary):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'}
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()


