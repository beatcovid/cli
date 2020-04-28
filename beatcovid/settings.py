import os
from base64 import b64encode

from dotenv import load_dotenv

"""
The ACCESS_KEY SECRET_KEY are credentials AWS credentials with write privileges
to BUCKET_NAME.

FORM_ID is a number id of the kobo form to export data from, hosted at
KOBOCAT_API_URI with authorization provided by KOBOCAT_API_CREDENTIALS
"""

load_dotenv()

BUCKET_NAME = os.environ.get("S3_BUCKET", default=None)

REDIS_HOST = os.environ.get("REDIS_HOST", default="127.0.0.10")

FORM_ID = os.environ.get("FORM_ID", default="3")

KOBOCAT_API_URI = os.environ.get("KOBOCAT_API", default="https://kc.beatcovid19now.org/")

# Auth
KOBOCAT_API_USERNAME = os.environ.get("KOBOCAT_API_USERNAME", default=None)
KOBOCAT_API_PASSWORD = os.environ.get("KOBOCAT_API_PASSWORD", default=None)

# -- or --
KOBOCAT_API_TOKEN = os.environ.get("KOBOCAT_API_TOKEN", default=None)

# -- or --

KOBOCAT_API_CREDENTIALS = os.environ.get("KOBOCAT_CREDENTIALS", default=None)


def get_kobocat_uri():
    if KOBOCAT_API_URI:
        _uri = KOBOCAT_API_URI

        # normalize the slashes
        if _uri.endswith("/"):
            _uri = _uri[:-1]

        return _uri
    raise Exception("KOBOCAT_API_URI is not set")


def get_kobocat_auth():
    if KOBOCAT_API_CREDENTIALS:
        return f"Basic {KOBOCAT_API_CREDENTIALS}"

    if KOBOCAT_API_TOKEN:
        return f"Token {KOBOCAT_API_TOKEN}"

    if KOBOCAT_API_USERNAME:
        _encoded_auth = b64encode(f"{KOBOCAT_API_USERNAME}:{KOBOCAT_API_PASSWORD}")
        return f"Basic {_encoded_auth}"

    # fallback onto .netrc and let requests handle it
    return None
