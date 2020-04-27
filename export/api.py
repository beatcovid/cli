#!/usr/bin/env python
# coding: utf-8

import json
import os

import requests

from export import logger

from .settings import FORM_ID, KOBOCAT_API_CREDENTIALS, KOBOCAT_API_URI


def get_surveys(since=None):
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
