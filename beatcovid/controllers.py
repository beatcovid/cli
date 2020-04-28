from beatcovid.serializer import (
    filter_metadata_fields,
    filter_server_fields,
    parse_surveys,
    parse_surveys_csv,
    parse_surveys_jsonl,
)


def map_many(iterable, function, *other):
    if other:
        return map_many(map(function, iterable), *other)
    return map(function, iterable)


def csv_export(surveys):
    # surveys = map(filter_metadata_fields, surveys)
    surveys = filter_metadata_fields(surveys)
    surveys = filter_server_fields(surveys)

    return parse_surveys_csv(surveys)


def json_export(surveys):
    # surveys = map(filter_metadata_fields, surveys)
    surveys = filter_metadata_fields(surveys)
    surveys = filter_server_fields(surveys)

    return parse_surveys(surveys)


def jsonl_export(surveys):
    # surveys = map(filter_metadata_fields, surveys)
    surveys = json_export(surveys)

    return parse_surveys_jsonl(surveys)
