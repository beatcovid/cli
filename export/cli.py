import argparse
import logging
from pprint import pprint

from export import logger
from export.api import get_submission_data
from export.serializer import parse_surveys

OUTPUT_FORMATS = ["csv", "json", "jsonl"]


def get_parser():
    parser = argparse.ArgumentParser(prog="beatcovid", description="beatcovid exporter.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't run database imports"
    )
    parser.add_argument("--debug", action="store_true", help="Debug output")
    parser.add_argument(
        "-n", "--no-geocode", action="store_true", help="Don't do geocode lookups"
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty print output")
    parser.add_argument(
        "--limit", type=int, default=50, help="Limit number of records processed"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="json",
        choices=OUTPUT_FORMATS,
        help="Format of export (csv, json, jsonl)",
    )

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        responses = get_submission_data(limit=args.limit)

        surveys = parse_surveys(responses)

        if args.pretty:
            pprint(surveys)
        else:
            print(surveys)

    except KeyboardInterrupt as e:
        logger.error("User stopped process")
    except Exception as e:
        logger.exception(e)
