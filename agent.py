from calendar_utils import book_event, service, calendar_id
from datetime import datetime, timedelta
import dateparser  # type: ignore
import pytz        # type: ignore
import re

# Timezone
IST = pytz.timezone('Asia/Kolkata')

# State
pending_booking = {}
last_context = {}

def extract_time_range(text):
    match = re.search(
        r"(\d{1,2})(:(\d{2}))?\s*(AM|PM)?\s*(to|-|–)\s*(\d{1,2})(:(\d{2}))?\s*(AM|PM)?",
        text, re.IGNORECASE
    )
    if match:
        start_hour = int(match.group(1))
        end_hour = int(match.group(6))
        ampm1 = match.group(4)
        ampm2 = match.group(10) or ampm1

        if ampm1 and ampm1.lower() == "pm" and start_hour < 12:
            start_hour += 12
        if ampm2 and ampm2.lower() == "pm" and end_hour < 12:
            end_hour += 12

        return start_hour, end_hour
    return None, None

def smart_parse(text, previous_date=None):
    duration_minutes = 30
    start_hour, end_hour = extract_time_range(text)

    has_date = any(word in text.lower() for word in [
        "january", "february", "march", "april", "may", "june", "july",
        "august", "september", "october", "november", "december",
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
        "tomorrow", "today", "next", "this", "week", "month"
    ])

    if has_date:
        parsed = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
        base_date = parsed if parsed else datetime.now() + timedelta(days=1)
    elif previous_date:
        base_date = previous_date
    else:
        base_date = datetime.now() + timedelta(days=1)

    date_only = base_date.replace(hour=0, minute=0, second=0, microsecond=0)

    if start_hour is not None:
        start_time = date_only.replace(hour=start_hour)
        end_time = date_only.replace(hour=end_hour)
    elif "afternoon" in text.lower():
        start_time = date_only.replace(hour=14)
        end_time = date_only.replace(hour=17)
    else:
        start_time = date_only.replace(hour=15)
        end_time = start_time + timedelta(minutes=duration_minutes)

    return IST.localize(start_time), IST.localize(end_time), has_date

def find_free_slot_between(start, end, duration_minutes=30):
    current = start
    while current + timedelta(minutes=duration_minutes) <= end:
        slot_start = current
        slot_end = slot_start + timedelta(minutes=duration_minutes)

        events = service.events().list(
            calendarId=calendar_id,
            timeMin=slot_start.isoformat(),
            timeMax=slot_end.isoformat(),
            singleEvents=True
        ).execute()

        if not events.get('items', []):
            return slot_start, slot_end
        current += timedelta(minutes=15)

    return None, None

def run_agent(user_input):
    global pending_booking, last_context

    # Booking confirmation
    if user_input.strip().lower() in ["yes", "book it", "confirm", "sure"] and pending_booking:
        slot_start, slot_end = pending_booking["slot"]
        event = book_event(
            slot_start.isoformat(),
            slot_end.isoformat(),
            summary="Meeting booked via TailorTalk"
        )
        pending_booking = {}
        return f"✅ Meeting booked for {slot_start.strftime('%A, %d %B %Y at %I:%M %p')}!\nEvent ID: {event.get('id')}"

    # Parse intent
    start_time, end_time, has_date = smart_parse(user_input, last_context.get("date"))
    if has_date:
        last_context["date"] = start_time

    is_fixed = (end_time - start_time) <= timedelta(minutes=31)

    if is_fixed:
        # Check for conflicts
        events = service.events().list(
            calendarId=calendar_id,
            timeMin=start_time.isoformat(),
            timeMax=end_time.isoformat(),
            singleEvents=True
        ).execute()

        print("🧪 Calendar check:", events.get("items", []))  # Debugging

        if not events.get("items", []):
            pending_booking = {"slot": (start_time, end_time)}
            return f"🕒 You're free on {start_time.strftime('%A, %d %B %Y at %I:%M %p')}. Shall I book it?"
        else:
            conflict = events.get("items")[0]
            when = conflict['start'].get('dateTime', conflict['start'].get('date'))
            return f"❌ You're already booked at {when}. Try another time."

    # Handle flexible ranges
    slot_start, slot_end = find_free_slot_between(start_time, end_time)
    if slot_start:
        pending_booking = {"slot": (slot_start, slot_end)}
        return f"🕒 You're free on {slot_start.strftime('%A at %I:%M %p')}. Shall I book it?"
    else:
        return "❌ You're already booked during that time range. Try another window."

