"""
    saves exports to cloud

    currently supports AWS S3 buckets
"""
import json
from datetime import datetime

import boto3
import pandas as pd

from beatcovid import logger
from beatcovid.api import get_surveys
from beatcovid.settings import BUCKET_NAME

client = boto3.client("s3")


def get_dataframe(json_dict):
    """
    convert a json string to pandas dataframe
    """
    dataframe = pd.read_json(json.dumps(json_dict))
    return dataframe


def s3_save_full():
    pass


def s3_save_diff():
    """
        save a diff of data since last write
    """
    last_fmt = "%Y-%m-%dT%H:%M:%S+00:00"
    now = datetime.now()
    now_str = now.strftime(last_fmt)

    last_dump_fn = "lastdumped_v1_1"

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
    json_d = get_surveys(start)

    if len(json_d) > 0:
        logger.info("Writing {} new entries".format(len(json_d)))

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
