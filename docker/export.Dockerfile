FROM python:3.7-slim

ADD ./ ./app

COPY ./docker/export /etc/cron.hourly/export

# REQUIREMENTS: APT
RUN apt-get update && apt-get -y install cron

# REQUIREMENTS: PIP
RUN pip3 install -r /app/requirements/pip.txt

WORKDIR /app
ENTRYPOINT ["/app/docker/export-entrypoint.sh"]
