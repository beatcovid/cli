FROM python:3.7-slim as base

# REQUIREMENTS: APT
RUN apt-get update && apt-get -y install cron

FROM base as build

WORKDIR /app
ADD ./app/requirements/pip.txt /app/requirements/pip.txt

COPY ./docker/export /etc/cron.hourly/export

# REQUIREMENTS: PIP
RUN pip3 install -r /app/requirements/pip.txt

FROM build as app

ADD . /app

ENTRYPOINT ["/app/docker/export-entrypoint.sh"]
