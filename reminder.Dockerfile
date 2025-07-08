# ./reminder.Dockerfile
FROM python:3.9-slim

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PYTHONUNBUFFERED=1

RUN pip install schedule pytz

WORKDIR /app

# COPY both Python files now
COPY reminder_logic.py .
COPY send_reminder.py .
COPY src/schedule.json src/schedule.json

CMD ["python", "send_reminder.py"]