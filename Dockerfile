FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN apt-get update && apt-get install cron -y
ADD crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

RUN mkdir /app
COPY ./app /app

ENTRYPOINT ["cron", "-f"]





