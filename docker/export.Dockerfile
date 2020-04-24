
# build base
FROM python:3.7-slim as base
RUN apt-get update && apt-get -y install cron
COPY ./docker/export /etc/cron.hourly/export

# build deps
FROM base as build
RUN mkdir /app
WORKDIR /app
ADD ./requirements/pip.txt /app/pip.txt
RUN pip3 install -r /app/pip.txt

# include app
FROM build as app
ADD . /app
ENTRYPOINT ["/app/docker/export-entrypoint.sh"]
