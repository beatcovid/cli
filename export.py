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

logging.basicConfig(level=logging.DEBUG,)
logger = logging.getLogger("beatcovid.exporter")

def get_json():
    """"
    @TODO This needs to accept a datetime, which is the date from which onwards the data is to be exported

    """
    data_endpoint = f"{KOBOCAT_API_URI}api/v1/data/{FORM_ID}"
    _headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {KOBOCAT_API_CREDENTIALS}",
        }
    try:
        f = requests.get(data_endpoint, headers=_headers)
    except Exception as e:
        logger.error(e)
        return None
    return f.json()

def get_dataframe(json_dict):
    """
    convert a json string to pandas dataframe
    """
    dataframe = pd.read_json(json.dumps(json_dict))
    return dataframe

output_fn_local = "export_v1_1.csv"
json_d = get_json()
dataframe = get_dataframe(json_d)
dataframe.to_csv(output_fn_local, index=False)

last_fmt = "%Y-%m-%d-%H:%M:%S"
now = datetime.now()
now_str = now.strftime(last_fmt)

last_dump_fn = "lastdumped_v1_1"

client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
lastdump_meta = client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=last_dump_fn)

last = "from_start"
if lastdump_meta['KeyCount'] > 0:
    client.download_file(Bucket=BUCKET_NAME, Key=last_dump_fn,
                         Filename=last_dump_fn)
    with open(last_dump_fn) as fh:
        last = fh.read().strip()
        start = datetime.strptime(last, last_fmt)
        print("dumping from", start)
else:
    start = datetime.strptime("2000-01-01-00:00:01", last_fmt)

output_fn_remote = "dump_" + last + ".csv"
with open(output_fn_local, "rb") as fh:
    client.upload_fileobj(fh, BUCKET_NAME, output_fn_remote)

with open(last_dump_fn, "w") as fh:
    fh.write(now_str)
client.upload_file(last_dump_fn, BUCKET_NAME, last_dump_fn)
