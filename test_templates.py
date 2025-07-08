# ./test_templates.py
import sys
from datetime import datetime
import reminder_logic

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_templates.py <YYYY-MM-DD>")
        print("Example: python test_templates.py 2025-07-11")
        return

    try:
        base_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    schedule_data = reminder_logic.load_schedule_data("./src/schedule.json")
    if not schedule_data:
        return
        
    print("\n" + "="*50)
    print(f"  GENERATING TEMPLATES FOR DATE: {base_date.strftime('%A, %Y-%m-%d')}")
    print("="*50 + "\n")
    
    reminder_types = {
        'morning':    "Morning Template (7 AM)",
        'evening':    "Evening Checklist (6 PM)",
        'late_night': "Late Night Template (10 PM)"
    }
    for type_key, title in reminder_types.items():
        # Get all content from the single source of truth
        content = reminder_logic.generate_reminder_content(type_key, base_date, schedule_data)
        
        print(f"--- {title} ---")
        print(f"Subject: {content['subject']}")
        print("Body:\n" + content['body'])
        print("-"*(len(content['subject']) + 9) + "\n")


if __name__ == "__main__":
    main()