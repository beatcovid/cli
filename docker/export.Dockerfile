FROM python:3.7-alpine

ADD ./ ./app

COPY ./docker/export /etc/periodic/hourly/export
RUN pip3 install -r /app/requirements/pip.txt

WORKDIR /app
ENTRYPOINT ["/app/docker/export-entrypoint.sh"]
