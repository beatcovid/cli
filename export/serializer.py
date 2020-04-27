import csv
import io
import re
from collections.abc import Iterable

from export import logger

__is_number = re.compile(r"^\d+$")
__is_single_number = re.compile(r"^\d$")


def is_iterable(obj):
    return isinstance(obj, Iterable)


def is_number(value):
    if re.match(__is_number, value):
        return True
    return False


def is_number_single(value):
    if re.match(__is_single_number, value):
        return True
    return False


def cast_value_strings(tag):
    """ strips those _0 numbers from the end of values"""
    if type(tag) is str and "_" in tag:
        _, suffix = tag.split("_", 1)
        if is_number_single(suffix):
            return int(suffix)
    return tag


def get_value_label(tag):
    if type(tag) is str and "_" in tag:
        value, suffix = tag.split("_", 1)
        if is_number_single(suffix):
            return value.capitalize()
    return tag


def cast_strings_to_bool(tag):
    if not type(tag) is str:
        return tag

    if tag in ["none", "no"]:
        return False

    if tag in ["yes"]:
        return True

    return tag


def filter_metadata_fields(surveys):
    if is_iterable(surveys):
        surveys = list(surveys)

    return [
        {
            k: v
            for k, v in i.items()
            if not (k.startswith("_") and not k in ["_id", "_submission_time", "_uuid"])
        }
        for i in surveys
    ]


def filter_server_fields(surveys):
    if is_iterable(surveys):
        surveys = list(surveys)

    return [
        {k: v for k, v in i.items() if k not in ["session_id", "server_env"]}
        for i in surveys
    ]


def parse_ua_field(survey):
    if not "user_agent" in survey:
        return survey


def parse_surveys(surveys):
    if is_iterable(surveys):
        surveys = list(surveys)

    if not type(surveys) is list:
        surveys = [surveys]

    return [parse_survey(s) for s in surveys]


def parse_survey(survey):
    """ make more sense of the survey """

    deep_fields = [
        "symptom",
        "activity",
        "worry",
        "userdetail_city",
        "userdetail",
        "feeling",
        "contact",
        "face_contact",
    ]

    survey_out = {}

    for field in survey.keys():
        field_matched = False

        value = cast_value_strings(survey[field])
        value = cast_strings_to_bool(value)

        for parse_field_name in deep_fields:
            if field.startswith(parse_field_name) and not field_matched:

                field_matched = True

                if not parse_field_name in survey_out:
                    survey_out[parse_field_name] = {}

                depth = parse_field_name.count("_") + 1

                if parse_field_name == field:
                    v = "id"
                else:
                    field_splits = field.split("_", depth)
                    v = field_splits[depth]

                survey_out[parse_field_name][v] = value

        if not field_matched:
            survey_out[field] = value

    return survey_out


def get_csv_headers(surveys):
    keys = set()

    for s in surveys:
        keys.update(s.keys())

    first_keys = ["_id", "_uuid", "user_id"]

    remainder_keys = list(sorted(keys.difference(set(first_keys))))

    return first_keys + remainder_keys


def parse_surveys_csv(surveys):
    if is_iterable(surveys):
        surveys = list(surveys)

    if not type(surveys) is list:
        surveys = [surveys]

    data = io.StringIO()
    csv_header = get_csv_headers(surveys)

    writer = csv.DictWriter(data, csv_header)
    writer.writeheader()

    for survey in surveys:
        writer.writerow(survey)

    return data.getvalue()
