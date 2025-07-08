# ./reminder_logic.py
"""
This module contains the core business logic for fetching schedule data
and generating all reminder content (subjects and bodies).
It is the single source of truth.
"""
import json
from datetime import datetime, timedelta

def load_schedule_data(file_path="./src/schedule.json"):
    # ... (this function is unchanged)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Schedule file not found at {file_path}")
        return None

def get_schedule_for_date(target_date, schedule_data):
    # ... (this function is unchanged)
    if not schedule_data:
        return None
    target_date_str = target_date.strftime("%Y-%m-%d")
    for entry in schedule_data:
        if entry["date"] == target_date_str:
            return entry
    return None

def _format_medication_lines(medications):
    # ... (this internal helper is unchanged)
    lines = []
    for med in medications:
        name = med.get("name")
        details = med.get("details")
        prefix = ""
        if med.get("is_start", False): prefix = "START: "
        elif med.get("is_stop", False): prefix = "LAST DAY: "
        elif med.get("is_trigger", False): prefix = "TRIGGER: "
        lines.append(f"- {prefix}{name.upper()} - {details}")
    return lines

def format_full_reminder_body(day_data, day_label):
    # ... (this function is unchanged)
    if not day_data:
        return f"No schedule found for {day_label}."
    body_lines = [f"--- {day_label}'s Schedule ---"]
    items_found = False
    milestone = day_data.get("milestone")
    appointments = day_data.get("appointments", [])
    if milestone or appointments:
        items_found = True
        body_lines.append("\nEvents & Appointments:")
        if milestone:
            body_lines.append(f"- {milestone}")
        for appt in appointments:
            body_lines.append(f"- {appt.get('time', '')}: {appt.get('what', '')} at {appt.get('where', '')}")
    medications = day_data.get("medications", [])
    if medications:
        items_found = True
        body_lines.append("\nMedications:")
        body_lines.extend(_format_medication_lines(medications))
    if not items_found:
        return f"No specific appointments or medications scheduled for {day_label}."
    return "\n".join(body_lines)

def format_evening_checklist_body(day_data):
    # ... (this function is unchanged)
    if not day_data or not day_data.get("medications"):
        return "No medications to checklist for this evening."
    medications = day_data.get("medications", [])
    body_lines = [
        "--- Medication Checklist for Today ---",
        "This is a check-in to make sure all of today's medications have been taken as scheduled.",
        ""
    ]
    body_lines.extend(_format_medication_lines(medications))
    return "\n".join(body_lines)

# --- NEW MASTER LOGIC FUNCTION ---
def generate_reminder_content(reminder_type, base_date, schedule_data):
    """
    Generates the subject, body, and send-worthiness for a given reminder type.
    This is the main logic function for the entire application.
    
    Returns: A dictionary {'subject': str, 'body': str, 'should_send': bool}
    """
    subject, body, day_data = None, None, None
    should_send = False

    if reminder_type == 'morning':
        day_data = get_schedule_for_date(base_date, schedule_data)
        subject = f"Reminder for {base_date.strftime('%A, %b %d')}"
        body = format_full_reminder_body(day_data, "Today")
        if day_data and (day_data.get('milestone') or day_data.get('appointments') or day_data.get('medications')):
            should_send = True

    elif reminder_type == 'evening':
        day_data = get_schedule_for_date(base_date, schedule_data)
        subject = "Today's Medication Checklist"
        body = format_evening_checklist_body(day_data)
        if day_data and day_data.get('medications'):
            should_send = True

    elif reminder_type == 'late_night':
        tomorrow = base_date + timedelta(days=1)
        day_data = get_schedule_for_date(tomorrow, schedule_data)
        subject = f"Heads up for tomorrow ({tomorrow.strftime('%A, %b %d')})"
        body = format_full_reminder_body(day_data, "Tomorrow")
        if day_data and (day_data.get('milestone') or day_data.get('appointments') or day_data.get('medications')):
            should_send = True

    else:
        body = f"ERROR: Unknown reminder_type '{reminder_type}'"
        subject = "Reminder Configuration Error"
        should_send = True # We want to be notified of errors

    return {'subject': subject, 'body': body, 'should_send': should_send}