# ./send_reminder.py
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
import schedule
import time

import reminder_logic

def send_email(subject, body, to_emails):
    # ... (this function is unchanged)
    sender_email = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASSWORD")
    if not sender_email or not password:
        print("ERROR: EMAIL_USER or EMAIL_PASSWORD environment variables not set.")
        return
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_emails)
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to_emails, msg.as_string())
        print(f"Email sent successfully: '{subject}'")
    except Exception as e:
        print(f"Error sending email: {e}")

def run_job(schedule_data, reminder_type):
    """Generic job runner that gets content from the logic module and sends it."""
    print(f"\n{datetime.now()}: Running job for reminder_type: '{reminder_type}'...")
    
    # The base date is always "now" when the job runs.
    base_date = datetime.now().date()
    
    # Get all content from the single source of truth
    content = reminder_logic.generate_reminder_content(reminder_type, base_date, schedule_data)
    
    if content['should_send']:
        recipients = ["4024693827@vtext.com", os.environ.get("EMAIL_USER")]
        send_email(content['subject'], content['body'], recipients)
    else:
        print(f"No items to report for '{reminder_type}' reminder. Skipping email.")


if __name__ == "__main__":
    schedule_data = reminder_logic.load_schedule_data("/app/src/schedule.json")
    if not schedule_data:
        print("FATAL: Could not load schedule data. Exiting.")
        exit(1)

    # Schedule the single, generic job runner with different parameters
    schedule.every().day.at("07:00", "America/Chicago").do(run_job, schedule_data=schedule_data, reminder_type='morning')
    schedule.every().day.at("18:00", "America/Chicago").do(run_job, schedule_data=schedule_data, reminder_type='evening')
    schedule.every().day.at("22:00", "America/Chicago").do(run_job, schedule_data=schedule_data, reminder_type='late_night')

    print("--- Reminder Scheduler Started ---")
    for job in schedule.get_jobs():
        print(f"Scheduled Job: {job}")
    print("----------------------------------")

    while True:
        schedule.run_pending()
        time.sleep(1)