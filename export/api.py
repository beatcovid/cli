#!/usr/bin/env python
# coding: utf-8

import json
import os
from urllib.parse import quote_plus

import requests

from export import logger
from export.settings import FORM_ID, get_kobocat_auth, get_kobocat_uri


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


def get_submission_data(
    query={}, form_id=None, limit=None, count=None, sort=None, data_format="json"
):
    """
        Gets submissoin data for a form

        @param formid - kpi asset id
        @param query - query the data as object with kobocat params
    """

    if not form_id:
        form_id = FORM_ID

    if not form_id:
        raise Exception("Require a form_id from somewhere")

    if not data_format in ["csv", "json", "xml", "jsonl"]:
        raise Exception(f"Not a valid format {data_format}")

    _formserver = get_kobocat_uri()
    _authorization = get_kobocat_auth()

    data_endpoint = f"{_formserver}/api/v1/data/{form_id}"
    _headers = {}

    if _authorization:
        _headers["Authorization"] = _authorization

    if data_format in ["json", "jsonl"]:
        _headers["Accept"] = "application/json"

    f = None

    _q = {"format": data_format}

    if query:
        _q["query"] = json.dumps(query)

    if limit:
        _q["limit"] = limit

    if count:
        _q["count"] = count

    if sort:
        _q["sort"] = json.dumps(sort)

    # we do this funky dance because we don't trust requests to encode it correctly
    payload_str = "&".join("%s=%s" % (k, quote_plus(str(v))) for k, v in _q.items())

    logger.debug(f"Fetching {data_endpoint}")
    logger.debug(payload_str)

    try:
        f = requests.get(f"{data_endpoint}?{payload_str}", headers=_headers)
    except Exception as e:
        logger.error(e)
        return None

    if f.status_code in [401, 403]:
        raise Exception(f"Auth error: {f.text}")

    if f.status_code >= 500:
        raise Exception(f"Server error: {f.text}")

    if data_format in ["csv", "xml"]:
        return f.text

    # Decode + parse json
    _resp = None

    try:
        _resp = f.json()
    except Exception as e:
        logger.error("get_data query: %s %s", data_endpoint, payload_str)
        logger.exception(e)
        logger.error("Error parsing response JSON {}".format(e))
        return False

    if not type(_resp) is list:
        _resp = [_resp]

    return _resp
