from export.serializer import (
    filter_metadata_fields,
    filter_server_fields,
    parse_surveys,
    parse_surveys_csv,
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
