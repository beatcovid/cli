import argparse
import logging
from pprint import pprint

from export import logger
from export.api import get_submission_data
from export.serializer import parse_surveys


def get_parser():
    parser = argparse.ArgumentParser(prog="beatcovid", description="beatcovid exporter.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't run database imports"
    )
    parser.add_argument("--debug", action="store_true", help="Debug output")
    parser.add_argument(
        "-n", "--no-geocode", action="store_true", help="Don't do geocode lookups"
    )
    parser.add_argument(
        "--limit", type=int, default=0, help="Limit number of records processed"
    )
    parser.add_argument(
        "--format", type=str, default="json", help="Format of export (csv, json, jsonl)"
    )

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        responses = get_submission_data(limit=args.limit)

        pprint(parse_surveys(responses))

        # for r in responses:
        # pprint(r)
    except KeyboardInterrupt as e:
        logger.error("User stopped process")
    except Exception as e:
        logger.exception(e)
