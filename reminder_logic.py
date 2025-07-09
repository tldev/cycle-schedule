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
    """Format medications with emojis and clear visual hierarchy."""
    # Drug information database matching the web app
    drug_info = {
        "Prenatal Vitamins": "💊",
        "Omnitrope": "💉",
        "Norethindrone": "💊",
        "Estradiol": "💊",
        "Clomid": "💊",
        "Follistim": "💉",
        "Menopur": "💉",
        "Ganirelix": "💉",
        "Pregnyl": "💉",
    }
    
    lines = []
    for med in medications:
        name = med.get("name")
        details = med.get("details")
        
        # Get the appropriate emoji from the drug database
        med_emoji = drug_info.get(name, "💊")  # Default to pill if not found
        
        # Use stop sign emoji for last day medications
        if med.get("is_stop", False):
            med_emoji = "🛑"
        
        # Determine prefix based on medication type
        if med.get("is_start", False):
            prefix = "**START:** "
        elif med.get("is_stop", False):
            prefix = "**LAST DAY:** "
        elif med.get("is_trigger", False):
            prefix = "**TRIGGER:** "
        else:
            prefix = ""
        
        # Format with bold name and clear details
        formatted_name = f"**{name.upper()}**"
        lines.append(f"{med_emoji} {prefix}{formatted_name}\n   _{details}_")
    return lines

def format_full_reminder_body(day_data, day_label):
    """Format a complete daily schedule with beautiful visual hierarchy."""
    if not day_data:
        return f"📅 No schedule found for {day_label}."
    
    body_lines = []
    items_found = False
    

    
    # Milestone section
    milestone = day_data.get("milestone")
    if milestone:
        items_found = True
        body_lines.append("🎯 **Milestone**")
        body_lines.append(f"_{milestone}_")
        body_lines.append("")
    
    # Appointments section
    appointments = day_data.get("appointments", [])
    if appointments:
        items_found = True
        body_lines.append("📅 **Events & Appointments**")
        for appt in appointments:
            time = appt.get('time', '')
            what = appt.get('what', '')
            where = appt.get('where', '')
            
            if time and what:
                if where:
                    body_lines.append(f"🕐 **{time}** - {what}\n   📍 {where}")
                else:
                    body_lines.append(f"🕐 **{time}** - {what}")
            else:
                body_lines.append(f"📝 {what}")
        body_lines.append("")
    
    # Medications section
    medications = day_data.get("medications", [])
    if medications:
        items_found = True
        body_lines.append("**MEDICATIONS**")
        body_lines.append("")
        body_lines.extend(_format_medication_lines(medications))
        body_lines.append("")
    
    if not items_found:
        return f"📅 No specific appointments or medications scheduled for {day_label}."
    
    return "\n".join(body_lines)

def format_evening_checklist_body(day_data):
    """Format an evening medication checklist with clear visual structure."""
    if not day_data or not day_data.get("medications"):
        return "✅ No medications to checklist for this evening."
    
    medications = day_data.get("medications", [])
    body_lines = [
        "**Please review each item:**"
    ]
    
    # Drug information database matching the web app
    drug_info = {
        "Prenatal Vitamins": "💊",
        "Omnitrope": "💉",
        "Norethindrone": "💊",
        "Estradiol": "💊",
        "Clomid": "💊",
        "Follistim": "💉",
        "Menopur": "💉",
        "Ganirelix": "💉",
        "Pregnyl": "💉",
    }
    
    # Add medications in the same format as morning messages
    for med in medications:
        name = med.get("name")
        details = med.get("details")
        
        # Get the appropriate emoji from the drug database
        med_emoji = drug_info.get(name, "💊")  # Default to pill if not found
        
        # Use stop sign emoji for last day medications
        if med.get("is_stop", False):
            med_emoji = "🛑"
        
        # Determine prefix based on medication type
        if med.get("is_start", False):
            prefix = "**START:** "
        elif med.get("is_stop", False):
            prefix = "**LAST DAY:** "
        elif med.get("is_trigger", False):
            prefix = "**TRIGGER:** "
        else:
            prefix = ""
        
        # Format with bold name and clear details (same as morning)
        formatted_name = f"**{name.upper()}**"
        body_lines.append(f"{med_emoji} {prefix}{formatted_name}\n   _{details}_")
        body_lines.append("")
    

    
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
        subject = f"🌅 Good Morning! Your Schedule for {base_date.strftime('%a. %-m/%-d')}"
        body = format_full_reminder_body(day_data, "Today")
        if day_data and (day_data.get('milestone') or day_data.get('appointments') or day_data.get('medications')):
            should_send = True

    elif reminder_type == 'evening':
        day_data = get_schedule_for_date(base_date, schedule_data)
        subject = f"🔍 Evening Check-in: {base_date.strftime('%a. %-m/%-d')}"
        body = format_evening_checklist_body(day_data)
        if day_data and day_data.get('medications'):
            should_send = True

    elif reminder_type == 'late_night':
        tomorrow = base_date + timedelta(days=1)
        day_data = get_schedule_for_date(tomorrow, schedule_data)
        subject = f"🌙 Tomorrow's Preview: {tomorrow.strftime('%a. %-m/%-d')}"
        body = format_full_reminder_body(day_data, "Tomorrow")
        if day_data and (day_data.get('milestone') or day_data.get('appointments') or day_data.get('medications')):
            should_send = True

    else:
        body = f"Unknown reminder_type '{reminder_type}'"
        subject = "Reminder Configuration Error"
        should_send = False # We want to be notified of errors

    return {'subject': subject, 'body': body, 'should_send': should_send}