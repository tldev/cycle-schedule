# ./send_reminder.py
import os
from datetime import datetime
import schedule
import time
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
import argparse

import reminder_logic

async def send_telegram_message(subject, body):
    """Sends a message to multiple Telegram users or groups."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_ids_str = os.environ.get("TELEGRAM_CHAT_IDS")

    if not bot_token or not chat_ids_str:
        print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_IDS environment variables not set.")
        return

    # Parse multiple chat IDs (comma-separated)
    chat_ids = [chat_id.strip() for chat_id in chat_ids_str.split(",")]
    
    try:
        bot = Bot(token=bot_token)
        for chat_id in chat_ids:
            await bot.send_message(chat_id=chat_id, text=f"*{subject}*\n\n{body}", parse_mode=ParseMode.MARKDOWN)
            print(f"Telegram message sent successfully to {chat_id}: '{subject}'")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def run_job_sync(schedule_data, reminder_type, base_date=None):
    """Sync wrapper for the async job runner, for schedule library compatibility."""
    asyncio.run(run_job(schedule_data, reminder_type, base_date))

async def run_job(schedule_data, reminder_type, base_date=None):
    """Generic job runner that gets content from the logic module and sends it."""
    print(f"\n{datetime.now()}: Running job for reminder_type: '{reminder_type}'...")
    
    # The base date is always "now" when the job runs.
    if not base_date:
        base_date = datetime.now().date()
    
    # Get all content from the single source of truth
    content = reminder_logic.generate_reminder_content(reminder_type, base_date, schedule_data)
    
    if content['should_send']:
        await send_telegram_message(content['subject'], content['body'])
    else:
        print(f"No items to report for '{reminder_type}' reminder. Skipping notification.")


if __name__ == "__main__":
    schedule_data = reminder_logic.load_schedule_data("/app/src/schedule.json")
    if not schedule_data:
        print("FATAL: Could not load schedule data. Exiting.")
        exit(1)

    reminder_date = os.environ.get("REMINDER_DATE")
    print(f"Reminder date: {reminder_date}")
    if reminder_date:
        try:
            base_date = datetime.strptime(reminder_date, "%Y-%m-%d").date()
            print(f"--- Running for specific date: {base_date} ---")
            asyncio.run(run_job(schedule_data, 'morning', base_date))
            asyncio.run(run_job(schedule_data, 'evening', base_date))
            asyncio.run(run_job(schedule_data, 'late_night', base_date))
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
    else:
        # Schedule the single, generic job runner with different parameters
        schedule.every().day.at("07:00", "America/Chicago").do(run_job_sync, schedule_data=schedule_data, reminder_type='morning')
        schedule.every().day.at("18:00", "America/Chicago").do(run_job_sync, schedule_data=schedule_data, reminder_type='evening')
        schedule.every().day.at("22:00", "America/Chicago").do(run_job_sync, schedule_data=schedule_data, reminder_type='late_night')

        print("--- Reminder Scheduler Started ---")
        for job in schedule.get_jobs():
            print(f"Scheduled Job: {job}")
        print("----------------------------------")

        while True:
            schedule.run_pending()
            time.sleep(1)
