#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import json
import pandas as pd
import boto3
import os

import logging
from settings import FORM_ID, KOBOCAT_API_CREDENTIALS, KOBOCAT_API_URI
from settings import ACCESS_KEY, SECRET_KEY, BUCKET_NAME
import requests

logging.basicConfig(level=logging.INFO,)
logger = logging.getLogger("beatcovid.exporter")


def get_json(since):
    """"
    since: entries newer than this date will be returned
    format of since is defined by last_fmt

    """
    # date_filter_inner = f'
    data_endpoint = f"{KOBOCAT_API_URI}api/v1/data/{FORM_ID}"
    _headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {KOBOCAT_API_CREDENTIALS}",
    }
    query_inner = f'"$gt":"{since}"'
    _query = '{"_submission_time": {' + query_inner + "}}"
    payload = {"query": _query}

    logger.info(f"Fetching {data_endpoint}")
    logger.info(payload)

    try:
        f = requests.get(data_endpoint, headers=_headers, params=payload)
    except Exception as e:
        logger.error(e)
        return None

    return_obj = None

    try:
        return_obj = f.json()
    except Exception as e:
        logger.exception(e)

    return return_obj


def get_dataframe(json_dict):
    """
    convert a json string to pandas dataframe
    """
    dataframe = pd.read_json(json.dumps(json_dict))
    return dataframe


last_fmt = "%Y-%m-%dT%H:%M:%S+00:00"
now = datetime.now()
now_str = now.strftime(last_fmt)

last_dump_fn = "lastdumped_v1_1"

client = boto3.client("s3")
lastdump_meta = client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=last_dump_fn)

last = "from_start"
if lastdump_meta["KeyCount"] > 0:
    client.download_file(Bucket=BUCKET_NAME, Key=last_dump_fn, Filename=last_dump_fn)
    with open(last_dump_fn) as fh:
        last = fh.read().strip()
        start = datetime.strptime(last, last_fmt)
        logger.info(f"dumping from {start}")
else:
    start = datetime.strptime("2000-01-01T00:00:01+00:00", last_fmt)

output_fn_local = "export_v1_1.csv"
json_d = get_json(start)

if len(json_d) > 0:
    dataframe = get_dataframe(json_d)
    dataframe.to_csv(output_fn_local, index=False)

    output_fn_remote = "dump_" + last + ".csv"
    with open(output_fn_local, "rb") as fh:
        client.upload_fileobj(fh, BUCKET_NAME, output_fn_remote)
else:
    logger.info("Nothing new to export")

with open(last_dump_fn, "w") as fh:
    fh.write(now_str)
client.upload_file(last_dump_fn, BUCKET_NAME, last_dump_fn)
