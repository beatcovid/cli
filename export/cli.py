import argparse
import logging
from pprint import pprint

from export import logger
from export.api import get_submission_data, get_submissions_since_date
from export.serializer import parse_surveys, parse_surveys_csv

from .controllers import csv_export

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
        "-f",
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

    logging.debug("Outputting in {args.format}")

    try:
        responses = get_submissions_since_date(hours=1)

        if args.format == "csv":
            logging.debug(f"Have {len(responses)} surveys")
            surveys = csv_export(responses)
            print(surveys)

        elif args.format is "json":
            surveys = parse_surveys(responses)

            if args.pretty:
                pprint(surveys)
            else:
                print(surveys)

        else:
            raise Exception("Format not supported")

    except KeyboardInterrupt as e:
        logger.error("User stopped process")
    except Exception as e:
        logger.exception(e)
