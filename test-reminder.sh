#!/bin/sh
# This script will manually trigger the reminder email.
docker-compose run --rm reminder python /app/send_reminder.py
