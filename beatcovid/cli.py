import argparse
import logging
from pprint import pprint

from smart_open import open

from beatcovid import logger
from beatcovid.api import get_submission_data, get_submissions_since_date

from .controllers import csv_export, json_export, jsonl_export

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
    parser.add_argument(
        "destination", metavar="destination", type=str, nargs="?", help="save to file",
    )

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug(args)
    logger.debug("Outputting in {args.format}")

    try:
        responses = get_submission_data(limit=args.limit)
        logging.debug(f"Have {len(responses)} surveys")

        # get the data in the correct format
        if args.format == "csv":
            surveys = csv_export(responses)

        elif args.format == "json":
            surveys = json_export(responses)

        elif args.format == "jsonl":
            surveys = jsonl_export(responses)

        else:
            raise Exception("Format not supported")

        # print to screen or write to file
        if not args.destination:

            if not type(surveys) is list:
                surveys = str(surveys.getvalue())

            if args.pretty:
                pprint(surveys)
            else:
                print(surveys)

        else:
            logging.info(f"Writing to file {args.destination}")

            with open(args.destination, "wb") as fh:
                fh.write(surveys.getbuffer())

    except KeyboardInterrupt as e:
        logger.error("User stopped process")
    except Exception as e:
        logger.exception(e)
